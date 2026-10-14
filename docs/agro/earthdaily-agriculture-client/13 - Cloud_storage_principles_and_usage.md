---
title: Cloud storage
description: How to write extractor outputs to S3 (or any S3-compatible store) — local disk, AWS S3, or MinIO — and the design behind the writer layer.
#icon: material/cloud-upload-outline
keywords:
  - cloud storage
  - s3
  - minio
  - writer
  - results
  - output path
  - zarr
  - cube
  - ZarrStore
---

# Cloud Storage — Principles and Usage

User-facing guide for the cloud-storage feature in EarthDaily Agriculture client. Read this when you want to know how to write extractor outputs to S3 (or any S3-compatible store) and what's behind the design choices that govern it.

> For the user-facing deployment patterns (GitHub Actions cron, Docker container on ECS / Cloud Run / Argo) that consume this writer-layer feature, see [`14 - Deployment_patterns.md`](14%20-%20Deployment_patterns.md). Come here to understand how cloud writes work; go there to operationalise a scheduled run.

---

## At a glance

Run any extractor — single-entity test, bulk parallel run, or a multi-step `WorkflowManager` YAML — and have its outputs land in one of three places, with the same code:

- **`<project-root>/results/`** — local disk (default; no setup needed).
- **`s3://<your-bucket>/...`** — real AWS S3 (cloud production).
- **`s3://<bucket>/...` on `localhost:9000`** — a MinIO container (local dev / CI).

Same DataFrames, same column names, same partial-save cadence, same HTML report. **The only thing that changes between the three is the path string** you give the extractor.

---

## Principles

The seven design choices below are what make cloud storage cheap to adopt, safe to ignore, and consistent with how local extractor runs already behave.

### 1. Path-based switching, not code-based

There's no `S3Extractor` class, no `cloud_mode` flag on the extractor, no parallel codepath. Cloud storage is a property of the **path string** in the config the extractor is built with — `manager.config` under `WorkflowManager`, or the dict you pass when you build an extractor yourself:

```python
manager.config["output_result_dir"]  = "s3://my-bucket/runs/2026-05-09/results"
manager.config["partial_result_dir"] = "s3://my-bucket/runs/2026-05-09/partials"
```

The extractor doesn't know or care. Internally, every writer routes through fsspec when it sees an `s3://` or `az://` prefix; through `pandas.to_csv` / `Path.write_text` for everything else.

> **GCS is recognized but not supported yet.** `gs://` and `gcs://` are in the writer's scheme list, but **no published extra installs `gcsfs`**, so a `gs://` path fails with an fsspec backend error unless you install it yourself. Treat GCS as untested until a `gcs` extra ships.

**Why this matters:** every extractor — current and future — gains S3 support for free. There's no per-extractor wiring to maintain and no risk of one extractor's S3 path drifting from another's.

### 2. Reads and writes are independently configurable

Cloud-storage routing applies only to **writes** (results, partials, failed-IDs, HTML report). **Reads** — entity loading from Geosys' S3 in Step 2 of most notebooks, or `pd.read_csv(...)` on an input file — go through whichever credentials and endpoint you set up at notebook init time and aren't affected by switching write modes.

The mechanism: `WorkflowManager` instantiates a boto3 client at construction time with the credentials present at that moment. Subsequent env-var changes (e.g. setting `AWS_ENDPOINT_URL` to point writes at MinIO) only affect *new* fsspec/boto3 calls — i.e. the writes.

**Why this matters:** you can develop locally with writes going to MinIO while still pulling entity CSVs from real Geosys S3, with no special-casing.

### 3. Credentials follow the standard chain — always

There's no EarthDaily Agriculture-specific cloud credentials API. Reads and writes both honor the chain that AWS SDKs already use:

1. Explicit env vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, optional `AWS_SESSION_TOKEN`, `AWS_DEFAULT_REGION`)
2. `.env` file at your project root (loaded by `setup_environment` via `python-dotenv`; it also accepts `src/.env`, which is where a repository checkout keeps credentials beside the source)
3. `~/.aws/credentials` profile
4. EC2 instance profile / ECS task role / EKS pod identity / Lambda execution role

For non-AWS S3 (MinIO, LocalStack, on-prem MinIO clusters, R2, etc.), `AWS_ENDPOINT_URL` redirects every S3 call to that endpoint without code changes.

