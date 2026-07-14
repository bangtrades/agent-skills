---
name: wl-bvc-report
description: >-
  Generate a WaiveLabs-branded Build & Value Creation Report — the client-facing PDF that
  summarizes what WaiveLabs built, how fast it was built versus a conventional design/dev team,
  the AI agents delivered, estimated recurring time savings, and the tech stack. Use this skill
  aggressively whenever bang asks for a "BVC report", "build report", "value creation report",
  "build summary for a client/prospect", "show what we built and what it's worth", "ROI one-pager
  for the build", or wants prospect-facing collateral quantifying a WaiveLabs engagement. Also
  trigger after finishing any client build when bang wants materials to show prospective clients.
  Produces a 4-page branded PDF via a bundled config-driven engine with a built-in client-safe
  language lint (no client names, no "simulated data", no "prototype"). Pairs with brand-waive
  (brand layer is baked into the engine). Do NOT use for pitch decks (client-pitch), proposals,
  or single-client demo apps.
---

# WaiveLabs — Build & Value Creation Report (`wl-bvc-report`)

A BVC report converts a finished WaiveLabs build into prospect-facing proof: *this is what we
built, this is how fast, this is what it would have cost the old way, and this is the recurring
value*. The audience is a prospective client's executive team — people who will never read code
and get confused (or suspicious) by engineering vocabulary. Everything about this skill is
designed to keep the story simple, quantified, and honest.

## Workflow

### 1. Gather the build facts (measure, don't guess)

Work from the actual project on disk and the session history:

- **Lines of code** — count real source only: exclude `node_modules`, `.next`, `.git`, lockfiles,
  and any `public/` copies that duplicate source. Round down to a clean "N+" figure.
- **Build time** — elapsed working days from first file to deployed application (file mtimes and
  session dates are your evidence).
- **Inventory** — workspaces/views, AI agents (list each with what it does), data tables/feeds and
  total rows, deployment surface, access-control features.
- Read `references/report-spec.md` for how to derive the comparison estimate (conventional team
  weeks) and the report-generation savings table. These numbers must be defensible — a prospect
  will poke at them.

### 2. Draft the content as a config

Copy `examples/example_report.json` and replace every value. The engine handles all layout,
brand, fonts, and chrome — you write only content. Structure (4 pages, in this order, because it
mirrors how an executive reads: outcome → substance → value → credibility):

1. **Cover + executive summary + "By the numbers"** — two prose paragraphs (what was built and
   the time comparison), then two 5-card KPI strips. Mark 3–4 of the 10 KPIs `"hot": true`
   (orange) — the time/value ones, never more, orange is the spark not the flood.
2. **What was built + the data foundation** — workspace table plus two prose paragraphs on the
   data layer, framed as *"engineered to the exact export formats of the systems a modern brand
   already runs"*.
3. **The agents + report generation before/after** — one table row per agent (governance framing
   in the intro: reasoning streamed, human approves), then the before/after table with an
   "Est. saved / yr" column and a bold one-line total.
4. **Technology stack + why this matters + next step** — stack table in plain English (each row:
   what the layer is, why the client should care), two closing paragraphs, a "Next step" callout
   **ending on a question**, and the `brand_band` block (navy footer, email CTA — never a
   calendar link).

Read `references/language.md` before writing a single sentence. The short version: the client is
"a high-growth [category] brand", never named; it's an "application", never a "prototype"; it's
"data", never "simulated/mock/synthetic data"; savings are always "estimated".

### 3. Render

```bash
python3 <skill>/scripts/build_report.py report.json
```

The engine lints every string against the forbidden-terms list first (exit 3 = fix the flagged
copy; nothing renders). Add engagement-specific words to `client_terms` in the config — the
client's brand name, hero products, retail partners, founders — so a stray mention can't slip
through. Exit 2 means a block overflowed its page: the warning names the block and the overage in
inches; trim that copy and re-run. Requires `reportlab` and `fonttools`
(`pip install reportlab fonttools --break-system-packages`); fonts download once and cache.

### 4. Verify before shipping

Render pages to PNG (`pdf2image` at ~80 dpi) and *look at every page* — check margins, table
collisions with the footer, and the KPI strip labels. Then run one final text-level scan:

```bash
pdftotext out.pdf - | grep -i -E "<client terms|forbidden terms>" || echo CLEAN
```

The lint checks the config; this checks the artifact. Both, always — this document goes in front
of prospects, and one leaked client name undoes the whole "confidential" promise.

## Config reference

Block types for `pages[].blocks[]`: `title` (text + dek), `h2` (text, optional accent
"orange"|"blue"), `para` (text; optional size/lead/bold/color "mute"|"deep"/after), `kpi_strip`
(items: value/label/hot), `table` (headers/rows/widths — widths in inches, `null` = flex),
`callout` (title/text — cream box, sun border, use for the key insight and the next step),
`brand_band` (tagline/contact — final page only). Top-level: `output`, `doc_type`, `date_line`,
`title` is set via a title block, `forbidden_terms` (override the default lint list),
`client_terms` (engagement-specific blocklist).

## References

- `references/report-spec.md` — page-by-page content spec, metric derivation rules, KPI selection
- `references/language.md` — client-safe language rules with before/after rewrites
- `examples/example_report.json` — complete working config (fictional client) to copy from
