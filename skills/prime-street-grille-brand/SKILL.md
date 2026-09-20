---
name: prime-street-grille-brand
description: The Prime Street Grille brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web apps, dashboards, demo UIs, charts, menus, social posts, or any visual or written deliverable for The Prime Street Grille (Prime Street, PSG, theprimestreetgrille.com — the White Plains, MD steakhouse & seafood restaurant). Also trigger when the user mentions Prime Street Grille branding, the plum-and-aubergine palette (#4D236C / #380647), Montserrat/Open Sans typography, the script "Prime Street" oval badge, the crab cake / hand-cut steak positioning, "American Classics, Elevated," or asks for a document "in the Prime Street style." Trigger even when the user just says "make this on-brand," "apply the Prime Street look," "use their palette," or names a PSG dish, the Primestreet project, or the agentic front-of-house engagement. This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output.
---

# The Prime Street Grille Brand Skill

You are creating a deliverable for **The Prime Street Grille** — a ~14-year-old, veteran- and locally-owned fine-dining steakhouse & seafood restaurant in White Plains, MD (Charles County / Waldorf corridor), owned by Nick White and Tony Graham, famous locally for no-filler jumbo-lump crab cakes and in-house hand-cut steaks, and operating at the ceiling of its capacity. Every deliverable you create must reflect their **warm-Southern-hospitality**, **quality-proud**, **community-rooted** identity.

## When to use this skill

Use this skill for ANY Prime Street Grille-related visual or written deliverable: pitch decks, proposals, demo web apps and dashboards (including WaiveLabs agentic front-of-house demos), site copy rewrites, menus, review responses, email/SMS flows, social posts, event one-pagers, gift-card promos, internal reports.

This skill is the BRAND LAYER. It works alongside format-specific skills:
- For a `.pptx` deck → also read the `pptx` skill
- For a `.docx` document → also read the `docx` skill
- For an `.xlsx` workbook → also read the `xlsx` skill
- For an HTML web app or dashboard → also read the `frontend-design` skill
- For a PDF → also read the `pdf` skill

If the deliverable is WaiveLabs-branded work *about* PSG (a pitch to them), pair with `brand-waive`: WaiveLabs frames, PSG content styled with PSG tokens inside the frame.

## Required reading before producing any deliverable

1. `references/visual-tokens.md` — colors, fonts, spacing, components
2. `references/voice-and-tone.md` — verbal system + the two-voices problem
3. `references/product-architecture.md` — menu structure, channels, pricing
4. `references/copy-archetypes.md` — reusable copy templates
5. `references/positioning-and-claims.md` — claim discipline + personas

Drop-in technical assets live in `assets/`:
- `assets/prime-street-grille-tokens.css` — CSS variables for any web deliverable
- `assets/prime-street-grille-tokens.json` — same tokens as JSON

## Core brand identity in one paragraph

The Prime Street Grille is Chesapeake luxury with Southern manners: an independent, veteran-owned dining room where local rockfish, blue-crab everything, and steaks cut in-house from premium beef are served at DC prices to Southern Marylanders celebrating something. The visual identity is a two-color system — deep plum and aubergine on white, ornate script "Prime Street" badge, dark appetite-forward food photography — that reads boutique rather than steakhouse-cliché. The voice is proud and warm, with a firm streak on policy (reservations rule the house). Deliverables should reinforce the wedge: this is the *only* upscale independent steak-and-seafood house in its corridor, drowning in demand it manages by hand — so every artifact should feel like the gracious hospitality voice, systematized, never the ALL-CAPS policy voice.

## Non-negotiable rules

1. **Claims discipline:** Never invent or amplify awards. "Award-winning" may be echoed only where PSG itself uses it, and never given a named source unless the owners substantiate one. Never state Michelin/press recognition that doesn't exist. Sourcing claims stay verbatim-true: "wild-caught," "local rockfish," "hand-cut in house," "top 2% of all beef" (their claim — attribute to them).
2. **Typography:** Montserrat for headings/UI, Open Sans for body. Never typeset the script logo style as text — the script exists only inside the logo badge. No serif "fine dining" cosplay fonts.
3. **Color hierarchy:** Plum `#4D236C` is the action/primary color; aubergine `#380647` is ink (text, dark surfaces). White dominates; light lavender-gray `#F5F3F7` for section bands. Gold/amber tones enter only through food photography, never as UI chrome. **Never use `#2EA3F2`** (Divi system default found in their CSS — not brand).
4. **Photography:** dark, close, appetite-forward, real dishes (crab cakes golden, steak marbled). No stock-photo restaurant interiors, no generic "chef hands" stock. The plum oval badge watermark is their pattern for social imagery.
5. **Voice:** write in the hospitality voice ("Let us do the cooking for you") — never the defensive ALL-CAPS policy voice. Policies are stated plainly, once, in sentence case, framed as fairness ("so every guest gets the evening they reserved").
6. **Identity facts:** veteran- and locally-owned, owners Nick White & Tony Graham, White Plains MD (NOT "St. Charles" — that's legacy residue), "Grille" with the -e everywhere. Est. 2012-or-earlier; say "for over a decade" rather than a precise year until the owners confirm one.
7. **Menu integrity:** prices and dish specs come from `references/product-architecture.md` (captured 2026-07-17) and must be re-verified before any public-facing use — restaurant prices move.
8. **Respect the scarcity:** never promise capacity that doesn't exist (private dining, parties >10, walk-in welcomes). Deliverables sell *access done well*, not *more tables*.

## Deliverable workflow

1. Determine the format and load the matching format skill alongside this brand skill.
2. Load all five reference files above.
3. Draft using the appropriate copy archetype from `references/copy-archetypes.md`.
4. Apply visual tokens via the asset files (CSS variables for web, exact hex/font names for office/pdf).
5. Self-check against the rules above — especially claims discipline and the two-voices rule.
6. Save the deliverable to the active project folder (`~/Projects/Primestreet` for the WaiveLabs engagement).

## Where deliverables live

WaiveLabs engagement artifacts → `~/Projects/Primestreet`. Research artifacts → `cortana-vault/research/brand-recon/prime-street-grille/`. Client-facing sends gate through bang.