**Why this matters:** local dev, IAM-role'd containers, AWS SSO, and on-prem object stores all work the same way without per-environment plumbing.

#### Azure Blob Storage (`az://`)

Writing to `az://<container>/<prefix>` works the same way — install the backend (`pip install -e ".[azure]"`, which pulls `adlfs`) and set credentials in the environment. Unlike AWS, Azure needs the account name + a credential passed explicitly, so `storage_options_for()` builds them from these env vars (first match wins):

1. `AZURE_STORAGE_CONNECTION_STRING` — carries account + credential in one string.
2. `AZURE_STORAGE_ACCOUNT_NAME` + `AZURE_STORAGE_SAS_TOKEN` (leading `?` optional).
3. `AZURE_STORAGE_ACCOUNT_NAME` + `AZURE_STORAGE_ACCOUNT_KEY`.
4. `AZURE_STORAGE_ACCOUNT_NAME` alone → adlfs's default credential chain (`DefaultAzureCredential`: **Managed Identity**, `az` CLI, env service-principal …) — the clean choice for ECS/Argo running in Azure, no secret in the environment.

```python
manager.config["output_result_dir"]  = "az://my-container/runs/2026-06-30/results"
manager.config["partial_result_dir"] = "az://my-container/runs/2026-06-30/partials"
```

The account is non-HNS Blob storage, so use the `az://` scheme (`abfs://` also works for ADLS Gen2). The four keys are templated in `template.env` at the repository root — copy it to `.env` and fill it in.

### 4. Partial saves and failed-entity retries work identically

Bulk extractors flush partials every `partial_frequency` entities and persist `failed_ids_*.csv` files when `fail_safe=True`. Both work over S3 the same way they work locally — same filenames, same timing, same resume semantics. After a successful run the cleanup pass removes the partials via fsspec; the `failed_ids_*.csv` files are left in place.

Resuming from those files is **explicit**: pass `retry_failed_only=True` (or a specific file path) to process only the recorded IDs — see *09b — Workflow YAML reference → Resuming a failed run*. `fail_safe` on its own means "tolerate per-entity failures" and never changes which entities are processed. Previously it silently implied the resume, so a leftover file capped every later `fail_safe` run while reporting success.

**What this does not cover: a run that crashes mid-way.** Partials are a progress record, not a checkpoint — nothing reads them back. If the process dies (killed, out of memory, a pod evicted), the next run starts the whole entity list again. Locally, the opt-in cache softens this — results cached per entity survive the crash (see *07 — Cache design context*) — but on S3 the cache is off (principle 5), so nothing does. Resume after a crash on S3 is therefore a matter of run size: keep each run short enough that redoing it is cheap (see Recipe D for container shards). What *does* resume is the failed-entity path above: a run that finishes with `fail_safe=True` records its failed IDs, and a later `retry_failed_only=True` run — a different process, even a different machine — reprocesses only those.

**Why this matters:** failed-entity retries behave the same on S3 as on local disk — there's no "S3 mode disables fail-safe" surprise — and the limit on crash recovery is stated, not discovered.

### 5. The cache is intentionally local-only

When `cache_dir` is `s3://...`, the cache subsystem **forces `use_cache=False`** at construction time and emits a one-time loguru WARNING explaining why.

The reason: `_update_cache` uses an atomic-rename pattern (`tempfile + Path.replace`) that has no equivalent on object stores — S3 has no atomic rename, and a per-pod cache wouldn't survive a container restart anyway. Rather than silently degrading to a non-atomic write that can race between concurrent extractors, the cache is disabled, you see why, and you decide whether to keep `cache_dir` local even when results live on S3.

**Why this matters:** caching is opt-in (default off), so most users never see this. When you opt in *and* point `cache_dir` at S3, you get a loud, traceable warning instead of silent corruption.

### 6. Logs follow a different policy from data outputs

Data outputs (results, partials, etc.) work on `s3://` paths. **Logs do not** — the `log_dir` argument to `setup_logging` is local-only by design. For containerized runs there's a separate switch:

- `EDAGRO_LOG_CONSOLE_ONLY=1` env var, or
- `WorkflowManager(..., log_to_console_only=True)` kwarg

…tells the logger to skip the file sink entirely and emit only to stdout. The container orchestrator (Argo, ECS, Cloud Run, Docker, etc.) then captures stdout the same way it captures any other process's logs.

