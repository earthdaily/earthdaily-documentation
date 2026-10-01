---
title: Extractor column mapping reference
description: Which internal entity fields each extractor reads at runtime, the default DataFrame columns they map to, and which are required.
#icon: material/table-column
keywords:
  - column_mapping
  - entity fields
  - get_entity_value
  - required fields
  - DataFrame columns
---

# Extractor Column Mapping Reference

Each extractor inherits from `BaseExtractor` and uses `column_mapping` to resolve
entity fields from your DataFrame. This document lists which internal fields each
extractor actually uses at runtime.

**How to read these tables:**

- **Internal key** — the canonical name used in `get_entity_value(row, key)`
- **Default column** — the DataFrame column name looked up if no mapping is provided
- **Purpose** — what the extractor uses it for
- Fields marked **(required)** will cause errors if missing

---

## Foundational

### CoverageExtractor

**Module:** `earthdaily.agriculture.extractors.coverage_function`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for coverage query |
| `crop` | `crop` | Crop type (used in `crop_coverage` filter mode) |
| `start_date` | `start_date` | Coverage period start |
| `end_date` | `end_date` | Coverage period end |
| `historical_seasons` | `historical_seasons` | List of years for `crop_coverage` filter mode |

---

### FLMExtractor

**Module:** `earthdaily.agriculture.extractors.FLM_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for field-level map generation |
| `crop` | `crop` | Crop type (optional, for metadata) |

---

### VegationTsExtractor

**Module:** `earthdaily.agriculture.extractors.VTS_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon **(required)** |
| `crop` | `crop` | Crop type **(required)** |
| `start_date` | `start_date` | Time series period start |
| `end_date` | `end_date` | Time series period end |

---

### MRTSExtractor

**Module:** `earthdaily.agriculture.extractors.VTS_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for medium-resolution query |
| `crop` | `crop` | Crop type |
| `start_date` | `start_date` | Time series period start |
| `end_date` | `end_date` | Time series period end |

---

### WeatherExtractor

**Module:** `earthdaily.agriculture.extractors.weather_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon (centroid used for weather location) |
| `start_date` | `start_date` | Weather data period start |
| `end_date` | `end_date` | Weather data period end |

---

### cropidExtractor

**Module:** `earthdaily.agriculture.extractors.cropid_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for crop classification |
| `crop` | `crop` | Crop type (for result enrichment) |

---

### ZoningExtractor

**Module:** `earthdaily.agriculture.extractors.zoning_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for zoning query |

---

## Regional

### RegionalExtractor

**Module:** `earthdaily.agriculture.extractors.regional_ts_extractor`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Used for cache key columns |
| `amu_id` | `amu_id` | Regional AMU entity identifier (sent to API) |
| `start_date` | `start_date` | Regional time series period start |
| `end_date` | `end_date` | Regional time series period end |

---

## Crop Development & Stressors

### DiseaseExtractor

**Module:** `earthdaily.agriculture.processors.processor_disease_risk_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon (centroid for weather-based risk) |
| `start_date` | `start_date` | Disease risk period start |
| `end_date` | `end_date` | Disease risk period end |

---

### EmergenceExtractor

**Module:** `earthdaily.agriculture.processors.processor_emergence_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for emergence detection |
| `crop` | `crop` | Crop type for phenology model |
| `historical_seasons` | `historical_seasons` | *(optional, `HISTORICAL` only)* Calendar years this field actually grew the crop — `"2020,2022,2024"` or `[2020, 2022, 2024]`. Off-years are nulled out of `emergence_year_N`, and `avg_emergence_matching_years` averages only the years kept. **Absent, nothing is filtered and no error is raised** — all five years come back looking correct. |

> `sowing_date` is **not** read by this extractor. The season window comes from
> `season_start_month` / `season_start_day` / `season_duration` / `year` on
> `setup_emergence_parameters()`, and the request body carries only the geometry.

---

### GreennessExtractor

**Module:** `earthdaily.agriculture.processors.processor_greenness_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for greenness detection |
| `crop` | `crop` | Crop type for greenness model |
| `sowing_date` | `sowing_date` | Sowing date for season window |

---

### HarvestExtractor

**Module:** `earthdaily.agriculture.processors.processor_harvest_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for harvest detection |
| `crop` | `crop` | Crop type for harvest model |
| `historical_seasons` | `historical_seasons` | *(optional, `HISTORICAL_HARVEST` only)* Same contract as EmergenceExtractor above — filters `harvest_year_N` to the matching years and drives `avg_harvest_matching_years`. Silently inert when absent. |

