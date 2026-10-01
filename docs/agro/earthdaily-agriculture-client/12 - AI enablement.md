---
title: AI enablement
description: How the package ships CLAUDE.md memory, an /earthdaily-agriculture skill, and per-extractor agent cards so AI coding assistants stay productive on your project.
#icon: material/robot-outline
keywords:
  - CLAUDE.md
  - claude code
  - cursor
  - copilot
  - ai
  - skill
  - agents
  - generate_ai_context
---

# AI enablement

Every extractor in this package follows the same shape — `setup_*_parameters()` → `get_*_api()` → `format_*_json()` → `process_*_bulk_parallel()` — but the *details* differ heavily: required entity fields, default parameters, output columns, KPI lists, gotchas. An AI coding assistant (Claude Code, Cursor, Copilot Chat) can't reliably guess those; it has to read source. Reading source for every question is slow, burns tokens, and tends to drift onto the wrong extractor.

This package ships three layers of pre-flattened context so AI assistants pick up the right extractor and configure it correctly without you hand-feeding them the manual:

| Channel                          | When loaded                                     | What's in it                                                                                |
| -------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `CLAUDE.md` (your project)        | Every turn (always-on)                         | Short, durable framing — package purpose, environment, workspace layout, key design rules    |
| `.claude/skills/earthdaily-agriculture/` (skill)  | When you type `/earthdaily-agriculture` or the description matches | Extractor decision table, paste-ready recipes, common pitfalls                          |
| Per-extractor cards               | On demand by tools that read them               | Full per-extractor cards (parameters, entity fields, output columns, methods)               |

All three are produced from a single source of truth: the **structured docstrings on each extractor class**.

---

## Out of the box: what gets generated automatically

If you scaffold your project from the cookiecutter template (see [`01 - Quick_Start_Guide.md`](01%20-%20Quick_Start_Guide.md)), the post-generation hook runs at project creation time and writes:

- `<your_project>/CLAUDE.md` — small (~30 lines) project-flavoured project memory: env (`prod`/`preprod`), package version, workspace layout, pointer to the `/earthdaily-agriculture` skill.
- `<your_project>/.claude/skills/earthdaily-agriculture/SKILL.md` — the skill body: YAML front matter, an auto-generated extractor decision table grouped by category, paste-ready Python and YAML recipes, common pitfalls.
- `<your_project>/.claude/skills/earthdaily-agriculture/extractors.md` — full per-extractor cards.

Drop your project into Claude Code and the always-on `CLAUDE.md` plus the on-demand `/earthdaily-agriculture` skill cover most of what an assistant needs to know.

If you didn't use the cookiecutter template, you can run the generator yourself any time:

```bash
python -m earthdaily.agriculture.ai_enablement.generate_ai_context --project-target .
```

