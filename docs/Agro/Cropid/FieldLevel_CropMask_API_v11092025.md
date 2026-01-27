
<meta property="og:title" content="This page presents the Field-Level Crop Mask API provided by Earthdaily Agro..">

# Field-Level API to get Crop Rotations


## 🌾 Introduction

The **Field-Level Crop Mask API** enables querying the planted crops for a given geometry and time window. The information is retrieved from the crop masks produced internally or sourced from public data. Understanding which crop has been planted is a foundational step for many downstream services. 

## 🗺️ Field-Level Crop Mask API Summary

### Access via **REST API**
The **Field-Level Crop Mask API** encompasses a suite of four endpoints designed to support variable applications and to be easily integrated into internal systems, analytical pipelines, or external applications.

| Method | Route | Description |Request |
|--------|---------|--------|---------|
| Post | `/cropmasks/crops`| Retrieve which crops are presen within a geometry for one or several agricultural seasons leveraging the latest crop mask available | JSON body with list of parameters|
|Post| `/cropmasks/crop-details`| Retrieve which crops are detected within a geometry and for all the crop masks available for one or more agricultural seasons|JSON body with list of parameters|
|Post| `/cropmasks/years`| Return the year(s) in which a specific crop has been detected within a given geometry, based on crop mask data.|JSON body with list of parameters|
|Post| `/cropmasks/layers-crop`| Retrieve which fields have a specific crop within a defined area for a targeted agricultural season|


### Supported Geometries
**The Field-Level Crop Mask API** supports Polygon geometries (fields level) in WKT format & Coordinates must be provided in WGS 84 (EPSG:4326)

---

## 🧭 API Endpoints

### 🔐 Authentication

All endpoints require secure access via **Identity Server API**, which manages:

- User and application-level authentication  
- Token-based access (OAuth 2.0)  
- Permission scopes to control access to specific data layers or regions

### 🌱 Endpoint 1: Dominant Crop Detection
 `/cropmasks/crops` (POST)


#### 🧾 Purpose

Identify the dominant crop(s) within a given geometry for one or more years by querying internal and external crop mask sources. This endpoint returns a list of detected crops, their properties, and the coverage percentage within the input field.


#### ⚙️ High-Level Functionality

- The user submits a geometry in WKT format.
- Optional metadata fields can be specified through `Properties` and `CropProperties`.
- Filters can be applied based on year, source, product type, season, and minimum coverage percentage.
- The response lists the detected crops with associated attributes, sorted by dominance if specified.

#### 📌 Business Rules

- `GeometryWkt` is **mandatory**.
- If `CropProperties` is defined, you must **explicitly list** each desired property.
- The following fields are **returned by default** (unless their values are `null`), even if not listed in the request:
  - `CropName`
  - `EDACropCode`
  - `RawCropName`
  - `CropMaskPercent`


### 🌱 Endpoint 2:  `/cropmasks/crop-details` (POST)

#### 🧾 Purpose

Retrieve all crop occurrences detected within a given geometry, using **every available crop mask**. This endpoint returns detailed crop detection results year by year, for each mask used.


#### ⚙️ High-Level Functionality

- Accepts the **same input structure** as `/cropmasks/crops`.
- For each year in the defined range, returns crop detections **from all masks** (not just the dominant one).
- Aggregates results **per year** and **per mask**, providing both crop-specific and mask-specific properties.

#### 📌 Business Rules

- `GeometryWkt` is **mandatory**.
- If `CropProperties` is defined, you must **explicitly list** each desired property.
- The following fields are **returned by default** (unless their values are `null`), even if not listed in the request:
  - `CropName`
  - `EDACropCode`
  - `RawCropName`


### 🌱 Endpoint 3:  `/cropmasks/years` (POST)

#### 🧾 Purpose

Return the **year(s)** in which a **specific crop** has been detected within a given geometry, based on crop mask data. This is useful for historical crop presence analysis and crop rotation tracking.

#### ⚙️ High-Level Functionality

- The user provides a geometry and optionally filters for a specific crop using one or more crop attributes.
- The system checks all relevant crop masks to determine in which years the crop is present.
- Optional filters let the user refine results by collections, products, sources, crop dominance, and percentage threshold.


#### 📌 Business Rules

- `GeometryWkt` is **mandatory**.
- At least one crop attribute in `CropInfo` must be provided to identify the target crop.
- If `CropMaskPercentMin` is set, years in which the crop coverage is below the specified threshold will **not** be returned.
- If `TakeOnlyMajorityCrop` is `true`, only the main (most dominant) crop will be considered for each year.


---
### 🌱 Endpoint 4:  `/cropmasks/layers-crop` (POST)

- **Purpose**: Retrieve which fields have a specific crop within a defined area for a targeted agricultural season. 
- **Output**: Array listing the intersected items where the given crop has been detected for a given year.
- **Get more details**: Reach out your local contact to get more details on how to use this endpoint.

---


## 🧰 Developer Resources

Interactive API documentation is available via Swagger:

👉 [CropMask API Swagger (PROD)](https://api.geosys-na.net/cropmasks/v1/swagger/index.html)

<swagger-ui src="https://api.geosys-na.net/cropmasks/v1/swagger/v1/swagger.json"/>
 
You can use this interface to:

- Explore available endpoints
- Test requests directly from the browser
- View request/response formats and examples


--8<-- "snippets/contact-footer.md"


