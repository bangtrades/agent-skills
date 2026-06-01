# Dossier Template — Section-by-Section Guidance

The actual skeleton lives at `assets/dossier.skeleton.md`. This file explains what goes in each section, in what tone, and what to NOT include.

The dossier is the centerpiece deliverable. It should be useful to bang six months from now when he's forgotten the details. The bar is: opinionated synthesis with concrete numbers, not a list of links.

## Frontmatter

```yaml
---
title: "{Entity Name} — Brand & Company Intel Dossier"
type: research
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [📚, brand-recon, dossier, {category-tag}, {key-themes}]
status: active
slug: {slug}
primary_url: https://{domain}
entity_legal_name: {Legal name with suffix}
hq_operating: {City, State}
hq_legal: {City, State}   # often different from operating HQ for US LLCs
founded: YYYY
sources:
  - https://...
  - https://...
related:
  - "[[vault page 1]]"
  - "[[vault page 2]]"
---
```

The `tags` field must lead with the obsidian skill's category emoji. For dossiers it's `📚` (Research). The `primary_url`, `slug`, and entity metadata fields are non-standard but useful for dataview queries inside Obsidian later.

The `sources` list must include **every URL** the investigation touched that the dossier's claims depend on. Don't bury sources in the body — they belong in frontmatter so they're queryable.

The `related` list is for Obsidian wikilinks to other vault pages — competitor dossiers, project pages, research topics. This is what populates the graph view edges.

## Section 0 — Executive Summary

One paragraph. The bar: someone who reads only this paragraph should understand the entity's stage, the most important strategic insight, and one actionable hook.

**Pattern:**
> {Entity} is a {age} {category} brand {key context — undergoing X, recently Y, owned by Z}. {One paragraph of synthesis covering: scale, ownership, defensible asset, competitive position, and the single most actionable opportunity.} {Closing sentence with the strategic wedge or hook.}

DO NOT use bullets in the executive summary. It's a paragraph, not an outline.

## Section 1 — Company Snapshot

A table of firmographic facts with sources. Every cell is a discrete fact.

Columns: **Field | Value | Source**

