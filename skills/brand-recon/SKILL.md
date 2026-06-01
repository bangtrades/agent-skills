---
name: brand-recon
description: Investigate a brand or company end-to-end and emit a structured dossier + a reusable per-entity brand skill into the Cortana Obsidian vault. Trigger aggressively whenever the user asks to research, audit, profile, recon, scope out, dig into, or deep-dive any company, brand, ticker, founder, or startup. Also trigger for "investigate X," "build a dossier on X," "find everything about X," "audit X's site + socials + financials," "pre-engagement research on X," "I'm meeting with X tomorrow," or a bare company URL with no other instruction. Use for DTC brands, SaaS, B2B services, consulting prospects, equity targets, and any entity bang is preparing to pitch, partner with, or invest in. Firecrawl by default; Chrome MCP fallback for Meta/Pinterest/LinkedIn. Self-improving — updates a playbook + source catalog after every run. Do NOT trigger for chart-only analysis (use nq-snapshot) or single-ticker BT Stock Reports (use bt-equity).
---

# brand-recon — End-to-End Brand & Company Investigation

You are running bang's standardized brand-recon investigation. Every run produces two compounding artifacts:

1. **A structured dossier** at `~/Cortana/cortana-vault/research/brand-recon/{slug}/dossier.md`
2. **A reusable per-entity brand skill** at `~/Cortana/cortana-vault/research/brand-recon/{slug}/{slug}-brand/` — invocable from any future session to keep deliverables on-brand for that entity

And every run feeds **three self-improving knowledge files** at the brand-recon root:
- `_playbook.md` — what worked, what didn't, lessons by source type
- `_sources.md` — known-good URLs, ranked by yield
- `_runs.md` — index of every investigation with timestamps and links

This skill exists because doing this work cold each time is wasteful. Codify the pattern, capture the learnings, get cumulatively smarter.

---

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
- Write to `~/Cortana/cortana-vault/research/brand-recon/{slug}/dossier.md` with Obsidian frontmatter (see `references/dossier-template.md`)
- Cross-link with `[[wikilinks]]` to related vault pages (existing competitor dossiers, project pages, research topics)

### Phase 13 — Per-entity brand skill emission
- Open `references/brand-skill-template.md` and the skeleton files in `assets/`
- Copy the brand-skill scaffold into `~/Cortana/cortana-vault/research/brand-recon/{slug}/{slug}-brand/`
- Fill in: visual tokens (from Phase 1), voice rules (from Phase 1 + 12), product architecture (from Phase 4 + 8), copy archetypes (synthesized from observed site copy), positioning/claims discipline (synthesized from competitive + sentiment phases)
- Emit `assets/{slug}-tokens.css` and `assets/{slug}-tokens.json` from the captured brand tokens
- Validate: read back the SKILL.md frontmatter to make sure description triggers are pushy and specific

### Phase 14 — Self-improvement closeout (mandatory)
- Follow `references/self-improvement.md` exactly
- Append to `_playbook.md` what worked, what was blocked, novel techniques learned
- Append to `_sources.md` each URL touched with a `quality` rating (high/medium/low) and `firecrawl` vs `chrome` vs `search` access mode
- Append to `_runs.md` a one-line index entry linking to the new dossier

### Phase 15 — Hand back to the user
- Present the dossier file via `present_files`
- Summarize the 3–5 highest-signal findings in chat
- Surface 1–2 open intel gaps the user could close manually
- Offer the brand skill for one-click install if the harness supports it

---

## Output destinations (exact paths)

The vault root is `~/Cortana/cortana-vault/`. All outputs land under it:

| Artifact | Path |
|---|---|
| Per-entity folder | `research/brand-recon/{slug}/` |
| Main dossier | `research/brand-recon/{slug}/dossier.md` |
| Raw scrapes (optional, for audit) | `research/brand-recon/{slug}/raw-scrapes/` |
| Brand skill folder | `research/brand-recon/{slug}/{slug}-brand/` |
| Brand skill entry | `research/brand-recon/{slug}/{slug}-brand/SKILL.md` |
| Brand skill references | `research/brand-recon/{slug}/{slug}-brand/references/*.md` |
| Brand skill assets | `research/brand-recon/{slug}/{slug}-brand/assets/{slug}-tokens.{css,json}` |
| Self-improvement playbook | `research/brand-recon/_playbook.md` |
| Source quality catalog | `research/brand-recon/_sources.md` |
| Run index | `research/brand-recon/_runs.md` |

If `~/Cortana/cortana-vault/` is not accessible (Cowork without that folder mounted), write to the working directory at `./research/brand-recon/{slug}/` and tell the user explicitly that they need to copy the folder into their vault. Never silently write to a different location.

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

- **`obsidian`** — brand-recon is a writer into the vault. The obsidian skill's vault conventions (frontmatter, emoji tags, naming, cross-linking) apply. Use the `📚` emoji tag for dossiers (research) and `🤖` for the per-entity brand skill (AI/tooling). After writing the dossier, append a log entry to `cortana-vault/log.md` following the obsidian skill's log format.
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
