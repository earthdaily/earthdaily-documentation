---
title: Bare Soil Detection
description: This section explains everything you need to know about the bare soil detection analytic.
# icon: fontawesome/question
#status: new
---
<!-- md:swagger API|https://bare-soil.aws.geosys.com/docs -->

# Bare Soil Detection

## 📖 Overview

The **bare soil detection analytic** identifies and quantifies periods when agricultural land lacks vegetative cover during a growing season. This processor analyzes satellite imagery using the Dry Bare Soil Index (DBSI) (1) to detect when fields are in a bare soil state. The analytic calculates the total number of bare soil days and identifies distinct bare soil periods within the specified season, providing critical insights for soil conservation monitoring, erosion risk assessment, and sustainable agricultural practice evaluation. This information supports biodiversity initiatives, carbon storage assessments, and compliance with agricultural sustainability standards.
{ .annotate }

1.  --8<-- "../../glossary.md:dbsi"


## 🗂️ Baseline Data

The analytic uses Medium Resolution imagery throughout the specified season to calculate the Dry Bare Soil Index (DBSI) (1) to distinguish bare soil from vegetated areas. Historical imagery data enables retrospective analysis of bare soil periods within a defined AOI (2).
{ .annotate }

1.  --8<-- "../../glossary.md:dbsi"
2.  --8<-- "../../glossary.md:aoi"

---

## ⚙️ API

<swagger-ui src="https://avuqeoz2lrpi2s5qovww5k4vca0itlyy.lambda-url.us-east-1.on.aws/v1/openapi-identity.json"/>

---

## ⚙️ Parameters & Variables

### Input Parameters

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| Season Duration     | seasonDuration         | Duration of the growing season in days (maximum 365 days)                                            | integer    |
| Season Start Day    | seasonStartDay         | Start day of the season (1-31)                                                                       | integer    |
| Season Start Month  | seasonStartMonth       | Start month of the season (1-12)                                                                     | integer    |
| Year                | year                   | Year of the first date of the season of the area of interest                                         | integer    |

---

### Request Body

| **Parameter**       | **Variable Name**     | **Description**                                                                                       | **Type**   |
|---------------------|------------------------|-------------------------------------------------------------------------------------------------------|------------|
| id                  | id                     | EarthDaily Agro internal ID of the area of interest (optional). Enables storage in Analytics database | string     |
| geometry            | geometry               | Geometry of the area of interest (WKT format - POINT or POLYGON)                                     | string     |

---

### Output Variables

| **Parameter**             | **Variable Name**       | **Description**                                               | **Type**   |
|---------------------------|--------------------------|---------------------------------------------------------------|------------|
| Year                      | year                    | Year of the analyzed season                                   | integer    |
| Season Duration           | seasonDuration          | Duration of the season in days                                | integer    |
| Season Start Day          | seasonStartDay          | Start day of the season (1-31)                                | integer    |
| Season Start Month        | seasonStartMonth        | Start month of the season (1-12)                              | integer    |
| Bare Soil Days            | baresoilDays            | Total number of bare soil days (sum of all period lengths)    | integer    |
| Bare Soil Periods         | baresoilPeriods         | Array of bare soil periods with start date, end date, and duration | array      |

### Bare Soil Period Object

| **Field**             | **Variable Name**       | **Description**                                               | **Type**   |
|-----------------------|--------------------------|---------------------------------------------------------------|------------|
| Start Date            | start                   | Date when the bare soil period begins (YYYY-MM-DD)            | string     |
| End Date              | end                     | Date when the bare soil period ends (YYYY-MM-DD)              | string     |
| Period Length         | periodLength            | Number of days in this bare soil period                       | integer    |

---

## 📋 Example Response
```json
{
  "id": "",
  "data": {
    "year": 2023,
    "seasonDuration": 300,
    "seasonStartDay": 1,
    "seasonStartMonth": 4,
    "baresoilDays": 159,
    "baresoilPeriods": [
      {
        "start": "2023-04-14",
        "end": "2023-06-13",
        "periodLength": 61
      },
      {
        "start": "2023-09-14",
        "end": "2023-12-20",
        "periodLength": 98
      }
    ]
  }
}
```

