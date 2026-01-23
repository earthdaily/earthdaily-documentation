---
title: In-season Potential Score
description: This section explains everything you need to know about the In-season Potential Score analytic.
# icon: fontawesome/question
#status: new
---
<!-- md:demo reflectance-datacube-processor -->
# In-season Potential Score

## 📖 Overview

The **In-season Potential Score**  analytic provides an indicator of the in-season potential score  in comparison to the past years, based on cumulative NDVI (Normalized Difference Vegetation Index). It serves as a benchmark to compare field performance across different areas within a region or across previous years.

The figure below illustrates the expected NDVI development for a typical annual grain crop. The analytic transforms the NDVI time series into a potential score, enabling comparisons between fields in the same region or across historical seasons.



![In-season Potential Score](../../assets/agro/potential_score/ndvi_plot.png)


---

## 🗂️ Baseline Data

- **NDVI MR/LR Time Series**

---

## ⚙️ API Access

<swagger-ui src="https://inseason-potential-score.aws.geosys.com/docs/openapi.json"/>

---

## ⚙️ Parameters & Variables

### General Parameters

| **Parameter**         | **Variable Name**       | **Description**                                                                                  | **Type**     |
|-----------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **ID**                | `id`                     | EarthDaily Agro internal ID                                                                      | `string`     |
| **Geometry**          | `geometry`               | Geometry of the Area of Interest (WKT format)                                                    | `string`     |
| **Historical Seasons** _(Optional)_ | `historicalSeasons` | List of years to compute historical potential and risk scores (e.g., `[2022, 2021, 2019]`)       | `List[int]`  |

### Input Parameters

| **Parameter**         | **Variable Name**       | **Description**                                                                                  | **Type**     |
|-----------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Season Duration**   | `seasonDuration`         | Duration of the season in days                                                                   | `int`        |
| **Season Start Day**  | `seasonStartDay`         | Start day of the season (1–31)                                                                   | `int`        |
| **Season Start Month**| `seasonStartMonth`       | Start month of the season (1–12)                                                                 | `int`        |
| **Number of Historical Years**| `numberHistoricalYears`  | Number of years used for the comparison to historical data                                | `float`      |
| **Threshold**         | `threshold`              | NDVI threshold (e.g., `0.7`)                                                                     | `float`      |
| **End Date** _(Optional)_ | `end_date`           | Date until when the score is computed. If None, end_date will be today.                          | `datetime` |
| **Data Source** _(Optional)_ | `dataSource`     | Data resolution: `LR` or `MR`. Defaults to `LR`                                                  | `string`     |
| **Crop** _(Optional)_ | `crop`                  | Crop code                                                                                        | `string`     |

---

## Output

| **Output**                    | **Variable Name**             | **Description**                                                                                  | **Type**     |
|------------------------------|-------------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Historical Potential Score**| `historical_potential_score`  | Mean potential score over the last five years                                                    | `double`     |
| **In-season Potential Score** | `inseason_potential_score`    | In-season potential score                                                                         | `double`     |
| **Relative Potential Score**  | `relative_potential_score`    | Percentage of potential compared to historical data                                              | `double`     |
| **ID**                        | `id`                          | EarthDaily Agro internal ID                                                                      | `string`     |

---

## 📊 Performance and Accuracy

- **Tested Crops**: Corn and Soybeans  
- **Tested Regions**: Brazil  
- **Average Generation Time**: < 1 second

---

## 📜Rules for Defining Historical Periods


---

## Use Cases

This analytic is used in:

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/)

---

## Glossary

| **Term**                        | **Description** |
|----------------------------------|-----------------|
| **NDVI (Normalized Difference Vegetation Index)** | Index that measures vegetation health based on visible and near-infrared light reflectance. Values range from -1 to 1, with higher values indicating denser, healthier vegetation. |
| **MR / LR**                      | Image resolutions: **MR** (Medium Resolution) and **LR** (Low Resolution). Define the spatial detail level of the NDVI data used. |
| **Season Duration**              | Duration of the crop season, in days, used to calculate cumulative NDVI. |
| **Season Start Day / Month**     | Day and month marking the beginning of the crop season. Define the starting point for NDVI accumulation. |
| **Threshold**                    | NDVI value used as a cutoff to determine relevant vegetative activity. |
| **End Date**                     | Date until which the in-season NDVI is accumulated. |
| **Potential Score**              | Indicator of the productive potential of an area based on cumulative NDVI during the season. |
| **Historical Potential Score**   | Mean of potential scores from previous seasons. |
| **In-season Potential Score**    | Cumulative NDVI-based score for the current season up to the specified end date. |
| **Relative Potential Score**     | Ratio (in %) of in-season score to historical potential score. |
| **WKT (Well-Known Text)**        | Standard format for representing spatial geometries such as polygons, points, and lines. |
| **AOI (Area of Interest)**       | User-defined area for analysis. |

---
--8<-- "snippets/contact-footer.md"