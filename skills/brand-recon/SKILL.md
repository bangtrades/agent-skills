---
name: brand-recon
description: Use when producing a sourced company or brand dossier and an optional reusable brand kit. For a compiler-enforced operating model use enterprise-knowledge-graph-research; for investment dossiers use bt-equity. A bare company URL alone does not request a full investigation.
version: 0.3.0
---

# brand-recon — End-to-End Brand & Company Investigation

You are running bang's standardized brand-recon investigation. A dossier run produces the first artifact below. Produce the second only when reusable brand guidance is requested or needed for authorized downstream work:

1. **A structured dossier** at `~/Cortana/cortana-vault/research/brand-recon/{slug}/dossier.md`
2. **A reusable per-entity brand skill** at `~/Cortana/cortana-vault/_inbox/skills/{slug}-brand/` — invocable from any future session to keep deliverables on-brand for that entity

And every run feeds **three self-improving knowledge files** at the brand-recon root:
- `_playbook.md` — what worked, what didn't, lessons by source type
- `_sources.md` — known-good URLs, ranked by yield
- `_runs.md` — index of every investigation with timestamps and links

This skill exists because doing this work cold each time is wasteful. Codify the pattern, capture the learnings, get cumulatively smarter.

---

## Artifact boundary

Read the current Cortana schema before writing. Emit brand packages only into `_inbox/skills/<name>/`; link the dossier and staged manifest from the research run index. Skill packages use skill frontmatter, while dossiers use vault frontmatter. Never publish an emitted skill from inside a research run.

## What you MUST read before starting

These files are not optional. They contain the actual playbook:

1. `references/investigation-workflow.md` — the 13 ordered phases of an investigation, with exact tool calls
2. `references/source-catalog.md` — the catalog of sources to hit, routed by firecrawl-friendly vs. Chrome-required vs. web-search-only. **This file evolves.** Always read the current version — the playbook updates it after every run.
3. `references/chrome-fallback-guide.md` — when and how to escalate to the Claude in Chrome MCP for sources firecrawl cannot reach (Meta, Pinterest, gated portals)
4. `references/dossier-template.md` — the 13-section dossier structure
5. `references/brand-skill-template.md` — the scaffolding for the per-entity `{slug}-brand` skill that this investigation emits
6. `references/self-improvement.md` — the closing routine that updates `_playbook.md`, `_sources.md`, and `_runs.md`. **This is mandatory at the end of every run.**

Also check, at the brand-recon root in the vault, the current state of `_playbook.md` and `_sources.md`. Previous runs may have flagged sources that are now blocked, paywalled, or producing low-quality output. Trust the playbook over your instincts on the first pass.

---

## The investigation, at a glance

The full workflow is in `references/investigation-workflow.md`. Here's the shape:

### Phase 0 — Scope & setup (60 seconds)
- Confirm entity name, primary URL, and (optionally) ticker / known affiliates with the user via AskUserQuestion if anything is missing or ambiguous.
- Derive `slug` from the entity name (kebab-case, ≤32 chars). Examples: `copperjoint`, `summer-fridays`, `acme-robotics`.
- Create the vault folder: `~/Cortana/cortana-vault/research/brand-recon/{slug}/`.
- Open the task list (TaskCreate) with the phase milestones so the user can watch progress.

### Phase 1 — Visual identity + URL discovery (parallel)
- `firecrawl_scrape` the homepage with `formats: ["markdown", "branding", "links"]` — this single call gives you colors, fonts, components, copy, and links.
- `firecrawl_map` the domain to discover product, blog, about, FAQ, contact, press, and policy pages.
- Capture brand tokens (colors, fonts, radius, button styles) into a working structure for the brand skill emission later.

### Phase 2 — Critical pages (parallel)
- `firecrawl_scrape` the About / Team / Story / Founders page
- `firecrawl_scrape` the FAQ / Help / Education page
- `firecrawl_scrape` the Contact / Investors / Press page
- `firecrawl_scrape` an `agents.md` at `{domain}/agents.md` if it exists — this is a tell that the brand is AI-native (a major signal worth surfacing in the dossier)

