# BT Equity Report — Structure Reference

A BT Stock Report is 5–10 pages of dense, opinionated single-name research in a fixed
section sequence. The 5-page core is non-negotiable; 6–10 pages is normal for complex
names (multi-segment, deeper capital structure, more catalysts). Don't go longer than
10 pages — beyond that, density turns into noise.

## The 5-page Druckenmiller-tier core

### PAGE 1 — One-pager hero

The page that gets sent solo when bang says "just give me the headline."

| Section | Purpose | Implementation |
|---------|---------|----------------|
| Amber-dot row | Brand mark | `AmberDots()` |
| Ticker title | Identity | `TickerTitle('VIAV')` |
| Subtitle | Page context | "Viavi Solutions · BT Stock Report — AI infrastructure validation, defense PNT, Spirent operating leverage" |
| Hero table (2-col) | Core View + Snapshot + Quarter cards | `heroTable` (left: thesis paragraph; right: stacked cards) |
| Why It Matters Now | 6 bullets that compress the thesis | `whyItMattersNow` (full-width, below the hero) |
| BT Read | 4–6 sentence synthesis paragraph | `btRead` |
| Working stance | Bucket / Character / Horizon / Style / Edge table | `workingStance` |
| Q[N] Print Setup Map | Bull-case vs bear-case print expectations | Optional but valuable when an earnings event is near |

The first sentence of Core View should answer "what is this trade?" in one breath. The
6 Why-It-Matters-Now bullets should each be a load-bearing fact a sophisticated reader
hasn't already seen.

### PAGE 2 — Variant Perception + Scenario PTs + Capital Structure + Earnings Model

This is the page where the report earns its institutional rating.

| Section | Purpose | Implementation |
|---------|---------|----------------|
| Variant Perception | 5–7 rows of "Consensus says / BT says / Why we differ" | 3-column `buildTable` with header |
| Scenario Price Targets · 12-month | 4-row table: Bull / Base / Bear / Probability-Weighted | 5-column table, color-coded rows |
| Capital Structure & Capital Return | Cash, debt, net cash, buybacks, convert exchanges, leverage | 3-column table |
| Earnings Model · BT vs Guide vs Street | FY current / guide / BT FY+1 / BT FY+2 across rev/seg/margin/EPS/FCF | 5-column table |

The Scenario PT table requires probability-weighted EV math. Compute it in the row.

### PAGE 3 — Business Quality + AI/Macro Tailwind + Competitive Moat

| Section | Purpose | Implementation |
|---------|---------|----------------|
| Business Overview | What does the company do, in plain language? | One paragraph |
| Mix Shift / Segment Build | If applicable — quantified mix shift table | `buildTable` |
| Big Tailwind | The thematic engine (AI infra, energy transition, reshoring, etc.) | 5–6 bullets with hard numbers |
| Hidden / Embedded Asset | Optional — overlooked franchise inside the company | Bullets |
| Spirent / Acquisition Scorecard | If recent M&A material to the thesis | 3-column table |
| Competitive Moat | 5–7 named competitors with strength/weakness/net | 5-column table |

This page tells the reader **why this name and not the obvious mega-cap proxy.**

### PAGE 4 — Catalyst Path + Quarterly Monitoring + Sentiment & Positioning

| Section | Purpose | Implementation |
|---------|---------|----------------|
| Catalyst Path | Calendar of events with probability + impact rating | 4-column `buildTable` |
| Quarterly Monitoring Dashboard | 8–10 KPIs to track each Q | Bullets |
| Sentiment & Positioning Dashboard | Stock vs ATH, sell-side rating, latest PT moves, insider activity, buyback pace, options/IV, retail sentiment, hyperscaler concentration | 3-column table |
| Analyst Price Target Migration | Old PT → New PT, per firm, with date and rating | 5-column table |

This is the page hedge fund analysts skip to first when sizing decisions.

### PAGE 5 — Risks + What Would Change My Mind + Trade Framework + Position Sizing + Bottom Line

