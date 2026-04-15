---
title: AI Enablement
description: Internal reference explaining how this documentation site is optimized for AI consumption through llms.txt generation, token estimation, structured front matter keywords, robots.txt discovery, and build metadata.
hide:
  - navigation
  - toc
keywords:
  - llms.txt
  - AI enablement
  - token estimation
  - SEO
  - front matter
  - keywords
  - LLM
  - robots.txt
---

# AI Enablement

This page documents the AI enablement approach used across this documentation site. The goal is to make EarthDaily's documentation **discoverable and consumable by AI assistants and LLMs** while keeping the authoring experience simple for contributors.

The approach relies on five pillars:

1. **`llms.txt` files** — machine-readable indexes and full-text exports generated at build time
2. **Token estimation** — approximate token counts for each page and section, helping LLMs fetch only what they need
3. **Front matter keywords** — structured metadata on every page, surfaced in the AI index for semantic filtering
4. **`robots.txt` discovery** — standard pointer so AI crawlers auto-discover `llms.txt`
5. **Build timestamp** — every generated index includes a build date so LLMs can assess freshness

---

## Architecture overview

```
mkdocs build
    │
    ▼
overrides/hooks/llms_txt.py  (on_post_build hook)
    │
    ├─► site/llms.txt                              ← index with links, descriptions, tokens, keywords, build date
    ├─► site/llms-full.txt                         ← all included pages concatenated
    └─► site/llms-full-{section-slug}.txt          ← per-section full-text files

docs/robots.txt  ──►  site/robots.txt              ← AI crawler discovery (copied by MkDocs)
```

The hook runs automatically after every build — no manual step is required.

---

## llms.txt files

### What is llms.txt?

