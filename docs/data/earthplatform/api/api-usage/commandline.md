---
title: Command Line Examples
description: Curl command examples for all EarthDaily STAC API endpoints
keywords:
  - curl
  - command line
  - STAC API
  - API examples
  - EarthDaily API
  - REST API
---

# Command Line Examples

The sections below include examples using [curl](https://curl.se/) commands. If a GUI is preferred, these commands can be [imported](https://learning.postman.com/docs/getting-started/importing-and-exporting-data/#importing-with-curl-commands) into [Postman](https://www.postman.com/).

## Collections

Return list of all Collections

```bash
curl --location https://api.earthdaily.com/platform/v1/stac/collections \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>'
```

## Collection

Return specific Collection

```bash
curl --location https://api.earthdaily.com/platform/v1/stac/collections/sentinel-2-l1c \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>'
```

## Items

Return paged Items ordered by datetime descending

```bash
curl --location https://api.earthdaily.com/platform/v1/stac/collections/sentinel-2-l1c/items \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>'
```

## Item

Returns a single Item for a given Collection and Item ID

```bash
curl --location https://api.earthdaily.com/platform/v1/stac/collections/sentinel-2-l1c/items/S2B_MSIL1C_20240422T190009_N0510_R027_T08JNQ_20240422T221641 \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>'
```

## Queryables

Returns the queryable names for the STAC API Item Search using Query Extension

```bash
curl --location https://api.earthdaily.com/platform/v1/stac/collections/landsat-c2l1/queryables \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>'
```

## Search

Implements STAC basic Item search functionality + extensions

```bash
curl --location 'https://api.earthdaily.com/platform/v1/stac/search' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>' \
  --data '{
    "datetime": "2023-01-01T18:50:42.000000Z/2023-02-01T18:50:42.000000Z",
    "collections": ["sentinel-2-l1c","sentinel-2-l2a"],
    "intersects": {
        "coordinates": [
          [
            [-2.226934111129964, 53.375337378064074],
            [-2.226934111129964, 50.0397331432938],
            [3.334960050757161, 50.0397331432938],
            [3.334960050757161, 53.375337378064074],
            [-2.226934111129964, 53.375337378064074]
          ]
        ],
        "type": "Polygon"
    }
  }'
```

### Query Extension via POST Method

!!! note
    EarthPlatform STAC API supports the [Query Extension](https://github.com/stac-api-extensions/query). It currently does not support the Filter Extension.

```bash
curl --location 'https://api.earthdaily.com/platform/v1/stac/search' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>' \
  --data '{
    "limit": 20,
    "collections": ["landsat-c2l2-sr"],
    "query": {
        "view:sun_elevation": {
            "gt": 40,
            "lt": 60
        },
        "eo:cloud_cover": {
            "lt": 10
        }
    }
  }'
```

### Fields Extension

The Fields Extension allows you to specify which fields are returned from the API, reducing data transfer size.

Include specific fields:

```bash
curl --location 'https://api.earthdaily.com/platform/v1/stac/search' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>' \
  --data '{
    "fields": {
      "include": ["id", "properties.datetime", "assets.aot"]
    }
  }'
```

Exclude specific fields:

```bash
curl --location 'https://api.earthdaily.com/platform/v1/stac/search' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>' \
  --data '{
    "fields": {
      "exclude": ["links", "geometry"]
    }
  }'
```

### Sortby Extension

By default, Items are returned by `datetime` descending. Then by `id` ascending.

```bash
curl --location 'https://api.earthdaily.com/platform/v1/stac/search' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>' \
  --data '{
    "sortby": [
        {
            "field": "properties.eo:cloud_cover",
            "direction": "asc"
        }
    ]
  }'
```

## Downloading Assets

```bash
curl --location 'https://api.earthdaily.com/platform/v1/stac/search' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>' \
  --header 'X-Signed-Asset-Urls: true' \
  --data '{
    "limit": 20,
    "collections": ["sentinel-2-l2a-cog-ag-cloud-mask"]
  }'
```

Example response:

```json
"assets": {
    "agriculture-cloud-mask": {
        "href": "s3://earthdaily-eds-edc-skyfox-generic/_PUBLIC/sentinel-2-l2a-cog-ag-cloud-mask/...",
        "alternate": {
            "download": {
                "href": "https://earthdaily-eds-edc-skyfox-generic.s3.amazonaws.com/_PUBLIC/...?AWSAccessKeyId=...&Signature=...&Expires=1694739928"
            }
        }
    }
}
```

## Cloud Masks

```bash
curl --location 'https://api.earthdaily.com/platform/v1/stac/search' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <ACCESS_TOKEN HERE>' \
  --data '{
    "collections": ["sentinel-2-l2a"],
    "datetime":"2022-07-01T00:00:00.000000Z/2022-08-01T00:00:00.000000Z",
    "query": {
        "eda:ag_cloud_mask_available": {
            "eq": true
        }
    }
  }'
```
