---
title: Vegetation Time Series
description: This section explains everything you need to know about the vegetation time series.
icon: material/toy-brick-outline
---

# Vegetation Time Series

## 📖 Overview

The **Vegetation Time Series** analytic provides temporal vegetation index data for over agricultural entities. It delivers time-series values of vegetation indices (such as NDVI) at different spatial levels: individual pixels, entity, or combinations thereof. This analytic enables users to track vegetation health and growth patterns over time, supporting crop monitoring, yield prediction, and agricultural decision-making.


## Low Resolution Time Series (LRTS)

The service  offers three data access options:

- **Pixel-level data**: Individual pixel measurements for detailed spatial analysis
- **Season field aggregated data**: Field-level averages for holistic field performance monitoring
- **Season field pixel data**: Combined pixel and field context for comprehensive analysis


### 🗂️ Baseline Data

- **Modis data**


### ⚙️ API Access

<!-- md:swagger API|http://api.geosys-na.net/vegetation-time-series/v1/swagger/index.html -->

<swagger-ui src="http://api.geosys-na.net/vegetation-time-series/v1/swagger/v1.0/swagger.json"/>

---

### ⚙️ Parameters & Variables

#### General Parameters

| **Parameter**         | **Variable Name**       | **Description**                                                                                  | **Type**     |
|-----------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Filter**            | `$filter`                | Filter expression to query specific records (e.g., date ranges, field IDs)                       | `string`     |
| **Sort**              | `$sort`                  | Ordered comma-separated list of fields to sort results                                           | `string`     |
| **Fields**            | `$fields`                | Comma-separated list of fields to retrieve in the response                                       | `string`     |
| **Group By**          | `$group-by`              | Ordered comma-separated list of fields to group results by                                       | `string`     |
| **Limit**             | `$limit`                 | Maximum number of records to return                                                               | `int`        |
| **Offset**            | `$offset`                | Number of records to skip (for pagination)                                                        | `int`        |

#### Input Parameters

| **Parameter**         | **Variable Name**       | **Description**                                                                                  | **Type**     |
|-----------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Accept Partial**    | `acceptPartial`          | Whether to accept partial data when full coverage is not available                                | `boolean`    |
| **Async Mode**        | `$async`                 | Asynchronous processing mode (0, 1, or 2)                                                         | `int`        |
| **Pixel ID**          | `pixel.id`               | Unique identifier for a specific pixel                                                            | `string`     |
| **Season Field ID**   | `seasonField.id`         | Unique identifier for a season field                                                              | `string`     |
| **Date Range**        | `date`                   | Date or date range for filtering vegetation index values                                          | `datetime`   |
| **Vegetation Index**  | `index`                  | Type of vegetation index (0: NDVI, 1: Other)                                                      | `int`        |



### 🔍 Query Capabilities

The API supports advanced filtering and querying through OData-style query parameters:

#### Filtering Examples
```
$filter=date ge '2024-01-01' and date le '2024-12-31'
$filter=index eq 0  (NDVI only)
$filter=seasonField.id eq 'field-123'
$filter=value gt 0.5  (values greater than 0.5)
```

#### Sorting and Grouping
```
$sort=date,-value  (sort by date ascending, value descending)
$group-by=seasonField.id,date
```

#### Field Selection
```
$fields=date,value,index  (return only specific fields)
```

#### Pagination
```
$limit=100&$offset=0  (first 100 records)
```


### Output
#### 1. Pixel Index Values
**Endpoint**: `GET /pixels/values`

Retrieves vegetation index values at the pixel level, providing the most granular spatial resolution for detailed field analysis.

**Response Object**: `PixelIndexValueDto`

| **Field**                | **Variable Name**       | **Description**                                                                                  | **Type**     |
|--------------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Pixel**                | `pixel`                  | Pixel geometry and identifier                                                                     | `object`     |
| **Index**                | `index`                  | Vegetation index type (NDVI, etc.)                                                                | `enum`       |
| **Date**                 | `date`                   | Observation date                                                                                  | `datetime`   |
| **Value**                | `value`                  | Vegetation index value                                                                            | `double`     |
| **Is Extrapolated**      | `isExtrapolated`         | Boolean indicating if the value was extrapolated due to missing data                              | `boolean`    |
| **ID**                   | `id`                     | Unique identifier for this observation                                                            | `string`     |

---

#### 2. Season Field Index Values
**Endpoint**: `GET /season-fields/values`

Retrieves aggregated vegetation index values at the field level for a specific growing season, ideal for field-scale monitoring and comparison.

**Response Object**: `SeasonFieldIndexValueDto`

