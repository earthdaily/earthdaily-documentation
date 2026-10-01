---
title: Extractor KPI reference
description: How kpi_filter aggregates time-series data into one value per entity, the supported aggregations, and which extractors support it.
#icon: material/chart-line
keywords:
  - kpi
  - kpi_filter
  - filter_timeseries_kpi
  - aggregation
  - historical comparison
---

# Extractor KPI Reference

KPI (Key Performance Indicator) filtering aggregates time-series data into a single value per entity,
with optional historical comparison. Instead of returning daily date/value rows, the extractor
returns one row per entity with the computed KPI, historical average, and percent change.

**Core function:** `filter_timeseries_kpi()` in `earthdaily.agriculture.core.api_utils`

See examples [here](./EDAgriculture_KPI_Showcase.ipynb)

---

## Supported extractors

| Extractor | Module | Setup method | KPI support |
|---|---|---|---|
| VegationTsExtractor | `earthdaily.agriculture.extractors.VTS_functions` | `setup_vegetation_ts_parameters()` | Yes |
| MRTSExtractor | `earthdaily.agriculture.extractors.VTS_functions` | `setup_mrts_parameters()` | Yes |
| WeatherExtractor | `earthdaily.agriculture.extractors.weather_functions` | `setup_weather_parameters()` | Yes |
| DiseaseExtractor | `earthdaily.agriculture.processors.processor_disease_risk_functions` | `setup_disease_parameters()` | Yes |
| CoverageExtractor | `earthdaily.agriculture.extractors.coverage_function` | `setup_coverage_parameters()` | No |
| FLMExtractor | `earthdaily.agriculture.extractors.FLM_functions` | `setup_flm_parameters()` | No |
| ZoningExtractor | `earthdaily.agriculture.extractors.zoning_functions` | `setup_zoning_parameters()` | No |
| cropidExtractor | `earthdaily.agriculture.extractors.cropid_functions` | `setup_cropid_parameters()` | No |
| RegionalExtractor | `earthdaily.agriculture.extractors.regional_ts_extractor` | `setup_regional_parameters()` | No |
| EmergenceExtractor | `earthdaily.agriculture.processors.processor_emergence_functions` | `setup_emergence_parameters()` | No |
| HarvestExtractor | `earthdaily.agriculture.processors.processor_harvest_functions` | `setup_harvest_parameters()` | No |
| GreennessExtractor | `earthdaily.agriculture.processors.processor_greenness_functions` | `setup_greenness_parameters()` | No |
| HistoricalScoreExtractor | `earthdaily.agriculture.processors.processor_score_functions` | `setup_historical_score_parameters()` | No |
| InseasonScoreExtractor | `earthdaily.agriculture.processors.processor_score_functions` | `setup_inseason_score_parameters()` | No |
| BaresoilExtractor | `earthdaily.agriculture.processors.processor_baresoil_function` | `setup_baresoil_parameters()` | No |
| ZARCExtractor | `earthdaily.agriculture.processors.processor_zarc_functions` | `setup_zarc_parameters()` | No |
| PlantedExtractor | `earthdaily.agriculture.processors.processor_plantedarea_functions` | `setup_planted_parameters()` | No |
| InSeasonMonitoringExtractor | `earthdaily.agriculture.processors.processor_inseason_monitoring_functions` | `setup_inseason_monitoring_parameters()` | No |

KPI filtering applies to extractors that produce **time-series data** (date + value rows).
Extractors that return single-event results (emergence date, harvest date, crop ID, scores) do not support KPI aggregation.

---

## How it works

1. The extractor retrieves the full time series from the API (current + historical years)
2. `filter_timeseries_kpi()` filters data into **current period** (start_date to end_date) and **historical periods** (same MM-DD window in past years)
3. The chosen aggregation is applied to both current and each historical year
4. Historical values are averaged, then compared to the current value

**Without** `kpi_filter`: output is one row per date (many rows per entity)
**With** `kpi_filter`: output is one row per entity with KPI columns

---

## Configuration

Pass `kpi_filter` as a dictionary to `setup_*_parameters()`:

```python
extractor.setup_mrts_parameters(
    start_date='2025-01-01',
    end_date='2025-06-30',
    historical_years=5,
    kpi_filter={
        'kpi_name': 'My KPI',           # Label (any string)
        'aggregation': 'accumulation',   # Required — aggregation method
        'threshold': None,               # Required for some aggregations (cutoff value, percentile rank, or (min, max) tuple)
        'window': None,                  # Required for rolling_avg* aggregations (integration period in records)
        'value_column': None,            # Optional — column to aggregate (auto-detected if omitted)
    }
)
```

