---
title: API reference
description: Auto-generated API reference for the public earthdaily-agriculture surface.
#icon: material/api
keywords:
  - api reference
  - extractors
  - WorkflowManager
  - BaseExtractor
---

# API reference

The API reference is generated from the source docstrings by
[`mkdocstrings`](https://mkdocstrings.github.io/) at build time, so it always
reflects the installed package. It's split into one page per group below. For *when to use* each analytic and worked
examples, see the topical guides; these pages are the parameter/return contract.

| Group | Classes |
|-------|---------|
| [Orchestration](15a%20-%20API_Orchestration.md) | `WorkflowManager`, `BaseExtractor` |
| [Foundational extractors](15b%20-%20API_Foundational.md) | `CoverageExtractor`, `FLMExtractor`, `VegationTsExtractor`, `MRTSExtractor`, `WeatherExtractor`, `cropidExtractor`, `LocationBasedBorderExtractor`, `ZoningExtractor` |
| [Benchmark and warning extractors](15c%20-%20API_Benchmark_and_warning.md) | `ChangeIndexExtractor`, `InSeasonMonitoringExtractor`, `DifferenceExtractor` |
| [Crop development and stressors extractors](15d%20-%20API_Crop_development_and_stressors.md) | `DiseaseExtractor`, `EmergenceExtractor`, `GreennessExtractor`, `HarvestExtractor`, `PlantedExtractor`, `GDDExtractor`, `GDDOffsetExtractor` |
| [Sustainability extractors](15e%20-%20API_Sustainability.md) | `BaresoilExtractor` |
| [Risk management extractors](15f%20-%20API_Risk_management.md) | `HistoricalScoreExtractor`, `InseasonScoreExtractor`, `ZARCExtractor` |
| [Regional extractors](15g%20-%20API_Regional.md) | `RegionalExtractor` |
| [Entity and user management](15h%20-%20API_Entity_and_user_management.md) | `EntityManager`, `UserManager` |

Source code isn't reproduced on these pages. It is available in the installed package and in the public
[`earthdaily-agriculture`](https://github.com/earthdaily/earthdaily-agriculture) repository.
