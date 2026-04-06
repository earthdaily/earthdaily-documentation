---
title: Explorer
description: Search, visualize, and manage geospatial data products using the EarthOne Explorer web interface
keywords:
  - Explorer
  - data visualization
  - map viewer
  - satellite imagery
  - product search
  - web interface
---

# Explorer

Our [Explorer](https://earthone.earthdaily.com/explorer) interface
allows users to search and visualize data products available on the
Platform. Utilizing Explorer is a great way to become familiar with data
products and their metadata. It also allows users to manage their own
datasets. All raster products uniquely available or owned by a user are
shown in Explorer.

![Explorer Empty Page](static_images/empty-explorer.png)

## View Product Details

Clicking on "Add layer" will open up the Datasets view. Here the user
can see all available data Products, you have the option to toggle
between "Core products" as well as "My products". Clicking on a layer's
entry will open a dedicated page that shows all the associated metadata
of the product. Here is the page for `Sentinel-2 L2A`, for example. One
of the first things to point out is the Product ID. This ID is used to
search for imagery programatically in the Python client.

![Sentinel-2 L2A Metadata View](static_images/sentinel-2-l2a-dataset-page.png)

The product's band information is also displayed here, including if they
are native to the platform or sensor. All associated metadata about the
bands are listed as well, in terms of band type, data type and a short
description of the band. Clicking a band provides more information
specific to that band. It has important information such as spatial
resolution (resolution, resolution_unit), processing level
(processing_level), and the range of the data (data_range).

![Sentinel-2 L2A Bands View](static_images/sentinel-2-l2a-bands-page.png)

## Product Extent

For each product, the number of scenes available is coveniently plotted
by date toward the bottom of the product details panel.

## Adding Data to the Map

Clicking "Add to Map" from a layer's dataset view will add that
specified layer to the Explorer map viewport.

![Sentinel-2 L2A imagery](static_images/explorer-w-cloudy-sentinel-2.png)

## Layer Opacity

Use the opacity slider beside the desired layer's name to adjust its
opacity.

![Opacity Slider](static_images/opacity-slider.png)

## Image Outlines

To toggle on and off Image outlines, click the "Metadata grid
visibility" button.

![Opacity Slider](static_images/outline-visibility.png)

## Image Feature Metadata

To view a particular Image's metadata attributes, such as Image ID,
acquired date, and cloud fraction, click on the grid cell with Metadata
grid visibility toggled on.

![Image Metadata](static_images/image-metadata.png)

## Date Range Selector

Sentinel-2 L2A has an incredible temporal resolution. To browse datasets
temporally, use the Date Range selector. Expand "General Settings" to
change the mosaicked date range in the viewport.

![Changing Date Ranges](static_images/date-range-selector.png)

## Cloud Fraction Slider

Some Products, such as Sentinel-2 L2A, store `cloud_fraction` as an
Image metadata attribute. Under "General Settings" the user can omit
Images from the visualized mosaic that have a specified cloud fraction.

![Changing Cloud Fraction](static_images/cloud-fraction.png)

## Explore Band combinations

In the "Settings" view click the dropdown labeled "Bands". Here the user
can specify RGB or Single Band to visualize different combinations, such
as a False Color Composite (NIR to Red, Red to Green, and Green to Blue)

![Changing Band Combinations](static_images/false-color-composite.png)

## Feature Metadata

To find the complete metadata associated with a feature, select the
comment box icon in the top right hand corner of the layer window and
click on an image to view its metadata.

## Drawing vectors

Users can add, load, and download point, line, and polygon vector
features to your Explorer window. To access these tools, click the
"Analyze" tab to draw and upload simple GeoJSON Feature Collections.

![Drawing Tools](static_images/drawing-tools.png)

## Sharing Explorer Links

In the top left hand corner of the Explorer window find the Share URL
button. To get the Shareable Explorer URL click this button. This
Explorer link will maintain the layers loaded, layer configurations, and
zoom level and context such as
[this](https://earthone.earthdaily.com/explorer?id=49aece60-8713-4a71-8422-7d608db3abab).
