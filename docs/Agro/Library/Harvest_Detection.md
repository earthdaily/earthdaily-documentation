
# Harvest Detection Computation

## 📖 Overview

The **harvest detection analytic** determines the harvest date or readiness of a crop field by analyzing time series of vegetation indices and other relevant data. It supports multiple detection modes:

- **INSEASON_HARVEST**: Detects if the harvest has occurred and computes the harvest date for the current season.
- **HISTORICAL_HARVEST**: Computes harvest dates for the past 5 years.
- **HARVEST_READINESS**: Provides the first date when the crop reaches maturity level and is ready for harvest.

This process uses crop-specific parameters and seasonal information to deliver accurate and timely results for operational and historical analysis.

---

## 🗂️ Baseline Data

- **NDVI Time Series**
- **Crop Season Parameters**
- **Satellite Imagery (LR/MR)**

---

## ⚙️ API

<swagger-ui src="https://harvest-detection.aws.geosys.com/openapi.json"/>

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Harvest Type        | harvestType            | Enum: "INSEASON_HARVEST", "HISTORICAL_HARVEST", "HARVEST_READINESS"                                  | string     |
| Crop                | crop                   | Enum: "CORN", "SECOND CORN", "SUGARCANE", "SOYBEANS", "OTHERS"                                      | string     |
| Season Duration     | seasonDuration         | Duration of the season, in days                                                                       | integer    |
| Season Start Day    | seasonStartDay         | Starting day of the season (1–31)                                                                     | integer    |
| Season Start Month  | seasonStartMonth       | Starting month of the season (1–12)                                                                   | integer    |
| Year                | year                   | Year of the first date of the season                                                                  | integer    |
| Data Source         | dataSource             | Image resolution: LR (Low Resolution) or MR (Medium Resolution); default is LR                        | string     |

---

### Request Body

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | id                     | EarthDaily Agro internal ID of the area of interest (optional)                                       | string     |
| geometry            | geometry               | Geometry of the area of interest (WKT format)                                                        | string     |

---

### Output Variables

#### In-season Harvest

| **Parameter**       | **Variable Name**     | **Description**                                               | **Type**   |
|---------------------|------------------------|---------------------------------------------------------------|------------|
| Harvest Date        | harvestDate            | Detected harvest date (can be null if not detected)           | datetime   |
| Harvest Status      | harvestStatus          | Indicates whether harvest was detected                        | boolean    |

#### Historical Harvest

| **Parameter**       | **Variable Name**     | **Description**                                               | **Type**   |
|---------------------|------------------------|---------------------------------------------------------------|------------|
| Harvest Year - 1    | harvest_year_1         | Detected harvest date (can be null if not detected)           | datetime   |
| Harvest Year - 2    | harvest_year_2         | Detected harvest date (can be null if not detected)           | datetime   |
| Harvest Year - 3    | harvest_year_3         | Detected harvest date (can be null if not detected)           | datetime   |
| Harvest Year - 4    | harvest_year_4         | Detected harvest date (can be null if not detected)           | datetime   |
| Harvest Year - 5    | harvest_year_5         | Detected harvest date (can be null if not detected)           | datetime   |
| Historical Harvest Average | harvestAverageDate | Indicates the average harvest date (DD-MM)                    | datetime   |

#### Harvest Readiness

| **Parameter**       | **Variable Name**     | **Description**                                               | **Type**   |
|---------------------|------------------------|---------------------------------------------------------------|------------|
| Readiness Harvest Date | readinessDate       | Detected harvest readiness date                                | datetime   |

---

## 📊 Performance and Accuracy

- **Tested Crops**:
    - Corn
    - Soybeans
    - Sugarcane

- **Tested Regions**:
    - Brazil
    - United States

---

## 💼 Use Case and Product Integration

This analytic is used in:

- /earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/* 

---

## 📚 Glossary

| **Term**                             | **Description**                                                                                                   |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **Harvest Detection**               | The process of identifying the harvest date or readiness based on vegetation index and crop maturity.             |
| **Harvest Type**                    | Defines the detection mode: **INSEASON_HARVEST**, **HISTORICAL_HARVEST**, or **HARVEST_READINESS**.              |
| **NDVI (Normalized Difference Vegetation Index)** | A vegetation index derived from visible and near-infrared reflectance. Values range from -1 to 1.                |
| **WKT (Well-Known Text)**           | A standard text format for representing spatial geometries such as points, lines, and polygons.                   |
| **AOI (Area of Interest)**          | A user-defined geographic area selected for analysis.                                                             |

---
