---
title: In-Season Monitoring
description: This section explains everything you need to know about the in-season monitoring analytic.
# icon: fontawesome/question
#status: new
---
<!-- md:swagger API|https://5gciu5p2msxwjrt54fks3kvvxu0oxdyr.lambda-url.us-east-1.on.aws/docs -->

# In-Season Monitoring

## 📖 Overview

The **in-season monitoring analytic** computes vegetation performance indicators after crop emergence by analyzing cumulative NDVI (1) values compared to historical averages. This process tracks daily vegetation development throughout the growing season and compares current performance against the average of the previous 5 years. The analytic calculates cumulative vegetation indices and provides comparative metrics to assess whether crop development is above, below, or on par with historical patterns. This monitoring capability enables real-time crop performance assessment and early identification of potential issues during the growing season.
{ .annotate }

1.  --8<-- "../../glossary.md:ndvi"

---

## 🗂️ Baseline Data

The analytic uses NDVI (1) time series data from satellite imagery captured after crop emergence, combined with historical vegetation patterns from the previous 5 years to accurately monitor current season performance within a defined AOI (2).
{ .annotate }

1.  --8<-- "../../glossary.md:ndvi"
2.  --8<-- "../../glossary.md:aoi"

---

## ⚙️ API

<swagger-ui src="https://5gciu5p2msxwjrt54fks3kvvxu0oxdyr.lambda-url.us-east-1.on.aws/openapi.json"/>

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Season Duration     | season_duration        | Duration of the growing season in days                                                               | integer    |
| Season Start Day    | season_start_day       | Start day of the season (1-31)                                                                       | integer    |
| Season Start Month  | season_start_month     | Start month of the season (1-12)                                                                     | integer    |
| Year                | year                   | Year of the first date of the season. Historical data from the 5 past years will be used             | integer    |
| Data Source         | data_source            | Enum: "LR" (Low Resolution) or "MR" (Medium Resolution)                                             | string     |
| Crop                | crop                   | Enum: "CORN", "SECOND CORN", "SOYBEANS", "SUGARCANE", "COTTON", "OTHERS" (optional)                | string     |

---

### Request Body

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | id                     | EarthDaily Agro internal ID of the area of interest (optional)                                       | string     |
| geometry            | geometry               | Geometry of the area of interest (WKT format)                                                        | string     |

---

### Output Variables

| **Parameter**                                    | **Variable Name**                              | **Description**                                                                                      | **Type**   |
|--------------------------------------------------|------------------------------------------------|------------------------------------------------------------------------------------------------------|------------|
| Season                                           | Season                                         | Season identifier                                                                                    | integer    |
| Request Date                                     | RequestDate                                    | Date of the monitoring request                                                                       | string     |
| Emergence Date                                   | EmergenceDate                                  | Date when crop emergence was detected                                                                | string     |
| Days Since Emergence                             | DaysSinceEmergence                             | Number of days elapsed since crop emergence                                                          | integer    |
| Vegetation Index Value                           | VegetationIndexValue                           | Current NDVI value                                                                                   | float      |
| Cumulative Vegetation Index                      | CumulativeVegetationIndex                      | Sum of daily NDVI values since emergence for the current season                                      | float      |
| Historical Average Cumulative Vegetation Index   | HistoricalAverageCumulativeVegetationIndex     | Average cumulative NDVI from the previous 5 years at the same point in the season                   | float      |
| Cumulative Vegetation Compared To Average        | CumulativeVegetationComparedToAverage          | Comparison metric between current and historical cumulative vegetation indices                       | float      |
| Delta                                            | Delta                                          | Relative difference calculated as (CumulativeVegetationIndex / HistoricalAverageCumulativeVegetationIndex) - 1 | float      |
| ID                                               | id                                             | EarthDaily Agro internal ID of the area of interest                                                  | string     |

---

## ⚠️ Error Management

| Status Code | Error Type | Description | Example Response |
|-------------|------------|-------------|------------------|
| 401 | Not Authenticated | Missing or invalid authentication token | `{"detail": "Not authenticated"}` |
| 422 | Validation Error | Request validation failed | `{"detail": [{"loc": ["string or integer"], "msg": "string", "type": "string"}]}` |
| 500 | Internal Server Error | Error during in-season monitoring calculation | `{"detail": "Error while calculating in-season monitoring"}` |

---

## 📊 Performance and Accuracy


- **Historical Reference Period**: 5 previous years

- **Supported Crops**:
    - Corn
    - Second Corn (2nd Corn)
    - Soybeans
    - Sugarcane
    - Cotton
    - Others (generic monitoring)

- **Key Performance Indicators**:
    - **Delta > 0**: Current season vegetation is performing above historical average
    - **Delta = 0**: Current season vegetation is performing at historical average
    - **Delta < 0**: Current season vegetation is performing below historical average

---

## 💼 Use Case and Product Integration

This analytic is used for:

- **Real-time crop performance monitoring** during the growing season
- **Early detection of vegetation stress** or underperformance
- **Comparative analysis** of current season against historical patterns
- **Decision support** for in-season management interventions

---

## ⚠️ Important Notes

- The analytic requires emergence detection to have occurred before monitoring can begin
- Historical averages are calculated from 5 previous years of data based on the specified year parameter
- When crop parameter is not provided, the analytic computes generic emergence patterns
- Cumulative indices are calculated from the emergence date forward
- The Delta metric provides a normalized comparison: 
  - Delta of 0.10 means 10% above historical average
  - Delta of -0.10 means 10% below historical average

---

--8<-- "snippets/contact-footer.md"