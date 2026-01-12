---
title: Emergence
description: This section wil explain all you need to know on emergence detection. 
# icon: fontawesome/question
#status: new
---

#  Emergence Delay

## 📖 Overview

This analytic compares the current season emergence to the average historical emergence at the field level. The result is the number of days of difference.

## Baseline data

- **NDVI MR/LR Time Series**
## API 

<swagger-ui src="https://emergence-detection.aws.geosys.com/openapi.json"/>


### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | `id`(optional)          | Earthdaily Agro internal ID of the area of interest                                                            | string     |
| geometry            | `geometry`               | Geometry of the area of interest (WKT format)                                                         | string     |
| crop                | `crop` (optional)        | Crop code of the area of interest (must match available crop list)                                   | string     |
| seasonDuration      | `seasonDuration`         | Duration of the season, in days                                                                       | integer    |
| seasonStartDay      | `seasonStartDay`        | Start day of the season (1–31)                                                                        | integer    |
| seasonStartMonth    | `seasonStartMonth`       | Start month of the season (1–12)                                                                      | integer    |
| year                | `year` (optional)        | Year of the first date of the season (used to retrieve past 5 years of data)                          | integer    |
| dataSource          | `dataSource` (optional)  | Data resolution: LR (Low Resolution) or MR (Medium Resolution); default is LR                         | string     |

---

### Output Variables

| **Parameter**       | **Variable Name**     | **Description**                                               | **Type**   |
|---------------------|------------------------|---------------------------------------------------------------|------------|
| Emergence Date       | `EmergenceDate`          | Detected emergence date (can be null if not detected)         | datetime   |
| Average Emergence Date | `AverageEmergenceDate` | Average emergence date of the past five seasons     | datetime    |
| Emergence Delay  | `EmergenceDelay`     | Days differences between the current emergence date and the average emergence date              | string     |

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

## 💼 Use Case and Product Integration

This analytic is used in:
    - [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/)
    - 

## 📚 Glossary

| **Term**                             | **Description**                                                                                                                                       |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| **NDVI (Normalized Difference Vegetation Index)** | A vegetation index derived from visible and near-infrared reflectance. Values range from -1 to 1, with higher values indicating healthier vegetation. |
| **MR / LR**                          | Image resolutions used in analysis: **MR** (Medium Resolution) and **LR** (Low Resolution).                                                           |
| **Season Duration**                  | Total number of days in the crop season, used to calculate cumulative NDVI.                                                                           |
| **Season Start Day / Month**         | Day and month marking the beginning of the crop season, used to define the NDVI accumulation period.                                                  |
| **WKT (Well-Known Text)**            | A standard text format for representing spatial geometries such as points, lines, and polygons.                                                       |
| **AOI (Area of Interest)**           | A user-defined geographic area selected for analysis.                                                                                        




--8<-- "snippets/contact-footer.md"