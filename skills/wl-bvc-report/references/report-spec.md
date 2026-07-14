# BVC Report — Content Spec

## Why each page exists

An executive reads this in under three minutes. Page 1 must land the whole story alone (many
readers stop there). Pages 2–3 are for the skeptic who wants substance. Page 4 is for the person
who forwards it to their technical advisor.

## Page 1 — Cover, executive summary, by the numbers

- Title block: `Build & Value Creation Report` + a dek naming the *product* (e.g. "The AI Growth
  Desk — an agentic commerce command center, designed, built, and shipped by WaiveLabs").
- Executive summary, two paragraphs of prose (never bullets):
  1. What WaiveLabs delivered — application, agents, data foundation, training layer — ending
     with total elapsed build time.
  2. The conventional-team comparison and the compression percentage, with one clause listing
     the disciplines covered (product design, custom visualization, agent layer, secure
     deployment, data engineering, content).
- Two `kpi_strip` blocks of 5 cards each. Pick from: build days, conventional estimate, %
  compression, agent count, LOC, workspace count, data rows, data feeds, est. hours saved/yr,
  "100% human-approved actions". Mark the time/value cards hot.
- Closing `callout` ("The takeaway"): one generalizing sentence — the same approach applies to
  the prospect's business.

## Page 2 — What was built + data foundation

- Workspace/module table: name + one plain-English sentence of what it does *for the executive
  who uses it* (not how it's implemented).
- Data foundation: two paragraphs. Name the vendor systems (Shopify, Amazon, GA4, Klaviyo, paid
  media platforms…) because prospects recognize their own stack in the list — that recognition
  is the sales moment. State total rows and table count. Include the portability line: "the
  connectors change, the application does not."

## Page 3 — Agents + report generation before/after

- Agent table: one row per agent, name + what it does. Intro paragraph carries the governance
  story (reads live data, returns one quantified recommendation, reasoning streamed, human
  approves). Governance is a feature, not a caveat — executives buy control.
- Before/after table: rows = recurring reports/outputs the client's team produces. Columns:
  Report · Conventional · With [product] · Est. saved / yr. Close with a bold `para`
  (color "deep") totaling the annual hours, anchored to something tangible ("about half a
  full-time analyst").

## Page 4 — Stack, why it matters, next step

- Stack table rows: Application, Agent layer, Platform, Security & access, Data engineering.
  Each detail cell says what it is AND why it matters to the buyer ("no secrets ever exposed to
  the browser", "always performs — on stage, on a plane, or in a boardroom").
- Two paragraphs: (1) the operating model end-to-end, ending on "a working application your
  executives can open on Monday morning"; (2) the economics shift — multi-month engagement
  pricing → weeks — ending on the reframed budget question.
- `callout` "Next step": private walkthrough offer, email CTA (mailto only), **end on a
  question** (brand voice rule).
- `brand_band` block last.

## Deriving the numbers (defensible or absent)

- **LOC**: source only. Exclude vendored deps, build output, lockfiles, and duplicated
  `public/` copies. State as "N+" rounded down to the nearest hundred.
- **Build time**: elapsed working days, evidenced by file mtimes / session logs. Don't shave it.
- **Conventional estimate**: sum per-discipline person-weeks, then convert to calendar weeks for
  the stated team size. Rules of thumb from real builds: a bespoke data-heavy workspace with
  custom visualization ≈ 1.5–2 senior-FE weeks; an LLM agent layer with structured tool-calling,
  streaming, and fallback ≈ 1 week if the team has done it before; auth/gating + deploy ≈ 1
  week; calibrated multi-source data engineering ≈ 3–4 weeks (always underestimated — say so);
  curriculum/content ≈ 2–3 weeks and usually needs a writer. Present as a range ("14–16 weeks"),
  never a point estimate.
- **Report savings**: per recurring report, (conventional minutes − new minutes) × annual
  frequency. Round to friendly numbers, prefix "Est.", total to a tangible anchor (fraction of
  an FTE). Never claim revenue impact — hours only, unless the client has given real revenue
  numbers in writing.
- **Compression %**: (1 − build_days / midpoint_conventional_days), rounded to the nearest 5%,
  prefixed "~".

If a number can't be evidenced, leave it out. One indefensible figure poisons the nine
defensible ones — the brand rule is honesty: never claim a result WaiveLabs doesn't hold.
