---
title: Extractor parameters reference
description: The extractor-specific setup_*_parameters() options for every extractor, with defaults and value ranges.
#icon: material/tune
keywords:
  - parameters
  - setup_parameters
  - extractor configuration
  - defaults
  - reference
---

# Extractor Parameters Reference

Each extractor has a `setup_*_parameters()` method that configures the extraction.
This document lists the **extractor-specific** parameters for each.

**Shared parameters** (available on all extractors, not listed below):
`column_mapping`, `output_mapping`, `exclude_columns`, `output_columns`, `use_cache`, `partial_frequency`

## Check the output modes before you write a transform

Several extractors take a parameter that changes the **shape** of what they
return, not just its content — `cropidExtractor`'s `mode`, `FLMExtractor`'s and
`ZoningExtractor`'s `postprocess`, `MRTSExtractor`'s `mode`,
`HistoricalScoreExtractor`'s `detail_level`, `BaresoilExtractor`'s `filter`.
They exist so a chain can get its input in the shape the next step wants,
without glue.

So when you are about to write a transform, check the producing extractor's mode
table first. The common mistake is to take the default shape and reshape it by
hand: chaining CropID into Emergence looks like it needs a transform to collapse
CropID's one-row-per-year output into a per-entity list of years — but
`mode: historical_season` already emits exactly that, one row per entity.

Two things follow, and they remove most of the remaining glue:

- **Entity columns ride through.** Every extractor stamps the input row's
  columns onto its results (`normalize_with_metadata`), which is why
  `exclude_columns=["geometry"]` exists at all. So `id`, `geometry` and `crop`
  survive a step, and a downstream `depends_on` receives them — no merge-back.
- **Reach for a transform when the grain genuinely changes**, or when two
  independent branches have to be joined. Renaming a column is not that; use
  `column_mapping` (entity side) or `output_mapping` (result side).

> ⚠️ `output_mapping` is an extractor-level setting, applied via
> `configure_output()`. **A workflow step cannot reach it** — a step's `setup`
> block is a single method call, so it runs `setup_*_parameters()` *or*
> `configure_output()`, not both. In a workflow, rename on the entity side with
> `settings.column_mapping`, which is global to the run.

---

## Foundational

### CoverageExtractor

**Method:** `setup_coverage_parameters()`
**Module:** `earthdaily.agriculture.extractors.coverage_function`

| Parameter | Default | Description |
|---|---|---|
| `vegetation_index` | `"NDVI"` | Index type (NDVI, EVI, CVI, CVIN, GNDVI, LAI, NDWI, NDMI, S2REP) |
| `start_date` | `"2025-01-01"` | Coverage period start (YYYY-MM-DD) |
| `end_date` | `None` | Coverage period end (YYYY-MM-DD). `None` applies **no upper bound** — every image from `start_date` onward is returned, it is not capped at today |
| `clear_cover_min` | `90` | Minimum clear cover percentage |
| `clear_cover_max` | `100` | Maximum clear cover percentage |
| `use_specific_date` | `False` | Use exact date matching |
| `filter` | `"none"` | Filter mode: `none`, `duplicate`, `crop_coverage` |
| `delay` | `3` | Processing delay in days |
| `mask` | `"auto"` | Mask type: `auto`, `native`, `ACM`, `ML` |
| `recalibration` | `False` | Enable sensor recalibration |
| `historical_seasons` | `None` | List of prior years — **required** when `filter="crop_coverage"` (e.g. `[2024, 2023, 2022]`); the per-entity window is the entity's `start_date`/`end_date` month-day applied to each of those years |

---

### FLMExtractor

**Method:** `setup_flm_parameters()`
**Module:** `earthdaily.agriculture.extractors.FLM_functions`

| Parameter | Default | Description |
|---|---|---|
| `vegetation_index` | `"NDVI"` | Index type for field-level maps |
| `map_format` | `None` | Output map format |
| `output_epsg` | `4326` | Output coordinate system EPSG code |
| `postprocess` | `"stats"` | Post-processing mode: `stats`, `links`, `file`, `histogram` |
| `extract_stats` | `False` | Extract statistics from maps |
| `directLinks` | `False` | Return direct download links |
| `clipping` | `"FieldBorder"` | Clipping method |
| `buffer` | `0` | Buffer around geometry (meters) |
| `skip_existing` | `True` | Skip already-downloaded maps |
| `output_path` | `None` | Override output directory |

