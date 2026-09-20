# HBEF Word Document (.docx) Instructions

How to apply the **HBEF 2026 brand system** to Word documents. Pair this with the `docx` skill (which provides `python-docx` mechanics) and `assets/brand-tokens.json` (which holds every hex/font value).

> **Rebrand note.** Everything below is the 2026 system: **Aleo** (headings/display) + **Lato** (body/UI), Navy `#0C3B5D`, Teal `#186892`, View `#FFCD00`. Montserrat, BauhausBold, `#0B4261`, `#F79B32`, `#75C4B9`, `#E7E7E7`, and the `INK*` tokens are retired — do not use them, and do not carry them forward from an older HBEF Word file. See `references/legacy-brand.md` if you must migrate one.

## Fonts — bundled and embeddable

Both brand families are **open source under the SIL Open Font License 1.1** and ship inside this skill:

- `assets/fonts/Aleo-{Regular,Bold,Italic,BoldItalic}.ttf` — headings, cover titles, display, pull quotes
- `assets/fonts/Lato-{Light,Regular,Italic,Bold,BoldItalic,Black}.ttf` — body, tables, captions, UI, fine print
- License texts: `assets/fonts/Aleo-OFL.txt`, `assets/fonts/Lato-OFL.txt`

Because they are OFL, you may **install them on the machine building the document and embed them in the .docx or exported PDF** without a licensing problem. This is a real change from the pre-2026 system, whose display face (BauhausBold) was proprietary and could not legally be embedded or shipped — documents had to hope the recipient had it. Now the correct move is to embed.

- In Word: *File → Options → Save → Embed fonts in the file* (uncheck "Embed only the characters used" for templates you expect others to edit).
- In `python-docx`: set the font name on **every run** (Word does not reliably inherit a theme font for east-asian/complex scripts — see `set_run_font()` below), then rely on PDF export to embed.
- If a recipient will open the file without the fonts installed, ship a PDF alongside the .docx.

**Fallback chains** (put these in CSS/HTML companions, and use them when substituting):

- Aleo → `Aleo, "Roboto Slab", "Zilla Slab", Rockwell, Georgia, serif` — **always fall back to a slab or serif, never a sans.**
- Lato → `Lato, "Helvetica Neue", Helvetica, Arial, sans-serif`

## Page setup