### Phase 3 — Press releases & news (parallel)
- `firecrawl_search` for "{Entity} press release", "{Entity} announces", "{Entity} launches"
- `firecrawl_scrape` the top 2–4 most recent press releases — they often reveal ownership changes, leadership, product line architecture, strategic direction
- openPR, PRNewswire, BusinessWire, GlobeNewswire are usually firecrawl-friendly

### Phase 4 — Company profile (web search lane)
- WebSearch: "{Entity} founder year headquarters parent company"
- WebSearch: "{Entity} acquired OR acquisition OR ownership"
- WebSearch: "{Entity} LinkedIn employees CEO"
- WebSearch: "{Entity} Crunchbase ZoomInfo Owler profile"

### Phase 5 — Financial signals (web search lane)
- WebSearch: "{Entity} revenue funding investors valuation"
- WebSearch: "{Entity} SEC EDGAR filings" (for public or recently public entities)
- WebSearch: "{Entity} Amazon best seller rank storefront" (for DTC/B2C)
- WebSearch: "{Entity} pricing tiers ARR MRR" (for SaaS)
- WebSearch: "{Entity} Glassdoor employees salary" (employee count proxy)
- `firecrawl_scrape` any surfaced profile pages on Crunchbase / Owler / RocketReach / D&B / OpenCorporates / SEC EDGAR

### Phase 5b — Claim verification (research-index lane; only when the entity makes scientific, clinical, or technical claims)
- Trigger: health/wellness/supplement/medtech/skincare brands, any "clinically proven" / "study shows" copy captured in Phase 2, any AI/ML vendor citing benchmarks.
- `firecrawl_research_search_papers` for each named claim (ingredient + outcome, device + indication, model + benchmark). `k: 10`.
- `firecrawl_research_read_paper(id, question)` on the top hit to confirm the claim is actually in the body (dose, population, effect size). Abstract-only = unverified.
- `firecrawl_research_related_papers(seed_ids, intent, mode: "citers")` once, to catch replication failures or contradicting evidence.
- Record in the dossier "Claims & compliance" block: claim → source id (`pmid:` / `doi:` / `arxiv:`) → verdict (supported / partial / unsupported / contradicted). This is a selling point in the WaiveLabs pitch (claim-substantiation gap = agent opportunity) and a legal flag for the client.
- Source routing for this lane is in `references/source-catalog.md` → "Phase 5b — Academic / clinical evidence". Canonical vault reference: `[[research/topics/firecrawl-research-index]]`.

### Phase 6 — Customer sentiment (web search lane)
- WebSearch: "{Entity} reviews trustpilot reddit complaints"
- WebSearch: "{Entity} BBB consumer reports"
- `firecrawl_search` for "{Entity} site:reddit.com" — Reddit is rich signal
- `firecrawl_scrape` Trustpilot / BBB / Glassdoor pages where surfaced
- `firecrawl_scrape` the App Store / Google Play reviews if it's a mobile-app entity

### Phase 7 — Competitive landscape
- WebSearch: "{Entity} vs competitor1 vs competitor2"
- WebSearch: "{Entity} alternatives best {category} brands"
- Identify the 4–6 most-cited competitors and capture their positioning, vulnerabilities, and (if available) revenue band

### Phase 8 — Marketplace footprint (if applicable)
- For DTC: scrape Amazon storefront via `firecrawl_scrape` of `amazon.com/stores/{Brand}` — pulls ASIN inventory, reviews, ratings
- For SaaS: scrape G2 / Capterra / TrustRadius listings
- For B2B services: scrape Clutch / GoodFirms / The Manifest

### Phase 9 — Social media footprint (firecrawl with Chrome fallback)
- Try firecrawl on Facebook, Instagram, Pinterest, TikTok, LinkedIn pages. **Firecrawl blocks Meta and Pinterest.** When blocked, fall back to **Claude in Chrome MCP** (`mcp__Claude_in_Chrome__*`) — see `references/chrome-fallback-guide.md`. If Chrome is unavailable, fall back to WebSearch for follower counts and engagement signals.
- Capture: handle, follower count, post cadence (daily/weekly/dormant), content pillars, engagement signal, recent campaign themes

