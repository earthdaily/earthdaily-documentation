---
title: Mineral Map
description: "Create classified mineral maps in Marigold by combining SAM results, mineral indices, and other indicator layers into a single output layer."
keywords:
  - mineral map
  - classified layer
  - mineral indices
  - SAM results
  - mineral classification
  - Marigold
---

## Mineral map

The **Mineral map creator** tool is used to generate a classified layer from
mineral indicator layers, such as [SAM](sam.md) results or computed
[mineral indices](mineral-indices.md). By combining multiple layers, you can
easily create a single map that shows all of the minerals of interest within
your AOI.

### **Usage**

The mineral map creator dialog allows you to choose a layer, band, and clip
value from all available raster layers and bands in your project, and give a
name to each one. Click `Add layer` to add more classes to the output map, and
click `Create map` to create the final output layer. The output layer will be a
classified layer corresponding to each of the input layers and clipping values.

<!-- prettier-ignore-start -->

!!! note
    If one pixel in the output map can fall into multiple defined classes, the rule
    at the topmost layer in the list will be used.

<!-- prettier-ignore-end -->

--8<-- "snippets/contact-footer.md"
