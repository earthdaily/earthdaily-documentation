---
title: Greenness Detection
description: This section explains everything you need to know about the greenness detection analytic.
# icon: fontawesome/question
#status: new
---
<!-- md:swagger API|https://zn6hzsqoyoe3qgaoau4ssgpq440vtmpa.lambda-url.us-east-1.on.aws/docs -->

# Greenness Detection

## 📖 Overview

The **greenness detection analytic** identifies whether the maximum vegetation development (peak greenness) has been reached for a crop field during a growing season. This process analyzes NDVI (1) time series data from satellite imagery to detect the vegetation peak and returns the peak date and maximum NDVI (1) value if detected. The algorithm uses historical patterns based on the specified crop type, season parameters, and sowing date to determine if peak greenness has occurred. This analytic is essential for monitoring crop development stages and timing agricultural operations.
{ .annotate }

1.  --8<-- "../../glossary.md:ndvi"

---

## 🗂️ Baseline Data

The analytic uses NDVI (1) time series data from satellite imagery captured throughout the growing season, combined with season parameters and crop-specific vegetation patterns to accurately detect peak greenness within a defined AOI (2).
{ .annotate }

1.  --8<-- "../../glossary.md:ndvi"
2.  --8<-- "../../glossary.md:aoi"

---

## ⚙️ API

<swagger-ui src="https://zn6hzsqoyoe3qgaoau4ssgpq440vtmpa.lambda-url.us-east-1.on.aws/openapi.json"/>

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Season Duration     | season_duration        | Duration of the growing season in days                                                               | integer    |
| Season Start Day    | season_start_day       | Start day of the season (1-31)                                                                       | integer    |
| Season Start Month  | season_start_month     | Start month of the season (1-12)                                                                     | integer    |
| Year                | year                   | Year of the first date of the season. Historical data from the 5 past years will be used             | integer    |
| Sowing Date         | sowing_date            | Sowing date of the field, format: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS                                 | string     |
| Crop                | crop                   | Enum: "CORN", "SECOND CORN", "SOYBEANS", "SUGARCANE", "COTTON", "OTHERS"                           | string     |
| Data Source         | data_source            | Enum: "LR" (Low Resolution) or "MR" (Medium Resolution)                                             | string     |

---

### Request Body

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | id                     | EarthDaily Agro internal ID of the area of interest (optional)                                       | string     |
| geometry            | geometry               | Geometry of the area of interest (WKT format)                                                        | string     |

---

### Output Variables

| **Parameter**             | **Variable Name**       | **Description**                                               | **Type**   |
|---------------------------|--------------------------|---------------------------------------------------------------|------------|
| Peak Found               | peak_found              | Indicates whether the vegetation peak has been reached        | boolean    |
| Maximum NDVI Value       | max_NDVI_val            | Maximum NDVI value detected during the season                | float      |
| Maximum NDVI Date        | max_NDVI_date           | Date when the maximum NDVI value was reached (YYYY-MM-DD)    | string     |
| ID                       | id                      | EarthDaily Agro internal ID of the area of interest          | string     |

---

## ⚠️ Error Management

| Status Code | Error Type | Description | Example Response |
|-------------|------------|-------------|------------------|
| 401 | Not Authenticated | Missing or invalid authentication token | `{"detail": "Not authenticated"}` |
| 422 | Validation Error | Request validation failed | `{"detail": [{"loc": ["string or integer"], "msg": "string", "type": "string"}]}` |
| 500 | Internal Server Error | Error during greenness detection calculation | `{"detail": "Error while calculating greenness detection"}` |

---

## 📊 Performance and Accuracy

- **Processing Time**: Less than 1 second per field

- **Tested Crops**:
    - Corn
    - Second Corn (2nd Corn)
    - Soybeans
    - Sugarcane
    - Cotton

- **Tested Regions**:
    - Brazil

- **Accuracy Considerations**:
    - Calibration of parameters necessary before testing in other contexts
    - Time series profiles need to be well-defined, requiring sufficient image coverage
    - Sufficient time period after the NDVI peak is needed for detection
    - Detection accuracy is field-specific and depends on peak shape parameters


## 💼 Use Case and Product Integration

This analytic is used in:

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/)

## ⚠️ Important Notes

- The algorithm requires sufficient vegetation coverage and time series data to accurately detect the peak
- Parameters may need calibration when applying to new crops or regions
- Peak detection requires a sufficient time period after the actual peak has occurred
- The detection model uses historical patterns from the 5 previous years based on the specified year parameter

---

--8<-- "snippets/contact-footer.md"