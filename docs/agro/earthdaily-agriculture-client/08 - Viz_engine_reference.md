---
title: Viz engine reference
description: YAML-driven charting and statistics for any extraction DataFrame via col_specs.
#icon: material/chart-box-outline
keywords:
  - viz_engine
  - charts
  - col_specs
  - plotting
  - statistics
  - reporting
---

# Viz Engine Reference

`earthdaily.agriculture.reporting.viz_engine` provides YAML-driven charting and statistics
for any extraction DataFrame. All functions accept `col_specs` — a list of column
descriptors that control what gets plotted and how.

See examples [here](./EDAgriculture_viz_engine_Showcase.ipynb)

---

## Column Spec Format

Every chart function is driven by `col_specs` — a list of dicts:

```python
col_specs = [
    {
        "name": "coverage_percent",    # column name in DataFrame (required)
        "label": "Coverage (%)",       # display label (optional, auto-derived from name)
        "type": "timeseries",          # numeric | timeseries | categorical | date
        "agg": "mean",                 # aggregation for multi-row data (optional)
        "color_scale": [               # threshold coloring for bar charts (optional)
            {"above": 90, "color": "#4CAF50"},
            {"above": 70, "color": "#FFC107"},
            {"above": 0,  "color": "#F44336"},
        ],
    },
]
```

| Field | Required | Values | Description |
|---|---|---|---|
| `name` | yes | column name | DataFrame column to visualize |
| `label` | no | string | Display label (defaults to `name` in Title Case) |
| `type` | yes | `numeric`, `timeseries`, `categorical`, `date` | Determines which charts handle this column |
| `agg` | no | `mean`, `max`, `min`, `last` | Aggregation for multi-row-per-entity data |
| `color_scale` | no | list of `{above, color}` | Threshold coloring for per-entity bars |

---

## Config Generation

### generate_viz_config

Auto-generate `col_specs` from a DataFrame instead of writing them manually.

```python
generate_viz_config(df, entity_col="id", date_col="date", save_to=None, timeseries_threshold=10)
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame to analyze |
| `entity_col` | `"id"` | Entity identifier column (skipped from specs) |
| `date_col` | `"date"` | Date column (skipped from specs) |
| `save_to` | `None` | Path to save as YAML (e.g. `"results/coverage_viz.yaml"`) |
| `timeseries_threshold` | `10` | Min unique values per entity to classify as `timeseries` vs `numeric` |

**Returns:** `dict` with keys `entity_col`, `date_col`, `col_specs`

```python
from earthdaily.agriculture.reporting.viz_engine import generate_viz_config

config = generate_viz_config(df, save_to="results/coverage_viz.yaml")
# Edit the YAML, then reload
```

---

### load_viz_config

Reload a saved YAML config.

```python
load_viz_config(path)
```

| Parameter | Default | Description |
|---|---|---|
| `path` | *required* | Path to the YAML file |

**Returns:** `dict` with keys `entity_col`, `date_col`, `col_specs`

**Requires:** `pyyaml` (`pip install pyyaml`)

```python
from earthdaily.agriculture.reporting.viz_engine import load_viz_config

config = load_viz_config("results/coverage_viz.yaml")
timeseries_chart(df, config["col_specs"],
    entity_col=config["entity_col"], date_col=config["date_col"])
```

---

## Statistics & KPI

### kpi_summary

Text-based statistical summary for all column types.

```python
kpi_summary(df, col_specs, entity_col="id", date_col="date")
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_specs` | *required* | Column specifications |
| `entity_col` | `"id"` | Entity identifier column |
| `date_col` | `"date"` | Date column |

**Handles:** `numeric`/`timeseries` (mean, median, std, min, max), `categorical` (value counts), `date` (earliest, latest, median)

---

### print_column_stats

Detailed descriptive statistics for a single column.

```python
print_column_stats(df, column, top_n=10)
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `column` | *required* | Column name to analyze |
| `top_n` | `10` | Number of top values to show |

**Handles:** any column type — null counts, unique counts, top-N values, numeric stats

---

### column_stats

Same as `print_column_stats` but returns a dict instead of printing.

```python
column_stats(df, column, top_n=10)
```

**Returns:** `dict` with keys like `total`, `non_null`, `null`, `unique`, `mean`, `median`, `std`, `min`, `max`, `top_values`

---

### grouped_stats

Statistics for a numeric column broken down by a categorical column.

