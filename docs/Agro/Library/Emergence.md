---
title: Emergence
description: This section explains everything you need to know about emergence detection.
# status: new
---

# Emergence Detection

## 📖 Overview

The **emergence detection analytic** identifies the beginning of the crop development by analyzing time series of the vegetation index NDVI (1). Using this data, it calculates both the growth rate and the acceleration of the NDVI curve. Emergence is detected when the NDVI exceeds a defined minimum threshold and demonstrates consistent, accelerating growth over a continuous period. The algorithm validates this behavior using predefined criteria and records the corresponding date as Emergence Date (2). It also reports whether emergence was detected (`EmergenceStatus`) and which detection method was applied (`ConfirmationStatus`). The process is fast, robust, and adaptable to various crops and geographic regions.
{ .annotate }

1.  --8<-- "../../glossary.md:ndvi"
2.  --8<-- "../../glossary.md:emergence_date"

---

## 🗂️ Baseline Data

The analytic uses NDVI (1) time series data available at both LR (2) and MR (3) resolutions to detect crop emergence dates across various agricultural regions.
{ .annotate }

1.  --8<-- "../../glossary.md:ndvi"
2.  --8<-- "../../glossary.md:lr"
3.  --8<-- "../../glossary.md:mr"

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

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/)

---

--8<-- "snippets/contact-footer.md"