---
title: Workflow YAML reference
description: Field-by-field reference for the workflow YAML consumed by WorkflowManager.load_workflow() and run_workflow().
#icon: material/file-code-outline
keywords:
  - workflow yaml
  - configuration
  - steps
  - settings
  - WorkflowManager
  - run_workflow
---

# Workflow YAML Reference

Companion to `08 - Workflow_architecture.md`. This document is a field-by-field reference for the YAML configuration consumed by `WorkflowManager.load_workflow()` and executed by `run_workflow()`.

## File Layout

A workflow YAML has a single top-level `workflow` key containing metadata, global settings, and an ordered list of steps.

```yaml
workflow:
  name: "My Pipeline"
  description: "What this workflow does"

  settings:
    max_workers: 10
    partial_frequency: 100
    max_parallel_steps: 4
    fail_safe: false
    column_mapping:
      id: field_id
      geometry: wkt

  steps:
    - name: step_a
      extractor: ...
    - name: step_b
      depends_on: step_a
      transform: ...
```

## Key reference

Every key `WorkflowManager` reads, generated from `services/workflow_schema.py`. `load_workflow()` warns, with a suggestion, about any key not listed here (an error in 3.0); an extra `settings` key is fine when a step's setup method accepts it.

<!-- BEGIN GENERATED: workflow-keys (generate_ai_context.py from services/workflow_schema.py; do not edit) -->

### `workflow:` (top level)

| Key | Type | What it does |
|---|---|---|
| `name` | str | workflow name, shown in logs and reports |
| `description` | str | free text |
| `settings` | settings block | defaults for every step (see settings) |
| `steps` | list of step block | the steps, required (see step) |
| `entity_source` | entity_source block | free-form block for your own entity loading; date sentinels in its params are rewritten |

### `settings:`

