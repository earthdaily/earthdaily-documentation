---
title: Weather extractors
description: Field-level weather with WeatherExtractor (Weather v1) and WeatherFlowExtractor (WeatherFlow API) — choosing one, models, limits, columns and units, and how dates and times line up across countries.
keywords:
  - weather
  - WeatherFlow
  - ERA5
  - IFS
  - ICON-EU
  - forecast
  - hourly
  - time zones
---

# Weather extractors

Two extractors return field-level weather. Both take the field's **centroid**, a date range,
and return one row per day (or per hour) with your input columns kept.

| | `WeatherExtractor` | `WeatherFlowExtractor` |
|---|---|---|
| API | Weather v1 | WeatherFlow |
| Auth | EarthDaily Agriculture token | WeatherFlow API key (`X-API-Key`) |
| History | daily | daily and hourly |
| Forecast | daily and hourly | daily and hourly |
| Models | one provider | `era5`, `seamless`, `ifs`, `icon_eu` |
| Column names | `temperature.standardMax`, `precipitation.cumulative`, ... | the same Weather v1 names by default (or the API's own: `temperature_2m_max`, ...) |
| Units | your account's unit profile | `units="metric"` (default) or `"imperial"`, whatever the model |
| Soil moisture | no | yes (`soil.moisture0to7cm` ... `soil.moisture100to289cm`, `soil.moisture0to1cm`) |

Both share the same flow, so switching is mostly renaming:

| Step | `WeatherExtractor` | `WeatherFlowExtractor` |
|---|---|---|
| Setup | `setup_weather_parameters()` | `setup_weatherflow_parameters()` |
| One call | `get_weather_data()` | `get_weatherflow_data()` |
| Format | `format_weather_json()` | `format_weatherflow_json()` |
| One field | `process_single_entity_weather()` | `process_single_entity_weatherflow()` |
| Bulk | `process_entity_weather_bulk_parallel()` | `process_entity_weatherflow_bulk_parallel()` |

`historical_years`, `kpi_filter`, `use_cache` and `spatial_grouping` behave the same in both.

---

## WeatherFlowExtractor

### Authentication

WeatherFlow uses its own API key, not the EarthDaily Agriculture credentials. The first match
wins:

1. `WeatherFlowExtractor(..., api_key="...")`
2. `config["weatherflow_api_key"]`
3. `PROD_WEATHERFLOW_API_KEY` / `PREPROD_WEATHERFLOW_API_KEY` (keys are environment-specific)
4. `WEATHERFLOW_API_KEY`

Put the key in your `.env` file. A missing key fails when the extractor is built, not halfway
through a bulk run. The extractor needs no EarthDaily Agriculture token, so the first two
arguments can be `None`:

```python
from earthdaily.agriculture.core.functions_enhanced import setup_environment
from earthdaily.agriculture.extractors.weatherflow_functions import WeatherFlowExtractor

config = setup_environment(env="prod")
wf = WeatherFlowExtractor(None, None, config)
```

### Quick start

```python
import pandas as pd

fields = pd.DataFrame([
    {"id": "field_001", "geometry": "POLYGON ((...))", "start_date": "2025-04-01", "end_date": "2025-09-30"},
])

# Daily history (model None → era5)
wf.setup_weatherflow_parameters(weather_type="HISTORICAL_DAILY")
result = wf.process_entity_weatherflow_bulk_parallel(fields, spatial_grouping=True)
daily = result["results_df"]

# Keep only some columns, by Weather v1 name (or by API name: "temperature_2m_max")
wf.setup_weatherflow_parameters(weather_parameters=["temperature.standardMax", "precipitation.cumulative"])

# US units
wf.setup_weatherflow_parameters(units="imperial")

# Hourly forecast (model None → ifs). Dates are local to each field: see "Dates and times".
wf.setup_weatherflow_parameters(weather_type="FORECAST_HOURLY")

print(wf.output_units)  # {"temperature.standardMax": "°C", "precipitation.cumulative": "mm", ...}
```

`list_models()` lists what every model serves; `describe_model("era5")` lists each model's
columns with the units the API sends them in.

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `weather_type` | `"HISTORICAL_DAILY"` | `HISTORICAL_DAILY`, `HISTORICAL_HOURLY`, `FORECAST_DAILY` or `FORECAST_HOURLY` |
| `model` | `None` | `era5`, `seamless`, `ifs` or `icon_eu`. `None` uses `era5` for history and `ifs` for forecasts |
| `weather_parameters` | `"none"` | Columns to keep, by Weather v1 name or API name; `"none"` keeps all |
| `units` | `"metric"` | Output unit profile: `metric`, `imperial`, or `native` (the API's own units) |
| `naming` | `"weather_v1"` | Output column names: `weather_v1` (`temperature.standardMax`) or `api` (`temperature_2m_max`) |
| `historical_years` | `0` | Prior years to fetch for a KPI comparison (0–15, or a list of years) |
| `kpi_filter` | `None` | KPI aggregation, as for `WeatherExtractor` |
| `use_cache` | `None` | Reuse cached responses |

### Models and limits

What each model serves, from `GET /models` (October 2026):

| Model | Daily history | Hourly history | Daily forecast | Hourly forecast |
|---|---|---|---|---|
| `era5` | yes | yes | — | — |
| `seamless` | yes | yes | — | — |
| `ifs` | yes (last 15 days) | yes (last 15 days) | yes | yes (3-hour steps) |
| `icon_eu` | yes | — | — | yes |

Setup checks the combination against `GET /models` and refuses one the model does not serve,
naming what it does serve.

| Limit | What the extractor does |
|---|---|
| One call covers at most **366 days** (daily) or **10 local days** (hourly) | Splits longer ranges into consecutive calls |
| `ifs` history covers the last **15 complete local days** only | The API refuses older dates; use `era5` or `seamless` for older history |
| A forecast starts **no earlier than today at the field's location** | Explains the refusal: ahead of UTC (Europe, Asia) "today" can already be tomorrow in UTC |
| A forecast stops at the model's horizon (about 14 days for `ifs`, 5 for `icon_eu`) | Logs a warning when the data ends before the requested end date |
| Days can be missing inside the range, answered as a normal 200 | Logs a warning naming the missing days; the rows returned are kept as they are |
| Soil moisture is empty from **2023-09-11 to 2023-12-07** on `era5` and `seamless`, worldwide: the ERA5 source has none for that period, so it cannot be rebuilt. Every other variable has values | Returns those days as normal rows, with the `soil.moisture...` columns (`swvl1` ... `swvl4`) empty (NaN) |
| Busy server (HTTP 503) | Retries after `Retry-After` |

### Output columns

`entity_id`, `date`, `date_utc` (hourly only), `geohash`, `model`, `aggregation_timezone`, then
the model's weather columns, plus your input columns (except `geometry`).

The weather columns are **normalized**: the same column has the same name and the same unit
whatever the model or dataset. Two independent settings control it.

**Names (`naming`).** By default columns use Weather v1's `parameter.subParameter` names, so code
written for `WeatherExtractor` reads WeatherFlow output unchanged. `naming="api"` keeps the API's
names instead.

| Weather v1 name (default) | API name (daily) | API name (hourly) |
|---|---|---|
| `temperature.standard` / `standardMax` / `standardMin` | `temperature_2m_mean` / `_max` / `_min` | `temperature_2m` |
| `dewPoint.value` | | `dew_point_2m` |
| `humidity.relative` / `relativeMax` / `relativeMin` | `relative_humidity_2m_mean` / `_max` / `_min` | `relative_humidity_2m` |
| `precipitation.cumulative` | `precipitation_sum` | `precipitation` |
| `precipitation.hours` | `precipitation_hours` | |
| `wind.speed.at10M` / `maxAt10M` / `minAt10M` | `wind_speed_10m_mean` / `_max` / `_min` | `wind_speed_10m` |
| `wind.gust.at10M` / `maxAt10M` | `wind_gusts_10m_mean` / `_max` | `wind_gusts_10m` |
| `wind.direction.at10M` | `wind_direction_10m_dominant` | `wind_direction_10m` |
| `solarRadiation.surfaceDownwardShortWave` | `shortwave_radiation_sum` | `shortwave_radiation` |
| `cloudCover.value` / `max` / `min` | `cloud_cover_mean` / `_max` / `_min` | `cloud_cover` |
| `snow.waterEquivalent` | `snowfall_sum` (history), `snowfall_water_equivalent_sum` | `snowfall_water_equivalent` |
| `snow.freshSnow` | `snowfall_sum` (`ifs` forecast) | `snowfall` |
| `snow.depth` | | `snow_depth` |
| `soil.moisture0to7cm` / `7to28cm` / `28to100cm` / `100to289cm` | `swvl1` / `swvl2` / `swvl3` / `swvl4` | |
| `soil.moisture0to1cm` | `soil_moisture_0_to_1cm_mean` | `soil_moisture_0_to_1cm` |

Columns with no Weather v1 equivalent keep their API name (`rain_sum`, `visibility`,
`weather_code`, ...). `precipitation.hours` and the `soil.moisture...` names extend the v1
pattern; the soil depths are the ECMWF layers of `era5`, `ifs` and `seamless`.

**Units (`units`).** Each column's unit as sent by the API is read from `describe_model()`, then
converted to the profile:

| Quantity | `metric` (default) | `imperial` |
|---|---|---|
| Temperature, dew point | °C | °F |
| Precipitation, snow water equivalent | mm | in |
| Fresh snow | cm | in |
| Snow depth | cm | in |
| Wind speed, gusts | km/h | mph |
| Solar radiation | W/m² | W/m² |
| Visibility | m | mi |
| Humidity, cloud cover | % | % |
| Soil moisture | m³/m³ | m³/m³ |

`metric` and `imperial` match the EarthDaily Agriculture account unit profiles **EU** and
**US** for every weather quantity they define, so output agrees with the rest of the
platform.

`units="native"` keeps what the API sends, which differs between models: wind is m/s in history
but km/h in the `ifs` forecast. Two rules hold in every profile:

- **Daily solar radiation is the day's mean irradiance in W/m²**, like Weather v1. The API sends
  the day's total in MJ/m², which is divided by the length of the day (× 11.574).
- **Fresh snow and snow water equivalent are never converted into each other.** They are
  different quantities (snow depth vs water), so they come out as two columns.

Both tables are data in `earthdaily/agriculture/config/weather_normalization.py`
(`WEATHERFLOW_VOCABULARY` for names and kinds, `UNIT_PROFILES` for units): a new API column
is supported by adding it there.

The units of the current output are in `wf.output_units`, in `df.attrs["units"]` on each
formatted frame, and in the export manifest (`export_manifest=True`) with the profile and
naming. A column whose unit the API does not report is left as sent, with a warning.

### Dates and times

**Daily rows:** `date` is the **local calendar day** at the field. Each daily value (maximum
temperature, precipitation total) covers local midnight to midnight, and
`aggregation_timezone` names the zone. Dates from different countries join directly: a date
means the same day everywhere.

**Hourly rows:** `date` is the **local clock time**, and `date_utc` is the same moment in UTC.

| Use | Column |
|---|---|
| KPIs, date windows, anything defined in local days | `date` |
| Several countries on one timeline, joins with other timestamped data, deduplication, sorting | `date_utc` |

`date_utc` matters when daylight saving ends: the local hour repeats, so two real hours share
the same `date` but not the same `date_utc`.

| API value | `date` | `date_utc` |
|---|---|---|
| `2025-10-26T02:00+02:00` (Paris) | 02:00 | 00:00 |
| `2025-10-26T02:00+01:00` (Paris) | 02:00 | 01:00 |

Use `(entity_id, date_utc)` as the key for hourly rows; `(entity_id, date)` would merge two
different hours.

---

## WeatherExtractor (Weather v1)

```python
from earthdaily.agriculture.extractors.weather_functions import WeatherExtractor

weather = WeatherExtractor(manager.bearer_token, manager.token_expiration, config=manager.config)
weather.setup_weather_parameters(
    weather_type="HISTORICAL_DAILY",
    weather_parameters=["Temperature.standardmax", "precipitation.cumulative"],
)
result = weather.process_entity_weather_bulk_parallel(fields)
```

`weather_parameters` defaults to `"precipitation.cumulative"`; pass `"none"` for every
parameter. Despite its name, `precipitation.cumulative` is a **daily** total, not a running sum.

!!! warning "Weather v1 dates are local days labeled as UTC midnight"
    Weather v1 returns `2025-06-01T00:00:00Z`, but the values cover the **local** day
    2025-06-01, not the UTC day (measured in Japan and Australia, where the two differ most).
    Take the calendar date (`df["date"].dt.date`) and never convert it to a local time zone:
    west of UTC that moves it to the previous day.

### Comparing Weather v1 with WeatherFlow

With the defaults (`naming="weather_v1"`, `units="metric"`), WeatherFlow columns carry the same
names and units as Weather v1's metric output, so daily rows from both merge on the calendar
date and compare column by column:

```python
v1_df = v1_df.assign(date=pd.to_datetime(v1_df["date"]).dt.tz_localize(None).dt.normalize())
both = v1_df.merge(wf_df, on="date", suffixes=(" v1", " wf"))
```

The two services use different models, so expect differences: over June–August 2025, daily
minimum temperature differed by about 1 °C on average and daily precipitation correlated at
0.74–0.81. Over June 2025 at one field, daily solar radiation differed by 37 W/m² on average.
