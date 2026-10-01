---
title: Optimizing extractor output
description: Use extractors properly and configure their output — a regional-monitoring case study where good configuration turns a 16 GB CSV into ~22 MB of Parquet, losslessly.
keywords:
  - extractor configuration
  - parquet
  - output columns
  - manifest
  - regional monitoring
  - optimization
---

# Optimizing extractor output

Every extractor turns an entity DataFrame into a results DataFrame and writes it to disk.
The **default** write is deliberately simple — CSV, every column, one row per record. That
is fine for a handful of fields, but on a large pull the difference between a naive call and
a well-configured one can be **three orders of magnitude** in file size, with no loss of
information.

This guide shows the levers, using a real case: exporting a **regional-monitoring** indicator
for administrative block **b129** (2,984 regions × ~1,094 daily dates) with `RegionalExtractor`.

---

## 1. Use an extractor properly (the lifecycle)

Every extractor follows the same three steps:

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager
from earthdaily.agriculture.extractors.regional_ts_extractor import RegionalExtractor

manager = WorkflowManager("prod")                       # 1. auth + config
ext = RegionalExtractor(manager.bearer_token, manager.token_expiration,
                        config=manager.config, workflow_ref=manager)
ext.setup_regional_parameters(index="average-temperature", ...)   # 2. configure
res = ext.process_entity_regional_bulk_parallel(entity_list=entities, ...)   # 3. run in bulk
```

`setup_*_parameters()` is where you make every decision that shapes the **output** — not just
the analytic parameters (index, dates, thresholds) but also the **output columns**, the
**export format**, and whether a **manifest** is written. Those output decisions are the
subject of this guide.

> Output configuration lives once on `BaseExtractor` and flows through the shared
> `export_results()` / `_finalize_extraction()` writer, so **every** extractor honours the
> same knobs — nothing here is specific to `RegionalExtractor`.

---

## 2. Case study — the naive call

```python
# ⚠️ Naive: defaults everywhere
ext.setup_regional_parameters(index="average-temperature",
                              start_date="2023-01-01", end_date="2025-12-31",
                              idblock=129, idpixeltype=8)
ext.process_entity_regional_bulk_parallel(entity_list=regions, output_path=OUT)
```

This produces a **~16 GB CSV** for a single indicator. Why so large?

- The output carries **`amu_geometry`** — the region's full WKT polygon (~3.3 KB) — **stamped
  onto every one of the 3.26 million rows**. That single column is **94.8 % of the file**.
- Nine more columns are **constant** for the whole extraction (`indicator_name`, `id_block`,
  `idpixeltype`, `pixel_type_name`, `start_date`, `end_date`, …) and one (`idblock`) duplicates
  another — all repeated on every row.
- CSV stores everything as text with no compression and loses dtypes.

The actual signal is three columns: `date`, `value`, and `amu_id`.

---

## 3. Case study — the configured call

```python
# ✅ Configured: right columns, Parquet, manifest
ext.setup_regional_parameters(
    index="average-temperature", start_date="2023-01-01", end_date="2025-12-31",
    idblock=129, idpixeltype=8,
    column_mapping={"id": "amu_id"},
    output_columns=["entity_id", "date", "day_id", "value"],   # the lean set — no geometry
)
ext.export_format = "parquet"                                   # columnar + compression
ext.export_manifest = True                                      # provenance sidecar
ext.manifest_metadata = {"region_dimension_file": "regions_b129.parquet", "join_key": "amu_id"}
ext.process_entity_regional_bulk_parallel(entity_list=regions, output_path=OUT,
                                          prefix="regional_b129_average-temperature")
