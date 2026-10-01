---
title: Result caching
description: How extractor results are cached locally and how to enable, tune, and troubleshoot it.
#icon: material/database-outline
keywords:
  - cache
  - caching
  - parquet
  - cache_key_columns
  - cache_ttl_days
  - use_cache
  - performance
  - spatial_grouping
  - geohash
  - spatial_max_window_days
---

# Result caching

Every extractor inherits a local result cache from `BaseExtractor`. When enabled, extracted rows are stored to a per-extractor parquet file keyed by the extractor's parameters; subsequent runs over the same entities skip the API call and return the cached rows.

The cache is **opt-in per extractor**, **TTL-driven**, and **single-machine** — it lives on local disk and is automatically disabled if pointed at object storage.

See worked examples in [`EDAgriculture_extractor_cache_showcase.ipynb`](./EDAgriculture_extractor_cache_showcase.ipynb).

---

## When to enable the cache

Turn it on whenever you re-run the same extraction over the same entities multiple times — typical scenarios:

- **Iterative analysis.** Same set of fields, repeated tweaks to downstream charts / transforms. The API call doesn't need to repeat.
- **Recurring reports** (daily / weekly / monthly). Most rows are unchanged from the previous run; only a small frontier of new dates / entities needs to be fetched.
- **Long bulk runs you may need to resume.** Cached rows survive a crash; the next run picks up where the previous one stopped.

Don't enable it when:

- You're writing outputs to S3 / GCS / any object store — the cache silently disables itself (see below).
- The underlying data is expected to *change* for the same parameters (rare; the API normally returns deterministic results for a given parameter set, but a recompute on the platform side would not invalidate your cache automatically).
- You're running one-off probes where the extra parquet I/O outweighs the saved API call.

---

## Enabling the cache

Two equivalent ways: globally via `WorkflowManager` config, or per-extractor in its setup call.

### Globally

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager

manager = WorkflowManager(
    "prod",
    use_cache=True,
    cache_dir="cache/",          # default: <project_root>/cache
    cache_ttl_days=7,            # default: 7
)
```

Every extractor built through the manager inherits these defaults. Individual extractors can still flip themselves off in their own setup call.

### Per-extractor

```python
coverage = CoverageExtractor(token, config)
coverage.setup_coverage_parameters(
    start_date="2025-04-01",
    end_date="2025-09-30",
    use_cache=True,              # overrides the manager default
)
```

`use_cache` is a recognized kwarg on every `setup_*_parameters()` method.

---

## Cache keys

A cache entry is identified by three things together:

| Identifier              | Source                                                                    |
| ----------------------- | ------------------------------------------------------------------------- |
| **Extractor class**     | Class name, lowercased (e.g. `coverageextractor`)                         |
| **Parameter signature** | MD5 hash of the extractor's `setup_*_parameters()` dict                   |
| **Entity key columns**  | A small list each extractor declares in setup (e.g. `[id_col, "date"]`)   |

The first two determine the **parquet file name**; the third determines which rows inside that file are considered "the same record."

Two consequences worth knowing:

- **Changing any setup parameter invalidates the cache** — the params hash changes and a new file is used. If you flip `clear_cover_min=95 → 90`, the previous cache is still on disk but won't be read.
- **Two extractors of the same class in the same project share a cache file** if their setup params are identical. This is normally what you want; if you need parallel caches for the same class with the same params, override `cache_dir`.

To see the file an extractor is using:

```python
print(extractor._cache_path())     # absolute path to the parquet file
```

---

## Spatial grouping — a second, cell-keyed cache

`WeatherExtractor`, `GDDExtractor` and `GDDOffsetExtractor` query the API by field **centroid**, not by polygon. Fields whose centroids land in the same geohash cell therefore receive identical values, and calling the API once per field pays for the same answer many times over.

Opt in per bulk run:

```python
result = extractor.process_weather_bulk_extraction_parallel(
    entity_list=fields,
    spatial_grouping=True,     # off by default
    spatial_precision=5,       # geohash-5, ~4.9 km cells
)
```

or declaratively, for every step in a workflow:

```yaml
workflow:
  settings:
    spatial_grouping: true
