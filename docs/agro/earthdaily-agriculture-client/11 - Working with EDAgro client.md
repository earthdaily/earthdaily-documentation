---
title: Working with earthdaily-agriculture
description: Practical day-to-day guide — WorkflowManager patterns, DEBUG logging, entity loading, caching, transforms.
#icon: material/console
keywords:
  - workflow manager
  - debug logging
  - examples
  - recipes
  - bulk extraction
  - transforms
---

# Working with earthdaily-agriculture

Practical recipes for the most common day-to-day patterns: debugging an extractor that returns empty results, loading entities from a file vs. the platform, driving a single extractor vs. a full YAML workflow, wiring the cache, and the standard notebook bootstrap.

For getting started, see [`01 - Quick_Start_Guide.md`](01%20-%20Quick_Start_Guide.md). For the architectural rationale behind `WorkflowManager` and the transform pattern, see [`09 - Workflow_architecture.md`](09%20-%20Workflow_architecture.md).

---

## Tip — Use `log_level="DEBUG"` to surface every API request and response

Every extractor sprinkles `logger.debug(...)` calls on the API call path. At the default `INFO` level they stay silent; flipping to `DEBUG` makes them visible and gives you:

- The full API URL being called (endpoint + query string)
- The request payload (geometry, filters, parameters)
- The raw JSON response coming back

This is the fastest way to answer "why did I get empty results?" or "is my date actually making it to the API?".

### Enabling DEBUG

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager

manager = WorkflowManager(
    "prod",
    log_level="DEBUG",          # flip from the default "INFO"
    log_to_console=True,        # keep stderr output so you see it live
)
```

Logs also land in `logs/earthdaily_<YYYY-MM-DD>.log` (daily rotation, 30-day retention) — useful for post-mortem inspection when you don't want console noise during a long run.

### What DEBUG actually prints

Sampling a few extractors:

| Extractor             | Module                                  | DEBUG output                                                          |
| --------------------- | --------------------------------------- | --------------------------------------------------------------------- |
| `CoverageExtractor`   | `extractors.coverage_function`          | `API URL: …`, `Payload: …`, `API response: …`                          |
| `cropidExtractor`     | `extractors.cropid_functions`           | URL, filters (`begin_year`–`end_year`, `mask_type`), payload, response |
| `WeatherExtractor`    | `extractors.weather_functions`          | `Entity <id>: API URL: …`, `Entity <id>: API response: …`              |

Every other extractor follows the same pattern. If a call is silent at DEBUG, the extractor likely short-circuited before reaching the HTTP layer (e.g. missing required entity field).

### When to turn it off

DEBUG is verbose — each bulk run can produce tens of megabytes of logs. Leave it at `INFO` by default and flip to DEBUG only while diagnosing a specific entity or a failing extractor.

### Scoping DEBUG to a single call

If you want DEBUG just for one manual `get_*_api()` inspection without re-instantiating the manager, override loguru directly:

```python
import sys
from loguru import logger

logger.remove()
logger.add(sys.stderr, level="DEBUG")
```

Then run your single call and restore `INFO` when done.

---

## Using `WorkflowManager`

`WorkflowManager` is the single entry point for any extraction: it handles authentication, entity loading, path resolution, cache configuration, and — optionally — orchestration of a multi-step pipeline defined in YAML.

### Initialisation

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager

manager = WorkflowManager(
    env="prod",              # "prod" | "preprod" (reads from ENVIRONMENT env var if omitted)
    log_level="INFO",        # "TRACE" | "DEBUG" | "INFO" | "WARNING" | "ERROR"
    log_to_console=True,     # stream loguru to stderr
    project_root=None,       # override the auto-detected project root
)
```

On construction the manager:

1. Loads `.env`, resolves credentials for the chosen environment.
2. Authenticates and stores `manager.bearer_token` + `manager.token_expiration`.
3. Resolves workspace paths: `manager.config["output_result_dir"]`, `partial_result_dir`, `cache_dir`, `logs_dir`.
4. Sets up loguru file logging at `logs/earthdaily_<date>.log`.

