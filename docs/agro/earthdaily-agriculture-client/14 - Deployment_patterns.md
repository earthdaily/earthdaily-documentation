---
title: Deployment patterns
description: Two supported ways to operationalise an EarthDaily Agriculture extraction in production — GitHub Actions cron and a Docker container — with cost guidance and a migration path between them.
#icon: material/rocket-launch-outline
keywords:
  - deployment
  - github actions
  - docker
  - ecs fargate
  - cloud run
  - terraform
  - cron
  - automation
---

# Deployment patterns

Once an extraction works in a notebook, you'll typically want it to run on its own — daily, hourly, or on demand — without a human in front of a kernel. Two patterns are supported, and most projects start on one and graduate to the other only when the first hits a hard limit.

- **Pattern A — GitHub Actions cron.** A scheduled workflow runs a headless Python entrypoint and ships the output to S3. Zero infrastructure to provision; one workflow file and a handful of secrets.
- **Pattern B — Docker container.** A single image whose entrypoint is the extraction CLI. The same image runs locally, on ECS / Cloud Run jobs, in Argo, or wherever else you schedule containers.

They're complementary, not competing. Pattern A is the right starting point for the majority of single-step daily / weekly extractions. Pattern B is the right destination for runs that exceed Actions' time budget, need private network access, or fan out across many shards.

---

## Picking a pattern

| Question                                                   | If "yes" use…                       |
| ---------------------------------------------------------- | ----------------------------------- |
| Daily or weekly cadence?                                   | Pattern A                           |
| Single CSV / parquet / report per run?                     | Pattern A                           |
| Run finishes in under ~4 hours?                            | Pattern A                           |
| Run state is purely idempotent given a `--prefix`?         | Pattern A                           |
| Run takes longer than ~4 hours?                            | Pattern B                           |
| Fan-out across hundreds of shards?                         | Pattern B                           |
| Needs a private VPC / on-prem data source?                 | Pattern B                           |
| Sub-hourly cadence or event-triggered?                     | Pattern B                           |
| Multi-step orchestration (DAG retries, backfills)?         | Pattern B + Argo / Step Functions   |

If none of A's limits bite, **start with A**. It's dramatically less operational surface area: one repo, one workflow file, no image registry, no IAM role to attach. The escape hatch (Pattern B) shares the same Python entrypoint, so when you outgrow A the move is mechanical.

---

## Pattern A — GitHub Actions cron

A scheduled GitHub Actions workflow installs the package, runs a headless Python entrypoint, captures the output path, and uploads to S3 plus as a workflow artifact.

### Shape

```
┌─────────────────────────┐
│ GitHub Actions cron     │   triggers daily
└──────────┬──────────────┘
           ▼
┌─────────────────────────┐
│ python -m app.run_pipeline
│   --prefix run_YYYYMMDD │   one CLI, one stdout contract
└──────────┬──────────────┘
           │  prints REPORT_PATH=<abs path> on its last line
           ▼
┌─────────────────────────┐
│ Workflow scrapes path,  │
│ uploads to:             │
│   • workflow artifact   │   (14-day retention, debugging)
│   • S3 bucket           │   (final delivery)
└─────────────────────────┘
```

### What lives in your extraction repo

| Component                                  | Purpose                                                                                                  |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `app/run_pipeline.py`                      | Headless entrypoint. Reads workflow config, drives `WorkflowManager`, prints `REPORT_PATH=…` last.       |
| `configuration/*.yml`                      | Workflow DAG, entity source, transforms. Same file drives the notebook and the cron run.                  |
| `requirements.txt`                         | Pins `earthdaily-agriculture==X.Y.Z` (and any project-specific dependencies). CI installs from this.                |
| `.github/workflows/automated_extraction.yml` | Cron schedule, secrets, post-run uploads.                                                                |
| `docs/DEPLOYMENT.md` (optional)            | Per-project secret list, schedule rationale, troubleshooting.                                            |

### The stdout contract

`run_pipeline.py` prints exactly one line of the form:

```
REPORT_PATH=/absolute/path/to/final-artifact.csv
```

as its last meaningful stdout line. The workflow scrapes it:

```yaml
python -m app.run_pipeline --prefix "run_$(date -u +%Y%m%d)" $ARGS | tee run.log
REPORT=$(grep '^REPORT_PATH=' run.log | tail -1 | cut -d= -f2-)
[ -z "$REPORT" ] && { echo "no REPORT_PATH"; exit 1; }
echo "report_path=$REPORT" >> "$GITHUB_OUTPUT"
```

Why this stays clean:

- Downstream steps (S3, FTP, Slack, artifact upload) are decoupled from the Python entrypoint.
- No JSON parsing in shell. No env-file gymnastics. No temp-directory conventions to memorise.
- Trivially testable: `python -m app.run_pipeline --limit 1 | tail -1` is the whole smoke test.

For pipelines that emit multiple terminal artifacts, generalise to a tiny manifest — e.g. `REPORT_MANIFEST=<json path>` — and let the workflow loop. Don't parse arbitrary log lines.

### Installing the package in CI

```bash
pip install --no-cache-dir -r requirements.txt
```

with `requirements.txt` pinning the exact version:

```
earthdaily-agriculture==X.Y.Z
```

Pin the version, don't float. CI then uses the same package version a developer tested locally, and upgrading is a one-line PR with a clean diff. The same applies to all transitive dependencies — `pip-compile` or `uv pip compile` produces a lock file that makes the run reproducible.

### Workflow skeleton

Reusable as-is once you substitute the secret names and the CLI invocation:

```yaml
name: <extraction> daily extraction

on:
  schedule:
    - cron: "0 6 * * *"        # 06:00 UTC — avoid 0/6/12 UTC busy hours
  workflow_dispatch:
    inputs:
      limit:
        description: "Optional smoke-test limit"
        required: false
        default: ""

permissions:
  contents: read
  id-token: write              # only needed when you switch to AWS OIDC

jobs:
  run:
    runs-on: ubuntu-latest
    timeout-minutes: 300
    env:
      ENVIRONMENT: prod
      PROD_API_CLIENT_ID:     ${{ secrets.PROD_API_CLIENT_ID }}
      PROD_API_CLIENT_SECRET: ${{ secrets.PROD_API_CLIENT_SECRET }}
      PROD_API_USERNAME:      ${{ secrets.PROD_API_USERNAME }}
      PROD_API_PASSWORD:      ${{ secrets.PROD_API_PASSWORD }}
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"
      - run: pip install --no-cache-dir -r requirements.txt
      - id: run
        run: |
          set -o pipefail
          ARGS=""
          [ -n "${{ github.event.inputs.limit }}" ] && ARGS="--limit ${{ github.event.inputs.limit }}"
          python -m app.run_pipeline --prefix "run_$(date -u +%Y%m%d)" $ARGS | tee run.log
          REPORT=$(grep '^REPORT_PATH=' run.log | tail -1 | cut -d= -f2-)
          [ -z "$REPORT" ] && { echo "no REPORT_PATH"; exit 1; }
          echo "report_path=$REPORT" >> "$GITHUB_OUTPUT"
          echo "report_basename=$(basename "$REPORT")" >> "$GITHUB_OUTPUT"
      - if: always()
        uses: actions/upload-artifact@v4
        with:
          name: <extraction>-${{ github.run_id }}
          path: |
            results/*.csv
            logs/
          retention-days: 14
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id:     ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region:            ${{ secrets.AWS_REGION }}
      - env:
          S3_BUCKET: ${{ secrets.S3_BUCKET }}
          S3_PREFIX: ${{ secrets.S3_PREFIX }}
        run: |
          DATE=$(date -u +%Y-%m-%d)
          aws s3 cp "${{ steps.run.outputs.report_path }}" \
            "s3://${S3_BUCKET}/${S3_PREFIX}/${DATE}/${{ steps.run.outputs.report_basename }}"
```

Three small details that matter:

- **`if: always()`** on the artifact upload so a failed run still gives you the partial CSVs and log tree.
- **`timeout-minutes: 300`** is the GitHub hosted-runner maximum. Pick something lower if your run has a known upper bound — fast failure beats a stuck cron.
- **`set -o pipefail`** is essential: without it, `tee run.log` swallows a non-zero exit from the Python entrypoint and the workflow goes green on a silently-broken run.

### Bringing it online

