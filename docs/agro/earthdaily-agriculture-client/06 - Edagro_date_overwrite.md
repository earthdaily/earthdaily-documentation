---
title: Date parameter override
description: Which date parameters each extractor exposes and whether they can be overridden per-entity from the input DataFrame.
#icon: material/calendar-edit
keywords:
  - dates
  - start_date
  - end_date
  - sowing_date
  - per-entity override
  - get_entity_value
---

# EarthDaily Agriculture Utils — Date Parameter Override Documentation

## Overview

This document maps every extractor's date-related parameters (`start_date`, `end_date`, `sowing_date`, `emergence_date`, season windows, `year`, etc.) declared in their `setup_*_parameters()` method, and whether those dates can be overridden per-entity by values carried in the input DataFrame (via `get_entity_value()` / `has_entity_field()` in the `get_*_api()` path).

Convention:
- **OVERRIDABLE** — entity value is read first, falling back to the setup param
- **ENTITY_ONLY** — date is read from the entity at API call time (no setup default, or setup acts as last-resort fallback)
- **NOT_OVERRIDABLE** — only `self.params` is read; entity date columns are ignored
- **N/A** — no date parameters in setup

> **A NOT_OVERRIDABLE row does not mean "reads no dates from the entity".** The
> matrix below is keyed on *setup* parameters, so a year-valued input that has no
> setup counterpart at all has no row to appear in. `historical_seasons` on
> Emergence and Harvest is exactly that case — see the section at the end. Read
> a NOT_OVERRIDABLE verdict as "the setup dates listed here are not overridable",
> not as a complete inventory of what the extractor reads per entity. Doc 04 is
> that inventory.

## Quick Reference Matrix

| Extractor | File | Date params in setup | Override status |
|---|---|---|---|
| **CoverageExtractor** | `extractors/coverage_function.py` | `start_date`, `end_date` | NOT_OVERRIDABLE (user-facing) |
| **FLMExtractor** | `extractors/FLM_functions.py` | — | N/A (image_id driven) |
| **VegetationTsExtractor** | `extractors/VTS_functions.py` | `start_date`, `end_date` | OVERRIDABLE |
| **MRTSExtractor** | `extractors/VTS_functions.py` | `start_date`, `end_date` | OVERRIDABLE |
| **WeatherExtractor** | `extractors/weather_functions.py` | — | ENTITY_ONLY (`start_date`, `end_date` read from row) |
| **RegionalExtractor** | `extractors/regional_ts_extractor.py` | `start_date`, `end_date` | NOT_OVERRIDABLE |
| **cropidExtractor** | `extractors/cropid_functions.py` | `begin_year`, `end_year` | NOT_OVERRIDABLE |
| **ZoningExtractor** | `extractors/zoning_functions.py` | — | N/A (image_id driven) |
| **DifferenceExtractor** | `extractors/difference_functions.py` | — | N/A (image_id pair) |
| **ChangeIndexExtractor** | `processors/processor_change_index_functions.py` | — | N/A (image_id pair) |
| **GreennessExtractor** | `processors/processor_greenness_functions.py` | `season_duration`, `season_start_day`, `season_start_month`, `year`, `sowing_date` | OVERRIDABLE (`sowing_date` only) |
| **DiseaseExtractor** | `processors/processor_disease_risk_functions.py` | `start_date`, `end_date` | OVERRIDABLE |
| **EmergenceExtractor** | `processors/processor_emergence_functions.py` | `season_duration`, `season_start_day`, `season_start_month`, `year` | NOT_OVERRIDABLE — but see `historical_seasons` below, an ENTITY_ONLY year input with no setup counterpart |
| **HarvestExtractor** | `processors/processor_harvest_functions.py` | `season_duration`, `season_start_day`, `season_start_month`, `year` | NOT_OVERRIDABLE — but see `historical_seasons` below, an ENTITY_ONLY year input with no setup counterpart |
| **PlantedExtractor** | `processors/processor_plantedarea_functions.py` | `emergence_date` | NOT_OVERRIDABLE |
| **HistoricalScoreExtractor** | `processors/processor_score_functions.py` | `season_duration`, `season_start_day`, `season_start_month`, `year`, `threshold_start`, `historical_seasons` | OVERRIDABLE (`historical_seasons` only) |
| **InSeasonScoreExtractor** | `processors/processor_score_functions.py` | `season_duration`, `season_start_day`, `season_start_month`, `nb_historical_year`, `threshold_start`, `historical_seasons` | OVERRIDABLE (`sowing_date`, `end_date`, `historical_seasons`) |
| **InSeasonMonitoringExtractor** | `processors/processor_inseason_monitoring_functions.py` | `season_duration`, `season_start_day`, `season_start_month`, `year` | NOT_OVERRIDABLE |
| **BaresoilExtractor** | `processors/processor_baresoil_function.py` | `season_duration`, `season_start_day`, `season_start_month`, `year` | NOT_OVERRIDABLE |
| **ZARCExtractor** | `processors/processor_zarc_functions.py` | — | ENTITY_ONLY (**`emergence_date`** required on row — *not* `sowing_date`) |