`historical_years` controls how many past years are included for comparison.
Set to `0` to compute only the current period value (no historical comparison).

---

## Aggregation methods

| Aggregation | Description | Threshold | Window | Example use case |
|---|---|---|---|---|
| `accumulation` | Sum of all values in the period | Not used | Not used | Total NDVI over a season |
| `top_accumulation` | Sum of the N highest values | `int` — number of top days | Not used | Sum of 30 best NDVI days |
| `average` | Mean of all values | Not used | Not used | Average temperature |
| `max` | Maximum value in the period | Not used | Not used | Peak NDVI |
| `min` | Minimum value in the period | Not used | Not used | Lowest temperature |
| `std` | Standard deviation | Not used | Not used | Variability measurement |
| `count_gt` | Count of values above threshold | `float` — lower bound | Not used | Days with NDVI > 0.7 |
| `count_lt` | Count of values below threshold | `float` — upper bound | Not used | Days with temp < 0 |
| `count_between` | Count of values in range | `(min, max)` tuple | Not used | Days with NDVI between 0.3 and 0.7 |
| `rolling_avg` | Mean of the rolling-mean series over the period | Not used | `int` — integration period (records) | Smoothed seasonal NDVI |
| `rolling_avg_gt` | Count of rolling-mean points strictly above threshold | `float` — lower bound | `int` — integration period | Sustained high vigor periods |
| `rolling_avg_lt` | Count of rolling-mean points strictly below threshold | `float` — upper bound | `int` — integration period | Sustained low-vigor / stress windows |
| `percentile` | Value at the Pth percentile of the period | `float` — percentile rank 0–100 | Not used | Robust upper/lower-tail summary |
| `percentile_gt` | Count of values strictly above the Pth percentile of the period | `float` — percentile rank 0–100 | Not used | Upper-tail count (compare to historical) |
| `percentile_lt` | Count of values strictly below the Pth percentile of the period | `float` — percentile rank 0–100 | Not used | Lower-tail count (compare to historical) |

---

## Threshold and window rules

| Aggregation | Threshold required | Window required | Threshold type | Example |
|---|---|---|---|---|
| `accumulation` | No | No | — | — |
| `top_accumulation` | **Yes** | No | Positive `int` | `30` |
| `average` | No | No | — | — |
| `max` | No | No | — | — |
| `min` | No | No | — | — |
| `std` | No | No | — | — |
| `count_gt` | **Yes** | No | `int` or `float` | `0.7` |
| `count_lt` | **Yes** | No | `int` or `float` | `0.0` |
| `count_between` | **Yes** | No | Tuple `(min, max)` | `(0.3, 0.7)` |
| `rolling_avg` | No | **Yes** | — | `window=5` |
| `rolling_avg_gt` | **Yes** | **Yes** | `int` or `float` | `window=5, threshold=0.6` |
| `rolling_avg_lt` | **Yes** | **Yes** | `int` or `float` | `window=5, threshold=0.4` |
| `percentile` | **Yes** | No | `float` 0–100 (percentile rank) | `90` |
| `percentile_gt` | **Yes** | No | `float` 0–100 (percentile rank) | `90` |
| `percentile_lt` | **Yes** | No | `float` 0–100 (percentile rank) | `10` |

Providing a threshold for an aggregation that does not support it, or omitting one that's required, raises a `ValueError`.

`window` counts **records**, not calendar days — for sparse satellite series each record is an acquisition; for dense daily weather it is one day.

---

## Output columns

When `kpi_filter` is set, `process_single_entity_*()` returns a single-row DataFrame with:

| Column | Description |
|---|---|
| `kpi_name` | Label from `kpi_filter['kpi_name']` |
| `aggregation` | Aggregation method used |
| `start_date` | Period start |
| `end_date` | Period end |
| `current_value` | Computed KPI for current period |
| `current_num_records` | Number of data points in current period |
| `historical_avg` | Average KPI across historical years |
| `historical_num_years` | Number of historical years with data |
| `difference` | `current_value - historical_avg` |
| `percent_change` | Percentage change vs historical average |

Plus all entity metadata columns (id, name, crop, etc.) added by `normalize_with_metadata`.

---

## Value column

All extractors support an optional `value_column` key in `kpi_filter` to explicitly choose which column to aggregate.
When omitted, each extractor auto-detects a sensible default:

| Extractor | Default value column | Notes |
|---|---|---|
| VegationTsExtractor | `value` | Single value column |
| MRTSExtractor (raw mode) | `raw_value` | Raw satellite observations |
| MRTSExtractor (full mode) | `smoothed_value` | Smoothed interpolated curve |
| WeatherExtractor | First numeric column | Set `value_column` explicitly for weather (e.g. `precipitation`, `temperature_max`) |
| DiseaseExtractor | Set via `value_column` | Required — no auto-detection |

Override example — force MRTS to use `raw_value` even in full mode:

```python
kpi_filter={
    'kpi_name': 'Raw NDVI Total',
    'aggregation': 'accumulation',
    'value_column': 'raw_value',
}
```

---

## Examples by aggregation

### accumulation — Total NDVI over a season

```python
kpi_filter={
    'kpi_name': 'Season NDVI Total',
    'aggregation': 'accumulation',
}
```

### top_accumulation — Sum of 30 best days

```python
kpi_filter={
    'kpi_name': 'NDVI Top-30 Accumulation',
    'aggregation': 'top_accumulation',
    'threshold': 30,
}
```

### average — Mean LAI

```python
kpi_filter={
    'kpi_name': 'Average LAI',
    'aggregation': 'average',
}
```

### max — Peak vegetation index

```python
kpi_filter={
    'kpi_name': 'Peak NDVI',
    'aggregation': 'max',
}
```

### min — Minimum temperature

```python
kpi_filter={
    'kpi_name': 'Min Temperature',
    'aggregation': 'min',
}
```

### std — Vegetation variability

```python
kpi_filter={
    'kpi_name': 'NDVI Variability',
    'aggregation': 'std',
}
```

### count_gt — Days above threshold

```python
kpi_filter={
    'kpi_name': 'High Vigor Days',
    'aggregation': 'count_gt',
    'threshold': 0.7,
}
```

### count_lt — Days below threshold

```python
kpi_filter={
    'kpi_name': 'Frost Days',
    'aggregation': 'count_lt',
    'threshold': 0.0,
}
```

### count_between — Days in range

```python
kpi_filter={
    'kpi_name': 'Moderate NDVI Days',
    'aggregation': 'count_between',
    'threshold': (0.3, 0.7),
}
```

### rolling_avg — Smoothed mean over an integration window

```python
kpi_filter={
    'kpi_name': 'NDVI 5-Obs Rolling Avg',
    'aggregation': 'rolling_avg',
    'window': 5,
}
```

### rolling_avg_gt — Sustained high vigor periods

```python
kpi_filter={
    'kpi_name': 'High NDVI Rolling Periods (>0.6)',
    'aggregation': 'rolling_avg_gt',
    'window': 5,
    'threshold': 0.6,
}
```

### rolling_avg_lt — Sustained low vigor / stress windows

```python
kpi_filter={
    'kpi_name': 'Low NDVI Rolling Periods (<0.4)',
    'aggregation': 'rolling_avg_lt',
    'window': 5,
    'threshold': 0.4,
}
```

### percentile — Pth percentile value

```python
kpi_filter={
    'kpi_name': 'NDVI 90th Percentile',
    'aggregation': 'percentile',
    'threshold': 90,
}
```

### percentile_gt — Days above the period's Pth percentile

Most informative when combined with `historical_years` — exposes whether the upper tail of the current season is more (or less) populated than past seasons.

```python
kpi_filter={
    'kpi_name': 'Days Above 90th Percentile',
    'aggregation': 'percentile_gt',
    'threshold': 90,
}
```

### percentile_lt — Days below the period's Pth percentile

```python
kpi_filter={
    'kpi_name': 'Days Below 10th Percentile',
    'aggregation': 'percentile_lt',
    'threshold': 10,
}
```

---

## Standalone usage

`filter_timeseries_kpi` can also be called directly on any DataFrame with a date and value column:

```python
from earthdaily.agriculture.core.api_utils import filter_timeseries_kpi, format_kpi_results

result = filter_timeseries_kpi(
    timeseries_df=my_df,
    start_date='2025-01-01',
    end_date='2025-06-30',
    kpi_name='Custom KPI',
    aggregation='accumulation',
    threshold=None,         # cutoff value, percentile rank, or (min, max)
    window=None,            # integration period for rolling_avg* aggregations
    years='ALL',
    date_column='date',
    value_column='value'
)

# Pretty-print as DataFrame
display(format_kpi_results(result))
```

The `years` parameter controls historical comparison:
- `None` — no historical comparison
- `"ALL"` — use all available past years in the data
- `[2024, 2023, 2022]` — use only these specific years
