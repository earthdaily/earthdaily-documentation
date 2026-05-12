---
title: Ternary Plot
description: "Create ternary RGB plots from spectral band ratios in Marigold to highlight mineral groups and support mineral exploration interpretation."
keywords:
  - ternary plot
  - band ratio
  - mineral indices
  - RGB composite
  - spectral analysis
  - mineral mapping
---

## Ternary plot

**Ternary plots** are RGB maps of spectral band ratios, which take advantage of
known absorption spectra to highlight mineral groups. The ternary plot takes
three band ratios and assigns them to red, green, and blue so mineral species
highlighted by ratio one will stand out in red, ratio two in green, and ratio
three in blue.

**Usage:**

- Click **Band algebra** in the **Processing toolbox**, then click **Mineral
  indices**.
- Select the layer you want to derive mineral indices from in the **Product**
  dropdown menu.
- Choose three indices you'd like to highlight in your ternary plot.
- Enter text in the **Output layer name** field to name your ternary plot.
- Click the **Calculate indices** button to create your ternary plot.
- If your layer looks washed out, go to the **Raster layers** menu and click the
  settings icon ( | ) for your ternary plot.
- Assign each mineral group to the color you want using the **Red**, **Green**,
  and **Blue** dropdown menus.
- Click **Calculate histograms** to see the distribution of values in each band
  within the current viewport.
- Enter numbers in the **Min** and **Max** fields to ensure that the minimum and
  maximum values for each color fall within the following ranges: 1.9--2.2 for
  Red, 1.0--1.5 for Green, and 0.9--1.1 for Blue.
- Click the **Apply** button.

**Tips:**

- All band ratios have non-zero values. So even if your area of interest doesn't
  contain a particular mineral group, the ternary layer may give you the
  impression that it is present. This is where user knowledge of the site is
  important.

--8<-- "snippets/contact-footer.md"