```python
grouped_stats(df, column, groupby, decimals=4)
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `column` | *required* | Numeric column to analyze |
| `groupby` | *required* | Categorical column to group by |
| `decimals` | `4` | Decimal precision |

**Returns:** `pd.DataFrame` with stats (count, mean, median, std, min, max) per group

---

### kpi_groupby

Cross-table of KPI statistics broken down by a grouping column.

```python
kpi_groupby(df, col_specs, groupby, entity_col="id", date_col="date", decimals=4, stats=None)
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_specs` | *required* | Column specifications |
| `groupby` | *required* | Column to group by |
| `entity_col` | `"id"` | Entity identifier column |
| `date_col` | `"date"` | Date column |
| `decimals` | `4` | Decimal precision |
| `stats` | `None` | List of stats to include (default: all) |

**Handles:** `numeric`, `timeseries`
**Returns:** `pd.DataFrame` with KPI labels as rows, (group, stat) as MultiIndex columns

---

## Charts

### distribution_chart

Histograms and bar charts for non-timeseries columns.

```python
distribution_chart(df, col_specs, entity_col="id", date_col="date", env="")
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_specs` | *required* | Column specifications |
| `entity_col` | `"id"` | Entity identifier column |
| `date_col` | `"date"` | Date column |
| `env` | `""` | Environment label for title |

**Handles:**
- `numeric` — histogram across all entities
- `date` — histogram by day-of-year
- `categorical` — value-counts bar chart

**Skips:** `timeseries` (use `timeseries_chart` instead)

---

### per_entity_chart

Horizontal bar chart showing each entity's value, sorted and color-coded.

```python
per_entity_chart(df, col_specs, entity_col="id", date_col="date", env="")
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_specs` | *required* | Column specifications |
| `entity_col` | `"id"` | Entity identifier column |
| `date_col` | `"date"` | Date column |
| `env` | `""` | Environment label for title |

**Handles:** `numeric` (sorted bars with `color_scale` thresholds), `date` (day-of-year bars)
**Skips:** `timeseries`, `categorical`

---

### entity_chart

Grouped bar chart comparing multiple numeric properties across entities.

```python
entity_chart(df, col_specs, entity_col="id", name_col=None, date_col="date")
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_specs` | *required* | Column specifications |
| `entity_col` | `"id"` | Entity identifier column |
| `name_col` | `None` | Column for entity display names (falls back to `entity_col`) |
| `date_col` | `"date"` | Date column |

**Handles:** `numeric`, `timeseries` — each becomes a bar group per entity

---

### timeseries_chart

Line charts with three display modes.

```python
timeseries_chart(df, col_specs, entity_col="id", date_col="date", env="",
                 mode="all", aggregation="mean", entity_id=None,
                 season_config=None,
                 season_start=None, season_end=None, season_duration=None)
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_specs` | *required* | Column specifications |
| `entity_col` | `"id"` | Entity identifier column |
| `date_col` | `"date"` | Date column |
| `env` | `""` | Environment label for title |
| `mode` | `"all"` | Display mode (see below) |
| `aggregation` | `"mean"` | Central tendency: `mean` or `median` |
| `entity_id` | `None` | Entity to display (season mode only) |
| `season_config` | `None` | Season config dict from YAML |
| `season_start` | `None` | Season start as `"DD/MM"` (overrides season_config) |
| `season_end` | `None` | Season end as `"DD/MM"` (overrides season_config) |
| `season_duration` | `None` | Season length in days (overrides season_config) |

**Handles:** `timeseries` only

**Modes:**

| Mode | Description |
|---|---|
| `"all"` | One line per entity, overlaid on the same chart |
| `"aggregation"` | Central tendency line +/- std deviation band across entities |
| `"season"` | Single entity sliced into growing seasons, overlaid year-by-year |

**Season mode** requires `entity_id` and either `season_start` + `season_end` or `season_start` + `season_duration`:

```python
timeseries_chart(df, specs, mode="season", entity_id="field_001",
                 season_start="01/10", season_duration=270)
```

---

### crosstab_chart

Heatmap of the cross-tabulation between two categorical columns.

```python
crosstab_chart(df, row_col, col_col, normalize=False)
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `row_col` | *required* | Categorical column for rows |
| `col_col` | *required* | Categorical column for columns |
| `normalize` | `False` | Show percentages (column-normalized) instead of counts |