**Why this matters:** stdout-with-orchestrator-capture is the right pattern for ephemeral runtimes. Pushing log files to S3 every few seconds would be expensive and fragile; relying on the platform's existing log-collection is cheap, standard, and works with every cloud runtime.

### 7. Default-to-local — strictly opt-in for cloud

Three independent switches enable cloud storage, all default-off:

| Switch | Where | Default |
|---|---|---|
| Path string `s3://...` in `manager.config` | Notebook / script / YAML | `<project-root>/results` |
| `EDAGRO_OUTPUT_PREFIX=s3://...` env var | Process env (orchestrator) — honored by `WorkflowManager`, `setup_environment()` and directly-built extractors | unset |
| `storage=` kwarg | `WorkflowManager(..., storage=...)`, `setup_environment(..., storage=...)` | `"auto"` (env var wins if set) |
| `[s3]` extra (`s3fs`, `fsspec`) | `pip install -e ".[s3]"` | not pulled by `[test]` or `[jupyter]` |
| `[azure]` extra (`adlfs`, `fsspec`) | `pip install -e ".[azure]"` | not installed |
| `[cloud]` extra (`s3` + `azure` together) | `pip install -e ".[cloud]"` | not installed |
| `[cube]` extra (`xarray`, `zarr`, `rioxarray`) | `pip install -e ".[cube]"` | not installed |
| `EDAGRO_LOG_CONSOLE_ONLY=1` | Process env | unset (file sink active) |

If you don't flip any of them, your notebook does **exactly** what it did before this feature existed — no new dependencies, no new env vars, no new code paths. Verified by `TestExportResultsLocalRoundtrip` (byte-identical CSV round-trip) and `TestFinalizeExtractionLocal` in `tests/test_fs_helpers.py`.

`fsspec` and `s3fs` are imported lazily — they only load when a write hits a remote URI. Local notebooks never pay the import cost or pull the transitive dependencies.

---

## How to use it — four concrete recipes

### Recipe A — Local only (default)

Nothing to do. Existing notebooks keep working as today.

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager
manager = WorkflowManager("prod")
# manager.output_result_dir   == "<project-root>/results"
# manager.partial_result_dir  == "<project-root>/partials"
# manager.cache_dir           == "<project-root>/cache"  (cache only used if use_cache=True)
# Logs rotate to <project-root>/logs/earthdaily_<date>.log
```

Verifying you're in this mode:

```python
print(manager.config["output_result_dir"])   # local path
```

**Pinning to local explicitly.** If you want a dev notebook to ignore any
`EDAGRO_OUTPUT_PREFIX` that might leak in from `.env` or the parent shell
(e.g. a teammate set it for their own container test), pass `storage="local"`:

```python
manager = WorkflowManager("prod", storage="local")
# Forces local <project-root>/{results,partials,cache} regardless of env vars.
```

`storage` is a `Literal["auto", "local", "s3"]` kwarg; the default `"auto"` is
the existing behavior (env var wins if set, otherwise local).

### Recipe B — Real AWS S3

For shared-team workflows, scheduled batch jobs, container deploys, or anywhere outputs need to outlive the local machine.

**One-time setup:**

```bash
pip install -e ".[s3]"          # pulls s3fs + fsspec
```

Make sure AWS credentials are reachable via *one* of:

- `.env` at your project root with `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
- `~/.aws/credentials` profile
- IAM role / instance profile (containers / EC2)
- AWS SSO logged in (`aws sso login`)

Verify with `aws s3 ls` (should not error).

**Per-notebook switch** — construct `WorkflowManager` with the S3 paths in one shot:

```python
import uuid

S3_BUCKET = "your-aws-bucket"           # bucket you own and have write access to
run_prefix = f"runs/regional/{uuid.uuid4().hex[:8]}"
base = f"s3://{S3_BUCKET}/{run_prefix}"

manager = WorkflowManager(
    "prod",
    output_result_dir=f"{base}/results",
    partial_result_dir=f"{base}/partials",
    cache_dir=f"{base}/cache",          # auto-disables cache on remote paths
)
```

Run the rest of the notebook normally. Verify:

```python
import s3fs
fs = s3fs.S3FileSystem()                                   # no client_kwargs → real AWS
print(fs.ls(f"{S3_BUCKET}/{run_prefix}/results"))
```

