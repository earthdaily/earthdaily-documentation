---
title: EDA STAC Extension
description: EDA-specific STAC extension fields for collections and items
keywords:
  - EDA extension
  - STAC metadata
  - cloud mask
  - sensor type
  - geometric accuracy
  - EarthDaily Analytics
  - satellite imagery metadata
---

# EDA STAC Extension

- **Title:** EDA Extension
- **Identifier:** [https://earthdaily-stac-extensions.s3.amazonaws.com/eda/v0.1.0/schema.json](https://earthdaily-stac-extensions.s3.amazonaws.com/eda/v0.1.0/schema.json)
- **Field Name Prefix:** `eda`
- **Scope:** Item, Collections

This document explains the EDA Extension to the [SpatioTemporal Asset Catalog (STAC)](https://github.com/radiantearth/stac-spec) specification.

EDA Extension adds metadata related to EDA specific details like ImagerMode, Sensor Type, Water Cover, Radiometric Scaling, Geometric Accuracy RMSE etc that affect the view of resulting data. It will often be combined with other extensions that describe the actual data, such as the eo, proj or sat extensions.

## Public Fields

The fields in the table below can be used in these parts of STAC documents:

- [ ] Catalogs
- [x] Collections
- [x] Items
- [ ] Assets
- [ ] Links

| Field Name | Type | Description |
|------------|------|-------------|
| `eda:order_line_item_id` | String | Specifies the order line item id within EarthPipeline |
| `eda:source_l0_ids` | List of Strings | Archive IDs of the source level-0 datasets |
| `eda:source_l0_scene_ids` | List of Strings | Scene IDs of the source Level-0 datasets |
| `eda:segment_id` | String | Dataset identifier for the acquisition used to generate the product `<Datetime>_<Sensor><SID><Cat>` |
| `eda:imager_mode` | String | Non-experimental modes: "TDI_LAND", "TDI_MARITIME", "TDI_GLOBAL", "PUSH_FRAME_GLOBAL". Only provided for Catalogue products |
| `eda:image_section_counter` | Number | Image section counter. Only provided for Catalogue products |
| `eda:geometric_accuracy_rmse` | Number | Radial RMSE, in meters. Only provided for specific L1C and L2A products |
| `eda:sensor_type` | String | The sensor type (currently "OPTICAL") |
| `eda:product_type` | String | Only available for the "GOES" collection |
| `eda:water_cover` | Number | Estimate of water cover, in % |
| `eda:derived_from_item_id` | String | L2 item used for L2 derived products |
| `eda:derived_from_collection_id` | String | L2 collection used for L2 derived products |
| `eda:ag_cloud_mask_available` | Boolean | Whether EDAgro cloud mask is available |
| `eda:ag_cloud_mask_item_id` | String | EDAgro Cloud Mask item id |
| `eda:ag_cloud_mask_collection_id` | String | EDAgro Cloud Mask collection id |
| `eda:cloud_mask_available` | Boolean | Whether EDA cloud mask is available |
| `eda:cloud_mask_item_id` | String | EDA Cloud Mask item id |
| `eda:cloud_mask_collection_id` | String | EDA Cloud Mask collection id |
| `eda:area_km2` | Number | Mosaic - approximate area in km^2 of the valid region |
| `eda:radiometric_scaling` | Number | Obsolete |
| `eda:pixel_composite_method` | String | Pixel Composite Method used for Mosaics |

