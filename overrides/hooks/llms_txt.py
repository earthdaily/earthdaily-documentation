from __future__ import annotations

import re
from collections import OrderedDict
from pathlib import Path
from mkdocs.config.defaults import MkDocsConfig

# -----------------------------------------------------------------------------
# Configuration - folders to include (relative to docs/, forward slashes)
#
# Pages are included if their nav path starts with any of these prefixes.
# Comment/uncomment to control what appears in llms.txt and llms-full.txt.
# -----------------------------------------------------------------------------

INCLUDE_FOLDERS = [
    "Agro/Library",
#    "Agro/Digital_ag",
#    "Agro/Portfolio",
#    "Agro/Cropid",
#    "Agro/Commodities_intelligence",
#    "Agro/Parametric",
#    "Agro/Territory_insights",
#    "Agro/App",
#    "Agro/QGIS",
#    "Support",
]

# How many breadcrumb levels to keep for section grouping (e.g. 2 -> "Agriculture > Analytic catalog")
SECTION_DEPTH = 2

# Static intro block inserted at the top of llms.txt (after the header, before the index).
# Use markdown. Set to "" to disable.
INTRO_BLOCK = """\
EarthDaily Analytics provides satellite imagery and geospatial analytics \
for agriculture, insurance, and environmental monitoring. \
For a full overview of EarthDaily's products and services, visit \
[earthdaily.com](https://earthdaily.com).
"""


# -----------------------------------------------------------------------------
# Hook
# -----------------------------------------------------------------------------

