---
title: earthone-python Package
description: Python client library for EarthDaily EarthOne platform APIs
keywords:
  - earthdaily-earthone
  - Python client
  - Catalog API
  - Compute API
  - Vector API
  - package structure
  - quick start
---

# earthone-python

`earthdaily-earthone` is the official Python client for the [EarthDaily EarthOne platform](https://github.com/earthdaily/earthone-python). It provides programmatic access to the Catalog, Compute, and Vector APIs.

## Installation

```bash
pip install earthdaily-earthone
```

## Package Structure

| Module | Description |
|--------|-------------|
| [**Auth**](auth.md) | Authentication and token management |
| [**Catalog**](catalog.md) | Catalog client for raster data discovery and management |
| [**Compute**](compute.md) | Compute client for running functions and jobs |
| [**Vector**](vector.md) | Vector client for vector data operations |
| [**Config**](config.md) | Configuration and environment management |
| [**Exceptions**](exceptions.md) | Custom exception hierarchy |

## Quick Start

```python
from earthdaily.earthone import auth, catalog, select_env

# Select environment
select_env("production")

# Authenticate
a = auth.Auth()

# Access the Catalog
client = catalog.CatalogClient(auth=a)
products = client.get_products()
```

## Top-level Exports

::: earthdaily.earthone
    options:
      show_root_heading: false
      members:
        - auth
        - catalog
        - compute
        - config
        - exceptions
        - geo
        - utils
        - vector
        - select_env
        - get_settings
      show_source: false
      heading_level: 3