| Key | Type | What it does |
|---|---|---|
| `column_mapping` | mapping | canonical field -> your column (id, geometry, crop, ...); GLOBAL: no per-step override |
| `export_format` | `csv` or `parquet` | csv (default) or parquet, for every step; a step-level key overrides it |
| `export_manifest` | bool | also write a `<prefix>_manifest_<ts>.json` next to each export |
| `fail_safe` | bool | record per-entity failures in failed_ids instead of raising (default false) |
| `max_parallel_steps` | int | independent steps run at once within a DAG level (default 4) |
| `max_workers` | int | default threads per step (default 10) |
| `output_prefix` | str | prefix for every output file name of the run |
| `output_uri` | str | second, durable copy of FLM / Difference / Zoning map files (s3:// gs:// az://) |
| `retry_failed_only` | bool or str | process only the ids in the newest (true) or the named `failed_ids_<prefix>_*.csv` |
| `timezone` | str | IANA zone for the 'today' date sentinels (default UTC) |

### `steps:` items

| Key | Type | What it does |
|---|---|---|
| `name` | str | unique step id, required; referenced by depends_on / input_from |
| `enabled` | bool | false loads the step but skips it; dependents cascade-skip (default true) |
| `depends_on` | str or list of str | step name(s) that must finish first; drives the DAG |
| `input_from` | str | 'original' or a step name: whose results_df becomes this step's entity_list |
| `transform` | transform block | a function run first on the entities (before condition and extractor; see transform) |
| `condition` | condition block | after the transform, keep only the entity ids passing a test on an upstream step's results |
| `extractor` | str | extractor class name, e.g. CoverageExtractor; needs module |
| `module` | str | import path of the extractor class |
| `setup` | call block | setup call: method + params (see call) |
| `run` | call block | bulk call: method + params, required with extractor (see call, run.params) |
| `export_format` | `csv` or `parquet` | per-step override of settings.export_format |
| `export_manifest` | bool | per-step override of settings.export_manifest |
| `output_uri` | str | per-step override of settings.output_uri |
| `retry_failed_only` | bool or str | per-step override of settings.retry_failed_only |

### `setup:` / `run:`

| Key | Type | What it does |
|---|---|---|
| `method` | str | method name on the extractor (setup_*_parameters / process_*_bulk_*) |
| `params` | mapping | keyword arguments; strings in setup.params may use date sentinels (today, today-30d, ...) |

### `transform:`

| Key | Type | What it does |
|---|---|---|
| `module` | str | import path of the module holding the function, required |
| `function` | str | function name, required |
| `params` | mapping | passed as the function's params argument (WorkflowManager adds _workflow_manager) |

### `condition:`

| Key | Type | What it does |
|---|---|---|
| `depends_on` | str | the upstream step whose results_df is filtered, required |
| `column` | str | column of that results_df, required |
| `operator` | `eq` or `ne` or `in` or `notnull` | eq (default), ne, in, notnull |
| `value` | Any | compared value (a list for in); required except for notnull |

### `entity_source:`

| Key | Type | What it does |
|---|---|---|
| `params` | mapping | parameters for your entity loader; date sentinels are rewritten |

### `run.params` keys WorkflowManager keeps

Every other key in `run.params` is passed to the bulk method as a keyword argument.

| Key | Default | What it does |
|---|---|---|
| `max_workers` | settings.max_workers, else 10 | threads for this step |
| `prefix` | the step name | output file prefix (composed with settings.output_prefix) |
| `skip_export` | true | results stay in memory unless set to false: a step does NOT write files by default |
| `fail_safe` | settings.fail_safe, else false | record per-entity failures instead of raising |
| `generate_report` | false | write the HTML extraction report |

<!-- END GENERATED: workflow-keys -->

## Top-Level `workflow` Block

The keys of this block, their types and what they do are in the generated **Key reference** above.

## `settings` Block

Global defaults. Step-level params override these where applicable.

The keys of this block, their types and what they do are in the generated **Key reference** above.

Any other key you put under `settings` is passed to each step's `setup` method if the method's signature accepts it (filtered via `inspect.signature`).

### Output Prefix Composition

Filenames are composed from up to three optional layers, slugified individually then joined with `_`:

```
<output_prefix>_<run_prefix>_<step_prefix>_results_<timestamp>_<suffix>.csv
```

| Layer | Source | When set |
|---|---|---|
| `output_prefix` | `settings.output_prefix` in the YAML | Workflow-level — same for every step, every run. |
| `run_prefix` | `manager.run_workflow(entity_list, run_prefix="...")` argument | Per-run tag (per-client / per-date / per-scenario). Reset to `None` after each `run_workflow()` call so a later call without the arg doesn't inherit it. |
| `step_prefix` | `run.params.prefix` on the step (or step `name` as fallback) | Per-step. |

Any of the three can be absent — only present layers contribute to the filename. Examples (assuming `step.name = "coverage"`):

| `output_prefix` | `run_prefix` | `step.run.params.prefix` | Resulting `prefix` kwarg |
|---|---|---|---|
| — | — | — | `coverage` |
| — | `2026_05_06_clientA` | — | `2026_05_06_clientA_coverage` |
| `proj` | — | `coverage_v2` | `proj_coverage_v2` |
| `proj` | `2026_05_06_clientA` | `coverage_v2` | `proj_2026_05_06_clientA_coverage_v2` |

Driver code:

```python
manager.load_workflow("configuration/workflow.yml")
results = manager.run_workflow(entity_list=entities, run_prefix="2026_05_06_clientA")
```

## Step Definition

Each item in `steps` is a dict. The combination of fields present determines the step type:

| Fields present | Step type | Behavior |
|---|---|---|
| `extractor` only (no `transform`) | **Extractor-only** | Runs extractor on the input entity list. |
| `transform` only (no `extractor`) | **Transform-only** | Runs transform; its DataFrame output becomes the step's `results_df`. |
| Both `transform` and `extractor` | **Combined** | Transform reshapes entities first, then extractor runs on the transformed entities. |

### Common Fields

The keys of this block, their types and what they do are in the generated **Key reference** above.

### Disabling a step

```yaml
steps:
  - name: weather
    enabled: false                # loaded but never executed
    extractor: WeatherExtractor
    module: earthdaily.agriculture.extractors.weather_functions
    setup: {method: setup_weather_parameters, params: {}}
    run:   {method: process_entity_weather_bulk_parallel, params: {prefix: weather}}
```

The same YAML stays in source control with non-relevant steps cleanly turned off. To re-enable, flip `enabled: true` (or remove the field — defaults to `true`).

#### Disabling steps without editing the YAML

Three runtime paths skip steps without mutating the YAML on disk:

**Headless / CLI / Argo** — `run_workflow(disabled_steps=[...])`:

```python
manager.load_workflow("configuration/workflow.yml")
results = manager.run_workflow(entity_list=entities, disabled_steps=["weather", "mrts"])
```

The override is applied to `step_map[*]["enabled"]` at the start of `run_workflow()` and rolled back in a `finally` block — even if a step raises mid-run, the loaded YAML state is preserved. Unknown step names raise `ValueError`.

**Notebook checkbox widget** — `manager.select_steps_to_run()`:

```python
manager.load_workflow("configuration/workflow.yml")
manager.select_steps_to_run(entity_list=manager.sfd_list)   # render in the cell
```

Returns an `ipywidgets.VBox` with one checkbox per step plus a "Run workflow" button. Toggling a checkbox flips `step_map[name]["enabled"]` in place; the button calls `run_workflow()` with the chosen subset. Per-step annotations show the extractor class and `depends_on` so you can predict cascade-skip behavior.

**Notebook clickable DAG** — `manager.interactive_workflow()`:

```python
manager.load_workflow("configuration/workflow.yml")
manager.interactive_workflow()                              # render in the cell
```

Returns a `plotly.graph_objects.FigureWidget` — same layout as `visualize_workflow()`, but clicking a node toggles its `enabled` state and recolors it gray. State persists on the manager between `interactive_workflow()` calls and into the next `run_workflow()`. Note: cascade-skip of downstream steps is only enforced at runtime (via the empty-upstream branch); the widget colors only the directly-clicked node.

### `depends_on`

Accepts a string or a list of strings.

```yaml
# Single dependency
depends_on: coverage

# Multiple dependencies (step runs after all complete)
depends_on: [coverage, cropid]
```

Steps with no `depends_on` are scheduled at level 1 and run first. Independent steps at the same DAG level run in parallel up to `settings.max_parallel_steps`.

### `input_from`

Declares which DataFrame the step receives as its `entity_list`. This is the data passed to the step's `transform` (if any) and ultimately to the extractor.

| `input_from` value | Behavior |
|---|---|
| `"original"` | Use the `entity_list` passed to `run_workflow()`. |
| `<step_name>` (string) | Use `workflow_results[step_name]["results_df"]` as the entity list. |
| omitted | Default to the first `depends_on` if present, else `"original"`. |

```yaml
# Default — auto-chains to the upstream's results_df
- name: coverage
  depends_on: mrts_field
  extractor: CoverageExtractor
  ...

# Explicit override — pull from a non-immediate ancestor
- name: zoning
  depends_on: image_selection
  input_from: cropid
  extractor: ZoningExtractor
  ...

# Force the original entity_list even though there is a depends_on (used purely for ordering)
- name: weather
  depends_on: cropid
  input_from: original
  extractor: WeatherExtractor
  ...
```

The `transform` (if any) still runs on top of the resolved entity list — a step can declare both `input_from: <step>` and a transform that further reshapes that DataFrame. With the default-to-`depends_on` behavior, no-op pass-through transforms (e.g. `use_upstream_entities`) are no longer required.

**Validation at load time.** `load_workflow()` rejects:
- non-string `input_from` values
- references to a step that does not exist
- references to the step itself, a parallel step, or a later step (must reference a step in an *earlier* execution level)

**Empty upstream.** If the resolved `input_from` step's `results_df` is empty (or the step was skipped), this step is marked `skipped` and not executed.

### `transform` Block

```yaml
transform:
  module: app.transforms
  function: my_transform
  params:
    depends_on: coverage
    any_other_key: value
```

| Field | Type | Required | Description |
|---|---|---|---|
| `module` | str | **Yes** | Python import path of the module containing the transform function. |
| `function` | str | **Yes** | Callable name. Must match the transform contract (see `08 - Workflow_architecture.md`). |
| `params` | dict | No | Passed to the transform as its `params` argument. Convention: include `depends_on` here so the transform reads the correct upstream step. |

The runner injects `_workflow_manager` into `params` so transforms can access auth, config, and paths if needed.

#### Built-in transform — `publish_to_cloud`

Post-extraction hand-off from local disk to cloud storage for **runs that wrote
results locally and want to push the whole bundle to a cloud bucket after the
fact**. The target backend is whatever fsspec scheme the prefix carries
(`s3://`, `az://`, `gs://` ...). (For runs that should write *directly* to cloud
storage during extraction, just pass `output_result_dir="s3://..."` to
`WorkflowManager` — `publish_to_cloud` is unnecessary.)

```yaml
- name: publish
  transform:
    module: earthdaily.agriculture.export.cloud_publish
    function: publish_to_cloud
    params:
      publish_prefix: s3://my-bucket/runs/2026-05-12   # required (s3:// / az:// / gs://)
      output_dir: results                              # where the *_manifest_*.json lives (default: "results")
      publish_formats: [parquet]                       # optional: filter by format
      rewrite_path_to_cloud: true                      # optional: set each uploaded entry's `path` to the cloud URI (default: false)
      # storage_options: { client_kwargs: { endpoint_url: "..." } }   # optional: MinIO / LocalStack
```

What it does:

1. Picks the most recent `*_manifest_*.json` under `output_dir` (or use `params.manifest_path` to be explicit).
2. Walks the manifest's `files` list and uploads every entry to `publish_prefix/<filename>` via fsspec.
3. Patches each file entry with a `cloud_upload` block (`{uri, key, bucket, uploaded_at}`).
4. Adds a top-level `cloud_publish` summary (`{bucket, publish_prefix, uploaded_files, skipped_files, total_files, published_at}`).
5. Writes the patched manifest both locally (overwriting the original) and to `publish_prefix/<manifest-filename>` so consumers reading straight from cloud storage see the full picture.

With `rewrite_path_to_cloud: true`, each uploaded entry's `path` is set to the cloud URI (same value as `cloud_upload.uri`) and the original local path is preserved under `local_path` — so a manifest read straight from cloud storage resolves `path` directly. Skipped entries keep their local `path`. Default is `false` (path stays local; only the `cloud_upload` block is added).

Returns `entity_list` unchanged so downstream steps that depend on this one don't need to know publish ran.

### `condition` Block

Applied after the transform (if any) to filter the entity list based on an upstream result.

```yaml
condition:
  depends_on: cropid
  column: confirmation_status
  operator: eq
  value: confirmed
```

| Field | Type | Required | Description |
|---|---|---|---|
| `depends_on` | str | **Yes** | Upstream step whose `results_df` holds the filter column. |
| `column` | str | **Yes** | Column in the upstream `results_df` to evaluate. |
| `operator` | str | No (`eq`) | One of `eq`, `ne`, `in`, `notnull`. |
| `value` | any | **Yes** (except `notnull`) | Value to compare against. For `in`, provide a list. |

Filtering is done by entity ID: passing entity IDs are kept, all others are dropped. If the upstream `results_df` is empty, the step is skipped.

### `extractor` + `module`

```yaml
extractor: CoverageExtractor
module: earthdaily.agriculture.extractors.coverage_function
```

The runner dynamically imports the module and instantiates the class with the current bearer token, token expiration, and workflow `config`. After instantiation, `settings.column_mapping` is merged into the extractor's mapping.

### `setup` Block

```yaml
setup:
  method: setup_coverage_parameters
  params:
    vegetation_index: NDVI
    start_date: "2025-01-01"
    clear_cover_min: 95
```

| Field | Type | Required | Description |
|---|---|---|---|
| `method` | str | **Yes** (if `setup` is present) | Setup method name on the extractor. |
| `params` | dict | No | Keyword arguments for the setup method. Merged with `settings` (step-level keys win). Params not accepted by the method signature are filtered out automatically — safe to pass a superset. |

#### Dynamic date sentinels

Any string param under `setup.params` (or `entity_source.params`) that matches one of these patterns is rewritten to an ISO date at `load_workflow()` time. Use them on `start_date` / `end_date` / `sowing_date_gte` etc. so scheduled runs always pick up the current date without YAML edits.

| Sentinel | Resolves to | Example output |
|---|---|---|
| `today` | today's date in workflow TZ (UTC by default) | `2026-05-12` |
| `yesterday` | `today − 1 day` | `2026-05-11` |
| `today±N` | `today ± N days` (unit defaults to days) | `today+10` → `2026-05-22` |
| `today±Nd` | `today ± N days` | `today-7d` → `2026-05-05` |
| `today±Nw` | `today ± N weeks` | `today+2w` → `2026-05-26` |
| `today±Nm` | `today ± N months` (30-day approx) | `today-1m` → `2026-04-12` |

```yaml
- name: mrts
  setup:
    method: setup_mrts_parameters
    params:
      start_date: "today-30d"   # rolling 30-day window
      end_date: "today"         # always up to today; no cron-day edits

- name: weather_forecast
  setup:
    method: setup_weather_parameters
    params:
      start_date: "today"
      end_date: "today+10"      # 10-day forecast window
```

To run "today" in a non-UTC zone, set `settings.timezone` to an IANA name (`America/Chicago`, `Europe/Paris`, ...). Default is UTC.

**Notes:**
- Both **past (`today-N`) and future (`today+N`) offsets** are supported. The unit suffix is optional and defaults to days, so `today+10` ≡ `today+10d`.
- Only **strings inside `setup.params` and `entity_source.params`** are walked — one level deep. `run.params`, `transform.params`, and arbitrary nested dicts pass through.
- Resolution happens **once, at load time**. Substitutions are logged at INFO (`🗓 step.setup.params.end_date: "today" → "2026-05-12"`).
- Anything that doesn't match the grammar is left alone — including already-resolved ISO dates, so the rewrite is idempotent on a re-load within the same day.

### `run` Block

```yaml
run:
  method: process_entity_coverage_bulk_parallel
  params:
    prefix: coverage
    skip_export: true
    max_workers: 10
    fail_safe: true
    generate_report: false
```

| Field | Type | Required | Description |
|---|---|---|---|
| `method` | str | **Yes** | Bulk-processing method name on the extractor (typically `process_*_bulk_parallel`). |
| `params` | dict | No | Reserved keys below are consumed by the runner; any others are forwarded to the run method's `params` argument. |

**Reserved keys inside `run.params`:**

| Key | Default | Description |
|---|---|---|
| `prefix` | step name | Filename prefix for partial and final exports. |
| `skip_export` | `true` | If `true`, results stay in memory (not written to `results/`). Set `false` to export immediately. |
| `max_workers` | `settings.max_workers` (or `10`) | Step-level override for parallelism. |
| `fail_safe` | `settings.fail_safe` (or `false`) | Step-level override. |
| `retry_failed_only` | `settings.retry_failed_only` (or `false`) | Step-level override. See **Resuming a failed run** below. |
| `generate_report` | `false` | If `true`, produces the HTML extraction report. |

## Rate limiting a step

Any other key in `run.params` that the bulk method accepts is forwarded to it. One worth
knowing is **`rate_limit`**: the most HTTP requests per second the step sends, retries
included, shared by all `max_workers` threads. Unset means no limit.

```yaml
workflow:
  steps:
    - name: weather
      extractor: WeatherExtractor
      module: earthdaily.agriculture.extractors.weather_functions
      setup:
        method: setup_weather_parameters
      run:
        method: process_entity_weather_bulk_parallel
        params:
          max_workers: 10
          rate_limit: 5     # at most 5 calls/s for this step, across its 10 threads
```

It is set **per step** on purpose; there is no workflow-wide `settings` key, since each API
has its own quota. Two steps that run in parallel each have their own limit. It counts
HTTP requests per second, retries included, and when the API answers 429 (too many
requests) every thread of the step waits the time the server asks for.

## Resuming a failed run

A run with `fail_safe: true` writes the IDs it could not process to
`partials/failed_ids_<prefix>_<timestamp>.csv`. To process **only** those IDs, ask for it
explicitly:

```yaml
workflow:
  steps:
    - name: cropid
      extractor: cropidExtractor
      module: earthdaily.agriculture.extractors.cropid_functions
      run:
        method: process_cropid_bulk_extraction_parallel
        params:
          prefix: cropid
          fail_safe: true
      retry_failed_only: true        # newest failed_ids_cropid_*.csv
      # retry_failed_only: "partials/failed_ids_cropid_1786470000.csv"   # or one exact file
```

Two properties worth relying on:

- **`fail_safe` alone never narrows the entity list.** Until this change it did: a leftover
  `failed_ids_*.csv` silently capped the next `fail_safe` run to those IDs while logging
  success, and because the cleanup pass only removes `<prefix>_*_partial.*`, the file
  persisted and every later run stayed capped. If a resume file exists and
  `retry_failed_only` is not set, the run now processes everything and logs a warning
  naming the file.
- **Requesting a resume with no file present raises.** Asking to resume and silently
  getting a full run is the same class of surprise, inverted.

Resume reads the file from wherever `partials/` lives, including `s3://` and `az://`
paths.

## Step Type Examples

### Extractor-only

```yaml
- name: coverage
  extractor: CoverageExtractor
  module: earthdaily.agriculture.extractors.coverage_function
  setup:
    method: setup_coverage_parameters
    params:
      vegetation_index: NDVI
      start_date: "2025-01-01"
      clear_cover_min: 95
  run:
    method: process_entity_coverage_bulk_parallel
    params:
      prefix: coverage
      skip_export: true
```

### Transform-only

```yaml
- name: image_selection
  depends_on: coverage
  transform:
    module: app.transforms
    function: select_best_images
    params:
      depends_on: coverage
      max_images: 3
```

The transform's returned DataFrame is stored directly as `results_df`.

### Combined (transform + extractor)

```yaml
- name: zoning
  depends_on: image_selection
  transform:
    module: app.transforms
    function: prepare_zone_entities
    params:
      depends_on: image_selection
  extractor: ZoningExtractor
  module: earthdaily.agriculture.extractors.zoning_functions
  setup:
    method: setup_zoning_parameters
    params:
      num_zones: 5
  run:
    method: process_entity_zoning_bulk_parallel
    params:
      prefix: zoning
```

The transform receives the resolved `entity_list` (here: `image_selection.results_df` via the `depends_on` default) and its output replaces the entity list passed to the extractor.

> **Note.** Prior versions required a no-op `use_upstream_entities` transform here just to swap `entity_list` for the upstream's `results_df`. With the `input_from` default-to-`depends_on` behavior, this boilerplate is no longer needed — the upstream `results_df` is already the entity list. Use a transform only when you need to actually reshape the data.

### With condition

```yaml
- name: scoring
  depends_on: [cropid, coverage]
  condition:
    depends_on: cropid
    column: confirmation_status
    operator: eq
    value: confirmed
  extractor: HistoricalScoreExtractor
  module: earthdaily.agriculture.processors.processor_score_functions
  setup:
    method: setup_historical_score_parameters
    params:
      season_duration: 120
  run:
    method: process_historical_score_bulk_extraction_parallel
    params:
      prefix: score
```

## Execution Semantics

- Steps are grouped into levels by topological order (Kahn's algorithm). Level 1 has all steps with no dependencies.
- Within a level, independent steps run concurrently (thread pool, bounded by `max_parallel_steps`).
- If a transform returns an empty DataFrame, the step is marked `skipped` and downstream steps see an empty `results_df` for it.
- An exception during parallel execution is caught per-step: the step's entry in `workflow_results` gets an empty `results_df` and the error in `global_errors`.
- `workflow_results` is a dict keyed by step name: `{step_name: {"results_df": df, "global_errors": [...], "failed_ids": [...], "skipped": bool?}}`.

## Run reporting (out of band)

Reporting is **not** configured in the YAML. Pass `generate_report=True` to `manager.run_workflow(...)` to opt in for the run — the manager builds a `WorkflowRunReporter` from the loaded YAML (workflow name, `output_prefix`, env, entity count), populates it after the DAG completes, and stashes the configured reporter at `manager.last_run_reporter` so the caller can amend its context (e.g. add a downstream `report_path`) and render HTML / JSON. Optional `report_options={...}` knobs control the reporter's constructor and run-context fields — see [`09 - Workflow_architecture.md` → Run reporting](09%20-%20Workflow_architecture.md#run-reporting) for the full surface.

## Validation (at `load_workflow` time)

- Every step must have a unique `name`.
- Every `depends_on` reference must resolve to a declared step.
- The DAG must be acyclic.
- If `extractor` is present, `run.method` is required.
- Every `input_from` value (when set) must be `"original"` or the name of a step in an *earlier* execution level (cannot reference itself, a parallel step, or a later step).

Errors surface as `ValueError` before any step runs, so misconfigurations fail fast.

## Legacy Format

An older flat format with an `analytics` top-level key is still parsed but logs a warning and is not compatible with `run_workflow()`. Migrate legacy files to the `workflow: { steps: [...] }` structure.

## Inspecting a Loaded Workflow

```python
manager.load_workflow("configuration/workflow.yml")

# Interactive Plotly DAG — color encodes role, hover reveals params + input_from
manager.visualize_workflow().show()

# Structured dict for programmatic checks
manager.inspect_workflow()
```

`visualize_workflow()` returns a `plotly.graph_objects.Figure`. Nodes are placed left→right by topological execution level; node color encodes role:

| Color | Role |
|---|---|
| Orange | Step has both a `transform` and an `extractor` |
| Green | Extractor-only |
| Blue | Transform-only |

Arrows show `depends_on` edges. Hovering over a node displays `depends_on`, the resolved `input_from` (suffixed `(default)` when inferred), the transform module/function and params, the extractor class with its `setup`/`run` methods and params, and any `condition` filter.

Optional kwargs let you tune layout: `height`, `h_spacing`, `v_spacing`, `max_value_len`.

`inspect_workflow()` returns one entry per step including:
- `input_from` — the resolved value (`"original"` or a step name)
- `input_from_explicit` — `True` if the YAML set the field, `False` if defaulted
