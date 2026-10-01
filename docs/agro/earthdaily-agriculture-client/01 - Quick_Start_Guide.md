---
title: Quick start
description: Install earthdaily-agriculture, scaffold a project, run your first extraction.
#icon: material/rocket-launch-outline
keywords:
  - quick start
  - install
  - cookiecutter
  - init_project
  - bootstrap
  - first extraction
---

# Quick start

From zero to a working extraction in roughly fifteen minutes. Two paths:

- **Scaffold a project (recommended).** A bootstrap script creates a complete project layout (`app/`, `configuration/`, `inputs/`, `results/`, …), pins the package version, drops in a starter workflow YAML and notebook, and wires up AI-assistant context out of the box.
- **From scratch.** `pip install`, write your own `.py` or notebook. Good for one-off exploration or integrating into an existing project.

Both paths end at the same place: a notebook that authenticates against the EarthDaily Agro API, loads entities, runs an extractor, and writes results to `results/`.

---

## Prerequisites

- **Python 3.10–3.13.** All four are covered by CI. 3.12.x is the recommended primary version and the one release wheels are built on.
- **EarthDaily Agro credentials.** OAuth2 client ID, client secret, username, and password. If you don't have these yet, contact your EarthDaily Agro representative.

---

## Scaffold a project

Two equivalent flows. Pick whichever fits your starting state.

### A.1 — Drop the bootstrap into an empty repo

Best when you've just created an empty GitHub repo and cloned it locally — the bootstrap fills the folder you're sitting in (no nested `<project_slug>/` folder created). The git repo name, folder name, and project slug all stay aligned automatically.

```bash
# 1. Create or clone your empty repo and cd into it.
cd path/to/my-empty-repo

# 2. Pull init_project.py from the package's GitHub repo:
curl -O https://raw.githubusercontent.com/earthdaily/earthdaily-agriculture/main/init_project.py

# 3. Run it.
python init_project.py
```

The script will:

1. **Discover or fetch the cookiecutter template.** It looks in a few common locations on disk first; if it doesn't find a local clone of `earthdaily-agriculture`, it uses the public GitHub URL and cookiecutter clones the repo on the fly.
2. **Lock `project_slug` to the target folder name** so the slug can never drift from the git repo / folder name.
3. **Prompt once** for `project_description`. Everything else uses sensible defaults (pass `--non-interactive` to skip this prompt too).
4. **Run cookiecutter** with `overwrite_if_exists=True` so the template populates your existing folder in place.
5. **Generate `CLAUDE.md` + `/earthdaily-agriculture` skill** via the post-generation hook (see [`12 - AI enablement.md`](12%20-%20AI%20enablement.md)).

Flags:

| Flag                       | Default       | Use when                                                                                |
| -------------------------- | ------------- | --------------------------------------------------------------------------------------- |
| `--target PATH`            | current dir   | Bootstrap a different folder than your shell is currently in.                            |
| `--template PATH`          | auto          | Multiple local clones of `earthdaily-agriculture` on disk; pin which one to use.         |
| `--project-name NAME`      | folder name   | Override the human-readable project name (slug stays locked to the folder name).         |
| `--project-description TEXT` | prompted     | Skip the description prompt for scripted runs.                                          |
| `--environment ENV`        | `prod`        | Pick `preprod` if the project targets the preprod API.                                  |
| `--non-interactive`        | off           | CI / automated bootstrap. No prompts at all.                                            |

### A.2 — Raw cookiecutter (creates a new folder next to you)

If you don't have an empty repo yet and want cookiecutter to create the project folder for you, run it directly:

```bash
pip install cookiecutter
cookiecutter https://github.com/earthdaily/earthdaily-agriculture --directory project_template
# prompts you for project_name, project_slug, environment, python_version, etc.
```

Cookiecutter creates `<project_slug>/` next to your current location, runs the post-generation hook, and you're done.

### Post-init checklist (both flows)

```bash
cd <project_slug>                # if you used A.2

cp .env.template .env            # then open .env in an editor and fill in
                                 # PROD_API_CLIENT_ID, _SECRET, _USERNAME, _PASSWORD

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

git status                       # review the generated files
git add -A
git commit -m "Initialize from earthdaily-agriculture template"
```

The generated layout is documented in [`10 - Project_structure_and_template.md`](10%20-%20Project_structure_and_template.md).

---

## From scratch

Use this when you have an existing Python project or you just want a single notebook to explore the API without the full scaffolding.

