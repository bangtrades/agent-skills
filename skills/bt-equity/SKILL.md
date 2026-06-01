---
name: bt-equity
description: Produce a BT Stock Report — bang's institutional-tier (Druckenmiller-style) equity research dossier on a single ticker — as a branded PDF with a markdown wiki companion routed into the Cortana Reports system. Trigger this skill aggressively whenever the user asks for an equity report, stock report, "BT report" / "BT Stock Report", deep dive, equity research, position thesis, or any single-name analysis on a ticker (e.g., "$VIAV", "$P", "Avis Budget"). Trigger even when the user just names a ticker and says "research it", "build me a thesis", "write up", "deep dive", "do your thing on this name", or "analyze for a position". DO trigger for variant-perception / scenario-PT / probability-weighted EV / capital-structure / position-sizing requests on individual equities. DO NOT trigger for macro-only requests, sector/theme baskets, intraday trade ideas, or pure technical-chart questions — those have other homes (macro-regime, sector-theme, NQ trading playbooks).
---

# BT Equity Report Generator

You are producing a BT Stock Report — an institutional-tier equity research dossier in
bang's house style. The output is a branded PDF (5–10 pages) plus a markdown wiki
companion, routed into the Cortana Reports system at `~/Cortana/Reports/equities/`.

## Why this skill exists

Bang trades equities, futures, and crypto. He needs single-name research that meets the
bar he'd send to Stanley Druckenmiller — variant perception, scenario PTs with
probability-weighted EV, capital structure, what-would-change-my-mind, position sizing —
not a generic analyst summary. The output must be *opinionated*, *dated*, *sourced*, and
*shareable with humans*.

The skill bundles three artifacts:

1. **`assets/build_report.js`** — the canonical docx-js template with the BT brand
   primitives (amber dots, Helvetica Neue, two-column hero, card pattern, scenario PT
   table, capital-structure box, etc.). You modify it in place per ticker.
2. **`references/`** — four reference docs you read on demand:
   - `brand-guide.md` — palette, typography, layout primitives
   - `report-structure.md` — the 5-page Druckenmiller-tier section structure
   - `research-checklist.md` — what to gather before drafting
   - `companion-md-template.md` — the markdown wiki companion frontmatter + body
3. **This SKILL.md** — the orchestration logic.

## Workflow

### 1. Clarify

Before researching, take 30 seconds to confirm:

- **Ticker + exchange** — is the user using a current symbol, a former symbol, or naming
  the company? Pre-IPO or recently rebranded names are an easy way to fabricate a wrong
  report. If the symbol is unfamiliar, web-search to confirm BEFORE researching.
- **Horizon** — multi-quarter swing (default), tactical (days/weeks), or methodology study?
- **Conviction** — first-pass research vs. final pre-commit dossier? The depth scales.
- **Output destination** — default is `~/Cortana/Reports/equities/`. Confirm if user
  wants a different location for one-offs.

If the user just says "$X" with no other context, default to multi-quarter swing,
full Druckenmiller-tier depth, Cortana destination.

### 2. Research

Read `references/research-checklist.md` for the full data-gathering checklist. The short
version: pull most-recent earnings (release + transcript + slides), management
commentary, capital structure, segment build, competitive landscape, AI/macro tailwind,
short interest + insider activity + analyst PT migration, options/IV if available.

**Use the available tools in priority order:**

1. **WebSearch** for current price, market cap, latest earnings results, analyst PT moves
2. **WebFetch** for source-of-truth material — earnings releases, IR pages, transcripts
3. **Crawl4AI MCP** if connected (see `tools-evals` runbook in vault) — for higher-volume
   scraping of finance sites that resist WebFetch

**Cross-check primary numbers against at least two sources.** Press releases > aggregator
re-renders. If sources disagree on a number, pick the more authoritative one and note
the discrepancy in your sources block.

### 3. Map the thesis

Before writing the PDF, sketch on paper (or in the conversation):

- **Bucket** — one phrase that captures what kind of trade this is. "AI infra storage /
  hyperscaler doorway" beats "tech stock". The bucket goes into the Snapshot card.