**Container deploys** — set `EDAGRO_OUTPUT_PREFIX` on the container and `/results`, `/partials`, `/cache` are derived from it automatically — by `WorkflowManager`, and equally by an extractor built directly from `setup_environment()` or from a minimal config (a stateless container with no `WorkflowManager`). No per-extractor code:

```bash
docker run --rm \
  -e EDAGRO_OUTPUT_PREFIX=s3://my-bucket/runs/2026-05-09/<workflow> \
  -e EDAGRO_LOG_CONSOLE_ONLY=1 \
  --env-file .env.prod \
  <your-project-image>:<tag> --prefix run_20260509
```

`<your-project-image>` is the image built from a scaffolded project's `Dockerfile`; its entrypoint is `python -m app.run_pipeline`, so only the arguments follow the image name.

Inside Python — `WorkflowManager("prod")` is enough, and so is an extractor built directly (Recipe D); no explicit kwargs needed. The env-var path takes effect when `EDAGRO_OUTPUT_PREFIX` is set; explicit constructor kwargs still win if you also pass them. See [`14 - Deployment_patterns.md`](14%20-%20Deployment_patterns.md) for the full Pattern B invocation.

**Asserting S3 mode in a notebook.** When you want the notebook to *refuse to
fall back to local* (typical for shared / scheduled extractions), pass
`storage="s3"`:

```python
manager = WorkflowManager("prod", storage="s3")
# Raises unless EDAGRO_OUTPUT_PREFIX is a remote URI (s3://, az://, ...) or a remote
# kwarg is provided. A *local* EDAGRO_OUTPUT_PREFIX is rejected too: it would let a
# run meant for S3 write to the machine's own disk.
```

Precedence (highest first):

1. Explicit kwargs (`output_result_dir=...`, etc.), or explicit paths in the config an extractor is built with
2. `storage=` flag (`"local"` blocks the env var; `"s3"` requires a remote path)
3. `EDAGRO_OUTPUT_PREFIX` env var (when `storage="auto"`)
4. Local `<project-root>/{results,partials,cache}` defaults

The same order holds whether the paths are resolved by `WorkflowManager`, by `setup_environment()`, or by a directly-built extractor — all three go through one function, `core._fs.apply_output_prefix()`. Only `WorkflowManager` enforces `storage="s3"`.

### Recipe C — Local dev with MinIO

For iterating on the cloud-storage code path without an AWS account: deterministic, free, and offline-friendly.

**One-time setup:**

```bash
docker compose -f tests/smoke_test/minio-compose.yml up -d
pip install -e ".[s3]"
```

MinIO listens on `localhost:9000` (S3 API) and `localhost:9001` (web console; login `minioadmin` / `minioadmin`).

**Per-notebook switch** — same as Recipe B, plus four MinIO-specific env vars and a bucket pre-creation step **before** building the manager (the S3 client init inside `WorkflowManager` needs the endpoint env vars to be set):

```python
import os, uuid, s3fs

# MinIO presets — overrides any real AWS creds in the environment.
os.environ["AWS_ACCESS_KEY_ID"]      = "minioadmin"
os.environ["AWS_SECRET_ACCESS_KEY"]  = "minioadmin"
os.environ["AWS_ENDPOINT_URL"]       = "http://localhost:9000"
os.environ["AWS_DEFAULT_REGION"]     = "us-east-1"

S3_BUCKET = "earthdaily-agriculture-dev"
fs = s3fs.S3FileSystem(client_kwargs={"endpoint_url": "http://localhost:9000"})
if not fs.exists(S3_BUCKET):
    fs.mkdir(S3_BUCKET)              # MinIO doesn't auto-create buckets

run_prefix = f"runs/regional/{uuid.uuid4().hex[:8]}"
base = f"s3://{S3_BUCKET}/{run_prefix}"
manager = WorkflowManager(
    "prod",
    output_result_dir=f"{base}/results",
    partial_result_dir=f"{base}/partials",
    cache_dir=f"{base}/cache",
)
```

The dev notebooks `EDAgriculture_regional_Function_Dev.ipynb` (and the same toggle pattern can be added to any extractor notebook) ship a `USE_S3 = True` toggle that does this in two lines.

**Tear down:**

```bash
docker compose -f tests/smoke_test/minio-compose.yml down -v   # -v drops volume; omit to keep test data
```