---

### choropleth_map

Geographic map colored by a numeric column. Requires a GeoDataFrame with geometry.

```python
choropleth_map(gdf, value_col, entity_col="id", name_col=None, label=None, map_config=None)
```

| Parameter | Default | Description |
|---|---|---|
| `gdf` | *required* | GeoDataFrame with geometry column |
| `value_col` | *required* | Numeric column for coloring |
| `entity_col` | `"id"` | Entity identifier column |
| `name_col` | `None` | Column for hover labels |
| `label` | `None` | Color bar label |
| `map_config` | `None` | Dict with `color_ramp` (list of hex colors) |

```python
choropleth_map(gdf, "coverage_percent", name_col="name",
               map_config={"color_ramp": ["#FFEDA0", "#FD8D3C", "#BD0026"]})
```

---

## Comparison Charts

### scatter_comparison

1:1 scatter plot with R², RMSE, MAE, and bias statistics.

```python
scatter_comparison(df, col_1, col_2, label_1=None, label_2=None,
                   date_col=None, value_threshold=0.0, title="Scatter Comparison")
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_1` | *required* | First numeric column (x-axis) |
| `col_2` | *required* | Second numeric column (y-axis) |
| `label_1` | `None` | Display label for col_1 |
| `label_2` | `None` | Display label for col_2 |
| `date_col` | `None` | Date column for color-coding points |
| `value_threshold` | `0.0` | Points below threshold in both columns shown in gray |
| `title` | `"Scatter Comparison"` | Chart title |

---

### comparison_chart

Side-by-side time series overlay + scatter plot for two columns.

```python
comparison_chart(df, col_1, col_2, date_col="date", label_1=None, label_2=None,
                 value_threshold=0.0, title="Time Series Comparison")
```

| Parameter | Default | Description |
|---|---|---|
| `df` | *required* | DataFrame |
| `col_1` | *required* | First value column |
| `col_2` | *required* | Second value column |
| `date_col` | `"date"` | Date column for x-axis |
| `label_1` | `None` | Display label for col_1 |
| `label_2` | `None` | Display label for col_2 |
| `value_threshold` | `0.0` | Points below threshold grayed out |
| `title` | `"Time Series Comparison"` | Chart title |

---

## Cross-Summary

### build_cross_summary

Build an entity-level summary table by aggregating one KPI per analytic.

```python
build_cross_summary(analytics_dict, entities_df, viz_analytics_cfg)
```

| Parameter | Default | Description |
|---|---|---|
| `analytics_dict` | *required* | Dict of `{analytic_name: DataFrame}` |
| `entities_df` | *required* | Entity reference DataFrame |
| `viz_analytics_cfg` | *required* | Viz config dict with analytic definitions |

**Returns:** `pd.DataFrame` with one row per entity, one column per analytic KPI

---

## Quick Reference — Functions by Column Type

| Function | `numeric` | `timeseries` | `categorical` | `date` | Notes |
|---|:---:|:---:|:---:|:---:|---|
| `generate_viz_config` | x | x | x | x | Auto-detects types |
| `load_viz_config` | x | x | x | x | Loads YAML |
| `kpi_summary` | x | x | x | x | Text output |
| `column_stats` | x | x | x | x | Returns dict |
| `print_column_stats` | x | x | x | x | Text output |
| `distribution_chart` | x | | x | x | Histograms & bars |
| `per_entity_chart` | x | | | x | Sorted horizontal bars |
| `entity_chart` | x | x | | | Grouped bars |
| `timeseries_chart` | | x | | | Lines: all/agg/season |
| `grouped_stats` | x | | x | | Stats by group |
| `kpi_groupby` | x | x | | | KPI cross-table |
| `crosstab_chart` | | | x | | Heatmap |
| `choropleth_map` | x | | | | Requires GeoDataFrame |
| `scatter_comparison` | x | | | | 1:1 + stats |
| `comparison_chart` | x | x | | | Overlay + scatter |

---

## Quick Reference — Common Shared Parameters

| Parameter | Default | Used by | Description |
|---|---|---|---|
| `df` | *required* | all | Input DataFrame |
| `col_specs` | *required* | most | Column specifications list |
| `entity_col` | `"id"` | most | Entity identifier column |
| `date_col` | `"date"` | most | Date column |
| `env` | `""` | distribution, per_entity, timeseries | Environment label in title |