```

The API is called once per (cell x request signature) group and the result is broadcast to every member field. Measured on 100 real soybean fields spanning 26 geohash-5 cells: **100 API calls become 26**, and zero on a warm cache. Dedup is entirely selection-dependent, though — the same source file yields 7.8x across all 5112 fields but only 1.1x on a random 100-field sample, because a scattered sample shares no cells. **It pays on contiguous AOIs**, not on sparse ones.

The default precision of 5 (~4.9 km) is matched to the coarse weather grid. Refine to 6 (~1.2 km) if you need tighter buckets.

### Why spatial grouping impacts caching?

Grouped runs do **not** use the entity cache described above. They use a separate, **cell-keyed** cache — keyed on the geohash cell x date, in its own parquet file.

The entity cache matches on entity id, so under grouping only the *representative* field's id ever landed in it. A later run over a different field set in the same cells re-fetched data that was already on disk. Keyed on the cell, any later run touching that cell is served from cache whatever field set — or sub-window — it asks for.

| | Entity cache | Spatial cache |
| --- | --- | --- |
| Key | Extractor + params hash + entity key columns | Extractor + params hash + `_cell_key` x date |
| Populated by | Any run with `use_cache=True` | Runs with `spatial_grouping=True` |
| Inspect / clear | `cache_info()` / `clear_cache()` | `spatial_cache_info()` / `clear_spatial_cache()` |

Coverage is **all-or-nothing per cell**: a window the cache does not fully span is refetched whole, which keeps each stored series contiguous rather than accumulating holes.

### Window union, and the cap that bounds it

Dates are deliberately left out of the group key, so a cell holding fields with staggered windows is pulled **once** over the union of its members' windows, and each field is sliced back out of that single response. Members are clipped to their own window, so a grouped run returns exactly what an ungrouped run would.

`spatial_max_window_days` (default 400) bounds how far a union may *widen*: a merge is allowed when the union is no longer than the cap **or** than a member's own window. That stops one long-history field dragging its neighbours into a decade-long pull. A cell that splits logs a WARNING naming the knob.

### The trap: cumulative columns

Widening a window only distorts columns that accumulate from the **request** start, and which ones those are cannot be inferred from the name. Measured against production by requesting one field over a wide and a narrow window and diffing the overlap:

| Column | Overlap identical | Verdict |
| --- | --- | --- |
| `precipitation.cumulative` | 62/62 (max diff 0.0) | **per-day despite its name** — must NOT be rebased |
| `temperature.standardMax` | 62/62 | per-day |
| `daily_gdd` | 62/62 | per-day |
| `cumulated_gdd` | 0/62, constant 977.2 offset | genuinely cumulative — rebased per member |

So rebasing is declared explicitly, never guessed: `GDDExtractor` sets `cumulative_columns=["cumulated_gdd"]` and re-zeroes it per member, year-segmented when `reset_cumulative_every_year` is set. An earlier revision auto-detected these by name and was silently corrupting weather output.

`GDDOffsetExtractor` groups but never widens — it returns one row per entity from a single base date, so there is no series to slice.

---

## TTL and eviction

Each cached row carries an `_cached_at` timestamp. Before any cache read, rows older than `cache_ttl_days` are evicted.

```python
manager = WorkflowManager("prod", use_cache=True, cache_ttl_days=14)
```

Picking a TTL:

- **Vegetation / weather time series** — 7–14 days is typical. New satellite passes and weather records arrive daily; an older cache will miss the freshest dates.
- **Crop ID / static classifications** — 90+ days, or effectively never expires. The underlying result doesn't change within a season.
- **Coverage searches** — 1–3 days if you want new imagery to surface promptly.

TTL is enforced at read time. There's no background sweep; stale rows simply disappear from the next read.

---

## What gets stored

Each cache write appends to the parquet file with these guarantees:

- **`_cached_at` timestamp column** is added on the way in (used for TTL eviction).
- **Deduplication on `cache_key_columns`** with `keep="last"` — the freshest fetch wins over older cached rows for the same key tuple.
- **Atomic writes.** The file is written to a temp path next to the target, then renamed. A crash mid-write leaves the previous good cache in place; you never end up with a half-written parquet.

---

## Object-storage cache is automatically disabled

If you set `cache_dir` to a remote URI (`s3://...`, `gs://...`), the cache disables itself at extractor construction time and logs a warning:

```
⚠️  Cache disabled: cache_dir='s3://my-bucket/cache' is a remote URI.
The local-only atomic-rename strategy used by _update_cache cannot run
against object stores. Set cache_dir to a local path to re-enable caching,
or leave it as the default project-local 'cache/' directory.
```

This is intentional. The atomic rename pattern that protects against half-written cache files has no portable equivalent on S3 / GCS, and a per-pod cache in an ephemeral container provides little benefit anyway. For cloud runs, leave the cache off and rely on the workflow's partial-result handling instead.

---

## How cache hits flow through extraction

Two layers cooperate, but you don't need to think about which fires when — the behaviour is the same either way:

| Layer            | When it fires                                              | What it does                                                                                   |
| ---------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Per-entity**   | `process_single_entity()` calls                            | Looks up the entity ID + params hash. On hit, returns the cached rows and skips the API call. |
| **Bulk wrapper** | `process_*_bulk_parallel()` with `use_cache=True`          | Filters the input frame down to "entities not in cache," runs the API only on the remainder, then merges fresh + cached. |

The bulk wrapper produces a single cache hit log line up front so you can see at a glance how much of the run is being served from cache:

```
[CoverageExtractor] cache: 412/500 entities served from cache, 88 to fetch
```

If the number on the left is `0/N`, the cache is empty or fully stale. If it's `N/N`, the API isn't called at all.

---

## Per-extractor cache key reference

Each extractor declares its key columns in `setup_*_parameters()`. The defaults below cover the common cases; override `cache_key_columns` on the extractor instance after `setup_*_parameters()` if you need a different uniqueness contract.

| Extractor              | Default `cache_key_columns`               |
| ---------------------- | ----------------------------------------- |
| `CoverageExtractor`    | `[id_col, "date", "image_id"]`            |
| `VegetationTsExtractor` | `[id_col, "date"]`                       |
| `MRTSExtractor`        | `[id_col, "date"]`                        |
| `WeatherExtractor`     | `[id_col, "date"]`                        |
| `RegionalExtractor`    | `[id_col, "date"]`                        |
| `cropidExtractor`      | `[id_col, "year"]`                        |
| `GreennessExtractor` / `EmergenceExtractor` / `HarvestExtractor` | `[id_col]` (one row per entity per season) |

`id_col` is the column you mapped to the canonical `id` field via `column_mapping`.

---

## Troubleshooting

**"Cache hits but I'm not seeing any speedup."**
The first hit on a parquet file pays a one-time read cost. Past a few hundred rows the saved API calls dominate. If the cache is mostly empty (run-1 of a new param set), expect run-1 to be the same speed as no-cache.

**"I bumped a parameter and the cache didn't update."**
That's correct — bumping a parameter writes to a *new* cache file under a different params hash. The old file is still on disk. Delete `cache/` (or the specific stale `<class>_<hash>_cache.parquet`) if you want to reclaim space.

**"Two parallel runs corrupted my cache."**
The atomic rename protects against crash mid-write, not against two processes writing simultaneously. For parallel runs, give each its own `cache_dir`. The cache is a single-machine accelerator, not a shared coordination primitive.

**"I want to inspect what's cached."**
The cache file is plain parquet — `pd.read_parquet(extractor._cache_path())` gives you the full table including the `_cached_at` timestamp.

**"Some entities are still calling the API even though they should be cached."**
Three usual causes:

1. TTL eviction — the rows existed but their `_cached_at` is older than `cache_ttl_days`.
2. Key mismatch — `cache_key_columns` includes a column that's slightly different between runs (e.g. one run has `image_id="X.tif"`, another has `image_id="X"`).
3. Different params signature — the setup dict for this run hashes to a different file than the previous one.

---

## See also

- [`EDAgriculture_extractor_cache_showcase.ipynb`](./EDAgriculture_extractor_cache_showcase.ipynb) — worked examples.
- [`13 - Cloud_storage_principles_and_usage.md`](13%20-%20Cloud_storage_principles_and_usage.md) — why the cache disables itself on remote `cache_dir`.
- [`09 - Workflow_architecture.md`](09%20-%20Workflow_architecture.md) — where `use_cache` is set globally via the workflow manager.
