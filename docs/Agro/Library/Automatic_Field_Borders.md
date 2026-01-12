---
title: Automatic Boundary
description: This section wil explain how to access field borders using a longitude and a latitude as the input. 
# icon: fontawesome/question
#status: new
---

# Automatic Field Borders

## Description

This analytic automatically generates field boundaries based on point coordinates (longitude and latitude). 
The feature is accessible via both the API and the GeosysApp.
Postman collection is available.
Your account requires specific permissions to access this API. Please contact us to request access.

## Baseline data

It leverages super-resolution Sentinel-2 imagery at 1-meter resolution to delineate field borders with high precision.

## API 

<swagger-ui src="https://api.geosys-na.net/field-borders/v1/swagger/v1/swagger.json"/>

### GET URL examples

- url = f"https://api.geosys-na.net/field-borders/v1/AutomaticBoundary?location={longitude},{latitude}&simplified_geom=true"
- url = "https://api.geosys-na.net/field-borders/v1/AutomaticBoundary?location=-54.889741119522725,-15.457580011321795&simplified_geom=true"

### Output

- The output is a GeoJSON-formatted geometry object.
- Example:
{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[-54.896934014,-15.459564873],[-54.896928958,-15.459505962],[-54.896866921,-15.459420837],[-54.89639611,-15.45899153],[-54.88685952,-15.450905368],[-54.886799685,-15.450888271],[-54.886716806,-15.450918856],[-54.88638171,-15.451127098],[-54.883536415,-15.452660488],[-54.883551241,-15.452762294],[-54.884096872,-15.454003786],[-54.887167296,-15.460781558],[-54.88724125,-15.460888693],[-54.887377023,-15.460898151],[-54.888441175,-15.460773089],[-54.889391261,-15.460620284],[-54.893506662,-15.460098733],[-54.894522788,-15.459938421],[-54.895206095,-15.459870722],[-54.896777703,-15.459642556],[-54.896888398,-15.459611659],[-54.896934014,-15.459564873]]]},"properties":{"id":"24073_21LYC_br-1202666904264365-mat-gro_202012","area":794938.3876514097,"area_acres":"196.433","area_ha":"79.494"},"id":"24073_21LYC_br-1202666904264365-mat-gro_202012"}

## Performance and accuracy

Intersection of Union average accuracy score of 0.94-0.96.

## Use case and product

This analytic is used in:
    - [Portfolio](/earthdaily-documentation/Agro/Portfolio/portfolio_product_site_draft/)
    - 

--8<-- "snippets/contact-footer.md"