---

### VegationTsExtractor

**Method:** `setup_vegetation_ts_parameters()`
**Module:** `earthdaily.agriculture.extractors.VTS_functions`

| Parameter | Default | Description |
|---|---|---|
| `start_date` | `None` | Time series start (YYYY-MM-DD) |
| `end_date` | `None` | Time series end (YYYY-MM-DD) |
| `vegetation_index` | `"NDVI"` | Index type |
| `is_extrapolated` | `True` | Enable end-of-curve extrapolation |
| `limit` | `3000` | Max data points per request |
| `historical_years` | `10` | Number of historical years to compare |
| `extraction_mode` | `"period"` | Extraction mode — see below |
| `target_dates` | `None` | List of specific dates to extract |
| `kpi_filter` | `None` | KPI aggregation filter |

**`extraction_mode` values:**

| Mode | Description |
|---|---|
| `period` | Continuous extraction between `start_date` and `end_date`. Default. |
| `specific_dates` | Extract only on the dates listed in `target_dates`. Requires `target_dates`. |
| `windows` | Per-entity windowed extraction; `start_date` / `end_date` (or per-entity overrides) define the window. |

---

### MRTSExtractor

**Method:** `setup_mrts_parameters()`
**Module:** `earthdaily.agriculture.extractors.VTS_functions`

| Parameter | Default | Description |
|---|---|---|
| `start_date` | `"2025-05-01"` | Time series start (YYYY-MM-DD) |
| `end_date` | `"2025-10-15"` | Time series end (YYYY-MM-DD) |
| `sensors` | `None` | Sensor filter (Sentinel-2, Landsat, etc.) |
| `vegetation_index` | `"NDVI"` | Index type |
| `aggregation` | `"average"` | Spatial aggregation method |
| `smoothing_method` | `"Whittaker"` | Smoothing algorithm |
| `apply_denoiser` | `True` | Enable denoising |
| `apply_end_of_curve` | `True` | Enable extrapolation |
| `clear_cover_min` | `100` | Minimum clear cover percentage |
| `output_saturation` | `True` | Output saturation flag |
| `extract_raw_datasets` | `True` | Include raw (unsmoothed) data |
| `compute_temporal_consistency` | `True` | Run temporal consistency check |
| `temporal_consistency_threshold` | `None` | Custom consistency threshold |
| `mode` | `"full"` | Output mode — see below |
| `historical_years` | `10` | Number of historical years |
| `kpi_filter` | `None` | KPI aggregation filter |

**`mode` values:**

| Mode | Description |
|---|---|
| `full` | Returns raw + smoothed values, with denoiser, end-of-curve extrapolation, and temporal-consistency flags. Default. |
| `raw` | Returns only raw per-image values (skips smoothing / denoising stages). |

---

### WeatherExtractor

**Method:** `setup_weather_parameters()`
**Module:** `earthdaily.agriculture.extractors.weather_functions`

| Parameter | Default | Description |
|---|---|---|
| `weather_type` | `"HISTORICAL_DAILY"` | Weather data type |
| `weather_parameters` | `"none"` | Specific weather parameters to extract |
| `kpi_filter` | `None` | KPI aggregation filter |

---

### cropidExtractor

**Method:** `setup_cropid_parameters()`
**Module:** `earthdaily.agriculture.extractors.cropid_functions`

| Parameter | Default | Description |
|---|---|---|
| `begin_year` | `2020` | First year of crop history |
| `end_year` | `2025` | Last year of crop history |
| `mask_type` | `"EndSeason"` | Mask type: `EndSeason`, `InSeason`, or `PreSeason` |
| `limit_nb_crop` | `1` | Number of top crops to return |
| `crop_mask_percent` | `50` | Minimum crop mask percentage |
| `mode` | `"history"` | Extraction mode — see below |

**`mode` values:**

| Mode | Shape | Description |
|---|---|---|
| `history` | long-form | One row per (year, crop) across the window. Default. |
| `year` | long-form | Filtered to the entity's `crop`; rows for matching years only. |
| `historical_season` | one row, one string column | Comma-separated string of matching years (e.g. `"2020,2022,2024"`). |
| `full_history` | wide-form | One row per entity, one column per year in `begin_year..end_year` (NaN if no data). Multi-crop years collapse to the top crop by `cropMaskPercent`. Convenient as an entity-level summary to merge alongside other extractors. |