**Why MinIO and not LocalStack:** MinIO is purpose-built for S3-compatible object storage and matches AWS S3's request shape closely. LocalStack emulates the broader AWS surface (Lambda, DynamoDB, etc.) but is heavier and has historically had more S3 quirks. For pure write-path testing, MinIO is faster and simpler. **MinIO ≠ AWS S3 byte-for-byte**, though — for production sign-off, run one smoke test against real AWS before declaring victory.

### Recipe D — An extractor called directly (stateless container, no `WorkflowManager`)

Large runs can skip `WorkflowManager`: each container builds the extractor itself and
runs it on its slice of entities. `EDAGRO_OUTPUT_PREFIX` works the same way
there — set it on the pod (one prefix per shard, so shards never overwrite each
other) and build the extractor from `setup_environment()`:

```python
from earthdaily.agriculture.core.functions_enhanced import setup_environment
from earthdaily.agriculture.core.identity import EDAuthenticator
from earthdaily.agriculture.processors.processor_harvest_functions import HarvestExtractor

# On the pod: EDAGRO_OUTPUT_PREFIX=s3://my-bucket/runs/2026-10-02/shard-3
config = setup_environment("prod")            # results / partials / cache under the prefix
token, expires = EDAuthenticator.get_new_token(env="prod")

extractor = HarvestExtractor(token, expires, config)
extractor.setup_harvest_parameters(harvest_type="INSEASON_HARVEST", year=2025)
result = extractor.process_harvest_bulk_extraction_parallel(
    entity_list=shard_entities,               # this pod's slice
    fail_safe=True,                           # one bad entity must not fail the pod
)
# Final results -> s3://my-bucket/runs/2026-10-02/shard-3/results/
# Partials      -> s3://my-bucket/runs/2026-10-02/shard-3/partials/
```

- **No `output_path` needed** — a bulk call without one writes to the extractor's own
  results path, which is the prefixed one.
- **A minimal config works too.** If you build the config dict yourself and leave
  **all** the paths out, the extractor falls back to `EDAGRO_OUTPUT_PREFIX` (and logs it
  once at INFO). Set any one of `output_result_dir` / `partial_result_dir` / `cache_dir`
  and the config is taken as complete — the prefix fills nothing in, so a run is never
  split between local disk and S3. Without `"env"`, the extractor uses
  `prod`.
- **The token refreshes itself.** A directly-built extractor refreshes an expired token
  through `EDAuthenticator`, from the same credential environment variables, so an
  hours-long shard does not need `WorkflowManager` for that either.
- **Nothing refuses a local fallback here.** `storage="s3"` is enforced by
  `WorkflowManager` only. On a pod, assert it yourself before running:
  `assert config["output_result_dir"].startswith(("s3://", "az://"))`.
- **The working directory must be writable.** `setup_environment()` still creates and
  write-tests `results/`, `partials/`, `cache/`, `inputs/` and `logs/` locally before
  re-pointing the writer paths, so a read-only root filesystem fails here even though
  nothing is written there later. Run with a writable `WORKDIR` (or a mounted volume).
- **The cache stays off.** With the prefix set, `cache_dir` is remote too, so caching
  is disabled (principle 5) — a retried pod re-fetches its entities.
- **Map files (FLM / Difference / Zoning, `postprocess="file"`)** — leave
  `output_path` out: they go to `<prefix>/results/maps` on S3. FLM's
  `skip_existing=True` then makes a retried pod skip the maps it already saved — the
  one place a crashed shard does resume (see *Rasters and maps* below).
- **Size shards so a retry is cheap.** When an orchestrator retries a container that
  crashed or was evicted, the shard starts again from its first entity: its partials on S3 are not
  read back (principle 4), and the cache is off. A retry is correct but costs the whole
  shard, so prefer many short shards (minutes) over a few long ones (hours). Slow
  extractors — LRTS waits up to 5 minutes per entity — need especially small shards.
- **Two retries, two mechanisms.** A container that *crashes* is retried by the
  orchestrator and redoes its shard. Entities that *fail* inside a pod that
  finishes are recorded on S3 (`fail_safe=True`); retry them with a follow-up run on
  the same prefix and `extractor.retry_failed_only = True`, which processes only those
  IDs.

---

## Rasters and maps (`postprocess="file"`)

The `postprocess="file"` writers — **FLM, Difference and Zoning** — save PNG, TIFF and
shapefile output through `BaseExtractor.save_map_file()`, which routes via `_fs` like
every other writer. So `output_path` accepts a remote URI directly:

