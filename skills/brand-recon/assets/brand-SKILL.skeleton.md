---
name: {slug}-brand
description: {ENTITY_NAME} brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web apps, charts, or any visual deliverable for {ENTITY_NAME}{ and named sub-brands or product lines}. Also trigger when the user mentions {ENTITY_NAME} branding, the {signature-color-1}-and-{signature-color-2} palette, {signature-font} typography, {voice-descriptor} voice, or asks for a document "in the {ENTITY_NAME} style." Trigger even when the user just says "make this on-brand," "apply the {ENTITY_NAME} look," "use our palette," or names a {ENTITY_NAME} product or sub-brand. This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output.
---

# {ENTITY_NAME} Brand Skill

You are creating a deliverable for **{ENTITY_NAME}** — {one-sentence company descriptor: stage, category, distinguishing characteristic, location, key affiliate}. Every deliverable you create must reflect their **{primary-voice-descriptor}**, **{secondary-voice-descriptor}**, **{tertiary-voice-descriptor}** identity.

## When to use this skill

Use this skill for ANY {ENTITY_NAME}-related visual or written deliverable: pitch decks, brand documents, product pages, social posts, web apps, dashboards, packaging mockups, marketplace copy, email sequences, blog drafts, internal reports, investor decks, consulting pitches.

This skill is the BRAND LAYER. It works alongside format-specific skills:
- For a `.pptx` deck → also read the `pptx` skill
- For a `.docx` document → also read the `docx` skill
- For an `.xlsx` workbook → also read the `xlsx` skill
- For an HTML web app or dashboard → also read the `frontend-design` skill
- For a PDF → also read the `pdf` skill

## Required reading before producing any deliverable

Always load these reference files BEFORE generating:

1. `references/visual-tokens.md` — colors, fonts, spacing, components
2. `references/voice-and-tone.md` — verbal system + voice rules
3. `references/product-architecture.md` — product lines, positioning, sub-brands
4. `references/copy-archetypes.md` — reusable copy templates (headlines, CTAs, taglines)
5. `references/positioning-and-claims.md` — what we can/cannot say (claim discipline)

Drop-in technical assets live in `assets/`:
- `assets/{slug}-tokens.css` — CSS variables ready to import into any web deliverable
- `assets/{slug}-tokens.json` — same tokens as JSON for build pipelines

## Core brand identity in one paragraph

{ONE PARAGRAPH synthesizing the brand. What they make / sell / do, the credible differentiator, the competitive context, and the strategic wedge that any deliverable should reinforce. This is the north star a deliverable must align with.}

## Non-negotiable rules

1. **{rule 1 — usually the strictest claim-discipline rule for the category}**
2. **{rule 2 — primary font and any substitution constraint}**
3. **{rule 3 — color hierarchy: primary vs secondary vs accent surface area}**
4. **{rule 4 — background discipline (warm off-white vs pure white, etc.)}**
5. **{rule 5 — any legacy/marketplace voice that must NOT be carried into new deliverables}**
6. **{rule 6 — any cultural / faith / political / partner constraints unique to this entity}**
7. **{rule 7 — credentialing rules for any named authority figure}**
8. **{rule 8 — voice differentiation across product lines / sub-brands}**

## Deliverable workflow

1. Determine the format (deck, doc, web, etc.) and load the matching format skill alongside this brand skill.
2. Load all five reference files above.
3. Draft using the appropriate copy archetype from `references/copy-archetypes.md`.
4. Apply visual tokens via the asset files (CSS variables for web, exact hex/font names for office/pdf).
5. Self-check against the rules above.
6. Save the deliverable to the user's project folder.

## Where deliverables live

{If the entity has an established folder structure or vault location for deliverables, name it. Otherwise, default to the user's current project workspace.}