def on_post_build(config: MkDocsConfig):
    """Generate llms.txt (index), llms-full.txt, and per-section full-text files."""
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])
    site_name = config.get("site_name", "EarthDaily documentation")
    site_description = config.get("site_description", "")
    site_url = (config.get("site_url", "") or "").rstrip("/")

    nav = config.get("nav")
    if not nav:
        print("llms_txt: no nav found in config, skipping")
        return

    # Collect pages grouped by section
    groups: OrderedDict[str, list[dict]] = OrderedDict()
    page_count = 0

    for breadcrumb, nav_title, rel_path in _walk_nav(nav):
        # Normalize path: fix double slashes, handle directory refs
        rel_path = rel_path.replace("\\", "/").replace("//", "/")
        if rel_path.endswith("/"):
            rel_path += "index.md"

        # Filter by configured folders
        if not any(rel_path.startswith(folder) for folder in INCLUDE_FOLDERS):
            continue

        # Read the source file
        file_path = docs_dir / rel_path
        if not file_path.is_file():
            print(f"  llms_txt: skipping missing file {rel_path}")
            continue

        content = file_path.read_text(encoding="utf-8", errors="replace")

        title = nav_title or _extract_title(content, Path(rel_path))
        description = _extract_description(content)
        keywords = _extract_keywords(content)
        resources = _extract_resources(content)
        body = _clean_markdown(content)

        if not body.strip():
            continue

        # Build URL
        url_path = rel_path.removesuffix(".md")
        if url_path.endswith("/index"):
            url_path = url_path.removesuffix("/index")
        url_path += "/"
        page_url = f"{site_url}/{url_path}" if site_url else ""

        # Section key from breadcrumb
        section_key = " > ".join(breadcrumb[:SECTION_DEPTH]) if breadcrumb else "General"

        groups.setdefault(section_key, []).append({
            "title": title,
            "url": page_url,
            "description": description,
            "keywords": keywords,
            "resources": resources,
            "body": body,
        })
        page_count += 1

    # --- Build per-section full-text files ---
    section_files: OrderedDict[str, str] = OrderedDict()
    for section, pages in groups.items():
        slug = _slugify(section)
        filename = f"llms-full-{slug}.txt"
        section_files[section] = filename

        section_header = f"# {site_name} — {section}\n\n"
        if site_description:
            section_header += f"> {site_description}\n\n"
        if INTRO_BLOCK:
            section_header += f"{INTRO_BLOCK}\n"

        parts = [section_header]
        for page in pages:
            part = f"## {page['title']}\n"
            if page["url"]:
                part += f"URL: {page['url']}\n"
            if page["keywords"]:
                part += f"Keywords: {', '.join(page['keywords'])}\n"
            if page["resources"]:
                part += "Resources:\n"
                for label, url in page["resources"]:
                    part += f"  - {label}: {url}\n"
            part += f"\n{page['body']}\n\n---\n"
            parts.append(part)

        (site_dir / filename).write_text("\n".join(parts), encoding="utf-8")

    # --- Build llms-full.txt (all sections combined) ---
    full_header = f"# {site_name}\n\n"
    if site_description:
        full_header += f"> {site_description}\n\n"
    if INTRO_BLOCK:
        full_header += f"{INTRO_BLOCK}\n"

    full_parts = [full_header]
    for section, pages in groups.items():
        full_parts.append(f"## {section}\n")
        for page in pages:
            part = f"### {page['title']}\n"
            if page["url"]:
                part += f"URL: {page['url']}\n"
            if page["keywords"]:
                part += f"Keywords: {', '.join(page['keywords'])}\n"
            if page["resources"]:
                part += "Resources:\n"
                for label, url in page["resources"]:
                    part += f"  - {label}: {url}\n"
            part += f"\n{page['body']}\n\n---\n"
            full_parts.append(part)

    (site_dir / "llms-full.txt").write_text("\n".join(full_parts), encoding="utf-8")

    # --- Build llms.txt (index with references to full-text files) ---
    index_parts = [f"# {site_name}\n\n"]
    if site_description:
        index_parts.append(f"> {site_description}\n\n")
    if INTRO_BLOCK:
        index_parts.append(f"{INTRO_BLOCK}\n")

    # Reference to full-text files so LLMs can fetch them
    index_parts.append("## Full documentation\n")
    if site_url:
        index_parts.append(f"- [All sections]({site_url}/llms-full.txt): Complete content for all included sections")
        for section, filename in section_files.items():
            index_parts.append(f"- [{section}]({site_url}/{filename}): Full content for {section}")
    index_parts.append("")

    # Per-section page index
    for section, pages in groups.items():
        index_parts.append(f"## {section}\n")
        for page in pages:
            entry = f"- [{page['title']}]({page['url']})"
            if page["description"]:
                entry += f": {page['description']}"
            if page["keywords"]:
                entry += f" [{', '.join(page['keywords'])}]"
            index_parts.append(entry)
            for label, url in page["resources"]:
                index_parts.append(f"  - {label}: {url}")
        index_parts.append("")  # blank line after section

    (site_dir / "llms.txt").write_text("\n".join(index_parts), encoding="utf-8")

    section_count = len(groups)
    print(
        f"Generated llms.txt, llms-full.txt, and {section_count} section file(s) "
        f"({page_count} pages in {section_count} sections)"
    )


# -----------------------------------------------------------------------------
# Nav walker
# -----------------------------------------------------------------------------

def _walk_nav(items, breadcrumb=None):
    """Recursively walk MkDocs nav, yielding (breadcrumb, title, rel_path) for each leaf page."""
    if breadcrumb is None:
        breadcrumb = []
    for item in items:
        if isinstance(item, str):
            # Bare path without a title
            if not item.startswith(("http://", "https://")):
                yield (breadcrumb, None, item)
        elif isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, str):
                    # Leaf page or external link
                    if not value.startswith(("http://", "https://")):
                        yield (breadcrumb, key, value)
                elif isinstance(value, list):
                    # Subsection
                    yield from _walk_nav(value, breadcrumb + [key])


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _slugify(text: str) -> str:
    """Turn a section name like 'Agriculture > Analytic catalog' into 'agriculture-analytic-catalog'."""
    text = text.lower()
    text = re.sub(r"[>\-/]", " ", text)
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", "-", text.strip())
    return text


