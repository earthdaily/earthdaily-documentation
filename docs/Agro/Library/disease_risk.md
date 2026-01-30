---
title: Disease Risk Assessment
description: This section explains everything you need to know about the disease risk assessment analytic.
# icon: fontawesome/question
#status: new
---
<!-- md:swagger API|https://t7izeqf7q5t4xseagqap5ev7xm0xpmmh.lambda-url.us-east-1.on.aws/v1/docs -->

# Disease Risk Assessment

## 📖 Overview

The **disease risk assessment analytic** calculates daily disease risk forecasts for corn and soybean crops based on weather conditions and validated epidemiological models. This processor leverages research from the University of Wisconsin-Madison Crop Risk Tool, implementing disease models that evaluate environmental conditions favorable to pathogen development. Using weather data, the analytic produces normalized risk scores (0-1 scale) for multiple key crop diseases, enabling proactive disease management and treatment timing decisions. The processor automatically handles geometry conversion, retrieves historical and forecast weather data, and computes moving averages and cumulative metrics required by each disease model.
{ .annotate }

---

## 🗂️ Baseline Data

The analytic uses comprehensive weather data including temperature, humidity, dew point, wind speed, and precipitation EarthDaily weather service. Both historical and forecast weather data are retrieved for a specified date range and processed through validated disease models specific to each pathogen. For computational consistency, polygon geometries are automatically converted to their centroid for weather data sampling within the defined AOI (1).
{ .annotate }

1.  --8<-- "../../glossary.md:aoi"

---

## ⚙️ API

<swagger-ui src="https://t7izeqf7q5t4xseagqap5ev7xm0xpmmh.lambda-url.us-east-1.on.aws/v1/openapi-identity.json"/>

---

## 🦠 Diseases Covered

### Corn Diseases
- **Tar Spot** - *Phyllachora maydis*
- **Gray Leaf Spot** - *Cercospora zeae-maydis*
- **Gibberella Ear Rot** - *Fusarium graminearum*