- **Page size:** US Letter (8.5" × 11" / 12240 × 15840 DXA)
- **Margins:** 1.0" all sides (1440 DXA) for body pages; 0" for the cover page; **2.0" top / 1.0" other** for letterhead pages (see the Letterhead section)
- **Content width:** 6.5" (9360 DXA)
- **Default font:** **Lato** (specify in the `Normal` style); fallback chain `'Lato', 'Helvetica Neue', Helvetica, Arial, sans-serif`
- **Heading font:** **Aleo** for Heading 1 / Heading 2 / Title; Lato Bold for Heading 3 and smaller
- **Line spacing:** 1.5 (body); 1.15–1.2 (headings — Aleo's slab serifs need a little less air than a sans)
- **Body color:** `HBEF_ASPHALT` `#515962`, never pure black

## Brand color constants

```python
from docx.shared import RGBColor

HBEF_NAVY      = RGBColor(0x0C, 0x3B, 0x5D)   # #0C3B5D  structure, headings, table headers
HBEF_TEAL      = RGBColor(0x18, 0x68, 0x92)   # #186892  supporting headers, rules
HBEF_TURQUOISE = RGBColor(0x12, 0x9F, 0xDA)   # #129FDA  links, energetic graphic accents
HBEF_VIEW      = RGBColor(0xFF, 0xCD, 0x00)   # #FFCD00  CTA / highlight (fill only, never small type)
HBEF_VISTA     = RGBColor(0xFF, 0xA4, 0x00)   # #FFA400  secondary highlight
HBEF_VALLEY    = RGBColor(0xEE, 0x76, 0x23)   # #EE7623  attention accent
HBEF_SKY       = RGBColor(0xB8, 0xD8, 0xEB)   # #B8D8EB  light band / callout fill
HBEF_SAND      = RGBColor(0xDD, 0xC9, 0xA3)   # #DDC9A3  warm alternate band
HBEF_WET_SAND  = RGBColor(0x98, 0x98, 0x9A)   # #98989A  metadata, captions, subtle borders
HBEF_ASPHALT   = RGBColor(0x51, 0x59, 0x62)   # #515962  body copy
WHITE          = RGBColor(0xFF, 0xFF, 0xFF)   # #FFFFFF  page + reversed type

# Document-only functional colors (not part of the public brand)
SUCCESS        = RGBColor(0x4A, 0x8B, 0x5C)   # #4A8B5C
RISK           = RGBColor(0xB2, 0x3A, 0x2D)   # #B23A2D
MUTED_BORDER   = RGBColor(0xD9, 0xD9, 0xD9)   # #D9D9D9  table borders, card outlines
SURFACE_ZEBRA  = "F7FAFC"                      # alternating table-row fill (hex string for w:shd)
SURFACE_TOTAL  = "E8F1F7"                      # total/summary-row fill (hex string for w:shd)
```

## Cover page

The cover is its own section with no header/footer. Structure top-to-bottom:

1. **`HBEF_NAVY` band** (full-width, ~3.5" tall):
   - Insert `assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png` centered horizontally, ~2.5" wide
   - Vertically centered within the navy band
   - Use the **Dark Mode** file — never the standard-color lockup on a navy fill

2. **White background** for the rest of the page

3. **Eyebrow line** (centered, **Lato Bold 9pt**, `HBEF_WET_SAND`, +1.2pt tracking, UPPERCASE):
   `HERMOSA BEACH EDUCATION FOUNDATION  ·  [DOCUMENT TYPE]`
   (e.g., `INVESTMENT COMMITTEE MEMO`, `ANNUAL REPORT`, `SPONSOR PROSPECTUS`)

4. **Title** (centered, **Aleo Bold 40pt**, `HBEF_NAVY`, **sentence or title case — do not uppercase, do not letterspace**; Aleo's slab serifs break down when tracked out)

5. **Subtitle** (centered, **Lato Light 18pt**, `HBEF_TEAL`, sentence case)

6. **Accent rule** (3pt horizontal, 1.5" wide, centered — color by deliverable type):

   | Deliverable | Rule color |
   |---|---|
   | Annual Giving / donor-facing (default) | `HBEF_VIEW` `#FFCD00` |
   | Event promo / recap — Hearts of Hermosa, Friendship Walk, Strand Classic | `HBEF_VALLEY` `#EE7623` |
   | Investment Committee / endowment | `HBEF_TEAL` `#186892` |
   | Technology Advisory Board / internal ops | `HBEF_TEAL` `#186892` |
   | Board governance / minutes | `HBEF_NAVY` `#0C3B5D` |

7. **Metadata block** (centered, bottom of page, **Lato 9pt**, `HBEF_WET_SAND`):
   `[Author Name] · [Month YYYY] · [Classification]`

8. **`HBEF_VIEW` footer band** (`#FFCD00`, 0.25" tall, full-bleed, no text)

### `python-docx` cover sketch

```python
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# Cover section: zero margins so bands can bleed
cover = doc.sections[0]
cover.top_margin = cover.bottom_margin = Inches(0)
cover.left_margin = cover.right_margin = Inches(0)

def set_run_font(run, name="Lato", size=11, bold=False, italic=False,
                 color=HBEF_ASPHALT):
    """Set a run's font on all script slots so Word doesn't substitute."""
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rFonts.set(qn(attr), name)
    return run

def set_tracking(run, points):
    """Letter-spacing in points (Word stores twentieths of a point)."""
    rPr = run._element.get_or_add_rPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:val'), str(int(points * 20)))
    rPr.append(spacing)
    return run
```

For brand bands, the cleanest `python-docx` pattern is a 1-cell table with the cell fill set to the brand hex:

```python
def add_band(doc, hex_fill, height_in=0.25, width_in=8.5):
    """Full-bleed color band rendered as a 1x1 borderless table."""
    band = doc.add_table(rows=1, cols=1)
    band.autofit = False
    cell = band.rows[0].cells[0]
    cell.width = Inches(width_in)

    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_fill)      # e.g. '0C3B5D' (HBEF_NAVY)
    tcPr.append(shd)

    # kill borders
    borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'nil')
        borders.append(el)
    tcPr.append(borders)

    band.rows[0].height = Inches(height_in)
    return band

navy_band  = add_band(doc, '0C3B5D', height_in=3.5)   # HBEF_NAVY hero band
view_band  = add_band(doc, 'FFCD00', height_in=0.25)  # HBEF_VIEW footer band
```

Place the cover logo inside the navy band's cell:

```python
logo_para = navy_band.rows[0].cells[0].paragraphs[0]
logo_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
logo_para.add_run().add_picture(
    "assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png",
    width=Inches(2.5),
)
```

## Running header

After the cover, headers appear on every page:

- **Left tab stop:** document title in **Lato Bold 8pt** `HBEF_NAVY` UPPERCASE, +0.6pt tracking
- **Right tab stop:** `Confidential` (or appropriate classification) in **Lato Italic 8pt** `HBEF_WET_SAND`
- **Bottom border:** 1.5pt `HBEF_TEAL` (`#186892`) line with 4pt space below

## Running footer

- **Left tab stop:** `Hermosa Beach Education Foundation · hbef.org` in **Lato 8pt** `HBEF_WET_SAND`
- **Right tab stop:** `Page N` in **Lato Bold 8pt** `HBEF_NAVY`
- **Top border:** 1pt `HBEF_TEAL` (`#186892`) line with 4pt space above — the SKILL.md multi-page footer pattern
- On a *letterhead* document the footer is different: see the mandatory EIN footer below.

```python
def add_paragraph_border(paragraph, edge="bottom", hex_color="186892",
                         size_eighths=12, space=4):
    """size_eighths = border weight in 1/8 pt (12 = 1.5pt, 8 = 1pt, 4 = 0.5pt)."""
    pPr = paragraph._p.get_or_add_pPr()
    borders = pPr.find(qn('w:pBdr'))
    if borders is None:
        borders = OxmlElement('w:pBdr')
        pPr.append(borders)
    el = OxmlElement(f'w:{edge}')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), str(size_eighths))
    el.set(qn('w:space'), str(space))
    el.set(qn('w:color'), hex_color)
    borders.append(el)
```

## Heading styles

Configure these as Word styles so they cascade consistently. **These are the exact 2026 document text-hierarchy values — do not invent sizes.**

| Style | Font | Size | Weight | Color | Casing | Space-before | Space-after |
|---|---|---|---|---|---|---|---|
| Title (cover) | Aleo | 40pt | Bold | `HBEF_NAVY` | Sentence / Title | — | 12pt |
| Cover subtitle | Lato Light (300) | 18pt | Light | `HBEF_TEAL` | sentence | 0 | 18pt |
| Heading 1 | Aleo | 24pt | Bold | `HBEF_NAVY` | Sentence / Title | 24pt | 8pt |
| Heading 2 | Aleo | 16pt | Bold | `HBEF_TEAL` | Sentence / Title | 18pt | 6pt |
| Heading 3 | Lato | 12pt | Bold | `HBEF_NAVY` | UPPER, +0.8pt tracking | 14pt | 6pt |
| Eyebrow / kicker | Lato | 9pt | Bold | `HBEF_WET_SAND` | UPPER, +1.2pt tracking | 0 | 4pt |
| Normal (body) | Lato | 11pt | Regular | `HBEF_ASPHALT` | sentence | 0 | 8pt |
| Lead | Lato | 13pt | Regular | `HBEF_ASPHALT` | sentence | 0 | 12pt |
| Quote (pull quote) | Aleo | 15pt | Italic | `HBEF_NAVY` | sentence | 12pt | 12pt |
| Caption | Lato | 9pt | Italic | `HBEF_WET_SAND` | sentence | 0 | 4pt |
| Footnote / legal | Lato | 8pt | Regular | `HBEF_WET_SAND` | sentence | 0 | 2pt |
| Link | Lato | inherit | Regular | `HBEF_TURQUOISE` | sentence | — | — |

Notes:

- **Heading 1** carries a 1pt `HBEF_VIEW` (`#FFCD00`) bottom border to mimic the section-divider rule. Across a long document, rotate the H1 rule color `HBEF_VIEW` → `HBEF_TEAL` → `HBEF_VALLEY` → `HBEF_TURQUOISE`, then loop.
- **Aleo headings are not uppercased and not letterspaced.** Only the Lato-set styles (H3, eyebrow, table header) take tracking and caps.
- **Pull quote** additionally gets a 0.4" left indent and a 3pt `HBEF_VIEW` left border.
- **Links** are `HBEF_TURQUOISE` `#129FDA`; underline them in print-bound documents, leave them clean on screen-only files.

```python
from docx.enum.style import WD_STYLE_TYPE

def define_hbef_styles(doc):
    styles = doc.styles

    normal = styles["Normal"]
    set_style_font(normal, "Lato", 11, False, HBEF_ASPHALT)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.space_after = Pt(8)

    h1 = styles["Heading 1"]
    set_style_font(h1, "Aleo", 24, True, HBEF_NAVY)
    h1.paragraph_format.space_before = Pt(24)
    h1.paragraph_format.space_after = Pt(8)

    h2 = styles["Heading 2"]
    set_style_font(h2, "Aleo", 16, True, HBEF_TEAL)
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(6)

    h3 = styles["Heading 3"]
    set_style_font(h3, "Lato", 12, True, HBEF_NAVY)   # uppercase the text itself
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)

def set_style_font(style, name, size_pt, bold, color):
    style.font.name = name
    style.font.size = Pt(size_pt)
    style.font.bold = bold
    style.font.color.rgb = color
    rPr = style.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rFonts.set(qn(attr), name)
```

## Tables

All tables span full content width (9360 DXA / 6.5"). Column widths must sum to exactly 9360.

**Header row:**
- Fill: `HBEF_NAVY` (`#0C3B5D`)
- Font: **Lato Bold, 10pt, `WHITE`**, UPPERCASE, +0.6pt tracking
- Cell margins: top/bottom 100 DXA, left/right 120 DXA

**Data rows:**
- Odd rows: plain (`WHITE` fill or no fill)
- Even rows: `SURFACE_ZEBRA` (`#F7FAFC`) — a very subtle cool stripe that reads as sea-glass, not gray
- Font: **Lato Regular, 10pt, `HBEF_ASPHALT`**

**Total / summary row:**
- Fill: `SURFACE_TOTAL` (`#E8F1F7`) — a pale Sky tint
- Font: **Lato Bold, 11pt, `HBEF_NAVY`**
- Optional 1pt `HBEF_TEAL` top border to separate it from the data body

**Sub-header / grouping row** (optional, for long financial tables):
- Fill: `HBEF_SKY` (`#B8D8EB`)
- Font: **Lato Bold, 10pt, `HBEF_NAVY`**

**Cell borders:** 0.5pt `MUTED_BORDER` (`#D9D9D9`)

**Notes column** (rightmost, if present): **Lato Italic 9pt `HBEF_WET_SAND`**

**Variance / status cells:** `SUCCESS` `#4A8B5C` for favorable, `RISK` `#B23A2D` for material risk, `HBEF_VISTA` `#FFA400` for caution. Color the *type*, not the cell fill, so the table stays quiet.

```python
def shade_cell(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_fill)
    tcPr.append(shd)

def style_table(table, headers, rows):
    # Header row
    for i, text in enumerate(headers):
        cell = table.rows[0].cells[i]
        shade_cell(cell, '0C3B5D')                      # HBEF_NAVY
        run = cell.paragraphs[0].add_run(text.upper())
        set_run_font(run, "Lato", 10, bold=True, color=WHITE)
        set_tracking(run, 0.6)

    # Data rows with zebra striping
    for r, row_data in enumerate(rows, start=1):
        for c, text in enumerate(row_data):
            cell = table.rows[r].cells[c]
            if r % 2 == 0:
                shade_cell(cell, 'F7FAFC')              # SURFACE_ZEBRA
            run = cell.paragraphs[0].add_run(str(text))
            set_run_font(run, "Lato", 10, color=HBEF_ASPHALT)
```

## Callout boxes

For sidebar emphasis ("Key takeaway:", "Recommendation:", etc.):

- 1-row, 1-cell table at 9360 DXA wide
- Cell fill: **`HBEF_SKY` (`#B8D8EB`)** — the default tinted callout. Use `HBEF_SAND` (`#DDC9A3`) only if the document has already committed to the warm neutral; never mix Sky and Sand callouts in the same file.
- Left border: 4pt `HBEF_VIEW` (`#FFCD00`) by default, or the deliverable's rotation color
- Cell margins: top/bottom 200 DXA, left/right 240 DXA
- Inside: H3-style label (**Lato Bold 12pt `HBEF_NAVY`**, uppercase, +0.8pt tracking) on the first line; body **Lato 11pt `HBEF_ASPHALT`** on subsequent lines
- 12pt space-before and space-after the callout

**Do not** put body text in `HBEF_VIEW` — yellow on a light fill fails contrast. View is a *border, band, or fill-behind-navy-text* color only.

## Rich bullet pattern

For lists where each item has a definition (program list, action items, etc.):

```
**Spanish Language:** 3rd–5th grade exploration program — funded entirely by HBEF.
**STEAM:** Sparks Lab, Idea Lab, Tech Lab across all three campuses.
```

Lead term in **Lato Bold `HBEF_NAVY`**, colon-space, description in **Lato Regular `HBEF_ASPHALT`**. Both 11pt. `spacing.after = 100` (DXA).

```python
def rich_bullet(doc, term, description):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(5)
    set_run_font(p.add_run(f"{term}: "), "Lato", 11, bold=True, color=HBEF_NAVY)
    set_run_font(p.add_run(description), "Lato", 11, color=HBEF_ASPHALT)
    return p
```

## Image guidance

- **Maximum width** for embedded images: 6.5" (full content width). Larger images get scaled down proportionally — never stretch.
- **Captions:** Centered below image, **Lato Italic 9pt `HBEF_WET_SAND`**. Credit `Jennifer Faulk Photography` where her work is identifiable.
- **Image borders:** None by default. If contrast is needed against the white page, add a 0.5pt `MUTED_BORDER` (`#D9D9D9`) border.
- **Logo placement by background:**

  | Background | File |
  |---|---|
  | Navy / Teal band (cover, dividers) | `assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png` |
  | White / Sky page, stacked space | `assets/logos/HBEF-Primary_Lockup-RGB@2x.png` |
  | White / Sky page, wide short space (letterhead, header) | `assets/logos/HBEF-Secondary_Lockup-RGB@2x.png` |
  | Navy header band, wide short space | `assets/logos/HBEF-Secondary_Lockup-Dark_Mode-RGB@2x.png` |
  | Tiny placement (< 1.25" wide) | `assets/logos/HBEF-Logomark.png` |

- **Clear space** = the height of the "HBEF" lettering, on all four sides. `HBEF-Logomark-space.png` has it pre-baked.
- **Minimum sizes:** lockups ≥ 1.25" wide; Logomark ≥ 0.4". Below 1.25", switch to the Logomark.
- Never stretch, rotate, recolor, add effects to, or reconstruct the logo.

---

## Letterhead (official HBEF layout)

HBEF's letterhead is the reference layout for every formal document — solicitation letters, donor thank-yous, press releases, board correspondence, grant cover letters.

**Master template:** `/Users/nolan/Projects/HBEF/HBEF BRANDING/LETTERHEAD/HBEF Letterhead.dotx`

**Use the template directly whenever you can.** It is the released, brand-approved file. Open it as the starting point (`Document("…/HBEF Letterhead.dotx")` works in `python-docx` — a `.dotx` is a valid OPC package; save the result as `.docx`), then write the letter body into it. Only build the layout from scratch when the deliverable can't start from the template (e.g. it's one section inside a larger generated report). The same folder holds `HBEF Letterhead Template.docx` (a sample letter) and `HBEF-Letterhead.pdf` (the visual proof — check your output against it).

### Layout spec

```
[Top margin 2.0" — header zone]

  LEFT (logo ≈ 3.5" wide)                 RIGHT (right-aligned, Lato Bold 9pt, HBEF_NAVY)
  Secondary lockup, with the tagline       1645 Valley Drive
  set beneath the wordmark                 Hermosa Beach, CA 90254
                                           (blank line)
                                           hbef.org
                                           @hbef90254

[Body — 1.0" left/right margins, generous leading]

[Footer, centered, Lato Italic 8pt, HBEF_ASPHALT]
HBEF is a registered 501(c)(3) non-profit organization. Contributions are
tax-deductible to the extent allowed by law. Federal tax identification
number (EIN): 33-0522270
```

- **Page:** US Letter 8.5 × 11", portrait.
- **Margins:** top **2.0"** (clears the header block), left/right/bottom **1.0"**.
- **Logo:** Secondary (horizontal) lockup, ≈ 3.5" wide, left-aligned in the header zone. Standard-color RGB file on the white page — `HBEF-Secondary_Lockup-RGB@2x.png`.
- **Address block:** right-aligned, **Lato Bold 9pt, `HBEF_NAVY`**, one line per element, with a blank line between the postal address and the digital block.
- **EIN footer:** centered, **Lato Italic 8pt, `HBEF_ASPHALT`**. **Mandatory on every letterhead page and every donor-facing document** — no exceptions, no abbreviation of the wording.
- **Letter body order:** date · recipient block · salutation · paragraphs · "Sincerely," · name · title · phone · email.
- No running header on letterhead pages; the header zone *is* the letterhead. On multi-page letters, page 2+ may use a plain Lato 8pt `HBEF_WET_SAND` continuation line (`Hermosa Beach Education Foundation · Page 2`) — but the EIN footer still appears on every page.

> **Known variance:** the released `.dotx` and the Strand Classic press release set body copy in **Aleo 12pt**, not Lato. The 2026 Brand Guidelines are authoritative — use **Aleo headings + Lato 11pt body** for new work. If you are editing one of those existing files in place, keep its native Aleo body so the document stays internally consistent, and tell the requester about the variance.

### Building a letterhead doc programmatically

```python
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT

LETTERHEAD_DOTX = "/Users/nolan/Projects/HBEF/HBEF BRANDING/LETTERHEAD/HBEF Letterhead.dotx"
LOGO_SECONDARY  = "assets/logos/HBEF-Secondary_Lockup-RGB@2x.png"

TAX_LANGUAGE = (
    "HBEF is a registered 501(c)(3) non-profit organization. Contributions are "
    "tax-deductible to the extent allowed by law. Federal tax identification "
    "number (EIN): 33-0522270"
)

ADDRESS_BLOCK = [
    "1645 Valley Drive",
    "Hermosa Beach, CA 90254",
    "",
    "hbef.org",
    "@hbef90254",
]


def new_letterhead(from_template=True):
    """Preferred path: start from the released .dotx."""
    if from_template:
        doc = Document(LETTERHEAD_DOTX)   # then just write the body
        return doc
    return build_letterhead_from_scratch()


def build_letterhead_from_scratch():
    doc = Document()

    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    sec.top_margin = Inches(2.0)                       # header zone
    sec.left_margin = sec.right_margin = Inches(1.0)
    sec.bottom_margin = Inches(1.0)
    sec.header_distance = Inches(0.5)
    sec.footer_distance = Inches(0.5)

    # --- Header: logo left, address block right -------------------------
    header = sec.header
    table = header.add_table(rows=1, cols=2, width=Inches(6.5))
    table.autofit = False
    left, right = table.rows[0].cells
    left.width, right.width = Inches(3.6), Inches(2.9)

    logo_p = left.paragraphs[0]
    logo_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    logo_p.add_run().add_picture(LOGO_SECONDARY, width=Inches(3.5))

    for i, line in enumerate(ADDRESS_BLOCK):
        p = right.paragraphs[0] if i == 0 else right.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.15
        set_run_font(p.add_run(line), "Lato", 9, bold=True, color=HBEF_NAVY)

    strip_table_borders(table)

    # --- Footer: mandatory EIN line -------------------------------------
    footer_p = sec.footer.paragraphs[0]
    footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_p.paragraph_format.line_spacing = 1.2
    set_run_font(footer_p.add_run(TAX_LANGUAGE),
                 "Lato", 8, italic=True, color=HBEF_ASPHALT)

    return doc


def strip_table_borders(table):
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            borders = OxmlElement('w:tcBorders')
            for edge in ('top', 'left', 'bottom', 'right'):
                el = OxmlElement(f'w:{edge}')
                el.set(qn('w:val'), 'nil')
                borders.append(el)
            tcPr.append(borders)


def write_letter_body(doc, date_str, recipient_lines, salutation,
                      paragraphs, signer, title, phone, email):
    def para(text, size=11, bold=False, italic=False,
             color=HBEF_ASPHALT, after=10):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.line_spacing = 1.5
        set_run_font(p.add_run(text), "Lato", size, bold, italic, color)
        return p

    para(date_str, after=18)
    for line in recipient_lines:
        para(line, after=0)
    para("", after=6)
    para(salutation, after=10)
    for body_para in paragraphs:
        para(body_para)
    para("", after=6)
    para("Sincerely,", after=36)          # room for a signature image
    para(signer, bold=True, color=HBEF_NAVY, after=0)
    para(title, size=10, color=HBEF_WET_SAND, after=0)
    para(f"{phone} · {email}", size=10, color=HBEF_WET_SAND, after=0)
    return doc
```

Save the result with `doc.save("HBEF-Letter-YYYY-MM-DD.docx")`. If the recipient may not have the fonts, also export a PDF (fonts embed from the OFL files).

---

## Section dividers inside a long document

```
[HBEF_SKY (#B8D8EB) full-width band, 0.4" tall]

[Eyebrow — Lato Bold 9pt, HBEF_WET_SAND, uppercase, +1.2pt tracking]
PART 02

[Title — Aleo Bold 16pt, HBEF_NAVY]
Section Title

[2pt rule, 100% width, 12pt below title]
```

Rule color rotation across a long document: `HBEF_VIEW` → `HBEF_TEAL` → `HBEF_VALLEY` → `HBEF_TURQUOISE`, then loop. Build the band with `add_band(doc, 'B8D8EB', height_in=0.4)`.

## Final checks (before sharing)

1. Cover loaded with the **Dark Mode** lockup on the navy band, and the correct accent-rule color for the deliverable type.
2. Header/footer present on body pages, absent on the cover.
3. All headings use defined styles (not hand-formatted). Aleo on H1/H2/Title, Lato Bold on H3.
4. No Montserrat, no BauhausBold, no `#0B4261` / `#F79B32` / `#75C4B9` / `#E7E7E7` anywhere in the file — search the XML if you inherited the doc from an older version.
5. Tables: Navy header row, `#F7FAFC` zebra stripes, `#E8F1F7` total row, `#D9D9D9` borders.
6. Body text is `HBEF_ASPHALT` `#515962` — no pure black, no `#1A1A1A`.
7. `HBEF_VIEW` `#FFCD00` used only as fill/border/rule, never as small type on light.
8. Tax language (EIN 33-0522270) present on donor-facing deliverables, and on **every** letterhead page.
9. Fonts embedded (or a PDF shipped alongside) — Aleo and Lato are OFL, so embedding is permitted.
10. PDF export tested if the document will be distributed externally; check it against `HBEF-Letterhead.pdf` for letterhead jobs.
11. Page numbers paginate correctly.
12. Spellcheck run on the final pass.