```python
extractor.setup_flm_parameters(postprocess="file", output_path="s3://bucket/prefix/tifs")
```

**Without `output_path`**, maps go to `<results dir>/maps` — so under
`EDAGRO_OUTPUT_PREFIX` they land on the prefix with no extra parameter, and
`saved_files` lists their `s3://` URIs. (File mode used to *require* `output_path`; a
stateless container then had to pass one, and a local folder put the maps on its disk, gone
with the container while `saved_files` still listed them.) A local `output_path` while the
prefix is remote and no `output_uri` is set now logs a warning for exactly that case.

Rasters differ from CSV results in one way that matters: the analysis step usually reads
every file back. Opening 100k TIFs over the network turns a seconds-long pass into
thousands of round trips, so writing *only* to object storage is rarely what you want.

Set `output_uri` to keep both — local working copy, remote durable copy:

```yaml
workflow:
  settings:
    output_uri: s3://bucket/prefix/tifs   # durable copy
    # output_path stays local — the working copy the analysis reads
```

```bash
export EDAGRO_OUTPUT_URI=s3://bucket/prefix/tifs
```

Precedence matches `export_format`: **step-level `output_uri:` > workflow `settings.output_uri`
> `EDAGRO_OUTPUT_URI` > `None`** (local only, the default).

Two details worth knowing:

- **`saved_files` records the local path**, not the URI. Manifests therefore stay
  openable by readers that use `Path(...)` / `open(...)`. If you want a manifest that
  points at object storage, the reader has to go through `_fs` first.
- **A failed durable write is a per-entity failure**, not a warning. This is deliberately
  unlike the manifest sidecar: a run that silently kept going would leave a manifest
  claiming rasters that only ever existed on the runner.

---

## N-D cubes — Zarr on object storage

