---
title: Environmental Layers
description: This section explains everything you need to know about the layers used in Environmental Compliance Report analytic.
keywords:
  - environmental layers
  - CAR
  - IBAMA
  - INCRA
  - conservation units
  - deforestation
  - Brazil
  - indigenous lands
# icon: fontawesome/question
#status: new
---

# Environmental Layers

## 📖 Overview

The **Environmental Layers** provide access to a comprehensive collection of geospatial datasets used by EarthDaily Agro to support environmental, agricultural, and compliance analyses in Brazil. Each dataset represents a specific environmental, regulatory, or land-use layer published by official national and state institutions (e.g., IBAMA (1), INCRA (2), ICMBio (3), SEMA (4), FUNAI). These layers can be queried individually or combined to identify overlaps with agricultural fields, farms, or other geometries — helping users assess legal compliance, conservation areas, and land management boundaries.
{ .annotate }

1.  --8<-- "../../glossary.md:ibama"
2.  --8<-- "../../glossary.md:incra"
3.  --8<-- "../../glossary.md:icmbio"
4.  --8<-- "../../glossary.md:sema"

The datasets include CAR property boundaries, SIGEF and SNCI land registries, conservation units managed by ICMBio, embargo lists from IBAMA and state agencies (SEMA-MT, SIGA-GO, SIGA-MT, IAT-PR), and the LDI-PA deforestation list. These comprehensive layers enable thorough environmental compliance assessment and land-use analysis across Brazilian territories.

---

## ⚙️ API Access

<swagger-ui src="https://api.geosys-na.net/layers/v1/swagger/index.html"/>

---

## 🗂️ Available Datasets

The following table lists all available environmental layers. Hover over acronyms (1) to see their definitions.
{ .annotate }

1.  Acronyms like CAR, INCRA, SIGEF, IBAMA, etc. are automatically linked to glossary definitions via tooltips.

