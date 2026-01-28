---
title: Harvest Detection
description: This section explains everything you need to know about the Harvest Detection analytic.
# icon: fontawesome/question
#status: new
---
<!-- md:swagger API|https://harvest-detection.aws.geosys.com/docs -->

# Harvest Detection Computation

## 📖 Overview

The **harvest detection analytic** (1) determines the harvest date or readiness of a crop field by analyzing time series of vegetation indices and other relevant data. It supports multiple detection modes through the Harvest Type (2) parameter:
{ .annotate }

1.  --8<-- "../../glossary.md:harvest_detection"
2.  --8<-- "../../glossary.md:harvest_type"

- **INSEASON_HARVEST**: Detects if the harvest has occurred and computes the harvest date for the current season.
- **HISTORICAL_HARVEST**: Computes harvest dates for the past 5 years.
- **HARVEST_READINESS**: Provides the first date when the crop reaches maturity level and is ready for harvest.

This process uses crop-specific parameters and seasonal information to deliver accurate and timely results for operational and historical analysis.

---

## 🗂️ Baseline Data

The analytic uses NDVI (1) time series data available at both LR (2) and MR (3) resolutions, combined with crop season parameters to detect harvest dates and readiness.
{ .annotate }

1.  --8<-- "../../glossary.md:ndvi"
2.  --8<-- "../../glossary.md:lr"
3.  --8<-- "../../glossary.md:mr"

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

- [Portfolio Management](../Portfolio/portfolio_product_site_draft/)

---

--8<-- "snippets/contact-footer.md"