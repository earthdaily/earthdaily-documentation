---
title: Workflow architecture
description: The three-layer model — YAML configuration, transform layer, extractors — that keeps business logic out of ad-hoc notebook cells.
#icon: material/sitemap-outline
keywords:
  - workflow
  - transforms
  - architecture
  - steps
  - business logic
  - WorkflowManager
---

# Workflow Architecture — Steps, Transforms, and Business Logic Isolation

## The Problem

Extractors are generic API wrappers: they fetch data from EarthDaily APIs, format responses into DataFrames, and handle retries, logging, and caching. They know nothing about business context.

Real-world analytics pipelines are never single-step. They chain multiple extractors where the output of one feeds the input of the next. The data flowing between extractors often needs reshaping, filtering, enrichment, or aggregation that is specific to the business use case.

Without a structured approach, this glue logic ends up in notebook cells — ad-hoc, non-reproducible, non-portable code that breaks when the notebook is re-run out of order.

## The Solution: Three-layer Architecture

```
┌─────────────────────────────────────────────────────────┐
│  YAML Workflow Configuration                            │
│  (pipeline definition, parameters, dependencies)        │
├─────────────────────────────────────────────────────────┤
│  Transform Layer (app/)                                 │
│  (business logic: reshape, enrich, aggregate, filter)   │
├─────────────────────────────────────────────────────────┤
│  Extractor Layer (earthdaily/agriculture/)                        │
│  (generic API wrappers: fetch, format, retry, cache)    │
└─────────────────────────────────────────────────────────┘
```

| Layer | Location | Responsibility | Reusable across projects? |
|---|---|---|---|
| **Extractors** | `earthdaily/agriculture/extractors/`, `earthdaily/agriculture/processors/` | Generic API wrapper. Fetch, format, return DataFrame. | Yes (shared package) |
| **Transforms** | `app/` (per project) | Business logic adapter. Reshape upstream outputs into downstream inputs. | No (project-specific) |
| **Workflow YAML** | `configuration/` (per project) | Pipeline definition. Steps, dependencies, parameters. | No (project-specific) |

## Core Design Principle: Low Adherence Between Extractors and Business Logic

**Generic extractors and business logic must stay decoupled.** An extractor should never import from `app/`, reference a client name, or encode assumptions about a specific pipeline. Business logic (crop-specific rules, client-specific filters, pipeline-specific reshaping) lives exclusively in the transform layer.

This low-adherence boundary is the single most important property of the architecture. When it is respected:

- Extractors are shared safely across clients and pipelines — changes to one project cannot break another.
- Business rules can evolve per-client without forking the `earthdaily.agriculture` package.
- The extractor layer remains a thin, testable API wrapper that matches the underlying EarthDaily service contract.

When it is violated (business logic leaks into an extractor, or an extractor is bypassed by ad-hoc API calls in a transform), the package drifts toward a tangled monolith where every client-specific change risks regressions elsewhere. Treat the `earthdaily/agriculture/` ↔ `app/` boundary as a hard contract, not a convention.

## Why Isolate Business Logic in Transforms

### Extractors stay generic

An extractor should work with any entity list that has the required fields. It should not know about CropID results, event dates, or sensor priority rankings. By keeping this logic in transforms, we can:

- Use the same `CoverageExtractor` in a fertilizer zoning pipeline, an impact assessment pipeline, and a crop monitoring pipeline
- Update an extractor without breaking any specific pipeline
- Test extractors in isolation with minimal mock data

### Transforms are testable

A transform is a pure function: DataFrame in, DataFrame out, no API calls, no side effects. This makes them easy to:

- Unit test with mock upstream results
- Debug by inspecting input and output DataFrames
- Reuse across similar pipelines (e.g., `use_upstream_entities` is used in every project)

### Workflows are declarative

The YAML configuration describes **what** to do, not **how** to do it. This makes pipelines:

- Readable by non-developers (parameters are explicit, dependencies are visible)
- Versionable (YAML changes are easy to diff in git)
- Portable (move a YAML + transforms to a new project)

## Workflow Execution Model

### Step Types

A workflow step can be one of three types:

**1. Extractor step** — Makes API calls to fetch data

```yaml
- name: coverage
  extractor: CoverageExtractor
  module: earthdaily.agriculture.extractors.coverage_function
  setup:
    method: setup_coverage_parameters
    params: { vegetation_index: NDVI, start_date: "2025-01-01" }
  run:
    method: process_entity_coverage_bulk_parallel
    params: { prefix: coverage, skip_export: true }
```

