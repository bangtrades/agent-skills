---
name: obsidian-review
description: >
  Run a comprehensive health review of the Cortana vault — audit frontmatter, tag hygiene, link
  density, orphan pages, broken links, content quality, cross-linking gaps, and staleness. Produces
  a reproducible status report with specific fix recommendations, and checks that log.md is
  strictly reverse-chronological with nothing stranded below "## Archive". Trigger on: vault review,
  vault audit, vault health, lint, maintenance, check vault, review connections, find orphans,
  log order, log ordering, stranded log entries, entries below Archive, or any mention of vault
  quality, graph health, or periodic maintenance. Runs daily at 04:05 as the scheduled
  obsidian-review task; also on-demand.
---

# Cortana Vault Review

You are running a periodic health review of an Obsidian knowledge vault. Your job is to
systematically audit every dimension of vault quality, produce a reproducible evidence packet and
derived report, and recommend specific fixes. Do not invent an aggregate health score.

**Before you begin, read** the vault's `SCHEMA.md` and the obsidian skill's
`references/vault-schema.md` to understand the vault's naming conventions, frontmatter specs,
emoji tag system, and project registry.

---

## Review Protocol

### Maintained Cortana review path (staged 2026-09-07)

For Cortana, the maintained producer is `cortana-vault/scripts/vault-review.py`, invoked through
`cortana-vault/scripts/vault-python`. Inspect both CLIs' current `--help` before constructing the
command. The review packet schema is `vault-review/v1`; its only top-level outcomes are `passed`,
`failed`, and `incomplete`, with exit codes 0, 1, and 2. Missing or partial required scopes are
non-green. The Markdown report must be derived from that packet and must not add an aggregate score.

Build one dated inventory snapshot and pass the same snapshot to every count consumer. Treat the
inventory producer's `cortana-vault-inventory/v2` schema as authoritative. Its canonical
`entity_cards`, `relation_entries`, and `directed_edges` mean compiler-eligible entities, eligible
ordered relations, and distinct eligible triples. Keep `candidate_entity_cards`,
`inactive_candidate_entity_cards`, and `candidate_relation_entries` separate, including
compiler-excluded material such as `web-design-excellence/context/_trash`. Determine
`distinct_rendered_edges` by comparing the actual canonical render bytes, including the Markdown
fallback, rather than by regex. Counts are live observations, never acceptance constants. Re-read
the producer and current packet schema before each run.

Supply the current canonical registry manifests and the authoritative lifecycle, staging, QA,
application, post-application, and hold packets. Every joined input and producer must be hash-bound,
and apply receipts must join the real postimage to the reviewed preimage. A stale or missing join is
`failed` or `incomplete`, never silently omitted.

The existing daily `obsidian-review` Cowork task remains the caller. Keep its 04:05 cadence and mount
the full `/Users/nolan/Cortana` root so `.obsidian/`, `cortana-vault/`, `Reports/`, `docs/`, and the
read-only registry are visible. Bootstrap only from an actual Python 3.14 executable when the pinned
runtime is absent, and verify Python 3.14 plus PyYAML 6.0.3. Native or Colima evidence does not certify
the Cowork caller. A completed scheduled run must bind its task/session identity, exact command,
mounted root, prompt/config revision, runtime pins, review source hash, packet hash, return code, and
start/end timestamps. The first post-migration run may prove the technical caller while remaining
`incomplete` for lack of a prior caller receipt; do not create a self-acceptance loop or claim final
scheduled acceptance from that run alone.
Treat the attestation as a claim until its referenced scheduled-session evidence files exist, their
hashes match, timestamps parse and order correctly, the mounted path resolves to the actual root,
and the recorded command and packet agree with the observed completed run. Schema validation alone
does not prove runtime execution. This acceptance gate remains unresolved until those checks and the
independent V08 QA pass.

The seven passes below are qualitative review guidance and historical context. Their ad-hoc shell
censuses and letter-grade scoreboard do not replace the maintained producer. Pass 8 (log ordering)
is mandatory on every scheduled run, not qualitative guidance.

Execute these passes in order. Each pass produces structured data that feeds into the final
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

### Pass 8: Log Ordering Check (mandatory, every scheduled run)