| **Field**                | **Variable Name**       | **Description**                                                                                  | **Type**     |
|--------------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Season Field**         | `seasonField`            | Season field information (ID, field details, sowing date)                                         | `object`     |
| **Index**                | `index`                  | Vegetation index type                                                                             | `enum`       |
| **Date**                 | `date`                   | Observation date                                                                                  | `datetime`   |
| **Value**                | `value`                  | Aggregated vegetation index value for the field                                                   | `double`     |
| **Is Extrapolated**      | `isExtrapolated`         | Indicates if the value was extrapolated                                                           | `boolean`    |
| **ID**                   | `id`                     | Unique identifier for this observation                                                            | `string`     |

---

#### 3. Season Field Pixel Index Values
**Endpoint**: `GET /season-fields/pixels/values`

Retrieves pixel-level vegetation index values within the context of season fields, combining detailed spatial data with field management information.

**Response Object**: `SeasonFieldPixelIndexValueDto`

| **Field**                | **Variable Name**       | **Description**                                                                                  | **Type**     |
|--------------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Season Field**         | `seasonField`            | Season field information                                                                          | `object`     |
| **Pixel**                | `pixel`                  | Pixel geometry and identifier                                                                     | `object`     |
| **Index**                | `index`                  | Vegetation index type                                                                             | `enum`       |
| **Date**                 | `date`                   | Observation date                                                                                  | `datetime`   |
| **Value**                | `value`                  | Vegetation index value for this pixel                                                             | `double`     |
| **Is Extrapolated**      | `isExtrapolated`         | Indicates if the value was extrapolated                                                           | `boolean`    |
| **ID**                   | `id`                     | Unique identifier for this observation                                                            | `string`     |
---

### 📊 Performance and Accuracy

- **Tested Crops**: All
- **Tested Regions**: Global  
- **Average Generation Time**: < 3 second

## Medium Resolution Time Series (MRTS)

The Medium Resolution Time Series service provides high-resolution vegetation monitoring using imagery from multiple satellite sensors. It delivers both raw and smoothed time series data with advanced filtering and quality control capabilities.

### 🗂️ Baseline Data

**Primary Sensors**:
- **Sentinel-2**: 10m resolution, 5-day revisit, open access
- **Landsat-8/9**: 30m resolution, 8-day revisit (combined), open access

**Additional Sensors** (availability varies by region):
- RapidEye, DEIMOS, DMC, ResourceSat, CBERS-4, GaoFen-1/6, HJ-2A/B, and others

- **Spatial Resolution**: 10m - 30m depending on sensor
- **Temporal Resolution**: 3-5 days (weather dependent)
- **Historical Archive**: 2015+ (varies by sensor and region)

### ⚙️ API Access

<swagger-ui src="https://api.geosys-na.net/field-level-maps/v5/swagger/v1/swagger.json"/>

### ⚙️ Parameters & Variables

#### General Parameters

| **Parameter**         | **Variable Name**       | **Description**                                                                                  | **Type**     |
|-----------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **EPSG Input**        | `$epsg-in`              | Coordinate system for input geometries (4326 or 3857). Default: 4326                             | `int`        |
| **EPSG Output**       | `$epsg-out`             | Coordinate system for output geometries (4326 or 3857). Default: 4326                            | `int`        |

#### Input Parameters

| **Parameter**            | **Variable Name**       | **Description**                                                                                  | **Type**     |
|--------------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Season Field**         | `seasonfield`           | Season field reference (geometry, crop, sowing date). **Required**                               | `object`     |
| **Sensors**              | `sensors`               | Array of satellite sensors to include (e.g., Sentinel_2, Landsat_8, Landsat_9)                  | `array`      |
| **Vegetation Index**     | `vegetationIndex`       | Index type: None, Ndvi, Bi, Evi, Cvi, Cvin, Ndwi, Ndmi, Ndre, GNdvi, S2Rep, Lai, Biomass, Cab, Rvi | `enum`   |
| **Band**                 | `band`                  | Spectral band selection for time series                                                          | `enum`       |
| **Aggregation**          | `aggregation`           | Spatial aggregation method (e.g., Average, Min, Max, Median)                                     | `enum`       |
| **Collections**          | `collections`           | Array of data collections to query                                                               | `array`      |
| **Clear Cover Min**      | `clearCoverMin`         | Minimum clear cover percentage threshold (0-100)                                                 | `double`     |
| **Start Date**           | `startDate`             | Start date for time series extraction (ISO 8601 format)                                          | `datetime`   |
| **End Date**             | `endDate`               | End date for time series extraction (ISO 8601 format)                                            | `datetime`   |

---

### 📊 API Endpoints

#### 1. Single Time Series
**Endpoint**: `POST /time-serie`

Generates a vegetation time series for a single field or geometry of interest.

**Request Body**: `SingleTimeSeriesBodyParameters`

**Response Object**: `SingleTimeSeriesDto`

| **Field**                | **Variable Name**       | **Description**                                                                                  | **Type**     |
|--------------------------|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Raw Data**             | `rawData`               | Array of unprocessed time series values with quality flags                                        | `array`      |
| **Smoothed Data**        | `smoothedData`          | Array of smoothed/interpolated time series values                                                 | `array`      |

