---
name: copperjoint-brand
description: CopperJoint brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web apps, charts, or any visual deliverable for CopperJoint, Core210, the Pink Sock Collection, Dr. Strasser content, or any Everyday/Performance/Wellness-line work. Also trigger when the user mentions CopperJoint branding, the copper-and-navy palette, Montserrat/Epilogue typography, clinical-but-warm voice, or asks for a document "in the CopperJoint style." Trigger even when the user just says "make this on-brand," "apply the CopperJoint look," "use our palette," or names a CopperJoint product or sub-brand. This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output.
---

# CopperJoint Brand Skill

You are creating a deliverable for **CopperJoint** — a US compression-wear brand reinvented under new family ownership (Sept 2025), operating from Nashville, TN, with Dr. Nicholas Strasser, MD as Chief Medical Advisor. Every deliverable you create must reflect their **clinical-but-warm**, **owner-operator**, **trust-built** identity.

## When to use this skill

Use this skill for ANY CopperJoint-related visual or written deliverable: pitch decks, brand documents, product pages, social posts, web apps, dashboards, packaging mockups, Amazon A+ copy, email sequences, blog drafts, internal reports, investor decks, consulting pitches.

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
3. `references/product-architecture.md` — three product lines, positioning, sub-brands
4. `references/copy-archetypes.md` — reusable copy templates (headlines, CTAs, taglines)
5. `references/positioning-and-claims.md` — what we can/cannot say (FTC-aware claim discipline)

Drop-in technical assets live in `assets/`:
- `assets/copperjoint-tokens.css` — CSS variables ready to import into any web deliverable
- `assets/copperjoint-tokens.json` — same tokens as JSON for build pipelines

## Core brand identity in one paragraph

CopperJoint makes compression wear that is **clinically credible without being intimidating** and **everyday-wearable without being generic**. The voice is warm, professional, and hedged on claims (we say "shown to support" not "cures"). The visual system is **deep navy + copper + warm gold on warm off-white**, with Montserrat typography. We compete on **trust and orthopedic insight** in a category where the giants (Tommie Copper) have been punished by the FTC for overclaiming. Our differentiator is Dr. Strasser, real product science, and the family behind the brand.

## Non-negotiable rules

1. **Never make unhedged medical claims.** Compression "helps support," "is shown to," "may reduce" — never "cures," "fixes," "guarantees medical outcomes." (Post-FTC discipline.)
2. **Always use Montserrat as primary type.** Epilogue as the clinical-callout secondary. Never substitute serifs unless explicitly told.
3. **Navy `#1A2332` is the dominant brand color, copper `#B87333` is the accent.** Do NOT lead with copper as the primary brand color — that mistake makes us look like Copper Fit / Tommie Copper.
4. **Background is warm off-white `#F2F2F2`**, never pure white. Pure white reads sterile-medical.
5. **The Amazon-storefront voice is LEGACY and must not be carried into new deliverables.** Always use the new site voice (clinical-but-warm, hedged claims, "Built on trust. Designed for what's next.").
6. **Faith-coded sub-brand (Core210 = Ephesians 2:10) is real but never preachy in copy.** Reference the meaning if relevant; never proselytize.
7. **Dr. Strasser is a credentialed person, not a marketing prop.** When quoting him or attributing content to him, use his real credentials: "Dr. Nicholas Strasser, MD — Board-Certified Orthopedic Surgeon, Fellowship-Trained Foot & Ankle, Vanderbilt-Affiliated."
8. **Three product lines have distinct voices.** Everyday Line = warm/comfortable. Performance/Core210 = capable/disciplined. Wellness Line = empathetic/medical-credible. Don't blend them.

## Deliverable workflow

1. Determine the format (deck, doc, web, etc.) and load the matching format skill alongside this brand skill.
2. Load all five reference files above.
3. Draft using the appropriate copy archetype from `references/copy-archetypes.md`.
4. Apply visual tokens via the asset files (CSS variables for web, exact hex/font names for office/pdf).
5. Self-check against the rules: hedged claims? right primary color hierarchy? right voice for the product line? Strasser correctly credentialed?
6. Save the deliverable to the appropriate project folder under `/Users/nolan/Projects/CopperJoint/CopperJoint/`.

## Where deliverables live

- `01-intel/` — research, dossiers, market intel
- `02-brand/` — this skill + brand assets
- `03-pitch/` — consulting pitch deck, executive deliverables
- `04-demos/` — demo web apps and prototypes
- `05-content/` — blog drafts, social copy, email sequences
- `06-amazon/` — Amazon A+ rewrites, listing copy, brand-store mockups
