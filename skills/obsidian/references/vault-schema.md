# Cortana System — Full Schema Reference

This is the complete architecture and operating manual for the Cortana system. The SKILL.md
gives you the overview; this file gives you every detail you need to execute correctly.

## Table of Contents

1. [System Layout — Vault + Reports](#system-layout)
2. [Vault Directory Structure](#vault-directory-structure)
3. [Reports Directory Structure](#reports-directory-structure)
4. [Page Types and Frontmatter](#page-types-and-frontmatter)
5. [File Routing Decision Tree](#file-routing-decision-tree)
6. [Existing Projects Registry](#existing-projects-registry)
7. [Two-Tier Directory Ingestion Details](#two-tier-directory-ingestion)
8. [Index Management](#index-management)
9. [Watcher Script Architecture](#watcher-script-architecture)
10. [Deep Dive Script Usage](#deep-dive-script-usage)

---

## System Layout

The Cortana system is two parallel folders sharing one Obsidian vault root:

```
~/Cortana/                  ← Obsidian vault root (.obsidian/ here)
├── cortana-vault/          ← The research knowledgebase (data IN)
└── Reports/                ← Synthesized work product (OUT)
```

**Mental model:** the vault is where data lands and gets organized for retrieval — research
topics, project session summaries, YouTube transcripts, raw ingested material. Reports/ is
where polished synthesized analysis ships — single-name equity dossiers, sector baskets, macro
calls, tool evals. They're siblings inside the same Obsidian vault, so search and graph view
span both. Cross-link from vault to Reports with `[[../Reports/...]]`.

---

## Vault Directory Structure

```
cortana-vault/
├── SCHEMA.md              # Human-readable operating manual
├── index.md               # Master index — tables of all projects, Dataview queries
├── log.md                 # Append-only chronological log of all operations
├── projects/              # Project work — one folder per project
│   ├── projects-directory.md
│   └── <project>/
│       ├── <project>.md   # Overview (same name as folder)
│       └── <project>--<item>.md  # Session/source pages
├── research/
│   ├── research-hub.md    # Dataview-powered research directory
│   ├── curricula/         # Learning paths
│   └── topics/            # Deep-dive concept pages — incl. methodology playbooks:
│                          #   bt-equities-playbook.md (Druckenmiller-tier 5-phase)
│                          #   ny-session-frameworks.md (4 intraday archetypes)
│                          #   astrology-trading-framework.md (Gann-tradition risk filter)
├── youtube/
│   ├── youtube-library.md # Video directory
│   ├── queue/             # Pending videos
│   └── transcripts/       # Processed video pages
├── inbox/                 # DROP ZONE — files land here for processing
│   └── README.md          # Usage instructions
├── raw/                   # Immutable source archive
│   ├── sessions/          # Raw Cowork transcripts
│   ├── ingested/          # Archived copies of everything ingested
│   └── assets/            # Images, attachments
├── scripts/
│   ├── vault-watcher.py   # Auto-ingestion daemon
│   ├── deep-dive.py       # On-demand archive materialization
│   ├── requirements.txt   # Python deps: watchdog, requests, PyPDF2, python-frontmatter
│   └── .venv/             # Python virtual environment (Hopper)
├── skills/                # Skill definitions
├── templates/             # Page templates
└── .obsidian/             # (vault-internal config, if Obsidian rooted here)
```

## Reports Directory Structure

```
Reports/                              ← sibling of cortana-vault, NOT inside it
├── Reports.md                        # Top-level hub
├── equities/
│   ├── equities.md                   # Category index
│   ├── YYYY-MM-DD-<ticker>.md        # MD wiki companion
│   ├── YYYY-MM-DD-<ticker>-bt-stock-report.pdf   # PDF
│   └── historical/                   # Externally-ingested research (file:// links)
├── ai-strategy/
│   ├── ai-strategy.md
│   └── historical/
├── macro-regime/
│   ├── macro-regime.md
│   └── historical/
├── sector-theme/
│   ├── sector-theme.md
│   └── historical/
└── tools-evals/
    ├── tools-evals.md
    └── (no historical/ — all tool evals are first-party)
```

**The `historical/` subfolder convention:** reports we author live in the parent category
folder; reports we ingest from external sources live in `historical/` with frontmatter
`historical: true` and `file://` links to the original PDFs (which stay at their host paths,
e.g., `/Volumes/Data/BT_Reports/...`). This keeps Reports/ free of large binary files while
preserving discoverability + cross-link surface.

**Production flow for a new report:**

1. The `bt-equity` skill (or equivalent skill for other report types) produces PDF + companion MD
2. Files land in `Reports/<category>/`
3. The obsidian skill (this one) updates indexes + log + cross-links
4. Companion MD frontmatter ties into vault `[[wikilinks]]` for graph visibility

---

## Page Types and Frontmatter

### Project Overview

```yaml
---
title: "Wick App"
type: project
created: 2026-04-10
updated: 2026-04-10
tags: [🎯, trading, platform, react, typescript]   # emoji category first
status: active
sources: []
related: ["[[projects/nq-trading/nq-trading]]"]
---
```

### Emoji Category Tags

Every page gets exactly ONE emoji tag as the first item in `tags:`. These provide visual scanning in Obsidian's tag pane:

| Emoji | Category | Covers |
|-------|----------|--------|
| 🎯 | Trading | NQ futures, indicators, backtesting, edge, PSO, Gann, Databento |
| 🤖 | AI/Agents | Claude skills, agent architecture, AOS, memory system, mission control |
| 📺 | YouTube | All video transcripts |
| 💼 | Business | Consulting, clients, proposals, finance/admin |
| 🔧 | Infrastructure | Dev environment, deployment, vault tooling |
| 📚 | Research | Curricula, deep dives, data science |

Pick the primary category based on the page's parent project.

### Session Summary

```yaml
---
title: "Fix Chart Explorer Rendering"
type: session
created: 2026-04-10
updated: 2026-04-10
tags: [🎯, wick-app, chart, bugfix]
status: completed
project: "[[projects/wick-app/wick-app|Wick App]]"
session_id: "abc123"
sources: ["raw/sessions/session-abc123.jsonl"]
related: []
---
```

### Directory Overview (Tier 1)

```yaml
---
title: "Claude Skills Library"
type: project
created: 2026-04-10
updated: 2026-04-10
tags: [🤖, claude-skill, library, reference]
status: active
source_dir: "claude-skills-main"
total_files: 3418
archive: "raw/ingested/claude-skills-main"
sources: ["claude-skills-main"]
related: []
---
```

### Research Curriculum

```yaml
---
title: "Particle Swarm Optimization for Trading"
type: curriculum
created: 2026-04-10
updated: 2026-04-10
tags: [🎯, pso, optimization, trading]
status: draft
source_url: "https://example.com/article"
estimated_hours: 12
related: ["[[projects/pso-research/pso-research]]"]
---
```

### YouTube Transcript

```yaml
---
title: "Market Microstructure Deep Dive"
type: youtube
created: 2026-04-10
updated: 2026-04-10
tags: [📺, trading, microstructure]
status: processed
url: "https://youtube.com/watch?v=..."
channel: "QuantChannel"
duration: "45:30"
published: "2026-03-15"
relevance: high
related: ["[[projects/nq-trading/nq-trading]]"]
---
```

### Report (Reports/ — synthesized work product, NOT in cortana-vault)

```yaml
---
title: "$VIAV · Viavi Solutions — BT Stock Report (Apr 2026)"
type: report
report_type: equities | ai-strategy | macro-regime | sector-theme | tools-evals
historical: true     # ONLY if ingested from external source
ticker: VIAV         # equities only
company: "Viavi Solutions Inc."
exchange: NASDAQ
date: 2026-04-27
created: 2026-04-27
updated: 2026-04-27
tags: [🎯, equities, ai-infrastructure, optical-test, druckenmiller-tier]
status: active | archived
spot: "$43.86"
market_cap: "~$10.1B"
bucket: "AI infra test / data-center optical / defense PNT"
horizon: "6–24 months"
pdf: "2026-04-27-viav-bt-stock-report.pdf"   # relative if PDF is alongside
                                              # OR: file:///Volumes/... for ingested
sources: []
related: [[adjacent reports]], [[vault topics]]
---
```

---

## File Routing Decision Tree

```
Is this DATA (research, source, methodology) or SYNTHESIS (opinionated dated analysis)?

DATA → cortana-vault/
├── Is it a directory?
│   └── YES → Two-Tier Ingestion (Tier 1 auto, Tier 2 on-demand)
│              Output: projects/<slug>/<slug>.md (single overview)
│              Archive: raw/ingested/<dirname>/
└── NO → Single file
    ├── YouTube URL/transcript? → youtube/transcripts/<slug>.md
    ├── Trading methodology / playbook (BT Equities Playbook, etc.)? → research/topics/<slug>.md
    ├── Research/learning material on a concept? → research/topics/<slug>.md
    ├── Matches existing project? → projects/<project>/<project>--<slug>.md
    ├── Defines a new project? → Create projects/<new-slug>/<new-slug>.md + source page
    └── Unclear? → research/topics/<slug>.md (safe default)

SYNTHESIS → ~/Cortana/Reports/
├── Single-name equity thesis? → Reports/equities/YYYY-MM-DD-<ticker>.md (+ PDF)
├── AI infrastructure / model launch / hyperscaler thesis? → Reports/ai-strategy/...
├── Fed / regime / dollar / treasuries call? → Reports/macro-regime/...
├── Multi-name basket / sector rotation? → Reports/sector-theme/...
├── Tool / framework eval (with adopt recommendation)? → Reports/tools-evals/...
└── Externally ingested (someone else's research PDF)? → Reports/<category>/historical/
   with frontmatter historical: true + file:// link to original
```

**Methodology vs. synthesis is the trickiest line.** A document explaining bang's *own* trading
playbook (NY Session Frameworks, Astro Risk Filter, BT Equities Playbook) is methodology — it
goes in `cortana-vault/research/topics/` because it's an INPUT to future analysis, not an
output. A document that *applies* that methodology to a specific name (e.g., a BT Stock Report
on $VIAV) is synthesis — it goes in `Reports/equities/`.

---

## Existing Projects Registry

Check these before creating new projects. If incoming material fits an existing project, file
it there instead of creating a new one.

| Slug | Domain | Description |
|------|--------|-------------|
| wick-app | Trading | Flagship trading platform (React/TS) |
| nq-trading | Trading | NQ/MNQ futures edge development |
| gann-indicator | Trading | Gann square indicator PRD |
| bt-aggression | Trading | Aggression analysis engine |
| pso-research | Trading | Particle swarm optimization |
| databento | Trading | CME futures market data |
| aos-platform | Platform | Enterprise agent platform |
| mission-control | Platform | Orchestration control plane |
| memory-system | Platform | Multi-user pattern recognition |
| claude-skills | Platform | Active skill integration |
| claude-skills-library | Platform | Reference catalog of 517 skills |
| dev-environment | Platform | Dev tooling setup |
| southbay-ai | Business | AI consulting practice |
| summer-fridays | Business | Competitive analysis |
| merida-perfume | Business | Luxury perfume B2B |
| father-daughter-adventures | Business | Adventure service |
| web-design-clients | Business | Client websites |
| vail-proposal | Business | AI infrastructure proposal |
| finance-admin | Finance | Tax, banking, email, budgeting |

---

## Two-Tier Directory Ingestion

### Tier 1: Scanning

When scanning a directory, collect:

1. **Total file count** and **extension breakdown** (e.g., `.md: 235, .py: 67, .json: 45`)
2. **Subdirectory list** with per-subdir file counts
3. **Directory tree** — 3 levels deep, show first 5 files per level, count the rest
4. **Samples** — 15-20 representative files (spread across subdirs), first 2000 chars each

### Tier 1: Summary Generation

Feed the scan data to the LLM and ask for:

```json
{
  "title": "Human-readable title",
  "one_liner": "One sentence — what IS this?",
  "summary": "2-4 paragraph overview",
  "categories": [
    {"name": "category", "description": "what's here", "file_count": 42,
     "standout_items": ["notable-item-1", "notable-item-2"]}
  ],
  "highlights": ["5-8 most interesting/useful items with brief why"],
  "relevance_to_trading": "Connection to bang's work",
  "search_keywords": ["15-20 searchable terms"],
  "tags": ["tag1", "tag2"],
  "recommended_deep_dives": ["Items worth materializing into full pages"]
}
```

### Tier 1: Overview Page Structure

The overview page should contain:
- One-liner summary as a blockquote
- Source/archive/date metadata line
- Overview section (the summary paragraphs)
- Categories section (bulleted list with standout items)
- Highlights section
- Relevance section
- Recommended Deep Dives with `> [!tip]` callout showing deep-dive.py commands
- Directory structure (code block)
- Search keywords (comma-separated, for Obsidian's search index)

### Tier 2: Deep Dive Materialization

When materializing a specific item from an archived directory:

1. Locate in `raw/ingested/<archive-name>/<path>`
2. Read full content
3. Generate detailed page with: one-line summary, detailed explanation, key takeaways,
   relevance to trading/AI, related concepts as wikilinks
4. Save as `projects/<project>/<project>--<item-slug>.md`
5. Log the operation

---

## Index Management

### Vault indexes

#### index.md

The master index uses Obsidian tables organized by domain (Trading & Markets, Platform &
Infrastructure, Business & Consulting, Finance & Admin). Each row has Project, Status,
Description. It also has Dataview query blocks for research curricula and YouTube library,
and a Reports section linking out to `[[../Reports/...]]`.

**When to update:** Any time a new project is created or a project's status changes.

#### projects-directory.md

A simpler bulleted list of all projects by domain, with session counts.

**When to update:** Any time a new project is created.

#### log.md

Append-only. Never modify existing entries. Format:

```markdown
## [YYYY-MM-DD] type | Title

- **type**: ingest | ingest (directory → compact overview) | deep-dive | session | research | youtube | lint | query
- **source**: filename or directory name
- **details**: What was done
- **pages created**: count
- **pages touched**: [[wikilink1]], [[wikilink2]]
```

### Reports indexes

#### Reports/Reports.md (top-level hub)

A markdown hub describing the categories + recent reports. Has a "Recent Reports" table that
should be kept current (newest at top, ~10 entries).

**When to update:** Every new report — add a row to "Recent Reports", trim the table back
to ~10 if it's growing past that.

#### Reports/<category>/<category>.md (category index)

One per category — equities.md, ai-strategy.md, etc. Has a Reports table with all reports in
the category. For equities, also has "Open Theses by Bucket" sub-section grouping reports by
thesis cluster, and a "Watchlist" section for names being researched but not yet written up.

**When to update:** Every new report in that category.

#### cortana-vault/index.md — Reports section

The vault index has a "Reports — Synthesized Work Product" section that links out to each
category and surfaces the most recent N reports. Update the recent-reports list when new
reports ship.

#### cortana-vault/log.md (also tracks Reports operations)

Reports/ creation, ingestion, and migration go in the same log.md as vault operations. Use
type `ingest` (for ingested research) or new types `report-create`, `report-update` for
authored reports. The pages-touched list should include cross-paths (`[[../Reports/...]]`).

---

## Watcher Script Architecture

`scripts/vault-watcher.py` is a Python daemon using the `watchdog` library. Key architecture:

- **API:** OpenAI-compatible chat completions (works with LM Studio, Ollama, OpenAI, etc.)
- **Default endpoint:** `http://localhost:1234/v1` (LM Studio, which may proxy via LM Link)
- **Default model:** `google_gemma-4-26b-a4b-it`
- **SETTLE_TIME:** 2 seconds (waits for large file copies to finish)
- **Dedup:** MD5 hash of filename + size + mtime, stored in `scripts/.processed`

Modes:
- `--process-once` — scan inbox, process everything, exit
- Default — watch mode with filesystem event handler

The watcher handles individual files (full LLM classify → wiki page) and directories (two-tier
scan → single overview page). It does NOT require this skill — it's standalone Python.

---

## Deep Dive Script Usage

`scripts/deep-dive.py` — CLI tool for Tier 2 materialization.

```bash
# List contents of an archive
python scripts/deep-dive.py <archive-name> --list

# Search by keyword (searches filenames + content)
python scripts/deep-dive.py <archive-name> --search "keyword"

# Materialize one file
python scripts/deep-dive.py <archive-name> "path/to/file"

# Materialize entire subdirectory
python scripts/deep-dive.py <archive-name> "subdirectory/" --all

# Custom LLM endpoint
python scripts/deep-dive.py <archive-name> "file" --api-base http://host:port/v1
```

It automatically finds the associated project directory by reading frontmatter from existing
overview pages. If no project exists, it creates one from the archive name.
