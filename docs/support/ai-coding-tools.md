---
title: AI Coding tool
description: This section will provide details on how to use Earthdaily analytics service with AI coding tools.
keywords:
  - AI coding tools
  - CLAUDE.md
  - AGENTS.md
  - llms.txt
  - Cursor
  - MCP connector
hide:
  - navigation
  - toc
---

# AI Coding Tools Integration

AI coding assistants generate better content when they have project-specific context. Each tool reads a different configuration file at session start. EDA provides ready-to-use files for both, generated directly from the extractor source code.

<div class="grid cards" markdown>

-   :material-file-document-outline: **llms.txt**

    Full AI context bundle hosted on the docs site. Use as a URL reference or Claude connector. 
    Please copy and paste in our AI tool

    <button class="md-button md-button--secondary" onclick="navigator.clipboard.writeText('https://docs.earthdaily.com/llms.txt').then(function(){var b=this;b.textContent='Copied!';setTimeout(function(){b.textContent='Copy link'},2000)}.bind(this))">Copy URL</button> 

-   :simple-anthropic: **CLAUDE.md**

    Context file for **Claude Code** (Anthropic). Drop it in your repo root — auto-loaded at session start.

    [:octicons-download-16: Coming soon](https://github.com/earthdaily){ .md-button }

-   :material-robot-outline: **AGENTS.md**

    Context file for **Codex, Cursor, Aider** and any tool supporting the AGENTS.md standard.s

    [:octicons-download-16: Coming soon](https://github.com/earthdaily){ .md-button }

</div>

---

## Overview

| Tool | Config file | Auto-loaded | Also read by |
|---|---|---|---|
| **Claude Code** (Anthropic) | `CLAUDE.md` | ✅ Yes | Claude Code only |
| **Codex CLI / Agent** (OpenAI) | `AGENTS.md` | ✅ Yes | Cursor · Aider · Builder.io |

!!! warning "Two files, not one"
    Neither tool reads the other's configuration file. If your team uses both Claude Code
    and Codex, place both `CLAUDE.md` and `AGENTS.md` in your repo root.
    EDA ships both — they share the same core content.

---

## Tool Compatibility

| Tool | `CLAUDE.md` | `AGENTS.md` | MCP connector | `llms.txt` via URL |
|---|---|---|---|---|
| Claude Code | ✅ Native | ✗ | ✅ Native | ✅ Via `CLAUDE.md` ref |
| Claude.ai (web) | ✗ | ✗ | ✅ Settings → Connectors | ✅ Paste URL in chat |
| Codex CLI / Agent | ✗ | ✅ Native | ⚡ stdio only | ✅ Via `AGENTS.md` ref |
| Cursor | ✗ | ✅ Native | ✅ | ✅ Paste URL |
| Aider | ✗ | ✅ Native | ✗ | ⚡ Manual |
| GitHub Copilot | ✗ | ✗ | ✗ | ⚡ Manual paste |

---

## Setup in 3 Steps

**1. Download and place the file(s) in your repo root**

Drop `CLAUDE.md` for Claude Code, `AGENTS.md` for Codex/Cursor, or both if your team
uses multiple tools. No other configuration is required — each tool picks up its file
automatically at session start.

**2. Start your AI session as normal**

Run `claude` or `codex` in your project directory. The tool loads the context file before
your first prompt. Verify it was read by asking:

> *"What EarthDaily does in mining?"*

<!-- **3. Optionally add the Claude connector for persistent access**

In Claude.ai, go to **Settings → Connectors → Add custom connector** and enter
`https://docs.eda.com/mcp`. This gives every Claude conversation live access to EDA
extractor knowledge without needing any file in the repo. -->

---

## Where Files Live

Depending on your setup, files can live in the extractor repo, in the client's project
repo, or just as a hosted URL — they don't all need to be in the same place.

| Artifact | Lives in | Maintained by | Updated |
|---|---|---|---|
| `CLAUDE.md` / `AGENTS.md` | Client's repo | Client (one-time copy) | On major EDA API changes |
| `llms.txt` bundle | EDA docs site | EDA CI pipeline | Automatically on every build |
| MCP connector | Claude settings | Each developer, once | Never — always live |

!!! info
    The bundle is the single source of truth. The config files are lightweight wrappers
    that reference it. Once the MCP connector is added to Claude settings, `CLAUDE.md`
    becomes optional — Claude already has full context before the repo is opened.
