---
name: obsidian-review
description: >
  Run a comprehensive health review of the Cortana vault — audit frontmatter, tag hygiene, link
  density, orphan pages, broken links, content quality, cross-linking gaps, and staleness. Produces
  a scored report with specific fix recommendations. Trigger on: vault review, vault audit, vault
  health, lint, maintenance, check vault, review connections, find orphans, or any mention of
  vault quality, graph health, or periodic maintenance. Run monthly or on-demand.
---

# Cortana Vault Review

You are running a periodic health review of an Obsidian knowledge vault. Your job is to
systematically audit every dimension of vault quality, produce a scored report, and recommend
specific fixes. The review should be completable by any agent with filesystem access.

**Before you begin, read** the vault's `SCHEMA.md` and the obsidian skill's
`references/vault-schema.md` to understand the vault's naming conventions, frontmatter specs,
emoji tag system, and project registry.

---

## Review Protocol

Execute these 7 passes in order. Each pass produces structured data that feeds into the final
report.

### Pass 1: Census

Count everything. Build the numbers table.

```bash
# Total wiki pages (exclude raw/, skills/, templates/, .obsidian/, .venv/, inbox/)
find . -name "*.md" -not -path "*/raw/*" -not -path "*/skills/*" \
  -not -path "*/.obsidian/*" -not -path "*/.venv/*" -not -path "*/templates/*" \
  -not -path "*/inbox/*" -not -path "*/scripts/*" \
  -not -name "README.md" | wc -l

# Pages by section
find ./projects -name "*.md" | wc -l      # project pages
find ./research -name "*.md" | wc -l      # research pages
find ./youtube -name "*.md" | wc -l       # youtube pages
```

Record:
- Total pages, project folders, session pages, YouTube transcripts, research pages, raw archives
- Emoji tag distribution (count per emoji)
- Average page size (line count)
- Vault age (days since first log entry)

### Pass 2: Frontmatter Audit

Check every page for YAML frontmatter compliance.

```bash
for f in $(find . -name "*.md" -not -path "*/raw/*" ...); do
  has_frontmatter=$(head -1 "$f" | grep -c "^---$")
  has_emoji=$(head -10 "$f" | grep -oP '🎯|🤖|📺|💼|🔧|📚' | head -1)
  has_related=$(grep -c "^related:" "$f")
  echo "$f | fm:$has_frontmatter | emoji:${has_emoji:-NONE} | related:$has_related"
done
```

Flag:
- Pages missing frontmatter entirely
- Pages missing emoji category tag
- Pages with wrong emoji for their parent project domain
- Pages with `related: []` (empty related array)
- Pages missing required fields (title, type, created, tags, status)

### Pass 3: Link Density Analysis

Map the wikilink graph.

```bash
# Outbound link count per page
for f in $(find ...); do
  links=$(grep -oP '\[\[' "$f" | wc -l)
  echo "$links links: $f"
done | sort -n

# Most-linked targets (inbound)
grep -rohP '\[\[([^\]|]+)' *.md | sed 's/\[\[//' | sort | uniq -c | sort -rn

# Broken links (targets that don't exist as files)
# Extract all link targets, check if corresponding .md file exists
```