### Key attributes you'll touch

| Attribute                                          | What it is                                                                        |
| -------------------------------------------------- | --------------------------------------------------------------------------------- |
| `manager.bearer_token` / `manager.token_expiration` | Current OAuth token — pass to extractors built manually                            |
| `manager.config`                                   | Dict with `env`, paths, and optional cache settings (`use_cache`, `cache_dir`, `cache_ttl_days`) |
| `manager.sfd_list`                                 | DataFrame of currently loaded entities (set by `load_seasonfields*` / `load_sfd_list`) |
| `manager.output_result_dir`                        | Final-results directory (absolute)                                                |
| `manager.partial_result_dir`                       | Intermediate bulk partials directory (absolute)                                    |

---

## Example 1 — Direct extractor mode (most common)

Use `WorkflowManager` purely for auth + config, then instantiate and run one extractor manually. This is the idiomatic pattern for notebook work and ad-hoc extractions.

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager
from earthdaily.agriculture.extractors.coverage_function import CoverageExtractor

manager = WorkflowManager("prod", log_level="INFO")

# Load entities from the EarthDaily platform
manager.load_seasonfields()

# Build the extractor — pass the manager as workflow_ref so token refresh is delegated
extractor = CoverageExtractor(
    manager.bearer_token,
    manager.token_expiration,
    config=manager.config,
    workflow_ref=manager,
)

extractor.setup_coverage_parameters(
    vegetation_index="NDVI",
    start_date="2025-01-01",
    clear_cover_min=80,
    filter="duplicate",
    column_mapping={"crop": "crop.id"},
)

results = extractor.process_entity_coverage_bulk_parallel(
    entity_list=manager.sfd_list.head(50),
    max_workers=10,
    output_path=manager.output_result_dir,
    prefix="coverage",
)

df = results["results_df"]
print(df.shape, df.columns.tolist())
```

---

## Example 2 — Loading entities from a file

`load_sfd_list()` accepts shapefile, parquet, geojson, gpkg, and CSV. Populates `manager.sfd_list`.

```python
from earthdaily.agriculture.core.geometry import load_geodataframe

manager = WorkflowManager("prod")
manager.sfd_list = load_geodataframe("inputs/my_fields.parquet")

print(f"Loaded {len(manager.sfd_list)} entities")
```

For very large platform extractions, use the batch variant which pages the MDM API 5 000 rows at a time:

```python
manager.load_seasonfields_batch(
    start_date="2025-01-01",
    end_date="2025-12-31",
    crop_id=123,
    batch_size=5000,
)
```

---

## Example 3 — Full YAML-driven workflow

Write a multi-step pipeline in `configuration/workflow.yml`, load it, visualise it, run it.

```yaml
# configuration/workflow.yml
workflow:
  name: "Weather + NDVI pipeline"

  settings:
    max_workers: 10
    partial_frequency: 50
    column_mapping:
      crop: crop.id
      start_date: sowingDate
      end_date: endDate

  steps:
    - name: weather_hist
      extractor: WeatherExtractor
      module: earthdaily.agriculture.extractors.weather_functions
      setup:
        method: setup_weather_parameters
        params:
          weather_type: HISTORICAL_DAILY
          weather_parameters:
            - Temperature.standardmax
            - Temperature.standardmin
            - precipitation.cumulative
      run:
        method: process_entity_weather_bulk_parallel
        params:
          prefix: weather_hist
          skip_export: true

    - name: mrts_ndvi
      extractor: MRTSExtractor
      module: earthdaily.agriculture.extractors.VTS_functions
      setup:
        method: setup_mrts_parameters
        params:
          vegetation_index: NDVI
          clear_cover_min: 95
          mode: full
      run:
        method: process_mrts_bulk_parallel
        params:
          prefix: mrts_ndvi
          skip_export: true

    - name: merge_report
      depends_on:
        - weather_hist
        - mrts_ndvi
      transform:
        module: app.transforms
        function: build_report
        params:
          weather_step: weather_hist
          ndvi_step: mrts_ndvi
          output_csv: results/report.csv
