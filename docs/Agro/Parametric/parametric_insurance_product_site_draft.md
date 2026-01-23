---
title: Parametric Insurance Data Pipeline
description: Nullam urna elit, malesuada eget finibus ut, ac tortor. 
#icon: material/api
#status: new
---

Skip to:
Top Bar
Sidebar
Main Content



Search

Create

Ask Rovo

9+



Back to top
Search by title

2025 Goals
Updated Dec 11, 2025
Vincent Lelandais
Edit

Share


2025 Goals



By Héni Ghariani

1 min

2

Add a reaction
Category

Deliverables

Reviewed by

delivery truck Deliverable for Parametric Insurance

Check Mark Status for Parametric Insurance

delivery truck Deliverable for Commodities Intelligence

Check Mark Status for Commodities Intelligence

Comments

Product Description (internal)

Product Documentation (how this is working)

Product Manager

Internal - Parametric Insurance Product User Guide
 

Parametric Insurance Index Business Rules  

Parametric Insurance Index Business Rules
 

Pasture Masks for Parametric Insurance
 

Check Mark Done

AQVPC Business Rules PowerPoint

https://earthdailyagro-my.sharepoint.com/personal/heni_ghariani_earthdaily_com/Documents/AQVPC%20Business%20Rules.pptxConnect your OneDrive account 

History Crop Mask Availability
 

AQPVC Crop Cycle Dates
 

Check Mark Done

 

Marketing Materials (internal)

Ability to do demos (Pre-configures accounts, scripts,...)

Product Manager

Parametric Insurance account creation
 

Trial Account Requirement for Parametric Insurance Product
 

Trial account for Parametric Insurance
 

Check Mark Done

light bulb 

Customer creation for Croptical
 

 

Check Mark Done

Chloé

compte de démo KA pour les Assurance param et Com. intel.

 

Documentation for Sales Support (internal)

Confluence pages: 

How to give access to Product?

Product contents (processors,..)

How it works (to understand if tickets raised are bugs or not)

Training sessions

 

Product Manager

& Customer Success

IndexBuilder walkthrough — Parametric Insurance GeosysApp Module
 

Check Mark Done

Internal Block Creation Process
 

Check Mark Done

Chloé

Onboarding : on on a besoin de compte comment on fait ? (Param.)

les rappels sur les masques pour commodities 

Customer-Facing Documentation

API description

App user-guide -when appropriate

Product Manager

& Customer Success

🌾 Parametric Insurance API - Swagger UI 

documentation.md

 

Check Mark Done

Agriquest API Documentation 

Check Mark Done

Chloé

La page doc exeterne de EarthDaily

Accès page catalogue API

Check Mark  Il faut Organiser un point avec 

Mathieu H

Cécile

Chloé

Vincent

Revoir pour fixer les Objectifs

Related content


2025 Q4 - Hawkeye Goals, Tech Debt Prioritization
EDA DP PathFinders
More like this
2026 Q1 Roadmap UI
EDA DP QA / UI
More like this
ToDos / Reminders 2025 (excl. business as usual)
R&D Funded Projects
More like this
P3-Q4-25 | Sprint 6 Work Progress for Review
EDAGRO P3 - Analytics Visualization
More like this
25Q4 OBJECTIFS PERS
Florence Lambourdiere
More like this
25Q4 P3 Documentation Update
Florence Lambourdiere
More like this






Add a comment

Add labels

Add a reaction

documentation.md
text · 4 KB

1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
61
62
63
64
65
**📌 What is Parametric Insurance ?**

Parametric insurance is a **modern, data-driven approach** to insurance that provides **fast and transparent payouts** based on predefined triggers, such as:

- 🌧️ **Rainfall levels**
    
- 🌡️ **Temperature variations**
    
- 🌿 **Vegetation indices (NDVI)**
    

Unlike traditional indemnity-based insurance, which requires damage assessment, **parametric insurance automatically compensates farmers** when certain conditions are met. This means:

✅ **No lengthy claims process**  
✅ **Reduced administrative burden**  
✅ **Quick financial support after adverse weather events** (droughts, floods, storms, etc.)

---

**⚡Parametric Insurance with EarthDaily Agro**

The Parametric Data Service capability provides Actuaries and Data Scientists with high-quality environmental and agronomic data which enables them to create effective parametric indices in the agricultural insurance space.

EarthDaily Agro’s **Parametric Insurance API** provides seamless access to:

🔹 **Crop Specific Historical vegetation indices based on NDVI**  
🔹 **Historical High-Resolution Scientific-level weather data**

This API supports:  
🗺️ **Predefined geometries** (e.g., U.S. counties, Brazilian Municipios, French Communes…)  
📍 **Custom user-defined regions** (e.g., a specific farm in France or Brazil)

Insurers, agronomists, and financial institutions can offer innovative risk management solutions tailored to real-world agricultural challenges by leveraging Earth observation data.

---

📖 **API Documentation**

📌 [<b>Swagger UI</b>](https://parametric-insurance.aws-dev.geosys.com/docs) – Interactive API testing  
📌 [<b>ReDoc</b>](https://parametric-insurance.aws-dev.geosys.com/redoc) – Detailed API reference  
📌 [<b>SandBox</b>](https://parametric-insurance.aws-dev.geosys.com/) – Interactive Web user interface

---

🌍 **Indicators and coverage**

| **Indicator** | **Description** | **Temporal coverage** | **Geographical coverage** |
| --- | --- | --- | --- |
| Weather — Soil Moisture | High-resolution (9 km) global coverage with daily updates, providing advanced land  <br>surface modeling and observational data assimilation, for precise, consistent, and long-term records. | 2004 → Now | Globally |
| Weather — Precipitation | Our soil moisture data combines 2 high-resolution climate datasets with advanced modeling  <br>techniques (satellite imagery and ground truth data) to deliver accurate, global coverage at \~5 km resolution with frequent updates. | 2004 → Now | Globally |
| Vegetation (NDVI) | We Provide inter-calibrated Normalized Vegetation Index (NDVI) based on MODIS and Sentinel-3 acquisitions.  <br>We are currently preparing the launch of [EarthDaily Constellation](https://earthdaily.com/constellation/) which will provide a daily continuous stream of scientific-quality  <br>and analytics-ready data for even better accuracy. | 2004 → Now | Globally |
| NDVI Masking | We are providing a pure NDVI indicator, enabling data masking with classes like: combined vegetation, combined crops,  <br>specific crop type, or even pasture to better understand the global health status and vegetation conditions. We are constantly  <br>producing multiple accurate, before the Season, In-Season, and End of Season crop mask layers relying on internal scientific expertise and  <br>external official government data sources from USDA, “Agence de service et de paiement”,  <br>and Canadian Soil Information Service to make sure you have the most updated data. | 2004 → Now | Globally |

---

🛠️ **Request Use Case**

<img src="https://content.pstmn.io/bf78d432-f7e2-4766-bdb0-4f3055843d7b/aW1hZ2UucG5n" width="1002" height="212">

---

✉️ **Contact**  
Let’s get in touch!

You can use this form to [contact us](https://earthdailyagro.com/contact/?lang=fr)


--8<-- "snippets/contact-footer.md"