Rows (omit any you can't source — better empty than wrong):
- Legal entity
- Founded year
- Founder(s)
- Current ownership / parent
- Legal HQ
- Operating HQ
- Self-reported / estimated revenue
- Employee count (and source — LinkedIn band, Glassdoor estimate, etc.)
- Platform / stack
- Geographic reach
- Press cadence
- Chief Medical/Scientific/Athletic Advisor (if applicable)

End the section with a one-paragraph "Why this matters for our pitch / engagement" call-out. This is the moment to connect firmographic facts to the strategic story.

## Section 2 — Brand Identity (Visual + Verbal)

Two subsections.

### 2.1 Visual System

A token table extracted via the firecrawl `branding` format:
- Primary color (hex + role name)
- Secondary color
- Accent color
- Background color
- Text colors
- Font primary
- Font secondary
- Button styles (radii, padding)
- Logo treatment

Plus a "Design observation" paragraph that interprets the system. Is it minimal? Maximalist? Clinical? Playful? Trend-aware? What aesthetic competitor does it most resemble?

### 2.2 Verbal System

- Voice descriptors (4–6 adjectives)
- Recurring nouns (lift from observed copy)
- Recurring verbs
- Claim posture (hedged? aggressive? medical? performance-bro?)
- Pillars (the 3–5 things the brand says about itself, in their own words)
- Slogans / wordmarks / taglines spotted in the wild

End this section with the **most important diagnostic finding**: where does the verbal system DRIFT across channels? Site voice vs. Amazon voice vs. press release voice vs. social voice. Coherence gaps are the most actionable brand-side finding you can surface.

## Section 3 — Product Catalog & Architecture

Three subsections.

### 3.1 Product lines / sub-brands

Each line gets its own paragraph: audience, positioning, tone, hero products.

### 3.2 SKU inventory

A list (not exhaustive — top 10–20 most signal-bearing) of hero singletons and bundles with URLs.

### 3.3 Collection / merchandising axes

How many ways do they slice the catalog? (Body part, persona, condition, use case, line?) Sophistication here is itself a finding.

End with a strategic read — what does the catalog architecture tell you about who they think their customer is?

## Section 4 — Site & Content Architecture

- Information architecture (nav structure)
- Content engine (blog channels, content depth)
- Loyalty / retention stack (Smile, Yotpo, Klaviyo, etc.)
- Trust signals (review widgets, badges, advisory boards, etc.)

This section is short — it's mostly about cataloging the visible tech stack. Anything notable goes in the **strategic insights** section.

## Section 5 — Social Media Footprint

A platform-by-platform table:
| Platform | Handle | Followers | Notes |

Caveat any blocked counts ("Pinterest count requires live Chrome scrape; firecrawl blocked").

End with a "Strategic read" — usually one of:
- "Social is the weak leg" (small brand with great product, no distribution)
- "Social is the moat" (engaged community at scale)
- "Social is mid-tier and underleveraged on platform X" (most common)

## Section 6 — Marketplace Footprint

If the entity has marketplace presence (Amazon, G2, Capterra, App Store, Clutch), this section is **the most actionable** of the dossier for any consulting engagement. Include:

- Storefront URL + brand registry status
- Hero SKU/ASIN with real review counts and ratings
- Pricing snapshot
- A read on whether the marketplace presence is coherent with the new brand voice

## Section 7 — Customer Sentiment Analysis

Three subsections.

### 7.1 Positive signals
4–6 themes with frequency estimates. Quote real customer language where possible.

### 7.2 Negative signals
Same format. Don't dilute — the negative signals are where the consulting opportunities live.

### 7.3 Sentiment opportunity
One paragraph interpreting the data. "Customers love X, struggle with Y → here's the actionable hook."

## Section 8 — Competitive Landscape

A comparison table:
| Brand | Estimated rev | Positioning | Channel strategy | Vulnerability |

Then a one-paragraph "Key strategic insight" that names the **strategic wedge** — usually a competitor's weakness or vacuum that the subject entity can credibly fill.

## Section 9 — Authority Asset (named flexibly per entity)

For health/wellness brands: "Medical / Clinical Authority"
For SaaS: "Technical / Engineering Authority"
For B2B services: "Industry / Experience Authority"
For DTC fashion: "Designer / Creative Authority"
For investment-adjacent: "Track Record / Returns Authority"

Whoever the named, credentialed humans behind the brand are, this is their section. Surface them prominently. The bar: by the end of this section, the reader should believe (or disbelieve) that the entity has a defensible authority moat.

## Section 10 — AI / Tech Posture

The under-rated section. Cover:
- E-commerce / business platform stack
- Loyalty + reviews + CS stack
- Email / analytics / A-B testing stack
- AI signals: agents.md, llms.txt, UCP, MCP endpoints
- Custom theme/site work visible in the source
- Anything unusual or signals-of-sophistication

The presence of agents.md / UCP / MCP is a major finding that changes the pitch entirely — the entity has already opted into the agentic future.

## Section 11 — Strategic Insights & Opportunity Vectors

**This is the most important section.** It's why the dossier exists. Surface 4–6 numbered opportunity vectors:

```
### Vector N — {Short title}
**Problem:** {one sentence}
**Deliverable:** {one to two sentences describing the deliverable that would address it}
**Why this is leveraged:** {one sentence on why it's high-value vs. cost}
```

Lead with the vectors that have the highest leverage / lowest cost. End with the bonus vectors (low-priority but worth flagging).

## Section 12 — Open Intel Gaps

A bulleted list of things you couldn't close in this run. Live socials count, exact revenue, customer-service vendor identity, etc. These are the user's manual-followup roadmap.

## Section 13 — Source-of-Truth Companion Files

A short list pointing to:
- The emitted `{slug}-brand` skill (location in the vault)
- Optionally: planned downstream deliverables that would be derived from this dossier

End with a single em-dash signature line: `— End of dossier —`

## Anti-patterns to avoid

- **Source dump.** The body is synthesis. Links live in frontmatter.
- **Fictional precision.** "Revenue is $4.7M" — if you sourced it, name the source; if you estimated, say "self-reported, RocketReach $1M floor."
- **Boosterism.** Don't sell the entity to the user. Be honest about gaps.
- **Hiding the wedge.** Section 8's strategic insight and Section 11's vector list are the load-bearing assets of the dossier. Don't bury them.
- **Generic competitor section.** Don't list 12 competitors. Name 4–6, position them precisely, and identify the vulnerabilities.
