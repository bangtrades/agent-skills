---
name: sd-wheel-brand
description: SD Wheel brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web apps, dashboards, charts, marketing copy, social posts, or any visual deliverable for SD Wheel, the SD Wheels growth desk, sdwheel.com, SD Wheel Wholesale, or Enthusiast Enterprises work touching the SD Wheel storefront. Also trigger when the user mentions SD Wheel branding, SD Orange (#FFA500), the orange-and-charcoal palette, Montserrat typography, "Ready To Roll," wheel & tire packages, fitment guarantee, ARKON / Anthem / Anovia house brands, or asks for a document "in the SD Wheel style." Trigger even when the user just says "make this on-brand," "apply the SD look," "use their palette," or names an SD Wheel product line or tool (fitmentWiz, offset guide, Today's Deals). This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design, epic-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant references/ file before generating output.
---

# SD Wheel Brand Skill

Brand system for **SD Wheel** (sdwheel.com) — aftermarket wheel-and-tire e-commerce retailer, founded 2003 by Steve Hamilton, flagship brand of Enthusiast Enterprises Inc. (Wrightstown, WI). Extracted 2026-07-10 by brand-recon. Companion dossier: `../dossier.md`.

## The brand in one paragraph

SD Wheel sells confidence to fitment-anxious truck and car enthusiasts: mounted, balanced, guaranteed-to-fit wheel & tire packages, shipped free, financeable at 0% APR. The voice is an enthusiast buddy who happens to be an expert — loud, warm, superlative-leaning (rein that in; see positioning-and-claims). The look is safety-orange on charcoal/white, all-Montserrat, square-edged, big type, product photography doing the aesthetic heavy lifting.

## Core tokens (fast reference)

| Token | Value |
|---|---|
| SD Orange (primary/accent/CTA) | `#FFA500` |
| Charcoal (text) | `#2F2F2F` |
| White (background) | `#FFFFFF` |
| Neutral gray (secondary buttons) | `#909090` |
| Black (on-orange text, dark sections) | `#000000` |
| Font — everything | Montserrat (700/800 headings, 400/500 body) |
| Buttons | Square corners (0 radius), orange bg, black text, bold uppercase-friendly |
| Inputs | 4px radius, subtle inset shadow |
| Type scale | H1 ~64px, H2 ~33px, body ~22px desktop (scale down proportionally for docs) |
| Logo | `https://images.sdwheel.com/logo/white-horizontal.svg` (use on dark/orange); legacy `https://images.sdwheel.com/old/sd-logo.png` (light bg) |

## Voice in one line

"Enthusiast expert on the phone with you": confident, warm, concrete about the deal (free mount/balance/ship, fitment guaranteed, 0% financing), aspirational about the build ("dream build," "Ready To Roll"), never corporate, never hedgy — but claims must be substantiated (see references/positioning-and-claims.md).

## References (load per task)

- `references/visual-tokens.md` — full palette, type, spacing, component specs; load for decks, web, dashboards, PDFs.
- `references/voice-and-tone.md` — voice rules + real example phrases; load for any copy.
- `references/product-architecture.md` — catalog structure, house brands, tools, sibling brands; load for product pages, merchandising, strategy docs.
- `references/copy-archetypes.md` — hero, CTA, deal, social, email patterns lifted from live copy; load for marketing deliverables.
- `references/positioning-and-claims.md` — what may/may not be claimed, competitive frame, claim substitutions; load for anything customer-facing or pitch-facing.

## Assets

- `assets/sd-wheel-tokens.css` — CSS custom properties.
- `assets/sd-wheel-tokens.json` — machine-readable tokens for dashboards/apps.

## Hard rules

1. Orange is an accent and CTA color, not a page-flood color — white/charcoal carry the layout.
2. Black text on orange buttons (not white).
3. Montserrat only. No serif, no second family.
4. Square buttons and cards; do not round corners beyond 4px (inputs only).
5. Replace inherited superlatives ("#1 in the world," "fastest shipping in the world") with substantiated claims — see positioning-and-claims.md.
6. When building for the growth-desk platform, this brand layer styles SD-facing surfaces; WaiveLabs-internal surfaces use brand-waive.
