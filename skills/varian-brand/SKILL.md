---
name: varian-brand
description: "Siemens Healthineers / Varian brand guide for generating consistent, on-brand documents and presentations. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), PDFs, HTML reports, or any visual deliverable for Varian, Siemens Healthineers, or VAIL (Varian Augmented Intelligence Layer). Also trigger when the user mentions Varian branding, Siemens Healthineers styling, petrol color, or asks for a document 'in the same style as' previous Varian deliverables. This skill should be used alongside format-specific skills (docx, pptx, pdf) — it provides the brand layer, they provide the file format mechanics."
---

# Siemens Healthineers / Varian Brand Guide

This skill defines the complete visual identity system for Varian (a Siemens Healthineers company) documents and presentations. Every color, font size, spacing value, and component pattern has been field-tested across 25+ page Word documents and 13-slide executive decks. Follow this guide to produce documents that are visually indistinguishable from the established suite.

## When to read reference files

This SKILL.md gives you the brand system and decision framework. For implementation, read these references:

- **`references/docx-patterns.md`** — Read when creating Word documents (.docx). Contains the complete `docx` library code patterns: Document styles, heading definitions, table builders, callout boxes, cover page layout, header/footer templates, and budget table builders. Copy these patterns directly.
- **`references/pptx-patterns.md`** — Read when creating PowerPoint decks (.pptx). Contains the complete `pptxgenjs` code patterns: dark slide backgrounds, card components, stat cards, icon rendering, slide layouts, and the accent-bar system.

Read the relevant reference file before writing any code. The patterns are tested and exact — don't improvise hex values or spacing from memory.

---

## Brand Color Palette

The palette has two modes: **light backgrounds** (Word documents, PDFs, printable reports) and **dark backgrounds** (presentation slides, dashboards).

### Primary Brand Colors

| Token | Hex | Role |
|-------|-----|------|
| PETROL | `#009999` | Primary brand accent. Headers, links, table header backgrounds, slide accent bars, icon fills. The signature Siemens Healthineers teal. |
| DARK_PETROL | `#007A7A` | Deeper variant for document headings (H1, H2), table headers on light backgrounds, and high-contrast text on white. |
| ORANGE | `#EC6602` | Secondary accent. H3 headings, warning/urgency callouts, "Full Send" tier, call-to-action elements. Official Siemens Healthineers orange. |

### Extended Palette — Light Mode (Documents)

| Token | Hex | Role |
|-------|-----|------|
| TEXT_DARK | `#2C2C2C` | Primary body text. All paragraph copy, bullet items, table cell text. |
| TEXT_MED | `#555555` | Secondary text. Captions, footnotes, italic recommendation blocks, metadata, table notes column. |
| LIGHT_GRAY | `#F5F5F5` | Alternating table row fill (even rows). Provides subtle zebra striping without distraction. |
| MID_GRAY | `#E8E8E8` | Table total rows, summary row backgrounds. Heavier than LIGHT_GRAY to anchor the eye. |
| WHITE | `#FFFFFF` | Page background, text on colored header cells. |
| ACCENT_BLUE | `#2563EB` | Moderate tier accent in callout boxes. Used sparingly. |
| AMBER | `#F59E0B` | Engineering domain accent. Used for engineering-specific table headers and section markers. |

### Extended Palette — Dark Mode (Presentations)

| Token | Hex | Role |
|-------|-----|------|
| DARK | `#0A1628` | Slide background. Deep navy-black, never pure black. |
| DARK2 | `#0F1F3D` | Footer bar background, secondary dark surface. |
| DARK3 | `#162A50` | Tertiary dark for inset shapes (hub ovals, recessed panels). |
| CARD_BG | `#111D35` | Card/container background. Slightly lighter than DARK to create depth. |
| PETROL_LIGHT | `#00CCCC` | Bright teal for slide accent text, highlighted values, and hub labels. |
| ORANGE_LIGHT | `#FF8534` | Warm orange for action-oriented icons and urgency indicators. |
| GRAY | `#8A9BB5` | Slide body text, card descriptions, subtitle copy. The workhorse slide text color. |
| LIGHT | `#C5D3E8` | Brighter than GRAY. Subtitle text, secondary emphasized content. |
| GREEN | `#2DD4A8` | Positive indicators, growth stats, marketing domain accent. |
| PURPLE | `#A855F7` | Research/science domain accent, brain/DNA icons. |
| BLUE_BRIGHT | `#3B82F6` | Data/analytics domain accent, chart-related icons. |

### Callout Box Fills (Light Mode)

These soft pastel fills are used for summary/comparison callout cells in documents:

| Context | Fill Hex | Accent Text Color |
|---------|----------|-------------------|
| Lean tier | `#E8F5E9` (soft green) | `#2E7D32` (dark green) |
| Moderate tier | `#E3F2FD` (soft blue) | `#2563EB` (accent blue) |
| Full Send tier | `#FFF3E0` (soft orange) | `#EC6602` (orange) |

### Risk/Status Colors