```

Driver code:

```python
manager = WorkflowManager("prod")
manager.load_seasonfields()

manager.load_workflow("configuration/workflow.yml")
manager.visualize_workflow()     # prints the dependency DAG

results = manager.run_workflow(entity_list=manager.sfd_list)

for step, payload in results.items():
    df = payload.get("results_df")
    errs = payload.get("global_errors", [])
    print(f"{step:20s} rows={len(df):>6} errors={len(errs)}")
```

`manager.run_workflow(...)` executes steps in dependency order, feeds each extractor's output into the cache (if enabled), and hands upstream results to any `transform` step via `upstream_results`.

---

## Example 4 — Enabling the shared cache across a workflow

Set cache flags on `manager.config` before calling `load_workflow()` — every extractor the workflow instantiates inherits them.

```python
manager = WorkflowManager("prod")
manager.config["use_cache"] = True
manager.config["cache_dir"] = "cache"         # relative to project root
manager.config["cache_ttl_days"] = 7

manager.load_workflow("configuration/workflow.yml")
results = manager.run_workflow(entity_list=entities)
```

Re-running with the same entities replays from parquet; per-call override `use_cache=False` still forces a refresh for a single step. Full reference: [`07 - Cache_design_context.md`](07%20-%20Cache_design_context.md).

---

## Example 5 — Transform-only step (no API call)

Transforms are lightweight Python functions that reshape upstream results into a downstream input. They live in `app/transforms.py` and must follow the canonical signature:

```python
# app/transforms.py
import pandas as pd

def drop_small_fields(entity_list, upstream_results, params) -> pd.DataFrame:
    """Keep only fields above a minimum area (from a prior coverage step)."""
    min_area = params.get("min_area_sqm", 10_000)
    coverage_df = upstream_results[params["coverage_step"]]["results_df"]
    large_ids = coverage_df.loc[coverage_df["area_sqm"] >= min_area, "id"].unique()
    return entity_list[entity_list["id"].isin(large_ids)].reset_index(drop=True)
```

Wire it in the YAML:

```yaml
    - name: filter_small
      depends_on: coverage
      transform:
        module: app.transforms
        function: drop_small_fields
        params:
          coverage_step: coverage
          min_area_sqm: 20000
```

Downstream steps that `depends_on: filter_small` will receive the filtered entity list automatically.

---

## Example 6 — Driving from a notebook with the standard bootstrap

Every notebook starts with the same bootstrap cell followed by a `WorkflowManager` constructor:

```python
# Cell 1 — bootstrap
from earthdaily.agriculture.notebook_setup import init
init()

# Cell 2 — manager + entities
from earthdaily.agriculture.services.workflow_manager import WorkflowManager

manager = WorkflowManager("prod", log_to_console=False, log_level="WARNING")
manager.load_seasonfields()
```

From here you can either go direct-extractor (Example 1) or load a YAML (Example 3).

---

## Common pitfalls

- **Token expiry during long runs.** Extractors built with `workflow_ref=manager` automatically refresh the token. Extractors built without it will fail after ~1 hour.
- **Entity DataFrame column names.** If your data uses `sowingDate` / `crop.id` (platform output) or anything custom, set `column_mapping` either at `setup_*_parameters()` time or under `workflow.settings.column_mapping` (applies to every step). See [`04 - Extractor_column_mapping_reference.md`](04%20-%20Extractor_column_mapping_reference.md).
- **Empty results but no error.** Flip `log_level="DEBUG"` to see the actual API response. Often it reveals a geometry rejection or a missing required field (e.g. LAI extraction requires `crop`).
- **`clear_cover_min=100`** is very restrictive — most extractions want 80–95.
- **Per-entity date overrides.** Some extractors honour per-entity dates carried in the DataFrame; some don't. See [`06 - Edagro_date_overwrite.md`](06%20-%20Edagro_date_overwrite.md) for the per-extractor matrix.