---

### ZoningExtractor

**Method:** `setup_zoning_parameters()`
**Module:** `earthdaily.agriculture.extractors.zoning_functions`

| Parameter | Default | Description |
|---|---|---|
| `num_zones` | `5` | Number of management zones |
| `output_epsg` | `4326` | Output coordinate system EPSG code |
| `postprocess` | `"stats"` | Post-processing mode: `stats`, `stats_geo`, `links`, `file` |
| `map_format` | `None` | Output map format |
| `output_path` | `None` | Override output directory |
| `skip_existing` | `True` | Skip already-processed entities |
| `directLinks` | `False` | Return direct download links |

**`postprocess` values:**

| Mode | Description |
|---|---|
| `stats` | One field-level row per entity: variability, productivity/variability indices, and `zone_{n}_*` columns. Default. |
| `stats_geo` | One row **per zone**, carrying that zone's geometry (segments merged into a `GEOMETRYCOLLECTION`) plus its mean/max/min/area, with the field-level stats repeated on every row. |
| `links` | Direct download links (requires `directLinks=True`, set automatically). |
| `file` | Downloads the map; requires `map_format` and `output_path`. |

---

### LocationBasedBorderExtractor

**Method:** `setup_location_based_border_parameters()`
**Module:** `earthdaily.agriculture.extractors.location_based_border_functions`

Wraps the Geosys `/field-borders/v1/AutomaticBoundary` endpoint. Consumes a DataFrame with a Point WKT in the `geometry` column and returns the field polygon (WKT) containing that point.

| Parameter | Default | Description |
|---|---|---|
| `simplified_geom` | `True` | If `True`, the API returns a simplified field geometry (lower shape-point count). Maps to the `simplified_geom` query parameter. |

**Required entity fields:** `id`, `geometry` (must be a **Point** WKT — polygons are rejected with a clear error so callers can pre-process to a centroid via `core.geometry.get_centroid_wkt()`).

**Output columns:** `entity_id`, `point_geometry` (input echo), `polygon_geometry` (returned field border WKT), plus any flat scalar properties returned by the API (e.g. `area_ha`, `sourceId`).

---

## Regional

### RegionalExtractor

**Method:** `setup_regional_parameters()`
**Module:** `earthdaily.agriculture.extractors.regional_ts_extractor`

| Parameter | Default | Description |
|---|---|---|
| `index` | `"vegetation-vigor-index"` | Regional index type |
| `start_date` | `"2025-01-01"` | Period start (YYYY-MM-DD) |
| `end_date` | `None` | Period end (defaults to Dec 31 of current year) |
| `fillyeargap` | `False` | Fill year gaps in data |
| `idblock` | `None` | Block identifier |
| `idpixeltype` | `None` | Pixel type identifier |
| `indicatorTypeIds` | `None` | Indicator type IDs (auto-set to [1] for VVI) |

**Valid `index` values:** `vegetation-vigor-index`, `daily-precipitation`, `soil-moisture`, `min-temperature`, `max-temperature`, `average-temperature`, `surface-temperature`

**Valid `indicatorTypeIds`:** `1` (VVI), `2` (Weather ECMWF), `3` (Weather AROME France), `4` (Forecast ECMWF), `5` (Forecast GFS)

> `10` (Weather Reanalysis) and `11` (Rainfall Estimates HI-RES / CHIRPS) appear in the
> API documentation but are **not** accepted by this extractor — passing them raises
> `ValueError`. Widen `valid_indicatorTypeIds` in `regional_ts_extractor.py` first.

---

## Crop Development & Stressors

### DiseaseExtractor

**Method:** `setup_disease_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_disease_risk_functions`

| Parameter | Default | Description |
|---|---|---|
| `start_date` | `None` | Risk assessment period start |
| `end_date` | `None` | Risk assessment period end |

---

### EmergenceExtractor

**Method:** `setup_emergence_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_emergence_functions`

| Parameter | Default | Description |
|---|---|---|
| `emergence_type` | `"INSEASON"` | Detection type — see below |
| `season_duration` | `120` | Season length in days |
| `season_start_day` | `1` | Season start day of month |
| `season_start_month` | `4` | Season start month (1-12) |
| `year` | `2025` | Target year |
| `data_source` | `"LR"` | Data source: `LR` or `MR` |
| `publish_af` | `False` | Publish analytic feature |

**`emergence_type` values:**

