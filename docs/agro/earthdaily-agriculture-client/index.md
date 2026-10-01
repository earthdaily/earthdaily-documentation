---
title: Overview
description: earthdaily-agriculture — bulk analytics extraction from the EarthDaily Agriculture APIs.
#icon: material/sprout-outline
keywords:
  - earthdaily agriculture
  - extractors
  - satellite
  - NDVI
  - vegetation index
  - weather
  - crop monitoring
  - workflow
---

# EarthDaily Agriculture

`earthdaily-agriculture` is a Python toolkit for **bulk analytics extraction** from the
EarthDaily Agriculture APIs — vegetation-index time series, weather, crop detection,
disease risk, emergence/harvest, scoring, and more. Every analytic is exposed as an
**extractor** that turns a DataFrame of fields (id + geometry + optional crop/dates)
into a tidy results DataFrame, with shared token management, column mapping, parallel
bulk processing, optional caching, and HTML reporting.

## Install

```bash
pip install earthdaily-agriculture
```

```python
import earthdaily.agriculture
```

The package installs into the shared `earthdaily` namespace, alongside sibling packages
such as [`earthdaily-earthone`](https://pypi.org/project/earthdaily-earthone/).
Python 3.10–3.12 is supported.

## Quick start

```python
from earthdaily.agriculture.services.workflow_manager import WorkflowManager
from earthdaily.agriculture.extractors.coverage_function import CoverageExtractor
import pandas as pd

# 1. Authenticate + load config (reads credentials from the environment / .env)
manager = WorkflowManager("prod")

# 2. A DataFrame of fields — minimally an id + a WKT geometry
entities = pd.DataFrame([
    {"id": "field_001", "geometry": "POLYGON ((...))"},
])

# 3. Configure an extractor and run it in bulk
coverage = CoverageExtractor(manager.bearer_token, manager.token_expiration, config=manager.config)
coverage.setup_coverage_parameters(vegetation_index="NDVI", start_date="2025-01-01", clear_cover_min=95)
results = coverage.process_entity_coverage_bulk_parallel(entity_list=entities, max_workers=5)
```

Every extractor follows the same shape: `__init__(token, expiration, config)` →
`setup_<type>_parameters(...)` → `process_<type>_bulk_parallel(entity_list=...)`.

## Where to go next

- **[Quick start](01 - Quick_Start_Guide.md)** — install, scaffold a project, first extraction
- **[DataFrame 101](02 - Dataframe_101.md)** — the entity DataFrame and column mapping
- **[Extractor parameters](03 - Extractor_parameters_reference.md)** · **[column mapping](04 - Extractor_column_mapping_reference.md)** · **[KPIs](05 - Extractor_kpi_reference.md)**
- **[Optimizing extractor output](16 - Optimizing_extractor_output.md)** — Parquet, lean columns, and manifests: a regional case study turning a 16 GB CSV into ~22 MB, losslessly
- **[Workflow architecture](09 - Workflow_architecture.md)** — chaining extractors with `WorkflowManager`
- **[API reference](15 - API_reference.md)** — auto-generated from the source docstrings
