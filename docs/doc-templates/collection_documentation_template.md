---
title: Collection Documentation Template
description: Template for documenting satellite data collections on the EarthDaily platform.
tags:
  - template
---

# <Collection name>

## Overview

<!-- 
  2–4 sentences. Describe: (1) what instrument/sensor this comes from, 
  (2) what the data represents physically, (3) why it matters for EDS users.
  Add a representative illustration or false-color image below.
-->

![Collection banner](./assets/images/<collection-name>-banner.webp)
<!-- Caption: Brief description of the image content and the date/location of acquisition -->

---

## Key Characteristics

<!-- Quick-reference summary table. Fill every row; use "—" if not applicable. -->

| Attribute              | Value                                      |
|------------------------|--------------------------------------------|
| **Sensor / Mission**   | e.g. Sentinel-2 MSI / ESA Copernicus       |
| **Platform**           | e.g. Sentinel-2A & 2B (twin constellation) |
| **Processing level**   | e.g. Level-2A (Surface Reflectance)        |
| **Spatial resolution** | e.g. 10 m / 20 m / 60 m (band-dependent)  |
| **Revisit time**       | e.g. 5 days (global, at equator)           |
| **Temporal coverage**  | e.g. June 2015 – present                   |
| **Spatial coverage**   | e.g. Global land surface                   |
| **File format**        | e.g. Cloud-Optimized GeoTIFF (COG)         |
| **Projection / CRS**   | e.g. UTM (EPSG:326xx / 327xx), WGS84      |
| **Update frequency**   | e.g. Daily, within 6 h of acquisition      |
| **License**            | e.g. Copernicus Open Access (CC BY-SA 3.0) |

---

## Spectral Bands

<!--
  Include only if the collection has multiple spectral channels.
  Use nm for wavelengths. Mark the primary-use bands somehow (bold name, or a "★" in Notes).
-->

| Band | Name              | Central Wavelength | Bandwidth | Resolution | Notes                        |
|------|-------------------|--------------------|-----------|------------|------------------------------|
| B01  | Coastal Aerosol   | 443 nm             | 20 nm     | 60 m       | Atmospheric correction       |
| B02  | Blue              | 490 nm             | 65 nm     | 10 m       | ★ RGB composite              |
| B03  | Green             | 560 nm             | 35 nm     | 10 m       | ★ RGB composite              |
| B04  | Red               | 665 nm             | 30 nm     | 10 m       | ★ RGB composite / NDVI       |
| B08  | NIR               | 842 nm             | 115 nm    | 10 m       | ★ Vegetation indices         |
| B8A  | Narrow NIR        | 865 nm             | 20 nm     | 20 m       | Red-edge vegetation          |
| B11  | SWIR-1            | 1610 nm            | 90 nm     | 20 m       | Moisture / burn scars        |
| B12  | SWIR-2            | 2190 nm            | 180 nm    | 20 m       | Bare soil discrimination     |
| ...  | ...               | ...                | ...       | ...        | ...                          |

---

## Data Layers

<!--
  Use this section instead of (or in addition to) Spectral Bands when the collection 
  delivers derived layers (masks, indices, classifications, scores) rather than raw bands.
  Each row is one raster band or file in the delivered asset.
-->

| Layer | Name              | Data Type | Value Range  | No-data | Description                                      |
|-------|-------------------|-----------|--------------|---------|--------------------------------------------------|
| 1     | Surface Reflectance | Int16   | 0 – 10 000   | -9999   | Bottom-of-atmosphere reflectance, scaled × 10 000 |
| 2     | SCL (Scene Class) | UInt8     | 0 – 11       | 0       | Per-pixel land/cloud/shadow classification        |
| 3     | ...               | ...       | ...          | ...     | ...                                               |

---

## Processing & Methodology

<!--
  Describe the processing chain: input source → algorithm/model → output.
  Reference ESA, NASA, or internal EDS algorithm docs where applicable.
  A simple flowchart or block diagram is encouraged here.
-->

### Processing levels

| Level    | Description                                              | Provided by EDS |
|----------|----------------------------------------------------------|-----------------|
| Level-1C | Top-of-atmosphere reflectance, orthorectified            | ✗               |
| Level-2A | Bottom-of-atmosphere reflectance (Sen2Cor / LaSRC)       | ✓               |
| ARD      | Analysis-Ready Data with harmonized CRS and tiling       | ✓               |

### Algorithm

Briefly describe the atmospheric correction, calibration, or classification algorithm. Link to the relevant scientific publication or ATBD (Algorithm Theoretical Basis Document).

> **Reference:** Author et al. (Year). *Title of the paper or technical note*. Journal/Agency. [DOI or URL]

---

## Quality & Accuracy

<!--
  Quantitative performance metrics. Mirror Planet's approach: accuracy tables + caveats.
  Include sensor-level and algorithm-level quality information.
-->

### Known limitations

- **Cloud contamination:** pixels covered by cloud or shadow are flagged in the SCL layer and should be masked prior to analysis.  
- **BRDF effects:** surface reflectance values vary with sun-sensor geometry, particularly at high latitudes and on steep terrain.  
- **Saturation:** bright surfaces (snow, salt pans) may saturate in the VNIR bands.

### Validation

