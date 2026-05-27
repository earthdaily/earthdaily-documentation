---
title: Catalog API
description: Introduction to the EarthOne Catalog API — Products, Images, ImageCollections, Bands, and Blobs
keywords:
  - Catalog API
  - Products
  - Images
  - ImageCollection
  - Bands
  - Blobs
  - raster data
  - geospatial search
---

# EarthOne Catalog API

## An introduction to the EarthOne Catalog API and its key concepts, classes, and methods

### Overview

The [EarthOne Catalog API](https://docs.earthone.earthdaily.com/descarteslabs/catalog/readme.html) is a search and retrieval service designed for extremely high throughput access to raster image data. This article provides an overview of the base classes and methods in the Catalog API to get you up and running with the platform and assumes you have already installed and authenticated the EarthOne client on your Python environment.

Please visit the [Catalog Guide](https://docs.earthone.earthdaily.com/guides/catalog.html) for a more in-depth primer on the Catalog methods.

This document gives a high-level introduction to the Catalog API. For more detailed, practically applied tutorial notebooks please reference the [Example Notebooks](https://github.com/earthdaily/earthone-example-notebooks/) on GitHub or install them by running:

```
git clone https://github.com/earthdaily/earthone-example-notebooks.git
```

### Common Objects

#### Products

The core class within the Catalog raster data model is the [Product](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/product.html#descarteslabs.catalog.Product). A Product is a collection of image data with the same band information stored as pixels. Typically, Products correspond to a single satellite platform, such as [Sentinel-2](https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2), but more specifically a collection of image data with the same processing applied such as [Sentinel-2 L2A](https://sentiwiki.copernicus.eu/web/s2-processing).

Products are referenced by their *unique* IDs. In the case of Sentinel-2 L2A, the EarthOne core Product ID is `esa:sentinel-2:l2a:c1:v1`. There are two types of Products: **Core** and **Personal**. Core Products are those maintained by EarthDaily and Personal Products are those owned and shared by you, the user.

You can access a Product through the API via the [Product.get()](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/product.html#descarteslabs.catalog.Product.get) call:

```python
from earthdaily.earthone.catalog import Product

s2_product = Product.get("esa:sentinel-2:l2a:c1:v1")
s2_product
```

```
Product: Sentinel-2 L2A Collection 1
  id: esa:sentinel-2:l2a:c1:v1
  created: Wed Jan 17 18:58:54 2024
```

> **Note:** Search and visualize which data Products you have available to you, and retrieve their IDs, from [Explorer](https://app.earthone.earthdaily.com/explorer).

#### Images

Each Product stored in the Catalog contains a series of individual [Images](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.Image), which themselves represent raster data of any number of dimensions, or bands. Beyond simply storing the pixel data, Images also have several useful attributes for filtering, intersecting, and searching, such as:

- [geometry](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.Image.geometry) — outline of the scene the Image represents
- [cloud_fraction](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.Image.cloud_fraction) — common for optical data
- several datetime fields including [acquired](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.Image.acquired), [created](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.Image.created), and [modified](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.Image.modified)
- [extra_properties](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.Image.extra_properties) — a generic Python data dictionary

#### ImageCollections

When dealing with Images, we typically define a series of filters on a Product to identify a spatiotemporal subset of imagery, or an [ImageCollection](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/image.html#descarteslabs.catalog.ImageCollection). ImageCollections hold Images, as well as the common methods for loading and interrogating their underlying pixel data.

A typical spatiotemporal filter to retrieve an ImageCollection takes a geometry, a start, and end date to filter a Product's imagery through its [properties](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/search.html#descarteslabs.catalog.properties):

```python
from earthdaily.earthone.catalog import properties as p
from shapely import wkt

wkt_str = 'POLYGON ((-74.03 40.70, -73.91 40.70, -73.91 40.79, -74.03 40.79, -74.03 40.70))'
geom = wkt.loads(wkt_str)

start = '2024-01-01'
end = '2024-05-01'

image_col = (
     s2_product.images()
    .intersects(geom)
    .filter(start < p.acquired < end)
    .filter(p.cloud_fraction < 0.3)
).collect()
image_col
```

```
ImageCollection of 16 images
  * Dates: Jan 02, 2024 to Apr 29, 2024
  * Products: esa:sentinel-2:l2a:c1:v1: 16
```

#### Bands

All Images within a Product must contain the same [Bands](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html), otherwise referenced as *channels*. All Bands, regardless of their type, contain a:

- **Name**, which must be unique for each Product (Required)
- **ID**, automatically generated as Product ID + Band Name
- [Data Type](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/types.html#descarteslabs.catalog.DataType) for the pixel values in each band (Required)
- [Data Range](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.GenericBand.data_range), the range of pixel values for each band (Required)
- Spatial [Resolution](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/types.html#descarteslabs.catalog.Resolution) (Required)
- A valid [NoData](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.GenericBand.nodata) value representing missing or masked out data (Required)
- [Band Index](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.GenericBand.band_index), corresponding to the index of each band to the source data (Required)
- [File Index](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.GenericBand.file_index), corresponding to the index of each band's file in the source data (Required)

There are several subtypes of Bands within the Catalog API:

**Spectral Bands**

A [SpectralBand](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.SpectralBand) represents a range of wavelengths on the electromagnetic spectrum. Spectral Bands typically also contain [Physical Range](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.SpectralBand.physical_range) and Unit, as well as Wavelength [Min](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.SpectralBand.wavelength_nm_min), [Max](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.SpectralBand.wavelength_nm_max), [Center](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.SpectralBand.wavelength_nm_center), and [FWHM](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.SpectralBand.wavelength_nm_fwhm) values in nanometers.

**Microwave Bands**

A [MicrowaveBand](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.MicrowaveBand) contains data on the microwave spectrum, typically for SAR or passive radar sensors, with unique attributes for [Frequency](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.MicrowaveBand.frequency) (GHz), [Bandwidth](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.MicrowaveBand.bandwidth) (MHz), and Physical Range.

**Classified Bands**

A [ClassBand](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.ClassBand) is generally used for finite values that may or may not be continuous, such as the results of a Land Use/Land Classification model. Typically these bands also contain a [Colormap](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.ClassBand.colormap) and [Class Labels](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.ClassBand.class_labels).

**Mask Bands**

[MaskBands](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.MaskBand) are binary bands frequently used to mask out portions of an image (values: 0 or 1).

**Generic Bands**

Any other data that does not fall within one of the predefined band models can be stored as a [GenericBand](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/band.html#descarteslabs.catalog.GenericBand).

#### Blobs

The EarthOne Catalog API also supports arbitrary data storage and access through the [Blob](https://docs.earthone.earthdaily.com/descarteslabs/catalog/docs/blob.html) class. Blobs can be any type of data — whether stored in-memory or any file stored on disk. Typical use cases include storing pre-trained model weights files for inference through [Batch Compute](https://docs.earthone.earthdaily.com/descarteslabs/compute/readme.html) and retrieving the results of a completed [Job](https://docs.earthone.earthdaily.com/descarteslabs/compute/readme.html#descarteslabs.compute.Job).

### Common Concepts

#### Quotas and Limits

The Catalog API is designed for extremely high rates of search and retrieval of the above defined objects. Commonly accessed from asynchronous [Batch Compute](https://docs.earthone.earthdaily.com/descarteslabs/compute/readme.html) nodes, these limits are typically on the order of thousands of queries per minute. Please reference the [Quotas & Limits Documentation page](https://docs.earthone.earthdaily.com/guides/quota.html) for more detailed information.