Each step below has a clear "done" signal so you can hand off to someone else mid-flight.

1. **Add the API secrets** under `Settings → Secrets and variables → Actions → New repository secret`:
   - `PROD_API_CLIENT_ID`
   - `PROD_API_CLIENT_SECRET`
   - `PROD_API_USERNAME`
   - `PROD_API_PASSWORD`

   Add `PREPROD_*` mirrors only if your project flips between environments. **Done when:** all four names appear in the Secrets list.

2. **Smoke-test via `workflow_dispatch`.** From the Actions tab, find the workflow, click **Run workflow**, set `limit=5`, and watch it. **Done when:** the run goes green, the artifact tab shows `<project>-<run-id>` with `results/*.csv` and `logs/`, and the log ends with a `REPORT_PATH=…` line.

3. **Add the S3 secrets** (same Settings page):
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`
   - `AWS_REGION` (e.g. `us-east-1`)
   - `S3_BUCKET` (name only, no `s3://`)
   - `S3_PREFIX` (project-scoped, e.g. `<project>/reports`)

   **Done when:** all five names appear in the Secrets list.

4. **Enable the S3 delivery step.** Uncomment the AWS-configure and `aws s3 cp` blocks in the workflow file. Commit. **Done when:** a re-run of `workflow_dispatch` shows the final CSV at `s3://<bucket>/<prefix>/<date>/<filename>`.

5. **Add failure notifications** (recommended — silent cron failures are worse than no cron). Create a Slack app with an Incoming Webhook URL, add it as `SLACK_WEBHOOK_URL`, and add a final notification step gated on `if: failure()`. **Done when:** a deliberately failing run posts a message to your channel.

6. **Enable the cron.** Uncomment the `schedule:` block at the top of the workflow file. Tune the cron expression to your cadence + timezone (see *Schedule choices* below). Commit and push to the **default branch** — schedules don't fire from feature branches.

7. **Wait for the first cron-driven run.** It's the real proof. **Done when:** Actions shows a scheduled run that didn't come from `workflow_dispatch`, and the artifact / S3 file are present.

After step 6 the cron is live. After step 7 the deployment is real.

### Secrets

Two tiers — keep them named consistently across your projects:

| Tier  | Secrets                                                                                                                |
| ----- | ---------------------------------------------------------------------------------------------------------------------- |
| API   | `PROD_API_CLIENT_ID`, `PROD_API_CLIENT_SECRET`, `PROD_API_USERNAME`, `PROD_API_PASSWORD` (`PREPROD_*` mirrors if needed) |
| S3    | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, `S3_BUCKET` (no `s3://`), `S3_PREFIX` (project-scoped)        |

Move to OIDC (`aws-actions/configure-aws-credentials@v4` with `role-to-assume`) once key rotation becomes a compliance question or you're operationalising more than ~3 extractions.

### Schedule choices

- **`0 6 * * *`** (06:00 UTC) is a sensible default. Early enough for a US-grower morning report, late enough to dodge the GitHub scheduler's busy windows. Avoid `0 0 * * *` specifically — the worst delays cluster on hour-boundary schedules at 00/06/12 UTC.
- Scheduled runs can be delayed by up to 10 minutes under load. Don't chain extractions back-to-back; leave at least 30 minutes of slack or use `workflow_run` triggers.
- The first scheduled run only fires once the workflow file is **on the default branch**. Pushing it to a feature branch and waiting for cron is a common first-day mistake.

### What this pattern deliberately does not do

- **No orchestrator (Airflow, Prefect, Dagster).** For a daily single-step extraction, GitHub Actions cron + a Python CLI is dramatically less operational surface area. Reach for an orchestrator when you have inter-DAG dependencies, backfills, or SLA-driven retries.
- **No separate prod config.** The same `configuration/*.yml` drives both the notebook and the cron. Divergence is the leading cause of "works locally, fails in prod" — don't introduce it.
- **No retries inside the entrypoint.** Cron fires again tomorrow. Alerting + manual rerun via `workflow_dispatch` is the answer, not silent retry logic that masks signal.

---

## Pattern B — Docker container

A container image whose entrypoint is the extraction CLI. The same image runs everywhere: manual `docker run`, ECS scheduled tasks, Cloud Run jobs, Argo Workflows, GitHub Actions runners.