| Section | Purpose | Implementation |
|---------|---------|----------------|
| Key Risks | 6–8 thesis-specific risks (NOT generic "market risk") | Bullets |
| What Would Change My Mind | 6–8 explicit disconfirming triggers — pre-committed | Bullets, Druckenmiller-style framing in the lead-in |
| Trade Framework | Core thesis sizing, pre-print sizing, tactical structures, hedges, stops, exits | Bullets |
| Position Sizing — Kelly Sketch | Show the math: P(bull) × bull + P(base) × base + P(bear) × bear = PWM EV | One paragraph with the equation |
| Bottom Line | The 4–6 sentence synthesis that gets quoted | One paragraph |
| Sources | Italic prose listing of every source consulted | Reformatted citations |
| Disclaimer | Prepared date, "research + synthesis only — not investment advice" | One micro-size paragraph |

The "What Would Change My Mind" section is the **single most important section** for
distinguishing a thesis from a pitch. Every trigger should be falsifiable inside the
next 1–2 earnings prints.

## Section ordering rules

- **Page 1 is the one-pager.** It must stand alone if the rest never gets read.
- **Variant Perception goes BEFORE Scenarios.** You earn the right to set PTs only after
  you've articulated where you diverge from consensus.
- **Capital Structure goes on Page 2**, not buried at the end. Leverage is a multiple
  on every other assumption.
- **What Would Change My Mind goes BEFORE Trade Framework.** Disconfirming triggers
  inform sizing.
- **Bottom Line is the LAST narrative section** before sources. Not a recap — the synthesis.

## When to compress vs expand

**Compress (5 pages exactly)** when the thesis is mature and the reader will use the
report for sizing decisions, not learning the company.

**Expand (6–10 pages)** when:

- Multi-segment company needs detailed segment build (add page after Business Quality)
- M&A is recent and material — add a dedicated integration scorecard page
- Defense / regulated industries — add a regulatory landscape page
- Pre-IPO / SPAC — add a deal structure + valuation methodology page

**Never expand by adding more bullets to existing pages.** Density per page should stay
constant. Add a NEW page if you need more space.

## Common rendering pitfalls

- **Orphaned table rows** — a row stuck on its own page after a page break. Fix: ensure
  every table row has `cantSplit: true`.
- **Half-empty page 2** — happens when page 1 fills exactly and the explicit page break
  fires after natural overflow. Fix: use `pageBreakBefore: true` on the AmberDots paragraph
  of page 2, never standalone PageBreak.
- **Disclaimer alone on the last page** — happens when sources block fills the prior
  page exactly. Fix: use `keepLines: true` on the sources prose paragraph + the
  disclaimer paragraph, so they stay together.
- **Probability-Weighted row split from Bull/Base/Bear** — happens when the scenario
  table breaks across pages. Fix: make sure every row has `cantSplit: true` AND tighten
  the Variant Perception table by 1–2 rows so Scenarios fits on the same page.
- **Catalyst Path table colon spacing** — "Constructive: 80%" can wrap awkwardly inside
  a narrow column. Use "Constr. 80%" or "Beat 70%" instead of "Beat: 70%".

## Special-case structures

### Squeeze / market-structure trade (e.g., $CAR)

When the report is about a market-structure trade (short squeeze, distressed
deleveraging, ATM-driven move) rather than a fundamental thesis, modify:

- Replace Scenario PTs with a "Two stocks at the same time" paragraph
- Replace Earnings Model with the credit math (debt stack, EBITDA cover, ATM lever math)
- Heavy emphasis on positioning data (short interest, days to cover, options IV)
- Trade framework dominates over fundamental thesis

### Pre-IPO / private (e.g., Securitize)

- Replace price/market-cap snapshot with "private / pre-IPO SPAC watch" status
- Replace scenario PTs with implied valuation at potential IPO
- Catalyst path becomes "path to public listing" milestones

### Sector-theme report (NOT a single-name report)

These belong in `Reports/sector-theme/`, not equities. They use a different structure —
multi-name basket with sub-categorization. See the `obsidian` skill for routing rules.
