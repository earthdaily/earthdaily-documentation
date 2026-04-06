---
title: Python Package Documentation Guide
description: Guide for documenting Python packages like the EarthOne Python client using mkdocstrings, combining hand-written narrative with auto-generated API reference from docstrings.
hide:
  - navigation
  - toc
keywords:
  - mkdocstrings
  - Python documentation
  - docstrings
  - API reference
  - EarthOne Python client
  - auto-generated documentation
---

# Python Package Documentation Guide

This guide explains how to document Python packages (such as the EarthOne Python client) in this MkDocs site using the **layered documentation** approach: hand-written narrative content combined with auto-generated API reference pulled from Python docstrings at build time.

---

## Why layered documentation?

Auto-generated API docs from docstrings are accurate but lack context. Hand-written docs provide context but go stale. The layered approach gives you both:

| Layer | Source of truth | What it provides |
|-------|----------------|------------------|
| **Hand-written** | Markdown files in `docs/` | Architecture explanations, getting started guides, usage examples, cross-links to related pages |
| **Auto-generated** | Python docstrings via `:::` directives | Function signatures, parameter types, return values, source code links |

A single page combines both layers — the human writes the "why" and "when", while docstrings provide the "what" and "how".

---

## Prerequisites

### Plugin configuration

The `mkdocstrings` plugin is already configured in `mkdocs.yml`:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        python:
          paths: []
          options:
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            heading_level: 2
            members_order: source
            show_signature_annotations: true
            separate_signature: true
            docstring_style: google
```

Key settings:

- **`paths: []`** — The package must be installed in the build environment (listed in `requirements.txt`). mkdocstrings discovers it from the Python path.
- **`docstring_style: google`** — Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) in your Python code.
- **`show_source: true`** — Source code links are shown by default.
- **`heading_level: 2`** — Root objects render as H2 by default (override per page).

### Dependencies

Ensure these are in `requirements.txt`:

```
mkdocstrings-python
earthdaily
```

The package must be **pip-installable** — mkdocstrings imports it at build time to read docstrings.

---

## Writing docstrings (Python side)

Use Google-style docstrings in your Python code. mkdocstrings parses these into structured documentation automatically.

### Function example

```python
def search_images(
    self,
    geometry: dict,
    start_date: str,
    end_date: str,
    max_cloud_cover: float = 100.0,
) -> ImageCollection:
    """Search for satellite images within a geometry and date range.

    Queries the Catalog API for images intersecting the given geometry,
    filtered by acquisition date and cloud cover percentage.

    Args:
        geometry: GeoJSON geometry dict (Polygon or MultiPolygon).
        start_date: Start date in ISO 8601 format (e.g., "2024-01-01").
        end_date: End date in ISO 8601 format.
        max_cloud_cover: Maximum cloud cover percentage (0-100).
            Defaults to 100 (no filter).

    Returns:
        An ImageCollection containing matching images, sorted by date.

    Raises:
        AuthenticationError: If the auth token is expired or invalid.
        NotFoundError: If no images match the query.

    Example:
        ```python
        images = client.search_images(
            geometry=my_polygon,
            start_date="2024-06-01",
            end_date="2024-06-30",
            max_cloud_cover=20.0,
        )
        ```
    """
```

### Class example

```python
class CatalogClient:
    """Client for the EarthOne Catalog API.

    Provides methods for discovering, searching, and managing raster data
    products and images stored on the EarthOne platform.

    Args:
        auth: An authenticated Auth instance.
        timeout: Request timeout in seconds. Defaults to 30.

    Example:
        ```python
        from earthdaily.earthone import auth, catalog

        a = auth.Auth()
        client = catalog.CatalogClient(auth=a)
        products = client.get_products()
        ```
    """
```

### Tips for effective docstrings

- **First line** should be a concise summary (this appears in the generated docs as the description)
- **Args** section is mandatory for public functions — include types and defaults
- **Returns/Raises** only when non-obvious
- **Example** blocks render as syntax-highlighted code in the docs
- Avoid documenting internal/private methods (`_prefixed`) — they are excluded by default

---

## Writing documentation pages (Markdown side)

### Page structure

Every page follows this pattern:

```markdown
---
title: Module Name
description: One-line description for SEO and AI index.
keywords:
  - keyword1
  - keyword2
---

# Module Name

Hand-written introduction explaining what this module does, when to use it,
and how it fits into the broader system.

## ClassName

::: package.module.ClassName
    options:
      heading_level: 3
      show_source: true
```

The `::: package.module.ClassName` directive tells mkdocstrings to auto-generate documentation for that Python object from its docstring.

### Existing example: EarthOne Python client

From `docs/Data/earthone/earthone-python/auth.md`:

```markdown
---
title: Auth Module
description: Authentication and JWT token management for EarthOne APIs
keywords:
  - authentication
  - JWT token
  - OAuth
