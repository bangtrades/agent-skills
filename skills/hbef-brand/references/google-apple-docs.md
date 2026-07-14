# HBEF — Google Docs, Sheets, Slides & Apple Pages, Numbers, Keynote

How to apply the HBEF brand system in cloud / Apple-native formats where the Office binary tooling (`python-docx`, `openpyxl`, `python-pptx`) doesn't apply. Two paths are available:

1. **Export from a generated Office file** — best fidelity, recommended for most deliverables
2. **Manual paste-in styling** — when the deliverable must originate in the cloud format

This file documents both paths plus the font-substitution rules that keep brand integrity intact.

---

## Path 1: Export from Office (recommended)

Generate the file using the Word/Excel/PowerPoint pattern from this skill, then:

| Target format | Export path | Fidelity |
|---|---|---|
| **Google Docs** | Upload `.docx` to Drive → right-click → "Open with Google Docs" | High — preserves styles, tables, images. Watch fonts. |
| **Google Sheets** | Upload `.xlsx` to Drive → "Open with Google Sheets" | High — preserves formulas, formatting. Tab colors transfer. |
| **Google Slides** | Upload `.pptx` to Drive → "Open with Google Slides" | Medium — some layout drift on complex slides. Verify visually. |
| **Apple Pages** | Open `.docx` directly in Pages | High — Pages handles docx well. Watch table styling. |
| **Apple Numbers** | Open `.xlsx` directly in Numbers | Medium — Numbers re-flows tables. Charts may need redo. |
| **Apple Keynote** | Open `.pptx` directly in Keynote | Medium — fonts and gradient fills may shift. Verify each slide. |

**Verification step:** Open the converted file and screenshot or PDF-export to confirm brand colors and typography survived the conversion. If fonts dropped to a default (Arial, Helvetica), it's a font-substitution issue — see below.

---

## Path 2: Manual paste-in styling (for native authoring)

When the user wants to start in Google Docs / Pages directly, here are the manual recipes.

### Google Docs

**Page setup** (File → Page setup):
- Letter, portrait
- Margins: 1" all sides
- Page color: White

**Define paragraph styles** (Format → Paragraph styles → Options → "Save current as default"):

| Style | Font | Size | Weight | Color | Other |
|---|---|---|---|---|---|
| Title | Montserrat | 42 | Bold | `#0B4261` | UPPER, +1 spacing |
| Heading 1 | Montserrat | 28 | Bold | `#0B4261` | UPPER |
| Heading 2 | Montserrat | 18 | Bold | `#0B4261` | UPPER |
| Heading 3 | Montserrat | 13 | Bold | `#417987` | UPPER |
| Normal | Montserrat | 11 | Regular | `#1A1A1A` | Line height 1.5 |
| Subtitle | Montserrat | 22 | Light (Thin) | `#75C4B9` | sentence case |

**Add HBEF logo:** Insert → Image → Upload → use `assets/logos/hbef-secondary-lockup-dark.png`. Wrap "In line with text" at top of cover page.

**Color codes to memorize** (paste from `assets/brand-tokens.json`):
- Navy `#0B4261` · Orange `#F79B32` · Teal `#75C4B9` · Teal-muted `#417987` · Page `#E7E7E7`

**Tables:** Use the table tool, then format the first row: right-click → Table properties → Header row → Background color = `#0B4261`, text color = white, bold.

**Tax footer:** Insert → Footer → paste:
> *HBEF is a registered 501(c)(3) non-profit organization. Contributions are tax-deductible to the extent allowed by law. EIN: 33-0522270.*

### Google Sheets

**Tab colors:** Right-click tab → Change color → choose closest to:
- Cover tab: dark blue (closest to `#0B4261`)
- Summary tab: orange (closest to `#F79B32`)
- Data tab: teal/cyan (closest to `#75C4B9`)
- Notes tab: gray

**Header row:** Select row 1 → Format → Cell background `#0B4261` → Text color white → Bold.

**Total row:** Background `#E7E7E7` → Text color `#0B4261` → Bold → Top + bottom border (medium, `#0B4261`).

**Conditional formatting** for variance columns:
- Custom formula → If positive → text color `#5A9E78`
- If negative → text color `#B23A2D`

**Chart styling:** Insert chart → Customize → Chart style → Background `WHITE`. Series colors paste in order: `#0B4261`, `#F79B32`, `#75C4B9`, `#417987`, `#124362`, `#5C5C5C`.

### Google Slides

**Theme setup:** View → Theme builder (Edit theme):
- Background: white
- Title font: Montserrat (size 60, bold, `#0B4261`)
- Body font: Montserrat (size 16, regular, `#1A1A1A`)
- Accent 1: `#0B4261`
- Accent 2: `#F79B32`
- Accent 3: `#75C4B9`

**Cover slide:** Insert → Shape → Rectangle covering top 30% → Fill `#0B4261`. Insert → Image → upload HBEF lockup, center in band.

**Section dividers:** New slide → Layout: Blank → Insert rectangle full-bleed `#0B4261` → Add title text `WHITE` Montserrat 44 bold uppercase.

### Apple Pages

**Document setup** (Document inspector):
- Letter, portrait, 1" margins
- Body font: Montserrat 11 — install via Font Book if not present
- Paragraph spacing: 8pt after