> `sowing_date` is **not** read by this extractor, for the same reason as
> EmergenceExtractor.

---

### PlantedExtractor

**Module:** `earthdaily.agriculture.processors.processor_plantedarea_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for planted area estimation |

---

### InSeasonMonitoringExtractor

**Module:** `earthdaily.agriculture.processors.processor_inseason_monitoring_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for monitoring |
| `crop` | `crop` | Crop type for monitoring model |

---

## Risk Management

### HistoricalScoreExtractor

**Module:** `earthdaily.agriculture.processors.processor_score_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for score computation |
| `crop` | `crop` | Crop type for historical comparison |
| `historical_seasons` | `historical_seasons` | List of years to compare against |

---

### InseasonScoreExtractor

**Module:** `earthdaily.agriculture.processors.processor_score_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for score computation |
| `crop` | `crop` | Crop type for in-season scoring |
| `sowing_date` | `sowing_date` | Sowing date for season window |
| `end_date` | `end_date` | Season end date |
| `historical_seasons` | `historical_seasons` | List of years to compare against |

---

### ZARCExtractor

**Module:** `earthdaily.agriculture.processors.processor_zarc_functions`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for ZARC zone lookup |
| `crop` | `crop` | Crop type for ZARC compliance check |

---

## Sustainability

### BaresoilExtractor

**Module:** `earthdaily.agriculture.processors.processor_baresoil_function`

| Internal key | Default column | Purpose |
|---|---|---|
| `id` | `id` | Entity identifier |
| `geometry` | `geometry` | WKT polygon for bare soil analysis |

---

## Tips & Tricks

### Forcing setup-level values by neutralizing column_mapping

When chaining extractors in a workflow, the workflow-level `column_mapping` (e.g.
`start_date: "sowingDate"`) is applied to **all** extractors. A downstream extractor
will then pick up `sowingDate` from entity rows even when explicit values are set in the
setup params — because `get_entity_value` checks the entity row first and only falls
back to params when the mapped column is not found.

**Workaround:** Override the mapping at the step level to point at a column name that
doesn't exist in the entity rows. The extractor will then fall back to the setup-level
value.

```yaml
# Example: entity rows carry "sowingDate" but we want the extractor to use setup dates
column_mapping:
  start_date: "start_date"   # no column named "start_date" in rows → falls back to setup value
  end_date: "end_date"       # no column named "end_date" in rows → falls back to setup value
```

**Why it works:** `get_entity_value(row, "start_date", params.get("start_date"))` resolves
the mapped column name, finds no match in the row, and returns the params default.

This pattern applies to any internal key you want to force to the setup default:
`start_date`, `end_date`, `sowing_date`, `crop`, etc.

---

## Quick Reference — All Fields by Extractor

`x` = read at runtime · `o` = read at runtime, **optional and silently inert when
absent** — the run succeeds and the output looks complete, so a missing column is
only visible in the values.

| Extractor | `id` | `geometry` | `crop` | `start_date` | `end_date` | `sowing_date` | `historical_seasons` | `amu_id` | `batch_id` |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| CoverageExtractor | x | x | x | x | x | | x | | |
| FLMExtractor | x | x | x | | | | | | |
| VegationTsExtractor | x | x | x | x | x | | | | |
| MRTSExtractor | x | x | x | x | x | | | | |
| WeatherExtractor | x | x | | x | x | | | | |
| cropidExtractor | x | x | x | | | | | | |
| ZoningExtractor | x | x | | | | | | | |
| RegionalExtractor | x | | | x | x | | | x | |
| DiseaseExtractor | x | x | | x | x | | | | |
| EmergenceExtractor | x | x | x | | | | o | | |
| GreennessExtractor | x | x | x | | | x | | | |
| HarvestExtractor | x | x | x | | | | o | | |
| PlantedExtractor | x | x | | | | | | | |
| InSeasonMonitoringExtractor | x | x | x | | | | | | |
| HistoricalScoreExtractor | x | x | x | | | | x | | |
| InseasonScoreExtractor | x | x | x | | x | x | x | | |
| ZARCExtractor | x | x | x | | | | | | |
| BaresoilExtractor | x | x | | | | | | | |