### Phase 10 — People & key affiliates
- WebSearch for named leadership: "{Founder} {Entity}", "{CEO} {Entity} LinkedIn"
- WebSearch for medical/scientific/advisory board members: "{Entity} chief medical officer OR advisor OR scientific board"
- Capture credentialed authorities — they are often dramatically underleveraged dual-brand assets

### Phase 11 — AI/tech posture (the under-rated signal)
- Check `{domain}/agents.md`, `{domain}/.well-known/ucp`, `{domain}/llms.txt`, `{domain}/sitemap.xml` for AI-readiness signals
- Check the page source for Shopify / WooCommerce / Salesforce Commerce / custom stack
- Check footer for: Klaviyo, Recharge, Smile.io, Judge.me, Intercom, Drift, ZenDesk, Gorgias — the stack tells you what they spend money on and what's missing
- Flag any AI signals (agents.md, MCP endpoints, LLM-as-search) prominently — these are huge tells about owner sophistication

### Phase 12 — Dossier synthesis
- Open `references/dossier-template.md` and `assets/dossier.skeleton.md`
- Fill the 13 sections in order: Executive Summary → Company Snapshot → Brand Identity → Product Catalog → Site/Content Architecture → Social Footprint → Marketplace Footprint → Customer Sentiment → Competitive Landscape → Medical/Clinical Authority (or equivalent) → AI/Tech Posture → Strategic Insights & Opportunity Vectors → Open Intel Gaps
- Write to `~/Cortana/cortana-vault/research/brand-recon/{slug}/dossier.md` with Obsidian frontmatter (see `references/dossier-template.md`). The dossier is `type: topic` — never `type: research`, which is a legacy alias the linter re-flags on every pass. `slug`, `created`, `status` and `primary_url` are load-bearing (the research hub roster is a dataview over them) and must never be omitted.
- Cross-link with `[[wikilinks]]` to related vault pages (existing competitor dossiers, project pages, research topics). Section 13 links the run's evidence (`raw-slices/`, `raw-scrapes/00-INDEX`) as wikilinks, never as code-span paths — see "Evidence page contracts" below.

### Phase 13 — Per-entity brand skill emission (when needed)

Skip this phase when the dossier is the only requested artifact. Before emission, compare existing registry, project, and staged packages for this entity. Preserve any existing staged edits; merge a reviewed patch or record a conflict rather than overwriting the shared destination.
- Open `references/brand-skill-template.md` and the skeleton files in `assets/`
- Copy the brand-skill scaffold into `~/Cortana/cortana-vault/_inbox/skills/{slug}-brand/`
- Fill in: visual tokens (from Phase 1), voice rules (from Phase 1 + 12), product architecture (from Phase 4 + 8), copy archetypes (synthesized from observed site copy), positioning/claims discipline (synthesized from competitive + sentiment phases)
- Emit `assets/{slug}-tokens.css` and `assets/{slug}-tokens.json` from the captured brand tokens
- Validate: read back the SKILL.md frontmatter to make sure description triggers are pushy and specific

### Phase 14 — Self-improvement closeout (mandatory)
- Follow `references/self-improvement.md` exactly
- Append to `_playbook.md` what worked, what was blocked, novel techniques learned
- Append to `_sources.md` each URL touched with a `quality` rating (high/medium/low) and `firecrawl` vs `chrome` vs `search` access mode
- Append to `_runs.md` a one-line index entry linking to the new dossier
- The `research/research-hub.md` Brand Recon roster is generated from dossier frontmatter (a dataview over `research/brand-recon` filtered to `file.name = "dossier"`) — do not hand-edit it. Appending the run to `research/brand-recon/_runs.md` is the only hub-facing write a run makes. This is why the dossier's `slug`, `created`, `status` and `primary_url` fields are load-bearing and must never be omitted.

### Phase 14b — Release gate (mandatory; immediately before hand-back)
Run, from the Cortana root, and do not release on a non-zero finding in the entity's tree:

```
python cortana-vault/scripts/vault-lint.py
```