---

## ⚠️ Error Management

| Status Code | Error Type | Description | Example Response |
|-------------|------------|-------------|------------------|
| 401 | Not Authenticated | Missing or invalid authentication token | `{"detail": "Not authenticated"}` |
| 403 | Forbidden | Authentication failed | `{"detail": "Not authenticated"}` |
| 422 | Validation Error | Request validation failed | `{"detail": [{"loc": ["string", 0], "msg": "string", "type": "string"}]}` |
| 500 | Internal Server Error | Error during bare soil calculation | `{"detail": "Internal Server Error"}` |

---

## 📊 Performance and Accuracy

- **Tested Regions**:
    - Europe
    - United States

- **Validation Results**: Very satisfactory accuracy across tested locations

- **Processing Capabilities**:
    - Field-level aggregation
    - Historical data analysis
    - Multiple bare soil period detection within a single season

---

## 💼 Use Case and Product Integration

### Primary Applications

**Agricultural Practice Characterization**:
- Rotation cycle monitoring
- No-till practice verification
- Cover crop adoption assessment
- Conservation agriculture compliance

**Soil Health and Conservation**:
- Soil preservation monitoring
- Erosion risk assessment and control
- Soil quality tracking (leaching and biological degradation risk)
- Biodiversity impact evaluation

**Sustainability and Carbon Programs**:
- Carbon storage potential assessment
- Agricultural sustainability certification
- Environmental compliance reporting
- Biodiversity conservation initiatives

---

## ⚠️ Important Notes

### Bare Soil Period Detection
- The analytic identifies **multiple distinct bare soil periods** within a single season
- Total bare soil days (`baresoilDays`) is the sum of all individual period lengths
- Periods are defined by continuous bare soil conditions based on DBSI threshold exceedance

### Season Definition Constraints
- Maximum season duration is **365 days**
- Season start is defined by month (1-12) and day (1-31) parameters
- Year parameter establishes the starting year of the analysis period

### Data Availability and Quality
- Bare soil detection depends on Sentinel-2 image availability (approximately 5-day revisit time)
- Cloud cover may limit detection capability during certain periods
- Historical analysis enables retrospective assessment of bare soil patterns

### Agricultural Context
- Bare soil periods are natural components of crop rotation cycles
- Extended bare soil periods may indicate:
  - Post-harvest to pre-planting transitions
  - Fallow periods in rotation systems
  - Potential soil conservation concerns if prolonged
  - Opportunities for cover crop implementation

---

## 🌱 Sustainability and Environmental Impact

### Soil Conservation Benefits
**Monitoring bare soil periods supports**:
- **Erosion Control**: Identify fields at risk during vulnerable bare soil phases
- **Soil Quality**: Track periods of increased leaching and biological degradation risk
- **Water Quality**: Assess potential for nutrient runoff during bare periods

### Biodiversity and Carbon Storage
**Bare soil metrics inform**:
- **Carbon Storage Assessment**: Extended bare periods reduce carbon sequestration potential
- **Biodiversity Practices**: Evaluate adoption of cover crops and conservation tillage
- **Ecosystem Services**: Quantify soil protection practices that support biodiversity

### Agricultural Sustainability
**Applications for sustainable agriculture**:
- Verify conservation practice adoption (no-till, cover crops)
- Support sustainability certification and reporting
- Guide farmer education on soil health management
- Enable carbon credit program verification

---

## 📈 Result Interpretation Guidelines

### Bare Soil Days Thresholds
- **<30 days**: Minimal bare soil exposure, good cover management
- **30-90 days**: Moderate bare periods, typical for conventional rotations
- **90-180 days**: Extended bare periods, potential conservation concern
- **>180 days**: Prolonged exposure, high erosion and degradation risk

### Seasonal Patterns
- **Early season bare periods**: Normal post-planting to emergence phase
- **Mid-season bare periods**: May indicate crop failure or management issues
- **Late season bare periods**: Harvest to cover crop or next crop establishment

---

--8<-- "snippets/contact-footer.md"