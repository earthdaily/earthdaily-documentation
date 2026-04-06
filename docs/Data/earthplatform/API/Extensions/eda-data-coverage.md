---
title: EDA Data Coverage Extension
description: EDA Data Coverage STAC extension fields for report items
keywords:
  - EDA extension
  - data coverage
  - STAC extension
  - report items
  - region coverage
  - EarthDaily Analytics
---

# EDA Data Coverage Extension

- **Title:** EDA Data Coverage Extension
- **Identifier:** [https://earthdaily-stac-extensions.s3.amazonaws.com/eda_data_coverage/v1.0.0/schema.json](https://earthdaily-stac-extensions.s3.amazonaws.com/eda_data_coverage/v1.0.0/schema.json)
- **Field Name Prefix:** `eda_data_coverage`
- **Scope:** Item

This document explains the EDA Data Coverage Extension to the [SpatioTemporal Asset Catalog (STAC)](https://github.com/radiantearth/stac-spec) specification.

EDA Data Coverage extension defines properties for the Data Coverage Reports.

## Fields

The fields in the table below can be used in these parts of STAC documents:

- [ ] Catalogs
- [ ] Collections
- [x] Items
- [ ] Assets
- [ ] Links

| Field Name | Type | Description |
|------------|------|-------------|
| `eda_data_coverage:region_id` | String | World divided into six regions for automated reports; users can also specify custom regions for manual reports |
| `eda_data_coverage:item_count` | Number | The number of items considered for this report |
| `eda_data_coverage:report_type` | String | Frequency of report generation: daily, weekly, or monthly. If manually triggered, the value is `custom` |
| `eda_data_coverage:region_version` | Number | Version tracking for region updates |
| `eda_data_coverage:month` | Number | Data Coverage Report Month |
| `eda_data_coverage:week` | Number | Data Coverage Report Week |