CSV and Parquet cover tabular results. When the natural shape is a **cube** rather than a table — a vegetation-index raster stack over time, or a regional series of `(date, entity)` x parameters — the package writes [Zarr](https://zarr.readthedocs.io/) through `ZarrStore`, and it works against a local path or `s3://` with the same call.

Zarr belongs in this document rather than the export one because its whole advantage is a cloud-storage property: the array is split into chunks stored as separate objects, so **each chunk is one S3 GET**. A reader wanting one field's time series fetches the chunks covering it, not the whole cube. A single monolithic file has no such option.

Install the backend:

```bash
pip install "earthdaily-agriculture[cube]"     # xarray, zarr, rioxarray
```

`xarray` and `s3fs` are imported lazily, so the module costs nothing until you use it.

### Writing and appending

```python
from earthdaily.agriculture.export import ZarrStore

store = ZarrStore("s3://bucket/prefix/cube.zarr")
store.write(ds, group="weather", chunks="auto")
store.append(new_days, dim="date", group="weather")     # idempotent
```

`append` deduplicates on the append dimension's coordinate, so re-running a day that is already
present is a no-op rather than a duplicate. Writing to a named `group` means appending to one
group never disturbs its siblings.

### Two things that will bite you

**Chunk both axes, not one.** `chunks="auto"` picks a shape-aware default — `{date: 365, entity: 512}` for a regional cube, `{time: 20, y: 256, x: 256}` for a `(time, y, x)` cube — targeting a bounded ~1-10 MB chunk regardless of field size. Chunking only the time axis makes per-entity reads fetch the entire spatial extent for every timestep. No dask is required; chunking is applied through `to_zarr(encoding=...)`.

**`append` is read-modify-write.** Each call loads the whole existing store and rewrites it, so one append costs O(current store size) in I/O and a season of N appends is roughly O(N^2) cumulatively. On a large, frequently-appended remote store that dominates everything else — **batch your appends**. A region write that would make this O(slab) per append is a tracked follow-up.

### Alignment on append is deliberately strict for rasters

When concatenating, alignment over the non-append dimensions is shape-aware:

| Cube shape | Join | Why |
| --- | --- | --- |
| `(date, entity)` | `outer` | entities onboarded mid-season pad older dates with NaN — intended |
| `(time, y, x)` | `exact` | a shifted pinned grid is corruption, not a union — it raises rather than NaN-padding two incoherent footprints |

Override per call with `append(join=...)` if you genuinely mean something else.

---

## Common gotchas

- **`storage_options={}` on reads.** Writes are taken care of by the extractor and the HTML reporter. Reads in your notebook (e.g. `pd.read_csv("s3://...")`) need `storage_options={}` so pandas routes through fsspec.

- **`AWS_ENDPOINT_URL` is sticky in a Jupyter kernel.** Once set (Recipe C), it stays in `os.environ` until kernel restart. Switching from MinIO to real AWS in the same kernel without `del os.environ["AWS_ENDPOINT_URL"]` will keep targeting MinIO. Easiest fix: restart the kernel before switching modes.

- **MinIO doesn't auto-create buckets.** The `s3fs.S3FileSystem.mkdir(...)` step in Recipe C handles it. AWS S3 also doesn't auto-create — use a pre-provisioned bucket per project.

- **Cache + `s3://` is a deliberate no-op.** Don't try to "fix" the warning by patching `_update_cache`; the local atomic-rename has no S3 equivalent. If shared-cache-across-pods becomes a real need, that's a follow-up project (S3-conditional-write or DynamoDB-based locking) and shouldn't ship without a careful look at the multi-pod race conditions.

- **`s3fs` install errors.** `s3fs` pulls `aiobotocore` which can clash with older `botocore` pins. If `pip install -e ".[s3]"` fails, upgrade together: `pip install -U boto3 botocore s3fs`.

- **Loguru `log_dir` is local-only.** Passing `s3://...` to `setup_logging(log_dir=...)` will create a literal local directory named `s3:` (Path mangles the URL). For container deploys use `EDAGRO_LOG_CONSOLE_ONLY=1` and let the orchestrator capture stdout.

- **Switching mid-notebook only affects future writes.** Files already written to local disk stay on disk; flipping to S3 mid-notebook just routes the *next* write. For a clean switch, restart the kernel and re-run from the top.

---

## Verifying it works

The fastest way to confirm cloud storage is wired correctly end-to-end on your machine:

```bash
# Recipe C (MinIO) — full integration suite, ~10s
docker compose -f tests/smoke_test/minio-compose.yml up -d
AWS_ACCESS_KEY_ID=minioadmin \
AWS_SECRET_ACCESS_KEY=minioadmin \
AWS_ENDPOINT_URL=http://localhost:9000 \
AWS_DEFAULT_REGION=us-east-1 \
pytest tests/test_cloud_writers_integration.py -v
```

Expect 7 tests passing. Each one exercises one of the writer surfaces (CSV results, partials, failed-IDs CSV, HTML report, partial cleanup, etc.) end-to-end against MinIO.

CI runs the same tests on every PR via `.github/workflows/cloud-writers.yml` so regressions are caught before merge.

---

## Where to look in the code

If you're debugging or want to confirm a specific behavior:

| Concern | File |
|---|---|
| Path detection / URL build / fsspec routing | `src/earthdaily/agriculture/core/_fs.py` |
| `EDAGRO_OUTPUT_PREFIX` routing (shared) | `src/earthdaily/agriculture/core/_fs.py:apply_output_prefix` — called by `setup_environment()`, `WorkflowManager.__init__`, `BaseExtractor.__init__` |
| Final results / errors CSV writes | `src/earthdaily/agriculture/core/api_utils.py:export_results` |
| Raster / map file writes, `output_uri` mirror | `src/earthdaily/agriculture/core/base_extractor.py:save_map_file` |
| `failed_ids` CSV, partial cleanup, HTML report write | `src/earthdaily/agriculture/core/base_extractor.py:_finalize_extraction` |
| Cache disable on remote `cache_dir` | `src/earthdaily/agriculture/core/base_extractor.py:__init__`, `apply_cache_setting` |
| Loguru file-sink toggle | `src/earthdaily/agriculture/core/logging_setup.py` |
| HTML reporter S3 routing | `src/earthdaily/agriculture/reporting/extraction_reporter.py:render_html` |
| MinIO compose for Recipe C | `tests/smoke_test/minio-compose.yml` |
| Integration tests | `tests/test_cloud_writers_integration.py` (skipped without `AWS_ENDPOINT_URL`) |
| Prefix without `WorkflowManager` | `tests/test_output_prefix_direct.py` |
| CI workflow | `.github/workflows/cloud-writers.yml` |

For the deployment patterns that build on this writer-layer feature (Docker container on ECS / Cloud Run / Argo Workflows, GitHub Actions cron), see [`14 - Deployment_patterns.md`](14%20-%20Deployment_patterns.md).
