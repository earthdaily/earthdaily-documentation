# Glossary

<!-- snippet: ndvi -->
## NDVI (Normalized Difference Vegetation Index)
Index that measures vegetation health based on visible and near-infrared light reflectance. Values range from -1 to 1, with higher values indicating denser, healthier vegetation.
<!-- endsnippet -->

<!-- snippet: lr -->
## LR images
Image resolutions: **MR** (Medium Resolution) and **LR** (Low Resolution). Define the spatial detail level of the NDVI data used.
<!-- endsnippet -->

<!-- snippet: mr -->
## MR images
Medium Resolution imagery are satellite optical images with a resolution ranging from 10m to 30m.
<!-- endsnippet -->

<!-- snippet: season_duration -->
## Season Duration
Duration of the crop season, in days, used to calculate cumulative NDVI.
<!-- endsnippet -->

<!-- snippet: season_start -->
## Season Start Day / Month
Day and month marking the beginning of the crop season. Define the starting point for NDVI accumulation.
<!-- endsnippet -->

<!-- snippet: threshold -->
## Threshold
NDVI value used as a cutoff to determine relevant vegetative activity.
<!-- endsnippet -->

<!-- snippet: end_date -->
## End Date
Date until which the in-season NDVI is accumulated.
<!-- endsnippet -->

<!-- snippet: potential_score -->
## Potential Score
Indicator of the productive potential of an area based on cumulative NDVI during the season.
<!-- endsnippet -->

<!-- snippet: historical_potential_score -->
## Historical Potential Score
Mean of potential scores from previous seasons.
<!-- endsnippet -->

<!-- snippet: inseason_potential_score -->
## In-season Potential Score
Cumulative NDVI-based score for the current season up to the specified end date.
<!-- endsnippet -->

<!-- snippet: relative_potential_score -->
## Relative Potential Score
Ratio (in %) of in-season score to historical potential score.
<!-- endsnippet -->

<!-- snippet: wkt -->
## WKT (Well-Known Text)
Standard format for representing spatial geometries such as polygons, points, and lines.
<!-- endsnippet -->

<!-- snippet: aoi -->
## AOI (Area of Interest)
User-defined area for analysis. Usually defined as WKT.
<!-- endsnippet -->

<!-- snippet: epsg -->
## ESPG code
EPSG codes are numerical codes associated with coordinate system definitions.
For example, the EPSG code: 4326 matches with WGS84 geographical projection and is commonly used.
<!-- endsnippet -->


<!-- snippet: car -->
## CAR (Cadastro Ambiental Rural)
Brazilian national public registry integrating environmental information about rural properties, including farm boundaries and environmental features.
<!-- endsnippet -->

<!-- snippet: incra -->
## INCRA (Instituto Nacional de Colonização e Reforma Agrária)
Federal agency responsible for land reform, land management, and maintaining Brazilian national land databases such as SIGEF and SNCI.
<!-- endsnippet -->

<!-- snippet: ibama -->
## IBAMA (Instituto Brasileiro do Meio Ambiente e dos Recursos Naturais Renováveis)
Federal environmental agency in charge of environmental law enforcement, licensing, and conservation at the national level.
<!-- endsnippet -->

<!-- snippet: icmbio -->
## ICMBio (Instituto Chico Mendes de Conservação da Biodiversidade)
Federal agency responsible for managing Brazil's conservation units and biodiversity preservation.
<!-- endsnippet -->

<!-- snippet: sema_mt -->
## SEMA-MT (Secretaria de Estado de Meio Ambiente de Mato Grosso)
State Secretariat for the Environment in Mato Grosso, responsible for environmental regulation and enforcement.
<!-- endsnippet -->

<!-- snippet: sema -->
## SEMA (Secretaria de Estado de Meio Ambiente)
State-level Secretariat for the Environment (generic term; each state may have its own, e.g., SEMA-MT).
<!-- endsnippet -->

<!-- snippet: siga_go -->
## SIGA-GO (Sistema de Gestão Ambiental de Goiás)
State environmental management system for Goiás, used to track infractions, embargoes, and environmental compliance.
<!-- endsnippet -->

<!-- snippet: siga_mt -->
## SIGA-MT (Sistema Integrado de Gestão Ambiental de Mato Grosso)
State environmental management system for Mato Grosso.
<!-- endsnippet -->