### When to use

- Run exceeds GitHub Actions' ~4-hour reliable budget (5-hour ceiling).
- Need a private VPC / VPN-only data source.
- Want fan-out across hundreds of shards.
- Multi-step orchestration with retries / DAG semantics.
- Already on Kubernetes / ECS and prefer to avoid GitHub Actions for production traffic.

### Dockerfile (multi-stage)

Typical image sizes: single-stage ~1.2 GB, multi-stage ~600 MB.

```dockerfile
# ---- Stage 1: build wheel ----
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml requirements.txt ./
COPY src/ ./src/
RUN pip install --no-cache-dir build && python -m build --wheel

# ---- Stage 2: runtime ----
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgdal32 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

RUN useradd --create-home --shell /bin/bash earthdaily-agriculture
USER earthdaily-agriculture
WORKDIR /home/earthdaily-agriculture

ENTRYPOINT ["earthdaily-agriculture"]
CMD ["--help"]
```

If you don't have project-specific code beyond the workflow config, you can drop the build stage and just `pip install earthdaily-agriculture==X.Y.Z` directly in the runtime stage.

### `.dockerignore`

Without this, the image balloons and may leak credentials into layers:

```
# Credentials — NEVER ship these
.env
src/.env
**/.env

# Local workspace output
inputs/
results/
partials/
logs/
cache/

# Build artifacts
build/
dist/
*.egg-info/

# Notebooks & dev material
notebooks/
*.ipynb
*.ipynb_checkpoints

# VCS & IDE
.git/
.github/
.vscode/
.idea/

# Python cruft
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
```

### Credentials

| Option                          | When                                                                                                                                          |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Static access keys (env vars)   | Local development, quick proof-of-concept. Long-lived — rotate frequently.                                                                     |
| IAM role                        | Recommended for cloud. ECS task role / EKS IRSA / Cloud Run Workload Identity / EC2 instance profile. Omit the `AWS_*_KEY` env vars; `boto3` finds the role automatically. |
| Secrets manager                 | Inject from AWS Secrets Manager / Parameter Store / Vault at container start. Orchestrator work, not image work.                              |

### S3 routing with `EDAGRO_OUTPUT_PREFIX`

Set this env var to route all writes (results / partials / cache) under a single S3 prefix:

```bash
docker run --rm \
  -e ENVIRONMENT=prod \
  -e EDAGRO_OUTPUT_PREFIX=s3://my-bucket/runs/$(date -u +%Y-%m-%d)/<workflow> \
  -e EDAGRO_LOG_CONSOLE_ONLY=1 \
  --env-file .env.prod \
  earthdaily-agriculture:latest \
  run-extractor --extractor CoverageExtractor --setup '{"start_date":"2025-01-01"}'
```

`WorkflowManager` reads `EDAGRO_OUTPUT_PREFIX` at construction time and sets:

- `output_result_dir = <prefix>/results`
- `partial_result_dir = <prefix>/partials`
- `cache_dir = <prefix>/cache` (which then auto-disables the cache because it's a remote path; see doc 13 §5)

Constructor kwargs take precedence if you pass them explicitly, so the env var is a default that orchestrators set and `docker run --rm -e EDAGRO_OUTPUT_PREFIX=…` becomes the canonical invocation.

For notebooks that need an explicit assertion rather than relying on the env var (typical when a developer's `.env` might shadow the orchestrator setting), pass `storage="s3"` to `WorkflowManager` — it raises if neither `EDAGRO_OUTPUT_PREFIX` nor an explicit remote kwarg is supplied. See [`13 - Cloud_storage_principles_and_usage.md`](13%20-%20Cloud_storage_principles_and_usage.md) Recipe B.

`EDAGRO_LOG_CONSOLE_ONLY=1` skips the loguru file sink so the container's stdout is the log stream.

### Endpoint override for MinIO / LocalStack

```bash
-e AWS_ENDPOINT_URL=https://minio.internal:9000
-e AWS_S3_FORCE_PATH_STYLE=true
```

Both are honoured by `boto3` and therefore by `fsspec`.

### Heartbeat / healthcheck

For long bulk runs, emit a heartbeat to stdout every N seconds or every K entities processed so `docker logs -f` and orchestrators can tell the process is alive:

```python
if processed % 100 == 0:
    self.logger.info(f"[heartbeat] {processed}/{total} entities done")
```

### Image lifecycle

- **Tag with the git SHA** — `earthdaily-agriculture:$(git rev-parse --short HEAD)` — so every run is traceable to source.
- **Also tag `latest`** on `main` for convenience; never rely on `latest` in production runs.
- **Publish to a private registry** — ECR, Artifact Registry, GHCR. Never a public one for production images.
- **Scan for vulnerabilities** — `trivy image earthdaily-agriculture:latest` or your registry's built-in scanner.

### Provisioning the AWS infrastructure with Terraform

A minimum-viable AWS setup to actually run a Pattern B extraction on a schedule. ECS Fargate, triggered by EventBridge cron.

- **In scope:** ECR repo + lifecycle, CloudWatch log group, ECS Fargate cluster + task definition + task/execution IAM roles, EventBridge schedule + invoker role, Secrets Manager wiring for API credentials.
- **Out of scope (you bring):** an S3 bucket for outputs (we just reference it), a VPC with at least one private subnet (we use the default VPC by default), an OIDC trust policy for GitHub Actions if you also want to deploy from CI, state-backend wiring.

If you're on GCP or Azure, the same shape translates — the resources change but the shopping list (registry / log group / job spec / IAM / schedule + invoker / secrets) doesn't.

#### Layout

Drop these three files into `terraform/`. They reference `var.s3_bucket` (your existing outputs bucket) and `var.image_tag` (the image you pushed to ECR earlier).

**`terraform/main.tf`**

```hcl
terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }

  # State backend — configure for your org. The block below is a stub;
  # replace with your team's bucket / DynamoDB table for state locking.
  # backend "s3" {
  #   bucket         = "<your-tfstate-bucket>"
  #   key            = "earthdaily-agriculture/${var.project_name}/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "<your-tfstate-lock-table>"
  # }
}

provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "default" {
  default = true
}
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

locals {
  name = "earthdaily-agriculture-${var.project_name}"
}

# --- Container registry --------------------------------------------------
resource "aws_ecr_repository" "this" {
  name                 = local.name
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration { scan_on_push = true }
}

resource "aws_ecr_lifecycle_policy" "this" {
  repository = aws_ecr_repository.this.name
  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Keep last 10 images"
      selection = {
        tagStatus   = "any"
        countType   = "imageCountMoreThan"
        countNumber = 10
      }
      action = { type = "expire" }
    }]
  })
}

# --- Logs ----------------------------------------------------------------
resource "aws_cloudwatch_log_group" "task" {
  name              = "/ecs/${local.name}"
  retention_in_days = 30
}

# --- Secrets (populate values out-of-band — keeps them out of state) -----
# After `terraform apply`, push the four API credentials in one shot:
#   aws secretsmanager put-secret-value --secret-id earthdaily-agriculture/<project>/api \
#     --secret-string '{"client_id":"...","client_secret":"...","username":"...","password":"..."}'
resource "aws_secretsmanager_secret" "api" {
  name = "earthdaily-agriculture/${var.project_name}/api"
}

# --- IAM: task execution role (pulls image, ships logs, reads secrets) ---
data "aws_iam_policy_document" "task_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${local.name}-exec"
  assume_role_policy = data.aws_iam_policy_document.task_assume.json
}

resource "aws_iam_role_policy_attachment" "task_execution_managed" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role_policy" "task_execution_secrets" {
  name = "${local.name}-exec-secrets"
  role = aws_iam_role.task_execution.id
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["secretsmanager:GetSecretValue"]
      Resource = [aws_secretsmanager_secret.api.arn]
    }]
  })
}

# --- IAM: task role (the running container's permissions: write to S3) ---
resource "aws_iam_role" "task" {
  name               = "${local.name}-task"
  assume_role_policy = data.aws_iam_policy_document.task_assume.json
}

resource "aws_iam_role_policy" "task_s3" {
  name = "${local.name}-task-s3"
  role = aws_iam_role.task.id
  policy = jsonencode({
    Statement = [
      {
        Effect = "Allow"
        Action = ["s3:PutObject", "s3:GetObject", "s3:ListBucket", "s3:DeleteObject"]
        Resource = [
          "arn:aws:s3:::${var.s3_bucket}",
          "arn:aws:s3:::${var.s3_bucket}/${var.project_name}/*",
        ]
      },
    ]
  })
}

# --- ECS cluster + task definition --------------------------------------
resource "aws_ecs_cluster" "this" {
  name = local.name
}

resource "aws_ecs_task_definition" "this" {
  family                   = local.name
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.task_cpu     # "1024" = 1 vCPU
  memory                   = var.task_memory  # "2048" = 2 GB
  execution_role_arn       = aws_iam_role.task_execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([{
    name      = "earthdaily-agriculture"
    image     = "${aws_ecr_repository.this.repository_url}:${var.image_tag}"
    essential = true
    environment = [
      { name = "ENVIRONMENT",             value = var.environment },
      { name = "EDAGRO_OUTPUT_PREFIX",    value = "s3://${var.s3_bucket}/${var.project_name}" },
      { name = "EDAGRO_LOG_CONSOLE_ONLY", value = "1" },
    ]
    secrets = [
      { name = "PROD_API_CLIENT_ID",     valueFrom = "${aws_secretsmanager_secret.api.arn}:client_id::" },
      { name = "PROD_API_CLIENT_SECRET", valueFrom = "${aws_secretsmanager_secret.api.arn}:client_secret::" },
      { name = "PROD_API_USERNAME",      valueFrom = "${aws_secretsmanager_secret.api.arn}:username::" },
      { name = "PROD_API_PASSWORD",      valueFrom = "${aws_secretsmanager_secret.api.arn}:password::" },
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-group         = aws_cloudwatch_log_group.task.name
        awslogs-region        = var.aws_region
        awslogs-stream-prefix = "ecs"
      }
    }
  }])
}

# --- EventBridge cron + invoker role ------------------------------------
resource "aws_cloudwatch_event_rule" "schedule" {
  name                = "${local.name}-schedule"
  schedule_expression = var.schedule_expression  # e.g. "cron(0 6 * * ? *)"
  state               = var.schedule_state       # "ENABLED" or "DISABLED" — start DISABLED, flip after smoke test
}

data "aws_iam_policy_document" "scheduler_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["events.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "scheduler" {
  name               = "${local.name}-scheduler"
  assume_role_policy = data.aws_iam_policy_document.scheduler_assume.json
}

resource "aws_iam_role_policy" "scheduler" {
  name = "${local.name}-scheduler"
  role = aws_iam_role.scheduler.id
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["ecs:RunTask", "iam:PassRole"]
      Resource = "*"
    }]
  })
}

resource "aws_cloudwatch_event_target" "task" {
  rule     = aws_cloudwatch_event_rule.schedule.name
  arn      = aws_ecs_cluster.this.arn
  role_arn = aws_iam_role.scheduler.arn

  ecs_target {
    task_definition_arn = aws_ecs_task_definition.this.arn
    launch_type         = "FARGATE"
    platform_version    = "LATEST"

    network_configuration {
      subnets          = data.aws_subnets.default.ids
      assign_public_ip = true   # default VPC. Switch to a private subnet + NAT for production.
    }
  }
}
```

**`terraform/variables.tf`**

```hcl
variable "project_name"        { type = string }                           # e.g. "<client>-field-report"
variable "aws_region"          { type = string, default = "us-east-1" }
variable "environment"         { type = string, default = "prod" }
variable "s3_bucket"           { type = string }                           # existing outputs bucket — Terraform does NOT create it
variable "image_tag"           { type = string, default = "latest" }
variable "task_cpu"            { type = string, default = "1024" }          # 1 vCPU
variable "task_memory"         { type = string, default = "2048" }          # 2 GB
variable "schedule_expression" { type = string, default = "cron(0 6 * * ? *)" }  # 06:00 UTC daily
variable "schedule_state"      { type = string, default = "DISABLED" }      # start DISABLED, flip after smoke test
```

**`terraform/outputs.tf`**

```hcl
output "ecr_repository_url"     { value = aws_ecr_repository.this.repository_url }
output "task_definition_arn"    { value = aws_ecs_task_definition.this.arn }
output "log_group_name"         { value = aws_cloudwatch_log_group.task.name }
output "secret_arn"             { value = aws_secretsmanager_secret.api.arn }
output "manual_run_command"     {
  value = "aws ecs run-task --cluster ${aws_ecs_cluster.this.name} --task-definition ${aws_ecs_task_definition.this.family} --launch-type FARGATE --network-configuration 'awsvpcConfiguration={subnets=[${join(",", data.aws_subnets.default.ids)}],assignPublicIp=ENABLED}'"
}
```

#### Workflow

```bash
# 1. Build + push the image
docker build -t <project>:$(git rev-parse --short HEAD) .
$(aws ecr get-login-password --region <region> | \
  docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com)
docker tag <project>:$(git rev-parse --short HEAD) \
  <ecr-url>:$(git rev-parse --short HEAD)
docker push <ecr-url>:$(git rev-parse --short HEAD)

# 2. Apply Terraform (creates everything except the secret value)
cd terraform
terraform init
terraform apply \
  -var="project_name=<project>" \
  -var="s3_bucket=<your-outputs-bucket>" \
  -var="image_tag=$(git rev-parse --short HEAD)"

# 3. Populate the API secret (out-of-band — keeps creds out of TF state)
aws secretsmanager put-secret-value \
  --secret-id "earthdaily-agriculture/<project>/api" \
  --secret-string '{"client_id":"...","client_secret":"...","username":"...","password":"..."}'

# 4. Smoke-test manually before flipping the schedule
eval "$(terraform output -raw manual_run_command)"

# 5. Enable the cron
terraform apply -var="schedule_state=ENABLED" -var="project_name=<project>" -var="s3_bucket=<your-outputs-bucket>" -var="image_tag=$(git rev-parse --short HEAD)"
```

#### What this deliberately doesn't do

- **No VPC / subnet creation.** Uses the default VPC. For production-grade isolation drop in a `module "vpc"` (terraform-aws-modules/vpc/aws) and point `subnets` at its private subnets + add a NAT gateway.
- **No CI/CD pipeline.** Build + push happens manually here. Wire to GitHub Actions OIDC for hands-off image rebuilds — a separate concern.
- **No alerting.** Add an `aws_sns_topic` + a CloudWatch alarm on the task's failure-count metric, or hook your existing monitoring stack.
- **No multi-env.** One TF state per project. Two extractions = two states. Use Terraform workspaces or per-env directories if you need it.
- **No GCP / Azure equivalent.** The shape transfers (Cloud Run job + Workload Identity + Cloud Scheduler + Secret Manager; Container Apps + managed identity + Logic Apps + Key Vault), but the resource names don't.

### Fan-out across N containers (no orchestrator)

```bash
for i in 0 1 2 3; do
  docker run --rm -d \
    --env-file .env.prod \
    -e EDAGRO_OUTPUT_PREFIX=s3://my-bucket/runs/2026-01-01/shard-${i} \
    earthdaily-agriculture:latest \
    run-extractor \
      --extractor CoverageExtractor \
      --shard ${i} --num-shards 4 &
done
wait
```

On Kubernetes this becomes an `argoproj.io/Workflow` with `withParallelism: 4`. On ECS, a Job array. On Cloud Run, parallel Job executions. Same container, same CLI, different driver.

---

## Cost considerations

Rough monthly compute cost on a baseline workload: **1 vCPU + 2 GB RAM, 30-min run**. Sensitivity to run duration is significant — numbers shift meaningfully if your run is 5 min vs 4 hours. Pricing reflects publicly listed rates as of early 2026; check current rates before budgeting.

### Daily cadence (~30 runs/month)

| Pattern                                          | Compute cost/month | Notes                                                                          |
| ------------------------------------------------ | ------------------ | ------------------------------------------------------------------------------ |
| A — GH Actions (private repo, 30-min run)        | **$0**             | 30 × 30 = 900 min, well inside the 2,000-min free tier                          |
| A — GH Actions (private repo, 4-hour run)        | ~$58               | 30 × 240 = 7,200 min → 5,200 over → 5,200 × $0.008                              |
| A — GH Actions (public repo, any run)            | **$0**             | Public repos get unlimited Actions minutes                                      |
| B — ECS Fargate (30-min, on-demand)              | ~$0.75             | 30 × $0.0247 (1 vCPU @ $0.04048/hr + 2 GB @ $0.004445/GB-hr)                    |
| B — Cloud Run jobs (30-min)                      | ~$0.45             | Billed in 100 ms increments; cheaper than Fargate at idle                       |

**Daily winner: Pattern A.** Free for any private repo whose total monthly compute fits the 2,000-min free tier. Pattern B's $1/month is dwarfed by its setup overhead.

### Hourly cadence (~720 runs/month)

| Pattern                                          | Compute cost/month | Notes                                                                          |
| ------------------------------------------------ | ------------------ | ------------------------------------------------------------------------------ |
| A — GH Actions (private repo, 30-min run)        | **~$157**          | 720 × 30 = 21,600 min → 19,600 billable → 19,600 × $0.008                       |
| A — GH Actions (private repo, 10-min run)        | ~$42               | 720 × 10 = 7,200 → 5,200 billable                                                |
| B — ECS Fargate (30-min, on-demand)              | **~$18**           | 720 × $0.0247                                                                   |
| B — Cloud Run jobs (30-min)                      | **~$11**           | Same workload, cheaper at-scale than Fargate                                    |
| B — Fargate Spot (30-min, killable)              | ~$5                | ~70% discount; only for runs that tolerate interruption                          |

**Hourly winner: Pattern B.** Crossover with A is ~$140/month for a 30-min run — more than enough to pay Pattern B's operational overhead.

### Costs that don't differentiate

Both patterns pay these:

- **S3 storage of outputs** — pennies/month either way.
- **S3 PUT requests** — pennies.
- **Egress** — free if your S3 bucket is in the same region as the runner (B); free for writes from GH Actions if you're not pulling artifacts back (A).
- **Image registry** (B only) — ECR / Artifact Registry / GHCR free tier is 500 MB; one 600 MB image is ~$0.10/month after.
- **CloudWatch / Cloud Logging** (B only) — ~$0.50/GB ingested; hourly cadence with 1 MB logs/run is ~$0.36/month.

### Caveats that matter more than the cost math

1. **GH Actions has a 6-hour hard ceiling per job.** Pattern A can't run anything that exceeds that, regardless of price. If your extraction creeps toward 4 hours, plan the B migration before it bites.
2. **GH Actions schedule reliability.** Cron is best-effort — runs can be delayed up to 10 min under platform load. For SLO-driven hourly cadence ("data must be in S3 by HH:05"), Pattern B's deterministic scheduling wins regardless of cost.
3. **Pattern B amortises setup.** Image build pipeline, vulnerability scan, IAM roles, monitoring — call it 0.5–1 day one-time + ~1 day/month operational toil. For one or two extractions that overhead is the dominant cost; for 10+ extractions sharing the same image, it disappears.

### Rule of thumb

- **Daily, < 2 hr/run** → Pattern A. Free + low operational overhead.
- **Sub-daily cadence OR > 4 hr/run OR VPC required** → Pattern B. The cost math says so; the reliability math says so more loudly.

---

## Migrating from A to B

The Python entrypoint doesn't change. The only thing that does is the driver:

1. **Build and publish an image** from your existing repo — `docker build -t <repo>/<name>:$(git rev-parse --short HEAD) .` then push to your private registry.
2. **Provision the scheduler** — ECS scheduled task, Cloud Run job, or Argo workflow targeting that image with the same `EDAGRO_OUTPUT_PREFIX` you'd build into the GH Actions step.
3. **Same stdout contract.** `REPORT_PATH=` still works; orchestrators just capture stdout differently.
4. **Disable the GitHub workflow** once the new scheduler is reliable. The Python code, YAML config, and pinned package version never changed.

---

## See also

- [`09 - Workflow_architecture.md`](09%20-%20Workflow_architecture.md) — how the workflow runner is wired.
- [`09b - Workflow_YAML_reference.md`](09b%20-%20Workflow_YAML_reference.md) — YAML shape, transform recipes (incl. `publish_to_cloud` post-run hand-off).
- [`13 - Cloud_storage_principles_and_usage.md`](13%20-%20Cloud_storage_principles_and_usage.md) — the writer-layer S3 support that both patterns depend on.
