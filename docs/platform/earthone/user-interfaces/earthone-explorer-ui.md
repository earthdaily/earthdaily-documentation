---
title: Explorer UI
description: Guide to the EarthOne Explorer UI — search, visualize, and manage geospatial data products
keywords:
  - Explorer UI
  - data visualization
  - geospatial search
  - satellite imagery
  - data products
  - cloud fraction filter
  - interactive map
---

# EarthOne Explorer UI

## An Overview of the EarthOne Explorer UI

### What is Explorer?

[EarthOne Explorer](https://earthone.earthdaily.com/explorer) is your first stop in discovering what geospatial data you have available to you — an interactive web mapping interface with a familiar GIS-style look and feel.

When you first log into Explorer, you will be dropped into an empty map view:

![Explorer empty map view](../../../assets/platform/earthone/ExplorerEmptyView.png)

### Finding Data Sources

To search and add new data to your Explorer viewport, click **Add a new Layer** in the top left of the application:

![Add a new Layer button](../../../assets/platform/earthone/AddLayer.png)

This will bring up a tabular view of data sources, or Products. You can toggle between **Core Products**, datasets maintained by EarthDaily, or **My Products**, data sources owned and maintained by you and your organization

![Core Products view](../../../assets/platform/earthone/CoreAllMyProducts.png)


Note that raster data sources are denoted by the image symbol, while vector data sources by a vector symbol.

### Product Metadata

To search for a particular data source, you can type the product name or keyword into the search bar.

For example, "Sentinel-2" brings up the various processing levels of Sentinel-2 data available on the EarthOne Catalog. Note the accompanying metadata such as:

- Description
- Temporal acquisition information
- Spatial resolution(s)
- Bands

![Sentinel-2 product metadata](../../../assets/platform/earthone/Sentinel2ProductDesc.png)

Note the basic scene acquisition info is located at the bottom of the description page:

![Sentinel-2 product specificiations](../../../assets/platform/earthone/ProductSpecs.png)

You can also view the expanded Band metadata in its own tab:

![Band metadata tab](../../../assets/platform/earthone/BandsView.png)

### Adding Data to the Map

By clicking **Add to Map** from the Product view, this will add the layer in question to the Explorer interactive web map:

![Add to Map button](../../../assets/platform/earthone/AddToMap.png)

![Layer added to map](../../../assets/platform/earthone/MapView.png)

*You can add as many data sources into your Explorer viewport as you'd like. This also works for vector layers!*

### Working with Imagery in Explorer

By default, Explorer will try to set the date range to the latest available imagery. You can change the visualized date range and inspect available coverage through the General Settings dialog and enabling the Coverage Chart option:

![General Settings and Coverage Chart](../../../assets/platform/earthone/CoverageChart.png)

#### My Viewport is Cloudy — now what?

A common filter to apply to temporal stacks of imagery is by cloud fraction. Explorer enables basic image filtering wherever that property is available, such as in Sentinel-2:

![Cloud fraction filter](../../../assets/platform/earthone/CloudFilter.png)

### Image Metadata

Clicking on an individual image, outlined in different colors per layer, will bring up the image properties:

![Image properties panel](../../../assets/platform/earthone/ImageMetadata.png)

### Visualization Options

Expanding the Bands dropdown will bring the option to visualize single-band with a specified colormap, or to create false-color RGB composites:

![Bands visualization options](../../../assets/platform/earthone/FalseColor.png)