Governed by `SCHEMA.md` § Log Format → **Log ordering contract — 2026-09-16**: `log.md` is strictly
reverse-chronological and `## Archive` is terminal. Nothing is ever written below `## Archive`.
The contract exists because four writers in the 30 days to 2026-09-18 appended entries to the
bottom of the file (`vault-watcher.py:append_to_log()` as the copied template, `vault-staging/apply.sh`
on 2026-09-01, the 2026-09-16 scheduled memory-maintenance run, and three 2026-09-17 sessions).
Two of those were hand-repaired; per `memories/promoted/repair-the-generator-not-its-output` the
fix belongs in the check, so this pass is the check.

**Where the check runs.** The target home is `scripts/vault-lint.py` as a `check_log_order()`
section (`=== LOG ORDER ===`, JSON key `log_order`, counted as **errors** not warnings; monthly shards
`log/YYYY-MM.md` get the same check minus the `## Archive` clause). That CODE-lane patch is
operator-applied. Until `vault-lint.py --json` emits `log_order`, this pass performs the same
detection itself, read-only, and reports it in the review. Once the linter carries it, consume the
linter's `log_order` block and do not duplicate the scan. Never patch `vault-lint.py` from inside a
scheduled review run.

**Detector — form-agnostic.** A heading-only detector (`^## \[YYYY-MM-DD\]`) scored the 2026-09-17
instances `0 / 0` because they were appended as `- **YYYY-MM-DD …**` bullets. Inside the Archive
section, *any* line carrying a date-bearing entry shape is a finding:

```python
def check_log_order(content_root):
    """log.md must be reverse-chronological with a terminal ## Archive section."""
    import os, re
    res = {"file": "log.md", "entries": 0, "out_of_order": [], "after_archive": []}
    path = os.path.join(content_root, "log.md")
    if not os.path.isfile(path):
        return res
    lines = open(path, encoding="utf-8").read().split("\n")
    archive_at = next((i for i, l in enumerate(lines) if l.strip() == "## Archive"), None)
    hdr = re.compile(r"^## \[(\d{4}-\d{2}-\d{2})\]")
    dated = [(i, m.group(1)) for i, l in enumerate(lines) if (m := hdr.match(l))]
    res["entries"] = len(dated)
    # order check over the heading-form entries that precede ## Archive
    body = [(i, d) for i, d in dated if archive_at is None or i < archive_at]
    for (i1, d1), (i2, d2) in zip(body, body[1:]):
        if d2 > d1:                       # a later date appearing further down
            res["out_of_order"].append({"line": i2 + 1, "date": d2, "after": d1})
    # anything below ## Archive that looks like an entry, in ANY form
    entryish = re.compile(r"^\s*(?:##\s*\[|[-*]\s+\*\*)(\d{4}-\d{2}-\d{2})")
    if archive_at is not None:
        for i, l in enumerate(lines[archive_at + 1:], start=archive_at + 1):
            if (m := entryish.match(l)):
                res["after_archive"].append({"line": i + 1, "date": m.group(1),
                                             "form": "heading" if l.lstrip().startswith("##") else "bullet",
                                             "heading": l[:90]})
    return res
```

The shard links under Archive (`- [[log/2026-08|…]] — 113 entries`) do not match: they carry no
`YYYY-MM-DD`. The Archive section's whole contract is those monthly shard links and nothing else.

**Output fields.** Every `after_archive` finding reports `line`, `date`, `form: heading|bullet`,
and the first 90 characters of the line. `form` identifies the writer class: `heading` is a writer
that knows the entry format and got placement wrong; `bullet` is a writer appending a one-line
session note, which is the `open(log, "a")` shape the contract forbids. Every `out_of_order`
finding reports `line`, `date`, and the earlier `after` date it sits beneath.

**What the scheduled run does with a finding.** Detect and report; **prepare, do not relocate.**
Moving an entry is an edit to `log.md` that is not in the pre-approved mechanical set of
`SCHEMA.md` § Scheduled write-run protocol — 2026-09-14, and the 2026-09-16 patch does not
authorize a scheduled run to apply it. For each finding, the run:

1. Lists it in the review report under **Log ordering** and in the run's own log entry
   (`line`, `date`, `form`, text prefix).
2. States the correct destination: immediately under `# Activity Log` for the newest date, or the
   run-time-warranted position inside the existing block for that date, with text verbatim and a
   `- **type**` line noting the relocation.
3. Leaves `log.md` untouched below `## Archive`. The operator, or a dev-lane run with a receipt,
   relocates. An operator-run on-demand review may relocate when asked and must say so in its log entry.
