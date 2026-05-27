---
title: API Details and Limits
description: Best practices for performant STAC API queries and API throttling limits
keywords:
  - STAC API
  - query optimization
  - API throttling
  - rate limiting
  - signed URLs
  - EarthDaily API
  - performance best practices
---

# Performant Query Best Practices

- [Specify Collections](#specify-collections)
- [Datetime Range](#datetime-range)
- [Field Extensions](#use-fields-extension)
- [Signed URLs](#only-request-signed-urls-when-needed)
- [ID Batching](#id-batching)
- [API Throttling](#api-throttling)

## Specify collections

Limit the query to only the collections you need. The STAC API uses a database architecture partitioned by collection_id. The more collections that are specified in the query, the more database tables will have to be scanned.

In cases where you are querying multiple collections and paging through thousands of results, the database is often having to discard matches to fit in the paging limit. It can often be more performant to run concurrent queries with individual collections.

## Datetime Range

The narrower the datetime range specified in your query, the fewer the number of results will need to be scanned. This is especially true for the following marketing tier collections, which are sub-partitioned by year at the database level.

- landsat-c2l1
- landsat-c2l2-sr
- landsat-c2l2-st
- sentinel-1-grd
- sentinel-1-rtc
- sentinel-2-l1c
- sentinel-2-l2a
- venus-l2a

## Use fields extension

Using the fields extension to only get the fields you need can result in dramatic reductions in database network traffic, and network traffic between you and the API.

## Only request Signed URLs when needed

Signing asset URLs has a performance impact. For collections with high numbers of assets, this additional latency can be multiple seconds. It's important to also note that Presigned URL expiry time is 12 hours.

## ID Batching

When trying to get multiple items by id, you can likely get better performance by batching requests with multiple values in ids.

Similarly, when searching for values by properties values, the `in_` query support can be used.

## API Throttling

By default, each EDS account is limited to 30 concurrent active HTTP requests to the STAC API. Requests which start to exceed this limit will be rejected with an HTTP 429 (Too Many Requests) status code.
