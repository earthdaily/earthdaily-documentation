from __future__ import annotations

import os
import re
from pathlib import Path
from mkdocs.config.defaults import MkDocsConfig

# -----------------------------------------------------------------------------
# Configuration - folders to include in llms.txt (relative to docs/)
# -----------------------------------------------------------------------------

INCLUDE_FOLDERS = [
    "Agro",
    "App",
    "Support",
    "QGIS",
]

# -----------------------------------------------------------------------------
# Hook
# -----------------------------------------------------------------------------

def on_post_build(config: MkDocsConfig):
    """
    Generate llms.txt at the root of the built site.
    Aggregates markdown content from the configured folders.
    """
    docs_dir = Path(config["docs_dir"])
    site_dir = Path(config["site_dir"])
    site_name = config.get("site_name", "EarthDaily documentation")
    site_description = config.get("site_description", "")
    site_url = config.get("site_url", "")

    sections: list[str] = []

    for folder in INCLUDE_FOLDERS:
        folder_path = docs_dir / folder
        if not folder_path.is_dir():
            continue

        md_files = sorted(folder_path.rglob("*.md"))
        if not md_files:
            continue

        for md_file in md_files:
            rel_path = md_file.relative_to(docs_dir)
            content = md_file.read_text(encoding="utf-8", errors="replace")

            title = _extract_title(content, rel_path)
            body = _clean_markdown(content)

            if not body.strip():
                continue

            # Build the URL path from the file path
            url_path = str(rel_path.with_suffix("")).replace("\\", "/") + "/"
            if url_path.endswith("index/"):
                url_path = url_path.replace("index/", "")

            page_url = f"{site_url.rstrip('/')}/{url_path}" if site_url else ""

            section = f"## {title}\n"
            if page_url:
                section += f"URL: {page_url}\n"
            section += f"\n{body}\n"
            sections.append(section)

    # Assemble llms.txt
    header = f"# {site_name}\n\n"
    if site_description:
        header += f"> {site_description}\n\n"

    output = header + "\n---\n\n".join(sections)

    output_path = site_dir / "llms.txt"
    output_path.write_text(output, encoding="utf-8")
    print(f"Generated llms.txt ({len(sections)} pages)")


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _extract_title(content: str, rel_path: Path) -> str:
    """Extract the first H1 heading or fall back to the file path."""
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove markdown formatting from title
        title = re.sub(r"[*_`]", "", title)
        return title
    return rel_path.stem.replace("_", " ").title()


def _clean_markdown(content: str) -> str:
    """Strip non-textual elements from markdown to keep llms.txt lean."""
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
    # Collapse multiple blank lines
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()