| Id                                | Name                                           | Description                                                                                                                                                                                                                                                                                                                                                                                      |
|:----------------------------------|:-----------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BR_LEGAL_AMAZON                   | Amazônia Legal                                 | Geographical delimitation of all states within the Amazon biome (only Maranhão is partially included) |
| BR_CAR_CONSOLIDATED_AREA          | Área Consolidada (CAR)                         | Consolidated areas are the land deforested before 2008-07-22                                                                                                                                                                                                                                                                                                                                     |
| BR_AGRICULTURAL_AREAS             | Área de Agricultura                            | Areas with agriculture land use.                                                                                                                                                                                                                                                                                                                                                                 |
| BR_CAR_PROPERTIES                 | Área Imóvel (CAR)                              | CAR is a Brazilian national public registry that integrates the environmental information of farms and its limits. The imovel database contains the farms limits.                                                                                                                                                                                                                                |
| BR_CAR_APP                        | Áreas de Preservação Permanente (CAR)          | Permanent Protected land that aims to preserve water resources, landscape, geological stability and biodiversity, facilitate the gene flow of fauna and flora, protect the soil and ensure the well-being of human populations.                                                                                                                                                                            |
| BR_RESTRICTED_USAGE               | Áreas de Uso Restrito (CAR)                    | Wetlands, swamp plains and areas with an inclination between 25° and 45°. Sustainable management and agrosilvopastoral activities are allowed as long as technical recommendations of official agencies are met.                                                                                                                                                                                 |
| BR_EMBARGOES_FREE_SEMAMT          | Áreas Desembargadas SEMA-MT                    | Territories that were embargoed before, but fixed (by paying fines and/or promoting environmental projects)                                                                                                                                                                                                                                                                                      |
| BR_QUILOMBOLAS                    | Áreas Quilombolas                              | Lands occupied by remnants of quilombo communities. They are protected by law to guarantee the communities physical, social, economic and cultural reproduction.                                                                                                                                                                             |
| BR_BIOMA                          | Bioma                                          | Large set of plant and animal life characterized by the dominant vegetation type.                                                                                                                                                                                                                                                                                                                |
| BR_DESFORESTATION_AFTER_2008      | Desmatamento após 2008                         | Satellite monitoring of clear-cut deforestation per year                                                                                                                                                                                                                                                                                                                                         |
| EMBARGOES_IAT_PR                  | Embargos IAT-PR                                | Embargoed territories of Paraná due to non-compliance with current environmental legislation.                                                                                                                                                                                                                                                                                                    |
| BR_EMBARGOES_IBAMA                | Embargos IBAMA                                 | Embargoed territories due to non-compliance with current environmental legislation.                                                                                                                                                                                                                                                                                                              |
| BR_EMBARGOES_ICMBIO               | Embargos ICMBio                                | Embargoed territories (mostly within Conservation Units) due to non-compliance with current environmental legislation.                                                                                                                                                                                                                                                                           |
| BR_LDI_ILLEGAL_DEFORESTATION_PARA | Embargos LDI-PA                                | Farms with illegal deforestation in Pará State.                                                                                                                                                                                                                                                                                                                                                  |
| BR_EMBARGOES_SEMAMT               | Embargos SEMA-MT                               | Embargoed territories of Mato Grosso due to non-compliance with current environmental legislation.                                                                                                                                                                                                                                                                                               |
| EMBARGOES_SIGA_GO                 | Embargos SIGA-GO                               | Embargoed territories of Goiás due to non-compliance with current environmental legislation.                                                                                                                                                                                                                                                                                                     |
| EMBARGOES_SIGA_GO_POINTS          | Embargos SIGA-GO (pontos)                      | Embargoed territories of Goiás due to non-compliance with current environmental legislation.                                                                                                                                                                                                                                                                                                     |
| EMBARGOES_SIGA_MT                 | Embargos SIGA-MT                               | Embargoed territories of Mato Grosso due to non-compliance with current environmental legislation.                                                                                                                                                                                                                                                                                               |
| EMBARGOES_SIGA_MT_POINTS          | Embargos SIGA-MT (pontos)                      | Embargoed territories of Mato Grosso due to non-compliance with current environmental legislation.                                                                                                                                                |
| INFRACAO_SIGA_GO                  | Infração SIGA-GO                               | Environmental infraction of Goiás                                                                                                                                                                                                                                                                                                                                                                |
| INFRACAO_SIGA_GO_POINTS           | Infração SIGA-GO (pontos)                      | Environmental infraction of Goiás                                                                                                                                                                                                                                                                                                                                                                |
| INFRACAO_SIGA_MT                  | Infração SIGA-MT                               | Environmental infraction of Mato Grosso                                                                                                                                                                                                                                                                                                                                                          |
| INFRACAO_SIGA_MT_POINTS           | Infração SIGA-MT (pontos)                      | Environmental infraction of Mato Grosso                                                                                                                                                                                                                                                                                                                                                          |
| BRAZIL_MUNICIPIOS                 | Municípios brasileiros                         | Brazilian municipalities borders                                                                                                                                                                                                                                                                                                                                                                 |
| BR_WATER_ALLOCATION               | Outorga d'água                                 | Right to use or interfere on water resources, provided by the Government for a certain time, purpose and condition.                                                                                                                                                                                                                                                                             |
| BR_CAR_LEGAL_RESERVE              | Reserva Legal (CAR)                            | Legal reserve are areas legally destined within a farm to hold native vegetation, in a percentage of up to 80%, depending on the biome where the farm is located.                                                                                                                                                                                                                                |
| BR_SIGEF_PROPERTIES               | Sistema de Gestão Fundiária (SIGEF)            | Land Management System, called SIGEF, is a system developed by INCRA to manage land information in the Brazilian rural areas. It is used to receive, validate, organize, regularize and make available georeferenced information on rural property boundaries.                                                                                                                               |
| BR_SNCI_PROPERTIES                | Sistema Nacional de Cadastro de Imóveis (SNCI) | National Property Certification System, called SNCI, is a system developed by INCRA to manage land information in the Brazilian rural areas.                                                                                                                                                                                                                                                 |
| BR_ARCHEOLOGICAL_SITES            | Sítios Arqueológicos                           | Heritage spread over the territory, comprising not only tangible but also intangible assets, the expression of popular traditions and the identity of the local communities.                                                                                                                                                                                                                     |
| BR_ARCHEOLOGICAL_SITES_POINTS     | Sítios Arqueológicos (pontos)                  | Heritage spread over the territory, comprising not only tangible but also intangible assets, the expression of popular traditions and the identity of the local communities.                                                                                                                                                                                                                     |
| BR_INDIGENOUS_LANDS               | Terras Indígenas                               | Indigenous Land are areas of special use, inhabited by indigenous communities. Those areas belong to the Federal Government, which keeps them for a public purpose by the Indigenous people.                                                                                                                                                                                                       |
| BR_CONSERVATION_UNITS             | Unidades de Conservação                        | Conservation Units of Full Protection seek nature preservation and only the indirect use of their natural resources is allowed.                                                                                                                                                                                                                                                                  |
| BR_CONSERVATION_UNITS_POINTS      | Unidades de Conservação (pontos)               | Conservation Units of Full Protection seek nature preservation and only the indirect use of their natural resources is allowed.                                                                                                                                                                                                                                                                  |

---

## 📋 Common Use Cases

### Environmental Compliance Checking

Query multiple layers to assess whether a property (1) overlaps with protected areas, embargoes, or indigenous lands:
{ .annotate }

1.  Properties can be identified using CAR, SIGEF, or SNCI registration data.

- **Conservation compliance**: Check overlap with ICMBio conservation units
- **Legal verification**: Cross-reference with IBAMA and state agency embargoes (SEMA-MT, SIGA-GO, SIGA-MT, IAT-PR)
- **Deforestation monitoring**: Verify against LDI-PA illegal deforestation list
- **Property validation**: Compare CAR boundaries with SIGEF and SNCI official registries

### Land Management Analysis

The INCRA-managed SIGEF and SNCI systems provide certified property boundaries that can be compared with CAR self-declared boundaries to identify discrepancies and ensure proper land registration.

---

--8<-- "snippets/contact-footer.md"