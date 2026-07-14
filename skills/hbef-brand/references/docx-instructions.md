# HBEF Word Document (.docx) Instructions

How to apply the HBEF brand system to Word documents. Pair this with the `docx` skill (which provides `python-docx` mechanics) and `assets/brand-tokens.json` (which holds every hex/font value).

## Page setup

- **Page size:** US Letter (8.5" × 11" / 12240 × 15840 DXA)
- **Margins:** 1.0" all sides (1440 DXA) for body pages; 0" for cover page
- **Content width:** 6.5" (9360 DXA)
- **Default font:** Montserrat (specify in Normal style); fallback chain `'Montserrat', 'Avenir Next', 'Helvetica Neue', Arial, sans-serif`
- **Line spacing:** 1.5 (body); 1.15 (headings)

## Cover page

The cover is its own section with no header/footer. Structure top-to-bottom:

1. **HBEF_NAVY band** (full-width, ~3.5" tall):
   - Insert the lockup `assets/logos/hbef-secondary-lockup-dark.png` centered horizontally, ~2.5" wide
   - Vertically centered within the navy band

2. **White background** for the rest of the page

3. **Eyebrow line** (centered, 9pt Montserrat 700, `INK_60`, +1.2pt tracking, UPPERCASE):
   `HERMOSA BEACH EDUCATION FOUNDATION  ·  [DOCUMENT TYPE]`
   (e.g., `INVESTMENT COMMITTEE MEMO`, `ANNUAL REPORT`, `SPONSOR PROSPECTUS`)

4. **Title** (centered, 42pt BauhausBold-or-Montserrat 800, `HBEF_NAVY`, UPPERCASE, +1.5pt tracking)

5. **Subtitle** (centered, 22pt Montserrat Light 200, `HBEF_TEAL`, sentence case)

6. **Accent rule** (3pt horizontal, `HBEF_ORANGE` by default — rotate per the SKILL.md rule by deliverable type):
   - Annual Giving / donor: `HBEF_ORANGE`
   - IC / endowment: `HBEF_NAVY_DEEP`
   - Event recap: `HBEF_TEAL`
   - Governance / minutes: `HBEF_NAVY`
   - Width: 1.5" centered

7. **Metadata block** (centered, bottom of page, 9pt Montserrat 400, `INK_60`):
   `[Author Name] · [Month YYYY] · [Classification]`

8. **HBEF_TEAL footer band** (0.25" tall, full-bleed, no text)

### `python-docx` cover sketch

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Cover section: zero margins
cover = doc.sections[0]
cover.top_margin = cover.bottom_margin = Inches(0)
cover.left_margin = cover.right_margin = Inches(0)

# (Insert image as inline shape with anchor=top-left in the navy band)
# (Use page-shape for the navy band — easier to render as a 1-row table)
```

For brand bands, the cleanest python-docx pattern is a 1-cell table with cell fill set to the brand hex:

```python
band = doc.add_table(rows=1, cols=1)
cell = band.rows[0].cells[0]
cell.width = Inches(8.5)
# Set cell fill via tcPr → shd element
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
tcPr = cell._tc.get_or_add_tcPr()
shd = OxmlElement('w:shd')
shd.set(qn('w:val'), 'clear')
shd.set(qn('w:fill'), '0B4261')  # HBEF_NAVY
tcPr.append(shd)
```

## Running header

After the cover, headers appear on every page:

- **Left tab stop:** document title in 8pt Montserrat 700 `HBEF_NAVY` UPPERCASE
- **Right tab stop:** `Confidential` (or appropriate classification) in 8pt Montserrat 400 italic `INK_60`
- **Bottom border:** 1.5pt `HBEF_TEAL` line with 4pt space below

## Running footer

- **Left tab stop:** `Hermosa Beach Education Foundation · hbef.org` in 8pt Montserrat 400 `INK_60`
- **Right tab stop:** `Page N` in 8pt Montserrat 700 `HBEF_NAVY`
- **Top border:** 0.5pt `MUTED_BORDER` line with 4pt space above

## Heading styles

Configure these as Word styles so they cascade consistently:

| Style | Font | Size | Weight | Color | Casing | Space-before | Space-after |
|---|---|---|---|---|---|---|---|
| Title (cover) | Montserrat 800 | 42pt | Bold | `HBEF_NAVY` | UPPER | — | 12pt |
| Heading 1 | Montserrat 700 | 28pt | Bold | `HBEF_NAVY` | UPPER | 24pt | 12pt |
| Heading 2 | Montserrat 700 | 18pt | Bold | `HBEF_NAVY` | UPPER | 18pt | 9pt |
| Heading 3 | Montserrat 700 | 13pt | Bold | `HBEF_TEAL_MUTED` | UPPER | 14pt | 6pt |
| Normal (body) | Montserrat 400 | 11pt | Regular | `INK` | sentence | 0 | 8pt |
| Lead | Montserrat 400 | 13pt | Regular | `INK` | sentence | 0 | 12pt |
| Caption | Montserrat 400 italic | 9pt | Italic | `INK_60` | sentence | 0 | 4pt |
| Quote | Montserrat 400 italic | 16pt | Italic | `HBEF_NAVY` | sentence | 12pt | 12pt |
| Footnote | Montserrat 400 | 8pt | Regular | `INK_60` | sentence | 0 | 2pt |

Heading 1 should also have a 1pt `HBEF_ORANGE` bottom border to mimic the section-divider rule.

## Tables

All tables span full content width (9360 DXA / 6.5"). Column widths must sum to exactly 9360.

**Header row:**
- Fill: `HBEF_NAVY` (`#0B4261`)
- Font: Montserrat 700, 10pt, `WHITE`, UPPERCASE, +0.8pt tracking
- Cell margins: top/bottom 100 DXA, left/right 120 DXA

**Data rows:**
- Odd rows: plain (`WHITE` fill or no fill)
- Even rows: `SURFACE_ZEBRA` (`#FAFAFA`) — very subtle stripe
- Font: Montserrat 400, 10pt, `INK`

**Total / summary row:**
- Fill: `SURFACE_TOTAL` / `HBEF_PAGE` (`#E7E7E7`)
- Font: Montserrat 700, 11pt, `HBEF_NAVY`

**Cell borders:** 0.5pt `MUTED_BORDER` (`#CCCCCC`)

**Notes column** (rightmost, if present): Montserrat 400 italic 9pt `INK_60`

## Callout boxes

For sidebar emphasis ("Key takeaway:", "Recommendation:", etc.):

- 1-row, 1-cell table at 9360 DXA wide
- Cell fill: `SURFACE_SOFT` (`#F2F2F2`) — soft gray
- Left border: 4pt `HBEF_ORANGE` (or rotation color)
- Cell margins: top/bottom 200 DXA, left/right 240 DXA
- Inside: H3-style label (e.g., "Key Takeaway") on first line, body 11pt on subsequent lines
- 12pt space-before and space-after the callout

## Rich bullet pattern

For lists where each item has a definition (program list, action items, etc.):

```
**Spanish Language:** 3rd–5th grade exploration program — funded entirely by HBEF.
**STEAM:** Sparks Lab, Idea Lab, Tech Lab across all three campuses.
```

Lead term in Montserrat 700 `HBEF_NAVY`, colon-space, description in Montserrat 400 `INK`. Both 11pt. `spacing.after = 100` (DXA).

## Image guidance

- **Maximum width** for embedded images: 6.5" (full content width). Larger images get scaled down.
- **Captions:** Centered below image, 9pt Montserrat 400 italic `INK_60`.
- **Image borders:** None by default. If contrast is needed against white page, add a 0.5pt `MUTED_BORDER` border.
- **Cover lockup:** Use `assets/logos/hbef-secondary-lockup-dark.png` for navy-band placements (white wordmark on navy). For all-white-background placements, the same PNG works.

## Letterhead pattern

For letters (Annual Giving solicitations, donor thank-yous):

- **Top 1"** of page 1:
  - Left: HBEF logo `hbef-secondary-lockup-dark.png` at 1.25" wide
  - Right: Right-aligned, 9pt Montserrat 400 `INK_60`:
    `Hermosa Beach Education Foundation`
    `1645 Valley Drive · Hermosa Beach, CA 90254`
    `hbef.org · admin@hbef.org`
- **1pt `HBEF_TEAL` horizontal rule** below the letterhead block
- Body starts ~0.5" below the rule
- Signature block at end, followed by a tax-language footnote in 8pt italic `INK_60`

## Final checks (before sharing)

1. Cover loaded with logo + correct accent-rule color for deliverable type.
2. Header/footer present on body pages, absent on cover.
3. All headings use defined styles (not hand-formatted).
4. Tables: header navy, zebra stripes, total row gray.
5. Tax language present on donor-facing deliverables.
6. PDF export tested if document will be distributed externally.
7. Page numbers paginate correctly.
8. Spellcheck run on final pass (Montserrat doesn't catch homophones).
