---
name: sense-neuro-brand
description: Sense Neuro Diagnostics brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web pages, charts, investor one-pagers, clinical evidence briefs, or any visual deliverable for Sense Neuro Diagnostics, Sense Diagnostics Inc., NeuroHawk, or NeuSTAT. Also trigger when the user mentions Sense Neuro branding, the "Time is brain" tagline, the medical-blue (#008ED1 / #004D71) + orange (#F39119) palette, Open Sans / Nunito Sans typography, the nine-antenna RF brain scanner, or asks for a document "in the Sense Neuro style." Trigger even when the user just says "make this on-brand," "apply the Sense look," "use our palette," or names a Sense product (NeuroHawk Military, NeuroHawk ED/EMS, NeuSTAT). This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output.
---

# Sense Neuro Diagnostics — Brand Skill

Sense Neuro Diagnostics (legal: **Sense Diagnostics, Inc.**) is a clinical-stage neurodiagnostics company building non-invasive **radio-frequency (RF) brain scanners** that detect and triage stroke subtype and TBI — and continuously monitor brain bleeds — at the point of care. Tagline: **"Time is brain."** This skill keeps every Sense deliverable visually and verbally on-brand.

> Emitted by brand-recon on 2026-06-18. Companion dossier: `../dossier.md`.

## When to use this skill
Any Sense Neuro / NeuroHawk / NeuSTAT deliverable: investor decks & one-pagers, clinical/evidence briefs, the website, partner/DoD materials, press releases, social posts, charts. Pair with the format skill (pptx/docx/pdf/xlsx/frontend-design) for mechanics.

## The 30-second brand
- **Essence:** credible, mission-driven medtech. "Time is brain" — speed to the *correct* treatment saves brain function.
- **Audience priority:** (1) investors, (2) clinicians/KOLs & hospital systems, (3) DoD/defense-medicine buyers. Rarely patients/consumers.
- **Look:** clean clinical blue-and-white with a single warm orange CTA. Open Sans headings, Nunito Sans body. Fully-rounded (pill) orange buttons, UPPERCASE.
- **Tone:** clinical, urgent, evidence-led, regulator-aware. Never hype. Always carry the FDA-stage disclaimer.

## Core tokens (full set in `references/visual-tokens.md` + `assets/`)
- **Primary blue** `#008ED1` · **Deep blue** `#004D71` · **Darkest navy** `#002A3A`
- **CTA orange** `#F39119` (buttons only — used sparingly)
- **Heading text** `#222222` · **Body** `#666666` · **BG** `#FFFFFF` / `#F9F9F9` · **Hairline** `#EEEEEE`
- **Headings:** Open Sans (500). **Body:** Nunito Sans (400). **Buttons:** Open Sans 700, UPPERCASE, letter-spacing 1px, pill radius.

## Non-negotiables (claims & legal)
This is a **pre-clearance medical device.** Every external deliverable MUST:
1. Refer to NeuroHawk™ / NeuSTAT™ as **investigational** — "not yet cleared or approved by the FDA; not available for sale or clinical use in the United States."
2. Frame trial data as **feasibility / early-stage**, not proof of efficacy ("results have not been reviewed by the FDA and do not imply clearance or approval").
3. Never state or imply diagnostic accuracy as established fact. Use "designed to," "intended to," "in development."
4. Use ™ on first mention of NeuroHawk and NeuSTAT.
See `references/positioning-and-claims.md` before writing any claim.

## Product taxonomy (say it consistently — see `references/product-architecture.md`)
**One RF platform, three settings:** NeuroHawk™ (Military/Field) · NeuroHawk™ (ED/EMS) · NeuSTAT™ (Continuous Hospital Monitoring). Reusable control unit + single-use disposable headset (razor/blade).

## How to load references
- Deck or web page → `visual-tokens.md` + `copy-archetypes.md`
- Press release / investor narrative → `voice-and-tone.md` + `positioning-and-claims.md`
- Product/spec page or evidence brief → `product-architecture.md` + `positioning-and-claims.md`
- Always skim `positioning-and-claims.md` for any external-facing piece.

## Validation checklist before shipping
- [ ] Palette: clinical blue dominant, orange only on primary CTAs
- [ ] Fonts: Open Sans headings, Nunito Sans body
- [ ] "Time is brain" used where a hero line fits
- [ ] ™ on NeuroHawk / NeuSTAT; product taxonomy consistent
- [ ] FDA investigational + feasibility-data disclaimers present
- [ ] No timeline contradictions (current FDA status = **De Novo submitted Sept 2025, under review**)
- [ ] Tone clinical/urgent, not promotional
