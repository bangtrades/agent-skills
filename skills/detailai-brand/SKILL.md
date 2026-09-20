---
name: detailai-brand
description: DetailAI brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web apps, app UI, dashboards, charts, SMS/email copy, or any visual or written deliverable for DetailAI, The Agent, or the Studio Site. Also trigger when the user mentions DetailAI branding, the black-cream-and-champagne-gold palette (#0A0A0A / #F4EDE2 / #C9A36A), Cormorant Garamond + Inter typography, the "concours grade" or atelier voice, or asks for a deliverable "in the DetailAI style." Trigger even when the user just says "make this on-brand," "apply the DetailAI look," "use our palette," mentions the detailai.ai site, Meridian Detail Studio demo persona, or names DetailAI product surfaces (The Agent, Studio Site, founding shops program). This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design, epic-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output.
---

# DetailAI Brand Skill

You are creating a deliverable for **DetailAI** — a prototype-stage (2026, Nashville TN, WaiveLabs-built) AI lead-response and instant-quote platform for premium auto-detailing studios: ceramic coating, paint correction, PPF shops with $2,000+ tickets. Every deliverable must reflect their **atelier-premium**, **terse-confident**, **craft-reverent** identity.

## When to use this skill

Use for ANY DetailAI-related visual or written deliverable: app UI, pitch decks, one-pagers, product pages, SMS conversation flows, onboarding docs, email sequences, dashboards, investor material, founding-shop outreach.

This skill is the BRAND LAYER. It works alongside format skills:
- `.pptx` deck → also read `pptx`
- `.docx` document → also read `docx`
- `.xlsx` workbook → also read `xlsx`
- HTML/web/app UI → also read `frontend-design` (or `epic-design` for marketing pages)
- PDF → also read `pdf`

## Required reading before producing any deliverable

1. `references/visual-tokens.md` — colors, fonts, spacing, components
2. `references/voice-and-tone.md` — verbal system + voice rules
3. `references/product-architecture.md` — SKUs, pricing, roadmap framing
4. `references/copy-archetypes.md` — reusable headline/CTA/section patterns
5. `references/positioning-and-claims.md` — claim discipline, competitive framing

Drop-in assets: `assets/detailai-tokens.css`, `assets/detailai-tokens.json`.

## Core brand identity in one paragraph

DetailAI sells recovered revenue to craftsmen. The product answers every missed call and text in seconds, quotes from the shop's own menu at the shop's own prices, and books the job — so the brand behaves like the software equivalent of a concours-prepped finish: black/cream/champagne-gold, display serif over quiet sans, short declarative sentences, quantified speed, zero SaaS clichés. It is priced 5× the category cluster ($499 vs $70–110), so every deliverable must sell ROI against the $2,000 job, never features against Urable. Exclusivity is part of the mechanics: private demos, founding shops, white-glove onboarding.

## Non-negotiable rules

1. **ROI framing, never feature-parity framing.** Price is defended by "one extra $2,000 job pays for four months" — do not build comparison grids against $70/mo tools.
2. **Cormorant Garamond for display, Inter for everything else.** Fallbacks: Playfair Display → Georgia (serif); system stack (sans). Never a geometric-sans display headline.
3. **Gold `#C9A36A` is scarce.** CTAs, diamond bullets (◆), key numerals only. Cream `#F4EDE2` carries text; near-black `#0A0A0A` carries the room. If gold exceeds ~10% of the surface, it's wrong.
4. **Dark by default.** Deliverables are black-canvas. If a document must be light (e.g., print contract), invert to cream paper `#F4EDE2` with near-black text and keep gold scarce.
5. **Pill buttons, sharp blocks.** CTAs are fully rounded (9999px); containers are 0-radius; inputs 8px. No drop shadows.
6. **Speed claims stay quantified and honest.** "Seconds," "90 seconds," "within a minute" — and quotes are always "confirmed by the shop." Never claim the agent invents prices: "Nothing is estimated or made up."
7. **Exclusivity register.** "Private demo," "founding shops," "white-glove." Never "free trial," "sign up now," "limited time offer," or discount language.
8. **Anti-positioning is load-bearing.** Built for studios, "not for volume car washes." Never broaden to car washes, quick lubes, or generic field service.
9. **Demo persona (owner decision, September 18, 2026): Apex Studio.** Use it for the current owner demo and new demo material. Meridian Detail Studio is a historical concept; preserve old fixtures and screenshots rather than renaming history. The demo persona is not a legal carrier-registration identity.

## Deliverable workflow

1. Determine format; load the matching format skill alongside this one.
2. Load the five reference files.
3. Draft using the closest copy archetype.
4. Apply tokens (CSS vars for web; exact hex/font names for office/pdf).
5. Self-check against the rules above — especially gold scarcity and ROI framing.
6. Save to the DetailAI project folder (`~/Projects/DetailAI/`).

## Where deliverables live

Project root: `~/Projects/DetailAI/` (docs → `docs/`, research → `research/`). Vault mirror: `cortana-vault/research/brand-recon/detailai/`.


## Evidence scope — September 20 reconciliation

Public positioning and August research describe intended product promises. They are not fresh company, pricing, deployment or acceptance evidence. See the platform current-state document for actual limits, including paused photo classification and incomplete custom vehicle-class interpretation. Do not claim a quoted latency, automatic booking capability or persona enforcement as verified without workflow evidence. Owner-confirmed Apex branding supersedes older Meridian-only instructions.
