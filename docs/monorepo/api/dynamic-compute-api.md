---
title: Dynamic Compute API Reference
description: Complete API reference for the Dynamic Compute module including Mosaic and ImageStack classes
keywords:
  - API reference
  - dynamic compute
  - Mosaic
  - ImageStack
  - raster operations
  - geospatial analysis
---

# Dynamic Compute API Reference

This page provides the API reference for the Dynamic Compute module (`earthdaily.earthone.dynamic_compute`).

## Mosaic

`earthdaily.earthone.dynamic_compute.Mosaic`

Class wrapper around mosaic operations.

### Class Methods

- **`Mosaic.from_product_bands(product_id, bands, start_datetime=None, end_datetime=None)`** - Create a new Mosaic from a product ID and band names.
- **`Mosaic.from_image_ids(image_ids, bands)`** - Create a new Mosaic from a list of image IDs.

### Instance Methods

- **`pick_bands(bands)`** - Create a new Mosaic with the specified bands.
- **`unpack_bands(bands)`** - Create a tuple of new single-band Mosaic objects.
- **`concat_bands(other)`** - Create a new Mosaic that stacks bands from this and another Mosaic.
- **`rename_bands(bands)`** - Rename the bands of an array.
- **`compute(aoi)`** - Evaluate this Mosaic for a particular AOI (GeoContext).
- **`visualize(name, map, colormap=None, scales=None, checkerboard=True)`** - Visualize this Mosaic on an ipyleaflet map.
- **`tile_layer(name=None, scales=None, colormap=None)`** - Create a DynamicComputeLayer for this Mosaic.
- **`mask(mask)`** - Apply a mask to the Mosaic.
- **`clip(lo, hi)`** - Bound the Mosaic values between lo and hi.
- **`filled(fill_val)`** - Fill masked values with a specified value.

### Reducers

- **`max(axis)`** - Apply `np.ma.max` over the specified axis.
- **`min(axis)`** - Apply `np.ma.min` over the specified axis.
- **`mean(axis)`** - Apply `np.ma.mean` over the specified axis.
- **`median(axis)`** - Apply `np.ma.median` over the specified axis.
- **`std(axis)`** - Apply `np.ma.std` over the specified axis.
- **`sum(axis)`** - Apply `np.ma.sum` over the specified axis.
- **`argmax(axis)`** - Apply `np.ma.argmax` over the specified axis.
- **`argmin(axis)`** - Apply `np.ma.argmin` over the specified axis.
- **`reduce(reducer, axis='bands')`** - Call a custom reduction function.

### Terrain

- **`slope(resolution_x=None, resolution_y=None)`** - Compute the slope of the mosaic.
- **`aspect(resolution_x=None, resolution_y=None)`** - Compute the aspect of the mosaic.
- **`gradient_x(resolution=None)`** - Compute the E-W gradient.
- **`gradient_y(resolution=None)`** - Compute the N-S gradient.

### Other

- **`update_resampler(resampler)`** - Create a new Mosaic with an updated resampler algorithm.

---

## ImageStack

`earthdaily.earthone.dynamic_compute.ImageStack`

Provides access to time-resolved geospatial data as a stack of images.

### Class Methods

- **`ImageStack.from_product_bands(product_id, bands, start_datetime, end_datetime, predicate_filter=None, sort_by=None, ascending=True)`** - Create a new ImageStack from a product ID and band names.

### Instance Methods

- **`pick_bands(bands)`** - Create a new ImageStack with the specified bands.
- **`unpack_bands(bands)`** - Create a tuple of new single-band ImageStack objects.
- **`concat_bands(other)`** - Create a new ImageStack that stacks bands.
- **`rename_bands(bands)`** - Rename the bands of an array.
- **`compute(aoi)`** - Evaluate this ImageStack for a particular AOI (GeoContext).
- **`filter(pred)`** - Filter images based on image properties (e.g., cloud fraction).
- **`filter_by_id(id_list)`** - Filter images by a list of image IDs.
- **`groupby(grouping_func)`** - Group images by a function over image metadata.
- **`length()`** - Proxy object for the length of the image stack.
- **`mask(mask)`** - Apply a mask to the ImageStack.
- **`clip(lo, hi)`** - Bound values between lo and hi.
- **`filled(fill_val)`** - Fill masked values with a specified value.

### Reducers

- **`max(axis)`** - Apply `np.ma.max` over the specified axis (`"bands"` or `"images"`).
- **`min(axis)`** - Apply `np.ma.min` over the specified axis.
- **`mean(axis)`** - Apply `np.ma.mean` over the specified axis.
- **`median(axis)`** - Apply `np.ma.median` over the specified axis.
- **`std(axis)`** - Apply `np.ma.std` over the specified axis.
- **`sum(axis)`** - Apply `np.ma.sum` over the specified axis.
- **`argmax(axis)`** - Apply `np.ma.argmax` over the specified axis.
- **`argmin(axis)`** - Apply `np.ma.argmin` over the specified axis.
- **`reduce(reducer, axis='images')`** - Perform a custom reduction over images or bands.

### Other

- **`update_resampler(resampler)`** - Create a new ImageStack with an updated resampler algorithm.
