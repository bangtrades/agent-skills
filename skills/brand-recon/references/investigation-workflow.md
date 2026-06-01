# Investigation Workflow — 13 Phases, In Order

This is the detailed playbook. SKILL.md gave you the shape; this file gives you the exact tool calls and decision points. Read it once at the start of a run, then execute.

## Conventions

- All `firecrawl_*` calls refer to tools under `mcp__7a79858f-1e94-4bbd-a8dc-5a71900f68b5__firecrawl_*` (or whatever the firecrawl MCP server is namespaced as in the current session — load via ToolSearch if deferred).
- `WebSearch` is the built-in search tool. Load via ToolSearch if deferred.
- `mcp__Claude_in_Chrome__*` are the Chrome MCP tools. Load via ToolSearch if deferred. Use only when firecrawl is blocked — see `chrome-fallback-guide.md`.
- `Read`, `Write`, `Edit` are filesystem tools — used to write the dossier, brand skill, and self-improvement files.
- `TaskCreate` / `TaskUpdate` track progress visibly.
- `AskUserQuestion` is for clarification BEFORE the run starts. Do not interrupt a run mid-phase with questions unless something is genuinely blocking.

---

## Phase 0 — Scope & setup

Goal: confirm the investigation target and create the working scaffold.

1. Confirm with the user (via AskUserQuestion if not provided): entity name, primary URL, optional ticker, any known aliases.
2. Derive `slug` from the entity:
   - Lowercase, kebab-case, ≤32 chars
   - Strip suffixes like `, Inc.`, `LLC`, `Holdings`
   - Examples: `CopperJoint, LLC` → `copperjoint`; `Summer Fridays` → `summer-fridays`; `Acme Robotics Inc.` → `acme-robotics`
3. Create the vault folder structure:
   ```
   ~/Cortana/cortana-vault/research/brand-recon/{slug}/
   ~/Cortana/cortana-vault/research/brand-recon/{slug}/raw-scrapes/
   ~/Cortana/cortana-vault/research/brand-recon/{slug}/{slug}-brand/
   ~/Cortana/cortana-vault/research/brand-recon/{slug}/{slug}-brand/references/
   ~/Cortana/cortana-vault/research/brand-recon/{slug}/{slug}-brand/assets/
   ```
4. Read the current `_playbook.md` and `_sources.md` to inherit prior learnings. If they don't exist yet, this is the bootstrap run — the seed playbook ships in this skill's `assets/playbook.seed.md`.
5. Create the TaskList with 14 phase milestones so the user can watch progress.

---

## Phase 1 — Visual identity + URL discovery

Goal: capture brand tokens (colors, fonts, components) and the site's URL inventory in a single pass.

**Parallel calls (run in the same message):**

```
firecrawl_scrape({
  url: "{primary_url}",
  formats: ["markdown", "branding", "links"],
  onlyMainContent: false
})

firecrawl_map({
  url: "{primary_url}",
  limit: 200
})
```

The `branding` format returns colors, fonts, button styles, and inferred design system in one call — do not waste subsequent calls extracting these from CSS.

**From the homepage scrape, capture into a working structure:**
- Primary, secondary, accent, background colors (hex)
- Font families (heading, body, special-use)
- Button radii and styles
- Logo URL and color treatment
- All header/footer/hero copy (later feeds voice analysis)
- All social links (later feeds Phase 9)
- All "as seen on" / press mentions visible on the homepage

**From the map, classify URLs into buckets:**
- Product pages
- Collection / category pages
- About / Team / Founder / Story
- FAQ / Help / Education
- Blog channels
- Policy pages
- Press / Investors
- agents.md / robots.txt / well-known paths (worth a try)

Save the raw branding JSON to `raw-scrapes/01-homepage-branding.json` for the audit trail.

---

## Phase 2 — Critical pages (parallel)

Goal: capture the verbal voice and the company-context pages.

**Parallel calls:**

```
firecrawl_scrape({ url: "{about_page_url}", formats: ["markdown"], onlyMainContent: true })
firecrawl_scrape({ url: "{faq_page_url}", formats: ["markdown"], onlyMainContent: true })
firecrawl_scrape({ url: "{contact_or_press_url}", formats: ["markdown"], onlyMainContent: true })
firecrawl_scrape({ url: "{primary_url}/agents.md", formats: ["markdown"] })
```

The `agents.md` check is cheap and reveals AI-readiness. If it 404s, fine; if it exists, this is a major dossier finding for the AI/Tech Posture section.

Optional, if the entity is heavily content-driven, also scrape:
- The blog hub page
- One top-of-funnel education page (best-of-class voice sample)

Save all to `raw-scrapes/02-*.md`.

---

## Phase 3 — Press releases & news