## Extractors where entity dates take precedence (OVERRIDABLE)

These extractors read the date(s) from the row first, and fall back to `self.params` only when the column is missing or empty.

| Extractor | Overridable fields | Notes |
|---|---|---|
| **VegetationTsExtractor** | `start_date`, `end_date` | In `period` mode the resolved `start_date` is expanded back by `historical_years` before the API call; `windows` mode uses dates as-is. |
| **MRTSExtractor** | `start_date`, `end_date` | `sowing_date` is surfaced but not injected into the payload. |
| **DiseaseExtractor** | `start_date`, `end_date` | Dates are resolved in `process_single_entity_disease()` and written back onto the row before the API call. |
| **GreennessExtractor** | `sowing_date` | Season window (`season_*`, `year`) remains fixed from setup — only `sowing_date` is per-entity. |
| **InSeasonScoreExtractor** | `sowing_date`, `end_date`, `historical_seasons` | If `end_date` is missing, it is computed as `sowing_date + season_duration`. |
| **HistoricalScoreExtractor** | `historical_seasons` | All other temporal params (`season_*`, `year`, `threshold_start`) are strictly from setup. |

## Extractors that require dates from the entity (ENTITY_ONLY)

These extractors do not expose date defaults in `setup_*_parameters()` and expect the date values to be present on each entity row.

| Extractor | Required entity date fields | Notes |
|---|---|---|
| **WeatherExtractor** | `start_date`, `end_date` | KPI mode extends `start_date` backwards internally for historical comparison. |
| **ZARCExtractor** | `emergence_date` | Read as `entity_data.get("emergence_date")` and **raises** when absent. Validated via `safe_parse_date()`. `sowing_date` is an API *output* column, never an input — the extractor never reads one. ⚠️ Read with a plain `.get()`, so `column_mapping` does **not** apply to it. |

## Extractors whose setup dates are NOT overridable per entity

These read dates strictly from `self.params`; any `start_date` / `end_date` / `sowing_date` columns on the input DataFrame are ignored.

| Extractor | Setup dates read only from params |
|---|---|
| **CoverageExtractor** | `start_date`, `end_date` (a private `_coverage_*` override path exists but is used only by the internal crop-coverage filter, never by end users) |
| **RegionalExtractor** | `start_date`, `end_date` |
| **cropidExtractor** | `begin_year`, `end_year` |
| **EmergenceExtractor** | `season_*`, `year` |
| **HarvestExtractor** | `season_*`, `year` |
| **PlantedExtractor** | `emergence_date` |
| **InSeasonMonitoringExtractor** | `season_*`, `year` |
| **BaresoilExtractor** | `season_*`, `year` |

## Extractors with no date parameters (N/A)

These extractors are driven by image IDs or geometry only, so date overrides are not applicable:

- **FLMExtractor** — `image_id`
- **ZoningExtractor** — `image_id`, `num_zones`
- **DifferenceExtractor** — `image_id_1`, `image_id_2`
- **ChangeIndexExtractor** — `image_id_1`, `image_id_2`

## Implementation pattern reference

The canonical override pattern (used by VTS, MRTS, Disease, Greenness, InSeasonScore) is:

```python
start_date = self.get_entity_value(entity_data, "start_date", self.params["start_date"])
end_date   = self.get_entity_value(entity_data, "end_date",   self.params["end_date"])
```

`get_entity_value()` honors the extractor's `column_mapping`, so platform exports that use e.g. `sowingDate` instead of `sowing_date` still resolve correctly when the mapping is configured at construction time.

## `historical_seasons` — a year input with no setup parameter

Two extractors read a per-entity list of calendar years that never appears in the
matrix above, because it has no `setup_*_parameters()` counterpart to be
overridable *of*:

| Extractor | Mode | Entity key | Status |
|---|---|---|---|
| **EmergenceExtractor** | `emergence_type: HISTORICAL` | `historical_seasons` | ENTITY_ONLY |
| **HarvestExtractor** | `harvest_type: HISTORICAL_HARVEST` | `historical_seasons` | ENTITY_ONLY |

```python
historical_seasons = self.get_entity_value(row, "historical_seasons", default=None)
```

The value is the years the field actually grew the crop — `"2020,2022,2024"` or
`[2020, 2022, 2024]`. Years outside it are nulled out of `<event>_year_N`, and
`avg_emergence_matching_years` / `avg_harvest_matching_years` average only the
years kept.

Contrast the Score extractors, where `historical_seasons` **is** a setup
parameter and therefore genuinely OVERRIDABLE: entity value first, setup value as
the fallback. On Emergence and Harvest there is no fallback to fall back to.

> **Absence is silent.** `default=None` means a missing or mis-mapped column
> filters nothing and raises nothing — the run succeeds with all five years and
> an average over all of them. Nothing in the output says the filter did not
> apply, so confirm the column resolved rather than inferring it from a clean run.
