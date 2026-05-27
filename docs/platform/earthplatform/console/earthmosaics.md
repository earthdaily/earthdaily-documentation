---
title: EarthMosaics
description: Create and manage AI-Ready Mosaics with EarthMosaics
keywords:
  - EarthMosaics
  - AI-Ready Mosaics
  - cloud-free imagery
  - mosaic ordering
  - NDVI
  - Sentinel-2
  - geospatial analysis
---

# EarthMosaics

## Introduction

[**EarthMosaics**](https://console.earthdaily.com/mosaics) delivers cloud-free, temporally coherent mosaics with the highest possible geolocation, radiometric quality, enabling users to examine true signals, minimize false positives in change detection, and easily contextualize with other geospatial datasets. From analysing a regional forest to monitoring a mining site, predicting water reservoir levels to measuring melting permafrost, EarthMosaics offers application-specific and customized insights fulfilling unique needs of each use case.

AI Ready Mosaics are complex, costly to produce, and designed to feed directly into ML applications.

[EarthMosaics](https://console.earthdaily.com/mosaics) from EarthDaily Analytics provides you a way to explore and get a free preview and you can also place orders for full resolution Mosaics.

## Getting started with Mosaics

Below is the landing page when you navigate to [EarthMosaics](https://console.earthdaily.com/mosaics):

![WelcomeMosaics](../../../assets/platform/EarthMosaicsUI/WelcometoMosaic.png)

When you are a first time user, you get the Welcome dialog with an option to Get Started.

Pressing `GetStarted` takes you to the New Orders page:

![MosaicsOrderSetup](../../../assets/platform/EarthMosaicsUI/MosaicOrderSetup.png)

| S. No | Label | Description |
|-------|-------|-------------|
| ![One](../../../assets/platform/NumberLabels/One.png) | Launch EarthDailyGPT | Use EarthDailyGPT to assist with generating a mosaic |
| ![Two](../../../assets/platform/NumberLabels/Two.png) | Area of Interest - draw on map | Draw a polygon for your mosaics order (limit < 200,000 km²). Only polygons supported (not multipolygons) |
| ![Three](../../../assets/platform/NumberLabels/Three.png) | Area of Interest - use GeoJSON | Enter an existing GeoJSON instead of drawing (same area limit) |
| ![Four](../../../assets/platform/NumberLabels/Four.png) | Time of Interest | Specify the time of interest |
| ![Five](../../../assets/platform/NumberLabels/Five.png) | Settings | Multiple choices to configure your order |
| ![Six](../../../assets/platform/NumberLabels/Six.png) | Mosaic Name | Enter a name for easy identification |

The AOI defines the geographic extent used to build the mosaic. You can either draw the AOI on the map or provide GeoJSON. To draw, choose Rectangle or Polygon option, then left-click on the map.

![AoI](../../../assets/platform/EarthMosaicsUI/AoI.png)

Once you draw a polygon, the area calculator displays the total area:

| S. No | Label | Description |
|-------|-------|-------------|
| ![Seven](../../../assets/platform/NumberLabels/Seven.png) | Fit Bounds | Bring back focus on the drawn area and fit to viewport |
| ![Eight](../../../assets/platform/NumberLabels/Eight.png) | GeoJSON | Enter or edit the GeoJSON |
| ![Nine](../../../assets/platform/NumberLabels/Nine.png) | Delete | Delete the existing AoI |

![GeoJSON](../../../assets/platform/EarthMosaicsUI/GeoJSON.png)

![ToI](../../../assets/platform/EarthMosaicsUI/ToI.png)

## Mosaic Preview Order

The settings define how your mosaic will be generated:

- **Resolution** — Preview is free, Full is paid. Create a Preview first to verify your settings.
- **Processing type** determines pixel selection:
    - **Best Measurement:** considers cloud, cloud shadow, distance to nearest occlusion, aerosol optical thickness, relative acquisition time, acquisition platform, and smoothness characteristics
    - **Min/Max NDVI (beta):** augments Best Measurement with per-pixel NDVI weighting
    - **Min/Max NBR (beta):** augments Best Measurement with per-pixel NBR weighting
- **Source** — Sentinel-2A only, or combination of Sentinel-2A and Landsat-8/9

![Settings](../../../assets/platform/EarthMosaicsUI/MosaicSettings.png)

After confirming settings and entering a name, submit the order:

![Submit](../../../assets/platform/EarthMosaicsUI/MosaicSubmit.png)

## Mosaic Full Resolution Order

Full Resolution orders are similar to Preview except with an additional payment step.

Preview orders have 2 steps: Configuration and Confirmation.
Full Resolution adds a third step: Quote.

Select "Full" as your Resolution setting:

![FullResOrder](../../../assets/platform/EarthMosaicsUI/MosaicFullResOrder.png)

Confirm the order settings to checkout:

![Checkout](../../../assets/platform/EarthMosaicsUI/MosaicCheckoutQuote.png)

The checkout screen shows the order price:

![Pay](../../../assets/platform/EarthMosaicsUI/Pay.png)

If you have coupons to redeem, enter the coupon code for eligible discounts. Once ready, proceed to pay.

## Managing Mosaics Orders

After placing the order (Preview or Full), you will be redirected to your Dashboard:

![AllOrdersFull](../../../assets/platform/EarthMosaicsUI/MosaicDashboardOrder.png)

Your order will show an "In Progress" state. There is a button to view all Mosaic Orders on EarthPlatform:

![AllOrders](../../../assets/platform/EarthMosaicsUI/MosaicAllOrdersList.png)

The Order ID can be found in your Account Information page under "My Orders":

![MyOrders](../../../assets/platform/EarthMosaicsUI/AccountParentOrder.png)

Click the Order Id link for more details:

![MyOrders Details](../../../assets/platform/EarthMosaicsUI/AccountOrderDetails.png)

Once processed successfully, the state changes to "Completed" with additional options:

![OrdersMgmt](../../../assets/platform/EarthMosaicsUI/OrderManagement.png)

| S. No | Label | Description |
|-------|-------|-------------|
| ![Ten](../../../assets/platform/NumberLabels/Ten.png) | Copy | Copy the order to reuse settings or make minor modifications |
| ![Eleven](../../../assets/platform/NumberLabels/Eleven.png) | Download | Download your product (Preview or Full) |
| ![Twelve](../../../assets/platform/NumberLabels/Twelve.png) | View | View the product in EarthPlatform |

The [EarthPlatform](earthplatform.md) visualizer opens in a new tab:

![Visualizer](../../../assets/platform/EarthMosaicsUI/MosaicVisualizer.png)