- **Core view** — 4–6 sentences that synthesize the convergence. What are the 3 vectors?
  What is the gating event?
- **Variant perception** — pick 5–6 places where consensus and BT diverge. Each delta
  must be testable inside the next 1–2 earnings prints.
- **Scenarios** — Bull/Base/Bear PTs with probabilities. Anchor each on a multiple ×
  earnings number. Compute probability-weighted EV. The Bull tail should be meaningfully
  larger than the Bear tail — if it's not, the trade is not asymmetric.
- **What would change my mind** — pre-commit 6–8 specific triggers. NSE growth below X%,
  margin retracement below Y%, hyperscaler-2 not named by Z date.
- **Trade framework** — sizing logic, hedge candidates, exits.

Don't draft the PDF until these are clear. If you can't articulate the variant
perception, you don't have a thesis yet — keep researching.

### 4. Build the PDF

The build process is `node` → docx → soffice → PDF. The template lives at
`assets/build_report.js`. Modify it in place per ticker.

**Setup (first time on a new project):**

```bash
mkdir ~/<ticker>-report && cd ~/<ticker>-report
cp <skill>/assets/build_report.js .
cp <skill>/assets/package.json .
npm install --silent
```

**Edit pattern:** open `build_report.js` and replace the ticker-specific content. The
brand primitives (palette, AmberDots, makeCard, buildTable, hero layout) stay untouched.
You change:

- Snapshot card values
- Quarter card values
- Core view paragraph
- Why It Matters Now bullets (6 of them)
- BT Read paragraph
- Working stance table rows
- Print Setup Map table (page 2)
- Variant Perception table (page 3)
- Scenario PT table (page 3)
- Capital Structure table (page 3)
- Earnings Model table (page 3)
- Business Overview, Tailwind, Catalyst Path, Risks, etc. (pages 4–5)

**Read `references/report-structure.md`** for the exact 5-page section sequence and
the canonical sections inside each page.

**Build + render:**

```bash
node build_report.js && \
python ~/.claude/skills/docx/scripts/office/soffice.py \
  --headless --convert-to pdf <ticker>-bt-stock-report.docx --outdir .
```

**Verify layout:** open the PDF, scan for orphans (single rows on their own page,
half-empty pages, truncated tables). The build script uses `cantSplit: true` on table
rows and `pageBreakBefore: true` on the AmberDots paragraph at each page header — those
are the levers that prevent layout breaks. **Do not** insert standalone PageBreak
paragraphs; they create empty pages when content already overflows naturally.

### 5. Write the markdown wiki companion

Read `references/companion-md-template.md` for the canonical frontmatter + body
structure. The companion lives next to the PDF in `~/Cortana/Reports/equities/` and
carries:

- YAML frontmatter (title, type, ticker, date, tags, bucket, pdf, related)
- Core thesis paragraph
- Snapshot table
- Quarter table
- Scenario PT table
- Variant perception (most important rows)
- Catalysts (checkbox format)
- What would change my mind (bulleted)
- Trade framework
- Related vault content (`[[wikilinks]]`)
- Sources

The companion is what makes the report **searchable in Obsidian** — PDFs index poorly,
markdown indexes richly. Don't skimp on this step.

### 6. Deliver + archive

**Output destinations:**

- PDF: `~/Cortana/Reports/equities/YYYY-MM-DD-<ticker>-bt-stock-report.pdf`
- MD companion: `~/Cortana/Reports/equities/YYYY-MM-DD-<ticker>.md`

**Update indexes:**

- Add a new row to `~/Cortana/Reports/equities/equities.md` in the "Reports" table
- Add a new row to `~/Cortana/Reports/Reports.md` in the "Recent Reports" table
- Append a log entry to `~/Cortana/cortana-vault/log.md`

**Present the result:**

Use `computer://` links for inline preview in Cowork. End the response with a tight
summary of the thesis + asymmetry, not a recap of what you did.

> [!info] Output discipline
> **PDF only — no docx.** The Word→Pages conversion path on macOS breaks alignments;
> the soffice → PDF path is reliable. Don't deliver a docx alongside the PDF.