---

# Auth Module

The `earthdaily.earthone.auth` module handles authentication against the
EarthOne platform, including JWT token management, OAuth integration, and
credential resolution from multiple sources.

## Auth

::: earthdaily.earthone.auth.Auth
    options:
      heading_level: 3
      show_source: true
```

**What this produces:**

1. The hand-written intro paragraph (always visible, explains context)
2. The `Auth` class heading
3. Auto-generated content: class docstring, constructor signature, all public methods with their docstrings, parameter types, return values, and source code links

---

## Enhancing auto-generated documentation

The raw output from mkdocstrings is functional but can be significantly improved. Here are concrete techniques to make the auto-generated docs more useful.

### Add narrative context before each class

The biggest improvement is adding a few sentences of context **before** each `:::` directive. Explain when and why someone would use this class, not just what it does.

```markdown
## CatalogClient

Use this client to discover available data products and search for imagery.
Most workflows start here — authenticate first, then create a `CatalogClient`
to find the images you need before passing them to `ComputeClient` for
processing.

::: earthdaily.earthone.catalog.CatalogClient
    options:
      heading_level: 3
      show_source: true
```

### Curate members for clarity

By default, mkdocstrings shows all public members. For large classes, this creates noisy pages. Use the `members` option to show only the most relevant methods:

```markdown
::: earthdaily.earthone.catalog.CatalogClient
    options:
      heading_level: 3
      members:
        - search_images
        - get_products
        - get_image
      show_source: true
```

You can also exclude specific members while showing everything else:

```markdown
::: earthdaily.earthone.catalog.CatalogClient
    options:
      heading_level: 3
      filters:
        - "!^_"
        - "!^deprecated_"
      show_source: true
```

### Group related methods with hand-written sections

For complex classes, break up the auto-generated output with hand-written subheadings:

```markdown
## CatalogClient

::: earthdaily.earthone.catalog.CatalogClient
    options:
      heading_level: 3
      members: false

### Searching for images

The search methods accept GeoJSON geometries and return `ImageCollection`
objects that can be iterated or filtered further.

::: earthdaily.earthone.catalog.CatalogClient.search_images
    options:
      heading_level: 4
      show_root_heading: true

::: earthdaily.earthone.catalog.CatalogClient.search_timeseries
    options:
      heading_level: 4
      show_root_heading: true

### Managing products

::: earthdaily.earthone.catalog.CatalogClient.get_products
    options:
      heading_level: 4
      show_root_heading: true
```

This gives you full control over the page flow while still pulling signatures and docstrings automatically.

### Add usage examples alongside the API reference

Place practical examples directly after the auto-generated section for a class or method:

```markdown
## ComputeClient

::: earthdaily.earthone.compute.ComputeClient
    options:
      heading_level: 3
      show_source: true

### Common workflows

#### Computing NDVI over a field