| Meaning | Hex | Context |
|---------|-----|---------|
| High risk / Net-new expense | `#C62828` | Risk table likelihood column, status indicators |
| Reassigned / Positive | `#2E7D32` | Status column "Reassigned" markers |

---

## Typography

### Font Families

- **Documents (Word, PDF):** Arial exclusively. Every TextRun, every heading, every cell — Arial. No exceptions.
- **Presentations (PPTX):** Calibri exclusively. All slide text uses Calibri.

This split is intentional: Arial is the Siemens corporate document font; Calibri renders better on projected slides.

### Document Text Hierarchy (docx — sizes in half-points)

| Element | Font | Size (half-pts) | Size (pts) | Weight | Color | Spacing |
|---------|------|-----------------|------------|--------|-------|---------|
| H1 | Arial | 36 | 18pt | Bold | DARK_PETROL | before: 360, after: 200 |
| H2 | Arial | 28 | 14pt | Bold | DARK_PETROL | before: 280, after: 160 |
| H3 | Arial | 24 | 12pt | Bold | ORANGE | before: 200, after: 120 |
| Body paragraph | Arial | 22 | 11pt | Normal | TEXT_DARK | after: 200 |
| Bullet item | Arial | 22 | 11pt | Normal | TEXT_DARK | after: 100 |
| Rich bullet (lead term) | Arial | 22 | 11pt | Bold | TEXT_DARK | after: 100 |
| Rich bullet (description) | Arial | 22 | 11pt | Normal | TEXT_DARK | — |
| Table cell (standard) | Arial | 20 | 10pt | Normal | TEXT_DARK | after: 0 |
| Table cell (bold) | Arial | 20 | 10pt | Bold | TEXT_DARK | after: 0 |
| Table header cell | Arial | 20 | 10pt | Bold | WHITE (on colored bg) | after: 0 |
| Table notes column | Arial | 18 | 9pt | Normal | TEXT_MED | after: 0 |
| Recommendation/footnote | Arial | 20 | 10pt | Italic | TEXT_MED | after: 200 |
| Cover title ("VAIL") | Arial | 72 | 36pt | Bold | DARK_PETROL | — |
| Cover subtitle | Arial | 36 | 18pt | Normal | ORANGE | — |
| Cover tagline | Arial | 28 | 14pt | Bold | TEXT_DARK | — |
| Cover sub-tagline | Arial | 24 | 12pt | Normal | TEXT_MED | — |
| Cover metadata | Arial | 20 | 10pt | Normal | TEXT_MED | — |
| Cover org line | Arial | 20 | 10pt | Normal | TEXT_MED, charSpacing: 80 | — |
| Header (running) | Arial | 16 | 8pt | Bold | DARK_PETROL | — |
| Header right ("Confidential") | Arial | 16 | 8pt | Italic | TEXT_MED | — |
| Footer | Arial | 16 | 8pt | Normal | TEXT_MED | — |

### Presentation Text Hierarchy (pptx — sizes in points)

| Element | Font | Size | Weight | Color |
|---------|------|------|--------|-------|
| Slide title | Calibri | 28pt | Bold | WHITE |
| Slide subtitle | Calibri | 13pt | Normal | GRAY |
| Org line ("SIEMENS HEALTHINEERS \| VARIAN") | Calibri | 12pt | Normal | GRAY, charSpacing: 4 |
| Title slide main text | Calibri | 44pt | Bold | WHITE / PETROL_LIGHT |
| Title slide tagline | Calibri | 16pt | Normal | LIGHT |
| Card title | Calibri | 12–13pt | Bold | WHITE |
| Card description | Calibri | 9–10pt | Normal | GRAY |
| Card label/badge | Calibri | 10pt | Bold | (accent color) |
| Stat card value | Calibri | 30pt | Bold | (accent color) |
| Stat card label | Calibri | 10pt | Normal | GRAY |
| Footer bar text | Calibri | 10pt | Normal | GRAY |
| Timestamp/meta | Calibri | 11pt | Normal | GRAY |

---

## Document Layout (Word / docx)

### Page Setup

- **Page size:** US Letter (12240 × 15840 DXA = 8.5" × 11")
- **Margins:** 1 inch all sides (1440 DXA)
- **Content width:** 9360 DXA (6.5 inches)

### Cover Page Structure

The cover page is a separate section with no header/footer:

1. Top spacer (600 DXA)
2. Organization line: `"SIEMENS HEALTHINEERS  |  VARIAN"` — Arial 10pt, TEXT_MED, character spacing 80
3. Spacer (200 DXA)
4. Title: Large bold text (36pt) in DARK_PETROL, with PETROL bottom border (6pt line)
5. Subtitle: 18pt in ORANGE
6. Spacer (300 DXA)
7. Document type: 14pt bold TEXT_DARK
8. Phase/scope: 12pt TEXT_MED
9. Spacer (400 DXA)
10. Metadata block: Classification, Date, Version — 10pt TEXT_MED
11. Spacer (200 DXA)
12. Prepared-for line: 10pt italic TEXT_MED, MID_GRAY top border separator

### Running Header