4. Names the writer class from `form` so the producing writer can be fixed at the source.

A non-empty `after_archive` or `out_of_order` is a review **error**; the run's status table reports
it as `failed`, never as a warning. A misplaced entry is invisible to anyone reading the log top-down,
which is how the 2026-09-16 entry survived a full day.

**Acceptance fixtures** (for the linter patch, and for verifying this pass by hand):

1. Current `log.md` (post-repair) reports `0 / 0`.
2. A fixture that appends a `## [YYYY-MM-DD]` heading below `## Archive` exits non-zero and names the line.
3. A fixture with `2026-09-10` sitting below `2026-09-08` exits non-zero and names both dates.
4. Nothing under `vault-contract.json → expected_failure_fixtures` is touched by the check or by any
   `--fix` path (execution-plan item 1.7).
5. A fixture appending `- **2026-09-17 ~07:52 ET** — …` below `## Archive` exits non-zero and reports
   `form: bullet`.

**Writer-side companions** (not this pass's job; listed so the finding routes correctly):
`scripts/vault-watcher.py:append_to_log()` is retired and should lose its `"a"` mode or be deleted
(in-vault, CODE lane); `vault-staging/apply.sh` is outside the vault and under a standing do-not-run
instruction; agent-written entries are fixed by the SCHEMA declaration plus this check.

---

## Report Template

Write the report as a vault page at:
`projects/cortana-platform/cortana-platform--vault-review-YYYY-MM-DD.md`

> **Canonical destination = `projects/cortana-platform/`** (per `SCHEMA.md` § Dashboard
> Maintenance). This supersedes the older `projects/metacortex/` path. `update-dashboard-reports.py`
> scans `cortana-platform/` and auto-archives reviews >7 days into `cortana-platform/reviews-archive/`.
> `metacortex` remains the home for vault *meta-operations*, not review output.

Use this structure:

```yaml
---
title: "Cortana Vault Review — Month YYYY"
type: session
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🔧, vault, review, maintenance, meta]
status: completed
project: "[[projects/cortana-platform/cortana-platform|Cortana Platform]]"
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
8. **Log ordering** — Pass 8 findings: `after_archive` and `out_of_order` with `line`, `date`,
   `form`, proposed destination; `0 / 0` stated explicitly when clean
9. **Status table** — producer outcomes and findings, with no aggregate score

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

For the existing Cortana automation, run daily at 04:05 through the maintained command. On-demand
qualitative sampling may supplement that result but cannot replace or override it. Every scheduled
run includes Pass 8 (log ordering) and reports its result even when clean.

Log every review run in `log.md` with type `lint`. Insert the entry before the first existing
`## [` heading (or at its run-time position inside the current date block) — never append to the
bottom of the file. A review run that strands its own log entry below `## Archive` is the defect
Pass 8 exists to catch.

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

---

## Changelog

### 2026-09-20 — staged reconciliation for publication

Base: the staged 2026-09-07 copy. Three-way compare against the registry copy (2026-06-03) and the
plugin-cache copy loaded by the scheduled runs (2026-08-08) showed the plugin cache byte-identical to
the registry body (frontmatter flattened to one-line strings only) and the 2026-09-07 copy a strict
superset of both, so no regression was present and the staged text was kept.

- **PATCH-2026-08-08-routing** — closed 2026-08-10 as harness drift, not a text patch. The
  `projects/cortana-platform/` report destination and its `metacortex` supersession note were
  already present in the registry, the plugin cache and the staged copy. No SKILL.md text changed;
  recorded here for provenance.
- **PATCH-2026-09-16-log-ordering-check** (with its 2026-09-18 addendum) — added **Pass 8: Log
  Ordering Check** as a mandatory step on every scheduled run: form-agnostic detector for entries
  stranded below `## Archive` (both `## [YYYY-MM-DD]` headings and `- **YYYY-MM-DD …**` bullets),
  `form: heading|bullet` output field, out-of-order detection above Archive, the five acceptance
  fixtures, and the scheduled-run rule (detect and report, prepare the relocation, never relocate
  from a scheduled run). Added a **Log ordering** report section, the daily-run requirement in
  Scheduling, and the insert-never-append rule for the review's own log entry. The `vault-lint.py`
  `check_log_order()` home for the check remains a separate operator-applied CODE-lane patch.
- Description gained log-ordering trigger cues and the 04:05 daily cadence.