```python
from earthdaily.earthone import auth, catalog, compute

a = auth.Auth()
cat = catalog.CatalogClient(auth=a)
comp = compute.ComputeClient(auth=a)

images = cat.search_images(
    geometry=my_field,
    start_date="2024-06-01",
    end_date="2024-06-30",
    max_cloud_cover=20.0,
)

ndvi = comp.calculate_index(images=images, index="NDVI")
```
```

### Cross-reference between modules

Use inline links to connect related modules, helping users navigate the documentation:

```markdown
The `CatalogClient` returns [`ImageCollection`](models.md#imagecollection)
objects that can be passed directly to
[`ComputeClient.calculate_index()`](compute.md#computeclient).
```

### Control the docstring section rendering style

The default table-style layout for Args/Returns can be changed per directive:

| Style | Best for |
|-------|----------|
| `table` (default) | Short parameter lists, compact layout |
| `list` | Long descriptions, parameters with complex types |
| `spacy` | Dense reference pages, minimal vertical space |

```markdown
::: earthdaily.earthone.catalog.CatalogClient.search_images
    options:
      docstring_section_style: list
```

### Hide source code for cleaner pages

For user-facing documentation (as opposed to developer reference), hiding source code reduces visual noise:

```markdown
::: earthdaily.earthone.auth.Auth
    options:
      heading_level: 3
      show_source: false
```

Keep `show_source: true` for developer-oriented reference pages where seeing the implementation is valuable.

---

## Common page patterns

### Pattern A: Package overview with selective exports

Use for the package's `index.md` — show only the most important top-level exports.

```markdown
# EarthOne Python Client

The `earthdaily` package provides Python access to EarthOne platform APIs.

## Installation

` ``bash
pip install earthdaily
` ``

## Package Structure

| Module | Description |
|--------|-------------|
| [**Auth**](auth.md) | Authentication and token management |
| [**Catalog**](catalog.md) | Data discovery and image search |
| [**Compute**](compute.md) | On-demand processing and index calculations |

## Top-level Exports

::: earthdaily.earthone
    options:
      show_root_heading: false
      members:
        - auth
        - catalog
        - compute
      show_source: false
      heading_level: 3
```

### Pattern B: Single class per section

Use for pages documenting one module with multiple classes.

```markdown
# Catalog Module

The catalog module provides data discovery and search capabilities.

## CatalogClient

::: earthdaily.earthone.catalog.CatalogClient
    options:
      heading_level: 3
      show_source: true

---

## Product

::: earthdaily.earthone.catalog.Product
    options:
      heading_level: 3
      show_source: true
```

### Pattern C: Whole module dump

Use for simple modules (e.g., exceptions, constants) where all members are relevant.

```markdown
# Exceptions

The exceptions module defines the error hierarchy for API errors.

::: earthdaily.earthone.exceptions
    options:
      heading_level: 2
      show_source: true
      members_order: source
```

### Pattern D: Narrative-heavy with targeted API inserts

Use when the hand-written content is the main value and API docs supplement it.

```markdown
# Authentication Guide

## Overview

Authentication uses OAuth 2.0 client credentials flow. You need a client ID
and secret, which you can obtain from the Console.

## Quick Start

` ``python
from earthdaily.earthone import auth

client = auth.Auth(client_id="...", client_secret="...")
token = client.get_token()
` ``

## How token refresh works

The Auth client automatically refreshes expired tokens. When a token is within
5 minutes of expiry, the next API call triggers a background refresh...

## API Reference

::: earthdaily.earthone.auth.Auth
    options:
      heading_level: 3
```

---

## Per-page option overrides

The `:::` directive accepts an `options` block that overrides the global config from `mkdocs.yml`:

| Option | Default | When to override |
|--------|---------|-----------------|
| `heading_level` | 2 | Set to 3 when the class is inside a `##` section |
| `show_source` | true | Set to false for user-facing guides or re-exports |
| `show_root_heading` | true | Set to false when you write the heading yourself |
| `members` | all public | Whitelist specific members for curated exports |
| `members_order` | source | Use `alphabetical` for large reference modules |
| `show_bases` | true | Set to false if inheritance chain is noisy |
| `filters` | `["!^_"]` | Customize to hide deprecated or internal members |
| `docstring_section_style` | table | Use `list` for verbose params, `spacy` for compact |

---

## Folder structure

Mirror your Python package structure in `docs/`:

```
docs/
  Data/
    earthone/
      earthone-python/
        index.md              ← Package overview + installation + quick start
        auth.md               ← Auth module (hand-written intro + ::: directive)
        catalog.md            ← Catalog module
        compute.md            ← Compute module
        vector.md             ← Vector module
        config.md             ← Configuration
        exceptions.md         ← Exception hierarchy
```

Add the section to `mkdocs.yml` nav:

```yaml
nav:
  - EarthOne Python Client:
    - Data/earthone/earthone-python/index.md
    - Auth: Data/earthone/earthone-python/auth.md
    - Catalog: Data/earthone/earthone-python/catalog.md
    - Compute: Data/earthone/earthone-python/compute.md
    - Vector: Data/earthone/earthone-python/vector.md
    - Config: Data/earthone/earthone-python/config.md
    - Exceptions: Data/earthone/earthone-python/exceptions.md
```

---

## What to write vs what to generate

| Write by hand | Let mkdocstrings generate |
|--------------|--------------------------|
| Module purpose and when to use it | Function/method signatures |
| Architecture decisions and trade-offs | Parameter names, types, and defaults |
| Getting started / quick start examples | Return types |
| Cross-links to related docs pages | Docstring content (Args, Returns, Raises) |
| Workflow examples combining multiple classes | Source code links |
| Comparison between approaches | Class hierarchy |

**Rule of thumb:** if it changes when the code changes, it belongs in the docstring. If it explains *why* or *when*, write it in markdown.

---

## Checklist for adding a new package

1. Add the package to `requirements.txt`
2. Create a folder under `docs/` mirroring the package structure
3. Write an `index.md` with installation, quick start, and module table
4. Create one `.md` per module with:
    - Front matter (`title`, `description`, `keywords`)
    - Hand-written introduction (1-3 sentences)
    - `:::` directives for each public class/function
5. Add the section to `mkdocs.yml` nav
6. Add the folder to `INCLUDE_FOLDERS` in `overrides/hooks/llms_txt.py` (for AI index)
7. Test locally with `mkdocs serve` — missing imports or typos in `:::` paths will show as build warnings

--8<-- "snippets/contact-footer.md"
