---
title: Weather
description: Historical and forecast weather at any location, by weather model (ERA5, IFS, ICON-EU), returned as daily or hourly rows in local time.
keywords:
  - weather data
  - weather forecast
  - historical weather
  - ERA5
  - ECMWF IFS
  - ICON-EU
  - daily and hourly aggregation
# icon: fontawesome/question
#status: new
---

<!-- md:flag swagger API | https://weatherflow.aws.geosys.com/docs -->

#  Weather

## 📖 Overview

This service returns historical and forecast weather at one location, for the weather model you choose. The location is resolved to its ~5 km grid cell, identified by a geohash (1), and the result is one JSON row per local day, or one row per time step with hourly aggregation.
{ .annotate }

1.  --8<-- "../../glossary.md:geohash"

Use it to:

- Retrieve the weather history of a field, back to 1940.
- Get the daily or hourly forecast for the next 5 to 15 days.
- Feed weather variables into crop analytics such as growth stage, disease risk or yield models.

## 🗂️ Baseline data

| **Model** | **Source** | **Coverage** | **Historical** | **Forecast** |
|-----------|------------|--------------|----------------|--------------|
| `era5` | ECMWF reanalysis | Global | From 1940 to about seven days ago — daily, hourly | — |
| `ifs` | ECMWF forecast model | Global | Last 15 complete days, from archived short-range forecasts — daily, hourly | About 15 days ahead — daily, hourly (3 h steps) |
| `icon_eu` | DWD forecast model | Europe only (latitude 29.5 to 70.5, longitude -23.5 to 62.5) | Since 2023-05-24, from archived short-range forecasts — daily | 5 days ahead — hourly |
| `seamless` | `era5`, then `ifs` up to yesterday | Global | From 1940 to yesterday — daily, hourly | — |

Historical weather comes from the ERA5 reanalysis (1) and from archived forecasts of the IFS (2) and ICON-EU (3) models. ERA5 and IFS are produced by ECMWF (4); ICON-EU by DWD (5).
{ .annotate }

1.  --8<-- "../../glossary.md:reanalysis"
2.  --8<-- "../../glossary.md:ifs"
3.  --8<-- "../../glossary.md:icon_eu"
4.  --8<-- "../../glossary.md:ecmwf"
5.  --8<-- "../../glossary.md:dwd"

!!! note "Seamless history"
    Each `seamless` row's `model` field says which model served it. An `ifs` day can change slightly once `era5` covers it.

## ⚙️API

