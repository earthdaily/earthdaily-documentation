---
title: Available Collections
description: Full list of open and EDA-specific collections available in Earth Data Store
keywords:
  - Earth Data Store collections
  - Sentinel-2
  - Landsat
  - Sentinel-1
  - satellite imagery catalog
  - open data collections
  - EDA collections
  - STAC collections
---

# Available Collections

## Accessing Available Collections

The collections listed below are available in our free tier to start with. You can search and interact with them using various ways:

- [EarthPlatform](../console/earthplatform.md) — The interactive UI available through EDS Platform
- [API](../api/api-usage/endpoints.md) — With [Command line](../api/api-usage/commandline.md), [Postman](../api/api-usage/postman.md), and [Python](../api/api-usage/python.md) examples
- [EarthDaily Python Client](https://github.com/earthdaily/earthdaily-python-client) — Package to accelerate your access to the EarthDataStore

## List of available Collections

### Open Collections

| Collection Name | Collection Id | Source of Collection | Time range |
|-----------------|---------------|----------------------|------------|
| Landsat Collection 2 L1 | `landsat-c2l1` | AWS Open Data — [USGS Landsat](https://registry.opendata.aws/usgs-landsat/) | Starting Jan 2013 |
| Landsat Collection 2 L2 Reflectance | `landsat-c2l2-sr` | AWS Open Data — [USGS Landsat](https://registry.opendata.aws/usgs-landsat/) | Starting Jan 2013 |
| Landsat Collection 2 L2 Temperature | `landsat-c2l2-st` | AWS Open Data — [USGS Landsat](https://registry.opendata.aws/usgs-landsat/) | Starting Jan 2013 |
| Sentinel 1 GRD | `sentinel-1-grd` | AWS Open Data — [Sentinel-1](https://registry.opendata.aws/sentinel-1/) | Starting Oct 2014 |
| Sentinel-1 RTC | `sentinel-1-rtc` | MSFT Planetary Computer — [Sentinel 1 RTC](https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc) | Starting Oct 2014 |
| Sentinel 2 L1C | `sentinel-2-l1c` | AWS Open Data — [Sentinel-2](https://registry.opendata.aws/sentinel-2/) | Starting June 2015 |
| Sentinel 2 L2A | `sentinel-2-l2a` | AWS Open Data — [Sentinel-2 COGs](https://registry.opendata.aws/sentinel-2-l2a-cogs/) | Starting Nov 2016 |
| Sentinel 2 C1 L2A | `sentinel-2-c1-l2a` | AWS Open Data — [Sentinel-2 COGs](https://registry.opendata.aws/sentinel-2-l2a-cogs/) | Starting Nov 2016. Reprocessing of Sentinel 2 L2A (which will be deprecated once fully populated) |
| Venus L2A | `venus-l2a` | Theia — [VM1](https://theia.cnes.fr/atdistrib/rocket/#/search?page=1928&collection=VENUS&processingLevel=LEVEL2A) / [VM5](https://theia.cnes.fr/atdistrib/rocket/#/search?page=42&collection=VENUSVM05&platform=VENUS&processingLevel=LEVEL2A) | Starting Nov 2017 |

### EDA Collections

| Collection Name | Collection Id |
|-----------------|---------------|
| Above Ground Biomass Density, Tree Height and Tree Cover (multi mode input at 10m resolution) | `earthdaily:carbon-analytics:multimode-10m-agbd:3x3:v2.1` |
| AI Ready Mosaics | `ai-ready-mosaics` |
| AI Ready Mosaics Preview | `ai-ready-mosaics-preview` |
| AI Ready Mosaics Sample | `ai-ready-mosaics-sample` |
| Cropland Data Layer US | `cropland-data-layer-us` |
| EDC Preview | `edc-preview` |
| Forest mask (multi mode input at 10m resolution) | `earthdaily:carbon-analytics:forestmask:3x3:v2.1` |
