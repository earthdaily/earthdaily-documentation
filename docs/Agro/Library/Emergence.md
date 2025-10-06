---
title: Emergence
description: This section explains everything you need to know about emergence detection.
status: new
---

# Emergence Detection

## 📖 Overview

The **emergence detection analytic** identifies the begining of the crop development by analyzing time series of the vegetation index (NDVI). Using this data, it calculates both the growth rate and the acceleration of the NDVI curve. Emergence is detected when the NDVI exceeds a defined minimum threshold and demonstrates consistent, accelerating growth over a continuous period. The algorithm validates this behavior using predefined criteria and records the corresponding date as `EmergenceDate`. It also reports whether emergence was detected (`EmergenceStatus`) and which detection method was applied (`ConfirmationStatus`). The process is fast, robust, and adaptable to various crops and geographic regions.


---

## 🗂️ Baseline Data

- **NDVI MR/LR Time Series**

---

## ⚙️ API

<swagger-ui src="https://emergence-detection.aws.geosys.com/openapi.json"/>

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | id (optional)          | EDA internal ID of the area of interest                                                            | string     |
| geometry            | geometry               | Geometry of the area of interest (WKT format)                                                         | string     |
| crop                | crop (optional)        | Crop code of the area of interest (must match available crop list)                                   | string     |
| seasonDuration      | seasonDuration         | Duration of the season, in days                                                                       | integer    |
| seasonStartDay      | seasonStartDay         | Start day of the season (1–31)                                                                        | integer    |
| seasonStartMonth    | seasonStartMonth       | Start month of the season (1–12)                                                                      | integer    |
| dataSource          | dataSource (optional)  | Data resolution: LR (Low Resolution) or MR (Medium Resolution); default is LR                         | string     |

---

### Output Variables

| **Parameter**       | **Variable Name**     | **Description**                                               | **Type**   |
|---------------------|------------------------|---------------------------------------------------------------|------------|
| EmergenceDate       | EmergenceDate          | Detected emergence date (can be null if not detected)         | datetime   |
| EmergenceStatus     | EmergenceStatus        | Indicates whether emergence was detected                      | boolean    |
| ConfirmationStatus  | ConfirmationStatus     | Indicates which algorithm was used for detection              | string     |

---

## 📊 Performance and Accuracy

- **Tested Crops**:
    - Soybeans
    - Corn
    - Wheat
    - Malting Barley

- **Tested Regions**:
    - Brazil  
    - United States
    - Ireland
    - Russia
    - France

- **Average Generation Time**: < 1 second per field

---

## 💼 Use Case and Product Integration

This analytic is used in:

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/* )


## 📚 Glossary

| **Term**                             | **Description**                                                                                                                                       |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **NDVI (Normalized Difference Vegetation Index)** | A vegetation index derived from visible and near-infrared reflectance. Values range from -1 to 1, with higher values indicating healthier vegetation. |
| **MR / LR**                          | Image resolutions used in analysis: **MR** (Medium Resolution) and **LR** (Low Resolution).                                                           |
| **Season Duration**                  | Total number of days in the crop season, used to calculate cumulative NDVI.                                                                           |
| **Season Start Day / Month**         | Day and month marking the beginning of the crop season, used to define the NDVI accumulation period.                                                  |
| **WKT (Well-Known Text)**            | A standard text format for representing spatial geometries such as points, lines, and polygons.                                                       |
| **AOI (Area of Interest)**           | A user-defined geographic area selected for analysis.                                                                                                 |


---