| Type | Description |
|---|---|
| `INSEASON` | Single emergence date for the current season (`emergence_date`, `emergence_status`, `confirmation_status`). Default. |
| `HISTORICAL` | Emergence dates for the last 5 years (`emergence_year_1`..`emergence_year_5`) plus `historical_average_emergence`. Also accepts an optional per-entity `historical_seasons` column — see below. |
| `DELAY` | Current-season emergence date compared to the historical average (`emergence_date`, `average_emergence_date`, `emergence_delay`). |

**`historical_seasons` — a per-entity input, not a setup parameter.** In
`HISTORICAL` mode the extractor reads a `historical_seasons` value off each
entity row (via `column_mapping`, like any other entity field): the calendar
years that field actually grew the crop, as `"2020,2022,2024"` or
`[2020, 2022, 2024]`. Years outside the list are nulled out of
`emergence_year_N`, and an extra `avg_emergence_matching_years` column (MM-DD)
holds the average recomputed over the years kept. `historical_average_emergence`
— the raw API average over all five seasons — is left untouched either way.

> **It fails silently.** The column is optional, so when it is absent (or mapped
> under the wrong name) nothing is filtered and nothing is raised: all five years
> come back and the output looks correct. If you are chaining CropID into
> Emergence to get this, check that the names line up — `cropidExtractor`'s
> `historical_season` mode emits **`historical_season`** (singular) while this
> extractor reads **`historical_seasons`** (plural), so the chain needs a
> `column_mapping` entry.

`HarvestExtractor` has the same mechanism in `HISTORICAL_HARVEST` mode, producing
`avg_harvest_matching_years`.

`sowing_date` is **not** read in any mode — the season window comes from
`season_start_month` / `season_start_day` / `season_duration` / `year` here.

---

### GreennessExtractor

**Method:** `setup_greenness_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_greenness_functions`

| Parameter | Default | Description |
|---|---|---|
| `season_duration` | `120` | Season length in days |
| `season_start_day` | `1` | Season start day of month |
| `season_start_month` | `4` | Season start month (1-12) |
| `year` | `2025` | Target year |
| `sowing_date` | `"2025-04-01"` | Default sowing date (YYYY-MM-DD) |
| `data_source` | `"LR"` | Data source: `LR` or `MR` |
| `publish_af` | `False` | Publish analytic feature |

---

### HarvestExtractor

**Method:** `setup_harvest_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_harvest_functions`

| Parameter | Default | Description |
|---|---|---|
| `harvest_type` | `"INSEASON_HARVEST"` | Detection type — see below |
| `season_duration` | `120` | Season length in days |
| `season_start_day` | `1` | Season start day of month |
| `season_start_month` | `4` | Season start month (1-12) |
| `year` | `2025` | Target year |
| `data_source` | `"LR"` | Data source: `LR` or `MR` |
| `publish_af` | `False` | Publish analytic feature |

**`harvest_type` values:**

| Type | Description |
|---|---|
| `INSEASON_HARVEST` | Single harvest date + status for the current season (`harvest_date`, `harvest_status`). Default. |
| `HISTORICAL_HARVEST` | Harvest dates for the last 5 years (`harvest_year_1`..`harvest_year_5`) plus `historical_harvest_average`. |
| `HARVEST_READINESS` | Estimated harvest-readiness date and an `is_ready` boolean. |

---

### PlantedExtractor

**Method:** `setup_planted_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_plantedarea_functions`

| Parameter | Default | Description |
|---|---|---|
| `processor_mode` | `"PLANTED_AREA"` | Processing mode — see below |
| `emergence_date` | `None` | Known emergence date override |
| `threshold` | `120` | Detection threshold |
| `control_threshold` | `4` | Control threshold |
| `publish_af` | `False` | Publish analytic feature |

**`processor_mode` values:**

| Mode | Description |
|---|---|
| `PLANTED_AREA` | Returns `planted_area_m2` and `planted_percentage` for the field. Default. |
| `CONTROL` | Returns control-check output: `difference`, `control_threshold`, `control_result` (used to validate planting status against a known baseline). |

---

### InSeasonMonitoringExtractor

**Method:** `setup_inseason_monitoring_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_inseason_monitoring_functions`

| Parameter | Default | Description |
|---|---|---|
| `season_duration` | `120` | Season length in days |
| `season_start_day` | `1` | Season start day of month |
| `season_start_month` | `4` | Season start month (1-12) |
| `year` | `"2025"` | Target year (string) |
| `data_source` | `"LR"` | Data source: `LR` or `MR` (one per run) |