```

Geometry and the region names are not thrown away — they are stored **once per region** in a
separate **region dimension** file (`regions_b129.parquet`, 2,984 rows) that you join back on
`amu_id` only when you actually need a polygon. The entity DataFrame you feed in *is* that
dimension, so no extra work is required.

### Result

| | Naive | Configured | |
|---|---|---|---|
| Fact table | **16 GB** CSV | **~16 MB** Parquet | one row per `(amu_id, date)` |
| Geometry / region attrs | on every row (94.8 %) | **~6 MB** shared `regions_b129.parquet` | stored once per region |
| Provenance | — | `…_manifest_*.json` | constants + structure + join key |
| **Total** | **~16 GB** | **~22 MB** | **~700× smaller, lossless** |

The constants that were repeated on every row now live once in the manifest's
`metadata.constant_columns`; the structure/entity-count/date-range/completeness are captured
there too, so a consumer understands the dataset without opening it.

---

## 4. The configuration levers (apply to any extractor)

### 4a. Output columns — `output_columns` / `exclude_columns` / `output_mapping`

Passed to `setup_*_parameters()`, these drive `configure_output()` (applied as rename →
exclude → select):

- **`output_columns=[...]`** — an explicit **whitelist**; the leanest, most predictable output.
- **`exclude_columns=[...]`** — drop specific columns (e.g. `["amu_geometry", "idblock"]`) while
  keeping the rest. Note the geometry column is `geometry` for most extractors but `amu_geometry`
  for regional — exclude the right name.
- **`output_mapping={"old": "new"}`** — rename columns for your downstream schema.

The single biggest win on any geometry-carrying extractor is **not emitting the geometry on
every row** — keep it in the input/dimension frame instead.

### 4b. Export format — `export_format`

`"csv"` (default) or `"parquet"`. Parquet is columnar, typed, and compressed — smaller files,
faster reads, preserved dtypes. Constant columns compress to almost nothing.

Resolution precedence: **workflow.yml `settings.export_format` > `EDAGRO_EXPORT_FORMAT` env var
> default `csv`**; or set `ext.export_format = "parquet"` directly. Error files always stay CSV.
See **[Cloud storage](13 - Cloud_storage_principles_and_usage.md)**.

### 4c. Manifest sidecar — `export_manifest`

Set `export_manifest = True` to also write a `<prefix>_manifest_<ts>.json` next to a successful
**bulk** export, describing the dataset (structure, entity count, date range, per-column
completeness) plus any `manifest_metadata` you attach (e.g. a region-dimension pointer + join
key). Precedence: **`settings.export_manifest` > `EDAGRO_EXPORT_MANIFEST` env > `False`**. It
fires only on a real bulk export (never on `skip_export=True` or single-entity calls) and is
non-fatal.

### 4d. KPI aggregation — `kpi_filter`

Where an extractor supports it (weather, VTS/MRTS…), a `kpi_filter` computes a
server/aggregate metric (e.g. a season sum or mean) and returns **one row per entity** instead
of one per day — often the largest row-count reduction available. See
**[KPIs](05 - Extractor_kpi_reference.md)**.

### 4e. Caching — `use_cache`

`use_cache=True` reuses cached per-entity responses and caches new ones, so re-runs skip the
API. Needs a **local** `cache_dir` (remote URIs disable it). See
**[Cache design](07 - Cache_design_context.md)**.

### 4f. Column mapping — `column_mapping`

Map your DataFrame's column names to the canonical ones the extractor expects
(`{"id": "amu_id"}`, `{"crop": "crop.id"}`, …). See
**[Column mapping](04 - Extractor_column_mapping_reference.md)**.

### 4g. Spatial grouping — `spatial_grouping`

The only lever here that cuts **API calls** rather than output size, and it applies to the
three centroid-queried extractors: `WeatherExtractor`, `GDDExtractor`, `GDDOffsetExtractor`.

Those query by field **centroid**, so fields whose centroids share a geohash cell get identical
values. With `spatial_grouping=True` the API is called once per cell and the result broadcast to
every member:

```python
result = ext.process_weather_bulk_extraction_parallel(
    entity_list=fields,
    spatial_grouping=True,     # off by default
)
```

Measured on 100 real soybean fields across 26 geohash-5 cells: **100 API calls become 26**, zero
on a warm cache, output identical to the ungrouped baseline.

**It pays on contiguous AOIs, not sparse ones.** Dedup is selection-dependent — the same source
file yields 7.8x across all 5112 fields but only 1.1x on a random 100-field sample, because a
scattered sample shares no cells. Check your geometry before assuming a win.

Grouped runs use a separate cell-keyed cache, and widening a window has consequences for
genuinely cumulative columns. Both are covered in
**[Result caching](07%20-%20Cache_design_context.md#spatial-grouping-a-second-cell-keyed-cache)**.



## 5. Recommended recipe

For a large, tidy, analysis-ready pull on any extractor:

```python
ext.setup_<type>_parameters(
    ...,                                   # analytic params
    output_columns=[...],                  # or exclude_columns=["geometry", ...]
    column_mapping={...},                  # if your columns differ
)
ext.export_format = "parquet"
ext.export_manifest = True                 # provenance + structure sidecar
res = ext.process_<type>_bulk_parallel(entity_list=entities, output_path=OUT,
                                        prefix="<dataset>", max_workers=8)
```

Declaratively, in `workflow.yml`:

```yaml
workflow:
  settings:
    export_format: parquet
    export_manifest: true
  steps:
    - name: regional
      extractor: RegionalExtractor
      module: earthdaily.agriculture.extractors.regional_ts_extractor
      setup:
        method: setup_regional_parameters
        params:
          index: average-temperature
          idblock: 129
          idpixeltype: 8
          output_columns: [entity_id, date, day_id, value]
          column_mapping: {id: amu_id}
```

---

## 6. When *not* to slim down

- **You need geometry per row downstream** (e.g. a GIS tool that can't join) — keep it, and
  prefer Parquet so the repeated polygon dictionary-encodes instead of being copied as text.
- **Ad-hoc exploration of a few fields** — the defaults are fine; optimization matters at scale.
- **A consumer that only reads CSV/SQL** — Parquet is columnar and not directly SQL-readable by
  every tool; keep CSV (or provide both) if the downstream can't read Parquet.

---

## See also

- **[Extractor parameters](03 - Extractor_parameters_reference.md)** — every `setup_*` argument
- **[Column mapping](04 - Extractor_column_mapping_reference.md)** · **[KPIs](05 - Extractor_kpi_reference.md)** · **[Cache design](07 - Cache_design_context.md)**
- **[Cloud storage](13 - Cloud_storage_principles_and_usage.md)** — Parquet + remote (S3/Azure) writes
