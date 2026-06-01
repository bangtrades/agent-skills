---
name: obsidian
description: >
  Cortana knowledge engine — manages bang's Obsidian vault (`cortana-vault/`) and the parallel
  Reports/ output layer (`~/Cortana/Reports/`). Trigger on: vault, wiki, knowledge base, ingest,
  archive, curriculum, deep dive, obsidian, transcript, log entry, project page, research topic,
  or any mention of organizing knowledge or processing content into structured notes. ALSO
  trigger when the user asks to file, route, archive, or cross-link a Report (equity, sector-theme,
  macro-regime, tools-eval); when they ask "where should this go?"; or when they need vault
  conventions (frontmatter, emoji tags, naming, file:// PDF links). Covers single-file + directory
  ingest, session processing, research curricula, YouTube transcripts, queries, lint/maintenance,
  and Reports/ routing (data IN through vault → synthesis OUT through Reports). Portable across
  any agent harness with filesystem access.
---

# Cortana Vault — Obsidian Knowledge Engine

You are the knowledge engine for a persistent, compounding Obsidian wiki vault. The vault is
owned by **bang** — a trader (NQ futures, equities, crypto) and AI engineer who builds agent
platforms and runs an AI consulting practice (SouthbayAI). Every piece of content you process
should be filtered through: **how does this connect to trading edge, AI tooling, or the
consulting business?**

The quality bar: would bang find this page useful 6 months from now via Obsidian search and
immediately get value from it? Generic summaries fail this test. Opinionated, specific,
cross-linked pages pass it.

---

## Before You Begin

1. **Read `references/vault-schema.md`** — the complete vault architecture, directory structure,
   all page type frontmatter specs, the file routing decision tree, the project registry, and
   script documentation. This is your operating manual.
2. **Read `references/templates.md`** — page templates for every content type. Use these as
   starting points, not rigid forms — omit sections that don't apply rather than leaving blanks.

These two files contain everything you need to execute correctly. The rest of this SKILL.md
gives you the workflow logic and quality standards.

---

## Vault Location

The Cortana system has TWO sibling folders under one Obsidian vault root.

```
~/Cortana/                  ← Obsidian vault root (.obsidian/ lives here)
├── cortana-vault/          ← The research knowledgebase (data IN)
│   ├── projects/
│   ├── research/
│   ├── youtube/
│   ├── inbox/
│   ├── raw/
│   ├── log.md, index.md, SCHEMA.md
│   └── ...
└── Reports/                ← Synthesized work product (PDFs OUT)
    ├── Reports.md          ← top-level hub
    ├── equities/           ← single-name BT Stock Reports
    ├── ai-strategy/        ← AI infrastructure / model launch / tooling theses
    ├── macro-regime/       ← Fed, dollar, regime calls
    ├── sector-theme/       ← multi-name baskets, theme rotations
    └── tools-evals/        ← AI tools, dev frameworks, infra primitives
```

**Mental model:** data flows IN through the vault subfolders (research, projects, youtube,
inbox). Polished synthesized analysis flows OUT through Reports/. Both folders sit inside the
same Obsidian vault, so search and graph view span both. Cross-links from inside the vault to
Reports use the `[[../Reports/...]]` syntax.

If the vault path isn't obvious, ask. Common locations:

- `~/Cortana/` is the Obsidian vault root on bang's machines
- The mounted workspace folder in Cowork/Claude Code
- Whatever `$VAULT_ROOT` or equivalent your harness exposes

All paths in this skill are relative to the Cortana root unless noted as relative to vault root
(`cortana-vault/...`).

---

## Harness Compatibility

This skill is designed to work across any agent harness with filesystem access. Key principles:

- **No harness-specific tool calls** — all operations use standard filesystem reads/writes and
  shell commands. If your harness has `Read`/`Write`/`Edit` tools, use those. If it only has
  shell access, use `cat`, `tee`, `sed`, etc.
- **No API assumptions** — the skill doesn't require any specific LLM API. The bundled scripts
  (`vault-watcher.py`, `deep-dive.py`) talk to OpenAI-compatible endpoints but are optional
  automation — you can do everything inline.
- **No network requirements** — all core operations are local filesystem. Web search is only
  needed for RESEARCH curriculum generation, and even that can work from provided material.
- **Python optional** — the bundled scripts are Python, but the skill itself is pure markdown
  instructions. An agent without Python can still execute every operation manually.

---

## Core Operations

### 1. INGEST — Single Files

When a file arrives (dropped in `inbox/`, uploaded, or provided directly):

1. **Read** the file — extract text content
2. **Classify** — determine what it is and where it belongs:
   ```json
   {
     "title": "Descriptive title",
     "summary": "2-3 sentences",
     "category": "trading | platform | business | research | finance | youtube",
     "project_slug": "lowercase-with-hyphens",
     "project_name": "Human Readable Name",
     "is_new_project": false,
     "tags": ["emoji-category", "tag1", "tag2"],
     "key_insights": ["insight1", "insight2"],
     "related_projects": ["existing-slug"],
     "relevance_to_trading": "How this connects to bang's work"
   }
   ```
3. **Route** — create the wiki page in the correct location:
   - Project-related → `projects/<slug>/<slug>--<title>.md`
   - Research → `research/topics/<title>.md`
   - YouTube → `youtube/transcripts/<title>.md`
4. **Archive** — copy raw source to `raw/ingested/<filename>`
5. **Update indexes** — append to `log.md`, update `index.md` if new project
6. **Cross-link** — add `[[wikilinks]]` to related existing pages

Always check the project registry in `references/vault-schema.md` before creating new projects.
If the material fits an existing project, file it there.

### 2. INGEST — Directories (Two-Tier)

When a directory arrives, **do not** create a page per file. The graph would drown in noise.

**Tier 1 — Automatic (always runs):**

1. **Scan**: count files, map subdirectories, identify file types, build a 3-level directory tree
2. **Sample**: read 15-20 representative files (spread across subdirs, first 2000 chars each)
3. **Generate ONE overview page** with: one-liner summary, categories with standout items,
   highlights (5-8 most useful things), relevance to trading/AI, search keywords (15-20 terms),
   and recommended deep dives
4. **Write** to `projects/<slug>/<slug>.md`
5. **Archive** the full directory to `raw/ingested/<dirname>/`
6. **Log** the operation

Result: a 3,000-file repo becomes 1 searchable page. The full source is always preserved.

**Tier 2 — On-demand (user requests):**

When the user asks to "deep dive" into a specific item from an archived directory:

1. Locate in `raw/ingested/<archive-name>/`
2. Read full content
3. Generate a detailed wiki page
4. Save as `projects/<project>/<project>--<item-slug>.md`
5. Log the operation

The bundled `scripts/deep-dive.py` handles this, but you can also do it inline:
```bash
python scripts/deep-dive.py <archive> --list          # browse contents
python scripts/deep-dive.py <archive> --search "term"  # find items
python scripts/deep-dive.py <archive> "path/to/item"   # materialize one item
```

### 3. SESSION — Processing Work Transcripts

When processing a session transcript (from Cowork, Claude Code, or any work session):

1. **Read** the full transcript
2. **Identify**: which project(s) were touched, what was accomplished, key decisions made
3. **Create** session summary: `projects/<project>/<project>--<session-slug>.md`
4. **Update** the project overview page with a new session link and any status changes
5. **Extract** actionable insights and update related pages

Use the session summary template (What We Did → Key Outcomes → Technical Details → Insights →
Next Steps). This structure makes sessions scannable months later.

### 4. RESEARCH — Curriculum Generation

When the user provides a topic or URL to learn about:

1. **Research** the topic (web search if available, or work from provided material)
2. **Create** curriculum page in `research/curricula/<topic-slug>.md`
3. **Structure** as: Why This Matters (for bang's work specifically), Prerequisites, Learning
   Path (3-7 modules with time estimates, resources, exercises tied to bang's projects),
   Connections to Current Work, Progress Tracker
4. **Create** topic pages in `research/topics/` for key concepts
5. **Cross-reference** with existing project pages
6. **Update** `research/research-hub.md` and `log.md`

Curricula should be opinionated — not "intro to X" but "how bang applies X to trading edge."

### 5. YOUTUBE — Video Processing

When the user provides a YouTube URL:

1. **Extract transcript** — use the bundled `scripts/yt_extract.py`:
   ```bash
   python scripts/yt_extract.py "VIDEO_URL" --output-dir /tmp/yt-ingest
   ```
   This produces `metadata.json` and `transcript.txt` with `[MM:SS] text` format.
   If yt-dlp isn't installed: `pip install yt-dlp --break-system-packages`

2. **Read the FULL transcript** — every line, no skimming. For long transcripts, read in chunks.
   Track: core thesis, specific techniques/tools, applicability to NQ trading or agent dev,
   contrarian takes, concrete numbers/benchmarks.

3. **Write the wiki page** at `youtube/transcripts/<descriptive-slug>.md`:
   - **Key Takeaways** (5-8 bullets) — insights, not summaries. Include specific numbers and
     results. Bad: "discussed context windows." Good: "Agent.md burns ~944 tokens/turn; skills
     use progressive disclosure at ~50 tokens. That's 18x savings for a 1000-line config."
   - **Relevance to Our Work** — the most important section. Connect to bang's actual projects
     with `[[wikilinks]]`. Be opinionated about what to do differently.
   - **Action Items** — concrete next steps in `- [ ]` checkbox format
   - **Detailed Notes** — organized by topic (not chronologically), with timestamps `(12:34)`
   - **Full Transcript** — collapsible `<details>` section pointing to archived raw transcript

4. **Rate relevance**: high (directly applicable, adopt/evaluate), medium (relevant domain,
   no immediate action), low (tangential, worth having for search)

5. **Archive** raw transcript to `raw/ingested/yt-VIDEO_ID-transcript.txt`

6. **Update** `youtube/youtube-library.md` and `log.md`

### 6. QUERY — Answering Questions

When the user asks about their work or accumulated knowledge:

1. Read `index.md` to find relevant pages
2. Read those pages for context
3. Synthesize answer with `[[wikilinks]]` to sources
4. If the answer is substantial and reusable, offer to create a wiki page

### 7. REPORTS — Routing Synthesized Analysis

When polished output needs a home — equity dossiers, sector baskets, macro calls, tool evals —
it goes to `Reports/`, NOT into `cortana-vault/projects/`. The Reports/ system is the synthesis
layer; the vault is the input/research layer.

**Routing rule:** is this *data* (research, source material, methodology, playbook) or
*synthesis* (an opinionated analysis of a name/theme/regime, dated, signed)?

| Content type | Routes to |
|--------------|-----------|
| Source material, transcripts, raw research | `cortana-vault/raw/ingested/` |
| Curriculum / topic page on a concept | `cortana-vault/research/topics/` |
| Trading methodology / playbook (BT Equities Playbook, NY Session Frameworks, etc.) | `cortana-vault/research/topics/` — these are *data INPUT* (bang's own playbooks), not synthesized output |
| Project session summary | `cortana-vault/projects/<slug>/<slug>--<session>.md` |
| **Single-name equity thesis** | `Reports/equities/YYYY-MM-DD-<ticker>.md` (+ PDF) |
| **AI strategy / hyperscaler thesis** | `Reports/ai-strategy/YYYY-MM-DD-<slug>.md` |
| **Macro / regime call** | `Reports/macro-regime/YYYY-MM-DD-<slug>.md` |
| **Sector basket / multi-name theme** | `Reports/sector-theme/YYYY-MM-DD-<slug>.md` |
| **Tool / framework eval** | `Reports/tools-evals/YYYY-MM-DD-<slug>.md` |
| **Externally ingested research** (someone else's PDF) | `Reports/<category>/historical/YYYY-MM-DD-<slug>.md` with `historical: true` flag, original PDF stays at host path, link via `file://` URI |

**The `historical/` subfolder convention:** reports we author live in the parent category folder
(e.g., `Reports/equities/`). Reports we ingest from external sources live in
`Reports/<category>/historical/` with frontmatter `historical: true` and a `file://` link back
to the original PDF. Both surface in the same Obsidian search and graph.

**Report frontmatter spec:**

```yaml
---
title: "$TICKER · Company Name — BT Stock Report (Mon YYYY)"
type: report
report_type: equities | ai-strategy | macro-regime | sector-theme | tools-evals
historical: true     # ONLY if ingested from external source
ticker: TICKER       # equities only
date: YYYY-MM-DD
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🎯, equities, theme1, theme2]   # emoji first, then specific tags
status: active | archived
bucket: "Short bucket label (e.g., AI infra storage / hyperscaler doorway)"
pdf: "YYYY-MM-DD-ticker-bt-stock-report.pdf"   # relative if PDF is alongside
                                                # OR: file:///Volumes/... for ingested
related: [[adjacent reports]], [[vault topics]]
---
```

**The `file://` PDF link convention:** when an original PDF lives outside the Cortana root
(e.g., archived inbound research at `/Volumes/Data/BT_Reports/...`), don't copy it into the
vault. Reference it via absolute `file://` URI in frontmatter (`pdf: "file:///Volumes/..."`)
and inline link (`[Open original (file://)](file:///Volumes/...)`). Obsidian will open `file://`
URIs in the system default app. This keeps Reports/ free of large binary files while preserving
discoverability.

**Index updates required for every new report:**

1. `Reports/<category>/<category>.md` — add row to "Reports" table
2. `Reports/Reports.md` — add row to "Recent Reports" table (top of list)
3. `cortana-vault/log.md` — append a log entry

**Cross-linking pattern between vault and Reports:**

- From inside `cortana-vault/index.md`: `[[../Reports/equities/...]]`
- From `cortana-vault/research/topics/bt-equities-playbook.md`: `[[../../Reports/...]]`
- From a Report companion: `[[Reports/equities/...]]` or `[[cortana-vault/projects/...]]`
- From within a category index: `[[Reports/equities/historical/...]]` (full path always safest)

**Coordinating with other skills:**

- `bt-equity` produces the BT Stock Report PDF + markdown companion. After it generates, the
  obsidian skill (this one) is responsible for the vault-side updates (log entry, cross-links
  to adjacent reports, index registration).
- The bt-equity skill handles report content + PDF rendering. The obsidian skill handles
  routing + indexing + graph health.

### 8. LINT — Vault Maintenance

When asked (or periodically), check vault health:

- **Orphan pages** — no inbound links
- **Broken links** — `[[wikilinks]]` pointing to nonexistent pages
- **Stale content** — old dates, outdated status fields
- **Missing pages** — frequently linked but don't exist (create stubs)
- **Index drift** — `index.md` or `projects-directory.md` missing new projects
- **Contradictions** — conflicting information across pages
- **Tag hygiene** — pages missing emoji category tags or using wrong categories

Fix automatically where safe (stubs, indexes, tag fixes). Flag contradictions for the user.

---

## Naming Conventions

These exist because Obsidian's graph view uses filenames as node labels. Generic names like
`overview.md` make the graph useless.

| What | Pattern | Example |
|------|---------|---------|
| Project folder | `lowercase-hyphens/` | `wick-app/` |
| Project overview | Same name as folder | `wick-app/wick-app.md` |
| Session file | Project-prefixed `--` | `wick-app--fix-chart-explorer.md` |
| Section index | Descriptive name | `projects-directory.md` |
| Slug rules | lowercase, hyphens, ≤80 chars | `nq-monthly-performance` |

## Frontmatter

Every wiki page MUST have YAML frontmatter:

```yaml
---
title: "Page Title"
type: project | session | curriculum | topic | youtube | source | overview
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🎯, relevant, tags]   # emoji category tag FIRST, then text tags
status: active | completed | archived | draft
sources: []
related: []
---
```

### Emoji Category Tags

Every page gets exactly ONE emoji as the first tag. These provide visual scanning in Obsidian's
tag pane without replacing granular text tags.

| Emoji | Category | Covers |
|-------|----------|--------|
| 🎯 | Trading | NQ futures, indicators, backtesting, edge, PSO, Gann, Databento |
| 🤖 | AI/Agents | Claude skills, agent architecture, AOS, memory system, mission control |
| 📺 | YouTube | All video transcripts |
| 💼 | Business | Consulting, clients, proposals, finance/admin |
| 🔧 | Infrastructure | Dev environment, deployment, vault tooling |
| 📚 | Research | Curricula, deep dives, data science |

Pick the primary category based on the page's parent project. When ambiguous, use the domain
that matters most for discoverability.

## Linking

- Use Obsidian wikilinks: `[[path/to/page|Display Text]]`
- Link aggressively — every entity, concept, project, or tool mentioned should link to its page
- Unresolved links are fine — Obsidian highlights them, which surfaces knowledge gaps

## Callouts

Use Obsidian callouts for scannable pages:

- `> [!tip]` — Actionable insights, things to try
- `> [!warning]` — Risks, concerns, failure modes
- `> [!question]` — Open questions, unresolved issues
- `> [!info]` — Context, background, supplementary detail

---

## Automation Scripts

The `scripts/` directory contains Python utilities for automated/background operations. These
are optional — everything they do can be done inline by the agent.

| Script | Purpose | Key Usage |
|--------|---------|-----------|
| `vault-watcher.py` | Watches `inbox/` for new files, auto-ingests | `python scripts/vault-watcher.py` (watch) or `--process-once` |
| `deep-dive.py` | Tier 2 materialization from archived dirs | `--list`, `--search "term"`, or pass a path |
| `yt_extract.py` | YouTube transcript + metadata extraction | `python scripts/yt_extract.py "URL" --output-dir /tmp/yt-ingest` |

All scripts talk to OpenAI-compatible API endpoints (LM Studio, Ollama, OpenAI, etc.).
Default: `http://localhost:1234/v1`. Override with `--api-base`.

**When to use scripts vs. inline:** If the user is in a conversation and asks you to ingest
something, do it inline following the patterns above. Scripts exist for autonomous/background
processing without an active conversation.

---

## Log Format

Every operation gets logged in `log.md` (append-only, never modify existing entries):

```markdown
## [YYYY-MM-DD] operation | Title

- **type**: ingest | ingest (directory) | deep-dive | session | research | youtube | lint | query
- **source**: filename, directory name, or URL
- **details**: What was done
- **pages touched**: [[page1]], [[page2]]
```

---

## Quality Standards

The bar is: useful to bang 6 months from now when he's forgotten the details.

- **Opinionated, not neutral** — relate everything to trading edge and AI tooling. Wikipedia
  summaries fail the test.
- **"So what?" for every fact** — why does this matter? What should we do about it?
- **Concrete specifics** — exact numbers, tool names, file paths. Not "various techniques."
- **Flag open questions** — use `> [!question]` callouts for unresolved issues
- **One concept per page** — keep pages focused, cross-link for related ideas
- **Link density** — a page without wikilinks is probably missing connections

---

## Project Domains

Check these before creating new projects. If incoming material fits an existing project, file
it there. The full registry with slugs is in `references/vault-schema.md`.

| Domain | Key Projects |
|--------|-------------|
| Trading & Markets | Wick App, NQ Trading, Gann Indicator, BT Aggression, PSO Research, Databento |
| Platform & Infrastructure | AOS Platform, Mission Control, Memory System, Claude Skills |
| Business & Consulting | SouthbayAI, Summer Fridays, Merida Perfume, Web Design Clients |
| Finance & Admin | Finance & Admin (tax, banking, email, budgets) |
