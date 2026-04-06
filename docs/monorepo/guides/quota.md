---
title: Quotas and Limits
description: API rate limits, compute time limits, and usage quotas for the EarthOne Platform services
keywords:
  - quotas
  - rate limits
  - usage limits
  - API limits
  - compute limits
---

# Quotas & Limits

Limits and quotas are tied to your user account and apply to all
requests you make.

Various limits and quotas apply to each service and operation. The most
common types of limits are Rate Limits and Usage Quotas.

**Rate limits** are used to prevent overloading the EarthOne Platform
with too many concurrent requests. Rate limits are specified as
`number of requests/unit of time`.

**Compute time limits** are used to prevent overloading the EarthOne
Platform with too many computationally intensive requests. The amount of
computation resources required to return the results of a search request
vary greatly based on the search parameters, and similarly with
rastering requests. If too many complex requests are sent to our
platform within a designated time frame by a single user, the service
will return a `RateLimitExceeded` error. The values of these limits are
expressed as `number of seconds of compute time/unit of time` and
represent aggregated usage across all queries in the unit of time.

**Usage quotas** keep track of how much you use the EarthOne Platform
and prevent you from accessing the platform after your quota has been
reached. Each service measures usage differently, see below for details
on how usage is measured and limited. Usage quotas are typically reset
monthly. Contact [Support](https://earthone.earthdaily.com/support) for
help with usage quotas.

## Catalog

These limits apply to the `Catalog`
client.

### Rate limits

Band operations

- Create a new band - **1000/minute**
- Change a band - **1000/minute**
- Delete a band - **1000/minute**
- Get a band - **20,000/minute**
- Search bands - **40,000/minute**

Image operations

- Create a new image - **20,000/minute**
- Change an image - **20,000/minute**
- Delete an image - **1000/minute**
- Get an image - **20,000/minute**
- Search images - **10,000/minute** (note: these requests are also
  limited by query time)
- Get image summary statistics - **120/minute** (note: these requests
  are also limited by query time)
- Upload an image file or `ndarray` - **20,000/minute**
- Get image upload task status - **1000/minute**

Product operations

- Create a new product - **1000/minute**
- Change a product - **1000/minute**
- Delete a product - **1000/minute**
- Get a product - **20,000/minute**
- Search products - **10,000/minute**
- Delete all related objects - **120/minute**
- Update permissions for all related objects - **120/minute**
- Retrieve the status for the above operations - **1000/minute**

## Compute

These limits apply to the `Compute`
client.

### General limitations

When creating or calling a `Function`

- Maximum concurrency for `Function` invocations - **1000**
- Maximum function return payload - **1MB**

CPU & Memory Configurations

| CPU value | Memory                                   |
|-----------|------------------------------------------|
| 0.25      | 0.5GB, 1GB, 2GB                          |
| 0.5       | 1GB, 2GB, 3GB, 4GB                       |
| 1         | 1GB, 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB   |
| 2         | Between 4GB and 16GB in 1GB increments   |
| 4         | Between 8GB and 30GB in 1GB increments   |
| 8         | Between 16GB and 60GB in 4GB increments  |
| 16        | Between 32GB and 120GB in 8GB increments |

## Vector

These limits apply to the `Vector` client.

### Rate limits

Table operations

- Create a new table - **1000/minute**
- Change a table - **1000/minute**
- Delete a table - **1000/minute**
- Get a table - **1000/minute**
- Search tables - **1000/minute**
- Join tables - **1000/minute**

Feature operations

- Create a new feature - **1000/minute**
- Change a feature - **1000/minute**
- Delete a feature - **1000/minute**
- Get a feature - **1000/minute**
- Search features - **1000/minute**
- Get feature statistics - **1000/minute**
