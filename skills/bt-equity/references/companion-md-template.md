# BT Equity Report — Markdown Companion Template

The PDF is the polished deliverable. The markdown wiki companion is what makes the
report **searchable in Obsidian** — PDFs index poorly, markdown indexes richly. Both
get saved to `~/Cortana/Reports/equities/` with matching dates.

## File naming

- PDF: `YYYY-MM-DD-<ticker>-bt-stock-report.pdf`
- MD:  `YYYY-MM-DD-<ticker>.md`

Use lowercase ticker. For private / pre-IPO names that don't have a ticker yet, use a
slug derived from the company name (e.g., `2026-03-09-securitize.md`).

## Frontmatter (canonical)

Every companion MD has this YAML frontmatter at the top:

```yaml
---
title: "$TICKER · Company Name — BT Stock Report (Mon YYYY)"
type: report
report_type: equities
ticker: TICKER
company: "Full Legal Name, Inc."
exchange: NYSE | NASDAQ | NYSE American
date: 2026-04-27
created: 2026-04-27
updated: 2026-04-27
tags: [🎯, equities, theme1, theme2, theme3]
status: active
spot: "$XX.XX"
market_cap: "~$X.XB"
bucket: "Short bucket label — e.g., AI infra storage / hyperscaler doorway"
horizon: "6–24 months" | "Days to weeks tactical"
pdf: "YYYY-MM-DD-ticker-bt-stock-report.pdf"
sources: []
related: [[adjacent reports]], [[vault topics]]
---
```

### Frontmatter field rules

- **`tags`** — first tag MUST be the emoji category (🎯 for trading-focused equity reports;
  🤖 if the report leans AI infrastructure thesis primarily). Then 3–5 specific text tags.
- **`status`** — `active` for current theses; `archived` for historical / superseded.
  Set `historical: true` instead of `status: archived` for ingested external research.
- **`pdf`** — file name only (relative); for ingested reports, use `file://` absolute path
  to the original location.
- **`bucket`** — one phrase that captures what kind of trade this is. Used in indexes.
- **`related`** — list of `[[wikilinks]]` to adjacent reports + relevant vault topics.
  At least 3 entries; this is what makes the graph useful.

## Body structure

The body mirrors the PDF section-by-section but compressed and converted to markdown.
Every section gets a heading; every numeric block gets a markdown table.

```markdown
# $TICKER · Company Name

> [!info] Report
> **PDF:** [[YYYY-MM-DD-ticker-bt-stock-report.pdf]]
> **Spot:** $XX.XX · **Market Cap:** ~$X.XB · **Bucket:** [bucket label]
> **Bucket label:** Druckenmiller-tier; thesis is [one-line synthesis].

## Core Thesis

[Single dense paragraph. 4–6 sentences. The thesis stated as one breath.]

## Snapshot

| | |
|---|---|
| Price | $XX.XX |
| Market Cap | ~$X.XB |
| 52W Range | $XX.XX – $XX.XX |
| P/E (TTM) | XXx |
| Cash + ST Inv. | $XXXM |
| Total Debt | ~$XXXM |
| Bucket | [bucket label] |

## Latest Quarter (QX FYYY)

| | |
|---|---|
| Revenue | $XXM (±X% YoY) |
| Non-GAAP EPS | $X.XX (beat $X.XX) |
| ... | ... |

## Scenario Price Targets (12-month)

| Scenario | Price | Probability | Implied Return | Anchor |
|----------|-------|-------------|----------------|--------|
| **Bull** | $XX | 30% | +X% | [anchor description] |
| **Base** | $XX | 45% | +X% | [anchor description] |
| **Bear** | $XX | 25% | -X% | [anchor description] |
| **PWM** | **$XX** | 100% | **+X%** | Asymmetry meaningfully bull-skewed |

## Variant Perception (most important)

- **Consensus:** [what the market believes]
- **BT:** [what we think]
- [continue for 2–3 most important deltas]

## Key Catalysts

- [ ] **Q[N] FY[YY] earnings** ([date]) — gating event
- [ ] [next catalyst with probability if known]
- [ ] [continue]

## What Would Change My Mind

- [Specific disconfirming trigger 1]
- [Specific disconfirming trigger 2]
- [continue]

## Trade Framework

- **Core position** — [how to size, when to add]
- **Pre-print** — [pre-event posture]
- **Tactical** — [defined-risk option structure if useful]
- **Hedge** — [pair candidate]
- **Exits** — [trim/scale targets]

## Related Vault Content

- [[Reports/equities/<adjacent-report>|<Adjacent ticker description>]]
- [[Reports/macro-regime/<related macro>|<macro context>]]
- [[cortana-vault/research/topics/<topic>|<relevant topic>]]

## Sources

[Italic prose summary of every source. Press releases, transcripts, analyst notes,
trade publications. Each citation should be enough that the reader can find the source
again — name the publication and approximate date.]
```

## Inline conventions

- **Bold tickers when first introduced** — `**$VIAV**` first time, then `$VIAV` later
- **Wikilink to adjacent reports** in prose with display text — `[[Reports/equities/2026-04-27-p|$P · Everpure]]`
- **Use callouts** for things that should jump out:
  - `> [!info]` — context, background
  - `> [!tip]` — actionable insights
  - `> [!warning]` — risks, concerns
  - `> [!question]` — open questions
- **Use checkboxes** for catalysts so they can be ticked off as they hit
- **Use tables** for any structured data — never bullet-list a 5-row dataset

## Connecting to adjacent reports

The companion's `related:` frontmatter and inline `[[wikilinks]]` are how Obsidian's
graph view connects this report to the rest of the vault. Always link to:

- **At least one adjacent equity report** in the same theme/bucket
- **At least one sector-theme or macro-regime report** that contextualizes
- **At least one vault topic page** if relevant (e.g., `[[bt-equities-playbook]]` for the methodology)

If you can't find adjacent reports to link to, that's a signal the vault is missing
context — flag it and offer to write a topic page.

## When to update vs. create new

- **Same thesis, new quarter** — update the existing companion. Add a "Update YYYY-MM-DD"
  section at the end. Bump `updated:` in frontmatter.
- **Thesis materially changed** — create a new companion with the new date in the filename.
  Add a `superseded_by:` field to the old one.
- **Position closed / thesis invalidated** — set `status: archived` in the old one, write
  a closing note in a new companion summarizing what changed.

## Index updates required

Every new companion requires three index updates:

1. `~/Cortana/Reports/equities/equities.md` — add a row to the Reports table
2. `~/Cortana/Reports/Reports.md` — add a row to the Recent Reports table (top of list)
3. `~/Cortana/cortana-vault/log.md` — append a new log entry

These updates are part of the report; not optional housekeeping.

## Example references

Real exemplars to model on:

- `Reports/equities/2026-04-27-p.md` — full-length flagship (Everpure)
- `Reports/equities/2026-04-27-viav.md` — earnings-week setup (Viavi)
- `Reports/equities/2026-04-20-car.md` — squeeze / market-structure variant (Avis Budget)
- `Reports/equities/historical/2026-03-09-securitize.md` — pre-IPO / private variant
