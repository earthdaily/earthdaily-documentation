---
title: Sentinel-2
description: Sentinel-2 multispectral optical imagery collections available through EarthDaily
keywords:
  - Sentinel-2
  - multispectral imagery
  - optical satellite
  - surface reflectance
  - 10m resolution
  - ESA Copernicus
  - L2A
  - L1C
---

# Sentinel-2

Multispectral optical imagery from ESA's Sentinel-2 constellation, providing global coverage every 5 days at 10–60m resolution.

## Available Collections

| Collection Name | Collection Id | Processing Level | Time Range |
|-----------------|---------------|------------------|------------|
| Sentinel 2 L1C | `sentinel-2-l1c` | Top-of-atmosphere reflectance | Starting June 2015 |
| Sentinel 2 L2A | `sentinel-2-l2a` | Surface reflectance | Starting Nov 2016 |
| Sentinel 2 C1 L2A | `sentinel-2-c1-l2a` | Surface reflectance (reprocessed) | Starting Nov 2016 |

## Key Characteristics

- **Spatial resolution**: 10m (visible + NIR), 20m (red edge + SWIR), 60m (atmospheric bands)
- **Revisit time**: 5 days at the equator with 2 satellites
- **Swath width**: 290 km
- **Number of bands**: 13 spectral bands

## Notes

- **Sentinel-2 C1 L2A** is the reprocessed version of Sentinel-2 L2A with improved radiometric calibration. It will replace Sentinel-2 L2A once fully populated.
- Source: AWS Open Data — [Sentinel-2](https://registry.opendata.aws/sentinel-2/) and [Sentinel-2 COGs](https://registry.opendata.aws/sentinel-2-l2a-cogs/)
