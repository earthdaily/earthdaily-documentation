---
title: ZARC (Agricultural Zoning of Climate Risk)
description: This section explains everything you need to know about the ZARC analytic.
# icon: fontawesome/question
#status: new
---

# ZARC (Agricultural Zoning of Climate Risk)

## 📖 Overview

The **Agricultural Zoning of Climate Risk (ZARC)** is a policy tool that guides crop planting based on analyses of climate, soil, and crop cycles. Its goal is to reduce climate-related risks by identifying the best planting windows for each municipality. Easy to apply, it is widely used by farmers, financial agents, and policymakers.


**EarthDailyAgro’s ZARC analytic** evaluates whether crop planting occurred within the climate risk windows defined by Brazil’s Ministry of Agriculture. Leveraging satellite-based time series data, the analytic detects the crop’s emergence date in the field and compares it against the official risk zones established for the crop, location, and planting period.

---

## 🗂️ Baseline Data

- **NDVI LR Time Series**

---

## ⚙️ API Access

<swagger-ui src="https://zvjihjkwfwohudwcnbhjbpsudq0jhszp.lambda-url.us-east-1.on.aws/docs/openapi.json"/>

---

## ⚙️ Parameters & Variables

###  General Parameters

| **Parameter**         | **Variable Name**       | **Description**                                                                                  | **Type**     |
|-----------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **ID**                | `id`                     | EarthDaily Agro internal ID                                                                      | `string`     |
| **Geometry**          | `geometry`               | Geometry of the Area of Interest (WKT format)                                                    | `string`     |
| **Crop**              | `crop`                   | Crop Code of the field used for the ZARC period computation                                      | `string`  |

###  Input Variables

| **Parameter**         | **Variable Name**       | **Description**                                                                                  | **Type**     |
|-----------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Starting date**     | `date_emergence`         | Starting date for emergence detection                                                            | `string`     |
| **Season Start Day**  | `nb_days_sowing_emergence` | Number of days to consider to compute the sowing date based on the detected emergence          | `int`        |
| **Soils Type**        | `soil_type`       | Soil type of the field, used for zarc period computation                                                | `string`     |
| **Cycle**             | `cycle`  | Variety type of the field, used for zarc period computation                                              | `string`     |


---

###  Output Variables

| **Output**                    | **Variable Name**             | **Description**                                                                                  | **Type**     |
|------------------------------|-------------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Emergence date**           | `emergence_date`    | Emergence date detected                                                                                    | `datetime`   |
| **Id**                       | `id`                | EarthDaily Agro internal id                                                                                | `string`     |
| **Sowing Date**              | `sowing_date`       | Sowing date detected                                                                                       | `datetime`   |
| **ZARC Start Date**          | `zarc_start_date`   | ZARC start period                                                                                          | `datetime`   |
| **ZARC End Date**            | `zarc_end_date`     | ZARC end period                                                                                            | `datetime`   |
| **ZARC Risk Level**          | `zarc_risk_level`   | ZARC period risk level                                                                                     | `double`     |
| **Status**                   | `status`            | Indicates if the detected sowing date is inside or outside the legal period                                | `boolean` |


---

## 📊 Performance and Accuracy

- **Tested Crops**:
    - Corn
    - 2nd Corn
    - Soybeans
    - Cotton
    - Drybeans
    - 2nd drybeans
    - Wheat

- **Tested Regions**: Brazil  
- **Average Generation Time**: < 1 second

---


## 📜 ZARC Logic and Business Rules

### Cycle


| Code | Cycle  |
|------|--------|
| 1    | Short  |
| 2    | Medium |
| 3    | Long   |



### Soil type specification

| **Soil Code** | **Soil Type**     | **Crop**                                                   |
|---------------|-------------------|-------------------------------------------------------------|
| 1             | ARENOSO           | CORN, 2ND_CORN, COTTON; 2ND_DRY_BEANS; DRY_BEANS           |
| 2             | ARGILOSO          | CORN, 2ND_CORN, COTTON; 2ND_DRY_BEANS; DRY_BEANS           |
| 3             | TEXTURA MÉDIA     | CORN, 2ND_CORN, COTTON; 2ND_DRY_BEANS; DRY_BEANS           |
| 11            | AD1               | SOYBEANS; WHEAT                                            |
| 12            | AD2               | SOYBEANS; WHEAT                                            |
| 13            | AD3               | SOYBEANS; WHEAT                                            |
| 14            | AD4               | SOYBEANS; WHEAT                                            |
| 15            | AD5               | SOYBEANS; WHEAT                                            |
| 16            | AD6               | SOYBEANS; WHEAT                                            |


### Business Logic Based on Query Parameters

The behavior of the **ZARC analytic** depends on the presence or absence of the `soil_type` and `cycle` query parameters:

#### Case 1: `soil_type` not provided
- The analytic retrieves ZARC data at the **municipality level**, filtered by **crop** and **cycle**.
- It returns the **earliest start date** and **latest end date** available for the selected crop-cycle combination.

#### Case 2: `cycle` not provided
- The analytic retrieves **summarized ZARC data** at the **municipality level**, filtered by **crop** and **soil_type**.

#### Case 3: Neither `soil_type` nor `cycle` provided
- The analytic retrieves **summarized ZARC data** at the **municipality level**, filtered only by **crop**.

---

### Risk Level Handling

- The `zarc_risk_level` output is only returned when both `soil_type` and `cycle` are specified.
- If either parameter is missing, the risk level is not included in the response.
- This ensures consistency, as risk levels are only meaningful when both soil and cycle are defined.


---

## 💼 Use Case and Product Integration

This analytic is used in:

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/)

---

## 📚 Glossary

| **Term**                     | **Description** |
|------------------------------|-----------------|
| **ZARC (Agricultural Zoning of Climate Risk)** | A strategic tool developed by Brazil’s Ministry of Agriculture to define safe planting windows for crops, based on regional climate risk, soil type, and crop cycle. |
| **NDVI (Normalized Difference Vegetation Index)** | An index derived from satellite imagery that measures vegetation health. Values range from -1 to 1, with higher values indicating healthier vegetation. |
| **Emergence Date**           | The date when the crop is first detected as emerging in the field, based on NDVI time series. |
| **Sowing Date**              | The estimated planting date, calculated by subtracting a fixed number of days from the emergence date. |
| **ZARC Start/End Date**      | The official start and end dates of the planting window defined by ZARC for a given crop, soil type, and cycle. |
| **ZARC Risk Level**          | The level of climate risk associated with the planting window. Only returned when both soil type and cycle are specified. |
| **Status**                   | Indicates whether the detected sowing date falls within the legal ZARC planting window (`true`) or not (`false`). |
| **Soil Type**                | Classification of soil used in ZARC to determine planting windows. Examples include ARENOSO, ARGILOSO, TEXTURA MÉDIA, and AD1–AD6. |
| **Cycle**                    | Refers to the crop variety duration: Short, Medium, or Long. |
| **Municipality Level**       | The administrative level at which ZARC data is aggregated when soil type and/or cycle are not specified. |
| **WKT (Well-Known Text)**    | A text markup language for representing vector geometry objects such as points, lines, and polygons. |
| **AOI (Area of Interest)**   | The geographic area selected for analysis. |


---
--8<-- "snippets/contact-footer.md"