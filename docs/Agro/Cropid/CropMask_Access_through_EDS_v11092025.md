<meta property="og:title" content="This page presents the Crop Mask API (STAC) to access Crop Mask Layer..">

# Crop Mask API (STAC) Documentation

## Overview
The Crop Mask API provides access to **public** and **private crop mask layers**. These datasets can be used for agricultural monitoring, land classification, and crop analytics.  

The API is built on top of the **EarthDaily platform** and follows the [STAC (SpatioTemporal Asset Catalog)](https://stacspec.org/) standard.

---
## Authentication

- **Endpoint:**  
  `POST https://api.earthdaily.com/account_management/v1/authentication/api_tokens/exchange`  

- **Request Body:**  
  JSON containing your `EDS_CLIENT_ID` and `EDS_SECRET`.  

- **Response:**  
  JSON object with an `access_token`, used in subsequent requests via:  
  ```
  Authorization: Bearer <access_token>
  ```

---

## Collections

- **Public Crop Mask** → `public-crop-mask`  
   
    The following crop mask layers are referenced on the STAC Catalog from Earthdaily Data Store
    - **Cropland Data Layer (CDL)**, a product from United States Department of Agriculture (USDA) National Agricultural Statistics Service (NASS). The CDL is an annual raster, geo-referenced, crop-specific land cover data layer produced using satellite imagery and extensive agricultural ground reference data. For more information, visit the [Cropland Data Layer homepage](https://www.nass.usda.gov/Research_and_Science/Cropland/SARS1a.php).

    - **Registre Parcellaire Graphique (RPG)**, a product from the French Ministry of Agriculture and Food Sovereignty. The RPG is an annual, vector-based, geo-referenced dataset that describes the agricultural parcels declared by farmers in the context of the European Union’s Common Agricultural Policy (CAP). It provides detailed crop type information at the parcel level. For more information, visit the [RPG portal](geoservices.ign.fr/documentation/donnees/vecteur/rpg).

    - **Crop Type Map (CTM)**, a product provided by the German Aerospace Center (DLR). The CTM is a raster, geo-referenced dataset generated from satellite imagery (such as Sentinel-2) using advanced classification algorithms. It provides annual information on crop type distribution at field level. For more information, visit the [DLR website](https://www.dlr.de/en/latest/news/2024/these-crops-grow-in-germany-six-year-analysis).

  All layers are referenced in one place for convenience, enabling seamless analysis of historical trends, crop rotations, and year-over-year changes — without the need to manage multiple data sources.  


- **Private Crop Mask (EDAgro Analytics)** → `edagro-analytics-crops-layer`  

  The **private collection** contains crop mask layers computed **during the growing season**, enabling enabling data-driven decisions based on crop-specific analytics. 



## Search for Crop Mask Items

**Endpoint:**  
  `GET https://api.earthdaily.com/platform/v1/stac/search`  

**Parameters:**  
  - `collections` → The collection ID (e.g., `edagro-analytics-crops-layer`)  
  - `bbox` → Bounding box filter `[minLon, minLat, maxLon, maxLat]`  
  - `datetime` → Date or date range (`YYYY-MM-DD` or `YYYY-MM-DD/YYYY-MM-DD`)  
  - `limit` → Maximum number of results  


**Response Example:**
  
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "id": "edagro_cropmask_france_2023",
      "collection": "edagro-analytics-crops-layer",
      "bbox": [2.0, 43.0, 3.0, 44.0],
      "properties": {
        "datetime": "2023-07-01T00:00:00Z",
        "crop_type": "maize",
        "confidence": 0.92
      },
      "assets": {
        "mask": {
          "href": "https://api.earthdaily.com/assets/edagro-analytics-crops-layer/edagro_cropmask_france_2023.tif",
          "type": "image/tiff",
          "title": "Crop Mask for Maize - France, 2023"
        }
      }
    }
  ]
}
```


## Downloading a Crop Mask

1. Perform a search on the `edagro-analytics-crops-layer` collection.  
2. From the response, identify the `assets` section.  
3. Use the `href` URL to download the file.  

- **Request:**  
  A standard `GET` request to the `href` URL, with your access token if required.  

- **Response:**  
  A binary GeoTIFF file that can be opened in GIS software or processed with remote sensing libraries.  

---

## Error Handling

| Status Code | Meaning                            |
|-------------|------------------------------------|
| `401`       | Unauthorized – check your token    |
| `403`       | Forbidden – insufficient access    |
| `404`       | Collection or item not found       |
| `429`       | Too many requests – rate limited   |
| `500`       | Internal server error              |

---

## Best Practices

- Apply **filters** (`bbox`, `datetime`) to reduce query size.  
- Cache authentication tokens until expiry.  
- Request access to `edagro-analytics-crops-layer` to access any dataset.  