```bash
pip install earthdaily-agriculture
```

Set credentials in a `.env` file at your project root:

```env
PROD_API_CLIENT_ID=<your_client_id>
PROD_API_CLIENT_SECRET=<your_client_secret>
PROD_API_USERNAME=<your_username>
PROD_API_PASSWORD=<your_password>
```

Create the workspace directories `WorkflowManager` expects (they'll be auto-created on first run, but you can pre-create them):

```bash
mkdir -p inputs results partials cache logs
```

Then in a notebook or `.py` file:

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager
from earthdaily.agriculture.extractors.coverage_function import CoverageExtractor

manager = WorkflowManager("prod")

# Load entities — either from the EarthDaily platform or a GeoDataFrame
manager.load_seasonfields(sowing_date_gte="2025-07-01", crop_id="WINTER_OSR")

extractor = CoverageExtractor(
    bearer_token=manager.bearer_token,
    token_expiration=manager.token_expiration,
    config=manager.config,
    workflow_ref=manager,
)
extractor.setup_coverage_parameters(
    vegetation_index="NDVI",
    start_date="2025-01-01",
    clear_cover_min=90,
)

results = extractor.process_entity_coverage_bulk_parallel(
    entity_list=manager.sfd_list,
    output_path=manager.output_result_dir,
    prefix="coverage",
    generate_report=True,
)

print(results["results_df"].head())
```

That's a complete extraction — credentials → entities → results in `results/` plus an HTML run report.

---

## Smoke test (both paths)

Inside the freshly-initialised project:

```bash
# 1. Bootstrap smoke test
python -c "from earthdaily.agriculture.notebook_setup import init; init(); print('OK')"

# 2. Single-entity API hit (only works after credentials are in .env)
python -c "from earthdaily.agriculture.services.workflow_manager import WorkflowManager; m = WorkflowManager('prod'); m.load_seasonfields(); print(m.sfd_list.head())"
```

If both print without errors, the project is wired correctly.

---

## What's next

- [`10 - Project_structure_and_template.md`](10%20-%20Project_structure_and_template.md) — walkthrough of the generated project layout, every file's purpose, transform conventions, YAML workflow structure.
- [Working with earthdaily-agriculture](11%20-%20Working%20with%20EDAgro%20client.md) — day-to-day recipes: `WorkflowManager` patterns, DEBUG logging, common pitfalls.
- [`03 - Extractor_parameters_reference.md`](03%20-%20Extractor_parameters_reference.md) — every `setup_*_parameters()` argument for every extractor.
- [`09 - Workflow_architecture.md`](09%20-%20Workflow_architecture.md) — multi-step YAML pipelines with transforms.

---

## Common pitfalls

- **Template not found** (Path A.1). The script lists where it looked when it fails. If you have a local clone you'd prefer to use, pass `--template <path>` or set `EDAGRO_CLIENT_PATH`. Otherwise the script falls back to the public GitHub URL — make sure you have network access.
- **`project_slug` doesn't match folder name** (Path A.2). Path A.1 guarantees alignment automatically (`no_input=True`); Path A.2 can drift if you over-edit the slug prompt. Stick with the default slug derivation unless you have a reason.
- **`'secrets' is undefined` Jinja error during cookiecutter render.** The template wraps GitHub Actions YAML in `{% raw %}…{% endraw %}` to keep Jinja from evaluating it. If you hit the error, pull the latest version of the template.
- **Corrupted generated notebook** (Path A.2 with a backslash path on Windows). If you manually answer the `edagro_source_path` prompt with a Windows-style backslash path (e.g. `C:\Users\…\src`), cookiecutter substitutes the raw backslashes into the generated notebook JSON, producing invalid escape sequences. Use **forward slashes** instead (`C:/Users/…/src`) — Python's `pathlib.Path` handles them fine on Windows. The defaults in `cookiecutter.json` are already forward-slash form, so just accept them. Path A.1's `init_project.py` normalises automatically.
- **Post-gen hook fails silently.** It logs a warning and continues so the project is still created. Re-run manually once the project venv is active:
  ```bash
  python -m earthdaily.agriculture.ai_enablement.generate_ai_context --project-target <project> --project-name "<name>" --environment <env>
  ```
- **Python version.** 3.10 through 3.13 are all tested in CI. Anything newer is untested — if you hit an install or import error on 3.14+, drop to 3.12.x, which is what release wheels are built on.