(Replace `.` with the path to your project if you're running from elsewhere.)

---

## Source of truth — extractor docstrings

The convention every extractor follows (see `CoverageExtractor` for the canonical example):

```python
class CoverageExtractor(BaseExtractor):
    """One-line description on the first line. A short paragraph follows
    explaining what the extractor does and when to use it.

    Documentation: https://docs.earthdaily.com/agro/earthdaily-agriculture/coverage/
    Notebook: EDAgriculture_coverage_Function_Dev.ipynb

    Args:
        vegetation_index (str): Vegetation index name. Default: "NDVI"
        start_date (str): ISO date. Default: None
        ...

    Entity fields:
        - id, geometry

    Output columns:
        - image_id, coverage_percent, date, mask, sensor, spatial_resolution
    """
```

Five sections matter (`Documentation:`, `Notebook:`, `Args`, `Entity fields`, `Output columns:`). The generator parses them and writes structured reference docs out of them.

Practical upshot: AI assistants get a reliable, machine-readable contract for every extractor without you having to write a separate spec.

---

## Layer 1 — `CLAUDE.md` (always-on memory)

`CLAUDE.md` files in your project root and inside the package's own repo are loaded automatically into Claude Code's context every turn. That makes them expensive — every line costs tokens forever — so they're kept short and durable.

### What's in your project's `CLAUDE.md`

After the post-gen hook runs (or you ran `generate_ai_context.py --project-target .`):

- Which environment the project targets (`prod` vs `preprod`)
- Which package version is pinned
- Where inputs/outputs/cache live
- That the `/earthdaily-agriculture` skill exists for the deep reference

Deliberately minimal — it doesn't repeat the package's internal documentation, because your project doesn't need to know how `BaseExtractor` works internally. It needs to know what to use and where to look for more.

### When to regenerate

After bumping the package version, after adding a new transform module under `app/`, or any time the layout of your project changes.

```bash
python -m earthdaily.agriculture.ai_enablement.generate_ai_context --project-target .
```

---

## Layer 2 — `/earthdaily-agriculture` skill (on-demand)

Skills are markdown files Claude Code loads only when invoked by name (`/earthdaily-agriculture`) or matched against your request via the skill's `description`. They cost nothing until used, which makes them ideal for *deep* content that's only relevant to specific tasks.

### Two variants you can install

| Variant                  | Lives at                                | Triggers                                        | Install via                                                                                       |
| ------------------------ | --------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Project-local `/earthdaily-agriculture`  | `<project>/.claude/skills/earthdaily-agriculture/`       | Inside that one project                          | Cookiecutter post-gen hook (automatic), or `generate_ai_context --project-target .`                |
| Personal `/earthdaily-agriculture` | `~/.claude/skills/earthdaily-agriculture/`         | Any project on the machine, including scratch dirs | `python -m earthdaily.agriculture.ai_enablement.generate_ai_context --personal-skill-target ~/.claude/skills/earthdaily-agriculture` (run once) |

Both coexist cleanly — the project-local one wins inside a project that has it; the personal one fires everywhere else.

### What's in the skill

Three layers, in this order:

1. **Decision table** — auto-generated from the package's extractor registry, grouped by category. Lets the assistant scan and pick the right extractor for the task.
2. **Recipes** — two paste-ready snippets (direct extractor mode + YAML workflow step) covering the 90 % use cases.
3. **Common pitfalls** — short, recurring gotchas (`clear_cover_min=100` too strict, missing `column_mapping` for platform DataFrames, LAI requires `crop`, etc.).

For *anything* deeper (a specific extractor's full parameter list, output columns, methods), the skill points the assistant at `extractors.md` in the same directory.

### Personal skill runbooks

The personal `/earthdaily-agriculture` skill also ships five runbooks under `~/.claude/skills/earthdaily-agriculture/runbooks/`:

| Runbook                       | When the assistant pulls it                                                              |
| ----------------------------- | ---------------------------------------------------------------------------------------- |
| `setup_client_notebook.md`    | Stand up a new notebook against the package — Step 0 → Step 3 layout                      |
| `debug_api_response.md`       | Empty result, Series-truthiness, token expiry, column-mapping mismatch, retry-on-400 misuse |
| `add_service_extractor.md`    | Subclass `BaseExtractor` for a new sync API                                              |
| `add_processor_extractor.md`  | Same for the submit-poll-retrieve async pattern                                          |
| `regenerate_context.md`       | When and how to re-run the generator across the three target modes                       |

---

## Layer 3 — Cookiecutter post-gen hook

When you create a project via the cookiecutter template, `project_template/hooks/post_gen_project.py` runs once immediately after the project directory is rendered. It shells out to `generate_ai_context.py --project-target <new-project>` and lets the script do all the work.

### Failure modes — fail soft, not blocking

- **Source path missing** (e.g. fresh checkout on a teammate's machine where `edagro_source_path` in `cookiecutter.json` is wrong): hook prints a warning with the exact command to re-run later.
- **Introspection fails** (deps missing): hook prints a warning; the project is created without the generated context. Re-run the script after `pip install -r requirements.txt`.
- **Network / filesystem issues**: subprocess returns non-zero → warning, project still created.

The principle is: **never block project creation on AI-context generation**. The project is the deliverable; the AI context is a convenience.

---

## The generator — `generate_ai_context.py`

Single Python module shipped with the package. Three modes, mutually exclusive — passing a target flag picks the mode:

### Project mode — `--project-target PATH`

Writes the project-flavoured `CLAUDE.md` plus the `/earthdaily-agriculture` skill into a project directory.

```bash
python -m earthdaily.agriculture.ai_enablement.generate_ai_context \
  --project-target /path/to/my_project \
  --project-name "My Project" \
  --environment prod
```

Writes:

- `<target>/CLAUDE.md`
- `<target>/.claude/skills/earthdaily-agriculture/SKILL.md`
- `<target>/.claude/skills/earthdaily-agriculture/extractors.md`

### Personal mode — `--personal-skill-target PATH`

Installs the personal `/earthdaily-agriculture` skill at `~/.claude/skills/earthdaily-agriculture/` so it fires anywhere on your machine, including scratch directories and ad-hoc notebooks.

```bash
python -m earthdaily.agriculture.ai_enablement.generate_ai_context \
  --personal-skill-target ~/.claude/skills/earthdaily-agriculture
```

Writes the `SKILL.md`, `extractors.md`, and the five runbooks listed above.

Run this once per developer machine. Re-run after a package upgrade to refresh the extractor reference embedded in the skill.

### Default mode — no target

Writes the package's own `CLAUDE.md` and `agents.md` (used by maintainers). Not needed for end-user projects.

---

## Lifecycle — keeping context fresh

| Event                                            | What to do                                                                                                       |
| ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| You upgrade `earthdaily-agriculture`             | Re-run `generate_ai_context --project-target .` in each project, and `--personal-skill-target ~/.claude/skills/earthdaily-agriculture` once. New extractors / new params land automatically. |
| You add a transform module under `app/`           | Re-run the project-target generator so `CLAUDE.md` reflects the new module layout.                                |
| Claude makes a recurring mistake on your project  | Add a one-liner to the "Common pitfalls" section of your project's `CLAUDE.md`. It's hand-editable below the auto-generated block. |

---

## Design principles in one paragraph

**Generate, don't duplicate.** The extractor docstrings are the source of truth; everything else is derived. **Split by load cost.** Always-on context (`CLAUDE.md`) stays short and durable; deep reference (`/earthdaily-agriculture` skill) loads on demand. **Project-flavoured, not package-flavoured, in your project.** Your project's `CLAUDE.md` tells the assistant what *your* project needs to know, not how `BaseExtractor` works internally. **Fail soft.** If context generation fails for any reason, the project is still created and still works.