Check `missing frontmatter`, `yaml parse failures`, `status offenders`, `missing emoji`, `legacy-type` warnings and `broken links` for `research/brand-recon/{slug}/`. A run is not done when its own evidence tree fails the contract — repair the page the run wrote, re-lint, then hand back. The linter needs the pinned runtime (Python 3.14 + PyYAML 6.0.3); where that is absent, build it **outside** the vault and pass `CORTANA_VAULT_PYTHON`. Acceptance: `missing frontmatter: 0` and no `legacy-type` warning under the entity tree with **no hand edit in between**.

### Phase 15 — Hand back to the user
- Present the dossier file via `present_files`
- Summarize the 3–5 highest-signal findings in chat
- Surface 1–2 open intel gaps the user could close manually
- Offer the brand skill for one-click install if the harness supports it

---

## Output destinations (exact paths)

The Obsidian root is `~/Cortana`; governed notes live in `cortana-vault/`. Dossiers stay in research; emitted skill packages stage in `_inbox/skills/`:

| Artifact | Path |
|---|---|
| Per-entity folder | `research/brand-recon/{slug}/` |
| Main dossier | `research/brand-recon/{slug}/dossier.md` |
| Raw scrapes (optional, for audit) | `research/brand-recon/{slug}/raw-scrapes/` — every `.md` capture carries the raw-scrape frontmatter below |
| Raw-scrape roll-up index | `research/brand-recon/{slug}/raw-scrapes/00-INDEX.md` — the ONE roll-up file name; never `README.md` / `capture-manifest.md` |
| Slice pages (when slice agents are dispatched) | `research/brand-recon/{slug}/raw-slices/NN-slice-name.md` — every slice carries the slice frontmatter below |
| Brand skill folder | `_inbox/skills/{slug}-brand/` |
| Brand skill entry | `_inbox/skills/{slug}-brand/SKILL.md` |
| Brand skill references | `_inbox/skills/{slug}-brand/references/*.md` |
| Brand skill assets | `_inbox/skills/{slug}-brand/assets/{slug}-tokens.{css,json}` |
| Self-improvement playbook | `research/brand-recon/_playbook.md` |
| Source quality catalog | `research/brand-recon/_sources.md` |
| Run index | `research/brand-recon/_runs.md` |

If `~/Cortana/cortana-vault/` is not accessible (Cowork without that folder mounted), write to the working directory at `./research/brand-recon/{slug}/` and tell the user explicitly that they need to copy the folder into their vault. Never silently write to a different location.

---

## Evidence page contracts (non-negotiable)

Every page a run writes under `research/brand-recon/{slug}/` is a vault page and must pass `vault-lint.py` without a hand edit afterwards. Six consecutive runs (2026-09-08 → 2026-09-17) shipped pages that failed this and were normalized by hand in the daily pass; these contracts repair the generator, not its output.

Rules that apply to **every** page the run writes:

- `tags` takes **exactly one** declared emoji category as its first item and no other emoji. `[📚, 🤖, …]` fails the contract. Brand-recon research pages (dossier, slices, raw scrapes, roll-up index) take `📚`.
- `type` and `status` come from `cortana-vault/scripts/vault-contract.json` (`types` / `statuses`). `research` is a legacy type — use `topic`. `fixed-round-1`, `complete`, `done` are not statuses.
- The six canonical keys (`title`, `type`, `created`, `updated`, `tags`, `status`) come **first, in that order**. Agent-specific keys (`researcher`, `tool_calls`, `fix_round`, `scope`, `confidence`, …) are welcome but go **after** them.
- **Quote any value containing `": "`, or starting with `~`, `>`, `|`, `&`, `*`, `!`, `%`, `@`, or a backtick.** `fix_round: 1 (2026-09-11) — inputs: 07-qa-gate.md` must be written `fix_round: "1 (2026-09-11) — inputs: 07-qa-gate.md"`; the unquoted form makes PyYAML raise `ScannerError` and the page becomes invisible to every frontmatter-driven query.
- `related:` is mandatory and must reach the dossier. Without it the page is a graph orphan and the evidence chain is unreachable.
- The dossier cites its evidence pages as **wikilinks**, never as backtick paths — a code-span path creates no graph edge.