<!-- snippet: iat_pr -->
## IAT-PR (Instituto Água e Terra do Paraná)
Environmental institute of Paraná responsible for licensing, monitoring, and conservation activities.
<!-- endsnippet -->

<!-- snippet: ldi_pa -->
## LDI-PA (Lista de Desmatamento Ilegal do Pará)
Official list of farms with illegal deforestation in the state of Pará.
<!-- endsnippet -->

<!-- snippet: snci -->
## SNCI (Sistema Nacional de Cadastro de Imóveis Rurais)
National Property Certification System developed by INCRA to manage cadastral and geospatial data of rural properties.
<!-- endsnippet -->

<!-- snippet: sigef -->
## SIGEF (Sistema de Gestão Fundiária)
Land Management System developed by INCRA to register and validate georeferenced rural property data.
<!-- endsnippet -->

<!-- snippet: cpf -->
## CPF (Cadastro de Pessoa Física)
Brazilian individual taxpayer registry number issued by the Federal Revenue Service. Used to identify natural persons.
<!-- endsnippet -->

<!-- snippet: cnpj -->
## CNPJ (Cadastro Nacional da Pessoa Jurídica)
Brazilian company (legal entity) taxpayer registry number issued by the Federal Revenue Service. Used to identify organizations and companies.
<!-- endsnippet -->

<!-- snippet: harvest_detection -->
## Harvest Detection
The process of identifying the harvest date or readiness based on vegetation index and crop maturity.
<!-- endsnippet -->

<!-- snippet: harvest_type -->
## Harvest Type
Defines the detection mode: **INSEASON_HARVEST**, **HISTORICAL_HARVEST**, or **HARVEST_READINESS**.
<!-- endsnippet -->

<!-- snippet: threshold_start -->
## Threshold Start
NDVI value used as a threshold to consider the start of relevant vegetative growth.
<!-- endsnippet -->

<!-- snippet: average_potential_score -->
## Average Potential Score
Mean of historical potential scores over the last five years.
<!-- endsnippet -->

<!-- snippet: olympic_mean -->
## Olympic Mean
Mean calculated by excluding the highest value and NaNs, used to reduce the impact of outliers.
<!-- endsnippet -->

<!-- snippet: standard_deviation -->
## Standard Deviation
Measure of variability in historical potential scores. Higher values indicate greater uncertainty.
<!-- endsnippet -->

<!-- snippet: risk_score -->
## Risk Score
Risk index calculated as: (`Standard Deviation` / `Average`) × 100. Indicates the stability of potential over time.
<!-- endsnippet -->

<!-- snippet: season_break -->
## Season Break
Boolean indicator showing whether a season's score was significantly below the historical average (less than 70% of the Olympic Mean).
<!-- endsnippet -->

<!-- snippet: emergence_date -->
## Emergence Date
The date when crop emergence was detected, used as a reference for planted area computation.
<!-- endsnippet -->

<!-- snippet: processor_mode -->
## Processor Mode
Defines the computation type: **PLANTED_AREA** for planted area calculation, **CONTROL** for unplanted area check.
<!-- endsnippet -->

<!-- snippet: control_threshold -->
## Control Threshold
Percentage threshold for unplanted area in CONTROL mode.
<!-- endsnippet -->

<!-- snippet: ndvi_index -->
## NDVI (Normalized Difference Vegetation Index)
Calculated as (NIR - Red) / (NIR + Red), NDVI measures vegetation health based on the difference between near-infrared and red light reflectance. Values range from -1 to 1, with higher values indicating healthier, denser vegetation. **Application:** General vegetation health monitoring, biomass estimation, and crop vigor assessment.
<!-- endsnippet -->

<!-- snippet: evi -->
## EVI (Enhanced Vegetation Index)
A modified vegetation index that corrects for atmospheric conditions and canopy background signals. EVI uses blue, red, and near-infrared bands with correction factors to minimize soil and atmospheric influences. **Application:** Improved sensitivity in high biomass areas, tropical rainforest monitoring, and areas with dense vegetation where NDVI saturates.
<!-- endsnippet -->

<!-- snippet: ndwi -->
## NDWI (Normalized Difference Water Index)
Calculated as (Green - NIR) / (Green + NIR), NDWI measures the water content in vegetation by comparing green and near-infrared reflectance. Higher values indicate higher water content. **Application:** Water stress detection, irrigation management, and drought monitoring in crops.
<!-- endsnippet -->

