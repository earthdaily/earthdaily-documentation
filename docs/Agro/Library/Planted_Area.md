
# Planted Area Computation

## 📖 Overview

The **planted area computation analytic** calculates the planted area of a crop field based on satellite imagery and emergence detection data. This process uses the emergence date as a reference and compares images taken before and after emergence to estimate the percentage of planted area. It supports different processing modes, including standard planted area calculation and control mode for unplanted area detection. The algorithm validates results using predefined thresholds and stores them for integration with other analytics and applications.

---

## 🗂️ Baseline Data

- **Satellite Imagery (Pre- and Post-Emergence)**
- **Emergence Detection Results**

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

#### PLANTED_AREA

| **Parameter**             | **Variable Name**       | **Description**                                               | **Type**   |
|---------------------------|--------------------------|---------------------------------------------------------------|------------|
| Planted Area             | planted_area            | Computed planted area in square meters                       | float      |
| Planted Area Percentage  | planted_percentage      | Computed planted area as a percentage                        | float      |

#### CONTROL

| **Parameter**       | **Variable Name**     | **Description**                                                                                  | **Type**   |
|---------------------|------------------------|--------------------------------------------------------------------------------------------------|------------|
| Difference          | difference            | Represents the numerical difference between the expected planted area and the actual computed planted area. | float      |
| Control Threshold   | control_threshold     | Defines the percentage limit of unplanted area allowed when operating in CONTROL mode.          | float      |
| Result              | result                | Indicates whether the computed value meets or exceeds the defined threshold (true/false).       | boolean    |

---

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

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/* )

---

## 📚 Glossary

| **Term**                             | **Description**                                                                                                   |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| **Emergence Date**                  | The date when crop emergence was detected, used as a reference for planted area computation.                     |
| **Processor Mode**                  | Defines the computation type: **PLANTED_AREA** for planted area calculation, **CONTROL** for unplanted area check.|
| **Control Threshold**               | Percentage threshold for unplanted area in CONTROL mode.                                                          |
| **WKT (Well-Known Text)**           | A standard text format for representing spatial geometries such as points, lines, and polygons.                   |
| **AOI (Area of Interest)**          | A user-defined geographic area selected for analysis.                                                             |

---


--8<-- "snippets/contact-footer.md"