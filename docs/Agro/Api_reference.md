---
title: API reference 
description: This page is dedicated to list all APIs provided by Earthdaily Agro
#icon: material/wallet-outline
hide:
  - toc
---

<style>

/* 3-column layout */
.md-typeset .grid.cards {
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 0.8rem !important;
}

/* Target the exact list items (cards) */
.md-typeset .grid.cards > ul > li {
    padding: 0.6rem !important;
    font-size: 0.8rem !important;
    display: flex !important;
    flex-direction: column !important;
    min-height: 100% !important;
}

/* Icon and title on same line */
.md-typeset .grid.cards > ul > li > p:first-child {
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    margin: 0 0 0.3rem 0 !important;
}

/* Card titles */
.md-typeset .grid.cards > ul > li p strong {
    font-size: 0.95rem !important;
}

/* Separator line */
.md-typeset .grid.cards > ul > li > hr {
    margin: 0.3rem 0 !important;
}

/* Card description paragraphs */
.md-typeset .grid.cards > ul > li > p {
    font-size: 0.8rem !important;
    line-height: 1.4 !important;
    margin: 0.3rem 0 !important;
}

/* Bullet points inside cards */
.md-typeset .grid.cards > ul > li ul li {
    font-size: 0.75rem !important;
    margin: 0.2rem 0 !important;
}

/* Container for buttons - push to bottom */
.md-typeset .grid.cards > ul > li > p:has(a.md-button) {
    display: block !important;
    white-space: nowrap !important;
    margin-top: auto !important;
    padding-top: 0.5rem !important;
}

/* Buttons */
.md-typeset .grid.cards a.md-button {
    font-size: 0.7rem !important;
    padding: 0.25rem 0.6rem !important;
    margin-right: 0.4rem !important;
    display: inline-block !important;
    white-space: nowrap !important;
}
</style>

# API Reference

Browse our comprehensive API documentation across all EarthDaily Agro analytics. Each API provides detailed Swagger documentation with interactive endpoints, request/response examples, and authentication requirements.

---

## Core

<div class="grid cards" markdown>

-   :material-shield-lock: **Identity & Authentication**

    ---
    
    OAuth 2.0 authentication service for secure API access. Provides token-based authentication with configurable scopes and expiration.
    
    [:simple-swagger: Swagger](https://identity.geosys-na.com/v2.1/swagger.html){ .md-button }
    [:octicons-link-external-16: Details](https://identity.geosys-na.com/v2.1/){ .md-button }

-   :material-database: **Entity Management**

    ---
    
    Unified store for agricultural master data including fields, seasons, growers, and farm hierarchies. Supports CRUD operations for Ag entities.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/master-data-management/v6/swagger){ .md-button }
    [:octicons-link-external-16: Details ](../Agro/index.md/..){ .md-button }

-   :material-cloud-upload: **Analytic Store**

    ---
    
    Access various analytics derived from imagery and weather data.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/analytics/swagger/index.html){ .md-button }
    [:octicons-link-external-16: Details ](../Agro/index.md/..){ .md-button }

</div>

---

## Foundational Analytics

<div class="grid cards" markdown>

-   :material-vector-polygon: **Field Borders**

    ---
    
    Automatic field boundary delineation using deep learning and satellite imagery. Generates accurate field polygons without manual digitization.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/field-borders/v1/swagger){ .md-button }
    [:octicons-link-external-16: Details ](./Library/Automatic_Field_Borders.md){ .md-button }