---

### ChangeIndexExtractor

**Method:** `setup_change_index_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_change_index_functions`

Compares a reference image (one per entity, via `reference_date`) against the nearest prior image within a configurable look-back window to flag significant change on a field. Useful for harvest detection, stress events, tillage, and other rapid changes.

| Parameter | Default | Description |
|---|---|---|
| `map_type` | `"NDVI"` | Vegetation index — one of `NDVI`, `EVI`, `CVI`, `GNDVI`, `NDWI` |
| `collections` | `None` | Satellite collections list (default `["Sentinel-2"]` when `None`) |
| `max_period_reference` | `7` | Max days back from `reference_date` for the reference image |
| `max_period_previous` | `15` | Max days before the reference image for the previous image |
| `min_period_previous` | `5` | Min days before the reference image for the previous image |
| `same_sensor` | `False` | If `True`, require the same sensor for both images |
| `parameter_profile` | `"change_index_v1"` | API parameter profile name |
| `publish_af` | `False` | If `True`, include `field_id` in the request so the result is registered on the platform. **Set this to `True` — see the note below.** |

> **`publish_af=False` currently fails on this extractor.** The change-index API rejects a
> payload without `field_id`:
>
> ```
> 422 {"detail":[{"type":"missing","loc":["body","field_id"],"msg":"Field required"}]}
> ```
>
> so the default cannot complete a call. Pass `publish_af=True` until that is fixed —
> note this registers the result on the platform, and the entity must carry an `id`.
>
> This is specific to ChangeIndex; the other processors exposing `publish_af` are unaffected
> and their `False` default works. A fix is ticketed on the API side, because requiring a
> platform-managed `field_id` conflicts with this package's geometry-first design.


**Required entity fields:** `id`, `geometry`, `reference_date` (column-mapping aware).
**Optional entity fields:** `crop`, `sowing_date`.

**Output columns:** `entity_id`, `reference_date`, `status`, plus any change metrics returned by the API for the selected `map_type`.

---

## Risk Management

### HistoricalScoreExtractor

**Method:** `setup_historical_score_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_score_functions`

| Parameter | Default | Description |
|---|---|---|
| `season_duration` | `120` | Season length in days |
| `season_start_day` | `1` | Season start day of month |
| `season_start_month` | `4` | Season start month (1-12) |
| `threshold_start` | `0.7` | Score threshold start |
| `year` | `2025` | Target year |
| `historical_seasons` | `None` | List of years to compare |
| `data_source` | `"LR"` | Data source: `LR` or `MR` |
| `detail_level` | `"full"` | Output detail level — see below |
| `publish_af` | `False` | Publish analytic feature |

**`detail_level` values:**

| Level | Description |
|---|---|
| `full` | Summary metrics (`average_potential_score`, `olympic_mean_potential_score`, `standard_deviation`, `risk_score`) plus per-season `potential_score_<year>` and `season_break_<year>` columns. Default. |
| `summary` | Summary metrics only — one row per entity, no per-season detail. |

---

### InseasonScoreExtractor

**Method:** `setup_inseason_score_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_score_functions`

| Parameter | Default | Description |
|---|---|---|
| `season_duration` | `120` | Season length in days |
| `season_start_day` | `1` | Season start day of month |
| `season_start_month` | `4` | Season start month (1-12) |
| `nb_historical_year` | `1` | Number of historical years |
| `threshold_start` | `0.7` | Score threshold start |
| `historical_seasons` | `None` | List of years to compare |
| `data_source` | `"LR"` | Data source: `LR` or `MR` |
| `detail_level` | `"full"` | Output detail level — see below |
| `publish_af` | `False` | Publish analytic feature |

**`detail_level` values:**

| Level | Description |
|---|---|
| `full` | Summary metrics plus per-season `potential_score_<year>` and `season_break_<year>` columns. Default. |
| `summary` | Summary metrics only — one row per entity, no per-season detail. |

---

### ZARCExtractor

**Method:** `setup_zarc_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_zarc_functions`

| Parameter | Default | Description |
|---|---|---|
| `crop` | `"OTHERS"` | Crop type for ZARC lookup |
| `nb_days_sowing_emergence` | `20` | Days from sowing to emergence |
| `soil_type` | `None` | Soil type classification |
| `cycle` | `None` | Crop cycle type |