Flag:
- **Islands**: Pages with 0-1 outbound links (these break the graph)
- **Broken links**: Wikilink targets that point to nonexistent pages
- **Dead ends**: Pages with many inbound links but 0 outbound (link sinks)
- **Hubs**: Pages with >10 links (verify they're still accurate)

### Pass 4: Content Quality Scan

Sample 20-30 pages across all sections. For each, assess:

1. **Usefulness test**: Would bang find this useful 6 months from now via Obsidian search?
2. **Specificity**: Does it contain concrete numbers, tool names, file paths — or vague hand-waving?
3. **Opinionation**: Does it relate content to trading edge / AI tooling — or is it neutral Wikipedia-style?
4. **"So what?"**: Does every piece of information have an implication or action?
5. **Grounding**: For architecture/design pages — is it clear what's built vs. what's designed?

Classify each sampled page into quality tiers:
- **Tier 1 — Excellent**: Keep and maintain
- **Tier 2 — Needs grounding**: Aspirational content not distinguished from reality
- **Tier 3 — Thin content**: Session dumps or summaries with minimal standalone value

### Pass 5: Cross-Link Opportunity Discovery

This is the most valuable pass. Look for connections between pages that should exist but don't.

Strategy:
1. Read project overview pages and identify which other projects they reference in prose but
   don't wikilink to
2. Check if CS229 lectures mention concepts used in trading/platform projects
3. Check if YouTube transcripts reference tools or techniques that map to existing projects
4. Check if business projects (SouthbayAI, web-design-clients) reference platform tools
5. Look for concept repetition across pages (same term in multiple pages = needs a hub page)

Produce a table:
```
| From | To | Why (specific reason) |
```

### Pass 6: Removal & Sanitization Candidates

Identify pages that should be removed, merged, or sanitized:

- **Superseded**: Pages that have been replaced by newer versions (e.g., v1 + v2 of same content)
- **Merge candidates**: Stub pages that could be sections in a parent page
- **Stale**: Pages with outdated status fields or "blocked" status older than 30 days
- **Sensitive data**: Pages that may contain PII, financial data, API keys, or other data that
  would be risky if the vault were shared. Flag but don't modify — human review required
- **Empty shells**: Pages with only frontmatter and headings, no actual content

### Pass 7: Research & Expansion Proposals

Based on what's in the vault, propose:

1. **Missing curricula**: Topics referenced across multiple pages but no learning path exists
2. **Missing topic pages**: Concepts that appear in >3 pages but have no dedicated page in
   `research/topics/`
3. **Pages needing more content**: Existing pages that are too thin to be useful
4. **New project proposals**: Work that's happening but not tracked in the vault

---

## Report Template

Write the report as a vault page at:
`projects/metacortex/metacortex--vault-review-YYYY-MM-DD.md`

Use this structure:

```yaml
---
title: "Cortana Vault Review — Month YYYY"
type: session
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🔧, vault, review, maintenance, meta]
status: completed
project: "[[projects/metacortex/metacortex|Metacortex]]"
sources: []
related: ["[[SCHEMA]]", "[[index]]"]
---
```

Sections:
1. **Vault Census** — numbers table
2. **Structural Health** — what's working + what's broken (with `> [!warning]` callouts)
3. **Content Quality Assessment** — tier breakdown with specific pages listed
4. **Proposed Connections** — the cross-link opportunity table (highest value)
5. **Removal & Sanitization Candidates** — with risk levels
6. **Research & Content Proposals** — ranked by impact
7. **Vault Architecture Improvements** — structural recommendations
8. **Summary Scoreboard** — letter grades per dimension

### Scoreboard Dimensions

| Dimension | What A Looks Like | What F Looks Like |
|-----------|-------------------|-------------------|
| Frontmatter compliance | 100% valid YAML with all required fields | Missing frontmatter on >20% of pages |
| Naming conventions | All files follow slug rules, project folders match overviews | Generic filenames, inconsistent separators |
| Tag hygiene | Every page has correct emoji + relevant text tags | Missing emojis, wrong categories, no text tags |
| Link density | Average >3 outbound links per page, <10% islands | >40% of pages are islands (0-1 links) |
| Content quality (overviews) | Opinionated, specific, "so what?" for every fact | Generic summaries, no connection to bang's work |
| Content quality (sessions) | Concrete outcomes, cross-linked, searchable | Thin dumps, 1 link, no standalone value |
| Cross-linking | Major project clusters connected, concept hubs exist | Project silos, no bridges between domains |
| Research depth | Active curricula, topic pages, learning paths in progress | Empty research section |
| Freshness | All active pages updated within 30 days | Stale statuses, outdated information |

---

## Post-Review Actions

After producing the report, propose a prioritized action list:

1. **Quick wins** (< 30 min): Fix broken links, fill empty `related:` fields, delete superseded pages
2. **Link enrichment** (1-2 hours): Add cross-links to island pages, especially CS229 lectures and session pages
3. **Content grounding** (2-4 hours): Add "what's built vs. designed" sections to aspirational pages
4. **Research bootstrapping** (4-8 hours): Create the highest-priority curriculum or topic pages
5. **Structural improvements** (next review): Implement any architecture changes proposed

The agent running this review should execute quick wins immediately (with user permission for
deletions) and present the rest as a prioritized backlog.

---

## Scheduling

This review should run:
- **Monthly** — full 7-pass review, scored report
- **Weekly** — passes 2-3 only (frontmatter audit + link density), no full report, just fix issues
- **On-demand** — when the user asks, or after a large batch ingest (>10 pages)

Log every review run in `log.md` with type `lint`.

---

## Process Learnings (from first full run, 2026-04-26)

These patterns emerged from running the first complete review + remediation cycle:

1. **Parallel agent execution is the right model for link enrichment.** CS229 lectures (20 pages)
   and session pages (28 pages) were enriched by two parallel agents in ~3 minutes. Sequential
   processing takes 10x longer. When enriching >10 pages, split the work across 2-3 agents
   operating on non-overlapping page sets.

2. **"Built vs. Designed" grounding is high-ROI and should be a standard pass.** Any page that
   describes architecture or design should have an explicit table showing what's running software
   vs. what's a specification. This prevents the vault from becoming a fiction library. Add this
   as a sub-check in Pass 4 (Content Quality).

3. **Research stubs compound as wikilink targets.** Even empty stubs with good questions and
   reading lists create targets that other pages can reference. The stubs attract content over
   time as agents encounter related material during ingestion.

4. **Templates should be excluded from island counts.** Template files (`./templates/*.md`) have
   0-1 links by design. Including them inflates the island percentage. The census commands above
   already exclude `*/templates/*` — ensure the link density pass does too.

5. **Cross-cluster bridges matter more than within-cluster links.** The Business↔Platform,
   Trading↔Research, and Platform↔Business bridges were the most impactful additions. Prioritize
   inter-cluster connections over adding more links between pages that already share a project folder.