-   :material-chart-line: **Time Series**

    ---
    
    Historical and near-real-time vegetation indices time series. Cloud-masked, smoothed data for accurate temporal analysis of crop development.
    
    [:simple-swagger: Swagger](http://api.geosys-na.net/vegetation-time-series/v1/swagger){ .md-button }
    [:octicons-link-external-16: Details](./Api_reference.md){ .md-button }

-   :material-barley: **Crop ID**

    ---
    
    AI-powered crop type classification using multi-temporal satellite imagery. Identifies major crop types with confidence scores and validation metrics.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/cropmasks/v1/swagger/index.html){ .md-button }
    [:octicons-link-external-16: Details](https://api.geosys-na.net/cropmasks/v1/swagger){ .md-button }
    

-   :material-layers: **Layer Service**

    ---
    
    Access satellite imagery layers, vegetation indices, and derived analytics products. Supports multiple sensors and on-demand processing.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/layers/v1/swagger){ .md-button }
    [:octicons-link-external-16: Details](./Api_reference.md){ .md-button }

-   :material-map: **Vegetation Index Maps**

    ---
    
    Generate field-level vegetation index maps including NDVI, EVI, NDRE. Supports prescription mapping and precision agriculture workflows.
    

    [:simple-swagger: Swagger](http://api.geosys-na.net/field-level-maps/v5/swagger){ .md-button }
    [:octicons-link-external-16: Details](./Api_reference.md){ .md-button }

-   :material-weather-cloudy: **Field Weather**

    ---
    
    Historical weather data and forecasts for agricultural fields. Includes temperature, precipitation, humidity, and derived agro-meteorological indices.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/Weather/v1/swagger){ .md-button }
    [:octicons-link-external-16: Details](./Api_reference.md){ .md-button }

</div>

---

## Benchmark and Warning

<div class="grid cards" markdown>

-   :material-radar: **Change Detection**

    ---
    
    Detect significant changes in field conditions using multi-temporal satellite analysis. Identifies anomalies, disturbances, and rapid vegetation changes.
    
    [:simple-swagger: Swagger](https://change-index.aws.geosys.com/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/Change_Index.md){ .md-button }

-   :material-chart-bar: **Benchmark**

    ---
    
    Compare field performance against historical patterns, regional averages, and peer benchmarks. Supports relative performance analysis.
    
    [:simple-swagger: Swagger](){ .md-button }
    [:octicons-link-external-16: Details](./Library/...){ .md-button }

-   :material-monitor-dashboard: **In-Season Monitoring**

    ---
    
    Real-time crop performance monitoring combining satellite data, weather, and agronomic models. Provides actionable insights for in-season decisions.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/Weather/v1/swagger){ .md-button }
    [:octicons-link-external-16: Details](./Library/..){ .md-button }

</div>

---

## Risk Management

<div class="grid cards" markdown>