def _extract_title(content: str, rel_path: Path) -> str:
    """Extract the first H1 heading or fall back to the file path."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        title = re.sub(r"[*_`]", "", title)
        return title
    return rel_path.stem.replace("_", " ").title()


def _extract_description(content: str) -> str:
    """Extract a one-line description from frontmatter or first paragraph."""
    # Try frontmatter description field
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm_match:
        desc_match = re.search(r"^description:\s*(.+)$", fm_match.group(1), re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip().strip("'\"")
            if desc:
                return desc

    # Fallback: first non-empty paragraph after frontmatter and headings
    body = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, count=1, flags=re.DOTALL)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    for block in re.split(r"\n{2,}", body):
        block = block.strip()
        if not block:
            continue
        # Skip headings, images, HTML, admonitions, tables, annotations
        if block.startswith(("#", "!", "<", "---", "??", "{", "|")):
            continue
        # Clean inline markdown
        line = re.sub(r"[*_`]", "", block)
        line = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", line)
        line = " ".join(line.split())
        if len(line) > 200:
            line = line[:197] + "..."
        return line
    return ""


def _extract_keywords(content: str) -> list[str]:
    """Extract keywords from frontmatter YAML list or comma-separated string."""
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if not fm_match:
        return []

    fm = fm_match.group(1)

    # YAML list format:  keywords:\n  - foo\n  - bar
    list_match = re.search(r"^keywords:\s*\n((?:\s+-\s+.+\n?)+)", fm, re.MULTILINE)
    if list_match:
        return [
            item.strip().strip("'\"")
            for item in re.findall(r"^\s+-\s+(.+)$", list_match.group(1), re.MULTILINE)
            if item.strip()
        ]

    # Inline list format:  keywords: [foo, bar]
    inline_match = re.search(r"^keywords:\s*\[(.+)\]\s*$", fm, re.MULTILINE)
    if inline_match:
        return [k.strip().strip("'\"") for k in inline_match.group(1).split(",") if k.strip()]

    # Comma-separated string:  keywords: foo, bar
    str_match = re.search(r"^keywords:\s*(.+)$", fm, re.MULTILINE)
    if str_match:
        val = str_match.group(1).strip().strip("'\"")
        if val:
            return [k.strip() for k in val.split(",") if k.strip()]

    return []


def _extract_resources(content: str) -> list[tuple[str, str]]:
    """Extract notebook, folder, and demo badge references as external resource links."""
    resources = []
    for match in re.finditer(r"<!--\s*md:(notebook|folder|demo)\s+(.+?)\s*-->", content):
        badge_type = match.group(1)
        badge_arg = match.group(2).strip()

        if badge_type == "notebook":
            label = "Notebook"
            if "/" in badge_arg:
                label += f" ({badge_arg.rsplit('/', 1)[1]})"
            url = f"https://github.com/earthdaily/Examples-and-showcases/blob/main/{badge_arg}.ipynb"
        elif badge_type == "folder":
            label = f"Examples ({badge_arg})"
            url = f"https://github.com/earthdaily/Examples-and-showcases/tree/main/Analytics%20as%20a%20service/{badge_arg}"
        elif badge_type == "demo":
            label = f"Demo ({badge_arg})"
            url = f"https://github.com/earthdaily/{badge_arg}"
        else:
            continue

        resources.append((label, url))
    return resources


def _clean_markdown(content: str) -> str:
    """Strip non-textual elements from markdown to keep content lean."""
    # Remove YAML front matter
    content = re.sub(r"^---\s*\n.*?\n---\s*\n", "", content, count=1, flags=re.DOTALL)
    # Remove HTML comments (including shortcode badges)
    content = re.sub(r"<!--.*?-->", "", content, flags=re.DOTALL)
    # Remove HTML tags
    content = re.sub(r"<[^>]+>", "", content)
    # Remove images
    content = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", content)
    # Remove admonition / details fences but keep their content
    content = re.sub(r"^!!!.*$", "", content, flags=re.MULTILINE)
    content = re.sub(r"^\?\?\?[+]?.*$", "", content, flags=re.MULTILINE)
    # Remove annotation markers like { .annotate }
    content = re.sub(r"^\{[^}]*\}\s*$", "", content, flags=re.MULTILINE)
    # Remove snippet includes
    content = re.sub(r"^--8<--.*$", "", content, flags=re.MULTILINE)
    # Collapse multiple blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()