- Left: Document title — Arial 8pt bold DARK_PETROL
- Right: "Confidential" — Arial 8pt italic TEXT_MED
- Bottom border: 2pt PETROL line with 4pt space
- Uses tab stops (left + RIGHT at MAX position)

### Running Footer

- Left: "Siemens Healthineers | Varian" — Arial 8pt TEXT_MED
- Right: "Page [N]" — Arial 8pt TEXT_MED
- Top border: 1pt MID_GRAY line with 4pt space
- Uses tab stops (left + RIGHT at MAX position)

---

## Component Patterns

### Tables

All tables span full content width (9360 DXA). Column widths must sum to exactly 9360.

**Header row:** Background fill of DARK_PETROL (default) or domain accent color (AMBER for engineering). White bold text.

**Data rows:** Alternating fill pattern — odd rows plain, even rows LIGHT_GRAY (`#F5F5F5`).

**Total/summary rows:** MID_GRAY fill (`#E8E8E8`), bold text.

**Cell margins:** top: 80, bottom: 80, left: 120, right: 120 (DXA).

**Borders:** 1pt CCCCCC on all sides.

**Budget table column widths** (the standard 5-column layout for cost tables):
- Category: 3200
- Lean: 1340
- Moderate: 1540
- Full Send: 1540
- Notes: 1740
- Sum: 9360

Budget values are right-aligned. Notes column uses smaller font (9pt / size 18) in TEXT_MED.

### Rich Bullets (Bold Lead Pattern)

Used extensively for agent descriptions, feature lists, and anywhere a term needs definition:

```
**Agent harness development:** Rapid edit-run-debug cycles on orchestration logic...
```

The lead term is bold, same font/size as the description. Both are 11pt Arial TEXT_DARK. The colon-space separates them. Each rich bullet has `spacing.after: 100`.

### Callout Boxes (Tier Summary)

Three cells in a single-row table, each 3120 DXA wide (9360 / 3). Each cell gets:
- Soft pastel fill (green/blue/orange per tier)
- Tier name: 14pt bold DARK_PETROL (or ORANGE for Full Send)
- Primary metric: 11pt bold in tier accent color
- Secondary metric: 9pt TEXT_MED
- Description: 9pt TEXT_MED
- Cell margins: 120 top/bottom, 160 left/right
- All text center-aligned

### Recommendation/Footnote Blocks

Italic paragraphs in 10pt TEXT_MED that serve as editorial notes, typically after a section:

```
VAIL PC members are not reassigned; they continue their primary roles...
```

These use `richPara` with two runs: bold italic label ("Recommendation: ") followed by regular italic body.

---

## Presentation Layout (PPTX)

### Slide Setup

- **Layout:** 16:9 (10" × 5.625")
- **Background:** DARK (`#0A1628`) — every slide
- **Author:** "Siemens Healthineers | Varian"

### Slide Anatomy

Every content slide follows this structure:

1. **Top accent bar:** Full-width rectangle, 0.04" tall at y=0, filled with section color (PETROL default, ORANGE for problem slides, AMBER for engineering)
2. **Title:** x=0.7, y=0.3, 28pt bold WHITE
3. **Subtitle:** x=0.7, y=0.85, 13pt GRAY
4. **Content area:** y=1.2 to y=4.2 (varies)
5. **Bottom bar** (optional): Full-width at y=5.2, 0.375" tall in DARK2

### Card Component

The fundamental building block for slide content. A dark container with an accent-colored top bar:

1. Background rectangle: CARD_BG fill with outer shadow (blur: 8, offset: 3, angle: 135, opacity: 0.3)
2. Accent bar: Same x/y as card, full card width, 0.04" tall, filled with accent color
3. Content inside the card uses standard text hierarchy

### Stat Card

A specialized card for KPI/metric display:
1. Base card with accent bar
2. Large stat value: 30pt bold in accent color, centered, y offset +0.12"
3. Label text: 10pt GRAY, centered, below the value

### Title Slide Pattern

- Left accent bar: 0.06" wide, full height, PETROL fill
- Bottom accent line: Full width at y=5.2, 0.06" tall, ORANGE at 40% transparency
- Org line at top: 12pt GRAY with charSpacing 4
- Main title: 44pt bold, split across two lines (WHITE + PETROL_LIGHT)
- Tagline: 16pt LIGHT
- Orange rule: 1.8" wide, 0.04" tall
- Bottom bar: DARK2, with domain list in 10pt GRAY

---

## Brand Voice in Document Content

While this skill focuses on visual branding, the documents also follow consistent content patterns:

- **Section numbering:** Decimal hierarchy (1., 1.1, 1.1.1)
- **Budget tiers:** Always "Lean", "Moderate", "Full Send" — never other names
- **Company references:** "Siemens Healthineers | Varian" (pipe separator) or "Varian (a Siemens Healthineers company)"
- **Classification:** "Confidential" in header
- **Footer pattern:** "Siemens Healthineers | Varian" left, "Page N" right
- **Currency:** USD with $ prefix, M suffix for millions, K suffix for thousands
- **Dates:** "Month YYYY" format (e.g., "April 2026")
