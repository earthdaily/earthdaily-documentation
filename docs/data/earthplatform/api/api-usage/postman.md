---
title: Postman Examples
description: Postman screenshots and configuration for EarthDaily STAC API endpoints
keywords:
  - Postman
  - STAC API
  - API testing
  - query extension
  - fields extension
  - sortby extension
  - EarthDaily API
---

# Postman Examples

Before you try out the various endpoints, you need to set up the authentication for Postman. [Authentication Page](../../getting-started/authentication.md#postman) describes how it is done.

## Collections

Return list of all Collections

![Collections](../../../../assets/data/STACAPI/PostmanExamples/Collections.png)

## Collection

Return specific Collection

![Collection](../../../../assets/data/STACAPI/PostmanExamples/Collection.png)

## Items

Return paged Items ordered by datetime descending

![Items](../../../../assets/data/STACAPI/PostmanExamples/Items.png)

## Item

Returns a single Item for a given Collection and Item ID

![Item](../../../../assets/data/STACAPI/PostmanExamples/ItemId.png)

## Queryables

Returns the queryable names for the STAC API Item Search using Query Extension

![Queryables](../../../../assets/data/STACAPI/PostmanExamples/Queryables.png)

## Search

Implements STAC basic Item search functionality + extensions

Ensure the **content-type** header is **application/json**

![Search](../../../../assets/data/STACAPI/PostmanExamples/PostSearchWithData.png)

### Query Extension via POST Method

!!! note
    EarthPlatform STAC API supports the [Query Extension](https://github.com/stac-api-extensions/query). It currently does not support the Filter Extension.

Advanced searching can be performed using a `query` object.

![Query Extension](../../../../assets/data/STACAPI/PostmanExamples/QueryExtension.png)

### Fields Extension

The Fields Extension allows you to specify which fields are returned from the API, reducing data transfer size.

Include:

![Fields Include](../../../../assets/data/STACAPI/PostmanExamples/FieldExtensionInclude.png)

Exclude:

![Fields Exclude](../../../../assets/data/STACAPI/PostmanExamples/FieldExtensionExclude.png)

### Sortby Extension

By default, Items are returned by `datetime` descending. Then by `id` ascending.

Sorting by property `eo:cloud_cover` is also supported on the `/search` endpoint:

| Ascending | Descending |
|-----------|-----------|
| ![Sort Asc](../../../../assets/data/STACAPI/PostmanExamples/SortAsc.png) | ![Sort Desc](../../../../assets/data/STACAPI/PostmanExamples/SortDesc.png) |

## Downloading Assets

![Downloading Assets](../../../../assets/data/STACAPI/PostmanExamples/DownloadingAssets.png)

## CloudMasks

![CloudMasks](../../../../assets/data/STACAPI/PostmanExamples/CloudMask.png)