<!-- snippet: ndmi -->
## NDMI (Normalized Difference Moisture Index)
Calculated as (NIR - SWIR) / (NIR + SWIR), NDMI uses near-infrared and shortwave infrared bands to assess vegetation water content. Values range from -1 to 1, with higher values indicating higher moisture content. **Application:** Canopy moisture content monitoring, water stress assessment, and fire risk evaluation.
<!-- endsnippet -->

<!-- snippet: ndre -->
## NDRE (Normalized Difference Red Edge)
Calculated as (NIR - Red Edge) / (NIR + Red Edge), NDRE uses the red edge band (around 700-750nm) which is sensitive to chlorophyll content. More responsive to plant health variations than NDVI. **Application:** Nitrogen content assessment, chlorophyll concentration monitoring, and precision agriculture applications for fertilizer management.
<!-- endsnippet -->

<!-- snippet: gndvi -->
## GNDVI (Green Normalized Difference Vegetation Index)
Calculated as (NIR - Green) / (NIR + Green), GNDVI substitutes the green band for the red band in the NDVI formula. More sensitive to chlorophyll concentration variations than NDVI. **Application:** Chlorophyll content assessment, photosynthetic activity monitoring, and early-stage crop health detection.
<!-- endsnippet -->

<!-- snippet: s2rep -->
## S2REP (Sentinel-2 Red Edge Position)
An index that estimates the position of the red edge inflection point in the spectral reflectance curve using Sentinel-2's red edge bands. The red edge position shifts with changes in chlorophyll content. **Application:** Chlorophyll and nitrogen status assessment, crop health monitoring, and precision agriculture for variable rate application of nutrients.
<!-- endsnippet -->

<!-- snippet: lai -->
## LAI (Leaf Area Index)
A dimensionless measure representing the total one-sided area of leaf tissue per unit ground surface area. LAI quantifies the amount of leaf material in the canopy and is derived from optical remote sensing data. **Application:** Canopy structure characterization, biomass estimation, crop growth monitoring, and yield prediction models.
<!-- endsnippet -->

<!-- snippet: biomass_index -->
## Biomass Index
An index derived from spectral bands to estimate the amount of living plant material (above-ground biomass) in a given area. Various formulations exist using combinations of visible, near-infrared, and shortwave infrared bands. **Application:** Above-ground biomass estimation, carbon stock assessment, crop productivity monitoring, and yield forecasting.
<!-- endsnippet -->

<!-- snippet: cab -->
## CAB (Chlorophyll A+B)
A biophysical variable that estimates the total chlorophyll concentration (Chlorophyll A and B combined) in vegetation canopy. Derived through radiative transfer models or empirical relationships from spectral data. **Application:** Chlorophyll concentration monitoring, photosynthetic capacity assessment, nitrogen status evaluation, and crop health diagnostics.
<!-- endsnippet -->

<!-- snippet: rvi -->
## RVI (Ratio Vegetation Index)
Calculated as NIR / Red, RVI is one of the simplest vegetation indices using the ratio between near-infrared and red reflectance. Values typically range from 0 to more than 10 for vegetation. **Application:** Simple vegetation assessment, quick biomass estimation, and basic crop monitoring where computational simplicity is preferred.
<!-- endsnippet -->

<!-- snippet: dbsi -->
## Dry Bare Soil Index (DBSI)
The analytic uses the **Dry Bare Soil Index** calculated medium resolution data.
```
DBSI = ((SWIR1 - Green) / (SWIR1 + Green)) - ((NIR - Red) / (NIR + Red))
```
**Formula Components:**
**First Term: `(SWIR1 - Green) / (SWIR1 + Green)`**
- Normalized difference using Short-Wave Infrared (SWIR1) and Green bands
- Highlights dry soil and bare surfaces
- Dry soil exhibits high SWIR reflectance, creating positive values
**Second Term: `(NIR - Red) / (NIR + Red)`**
- This is essentially the NDVI (1) (Normalized Difference Vegetation Index)
- Measures vegetation greenness and density
- Vegetated areas produce high positive values
<!-- endsnippet -->


--8<-- "snippets/contact-footer.md"