**Raw Data Value Properties**:

| **Field**                         | **Description**                                                                                  | **Type**     |
|-----------------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Date**                          | Observation date and time                                                                         | `datetime`   |
| **Value**                         | Vegetation index or band value                                                                    | `double`     |
| **Noised**                        | Boolean indicating if observation is flagged as noisy                                             | `boolean`    |
| **Temporal Consistency Check**    | Quality flag for temporal consistency                                                             | `enum`       |
| **Image**                         | Reference to source satellite image (sensor, date, cloud cover)                                   | `object`     |

**Smoothed Data Value Properties**:

| **Field**                | **Description**                                                                                  | **Type**     |
|--------------------------|--------------------------------------------------------------------------------------------------|--------------|
| **Date**                 | Observation date and time                                                                         | `datetime`   |
| **Value**                | Smoothed vegetation index or band value                                                           | `double`     |
| **Image**                | Reference to source satellite image                                                               | `object`     |

---

#### 2. Multiple Time Series
**Endpoint**: `POST /time-series`

Generates vegetation time series for multiple fields or geometries in batch mode.

**Request Body**: `MultiTimeSeriesBodyParameters`

**Response Object**: `MultiTimeSeriesDto`

Similar structure to Single Time Series but processes multiple geometries in parallel.

---

### 🔍 Data Processing Features

#### Analysis Ready Data
- **Cloud Masking**: Automatic removal of cloud-contaminated pixels
- **Shadow Detection**: Identification and filtering of cloud shadow effects
- **Temporal Consistency**: Statistical outlier detection and flagging
- **Noise Flagging**: Quality flags for potentially noisy observations

#### Post process options
- **Gap Filling**: Interpolation for missing observations due to clouds or sensor gaps
- **Temporal Smoothing**: Reduction of noise while preserving phenological patterns
- **Outlier Removal**: Automated detection and correction of anomalous values

#### Aggregation Methods
- **Average**: Mean value across field
- **Median**: Median value for robust statistics
- **Min/Max**: Minimum or maximum values
- **Percentile**: Custom percentile calculations

---

### 📊 Supported Vegetation Indices

| **Index**     | **Name**                                    | **Application**                                        |
|---------------|---------------------------------------------|--------------------------------------------------------|
| **NDVI**      | Normalized Difference Vegetation Index      | General vegetation health and biomass                   |
| **EVI**       | Enhanced Vegetation Index                   | Improved sensitivity in high biomass areas              |
| **NDWI**      | Normalized Difference Water Index           | Water content and stress detection                      |
| **NDMI**      | Normalized Difference Moisture Index        | Canopy moisture content                                 |
| **NDRE**      | Normalized Difference Red Edge              | Nitrogen content and chlorophyll                        |
| **GNDVI**     | Green NDVI                                  | Chlorophyll content                                     |
| **S2REP**     | Sentinel-2 Red Edge Position                | Chlorophyll and nitrogen status                         |
| **LAI**       | Leaf Area Index                             | Canopy structure and biomass                            |
| **Biomass**   | Biomass Index                               | Above-ground biomass estimation                         |
| **CAB**       | Chlorophyll A+B                             | Chlorophyll concentration                               |
| **RVI**       | Ratio Vegetation Index                      | Simple vegetation assessment                            |

---

### 📊 Performance and Accuracy

- **Tested Crops**: All  crops
- **Tested Regions**: Global coverage
- **Processing Time**: 5-30 seconds for single field, 1-5 minutes for batch processing
- **Data Availability**: Historical data from 2015+ 
- **Temporal Coverage**: Complete growing season with 3-5 day frequency

---

## 💼 Use Case and Product Integration

This analytic is used in:

- [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/) - Multi-field vegetation monitoring
- **Crop Health Monitoring**: Identify stress patterns and anomalies with high spatial detail
- **Yield Forecasting**: Analyze vegetation trends for yield prediction models
- **Insurance Assessment**: Document crop conditions for claims processing with audit trail
- **Variable Rate Application**: Generate high-resolution prescription maps
- **Historical Benchmarking**: Compare current season performance against historical data
- **Precision Agriculture**: Field-level variability analysis and zone management
- **Research & Development**: Crop phenology studies and algorithm validation


## 🔗 Enabled Analytics

As a foundational analytic, vegetation time series is the baseline input for the following analytics:

- [Historical Potential Score](./HistoricalPotentialScore.md) - Benchmark field performance
- [In-Season Monitoring](./InSeasonMonitoringmd) - Track crop development throughout the growing season
- [Emergence Detection](./Emergence.md) - Identify crop emergence dates
- [Greenness](./Emergence.md) - Identify crop peak vegetation

---


--8<-- "snippets/contact-footer.md"