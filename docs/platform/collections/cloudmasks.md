---
title: EDA Cloud Masks
description: EarthDaily's accurate cloud masking for Sentinel-2 and Landsat
keywords:
  - cloud mask
  - cloud detection
  - Sentinel-2 cloud mask
  - Landsat cloud mask
  - Auto Clear Mask
  - pixel compositing
  - CloudSEN12
---

# Cloud Masking

[EDA's Accurate Cloud Masking](https://earthdailyagro.com/spend-less-data-scientists-time-cleaning-data-high-quality-cloud-masks-for-sentinel2-landsat-and-others-available-today/) has been shown to be more accurate than current open data standard processing, which improves ML applications and the pixel compositing process for mosaics.

The accuracy of the EarthDaily Agro cloud mask is higher than the cloud mask of other providers, allowing for a reduction in under-detection and keeping a high quality on cloud over-detection to not miss clear areas.

| Cloud Mask Provider | Over-Detection | Under-Detection |
|:-------------------:|:--------------:|:---------------:|
| EDA's Cloud Masks | 1.65% | 3.85% |
| Fmask 4 (Matlab) | 0.21% | 27.18% |
| Fmask (Python) | 1.12% | 26.6% |
| ESA | 0.97% | 42.1% |

EDA's Auto Clear Mask (ACM) improves the detection and the efficiency of clouds in Sentinel-2, Landsat 8, and Landsat 9.

| Mosaics with ESA's Cloud Mask | RGB Image of Cloud Area | Mosaics with EDA's Cloud Masks |
|:-----------------------------:|:-----------------------:|:------------------------------:|
| ![ESA Cloud Mask](../../assets/platform/ProductImages/ESA_Cloud_Mask.png) | ![RGB Data](../../assets/platform/ProductImages/RGB_Cloud_Mask.png) | ![EDA Cloud Mask](../../assets/platform/ProductImages/EDA_Cloud_Mask.png) |

## Why do Cloud Masks Matter?

Under-Detected Cloud Masks lead to the inclusion of pixels that are not representative of the ground measurement a mosaic is seeking to construct. This can cause various artifacts within the mosaicing process which are avoided as much as possible, except where there is extremely limited data. In general the larger the Time Range of Interest, the more likely getting cloud-free measurements is.

| Pixel Halo Effect from Poor Cloud Masks | Challenged Pixel Balancing Example |
|:----------------------------------------:|:----------------------------------:|
| ![Cloud Halos](../../assets/platform/ProductImages/CloudHalos.png) | ![Pixel Selection](../../assets/platform/ProductImages/PixelSelection.png) |
| Mosaics produced with undetected cloud masks for mosaic construction. | Mosaics produced to demonstrate the inconsistency made worse with inadequate cloud masks. |

## References

EDA's cloud masking technology is built off of the [CloudSEN12](https://cloudsen12.github.io/) datasources.
