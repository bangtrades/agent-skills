---
name: solugenix-brand
description: Solugenix brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web apps, charts, or any visual deliverable for Solugenix, Aixcelrate, Genix/GENIX Accelerate, Nova, AskGenix, Vista, DocuGenix, AmplifAI, Proposal Agent, or any WaiveLabs × Solugenix partnership material. Also trigger when the user mentions Solugenix branding, the royal-blue-and-navy palette (#1E4FB5 / #0E2658), Maven Pro or Magistral typography, the "certainty and process maturity" voice, or asks for a document "in the Solugenix style." Trigger even when the user just says "make this on-brand for Solugenix," "apply the Solugenix look," "use their palette," or names a Solugenix capability, vertical, or accelerator. This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output.
---

# Solugenix Brand Skill

You are creating a deliverable for **Solugenix** — a 57-year-old, privately held (~$105–116M revenue, ~1,100 staff) IT services firm in Brea, CA, the self-described "first independent technology services provider" (1969), now betting on the **Aixcelrate** AI-accelerator suite, serving six regulated verticals with US/India/Dominican Republic "right-shoring." Every deliverable must reflect their **assured**, **operations-literate**, **anti-hype** identity.

> **WaiveLabs context:** Solugenix is a prospective WaiveLabs partner (WaiveLabs = agentic AI consulting arm extending their offerings). Deliverables are often co-branded pitches — keep Solugenix's visual system dominant when the audience is Solugenix; see `references/positioning-and-claims.md` for partnership framing rules.

## When to use this skill

ANY Solugenix-related visual or written deliverable: partnership pitch decks, one-pagers, brand-architecture audits, co-branded content, proposals, dashboards, demo web apps, email sequences, LinkedIn content drafts.

Format pairings: `.pptx` → pptx skill; `.docx` → docx skill; `.xlsx` → xlsx skill; HTML → frontend-design; PDF → pdf skill.

## Required reading before producing any deliverable

1. `references/visual-tokens.md` — colors, fonts, spacing, components
2. `references/voice-and-tone.md` — verbal system + the axiom-pair voice
3. `references/product-architecture.md` — service lines, Aixcelrate catalog, verticals
4. `references/copy-archetypes.md` — headline/CTA formulas from observed copy
5. `references/positioning-and-claims.md` — claim discipline + partnership framing

Drop-in assets: `assets/solugenix-tokens.css`, `assets/solugenix-tokens.json`.

## Core brand identity in one paragraph

Solugenix sells *certainty* to regulated enterprises: 57 years of process maturity, stable named teams, and "structure before scale." Its heritage (McDonald's first remote help desk, GPS routing databases, Cellular-ONE billing, Ibbotson 401(k) algorithms) is the proof; its new Aixcelrate accelerators extend that promise to AI — "an AI solution you can trust," delivered "in weeks, not months." Deliverables should feel like they came from a confident incumbent: calm royal blue on white, short declarative axioms, evidence over adjectives, risk-awareness without fear-mongering.

## Non-negotiable rules

1. **Never hype.** No "revolutionary," "game-changing," "magic." Their voice asserts calm, settled truths ("Technology doesn't create stability. It reveals it.").
2. **Type:** Magistral Medium for headings (substitute: Maven Pro Bold, then Arial Bold); Maven Pro for body (substitute: Verdana, then system sans). Never serif.
3. **Color hierarchy:** #1E4FB5 for CTAs/accents only (~10% surface); #0E2658 for text/headers; white backgrounds dominate. #3F85F7 sparingly for secondary highlights/charts.
4. **Backgrounds pure white** (#FFFFFF) or deep navy (#0E2658) for hero/cover sections with white logo. No gradients-heavy AI aesthetic, no neon.
5. **Naming discipline:** the platform is **Aixcelrate**; the accelerator suite may be called **Aixcelrate Accelerators**. Avoid the Genix/GENIX collision in new material unless quoting them. Product names: Nova, AskGenix, Vista, DocuGenix, AmplifAI, Proposal Agent.
6. **Heritage claims must be exact:** "first independent technology services provider" (1969); McDonald's = "one of the first remote help desks." Don't inflate ("invented the help desk" ❌).
7. **People:** CEO is **Shashi Jasthi** (President & CEO since 2004); AI lead is **Maruth Mulakala** (Head of Enterprise AI Practice). Use correct titles.
8. **Co-branded WaiveLabs material:** Solugenix = distribution/trust/verticals; WaiveLabs = agentic engineering depth. Never position WaiveLabs as subordinate ghost-labor; "partnership," not "vendor."

## Deliverable workflow

1. Determine format → load matching format skill.
2. Load the five reference files.
3. Draft with a copy archetype; apply tokens (CSS vars for web, hex/font names for office).
4. Self-check against the rules; check naming discipline (rule 5) explicitly.
5. Save to the user's project folder (WaiveLabs work: `~/Projects/agency` or the Cortana WaiveLabs project as directed).

## Source

Extracted 2026-06-09 from solugenix.com via Firecrawl branding analysis + full brand-recon run. Dossier: `research/brand-recon/solugenix/dossier.md`.