## Quality bar (Druckenmiller-tier, not generic analyst)

What separates a BT report from a generic analyst note:

- **Variant perception is explicit.** Every report has a "Consensus says / BT says / Why
  we differ" table. If you can't articulate where you diverge, the report is just summary.
- **Scenarios are probability-weighted.** Bull/Base/Bear PTs with probabilities; compute
  PWM EV; describe asymmetry. If bull tail ≤ bear tail, flag it explicitly.
- **Capital structure is broken out.** Net cash/debt, leverage trajectory, buybacks,
  convert exchanges. Not just "balance sheet looks fine."
- **Earnings model is a table, not prose.** FY current / guide / BT-est for next two
  fiscal years. Revenue + segment + op margin + EPS + FCF.
- **Catalyst path has probabilities + impact ratings.** Each catalyst gets a
  probability and high/med/low impact label.
- **What would change my mind is pre-committed.** 6–8 specific disconfirming triggers.
- **Position sizing has math.** Kelly sketch from the probability-weighted scenarios.
- **Sources are real.** Press release URLs, transcript URLs, analyst note dates. Aggregators
  are fine but flag them as such.

## Format notes

**Brand primitives (do not change):** see `references/brand-guide.md`.

**Section order (do not change):** see `references/report-structure.md`.

**Frontmatter (companion MD):** see `references/companion-md-template.md`.

The build template at `assets/build_report.js` already implements all three. You're
populating content into a working scaffold, not designing layout from scratch.

## When the report is for a private / pre-IPO company

Some research targets are private companies (e.g., Securitize on its way to a SPAC).
In that case:

- Set `ticker: "(private — pre-IPO)"` in the companion frontmatter
- Mark `bucket` with "pre-IPO" or "SPAC watch"
- Skip the price/market-cap snapshot (or note "private / not yet trading")
- Replace scenario PTs with "implied valuation at potential IPO" math
- File in `Reports/equities/` with the private flag visible

## When you need to skip parts of the workflow

Be explicit about what you're skipping and why:

- **Speed run** ("just give me the snapshot") — produce only Snapshot + Quarter + 3-bullet
  thesis + sources. No PDF; markdown-only.
- **Update an existing report** — read the previous version, append a "Update YYYY-MM-DD"
  section to the companion MD, regenerate PDF only if material changes.
- **Pre-flight check before writing** — if the user is unsure they want a full report,
  produce a 1-page "Research Brief" first to validate thesis direction.

## Coordinate with other skills

- `obsidian` — for vault routing, log updates, cross-link conventions. The Reports/
  hierarchy lives at the Cortana root (sibling of cortana-vault), so `[[../Reports/...]]`
  syntax is the cross-link pattern from inside the vault.
- `pdf` — if the user wants to manipulate the resulting PDF (merge, split, OCR, etc.).
- `docx` — fallback only if user explicitly requests Word output (rare; default is PDF).

## Anti-patterns

- **Don't paste the entire Q-earnings transcript into the report.** Synthesize 4–6
  bullets of what management said and why it matters. The transcript URL goes in sources.
- **Don't fabricate analyst PT moves.** If you can't find a recent firm-by-firm PT update,
  say "consensus PT $XX (n=N analysts)" without naming firms.
- **Don't anchor the bull case on a 50x revenue multiple.** If the multiple is heroic,
  call it that and explain what would have to be true.
- **Don't skip the disconfirming triggers.** "What would change my mind" is the difference
  between a thesis and a pitch.
- **Don't write generic risks ("market risk, regulatory risk").** Risks must be
  specific and tied to the thesis. If the bull case is "Meta deal opens hyperscaler
  doorway", the risk section must engage with hyperscaler vertical-integration risk
  specifically.

## After delivery

Offer the user:

- A standalone "what would invalidate this thesis" tracker (separate file in
  `cortana-vault/projects/<ticker>-watch/`)
- An update on the next earnings date with a pre-print setup map
- Cross-links to adjacent reports (sector basket / macro context)

The report is the start of a position-watching cadence, not the end.