[`llms.txt`](https://llmstxt.org/) is an emerging convention for websites to provide LLM-friendly content. It is analogous to `robots.txt` but designed for AI assistants rather than search engine crawlers.

### Generated files

| File | Content | Typical size |
|------|---------|-------------|
| `llms.txt` | Index listing every included page with URL, one-line description, token count, keywords, and build date | ~200+ lines |
| `llms-full.txt` | Complete text of all included pages concatenated | ~100k+ tokens |
| `llms-full-{section}.txt` | Full text for a single section (e.g., `llms-full-mining-marigold.txt`) | 3k-35k tokens each |

Section-specific files allow an AI assistant to fetch only the documentation it needs rather than downloading the entire corpus.

### Example `llms.txt` entry

```
- [API Reference](https://earthdaily.github.io/documentation/Agro/Library/Api_reference/):
  This page is dedicated to list all APIs provided by Earthdaily Agro
  (~3k tokens) [API reference, Swagger, OAuth 2.0, field borders, time series, vegetation index maps, weather API]
```

Each entry contains:

- **Link** — direct URL to the page
- **Description** — from front matter `description:` field
- **Token count** — approximate GPT-4o token count
- **Keywords** — from front matter `keywords:` list

### Build timestamp

Every `llms.txt` file includes a `Last built: YYYY-MM-DD` line near the top so AI systems can assess whether the content is current or stale. The date is generated in UTC at build time.

### Included sections

The hook is configured to include specific folders. This is controlled by the `INCLUDE_FOLDERS` variable at the top of `overrides/hooks/llms_txt.py`:

```python
INCLUDE_FOLDERS = [
    "Agro/Library",
    "Agro/Digital_ag",
    "Agro/Cropid",
    "Agro/Commodities_intelligence",
    "Data/Collections",
    "Data/earthplatform",
    "Data/earthone",
    "mining",
]
```

To add a new section to the AI index, append its path (relative to `docs/`) to this list and rebuild.

### Section grouping

Pages are grouped by breadcrumb depth, controlled by `SECTION_DEPTH` (default: `2`). For example, a page with breadcrumb `Agriculture > Analytic Catalog > Foundational Analytics` is grouped under `Agriculture > Analytic Catalog`.

---

## Token estimation

Each page and section file includes an approximate token count (e.g., `~3k tokens`). This helps AI systems decide whether to fetch a section or individual page.

### How it works

The hook uses the [`tiktoken`](https://github.com/openai/tiktoken) library with the `gpt-4o` encoding:

```python
import tiktoken

_enc = tiktoken.encoding_for_model("gpt-4o")

def _count_tokens(text: str) -> str:
    n = len(_enc.encode(text))
    if n >= 1000:
        return f"~{round(n / 1000)}k tokens"
    return f"~{n} tokens"
```

If `tiktoken` is not installed, token counts are silently omitted.

### Dependency

`tiktoken` is listed in `requirements.txt`:

```
tiktoken
```

---

## Front matter keywords

Every documentation page should include a `keywords` field in its YAML front matter. These keywords are:

- Surfaced in `llms.txt` entries for AI discovery
- Used by search engines for SEO
- Available to MkDocs plugins (e.g., `meta`, `tags`)

### Format

The hook supports three keyword formats. **YAML list is preferred** for consistency:

```yaml
---
title: Vegetation Time Series
description: Everything you need to know about the vegetation time series.
keywords:
  - vegetation time series
  - NDVI
  - EVI
  - Sentinel-2
  - Landsat
  - cloud masking
---
```

Also supported (but discouraged):

```yaml
# Inline list
keywords: [NDVI, EVI, Sentinel-2]

# Comma-separated string
keywords: NDVI, EVI, Sentinel-2
```

### Guidelines for choosing keywords

- Use **5-8 keywords** per page
- Include the **product name** (e.g., Marigold, Iris, EarthOne)
- Include **technical terms** an AI or user would search for
- Include **acronyms** alongside full names where relevant (e.g., `NDVI` and `vegetation index`)
- Avoid generic terms that apply to every page (e.g., `EarthDaily`, `documentation`)

### Coverage target

All pages listed in `INCLUDE_FOLDERS` should have `title`, `description`, and `keywords` in their front matter. Pages without `description` fall back to the first paragraph text (less precise). Pages without `keywords` appear in `llms.txt` without keyword tags, reducing discoverability.

---

## robots.txt and AI crawler discovery

A `robots.txt` file is served at the site root with a pointer to `llms.txt`:

```
User-agent: *
Allow: /

Sitemap: https://earthdaily.github.io/documentation/sitemap.xml

# AI / LLM discovery — see https://llmstxt.org
LLMsTxt: https://earthdaily.github.io/documentation/llms.txt
```

This allows AI crawlers and LLM-powered tools to auto-discover the documentation index without prior knowledge of the site structure. The `Sitemap` directive also points to the MkDocs-generated `sitemap.xml` for traditional search engines.

The file lives at `docs/robots.txt` and is copied to `site/robots.txt` by MkDocs during build.

---

## Content extraction and cleaning

Before writing page content to `llms-full*.txt`, the hook cleans the markdown to maximize signal for LLMs:

| Removed | Reason |
|---------|--------|
| YAML front matter | Metadata is already captured separately |
| HTML tags and comments | Not useful for text comprehension |
| Image references | LLMs cannot process images from text |
| Admonition markers (`!!!`, `???`) | Formatting noise |
| Code annotation comments (`// (1)`) | MkDocs-specific formatting |
| Snippet includes (`--8<--`) | Resolved at build time, not in source |

The cleaned body text is what gets concatenated into the full-text files.

---

## Resource linking

Pages can declare external resources (notebooks, repositories) using HTML comments:

```markdown
<!-- md:notebook https://github.com/earthdaily/Examples-and-showcases/blob/main/notebook.ipynb -->
```

These are extracted and listed below the page entry in `llms.txt`:

```
- [Page title](url): Description (~Xk tokens) [keywords]
  - Notebook (notebook): https://github.com/earthdaily/Examples-and-showcases/...
```

---

## Adding a new page to the AI index

No special action is needed beyond:

1. **Add front matter** with `title`, `description`, and `keywords` to your markdown file
2. **Place the file** under one of the folders listed in `INCLUDE_FOLDERS`
3. **Rebuild** — the hook picks it up automatically

If the page belongs to a new top-level section not yet in `INCLUDE_FOLDERS`, add the folder path to the list in `overrides/hooks/llms_txt.py`.

---

## Hook reference

| Item | Location |
|------|----------|
| Hook script | `overrides/hooks/llms_txt.py` |
| Hook registration | `mkdocs.yml` → `hooks:` section |
| Token estimation dependency | `requirements.txt` → `tiktoken` |
| Generated output | `site/llms.txt`, `site/llms-full*.txt` |
| Configuration variables | Top of `llms_txt.py` (`INCLUDE_FOLDERS`, `SECTION_DEPTH`, `INTRO_BLOCK`) |
| AI crawler discovery | `docs/robots.txt` → `site/robots.txt` |

---

## Future considerations

The following improvements could further enhance AI discoverability:

- **Structured data / JSON-LD** — Add Schema.org markup (`TechArticle`, `SoftwareApplication`) via a custom hook or template override, improving how search engines and AI understand page types

--8<-- "snippets/contact-footer.md"