**Define paragraph styles** (Format inspector → Style → "+"):
- Same hierarchy as Google Docs above

**Color picker:** Pages uses the standard macOS color picker. Type hex into the "Color sliders" → RGB Sliders → hex field at bottom.

**HBEF logo:** Drag PNG from Finder into the document. Use "Wrap with text" → Inline; Arrange → Bring to front.

**Tables:** Format → Table → Header row "Style 5 (Dark)" then override fill to `#0B4261`.

**Export to PDF:** File → Export To → PDF → Image quality "Better" — Pages embeds fonts correctly.

### Apple Numbers

Numbers' table model is different from Excel (sheets contain multiple free-floating tables rather than one grid). For HBEF deliverables, prefer this layout:

- **Sheet 1: "Cover"** — single table 4 cols × 8 rows holding the title block + metadata
- **Sheet 2+: "Data"** — one table per topic, header row stylized

**Header row styling:** Select first row → Format inspector → Cell → Fill color `#0B4261` → Text white bold Montserrat.

**Charts:** Numbers charts are styled per-chart. Apply HBEF colors via Format → Style → Chart Colors → manually set each series. Same 6-color palette as elsewhere.

**Export to PDF:** File → Export To → PDF → "Best (slow)".

### Apple Keynote

**Theme:** Keynote → File → New → "Basic White" → then customize. Don't start from a busy theme.

**Slide Master** (View → Edit Master Slides):
- Master 1 (Title): Add navy band rectangle, place HBEF lockup centered.
- Master 2 (Section): Full-bleed `#0B4261`, white text.
- Master 3 (Content): Top accent bar 0.05" `#0B4261`, title placeholder Montserrat 28 bold `#0B4261`.
- Master 4 (Stat): Centered placeholder Montserrat 120 thin `#0B4261`.
- Master 5 (Quote): Italic Montserrat 32 `#0B4261`, teal underline.
- Master 6 (Closing): Half navy / half white, donate URL.

**Export:** File → Export To → PowerPoint (`.pptx`) for distribution, or PDF for review copies.

---

## Font substitution rules

Both Montserrat and BauhausBold are free and easy to install — but recipients may not have them. Substitution rules in order of preference:

### Montserrat unavailable → fallback chain

1. **`Avenir Next`** (macOS default, Windows via Office) — very close geometric grotesque, looks 90% like Montserrat
2. **`Helvetica Neue`** (macOS, modern Office) — neutral, loses Montserrat's slight character but reads cleanly
3. **`Arial`** (everywhere) — last-resort fallback
4. *Never*: Calibri (too rounded), Times New Roman (wrong category), Comic Sans (obviously)

### BauhausBold unavailable → fallback chain

1. **`ITC Avant Garde Gothic`** — closest commercial match (geometric heavy)
2. **`Century Gothic`** (Microsoft) — widely available, geometric
3. **`Futura`** (macOS) — geometric, but lighter — bump weight to 800/900
4. **`Montserrat 800` or `900`** — fallback within the same family; works
5. *Never*: Impact (too condensed), Arial Black (too narrow), serif faces

### Installing fonts

**Google Fonts (Montserrat):**
- macOS: `brew install --cask font-montserrat` *or* download from fonts.google.com → double-click .ttf → Install
- Windows: Settings → Personalization → Fonts → drag .ttf files in

**BauhausBold:**
- Bundled in this skill at `assets/fonts/bauhaus-bold.ttf`
- Install via Font Book (macOS) or right-click → Install (Windows)
- *Note:* The .woff file is web-only; use .ttf for desktop installation

### Document metadata

In every deliverable, embed a small font-fallback note in the colophon / "About this document" footer for recipients:

> *This document is set in Montserrat (Google Fonts) and BauhausBold (HBEF custom). If the typography looks different on your machine, install the fonts from fonts.google.com/specimen/Montserrat — the document content is unchanged.*

---

## When to choose which path

| Scenario | Recommended path |
|---|---|
| One-off letter, memo, brief | Generate `.docx`, export to PDF, share PDF |
| Recurring board document (minutes, treasurer report) | Generate `.docx` → open in Google Docs for collaborative editing |
| Live-collab fundraising tracker | Native Google Sheets (manual styling) — multiple board members will edit simultaneously |
| Sponsor pitch deck for in-person presentation | Generate `.pptx`, open in Keynote on Mac for presenter mode |
| Annual report (final, print-ready) | Generate `.docx` → export PDF → share PDF |
| Email-attachment one-pager | Generate PDF directly (HTML→PDF path) |

---

## Final guardrails

- **Don't accept default fonts.** If Google Docs or Pages auto-substitutes when a font isn't installed, fix it before publishing. Default Arial in a brand doc reads as "we didn't bother."
- **Verify brand color codes after conversion.** Some apps re-quantize hex codes to their nearest palette swatch. After uploading a docx to Google Docs, click a navy heading and confirm it shows `#0B4261`, not `#0B4365` or similar.
- **Logo files travel with the doc** in cloud formats. Pages and Keynote embed images by default; Google Docs/Slides do too. No need to re-link.
- **Confidentiality:** Google Drive defaults to "anyone with the link can view" if shared casually. Set permission to "Restricted" or specific board emails before sharing donor data or IC memos.
