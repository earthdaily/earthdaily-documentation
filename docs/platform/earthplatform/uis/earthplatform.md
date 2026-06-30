---
title: EarthPlatform
description: Browse and interact with the EarthDaily image catalog using EarthPlatform
keywords:
  - EarthPlatform
  - image catalog
  - satellite imagery search
  - GeoJSON
  - visualization
  - EarthDaily Console
  - geospatial filtering
---

# EarthPlatform

## Introduction

Customers can access and browse through our image catalog and products through EarthPlatform. In addition to providing useful metadata and details about the listed images, it provides capabilities to interact with them. You can access EarthPlatform [here](https://console.earthdaily.com/platform).

## Search

EarthPlatform has a search panel with various customization options. Once you login with your credentials, the landing page is shown with the search filters and results panel on the left:

| S. No | Label | Description |
|-------|-------|-------------|
| ![One](../../../assets/platform/NumberLabels/One.png) | Search Box | Enter any geographic area like "Vancouver", "Chile" etc to find and focus |
| ![Two](../../../assets/platform/NumberLabels/Two.png) | Rectangle Tool | Select two vertices of the diagonal on the map to form a rectangular area as a geospatial filter |
| ![Three](../../../assets/platform/NumberLabels/Three.png) | Polygon Tool | Select a given area as a geospatial filter on the map by creating vertices with left clicks. Click the first vertex or double-click after the last vertex to complete |
| ![Four](../../../assets/platform/NumberLabels/Four.png) | Input GeoJSON | Click to enter or import a GeoJSON as a geospatial filter |
| ![Five](../../../assets/platform/NumberLabels/Five.png) | Viewport | Select to define the current map extents as a geospatial filter |
| ![Six](../../../assets/platform/NumberLabels/Six.png) | Basic Filters | Select one or more Collections (up to 15) and define a date range |
| ![Seven](../../../assets/platform/NumberLabels/Seven.png) | Advanced Filters | Click to define additional filters based on the selected Collections |
| ![Eight](../../../assets/platform/NumberLabels/Eight.png) | Reset Button | Click to reset all search filters |
| ![Nine](../../../assets/platform/NumberLabels/Nine.png) | Search Button | Click to submit the search |
| ![Ten](../../../assets/platform/NumberLabels/Ten.png) | Results Panel | Area where thumbnails of search results appear |

![EarthPlatform Landing Page - Search Filters and Results](../../../assets/platform/CatalogUI/LandingPageFilters.png)

!!! note
    The Advanced Filters panel expands with additional parameters based on the Collection selected. When there are results returned from the search, you can see the results panel populated with images, along with thumbnails if available. When you hover over a search result, the corresponding footprint will be highlighted in yellow on the map.

![EarthPlatform Filter Panel](../../../assets/platform/CatalogUI/Filter.png)

On the right hand side is the map, where you can define the Area of Interest (AOI) and see the footprints of the search results:

| S. No | Label | Description |
|-------|-------|-------------|
| ![Eleven](../../../assets/platform/NumberLabels/Eleven.png) | App Switcher | Click to switch to another EDA-hosted application |
| ![Twelve](../../../assets/platform/NumberLabels/Twelve.png) | Map Slider | Click to enable the Map Slider to enter image comparison mode |
| ![Thirteen](../../../assets/platform/NumberLabels/Thirteen.png) | Settings | Click to change base map layers, Footprint and Image Opacity |
| ![Fourteen](../../../assets/platform/NumberLabels/Fourteen.png) | AOI Controls | Center on AOI, Hide AOI, Copy AOI, Delete AOI, and show total area of the AOI. Only appears when there is an AOI on the map. |
| ![Fifteen](../../../assets/platform/NumberLabels/Fifteen.png) | Ruler | Click to draw a line and measure the distance between 2 points |
| ![Sixteen](../../../assets/platform/NumberLabels/Sixteen.png) | Bottom Panel | Shows latitude/longitude of current cursor position, zoom level, and scale bar |

![EarthPlatform Landing Page - Map](../../../assets/platform/CatalogUI/LandingPageMap.png)

Below are some images showing how the various controls work.

GeoJSON Viewer and Importer:

![EarthPlatform JSON Viewer](../../../assets/platform/CatalogUI/JSONViewer.png)

Streets and Satellite Views:

| Streets View | Satellite & Streets View |
|--------------|--------------------------|
| ![StreetView](../../../assets/platform/CatalogUI/StreetView.png) | ![SatelliteView](../../../assets/platform/CatalogUI/SatelliteView.png) |

AOI Area Calculation (the example shows the use of the Polygon tool, but the AOI area is displayed regardless of which tool you used to define the AOI):
![EarthPlatform Ruler](../../../assets/platform/CatalogUI/AreaCalculatorPolygon.png)

Ruler:

![EarthPlatform Ruler](../../../assets/platform/CatalogUI/Ruler.png)

## Interacting with the catalog

Once you have search results, you can perform various actions on the images:

| S. No | Label | Description |
|-------|-------|-------------|
| ![Seventeen](../../../assets/platform/NumberLabels/Seventeen.png) | Show Item Properties | Show the Item Properties on the right hand side panel |
| ![Eighteen](../../../assets/platform/NumberLabels/Eighteen.png) | Favorite Item | Tag the image as favorite, then use the toggle button (#26) to show only favorites |
| ![Nineteen](../../../assets/platform/NumberLabels/Nineteen.png) | Fly to Bounds | Zoom in to the image location |
| ![Twenty](../../../assets/platform/NumberLabels/Twenty.png) | Toggle Layer Visibility | Show/Hide the footprint on the map |
| ![TwentyOne](../../../assets/platform/NumberLabels/TwentyOne.png) | View on Map | Render the image on the map |
| ![TwentyTwo](../../../assets/platform/NumberLabels/TwentyTwo.png) | View Visualization Configuration | Toggles the visualization configuration panel to adjust min/max of color bands and gamma values |
| ![TwentyThree](../../../assets/platform/NumberLabels/TwentyThree.png) | Auto adjust Visualization | Auto adjust the image by clipping percentages based on a calculated histogram |
| ![TwentyFour](../../../assets/platform/NumberLabels/TwentyFour.png) | Multi-Select | Allows multi-selecting images for batch actions |
| ![TwentyFive](../../../assets/platform/NumberLabels/TwentyFive.png) | Multi-Select Actions | Actions for multiple images (e.g., 'View all on map') |
| ![TwentySix](../../../assets/platform/NumberLabels/TwentySix.png) | View Favorites Only | Toggle to show only favorited images |

![EarthPlatform Interaction](../../../assets/platform/CatalogUI/CatalogInteraction.png)

Item Properties panel:

![EarthPlatform Item Properties](../../../assets/platform/CatalogUI/ItemProperties.png)

Toggle the Show Full button to see the entire STAC item properties. Under Show Full mode you can also get individual asset URLs and download images by following the "href":

![EarthPlatform Show Full](../../../assets/platform/CatalogUI/ShowFull.png)

Tagging an item as favorite and viewing favorites:

| Favorites | View Favorites |
|-----------|----------------|
| ![Favorites](../../../assets/platform/CatalogUI/Favorites.png) | ![ViewFavorites](../../../assets/platform/CatalogUI/ViewFavourites.png) |

View on Map:

![EarthPlatform View on Map](../../../assets/platform/CatalogUI/MapView.png)

Visualization configuration:

![EarthPlatform Visualization](../../../assets/platform/CatalogUI/Visualization.png)

Auto visualization comparison. The image on the right has its visualization parameters auto-adjusted, while the one on the left uses default values:

![EarthPlatform Auto Visualization](../../../assets/platform/CatalogUI/AutoVisualization.png)

Fly to Bounds:

![EarthPlatform Fly To Bounds](../../../assets/platform/CatalogUI/FlyToBounds.png)

### Map Slider

Compare two images over different dates by using the Map Slider:

| S. No | Label | Description |
|-------|-------|-------------|
| ![TwentySeven](../../../assets/platform/NumberLabels/TwentySeven.png) | Show/Hide Map Slider | Toggle for the Map Slider comparison mode |
| ![TwentyEight](../../../assets/platform/NumberLabels/TwentyEight.png) | Move Image Left | Select the image for the left side of the slider |
| ![TwentyNine](../../../assets/platform/NumberLabels/TwentyNine.png) | Move Image Right | Select the image for the right side of the slider |
| ![Thirty](../../../assets/platform/NumberLabels/Thirty.png) | Slider | The map slider |

![EarthPlatform Map Slider](../../../assets/platform/CatalogUI/MapSlider.png)

Example showing solar panel installation between 2023-10-28 and 2024-01-26:

![EarthPlatform Map Slider Left](../../../assets/platform/CatalogUI/MapSliderLeft.png)

![EarthPlatform Map Slider Right](../../../assets/platform/CatalogUI/MapSliderRight.png)

### Opacity Controls

| S. No | Label | Description |
|-------|-------|-------------|
| ![ThirtyOne](../../../assets/platform/NumberLabels/ThirtyOne.png) | Footprint Opacity | Toggle the opacity/transparency of the footprint |
| ![ThirtyTwo](../../../assets/platform/NumberLabels/ThirtyTwo.png) | Image Opacity | Toggle the opacity/transparency of an image |

![EarthPlatform Image Sliders](../../../assets/platform/CatalogUI/ImageSliders.png)

Image opacity at 0%, 50%, and 100%:

| Image Opacity 0 | Image Opacity 50 | Image Opacity 100 |
|------------------|-------------------|-------------------|
| ![ImageOpacity0](../../../assets/platform/CatalogUI/ImageOpacity0.png) | ![ImageOpacity50](../../../assets/platform/CatalogUI/ImageOpacity50.png) | ![ImageOpacity100](../../../assets/platform/CatalogUI/ImageOpacity100.png) |

Footprint opacity:

| Footprint Opacity High | Footprint Opacity Low |
|------------------------|-----------------------|
| ![FootprintOpacityHigh](../../../assets/platform/CatalogUI/FootprintOpacityHigh.png) | ![FootprintOpacityLow](../../../assets/platform/CatalogUI/FootprintOpacityLow.png) |