---

## Sustainability

### BaresoilExtractor

**Method:** `setup_baresoil_parameters()`
**Module:** `earthdaily.agriculture.processors.processor_baresoil_function`

| Parameter | Default | Description |
|---|---|---|
| `season_duration` | `120` | Season length in days |
| `season_start_day` | `1` | Season start day of month |
| `season_start_month` | `4` | Season start month (1-12) |
| `year` | `2025` | Target year |
| `filter` | `"summary"` | Output mode: `summary` or `detailed` |
| `publish_af` | `False` | Publish analytic feature |

---

## Quick Reference — All Params by Extractor

Legend: **S** = season window params (`season_duration`, `season_start_day`, `season_start_month`, `year`)

| Extractor | Dates | Index / Type | Season (S) | Data Source | Other key params |
|---|---|---|---|---|---|
| CoverageExtractor | `start_date`, `end_date` | `vegetation_index` | | | `clear_cover_min`, `filter`, `mask`, `delay`, `historical_seasons` |
| FLMExtractor | | `vegetation_index` | | | `clipping`, `buffer`, `output_epsg`, `postprocess`, `extract_stats` |
| VegationTsExtractor | `start_date`, `end_date` | `vegetation_index` | | | `extraction_mode`, `target_dates`, `historical_years`, `kpi_filter` |
| MRTSExtractor | `start_date`, `end_date` | `vegetation_index` | | `sensors` | `smoothing_method`, `clear_cover_min`, `mode`, `historical_years`, `kpi_filter` |
| WeatherExtractor | | | | | `weather_type`, `weather_parameters`, `kpi_filter` |
| cropidExtractor | | | | | `begin_year`, `end_year`, `mask_type`, `limit_nb_crop`, `mode` |
| ZoningExtractor | | | | | `num_zones`, `output_epsg`, `postprocess` |
| RegionalExtractor | `start_date`, `end_date` | `index` | | | `idblock`, `idpixeltype`, `indicatorTypeIds`, `fillyeargap` |
| DiseaseExtractor | `start_date`, `end_date` | | | | |
| EmergenceExtractor | | | **S** | `data_source` | `emergence_type` |
| GreennessExtractor | | | **S** | `data_source` | `sowing_date` |
| HarvestExtractor | | | **S** | `data_source` | `harvest_type` |
| PlantedExtractor | | | | | `processor_mode`, `emergence_date`, `threshold`, `control_threshold` |
| InSeasonMonitoringExtractor | | | **S** | `data_source` | |
| ChangeIndexExtractor | `reference_date` (per entity) | `map_type` | | `collections` | `max_period_reference`, `max_period_previous`, `min_period_previous`, `same_sensor`, `parameter_profile`, `publish_af` |
| HistoricalScoreExtractor | | | **S** | `data_source` | `threshold_start`, `historical_seasons`, `detail_level` |
| InseasonScoreExtractor | | | **S** | `data_source` | `nb_historical_year`, `threshold_start`, `historical_seasons`, `detail_level` |
| ZARCExtractor | | | | | `crop`, `nb_days_sowing_emergence`, `soil_type`, `cycle` |
| BaresoilExtractor | | | **S** | | `filter` |

---

## Common Param Patterns

### Season window params (shared by 7 extractors)

```python
season_duration=120,      # season length in days
season_start_day=1,       # day of month (1-31)
season_start_month=4,     # month (1-12, 4=April)
year=2025,                # target year
```

Used by: Emergence, Greenness, Harvest, InSeasonMonitoring, HistoricalScore, InseasonScore, Baresoil

### Date range params

```python
start_date="2025-01-01",  # YYYY-MM-DD
end_date="2025-12-31",    # YYYY-MM-DD or None
```

Used by: Coverage, VegationTs, MRTS, Weather (via entity), Disease, Regional

### KPI filter

```python
kpi_filter=None,           # dict with KPI aggregation rules
```

Used by: VegationTs, MRTS, Weather

See [here](05%20-%20Extractor_kpi_reference.md) for more details.

### Data source

```python
data_source="LR",          # "LR" (low-res) or "MR" (medium-res)
```

A single source per run — the API query carries one `dataSource` value. Run the
extractor twice if you need both resolutions.

Used by: Emergence, Greenness, Harvest, HistoricalScore, InseasonScore, InSeasonMonitoring
