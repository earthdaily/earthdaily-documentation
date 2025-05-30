---
title: Parametric Insurance Data Pipeline
description: Nullam urna elit, malesuada eget finibus ut, ac tortor. 
icon: material/api
status: new
---

# Parametric Insurance Data Service

Welcome to the future of agricultural risk management.

---

## 🌾 Value Proposition

Incorporating **parametric insurance** into your agricultural portfolio provides **diversification**, **operational simplicity**, and **new revenue streams**. Yet, insurers often face major hurdles:

- **Data limitations** – especially for environmental variables  
- **Curation complexity** – vegetation data must match land use & crop type  
- **Long historical records** – essential for strike-point calibration  

**EarthDaily Analytics** solves these challenges with a scalable, data-rich platform. Our **Parametric Data API** unlocks over a decade of high-quality environmental, meteorological, soil, and crop-specific vegetation index data, enabling insurers to launch parametric products with confidence.

---

## 🚜 Key Challenges Solved

- ✅ High-quality agronomic data for differentiated products  
- ✅ Affordable, accurate yield loss proxies  
- ✅ Harmonized, long-term historical data records  
- ✅ Independent validation for payout triggers  
- ✅ Support for novel insurance unit creation

---

## 🛠 Product Overview

**Delivery Method:** REST API  
**Supported Geometries:**
- Pre-Defined Units: Counties, Municipalities, Agricultural Zones  
- Custom Units: User-supplied geometries processed by our team  

---

## 📊 Available Parameters

| **Parameter**       | **Record**      | **Regions**                                                        | **Description**                                                                 |
|---------------------|------------------|----------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Crop NDVI           | 2008–Current     | Corn & Soy (Brazil, USA), Pasture (USA, Brazil, Mexico, etc.)       | NDVI masked by crop type and aggregated by insurance unit. High-quality masks. |
| Cropland NDVI       | 2003–Current     | Global                                                               | NDVI for all cropland areas.                                                   |
| Vegetation NDVI     | 2003–Current     | Global                                                               | NDVI for general vegetation.                                                   |
| Precipitation       | 1990–Current     | Global                                                               | Daily totals from ERA5 (30km) & CHIRPS (6km).                                  |
| Soil Moisture       | 1990–Current     | Global                                                               | Daily values from ERA5 Land (9km).                                             |
| Temperature         | 1990–Current     | Global                                                               | Max/Min air temperatures from ERA5 (30km).                                     |

---

## 🗺️ Data Coverage

The following image highlights regional data availability for key NDVI and meteorological parameters:

![Data Coverage Table](/docs/assets/Agro/Data_coverage.png)

---

## 🧰 Documentation & Tools

- 📌 [**Swagger UI**](https://api-dev-test.geosys.com/parametric-insurance/docs) – Interactive API testing  
- 📌 **Postman Collection** – Downloadable Postman Example  
- 📌 [**SandBox**](https://api-dev-test.geosys.com/parametric-insurance/ui) – Interactive Web user interface  

---

## 🔗 Get Started

Launch your parametric product today with EarthDaily’s trusted, validated datasets and API-first delivery.

[Contact Us](#) to schedule a demo or get API access.
