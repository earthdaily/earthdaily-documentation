---
title: Key Features
description: Overview of the EarthOne Python stack — Catalog, Compute, and Dynamic Compute
keywords:
  - EarthOne Python
  - Catalog API
  - Compute API
  - Dynamic Compute
  - geospatial data
  - raster data
  - vector data
  - pip install
---

# Key Features of the EarthOne Platform

## An overview of the EarthOne Python stack

> **Note:** To get started, visit the [Installation article](../platform-apis/installation.md) and install the Python client with:
>
> ```
> pip install earthdaily-earthone
> ```

### Create, manage, search, and visualize geospatial data with Catalog

The [EarthOne Catalog API](https://docs.descarteslabs.com/descarteslabs/catalog/readme.html) serves as a comprehensive repository for geo-referenced data. It offers access to a vast collection of EarthDaily-provided geospatial data, amounting to approximately 40 petabytes. Additionally, users can augment the Catalog with their own data sources and store any derivative data.

One of the Catalog's main advantages is its simplification of access to spatiotemporal raster data. This enables customers to swiftly search for and extract the most pertinent data for their specific needs. The Catalog API provides a high-throughput data feed and storage mechanism which, when paired with EarthDaily-provided compute capabilities, powers global-scale modeling for the world's most complex problems.

Furthermore, the Catalog offers specialized storage and access to geo-referenced [Vector](https://docs.descarteslabs.com/descarteslabs/vector/readme.html) data. It also provides flexible file storage for model weights, results, and other types of data. Each dataset within the Catalog can be independently georeferenced, managed, searched, and shared, making it an advanced collaboration platform for geospatial projects.

### Leverage the power of scalable batch computing in EarthDaily's cloud infrastructure

When you need to deploy a model across a wide area, the [Compute](https://docs.descarteslabs.com/descarteslabs/compute/readme.html) service offers users the ability to utilize cloud computing infrastructure to parallelize and run code on a large scale. Users' Python code is packaged and executed on nodes that are hosted within EarthDaily's cloud infrastructure. This provides a flexible foundation for running complex machine learning and artificial intelligence algorithms on Catalog data.

### Dynamic Compute — our powerful on-demand geospatial analysis engine

[Dynamic Compute](https://docs.descarteslabs.com/api/dynamic-compute.html) allows users to focus on their specific problem rather than getting caught up in the details of the data. It provides users with a live-updating interactive map that displays their analysis. Users can combine different operations on Catalog data and add them to the map. These operations are computed as the user explores their area of interest on the map. This interactive approach allows users to develop analyses without needing to know specific geographic coordinates or deal with the complexities of the dataset.

> **Note:** Dynamic Compute is a separate Python package, install via:
>
> ```
> pip install earthdaily-earthone-dynamic-compute
> ```

### API Documentation and Guides

To learn more about the Python APIs, you can refer to the comprehensive API documentation available at [docs.earthone.earthdaily.com](https://docs.earthone.earthdaily.com). Additionally, EarthDaily provides detailed Example Notebooks [available publicly on GitHub](https://github.com/earthdaily/earthone-example-notebooks).
