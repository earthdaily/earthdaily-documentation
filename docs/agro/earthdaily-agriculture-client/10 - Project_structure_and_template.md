---
title: Project structure and template
description: The canonical project layout for an earthdaily-agriculture extraction project, what each directory holds, and how the YAML workflows + transform layer fit together.
#icon: material/folder-multiple-outline
keywords:
  - project structure
  - cookiecutter
  - app
  - transforms
  - workflow yaml
  - layout
---

# Project structure

Projects built around `earthdaily-agriculture` follow a standard layout that separates configuration, business logic, data, and execution. The cookiecutter template at [`project_template/`](https://github.com/earthdaily/earthdaily-agriculture/tree/main/project_template) scaffolds this layout for you, but the convention is just as useful if you want to wire up a project by hand.

## Standard layout

```
my_project/
├── .env                              # Credentials (gitignored, copy from .env.template)
├── .env.template                     # Credential template
├── requirements.txt                  # Pins `earthdaily-agriculture==X.Y.Z` and your project deps
├── README.md                         # Project-specific docs
│
├── app/                              # Project-specific business logic
│   ├── __init__.py
│   └── my_transforms.py              # Transform functions between workflow steps
│
├── configuration/                    # YAML workflow definitions
│   └── my_workflow.yml               # Multi-step pipeline configuration
│
├── docs/                             # Guides, copied in when the project is scaffolded
│   ├── 01 - Quick_Start_Guide.md     # ... the numbered reference set
│   └── study/                        # Your exploratory / service-delivery notebooks
│
├── inputs/                           # Input data (shapefiles, parquet, CSV)
├── results/                          # Final extraction outputs
├── partials/                         # Intermediate bulk processing results
├── cache/                            # Entity extraction cache (when enabled)
├── logs/                             # Loguru log files (daily rotation)
│
└── EDAgriculture_My_Project.ipynb           # Main execution notebook
```

## Directory reference

| Directory         | Purpose                                                                                                                          | Git-tracked         |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| `app/`            | Transform functions that adapt extractor outputs into downstream inputs. Each function follows the standard transform signature. | Yes                 |
| `configuration/`  | YAML workflow definitions. Each file describes a multi-step pipeline with dependencies, extractors, transforms, and parameters.   | Yes                 |
| `docs/`           | The numbered guides, **copied from the `earthdaily-agriculture` repo at scaffold time** rather than vendored in the template — so they match the version you generated from. Re-scaffolding overwrites them; keep your own writing in `docs/study/`. | Yes                 |
| `docs/study/`     | Yours. Exploratory and service-delivery work — coverage checks, zonal stats, custom maps, the notebook that answers a client question. Ships empty; never overwritten. | Yes                 |
| `inputs/`         | Input entity data — shapefiles (`.shp`), parquet (`.parquet`), CSV. Geometries and metadata for entities to process.              | Project-dependent   |
| `results/`        | Final outputs — CSV, parquet, TIFF, HTML reports, manifest JSON. Created by extractors and export transforms.                     | No                  |
| `partials/`       | Intermediate results saved during bulk parallel processing. Includes partial CSVs and failed-ID lists. Auto-cleaned on success.   | No                  |
| `cache/`          | Local parquet cache. Avoids re-fetching unchanged entities across runs. See [`07 - Cache_design_context.md`](07%20-%20Cache_design_context.md). | No                  |
| `logs/`           | Dated log files from loguru. Default rotation: daily, retention: 30 days.                                                         | No                  |

## Recommended `.gitignore`

```gitignore
# Credentials
.env

# Output directories
results/
partials/
cache/
logs/

# Python
__pycache__/
*.pyc
.ipynb_checkpoints/

# OS
.DS_Store
Thumbs.db
```

---

## `app/` — Transform functions

Transforms are the **business logic layer** between generic extractors. They reshape, enrich, or aggregate one extractor's output into the format the next one expects.

```
Extractor A  ──>  Transform  ──>  Extractor B
(generic API)    (project-specific)  (generic API)
```

### Function signature

Every transform must follow this contract:

```python
import pandas as pd

def my_transform(
    entity_list: pd.DataFrame,
    upstream_results: dict[str, dict],
    params: dict,
) -> pd.DataFrame:
    """
    Args:
        entity_list:      Original input entities for the workflow.
        upstream_results: Dict mapping step_name -> result_dict. Each result_dict
                          contains:
                            - "results_df": pd.DataFrame
                            - "global_errors": list[dict]
                            - "failed_ids": list[str]
        params:           Transform-specific parameters from YAML.

    Returns:
        Modified entity_list DataFrame for the next step.
    """
```

### Common patterns

**Pass-through** — use upstream results as the entity list for the next extractor:

```python
def use_upstream_entities(entity_list, upstream_results, params):
    source_step = params.get("depends_on")
    return upstream_results[source_step]["results_df"]
```

**Enrichment** — add columns from upstream results onto `entity_list`:

```python
def enrich_entities(entity_list, upstream_results, params):
    source_df = upstream_results[params["depends_on"]]["results_df"]
    new_cols = source_df.groupby("id")["value"].first().reset_index()
    return entity_list.merge(new_cols, on="id", how="inner")
```

**Filtering** — drop entities that don't meet criteria:

```python
def filter_by_status(entity_list, upstream_results, params):
    source_df = upstream_results[params["depends_on"]]["results_df"]
    valid_ids = source_df.loc[source_df["status"] == "confirmed", "id"].unique()
    return entity_list[entity_list["id"].isin(valid_ids)]
```

**Aggregation** — compute summary statistics from upstream results:

```python
def compute_stats(entity_list, upstream_results, params):
    source_df = upstream_results[params["depends_on"]]["results_df"]
    stats = source_df.groupby("id").agg({"value": ["mean", "min", "max"]})
    stats.columns = ["avg_value", "min_value", "max_value"]
    return entity_list.merge(stats.reset_index(), on="id", how="inner")
```

---

## `configuration/` — YAML workflows

### Structure

```yaml
workflow:
  name: "My Workflow"
  description: "What this workflow does"

  settings:
    max_workers: 10
    partial_frequency: 50
    column_mapping:          # Optional: map entity columns to canonical names
      crop: "crop_code"
      start_date: "sowingDate"

  steps:
    - name: step_name
      # ...
```

### Step types

#### Extractor step (API call)

Instantiates an extractor class, configures it, and runs bulk extraction:

```yaml
- name: coverage
  extractor: CoverageExtractor
  module: earthdaily.agriculture.extractors.coverage_function
  setup:
    method: setup_coverage_parameters
    params:
      vegetation_index: NDVI
      start_date: "2025-01-01"
      end_date: "2025-12-31"
      clear_cover_min: 90
  run:
    method: process_entity_coverage_bulk_parallel
    params:
      prefix: coverage
      skip_export: true
```

#### Transform-only step (no API call)

Runs a Python function to reshape data between extraction steps:

```yaml
- name: image_selection
  depends_on: coverage
  transform:
    module: app.my_transforms
    function: select_best_images
    params:
      depends_on: coverage
      max_images: 3
```

#### Combined step (transform + extractor)

Runs a transform to prepare entities, then an extractor on the result:

```yaml
- name: difference
  depends_on: image_selection
  transform:
    module: app.my_transforms
    function: use_upstream_entities
    params:
      depends_on: image_selection
  extractor: DifferenceExtractor
  module: earthdaily.agriculture.extractors.difference_functions
  setup:
    method: setup_difference_parameters
    params:
      product: NDVI
      postprocess: stats
  run:
    method: process_entity_difference_bulk_parallel
    params:
      prefix: difference
      skip_export: true
```

### Dependencies

Steps declare dependencies with `depends_on`. The workflow manager resolves the dependency graph and executes steps in order. A step without `depends_on` runs first.

```yaml
- name: step_a                  # Runs first (no dependency)

- name: step_b
  depends_on: step_a            # Runs after step_a

- name: step_c
  depends_on: step_b            # Runs after step_b
```

Multiple dependencies are supported — pass a list:

```yaml
- name: merge
  depends_on:
    - weather
    - vegetation
```

Full YAML reference: [`09b - Workflow_YAML_reference.md`](09b%20-%20Workflow_YAML_reference.md). Architecture rationale: [`09 - Workflow_architecture.md`](09%20-%20Workflow_architecture.md).

---

## The notebook — execution entry point

### Standard structure

Every project notebook follows this pattern:

| Section                            | Purpose                                                              |
| ---------------------------------- | -------------------------------------------------------------------- |
| Step 0: Environment setup          | Configure `sys.path`, call `init()`                                  |
| Step 1: Initialize WorkflowManager | Create manager, authenticate with EarthDaily Agro API                |
| Step 2: Load entities              | From the platform, a file, or a manually-built DataFrame             |
| Step 3: Manual pipeline (optional) | Run each step individually for inspection and debugging              |
| Step 4: YAML workflow execution    | Automated pipeline via `manager.run_workflow()`                      |
| Step 5: Explore results            | Visualise, analyse, threshold sensitivity                            |
| Step 6: Export                     | Save final results to `results/`                                     |

### Bootstrap cell

Every notebook starts with the same bootstrap cell. After `pip install earthdaily-agriculture` the `sys.path` block becomes unnecessary; the `init()` call handles working-directory and `.env` loading either way:

```python
# Step 0 — Environment setup
from earthdaily.agriculture.notebook_setup import init
init()
```

`init()`:

1. Walks up from the notebook's location to find the project root (the folder containing `pyproject.toml` or `.env`).
2. Sets `cwd` to that root so relative paths work correctly.
3. Loads `.env` so credentials are available to `WorkflowManager`.

---

## Creating a new project by hand

If you don't want to use the cookiecutter template (Path A in [`01 - Quick_Start_Guide.md`](01%20-%20Quick_Start_Guide.md)), the layout is short enough to build manually:

1. **Create the directory structure:**
   ```bash
   mkdir -p my_project/{app,configuration,inputs,results,partials,cache,logs}
   touch my_project/app/__init__.py
   cd my_project
   ```

2. **Configure credentials:**
   ```bash
   cat > .env <<EOF
   PROD_API_CLIENT_ID=<your_client_id>
   PROD_API_CLIENT_SECRET=<your_client_secret>
   PROD_API_USERNAME=<your_username>
   PROD_API_PASSWORD=<your_password>
   EOF
   ```

3. **Create `requirements.txt`:**
   ```
   earthdaily-agriculture==X.Y.Z
   pandas>=2.2
   numpy>=2.0
   geopandas>=1.0
   shapely>=2.0
   matplotlib>=3.10
   plotly>=6.0
   loguru>=0.7
   python-dotenv>=1.0
   pyyaml>=6.0
   jupyter>=1.0
   ipykernel>=6.28
   ```

4. **Write transforms** in `app/my_transforms.py` following the standard signature.

5. **Write a workflow YAML** in `configuration/my_workflow.yml`.

6. **Create a notebook** `EDAgriculture_My_Project.ipynb` following the standard section structure.

### Checklist

- [ ] Directory structure created (`app/`, `configuration/`, `inputs/`, `results/`, etc.)
- [ ] `.env` configured with API credentials
- [ ] `requirements.txt` pins `earthdaily-agriculture==X.Y.Z` and your project deps
- [ ] `app/__init__.py` exists
- [ ] Transform functions follow `(entity_list, upstream_results, params) -> DataFrame`
- [ ] YAML workflow steps have correct `module`, `extractor`, `setup`, `run` fields
- [ ] YAML transform steps reference functions in `app/` with correct `module` and `function`
- [ ] Notebook bootstrap cell calls `init()` from `earthdaily.agriculture.notebook_setup`
- [ ] `.gitignore` excludes `results/`, `partials/`, `cache/`, `logs/`, `.env`
