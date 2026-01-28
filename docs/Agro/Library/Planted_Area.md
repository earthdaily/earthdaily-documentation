---
title: Planted Area
description: This section explains everything you need to know about the planted area analytic.
# icon: fontawesome/question
#status: new
---
<!-- md:swagger API|https://planted-area.aws.geosys.com/docs -->

# Planted Area Computation

## 📖 Overview

The **planted area computation analytic** calculates the planted area of a crop field based on satellite imagery and emergence detection data. This process uses the Emergence Date (1) as a reference and compares images taken before and after emergence to estimate the percentage of planted area. It supports different processing modes through the Processor Mode (2) parameter, including standard planted area calculation and control mode for unplanted area detection. The algorithm validates results using predefined thresholds and stores them for integration with other analytics and applications.
{ .annotate }

1.  --8<-- "../../glossary.md:emergence_date"
2.  --8<-- "../../glossary.md:processor_mode"

---

## 🗂️ Baseline Data

The analytic uses satellite imagery captured before and after crop emergence, combined with emergence detection results to accurately calculate planted area within a defined AOI (1).
{ .annotate }

1.  --8<-- "../../glossary.md:aoi"

---

## ⚙️ API

<swagger-ui src="https://planted-area.aws.geosys.com/openapi.json"/>

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Emergence Date      | emergenceDate          | Emergence date, format: YYYY-MM-DD                                                                   | string     |
| Threshold           | threshold              | Number of days between the images taken before emergence and the second image                        | integer    |
| Processor Mode      | processorMode          | Enum: "PLANTED_AREA" or "CONTROL"                                                                    | string     |
| Control Threshold   | controlThreshold       | Percentage of unplanted area threshold, for CONTROL mode                                             | number     |

---

### Request Body

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | id                     | EarthDaily Agro internal ID of the area of interest (optional)                                       | string     |
| geometry            | geometry               | Geometry of the area of interest (WKT format)                                                        | string     |

---

### Output Variables

#### PLANTED_AREA Mode

| **Parameter**             | **Variable Name**       | **Description**                                               | **Type**   |
|---------------------------|--------------------------|---------------------------------------------------------------|------------|
| Planted Area             | planted_area            | Computed planted area in square meters                       | float      |
| Planted Area Percentage  | planted_percentage      | Computed planted area as a percentage                        | float      |

#### CONTROL Mode

| **Parameter**       | **Variable Name**     | **Description**                                                                                  | **Type**   |
|---------------------|------------------------|--------------------------------------------------------------------------------------------------|------------|
| Difference          | difference            | Represents the numerical difference between the expected planted area and the actual computed planted area. | float      |
| Control Threshold   | control_threshold     | Defines the percentage limit of unplanted area allowed when operating in CONTROL mode.          | float      |
| Result              | result                | Indicates whether the computed value meets or exceeds the defined threshold (true/false).       | boolean    |


## ⚠️ Error management

| Status Code | Error Type | Description | Example Response |
|-------------|------------|-------------|------------------|
| 400 | Bad Request | Invalid request parameters | `{"detail": "Parameters 'season_field_id' and 'polygon' cannot be both None or empty."}` |
| 401 | Not Authenticated | Missing or invalid authentication token | `{"detail": "Not authenticated"}` |
| 422 | Validation Error | Request validation failed | `{"detail": [{"loc": ["string or integer"], "msg": "string", "type": "string"}]}` |
| 500 | Internal Server Error | Error during planted area calculation | `{"detail": "Error while calculating planted area"}` |



## 📊 Performance and Accuracy

- **Tested Crops**:
    - Soybeans
    - Corn

- **Tested Regions**:
    - Brazil
    - United States

---

## 💼 Use Case and Product Integration

This analytic is used in:

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/)

---

--8<-- "snippets/contact-footer.md"