The full API reference is available at [weatherflow.aws.geosys.com/docs](https://weatherflow.aws.geosys.com/docs).

| **Endpoint** | **Description** |
|--------------|-----------------|
| `GET /models` | Lists every model, with the datasets and aggregations it serves. |
| `GET /models/{model}` | Describes one model: for each dataset and aggregation, the time step, the columns of a row with their units, and the time convention. |
| `GET /models/{model}/historical` | Past weather at one location. |
| `GET /models/{model}/forecast` | Forecast at one location, from the latest model run. |

- **Base URL:** `https://weatherflow.aws.geosys.com/prod`
- **Authentication:** API key passed in the `X-API-Key` header on every request.

### Example request

Daily ERA5 history for a field in Ames, Iowa, for the first week of June 2025:

```bash
curl -H "X-API-Key: <your key>" "https://weatherflow.aws.geosys.com/prod/models/era5/historical?latitude=42.03&longitude=-93.63&start=2025-06-01&end=2025-06-07"
```

```python
import requests

r = requests.get(
    "https://weatherflow.aws.geosys.com/prod/models/era5/historical",
    headers={"X-API-Key": "<your key>"},
    params={
        "latitude": 42.03,
        "longitude": -93.63,
        "start": "2025-06-01",
        "end": "2025-06-07",
    },
)
if r.status_code == 204:
    rows = []  # no row in the range, for example era5 days not yet published
else:
    r.raise_for_status()
    rows = r.json()
```

Response (first row):

```json
[
  {
    "date": "2025-06-01",
    "geohash": "9zmrj",
    "aggregation_timezone": "America/Chicago",
    "temperature_2m_mean": 21.3354,
    "temperature_2m_max": 27.9,
    "temperature_2m_min": 14.0,
    "precipitation_sum": 0.0,
    "precipitation_hours": 0.0,
    "snowfall_sum": 0.0,
    "wind_speed_10m_max": 4.3709,
    "wind_gusts_10m_max": 6.4,
    "wind_direction_10m_dominant": 140.0,
    "shortwave_radiation_sum": 29.988,
    "swvl1": 0.2452,
    "swvl2": 0.2691,
    "swvl3": 0.2383,
    "swvl4": 0.3086,
    "model": "era5"
  }
]
```

## ⚙️ Parameters & Variables

### Input Parameters

`/models/{model}/historical` and `/models/{model}/forecast` take the same parameters.

| **Parameter** | **Variable Name** | **Description** | **Type** |
|---------------|-------------------|-----------------|----------|
| model | `model` (path) | Weather model: `era5`, `ifs`, `icon_eu` or `seamless` for historical; `ifs` or `icon_eu` for forecast | string |
| latitude | `latitude` | Latitude of the location, decimal degrees (WGS84), -90 to 90 | number |
| longitude | `longitude` | Longitude of the location, decimal degrees (WGS84), -180 to 180 | number |
| start | `start` | Start date, `YYYY-MM-DD`, local date at the location | date |
| end | `end` | End date, `YYYY-MM-DD`, local date at the location (inclusive) | date |
| aggregation | `aggregation` (optional) | `daily`: one row per local day. `hourly`: one row per time step (3 h for the IFS forecast). Default is `daily` | string |

**Available combinations**

| **Model** | **Dataset** | **Aggregation** | **Time step** |
|-----------|-------------|-----------------|---------------|
| `era5` | historical | daily, hourly | 24 h, 1 h |
| `ifs` | historical | daily, hourly | 24 h, 1 h |
| `ifs` | forecast | daily, hourly | 24 h, 3 h |
| `icon_eu` | historical | daily | 24 h |
| `icon_eu` | forecast | hourly | 1 h |
| `seamless` | historical | daily, hourly | 24 h, 1 h |

**Request limits**

- Historical: `end` is today at the location at the latest. One call covers at most 366 days; hourly `era5` and `seamless` at most 10 local days. Split longer ranges into several calls.
- `ifs` history serves the last 15 complete days only. `icon_eu` history starts on 2023-05-24.
- Forecast: `start` is today at the location at the earliest.
- `era5` days are published with a delay of about seven days. A range that lies entirely in that delay returns `204`. A range that overlaps it returns `200` with only the published days, with no error and no padding: check the last `date` returned. Use `seamless` to fill the gap with `ifs`.

---

### Output Variables

The response body is the list of rows, in time order, with no envelope. Each row carries these columns:

| **Parameter** | **Variable Name** | **Description** | **Type** |
|---------------|-------------------|-----------------|----------|
| Date | `date` | Local date (daily) or local time with UTC offset (hourly), for example `2026-09-18T15:00:00-07:00` | string |
| Geohash | `geohash` | Identifier of the ~5 km grid cell the location resolves to | string |
| Model | `model` | Model that served the row (`era5` or `ifs` for `seamless`) | string |
| Aggregation Timezone | `aggregation_timezone` | Time zone used to define local days, for example `America/Chicago`. Over the sea, a fixed-offset zone with the POSIX sign: `Etc/GMT+1` is UTC-1 | string |

The weather variables depend on the model, dataset and aggregation. In the **Available in** column, *ERA5* stands for `era5` and `seamless` history, *IFS hist.* for `ifs` history, *IFS fcst.* for `ifs` forecast and *ICON-EU* for `icon_eu`.

!!! warning "Units vary by model"
    The `ifs` forecast gives wind speed and gusts in **km/h** and snowfall in **cm of fresh snow**, where the historical datasets give **m/s** and **mm of water equivalent**. Always check the units returned by `GET /models/{model}`.

#### Daily variables

| **Parameter** | **Variable Name** | **Description** | **Unit** | **Available in** |
|---------------|-------------------|-----------------|----------|------------------|
| Mean Temperature | `temperature_2m_mean` | Mean air temperature at 2 m | °C | All |
| Maximum Temperature | `temperature_2m_max` | Maximum air temperature at 2 m | °C | All |
| Minimum Temperature | `temperature_2m_min` | Minimum air temperature at 2 m | °C | All |
| Precipitation | `precipitation_sum` | Total precipitation (rain, showers and snow) | mm | All |
| Precipitation Hours | `precipitation_hours` | Number of hours with precipitation. Always `null` on `ifs` history rows, including the `ifs` rows of `seamless`: IFS 3-hour steps are not comparable to the ERA5 hourly count. In 3-hour steps for the `ifs` forecast | h | All |
| Snowfall | `snowfall_sum` | Total snowfall | mm water equivalent; cm fresh snow (IFS fcst.) | ERA5, IFS hist., IFS fcst. |
| Maximum Wind Speed | `wind_speed_10m_max` | Maximum wind speed at 10 m | m/s; km/h (IFS fcst.) | All |
| Maximum Wind Gusts | `wind_gusts_10m_max` | Maximum wind gusts at 10 m | m/s; km/h (IFS fcst.) | All |
| Dominant Wind Direction | `wind_direction_10m_dominant` | Dominant wind direction at 10 m | degrees (meteorological) | All |
| Solar Radiation | `shortwave_radiation_sum` | Total incoming shortwave solar radiation | MJ/m² | All |
| Soil Water, Layer 1 | `swvl1` | Volumetric soil water, 0–7 cm | m³/m³ | ERA5, IFS hist. |
| Soil Water, Layer 2 | `swvl2` | Volumetric soil water, 7–28 cm | m³/m³ | ERA5, IFS hist. |
| Soil Water, Layer 3 | `swvl3` | Volumetric soil water, 28–100 cm | m³/m³ | ERA5, IFS hist. |
| Soil Water, Layer 4 | `swvl4` | Volumetric soil water, 100–289 cm | m³/m³ | ERA5, IFS hist. |
| Relative Humidity | `relative_humidity_2m_mean`, `_max`, `_min` | Mean, maximum and minimum relative humidity at 2 m | % | IFS fcst., ICON-EU |
| Cloud Cover | `cloud_cover_mean`, `_max`, `_min` | Mean, maximum and minimum total cloud cover | % | IFS fcst., ICON-EU |
| Wind Speed | `wind_speed_10m_mean`, `_min` | Mean and minimum wind speed at 10 m | km/h | IFS fcst. |
| Wind Gusts | `wind_gusts_10m_mean`, `_min` | Mean and minimum wind gusts at 10 m | km/h | IFS fcst. |
| Rain | `rain_sum` | Total large-scale rain | mm | ICON-EU |
| Showers | `showers_sum` | Total convective precipitation | mm | ICON-EU |
| Snowfall | `snowfall_water_equivalent_sum` | Total snowfall | mm water equivalent | ICON-EU |
| Snow Depth | `snow_depth_max` | Maximum snow depth | m | ICON-EU |
| Direct Radiation | `direct_radiation_sum` | Total direct solar radiation | MJ/m² | ICON-EU |
| Diffuse Radiation | `diffuse_radiation_sum` | Total diffuse solar radiation | MJ/m² | ICON-EU |
| Soil Temperature | `soil_temperature_0cm_mean` | Mean soil surface temperature | °C | ICON-EU |
| Soil Moisture | `soil_moisture_0_to_1cm_mean` | Mean volumetric soil moisture, 0–1 cm | m³/m³ | ICON-EU |
| Visibility | `visibility_min` | Minimum visibility | m | ICON-EU |
| Weather Code | `weather_code_max` | Most severe weather condition of the day | WMO code | ICON-EU |

Soil water columns `swvl1` to `swvl4` are expressed as volumetric soil water (1); weather codes follow the WMO weather code table (2).
{ .annotate }

1.  --8<-- "../../glossary.md:volumetric_soil_water"
2.  --8<-- "../../glossary.md:wmo_weather_code"

#### Hourly variables

| **Parameter** | **Variable Name** | **Description** | **Unit** | **Available in** |
|---------------|-------------------|-----------------|----------|------------------|
| Temperature | `temperature_2m` | Air temperature at 2 m | °C | All |
| Dew Point | `dew_point_2m` | Dew point temperature at 2 m | °C | ERA5, IFS hist. |
| Relative Humidity | `relative_humidity_2m` | Relative humidity at 2 m | % | All |
| Precipitation | `precipitation` | Total precipitation over the time step | mm | All |
| Snowfall | `snowfall_water_equivalent` | Snowfall over the time step | mm water equivalent | ERA5, IFS hist., ICON-EU |
| Snowfall | `snowfall` | Snowfall over the time step | cm fresh snow | IFS fcst. |
| Snow Depth | `snow_depth` | Snow depth | m | IFS fcst., ICON-EU |
| Wind Speed | `wind_speed_10m` | Wind speed at 10 m | m/s; km/h (IFS fcst.) | ERA5, IFS hist., IFS fcst. |
| Wind Direction | `wind_direction_10m` | Wind direction at 10 m | degrees (meteorological) | ERA5, IFS hist., IFS fcst. |
| Wind Components | `wind_u_component_10m`, `wind_v_component_10m` | Eastward and northward wind components at 10 m | m/s | ICON-EU |
| Wind Gusts | `wind_gusts_10m` | Wind gusts at 10 m | m/s; km/h (IFS fcst.) | All |
| Solar Radiation | `shortwave_radiation` | Incoming shortwave solar radiation | W/m² | ERA5, IFS hist., IFS fcst. |
| Direct Radiation | `direct_radiation` | Direct solar radiation | W/m² | ICON-EU |
| Diffuse Radiation | `diffuse_radiation` | Diffuse solar radiation | W/m² | ICON-EU |
| Cloud Cover | `cloud_cover` | Total cloud cover | % | IFS fcst., ICON-EU |
| Cloud Cover by Level | `cloud_cover_low`, `_mid`, `_high` | Low, mid and high cloud cover | % | IFS fcst. |
| Rain | `rain` | Large-scale rain over the time step | mm | ICON-EU |
| Showers | `showers` | Convective precipitation over the time step | mm | ICON-EU |
| Soil Temperature | `soil_temperature_0cm` | Soil surface temperature | °C | ICON-EU |
| Soil Moisture | `soil_moisture_0_to_1cm` | Volumetric soil moisture, 0–1 cm | m³/m³ | ICON-EU |
| Visibility | `visibility` | Visibility | m | ICON-EU |
| Weather Code | `weather_code` | Weather condition | WMO code | ICON-EU |

---

### Time convention

- **Days are local** at the location: `start` and `end` are local dates, and `aggregation_timezone` names the zone.
- **Hourly rows are local time with an offset** (`2026-09-18T15:00:00-07:00`). Sort on the instant, not the string: the offset changes on daylight-saving nights, when a day has 23 or 25 hours.
- The 3-hourly grid of `ifs` is anchored on UTC, so the first step of a local day is rarely 00:00 local (00:30 in Tehran, 02:00 in Phoenix).
- Days are served only once they are **complete**.

### Errors

| **Status** | **Meaning** |
|------------|-------------|
| `200` | Rows returned. |
| `204` | No row in the requested range, for example `era5` days not yet published. The response has no body: check the status before parsing JSON. |
| `400` | The request is valid but outside what the model serves: range too long, location or dates not covered, dates in the future or the past. Also returned for a valid aggregation the model does not serve, for example `icon_eu does not serve historical/hourly`. The `detail` field says what to change, for example `start must be <= end`. |
| `401` | API key missing or invalid. |
| `422` | Malformed request: out-of-range value, unknown model or aggregation value, or a forecast asked from a history-only model. |
| `500` | Internal error while reading the data. Contact support if it persists. |
| `503` | The archive cannot be read for a moment. Retry after the number of seconds given in the `Retry-After` header. |
| `504` | The request timed out (29 s). Can happen on the first long request at a new location; retry. |

## 📊 Performance and Accuracy

- **Spatial resolution**: location resolved to a ~5 km cell; native model grids: ERA5 and IFS 0.25° (~28 km), ICON-EU ~7 km
- **Coverage**: Global (`era5`, `ifs`, `seamless`); Europe only (`icon_eu`)
- **Average Generation Time**: typically 1 to 2 s for a short range; up to about 20 s on the first request for a full year at a new location

## 💼 Use Case and Product Integration

This service is used in:

- [Portfolio Management](../portfolio/index.md)
- [Territory Insights](../territory_insights/index.md)
- [EarthDaily App](../app/en-us/03.%20Monitoring%20-%20Field.md), for field-level weather

## 📚 Glossary

Weather terms used on this page, such as ERA5, IFS, ICON-EU, reanalysis and geohash, are defined in the [Glossary](../../glossary.md). Hover over an acronym to see its definition.

--8<-- "snippets/contact-footer.md"
