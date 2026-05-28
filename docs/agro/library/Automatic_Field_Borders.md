---
title: Automatic Boundary
description: This section wil explain how to access field borders using a longitude and a latitude as the input.
keywords:
  - field borders
  - automatic boundary
  - Sentinel-2
  - super-resolution
  - GeoJSON
  - field delineation
# icon: fontawesome/question
#status: new
---

# Automatic Field Borders

## 📖 Overview

This analytic automatically generates field boundaries based on point coordinates (longitude and latitude). 
The feature is accessible via both the API and the GeosysApp.
Postman collection is available.
Your account requires specific permissions to access this API. Please contact us to request access.

## 🗂️ Baseline data

It leverages super-resolution Sentinel-2 imagery at 1-meter resolution to delineate field borders with high precision.

## ⚙️ API 

<!-- md:swagger https://api.geosys-na.net/field-borders/v1/swagger/index.html -->

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Location     | location     | Latitude and Longitude coordinates corresponding to the field's location     | string     |
| Simplified Geometry     | simplified_geom     | If TRUE, returns a more simplified geometry (fewer vertices - easier for large geoprocessing tasks)     | boolean     |

### Request Body

- Example URL
    - https://api.geosys-na.net/field-borders/v1/AutomaticBoundary?location={longitude},{latitude}&simplified_geom=true

### Output

- The output is a GeoJSON-formatted geometry object.

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Type    | type    | Object called a "Feature"    | string    |
| Geometry    | geometry    | Will include a type (Polygon) and Lat/Long coordinates of each vertice.     | string     |


## 📊 Performance and Accuracy

Intersection of Union average accuracy score of 0.94-0.96.

## Use case and product

This analytic is used in:

- [Portfolio](/earthdaily-documentation/agro/portfolio/portfolio_product_site_draft/)

--8<-- "snippets/contact-footer.md"