Goal: capture the announcement timeline and ownership story.

**Step 1 — Search:**

```
firecrawl_search({
  query: "\"{Entity Name}\" press release announces launches",
  limit: 10
})

WebSearch({
  query: "{Entity Name} press release 2025 OR 2026 launch announcement"
})
```

**Step 2 — Scrape the top 2–4 most recent releases that are NOT direct duplicates.** Common sources that are firecrawl-friendly:
- openpr.com (very firecrawl-friendly)
- prnewswire.com (usually works)
- businesswire.com
- globenewswire.com
- markets.financialcontent.com (syndication)

Pay attention to:
- Dates and HQ city in the press dateline (city is often more recent than registered HQ)
- Named spokespeople and titles (these are the contacts)
- Quoted positioning language (this is the brand's own narrative)
- Ownership / acquisition / leadership changes
- Product line launches and the strategic rationale

Save raw to `raw-scrapes/03-press-*.md`.

---

## Phase 4 — Company profile

Goal: build the company-snapshot section. Founder, year, HQ, ownership, employees.

**Parallel WebSearch calls:**

```
WebSearch({ query: "{Entity} founder history founding year headquarters" })
WebSearch({ query: "{Entity} acquired OR acquisition parent company ownership" })
WebSearch({ query: "{Entity} CEO leadership LinkedIn" })
WebSearch({ query: "{Entity} Crunchbase ZoomInfo Owler company profile" })
```

**Then `firecrawl_scrape` any surfaced profile pages** from Crunchbase, ZoomInfo, RocketReach, Owler, D&B, OpenCorporates. Many of these are paywalled — capture what's visible on the public profile shell, don't try to break paywalls.

**State of corporation filings** (for US LLCs): the entity's registered LLC may be in a different state than its operating HQ (very common: Wyoming, Delaware registration, real operations elsewhere). Note both.

If the entity is public, also:
```
WebSearch({ query: "{Ticker} SEC EDGAR 10-K most recent" })
firecrawl_scrape({ url: "{sec_filing_url}", formats: ["markdown"] })
```

---

## Phase 5 — Financial signals

Goal: revenue estimate, valuation, funding, marketplace performance. Anything quantifiable.

```
WebSearch({ query: "{Entity} revenue annual funding investors valuation" })
WebSearch({ query: "{Entity} Glassdoor employees count" })
WebSearch({ query: "{Entity} Amazon best seller storefront BSR" })   // DTC
WebSearch({ query: "{Entity} pricing SaaS tier ARR" })               // SaaS
WebSearch({ query: "{Entity} App Store Google Play downloads ranking" }) // mobile
```

If the entity has a Crunchbase / Owler / PitchBook profile that surfaces revenue band, capture the band even if it's a wide range. Note in the dossier whether the number is self-reported, RocketReach-estimated, or based on a real disclosure.

Marketplace ASIN-level scrapes are valuable enough to do in parallel during this phase if the entity is DTC:
```
firecrawl_scrape({ url: "https://www.amazon.com/stores/{Brand}", formats: ["markdown"] })
firecrawl_scrape({ url: "{specific_hero_asin_url}", formats: ["markdown"] })
```

---

## Phase 6 — Customer sentiment

Goal: what do real customers say? Both top-line aggregates (4.x stars on N reviews) and the topic-level themes.

```
WebSearch({ query: "\"{Entity}\" reviews trustpilot reddit complaints" })
WebSearch({ query: "\"{Entity}\" BBB consumer reports rating" })

firecrawl_search({
  query: "\"{Entity}\" site:reddit.com",
  limit: 10
})

firecrawl_search({
  query: "{Entity} trustpilot OR bbb OR cusrev review",
  limit: 10
})
```

Then scrape the surfaced Trustpilot / BBB / Reddit / CusRev pages. Reddit is particularly high-signal — bring back representative quotes (especially the negative ones).

For mobile-app entities: also scrape the App Store and Google Play listing pages and capture the rating distribution + recent reviews.

**Capture by theme, not by reviewer.** Group sentiment into 5–8 topics (comfort, fit, return process, customer service, durability, etc.) and tag each with positive % vs negative %.

---

## Phase 7 — Competitive landscape

Goal: identify the 4–6 most-cited competitors and capture positioning + vulnerabilities.

```
WebSearch({ query: "{Entity} vs alternative best {category} brands 2026" })
WebSearch({ query: "{Entity} competitor analysis" })
WebSearch({ query: "best {category} brands comparison" })
```

For each surfaced competitor, capture:
- Estimated revenue band
- Positioning one-liner
- Distribution channels
- Known vulnerabilities (FTC actions, recalls, customer complaints, lawsuits) — these become strategic wedges in the dossier

Look hard for "strategic wedges" — moments when a category leader has lost credibility, exited a segment, or been publicly punished. These are the most actionable opportunities a dossier can surface.

---

## Phase 8 — Marketplace footprint (if applicable)

Goal: deep marketplace intel for entities that depend on Amazon / G2 / Clutch / App Store.

For DTC brands on Amazon:
- Scrape the brand storefront
- Identify the hero ASIN (highest review count) and scrape it
- Note review velocity (recent reviews / total reviews)
- Look at the brand-store copy — older brand stores often hold legacy voice that has drifted from the new site (this is a major coherence finding — see CopperJoint as the reference case)

For SaaS:
- Scrape G2 / Capterra / TrustRadius — they expose rating, review count, segment fit

For B2B services:
- Scrape Clutch / GoodFirms / The Manifest — they expose project size, industry mix, client logos

For mobile apps:
- Scrape App Store + Google Play listing
- Note rating trend over time if visible

---

## Phase 9 — Social media footprint

Goal: handle, follower count, cadence, content pillars, engagement signal.

**Try firecrawl first on each platform:**
```
firecrawl_scrape({ url: "https://www.facebook.com/{handle}", formats: ["markdown"], waitFor: 5000 })
firecrawl_scrape({ url: "https://www.instagram.com/{handle}/", formats: ["markdown"], waitFor: 5000 })
firecrawl_scrape({ url: "https://www.pinterest.com/{handle}/", formats: ["markdown"], waitFor: 5000 })
firecrawl_scrape({ url: "https://www.tiktok.com/@{handle}", formats: ["markdown"], waitFor: 5000 })
firecrawl_scrape({ url: "https://www.linkedin.com/company/{handle}", formats: ["markdown"], waitFor: 5000 })
firecrawl_scrape({ url: "https://www.youtube.com/@{handle}", formats: ["markdown"], waitFor: 5000 })
```

**Known firecrawl-blocked platforms** (as of bootstrap, may change — check `_sources.md`):
- Facebook (Meta) — always blocked
- Instagram (Meta) — always blocked
- Pinterest — always blocked
- LinkedIn — sometimes works, often blocked
- TikTok — variable

**When blocked, escalate to Claude in Chrome MCP** per `chrome-fallback-guide.md`. If Chrome is unavailable in this session, fall back to:
```
WebSearch({ query: "{Entity} Facebook followers Instagram official social media" })
WebSearch({ query: "{Entity} TikTok handle viral video" })
```

WebSearch often surfaces follower bands ("2.4K Facebook followers"), recent post snippets, and engagement hints. It's a degraded but acceptable fallback for the dossier's social section.

---

## Phase 10 — People & key affiliates

Goal: catalog the named humans who matter to the brand.

```
WebSearch({ query: "\"{Founder Name}\" {Entity} background career" })
WebSearch({ query: "{Entity} chief medical officer OR scientific advisor OR board" })
WebSearch({ query: "{Entity} leadership team executives" })
```

For credentialed advisors (doctors, scientists, athletes, celebrities), also:
```
firecrawl_scrape({ url: "{advisor_personal_site_url}", formats: ["markdown"] })
WebSearch({ query: "\"{Advisor Name}\" published works credentials" })
```

A named, credentialed advisor with a real professional reputation is often **the most underleveraged brand asset**. Surface them prominently in the dossier's "Medical/Clinical Authority" section (or rename that section as appropriate — "Scientific Authority," "Athletic Authority," "Engineering Authority").

---

## Phase 11 — AI/tech posture

Goal: probe the entity's technical sophistication and AI-readiness. This section can completely change the consulting narrative.

**Probe these URLs (all cheap, all worth trying):**
```
firecrawl_scrape({ url: "{primary_url}/agents.md", formats: ["markdown"] })
firecrawl_scrape({ url: "{primary_url}/llms.txt", formats: ["markdown"] })
firecrawl_scrape({ url: "{primary_url}/.well-known/ucp", formats: ["markdown"] })
firecrawl_scrape({ url: "{primary_url}/robots.txt", formats: ["markdown"] })
firecrawl_scrape({ url: "{primary_url}/sitemap.xml", formats: ["markdown"] })
```

**Read the page source signals captured in Phase 1:**
- E-commerce stack: Shopify / WooCommerce / BigCommerce / Salesforce Commerce / custom
- Loyalty: Smile.io / Yotpo / LoyaltyLion
- Reviews: Judge.me / Yotpo / Stamped / Okendo
- Email: Klaviyo / Mailchimp / Drip (often inferable from footer or page source)
- Subscriptions: Recharge / Skio / Bold
- CS: Intercom / Drift / Gorgias / ZenDesk
- Analytics: Google Analytics 4 / Mixpanel / Heap (visible in page source)
- A/B testing: Optimizely / VWO / GrowthBook

Each of these is a buy signal. The presence of agents.md / llms.txt / UCP is a major AI-posture signal worth its own dossier subsection — these brands have already opted into the agentic future.

---

## Phase 12 — Dossier synthesis

Goal: write the final dossier markdown to the vault.

1. Open `assets/dossier.skeleton.md` (skeleton with placeholders) and `references/dossier-template.md` (section-by-section guidance).
2. Fill the 13 sections in order. Use specific numbers everywhere, link sources in the frontmatter `sources:` block, cross-link to vault peers with `[[wikilinks]]`.
3. Write to `~/Cortana/cortana-vault/research/brand-recon/{slug}/dossier.md`.
4. The dossier frontmatter must include the obsidian skill's required fields:
   ```yaml
   ---
   title: "{Entity Name} — Brand & Company Intel Dossier"
   type: research
   created: YYYY-MM-DD
   updated: YYYY-MM-DD
   tags: [📚, brand-recon, dossier, {category}, {key-themes}]
   status: active
   slug: {slug}
   primary_url: {url}
   sources: [list of every URL touched]
   related: [vault pages this is cross-linked to]
   ---
   ```
5. Verify the dossier passes the "6-month test": will bang find this useful in October when he has forgotten the details?

---

## Phase 13 — Per-entity brand skill emission

Goal: emit a fully populated `{slug}-brand` skill that any future session can invoke.

1. Open `references/brand-skill-template.md` and the skeleton files in `assets/`:
   - `brand-SKILL.skeleton.md`
   - `visual-tokens.skeleton.md`
   - `voice-and-tone.skeleton.md`
   - `product-architecture.skeleton.md`
   - `copy-archetypes.skeleton.md`
   - `positioning-and-claims.skeleton.md`
   - `tokens.css.skeleton`
   - `tokens.json.skeleton`

2. Substitute the per-entity values:
   - `{ENTITY_NAME}` — the human-readable brand name (e.g., "CopperJoint")
   - `{slug}` — kebab-case (e.g., `copperjoint`)
   - `{SLUG_UPPER}` — token prefix uppercase (e.g., `COPPERJOINT`)
   - All color, font, and component values from Phase 1
   - Voice rules synthesized from FAQ / about / press copy
   - Product architecture from product / collection scrapes
   - Copy archetypes extracted from real observed site copy
   - Positioning + claims discipline informed by the competitive + sentiment phases

3. Write all files into `~/Cortana/cortana-vault/research/brand-recon/{slug}/{slug}-brand/`.

4. The brand-skill SKILL.md frontmatter must have a *pushy, specific* description. Generic descriptions undertrigger. Lift the pattern from the CopperJoint brand skill that already exists.

5. Verify the brand skill is self-sufficient: a fresh agent reading only the brand skill should be able to produce on-brand deliverables without re-reading the dossier.

---

## Phase 14 — Self-improvement closeout

Goal: leave the playbook smarter than you found it.

Follow `references/self-improvement.md`. Concretely:
1. Append a `## YYYY-MM-DD — {slug}` block to `_playbook.md` summarizing:
   - What worked unusually well
   - What was blocked or low-yield
   - Novel techniques or sources discovered
2. Append per-URL entries to `_sources.md` with `quality: high|medium|low` and `access: firecrawl|chrome|search|paywall` tags
3. Append one row to the index table in `_runs.md`

This step is mandatory. Skipping it breaks the contract that makes the skill compounding.

---

## Phase 15 — Hand back to the user

Goal: surface the highlights and offer the brand skill for install.

1. Call `present_files` on the dossier path so the user can open it immediately.
2. In chat, surface the 3–5 highest-signal findings as a brief bulleted summary.
3. Surface 1–2 open intel gaps — things the user can close manually (e.g., "Live Instagram follower count needs a 30-second manual check, my socials access was degraded").
4. Offer the brand skill for one-click install if the harness supports `.skill` packaging.
5. Optionally: offer to schedule a re-run in 90 days to detect drift (use the `schedule` skill if available).

---

## Failure modes to watch

- **Premature synthesis.** Don't draft the dossier while phases are still in flight. Hold synthesis for Phase 12.
- **Source dump instead of synthesis.** The dossier is opinionated analysis, not a list of links. The links live in the `sources:` frontmatter; the body is judgment.
- **Skipping the playbook update.** Phase 14 is mandatory.
- **Hallucinated stats.** If a number isn't sourced, mark it as "estimated" or "self-reported, unverified."
- **Trying to break paywalls.** Don't. Capture what's visible on the public shell, move on.
- **Forgetting the brand skill.** The dossier without the emitted `{slug}-brand` skill is half the value. Don't ship without both.