**2. Transform-only step** — Reshapes data without API calls

```yaml
- name: image_selection
  depends_on: coverage
  transform:
    module: app.my_transforms
    function: select_best_images
    params: { depends_on: coverage, max_images: 3 }
```

**3. Combined step** — Transform prepares entities, then extractor processes them

```yaml
- name: zoning
  depends_on: image_selection
  extractor: ZoningExtractor
  module: earthdaily.agriculture.extractors.zoning_functions
  setup:
    method: setup_zoning_parameters
    params: { num_zones: 5 }
  run:
    method: process_entity_zoning_bulk_parallel
    params: { prefix: zoning }
```

By default, a step with `depends_on` receives the upstream step's `results_df`
as its entity list (see *Step Input Resolution* below). A no-op
`use_upstream_entities` transform is no longer required for this case.

### Step Input Resolution

Each step declares (explicitly or implicitly) which DataFrame it receives as
its `entity_list`. Use the `input_from` field on a step to control this:

| `input_from` value     | Behavior                                                                     |
|------------------------|------------------------------------------------------------------------------|
| `"original"`           | Use the `entity_list` passed to `run_workflow()`.                            |
| `<step_name>` (string) | Use `workflow_results[step_name]["results_df"]` as the entity list.          |
| omitted                | Default to the first `depends_on` if present, else `"original"`.             |

A `transform` (if defined) still runs on top of the resolved entity list — a
step can declare both `input_from: mrts_field` and a transform that further
reshapes that DataFrame.

`load_workflow()` validates `input_from` at load time:
- value must be `"original"` or a string matching another step's `name`
- the referenced step must appear in an *earlier* execution level (cannot
  reference itself, a parallel step, or a later step)

```yaml
# Auto-chains to mrts_field's results_df via the depends_on default
- name: coverage
  depends_on: mrts_field
  extractor: CoverageExtractor
  ...

# Explicit override — receives upstream results from a non-immediate ancestor
- name: zoning
  depends_on: image_selection
  input_from: cropid
  extractor: ZoningExtractor
  ...

# Force original entity_list even though there is a depends_on (purely for ordering)
- name: weather
  depends_on: cropid
  input_from: original
  extractor: WeatherExtractor
  ...
```

> **Migration note.** Prior to this field, every chained step needed a no-op
> `use_upstream_entities` transform to swap the `entity_list` with the upstream's
> `results_df`. With the default-to-first-`depends_on` behavior, that transform
> is redundant and can be removed. Existing YAMLs that have `depends_on` without
> `use_upstream_entities` AND rely on receiving the *original* entity_list must
> add `input_from: "original"` explicitly.

### Execution Flow

```
For each step (in dependency order):

1. Resolve dependencies
   └── Ensure all depends_on steps have completed

2. Run transform (if defined)
   └── transform_func(entity_list, upstream_results, params) -> modified_entity_list

3. If extractor is defined:
   │  a. Instantiate extractor class
   │  b. Call setup method with params
   │  c. Call run method with modified_entity_list
   │  d. Store results in upstream_results[step_name]
   │
   └── If no extractor (transform-only):
      └── Store transform output as results_df in upstream_results[step_name]
```

### Data Flow Between Steps

```
entity_list ──────────────────────────────────────────────────────────────>
     │                                                                    │
     ▼                                                                    ▼
[Step 1: Coverage]                                               [Final results]
     │
     │ results_df (image catalog)
     │
     ▼
[Step 2: Image Selection] ← transform reads coverage results
     │
     │ results_df (entities + image_id_1, image_id_2)
     │
     ▼
[Step 3: Difference] ← transform passes entities, extractor calls API
     │
     │ results_df (entities + difference stats)
     │
     ▼
[Step 4: Impact Analysis] ← transform reads difference results
     │
     └─ results_df (entities + impact metrics)
```

The `upstream_results` dict accumulates all completed step outputs. Any transform can read from any completed upstream step, not just the immediate dependency.

## Transform Contract

### Function Signature

```python
def my_transform(
    entity_list: pd.DataFrame,
    upstream_results: dict[str, dict],
    params: dict,
) -> pd.DataFrame:
```

