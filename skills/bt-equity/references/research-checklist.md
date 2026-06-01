# BT Equity Report — Research Checklist

What to gather before writing the PDF. Skipping items here causes the report to feel
thin. The order is also the rough sequence of web searches.

## Tier 1 — Identity + Latest Numbers (mandatory)

- [ ] **Current price** (intraday or last close), **market cap**, **52-week range**
- [ ] **Shares outstanding + float**
- [ ] **Most recent quarterly earnings** — release URL, transcript URL, slides URL
  - Revenue (total + by segment)
  - Operating margin (GAAP + non-GAAP)
  - EPS (GAAP + non-GAAP)
  - Operating cash flow + free cash flow
  - Cash + ST investments
  - Total debt + net debt position
- [ ] **Forward guidance** — next quarter rev/EPS/margin guide; FY guide if issued
- [ ] **Confirm the ticker is current.** Pre-IPO names, recent rebrands (e.g., Pure
  Storage → Everpure $P, Apr 2026), or symbol changes can poison a report immediately.

## Tier 2 — Company Quality (high priority)

- [ ] **Business segments** — what does each segment do, what % of revenue, growth
  trajectory by segment over last 4 quarters
- [ ] **End-market mix** — service provider vs hyperscale vs A&D vs consumer; track
  shifts year-over-year
- [ ] **Customer concentration** — name top customers if disclosed; flag any >20% concentration
- [ ] **Recent M&A** — closed deals last 18 months with size, expected synergies, integration
  status. Focus on whether the deal materially changes the thesis.
- [ ] **Capital allocation** — buyback authorization size + execution pace, dividend
  history, debt paydown
- [ ] **Insider activity** — last 90 days of Form 4 filings; was it 10b5-1 routine or
  outside the plan? Who's selling — CEO, CFO, board?

## Tier 3 — Competitive + Macro Context (medium priority)

- [ ] **Top 5 competitors** with rough scale + strength/weakness vs subject
- [ ] **TAM trajectory** — pull a credible market-sizing report or industry forecast
- [ ] **Macro/thematic tailwind or headwind** — AI capex, energy transition, defense
  budgets, reshoring, rate cycle; quantify with hard numbers (e.g., "AI optical TAM
  revised UP 43–46% for 2026/2027 per TrendForce")
- [ ] **Adjacent equity comparables** — what do peers trade at (EV/Sales, EV/EBITDA,
  P/E forward); use 2–3 closest comps, not a wall of names

## Tier 4 — Sentiment + Positioning (medium priority)

- [ ] **Sell-side rating + average PT** — buy / hold / sell distribution; consensus PT
- [ ] **Latest analyst PT actions** — last 30 days, name firms with old → new PT and
  date. Note divergence (e.g., Cowen raised, JPM cut — variance is the signal)
- [ ] **Short interest** — % of float, MoM change, days-to-cover
- [ ] **Implied move into next earnings** — straddle pricing if available
- [ ] **Retail / X / Stocktwits sentiment** — qualitative; flag if memetic or contrarian

## Tier 5 — Catalyst Calendar (high priority)

- [ ] **Next earnings date** — confirmed or expected window
- [ ] **Industry conferences** — investor days, user conferences (e.g., Pure Accelerate)
- [ ] **Regulatory milestones** — NRC approvals, FDA decisions, FTC reviews, etc.
- [ ] **Government contract announcements** — DoD program awards, NASA milestones
- [ ] **Adjacent catalysts** — competitor IPOs, sector reports, hyperscaler CapEx prints

## Tier 6 — Source-of-Truth Documents (when depth required)

For pre-commit dossiers (large positions, longer holds):

- [ ] **Most recent 10-Q / 10-K** — read the risk factors and MD&A
- [ ] **Earnings call transcript** — read it fully, not just the prepared remarks
- [ ] **Investor day presentation** if held in last 12 months
- [ ] **Latest investor day or analyst day Q&A** — managers are most candid here

## What to avoid pulling

- **Stock-screener summaries** — they're aggregator slop. Use them only to find primary
  sources.
- **Reddit / WSB threads as primary sources** — fine for sentiment color, never for facts.
- **Outdated press releases** — anything older than 12 months unless historically material
- **Paywalled content you can't actually access** — don't cite Bloomberg / FT / WSJ unless
  you successfully read the article. If you can only access the headline, don't cite the
  body.

## When sources disagree

- Press release > aggregator > analyst note > stock-screener page
- Pick the more authoritative source
- Note the discrepancy in your sources block (e.g., "MarketBeat shows Q3 rev $1.92B; PR
  Newswire release shows $1.94B — used PR figure")

## Cross-checking before drafting

Before writing a single sentence, verify:

- [ ] **Three most material numbers** in the report agree across at least two sources
- [ ] **The ticker is the current trading symbol** (not a former or pending symbol)
- [ ] **Any analyst PT cited has a date** — undated PTs are stale by default
- [ ] **The bucket / theme name** matches how the company actually positions (don't call
  a fuel-cell company an "AI infra" name unless the company itself frames it that way)

## How long this should take

| Depth                    | Research time   | PDF + companion time |
|--------------------------|-----------------|----------------------|
| Speed-run (snapshot only)| 15 min          | 15 min               |
| Standard                 | 60–90 min       | 60–90 min            |
| Pre-commit dossier       | 3–5 hours       | 2–3 hours            |
| Druckenmiller-tier flagship | 1–2 days     | half-day             |

If you're spending more than 3 hours on research without converging on a thesis, stop
and write what you have as a "Research Brief" — sometimes the act of writing surfaces
the thesis (or its absence).

## Tools to lean on

- **WebSearch** — first pass, finds the source-of-truth URLs
- **WebFetch** — pulls earnings releases, transcripts, IR pages
- **Crawl4AI MCP** (if connected) — for sites that resist WebFetch (SeekingAlpha, broker
  research portals); see `Reports/tools-evals/2026-04-27-crawl4ai-mcp-setup.md`
- **The vault** — check `cortana-vault/research/topics/` and adjacent equity reports
  before researching from scratch; bang may already have notes on the theme
- **Adjacent reports** — if you're researching $X, check `Reports/equities/` for related
  names. Their wiki companions cite the same primary sources you need.