-   :material-gauge: **Risk Score**

    ---
    
    Comprehensive risk assessment combining historical performance, in-season conditions, and predictive analytics. Supports underwriting and portfolio management.
    
    
    **Historical:** 
    [:octicons-link-external-16: Details](./Library/Historical_Potential_Score.md){ .md-button }
    [:simple-swagger: Swagger](https://historical-potential-risk-score.aws.geosys.com/docs){ .md-button }
    **In-Season:** 
    [:octicons-link-external-16: Details](./Library/In-season_Potential_Score.md){ .md-button }
    [:simple-swagger: Swagger](http://inseason-potential-score.aws.geosys.com/docs){ .md-button }

-   :material-leaf-maple: **Environmental Compliance**

    ---
    
    Track and report environmental sustainability metrics including carbon sequestration, conservation practices, and regulatory compliance.
    
    [:simple-swagger: Swagger](https://api.geosys-na.net/reporting/environmentalcompliance/v1/swagger){ .md-button }
    [:octicons-link-external-16: Details](./Library/CRA.md){ .md-button }

-   :material-calendar-check: **ZARC Agricultural Risk**

    ---
    
    Brazilian Agricultural Climate Risk Zoning (ZARC) compliance service. Determines optimal planting windows based on climate risk analysis.
    

    [:simple-swagger: Swagger](https://zvjihjkwfwohudwcnbhjbpsudq0jhszp.lambda-url.us-east-1.on.aws/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/ZARC.md){ .md-button }

</div>

---

## Crop Development and Stressors

<div class="grid cards" markdown>

-   :fontawesome-solid-seedling: **Emergence Detection**

    ---
    
    Automated detection of crop emergence dates using satellite-based phenology analysis. Monitors planting window and early growth stages.
    
    [:simple-swagger: Swagger](https://emergence-detection.aws.geosys.com/docsr){ .md-button }
    [:octicons-link-external-16: Details](./Library/Emergence.md){ .md-button }

-   :material-sprout-outline: **Planted Area**

    ---
    
    Accurate estimation of planted acreage using crop identification and field boundary analysis. Supports compliance and acreage reporting.
    
    [:simple-swagger: Swagger](https://planted-area.aws.geosys.com/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/Planted_Area.md) .md-button }

-   :material-leaf: **Greenness**

    ---
    
    Monitor crop canopy development and vegetation vigor through growing season. Tracks greenness progression and identifies stress periods.
    
    [:simple-swagger: Swagger](https://zn6hzsqoyoe3qgaoau4ssgpq440vtmpa.lambda-url.us-east-1.on.aws/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/){ .md-button }

-   :material-check-circle: **Harvest Readiness**

    ---
    
    Assess crop maturity and harvest readiness using vegetation indices and phenology models. Optimizes harvest timing decisions.
    

    [:simple-swagger: Swagger](https://harvest-detection.aws.geosys.com/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/Harvest_Detection.md){ .md-button }

-   :material-tractor: **Harvest Detection**

    ---
    
    Real-time harvest date identification and progress monitoring. Tracks harvest operations across fields and regions using change detection.
    
    [:simple-swagger: Swagger](https://harvest-detection.aws.geosys.com/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/Harvest_Detection.md){ .md-button }

-   :material-tractor: **Disease risk**

    ---
    
    Evaluate disease risk on location for Corn and Soybeans.
    
    [:simple-swagger: Swagger](https://t7izeqf7q5t4xseagqap5ev7xm0xpmmh.lambda-url.us-east-1.on.aws/v1/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/){ .md-button }

</div>

---

## Sustainability

<div class="grid cards" markdown>

-  :fontawesome-solid-landmark-flag: **Tillage**

    ---
    
    Detect tillage practices and soil disturbance events using radar and optical imagery. Supports conservation agriculture monitoring and carbon programs.
    
    [:simple-swagger: Swagger](https://api.geosys.com/processors/tillage/v1/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/){ .md-button }

-   :material-flower: **Cover Crop**

    ---
    
    Satellite-based cover crop detection and coverage analysis. Quantifies cover crop presence for sustainability programs.
    
    [:simple-swagger: Swagger](https://api.geosys.com/processors/cover-crop/v1/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/){ .md-button }

-   :material-weight: **Cover Crop Biomass**

    ---
    
    Estimate cover crop biomass and carbon sequestration potential. Supports carbon credit programs and soil health initiatives.
    

    [:simple-swagger: Swagger](){ .md-button }
    [:octicons-link-external-16: Details](){ .md-button }

-   :material-weight: **Baresoil**

    ---
    
    Estimate the number of days with bare soil exposed.
    

    [:simple-swagger: Swagger](https://avuqeoz2lrpi2s5qovww5k4vca0itlyy.lambda-url.us-east-1.on.aws/v1/docs){ .md-button }
    [:octicons-link-external-16: Details](./Library/){ .md-button }

</div>

---

## Regional Analytics

<div class="grid cards" markdown>

-   :material-earth: **Regional Monitoring**

    ---
    
    Large-scale crop monitoring and analytics for regions, counties, and administrative boundaries. Supports portfolio analysis and market intelligence.
    
    [:simple-swagger: Swagger](http://api.geosys.internal/Agriquest/Geosys.AgriQuest.CropMonitoring.WebApi/v0/swagger/ui/index){ .md-button }
    [:octicons-link-external-16: Details](./Library/Regional_Monitoring.md){ .md-button }

</div>

---