### Slice page contract (every slice agent emits this exact frontmatter)

Applies whenever the run dispatches slice agents (or an orchestrating skill dispatches them on brand-recon's behalf) and they write `raw-slices/NN-slice-name.md`:

```yaml
---
title: "<Entity> — <Slice topic>"
type: slice
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [📚, brand-recon, <entity-slug>, research-slice, <2–3 topic tags>]
status: completed        # draft while in flight; completed on release. NEVER invent a value.
slice: <NN-slice-name>
entity: <Entity>
related:
  - "[[research/brand-recon/<entity-slug>/dossier|<Entity> dossier]]"
  - "[[research/brand-recon/_playbook|Brand-Recon Playbook]]"
  - "[[research/brand-recon/_runs|Brand-Recon Run Index]]"
---
```

Fix-round state belongs in a `fix_round:` key, **not** in `status`.

### Raw-scrape capture rule

Every markdown file written to `raw-scrapes/` gets Cortana frontmatter before the captured body (non-markdown captures such as `01-homepage-branding.json` cannot carry frontmatter and are listed from the roll-up index instead):

```yaml
---
title: "<Entity> — raw capture: <source description>"
type: source
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [📚, brand-recon, <entity-slug>, raw-scrape, evidence]
status: captured
captured: <YYYY-MM-DD>
slice_owner: <NN>
source_url: "<canonical page URL — the page, not a CDN asset>"
related:
  - "[[research/brand-recon/<entity-slug>/dossier|<Entity> dossier]]"
  - "[[research/brand-recon/_sources|Brand-Recon Source Catalog]]"
---
```

**When the captured source has its own YAML front matter** (Hugging Face model cards, Jekyll/Hugo pages, `llms.txt` variants): do not leave it at the top of the file, where it becomes the page's frontmatter. Write the Cortana block above, then reproduce the upstream YAML inside a fenced ` ```yaml ` block in the body under an "Upstream front matter (verbatim capture)" heading. Source fidelity is preserved and the page still parses as a vault page.

### Raw-scrape roll-up index (`raw-scrapes/00-INDEX.md`)

The roll-up has no single `source_url` or `slice_owner`, so it takes this shape instead. It is always named `00-INDEX.md` — the library previously split three ways (`README.md` as `source`/`archived`, `capture-manifest.md` as `reference`/`captured`, or nothing at all); one name, one shape:

```yaml
---
title: "<Entity> — Raw Scrape Capture Index"
type: source
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [📚, brand-recon, raw-scrapes, <entity-slug>, provenance, firecrawl]
status: captured
captured: <YYYY-MM-DD>
related:
  - "[[research/brand-recon/<entity-slug>/dossier|<Entity> dossier]]"
  - "[[research/brand-recon/_sources|Brand-Recon Source Ledger]]"
---
```

The dossier's Section 13 must link this index as a wikilink (`[[research/brand-recon/<entity-slug>/raw-scrapes/00-INDEX|Raw scrape index]]`), not a code-span path.

---

## What this skill does NOT produce

This is critical to keep in mind, because the natural impulse is to do more. **Do not produce:**
- Pitch decks
- Investor decks
- Demo web apps or artifacts
- Live dashboards
- Marketing collateral
- Pricing recommendations
- A "next steps" implementation plan beyond the "Strategic Insights & Opportunity Vectors" section of the dossier

Those are downstream deliverables that a *different* engagement (or a different skill) builds on top of the dossier and brand skill. Keep brand-recon's surface area tight. If the user wants a pitch deck after seeing the dossier, that's a separate ask.

---

## Quality bar

The dossier should be useful to bang six months from now when he's forgotten the details. Concretely:
- **Specific numbers everywhere.** Not "many reviews" — "2,271 reviews at 4.1★ on the hero ASIN."
- **Sourced claims.** Every non-obvious claim in the dossier ties to a URL in the frontmatter `sources:` block.
- **Strategic synthesis, not data dump.** The "Strategic Insights" section is the most important part — it earns the dossier its existence. Be opinionated about what the leverage points are.
- **Honest about gaps.** "Open Intel Gaps" is mandatory and is the user's roadmap for what they need to find manually.
- **On-brand visual extraction.** The captured tokens should be tight enough that the emitted `{slug}-brand` skill produces deliverables indistinguishable from the entity's own design system.

---

## Coordination with other skills

- **`obsidian`** — brand-recon is a writer into the vault. The obsidian skill's vault conventions (frontmatter, emoji tags, naming, cross-linking) apply. Use the `📚` emoji tag for dossiers, slices and raw scrapes (research) and `🤖` for the per-entity brand skill (AI/tooling) — exactly one emoji per page, never both. After writing the dossier, append a log entry to `cortana-vault/log.md` following the obsidian skill's log format. Do not touch `research/research-hub.md`; its Brand Recon roster is derived from dossier frontmatter.
- **`bt-equity`** — when investigating a single ticker for a BT Stock Report, brand-recon can be invoked first to capture the brand intelligence layer that bt-equity then synthesizes into the published PDF. The dossier becomes a research input for bt-equity.
- **`yt`** — if the entity has a founder/CEO/medical-advisor with substantive YouTube content, optionally invoke the yt skill on 1–2 hero videos and link the resulting transcript pages from the dossier.
- **`canvas-design` / `frontend-design` / `pptx` / `docx`** — these are format skills that the *emitted* `{slug}-brand` skill pairs with downstream. brand-recon itself does not invoke them.

---

## Self-improvement is non-negotiable

Phase 14 must run on every investigation. The skill exists to compound knowledge. If you skip the playbook update because the run was "obvious," you've broken the contract.

The minimum playbook update is one bullet per major finding:
- `2026-05-27 — copperjoint — Firecrawl blocks Facebook, Instagram, Pinterest. Pivot to WebSearch for handle + follower band, Chrome MCP for live counts.`
- `2026-05-27 — copperjoint — agents.md at /agents.md is a major AI-posture signal worth its own dossier section.`

Each entry is a small payment into the bank. Over 20 investigations, this skill becomes uncannily good at knowing exactly which sources to hit first for each entity type.

---

## Final reminder

Run the full sweep every time unless the user explicitly says "lean pass" or "quick look." Bang chose full-sweep as the default for a reason — partial dossiers create more open questions than they answer. If a phase produces no useful signal, document the negative result in `_sources.md` and move on. Negative results are also data.

---

## Changelog

### 2026-09-20 — v0.3.0 — four staged patches applied

| Patch | Effect |
|---|---|
| `PATCH-2026-09-10-firecrawl-research-index.md` | New Phase 5b claim-verification lane (`firecrawl_research_*`); `research-index` route + "Phase 5b — Academic / clinical evidence" block in `references/source-catalog.md`; tool-namespace note in `references/investigation-workflow.md`; "Claims substantiation" table in the dossier template/skeleton. |
| `PATCH-2026-09-12-evidence-frontmatter-contract.md` | New "Evidence page contracts" section (slice page contract, raw-scrape capture rule, key-order/quoting/one-emoji rules); Phase 14b `vault-lint.py` release gate; dossier `type: research` → `type: topic` in `references/dossier-template.md`, `assets/dossier.skeleton.md`, `references/investigation-workflow.md`; dossier §13 cites evidence as wikilinks, not code-span paths. |
| `PATCH-2026-09-18-dossier-type-and-raw-scrape-frontmatter.md` | Superseded stub (`type: redirect`) — folded into the hub-roster patch; nothing applied. |
| `PATCH-2026-09-18-hub-roster-is-derived-not-hand-kept.md` | Amends 09-12 §2: one roll-up file (`raw-scrapes/00-INDEX.md`, `type: source` / `status: captured`) with its own frontmatter shape, wikilinked from dossier §13; the skill gains NO write step to `research/research-hub.md` — `_runs.md` is the only hub-facing write, and dossier `slug`/`created`/`status`/`primary_url` are load-bearing. |

Also in this release: the `_playbook.md` / `_sources.md` / `_runs.md` seed templates now carry the same vault frontmatter as the live ledgers (`🔧`, `type: source`/`index`, `status: active`), so a bootstrap run cannot emit a frontmatter-less ledger page.
