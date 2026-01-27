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


--8<-- "snippets/contact-footer.md"