| Argument | Type | Content |
|---|---|---|
| `entity_list` | DataFrame | Original input entities for the workflow |
| `upstream_results` | dict | `step_name -> {"results_df": DataFrame, "global_errors": list, "failed_ids": list}` |
| `params` | dict | Transform-specific parameters from YAML |
| **Returns** | DataFrame | Modified entity list for the next step |

### Rules

1. **Pure function** — No side effects, no API calls, no file I/O. Only reshape data.
2. **Returns a DataFrame** — The runner passes it to the step's extractor (or stores it as-is for transform-only steps).
3. **Handles empty gracefully** — If upstream results are empty, return `entity_list.iloc[0:0]` (empty DataFrame with correct schema).
4. **Logs via loguru** — Use `logger.info()` for progress, `logger.warning()` for dropped entities.
5. **Raises on misconfiguration** — If `depends_on` step is missing or required params are absent, raise `ValueError`.

### Common Transform Patterns

#### Pass-through
Use the results of a previous step as the entity list for the next extractor. This is the most common pattern when a transform-only step enriches entities that a downstream extractor needs.

```python
def use_upstream_entities(entity_list, upstream_results, params):
    source = params["depends_on"]
    return upstream_results[source]["results_df"]
```

#### Enrichment
Add columns from upstream results onto entity_list. Used when an extractor produces metadata (e.g., crop years) that a downstream step needs.

```python
def enrich_with_seasons(entity_list, upstream_results, params):
    cropid_df = upstream_results["cropid"]["results_df"]
    seasons = cropid_df.groupby("id")["year"].apply(sorted_list).reset_index()
    return entity_list.merge(seasons, on="id", how="inner")
```

#### Selection
Pick the best items from a large result set. Used to select optimal images, best crop years, or top-ranked entities.

```python
def select_best_images(entity_list, upstream_results, params):
    cov_df = upstream_results["coverage"]["results_df"]
    best = cov_df.sort_values("coverage_percent", ascending=False).drop_duplicates("id")
    return entity_list.merge(best[["id", "image_id"]], on="id", how="inner")
```

#### Aggregation
Compute summary statistics from detailed upstream results. Used for post-processing: impact metrics, productivity indices, risk scores.

```python
def compute_impact(entity_list, upstream_results, params):
    diff_df = upstream_results["difference"]["results_df"]
    # Sum impacted pixels per entity from range columns
    metrics = calculate_impact_per_entity(diff_df, threshold=params["threshold"])
    return entity_list.merge(metrics, on="id", how="inner")
```

#### Splitting
Partition upstream results into groups for parallel downstream processing. Used when one result set feeds multiple extractors (e.g., zone-level analysis).

```python
def prepare_zone_entities(entity_list, upstream_results, params):
    zoning_df = upstream_results["zoning"]["results_df"]
    # One row per zone with zone_entity_id and zone_geometry
    zoning_df["zone_entity_id"] = zoning_df["id"] + "__zone_" + zoning_df["zone_name"]
    return zoning_df
```

## Real-World Examples

### Fertilizer Optimized Placement

```
CropID → Coverage → Image Selection → Zoning → Aggregation → Export
```

Transforms:
- `enrich_with_historical_seasons` — CropID years to per-entity list
- `smart_crop_coverage` — Select top N images per year with sensor priority
- `use_upstream_entities` — Pass enriched entities to ZoningExtractor
- `prepare_zone_entities_for_mrts` — Create zone-level entity IDs for MRTS
- `enrich_with_aggregation` — Spatial join with township boundaries
- `export_workflow_results` — Export to parquet/CSV with manifest

### Impact Assessment

```
Coverage → Image Selection → Difference Map → Impact Analysis
```

Transforms:
- `select_before_after_images` — Split coverage into before/after event date
- `use_upstream_entities` — Pass image pairs to DifferenceExtractor
- `compute_impact_metrics` — Classify impacted area from difference ranges

## Dependencies and DAG

Steps declare dependencies with `depends_on`. The WorkflowManager resolves the dependency graph into a directed acyclic graph (DAG) and executes steps in topological order.

```yaml
steps:
  - name: a                     # No dependency → runs first
  - name: b
    depends_on: a               # Runs after a
  - name: c
    depends_on: a               # Runs after a (parallel with b if supported)
  - name: d
    depends_on: [b, c]          # Runs after both b and c complete
```

Visualize the DAG with:

```python
manager.load_workflow("configuration/my_workflow.yml")
manager.visualize_workflow().show()   # interactive Plotly figure
```

`visualize_workflow()` returns a `plotly.graph_objects.Figure`. Nodes are placed left→right by topological level; node color encodes role (transform-only / extractor / both). Hover over a node to see its `depends_on`, resolved `input_from`, transform, extractor, setup/run params, and condition.

## Run reporting

`run_workflow` accepts an opt-in `generate_report=True` kwarg that wires up a `WorkflowRunReporter` for the run. The manager builds the reporter, populates its context from the loaded YAML (workflow name, `output_prefix`, env, entity count), times the run on the monotonic clock, and after the DAG completes calls `set_step_results(...)` with each step's `results_df` row count, error count, and inferred kind (`extractor` / `transform` / `transform+extractor`). The configured reporter is stashed at `manager.last_run_reporter` so callers can amend its context and render outputs.

```python
manager.load_workflow("configuration/my_workflow.yml")
results = manager.run_workflow(
    entity_list=entities,
    generate_report=True,
    report_options={"parameters": {"limit": 100}},   # surfaces in the JSON receipt
)

# The reporter doesn't know report_path yet — typically the consumer builds
# the final per-field CSV downstream and amends it before rendering.
final_csv = export_final_report(results, "results/run.csv")
reporter = manager.last_run_reporter
reporter.amend_run_context(report_path=str(final_csv))

reporter.render_html(output_path="results/run.html")
receipt = reporter.render_json(output_path="results/run.json")
```

The JSON receipt is `schema_version: 1` — `{workflow, entities, duration_seconds, report_path, steps[], errors[]}` — designed to feed Slack notifications, S3 archives, or downstream dashboards without per-project shaping. Full reference lives in [`12 - AI enablement.md`](12%20-%20AI%20enablement.md) → "Layer 2 — `/earthdaily-agriculture` skill" alongside the extractor-level `ExtractionReporter`.

**Opt-in defaults:**

- `generate_report=False` → byte-identical to before; `manager.last_run_reporter` is set to `None`.
- `generate_report=True` with no `report_options` → reporter populated, no `parameters` / `column_mapping` / `resolved_yaml` fields in the receipt. Render whenever you're ready.
- Mid-run exception → `manager.last_run_reporter` is still populated with the steps that completed before the failure, so a partial report can be rendered for forensics.

`report_options` accepted keys (typos raise):

- **Constructor knobs:** `include_step_table`, `include_data_preview`, `preview_rows`, `max_errors_shown`.
- **Run-context fields:** `parameters`, `column_mapping`, `resolved_yaml`.

The reporter is YAML-agnostic — there is no `reporting:` block in the workflow YAML. Reporting is a run-time concern (callers may want different shapes per invocation), not a workflow-config concern.

## Best Practices

### Keep extractors generic (low adherence)
Never add business logic to an extractor. If you need to filter, reshape, or compute derived columns, write a transform. Extractors must not import from `app/`, hardcode client names, or assume a specific pipeline shape — if you feel tempted to, that logic belongs in a transform. Low adherence between `earthdaily/agriculture/` and `app/` is what lets the shared package stay stable across clients.

### One transform per concern
Each transform should do one thing. Prefer three simple transforms over one complex one. They are easier to test, debug, and recombine.

### Use `depends_on` in params
Always pass `depends_on` in transform params so the function knows which upstream step to read from. This keeps transforms decoupled from step names.

```yaml
transform:
  module: app.transforms
  function: my_transform
  params:
    depends_on: coverage    # Explicit — not hardcoded in the function
```

### Log entity counts
At the end of every transform, log how many entities survived (vs. input). This makes debugging pipeline drop-off easy.

```python
logger.info(f"  Entities with valid pairs: {len(result)}/{len(entity_list)}")
```

### Test transforms in isolation
Transforms are pure functions. Test them with mock DataFrames without needing API access:

```python
def test_select_images():
    entities = pd.DataFrame({"id": ["a", "b"], "geometry": ["...", "..."]})
    mock_results = {"coverage": {"results_df": mock_coverage_df}}
    result = select_before_after_images(entities, mock_results, params)
    assert "image_id_1" in result.columns
    assert "image_id_2" in result.columns
```

### Prefer YAML workflow over notebook cells
If a pipeline will be run more than once, encode it in YAML. Notebook cells are for exploration; YAML workflows are for reproducible execution.
