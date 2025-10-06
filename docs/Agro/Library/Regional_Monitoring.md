---
title: Regional Monitoring API
description: Overview of EarthDaily's Regional Monitoring API, including environments, workflows, weather data chain, and integration details.
icon: material/api
status: new
---

# 🌍 Regional Monitoring API

EarthDaily delivers a wide range of **digital agriculture services** through multiple channels:

- Web platforms  
- Reports  
- Datasets  
- APIs  

APIs allow external applications to **access insights and analytics**, expanding their capabilities and enabling seamless integration.

The **EarthDaily API** provides access to **innovative and packaged solutions** that can be easily integrated into your systems:

- ✅ Access **historical data** (satellite archive and weather)  
- ✅ Access **in-season data** and **forecast weather data**  
- ✅ Embed analytics into your platform to **supercharge your application** in the marketplace  

---

## 🧪 API Test Environment

EarthDaily provides credentials for the **API Test Environment** to allow integration and testing.  
> ⚠️ The test environment contains a **limited dataset** and is intended for development purposes only.

---

## 🚀 API Production Environment

Access to the **Production Environment** is provided under a **License Agreement** and requires a valid **user ID**.  

EarthDaily also provides access to a **Service Desk** with incident ticket tracking capabilities for support and troubleshooting.

---

## 🎯 What Is the Regional Monitoring API?

The **Regional Monitoring API** enables organizations to **observe, analyze, and report** on agricultural or environmental conditions across **large geographic areas**.

This capability is essential for businesses and institutions that need **strategic insights at scale**, such as crop monitoring, risk assessment, and market intelligence.

---

### ✅ How It Works
Regional monitoring leverages **satellite imagery**, **remote sensing data**, and **weather analytics** to provide a comprehensive view of crop and environmental conditions. Key features include:

- **Tracking crop development** and vegetation health across entire regions  
- **Analyzing soil moisture, NDVI, and crop masks** to identify trends and anomalies  
- **Comparing multiple datasets** (e.g., weather, vegetation indices) for regional benchmarking  

---

### ✅ Who Benefits?
- **Crop analysts and agribusinesses** assessing crop conditions and yield potential over large territories  
- **Government agencies and insurers** validating production data and monitoring risks  
- **Market intelligence teams** integrating multiple data sources for strategic planning  

---

### ✅ Why It Matters
Regional monitoring provides a **high-level, data-driven perspective** that supports better decision-making, resource allocation, and risk management across wide areas.

---

## 🔄 High-Level Workflow

![workflow](../../assets/agro/regional_monitoring/workflow.png)

1. The **client application** sends a request to the API Service for each analytic to be generated.  
2. The **back-end** processes the request and generates the requested metrics.  
3. The **API Service** returns the response to the client application.  
4. In parallel, the **back-end** tracks all actions for **reporting and invoicing**.  

---

## 🌦 What’s Included in the Weather Chain

### **Forecast Weather Models**
- **ENS model** (ECMWF\*, probabilistic, 20 km resolution, forecast D+14)  
- **GFS model** (NOAA-NCEP\*\*, deterministic, 25 km resolution, forecast D+14)  

---

### **Historical Data**
- Historical data depth from **1990 to 2019** (today minus 15 days)  

---

### **Sliding Reprocessing**
- **D - 3 months**, then **D - 15 days**  
- **ERA-5\*** (ECMWF) historical data integrated at the beginning of each month:
  - Current Month minus 3 months data  
  - Example: On July 31, the last available data is April 30 (3 months delay)  
- **ERA-5T\*** (ECMWF) historical data integrated **day by day** at D-15 days  
- **ENS (ECMWF)** D0 values (pseudo-analysis) stored from D0 to last ERA-5T historical available data (D-15 days)  

---

\* **European Center for Weather Forecasts (ECMWF)**, Reading, UK  
\*\* **National Oceanic and Atmospheric Administration – National Center for Environmental Prediction (USA)**  
\*\*\* The data assimilation system  

![Weather_chaim](../../assets/agro/regional_monitoring/weather_chain.png)
---

## 📊 Parameters, Related Maps, and Graphs

![Parameters](../../assets/agro/regional_monitoring/parameters.png)

---

## 🛠 Data Technical Description

![Description1](../../assets/agro/regional_monitoring/description1.png)
![Description2](../../assets/agro/regional_monitoring/description2.png)

## Agregation 

![Agregation](../../assets/agro/regional_monitoring/agregation.png)

## 🌐 Regional Monitoring Endpoints


| Environment | URL |
|-------------|-----|
| **Test**    | [https://api-pp.geosys-na.net/Agriquest/Geosys.AgriQuest.CropMonitoring.WebApi/v0]|
| **Prod**    | [https://api.geosys-na.net/Agriquest/Geosys.AgriQuest.CropMonitoring.WebApi/v0]|


*N.B. : This section summarizes the three main endpoints needed to use the Regional API. Details on the input/output and the various business rules will be found at the xxxxx section

---

### 🔐 Authentication

All endpoints require secure access via **Identity Server API**, which manages:

- User and application-level authentication  
- Token-based access (OAuth 2.0)  
- Permission scopes to control access to specific data layers or regions

<swagger-ui src="https://api.geosys-na.net/fintech/v1/swagger/v1.0/swagger.json"/>



## 📚 Developer Resources
- [Swagger UI – Production](https://api.geosys-na.net/fintech/v1/swagger/index.html)

---

Need Postman collections or API keys? Reach out to your EarthDaily Agro contact.