| Metric                | Value    | Reference                   |
|-----------------------|----------|-----------------------------|
| Absolute reflectance accuracy | ±3 %   | ESA Sentinel-2 Validation Report (2023) |
| Geolocation accuracy | < 12.5 m | ESA MPC QA Report            |
| Cloud mask accuracy  | ~95 %    | Zupanc (2021)                |

---

## Metadata Fields

<!--
  List the item-level metadata attributes that are searchable via the EDS API / STAC catalog.
  This mirrors Planet's "Metadata fields" section and helps users build filters.
-->

| Field                  | Type    | Range / Values         | Description                                      |
|------------------------|---------|------------------------|--------------------------------------------------|
| `datetime`             | string  | ISO 8601               | Scene acquisition UTC timestamp                  |
| `platform`             | string  | `sentinel-2a`, `sentinel-2b` | Satellite identifier                      |
| `eo:cloud_cover`       | float   | 0 – 100                | Percentage of scene covered by cloud             |
| `s2:mgrs_tile`         | string  | e.g. `33UUP`           | MGRS grid tile identifier                        |
| `s2:processing_baseline` | string | e.g. `05.00`          | ESA processing baseline version                  |
| `s2:nodata_pixel_percentage` | float | 0 – 100          | Percentage of pixels outside the swath footprint |
| `view:sun_azimuth`     | float   | 0 – 360 °              | Sun azimuth angle at scene centre                |
| `view:sun_elevation`   | float   | 0 – 90 °               | Sun elevation angle at scene centre              |

---

## Tiling & Delivery

<!--
  Describe how the data is tiled, gridded, and packaged for delivery on EDS.
-->

- **Tiling scheme:** MGRS 100 × 100 km tiles (e.g. `33UUP`), or EDS internal grid (link to grid spec).  
- **Delivery format:** Cloud-Optimized GeoTIFF (COG) with internal overviews.  
- **Archive structure:** `s3://eds-collections/<collection-id>/<year>/<month>/<day>/<tile>/`  
- **Compression:** LZW / Deflate, predictor 2.  
- **STAC Catalog endpoint:** `https://stac.eds.earthdaily.com/collections/<collection-id>`

---

## API Access

<!-- Remove or replace the swagger block with the correct EDS endpoint URL -->

<swagger-ui src="https://api.eds.earthdaily.com/openapi/<collection-id>.json"/>

### Quick start — Python

```python
import earthdaily

client = earthdaily.EarthDataStore()

items = client.search(
    collections=["<collection-id>"],
    datetime="2024-06-01/2024-06-30",
    bbox=[-95.5, 42.0, -93.5, 44.0],   # [west, south, east, north]
    query={"eo:cloud_cover": {"lt": 20}},
)

# Load first item as an xarray DataArray
da = items[0].assets["B04"].open()
```

### STAC example

```bash
curl -X GET "https://stac.eds.earthdaily.com/collections/<collection-id>/items" \
  -H "Authorization: Bearer $EDS_TOKEN" \
  -G \
  --data-urlencode "bbox=-95.5,42.0,-93.5,44.0" \
  --data-urlencode "datetime=2024-06-01/2024-06-30" \
  --data-urlencode "limit=10"
```

---

## Archive Availability

<!--
  Use admonitions for important caveats (gaps, reprocessing events, regional differences).
-->

This collection is available globally from **<start date>** to **present** (or **<end date>** if discontinued).

!!! info "Regional availability"
    Higher temporal density (daily revisit) is available over specific agricultural priority regions from **<date>**. Contact your EDS account representative for the regional coverage map.

!!! warning "Processing baseline change"
    Scene products generated before **<date>** were produced with processing baseline **vX.Y** and may exhibit radiometric offsets relative to more recent acquisitions. Apply the published offset correction before combining data across this boundary.

---

## Related Collections

| Collection                     | Relationship                                      | Link                          |
|--------------------------------|---------------------------------------------------|-------------------------------|
| `<collection-id-2>`            | Higher-resolution companion (5 m)                 | [→ Documentation](<link>)     |
| `<collection-id-3>`            | SAR complement for cloud-penetrating observations | [→ Documentation](<link>)     |
| `<analytic-name>`              | Derived analytic built on this collection         | [→ Documentation](<link>)     |

---

## Use Cases

This collection is used in the following EDS products and analytics:

- **<Product / Analytic name 1>** — brief explanation of how this collection feeds the product.  
- **<Product / Analytic name 2>** — brief explanation.

### Example applications

- Crop monitoring and phenology tracking using time-series NDVI derived from red and NIR bands.  
- Post-disaster damage assessment combining SWIR bands before/after the event.  
- Land-use / land-cover classification at national scale.

---

## License & Citation

**License:** <!-- e.g. Copernicus Open Access (CC BY-SA 3.0) / Landsat courtesy of USGS -->

**How to cite:**

```
<Agency/Provider> (<Year>). <Collection full name> [Data set]. 
EarthDaily Analytics EDS Platform. https://eds.earthdaily.com/collections/<collection-id>. 
Accessed <DATE>.
```

---

## References

- Author, A., & Author, B. (Year). *Title of paper*. *Journal Name*, Vol(Issue), pp–pp. [https://doi.org/xxx](https://doi.org/)  
- Agency (Year). *Algorithm Theoretical Basis Document (ATBD) for <product>*. Technical Report ESA-EOP-SD/1667. [URL]  
- Agency (Year). *<Collection name> User Guide*. [URL]