### Soybean Diseases
- **White Mold (Dryland)** - *Sclerotinia sclerotiorum*
- **White Mold (Irrigated - 15" row spacing)** - *Sclerotinia sclerotiorum*
- **White Mold (Irrigated - 30" row spacing)** - *Sclerotinia sclerotiorum*
- **Frogeye Leaf Spot** - *Cercospora sojina*

All risk values are normalized to a 0–1 scale, where **1 = highest modeled risk**.

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Start Date          | startDate              | Start date for risk calculation, format: YYYY-MM-DD (default: current date)                          | string     |
| End Date            | endDate                | End date for risk calculation, format: YYYY-MM-DD (default: current date)                            | string     |

---

### Request Body

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | id                     | EarthDaily Agro internal SeasonField ID (optional)                                                   | string     |
| geometry            | geometry               | Geometry of the area of interest - WKT format (POINT or POLYGON)                                     | string     |

**Accepted Geometry Types:**
- **POINT**: Used directly for weather data lookup
- **POLYGON**: Automatically converted to centroid for weather sampling
- **SeasonField ID**: External ID from EarthDaily

---

### Output Variables

| **Field**                    | **Variable Name**        | **Description**                                                    | **Type**   | **Crop**    |
|------------------------------|--------------------------|--------------------------------------------------------------------|------------|-------------|
| Date                         | date                     | Forecast date for the risk assessment                              | string     | All         |
| Tar Spot Risk                | tar_spot                 | Daily corn tar spot risk (0-1)                                     | float      | Corn        |
| Gray Leaf Spot Risk          | gray_leaf_spot           | Daily gray leaf spot risk (0-1)                                    | float      | Corn        |
| Gibberella Ear Rot Risk      | gibberella_ear_rot       | Daily Gibberella ear rot risk (0-1)                                | float      | Corn        |
| White Mold Dryland Risk      | white_mold_dry           | Soybean white mold dryland risk (0-1)                              | float      | Soybean     |
| White Mold Irrigated 15" Risk| white_mold_irr_15        | Soybean white mold risk for 15" row spacing under irrigation (0-1) | float      | Soybean     |
| White Mold Irrigated 30" Risk| white_mold_irr_30        | Soybean white mold risk for 30" row spacing under irrigation (0-1) | float      | Soybean     |
| Frogeye Leaf Spot Risk       | frogeye_leaf_spot        | Frogeye leaf spot risk (0-1)                                       | float      | Soybean     |
| ID                           | id                       | EarthDaily Agro internal ID of the area of interest                | string     | All         |
| Geometry                     | geometry                 | Original geometry submitted (WKT format)                           | string     | All         |

---

## 📋 Example Response
```json
{
  "id": "",
  "data": {
    "geometry": "POINT(-104.50231 40.37723)",
    "risks": [
      {
        "date": "2025-12-01",
        "tar_spot": 0,
        "gray_leaf_spot": 0.0003109,
        "gibberella_ear_rot": 1.86e-11,
        "white_mold_dry": 0,
        "white_mold_irr_15": 0.0000009677,
        "white_mold_irr_30": 0.0000000895,
        "frogeye_leaf_spot": 0.05306
      },
      {
        "date": "2025-12-02",
        "tar_spot": 0,
        "gray_leaf_spot": 0.0002839,
        "gibberella_ear_rot": 2.50e-12,
        "white_mold_dry": 0,
        "white_mold_irr_15": 0.000000630,
        "white_mold_irr_30": 0.0000000583,
        "frogeye_leaf_spot": 0.05187
      }
    ]
  }
}
```


## ⚠️ Error Management

| Status Code | Error Type | Description | Example Response |
|-------------|------------|-------------|------------------|
| 401 | Not Authenticated | Missing or invalid authentication token | `{"detail": "Not authenticated"}` |
| 422 | Validation Error | Request validation failed | `{"detail": [{"loc": ["string", 0], "msg": "string", "type": "string"}]}` |
| 500 | Internal Server Error | Error during disease risk calculation | `{"detail": "Error while calculating disease risk"}` |

---

## 🌦️ Weather Data Requirements

The processor automatically retrieves and processes comprehensive weather data:

### Daily Weather Variables
- Temperature (mean, max, min)
- Dew point (min)
- Relative humidity (max, mean)
- Wind speed (max at 10m)
- Precipitation (cumulative)

### Hourly Weather Variables
- Relative humidity (for calculating hours above thresholds)

### Computed Metrics
The processor calculates various moving averages and cumulative metrics required by disease models:

- **Moving Averages**: 14-day, 21-day, and 30-day periods for temperature, humidity, dew point, and wind speed
- **Cumulative Metrics**: Days with temperature >25°C, days with precipitation, hours with RH >80%, hours with RH >90% (nighttime)
- **Shifted Values**: 7-day lagged weather data for temporal disease model inputs

### Extended Date Range
Weather data is retrieved with extended boundaries to enable moving average calculations:
- **Extended start**: startDate - 30 days
- **Extended end**: endDate + 9 days

---

## 📊 Performance and Accuracy

- **Processing Mode**: Synchronous - results returned immediately with POST response

- **Data Source**: EarthDaily Weather API (historical and forecast weather data)

- **Scientific Foundation**: Based on University of Wisconsin-Madison Crop Risk Tool validated disease models

- **Supported Crops**:
    - Corn
    - Soybeans

- **Geometry Handling**: 
    - Point geometries: Used directly
    - Polygon geometries: Automatically converted to centroid
    - Ensures stable performance for large field polygons

---

## 💼 Use Case and Product Integration

This analytic is used in:

- **[Territory Insights](../Territory_insights/Territory_insights_overview.md)

### Key Applications:
- **Proactive disease management** - Early warning for disease-favorable conditions
- **Treatment timing optimization** - Data-driven fungicide application decisions
- **Risk assessment** - Comparative disease pressure across fields and regions
- **Forecasting** - Future disease risk based on weather forecasts

---

## ⚠️ Important Notes

### Geometry Processing
- All polygon geometries are automatically reduced to their centroid for weather data lookup
- This ensures computational consistency with the original Wisconsin-Madison disease models
- Provides stable performance regardless of field polygon size or complexity

### Weather Data Integration
- Both historical observations and forecast data are incorporated

### Risk Score Interpretation
- All risk values are normalized to a **0-1 scale**
- **0** = No modeled disease risk under current conditions
- **1** = Highest modeled disease risk based on optimal pathogen conditions
- Risk scores represent relative disease favorability, not absolute infection probability

### Disease Model Specificity
- Each disease model uses different combinations of weather variables
- Models account for crop-specific factors (e.g., row spacing for white mold)
- Temperature, humidity, and moisture conditions are primary risk drivers
- Some models incorporate lagged weather effects (e.g., 7-day historical conditions)

### Operational Advantages
- **Fully integrated API** - No weather extraction required
- **Scalable architecture** - Bulk processing capability through serverless infrastructure





--8<-- "snippets/contact-footer.md"