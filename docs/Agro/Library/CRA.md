---
title: Environmental Compliance
description: This section explains everything you need to know about the Environmental Compliance Report analytic.
# icon: fontawesome/question
status: new
---

# Environmental Compliance Report

## 📖 Overview

**EarthDailyAgro’s Environmental Compliance Report analytic** enables Brazilian customers to quickly check whether or not a given geometry (field, farm, policy or other) complies with environmental and national legislation. The user provides at least a geometry and a CPF/CPNJ number, and they can retrieve the report in json and PDF format, with all intersection percentage if any.

The **Environmental Compliance Report** is a tool that guides analysis based on federal, and state-level geospatial data from Brazilian public institutes. Its goal is to reduce environmental risks by identifying overlap with embargoes, historical deforestation, and protected territories such as native land, permanent protection areas, legal reserves, etc. Easy to apply, it is widely used by financial agents, banks, and insurance companies.



---

## 🗂️ Baseline Data

Description of each dataset on the [Environmental Layers](CRA_Layers.md) page.

---

## ⚙️ API Access

<swagger-ui src="https://api.geosys-na.net/reporting/environmentalcompliance/v1/swagger/index.html"/>

---

## ⚙️ Parameters & Variables


### Input Variables

| **Parameter** | **Variable Name** | **Description** | **Type** | **Usage** |
|----------------|-------------------|-----------------|-----------|------------|
| **Geometry** | `Geometry` | Geometry of the Area of Interest (WKT format) | `string` | Mandatory |
| **CPF** | `CPF` | Citizen or Company Registry (CPF or CNPJ) using the format with dots, dash and backslash | `string` | Mandatory |
| **CAR number** | `CARNumber` | CAR (Cadastro Ambiental Rural) number associated to the geometry | `string` | Optional |
| **Name** | `Name` | Name of the geometry | `string` | Optional |
| **Field ID** | `FieldId` | Id of the geometry to be displayed in the report | `string` | Optional |
| **ID** | `Id` | EarthDaily Agro internal id | `string` | Optional |



---

###  Output Variables  

| **Output**                | **Variable Name**          | **Description**                                                                 | **Type**     |
|----------------------------|-----------------------------|---------------------------------------------------------------------------------|--------------|
| **Id**                     | `id`                       | Unique identifier for the compliance request                                   | `string`     |
| **Report URL**             | `report_url`               | Link to the generated compliance report                         | `string` |
| **Request Date**           | `request_date`             | Date and time when the compliance request was made                             | `datetime`   |
| **Update Date**            | `update_date`              | Last update timestamp for the request                                          | `datetime`   |
| **Status**                 | `status`                   | Current status of the compliance process                                       | `string`     |
| **Compliance Items**       | `compliance_items`          | List of compliance layer checks associated with this request                   | `array`      |
| **Overlay Area**            | `overlay_area`             | Total area (in hectares) overlapped with the restriction layer | `double` |
| **Overlay Area Percent**    | `overlay_area_percent`     | Percentage of total area overlapping the restriction layer                     | `double` |
| **Overlay Geometry**        | `overlay_geometry`         | WKT Geometry of the overlapped area                                                | `string`|
| **Layer Date**              | `layer_date`               | Date of restriction layer most recent update                                 | `datetime`   |
| **Layer Name**              | `layer_name`               | Name of the restriction layer                         | `string`     |
| **Item Status**             | `item_status`              | Compliance check result for this layer (e.g., Unknown, Compliant, NotCompliant) | `string`     |
| **Reason**                  | `reason`                   | Reason for the compliance status  | `string`  |
| **Compliance Type**         | `compliance_type`          | Code name for the restriction layer | `string` |
| **Properties**                | `properties`               | List of requested property key-value pairs returned in the compliance result | `array`      |
| **Requested Property**        | `requested_property`       | Name of the requested property (e.g., Bioma, Municipality, AMAZONIA_LEGAL)     | `string`     |
| **Property Value**            | `property_value`           | Response of the requested property                                                | `string` or `json`  |
| **Centroid**                  | `centroid`                 | Center point coordinates of the analyzed area (WKT format)                     | `string`     |
| **Image**                     | `image`                    | Base64-encoded image used in the analysis                               | `string`     |
| **Errors**                    | `errors`                   | List of errors returned by the system (e.g., API or validation errors)         | `array` of `string` |
| **Field Id**                  | `field_id`                 | Identifier of the agricultural field being evaluated                           | `string`     |
| **Proposal**                  | `proposal`                 | Reference to a proposal related to this compliance check                       | `string`     |
| **Endorsement**               | `endorsement`              | Reference to an endorsement document associated with the compliance check      | `string`     |
| **Geometry**                  | `geometry`                 | Polygon geometry of the analyzed field (WKT)                 | `string`     |
| **CPF**                       | `cpf`                      | Document number linked to the property owner                                   | `string`     |
| **Compliance Status**         | `compliance_status`        | Final result of the compliance validation (e.g., `Compliant`, `NotCompliant`)   | `string`     |








---

## 📊 Performance

- **Region**: Brazil  
- **Average Generation Time**: < 10 seconds

---


## 💼 Use Case and Product Integration

This analytic is used in:

- [Portfolio](../Portfolio/portfolio_product_site_draft.md)

---

## 📚 Glossary

| Acronym | Full Name | Description |
|:---------|:-----------|:-------------|
| **CPF** | *Cadastro de Pessoa Física* | Brazilian individual taxpayer registry number issued by the Federal Revenue Service. Used to identify natural persons. |
| **CNPJ** | *Cadastro Nacional da Pessoa Jurídica* | Brazilian company (legal entity) taxpayer registry number issued by the Federal Revenue Service. Used to identify organizations and companies. |
| **CAR** | *Cadastro Ambiental Rural* | Brazilian national public registry integrating environmental information about rural properties, including farm boundaries and environmental features. |
| **WKT** | *Well-Known Text* | Text-based format for representing vector geometries such as points, lines, and polygons in GIS applications. |

---
