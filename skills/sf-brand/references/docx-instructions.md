# SF-Brand × Word Documents (.docx)

Use this with the **`docx` skill** when producing Word documents for the Summer Fridays project. The `docx` skill handles file mechanics (python-docx, OOXML); this file tells you what the output should look like.

## When this applies
Any Word deliverable for the SF project — research briefs, marketing plans, campaign briefs, partnership proposals, content calendars in prose form, executive memos.

## Toolchain
- **Python:** `python-docx` (preferred) — direct OOXML control
- **Alternative:** `docxtpl` for template-driven jobs (Jinja in a styled .docx)

## Document setup

```python
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# Page setup — US Letter, generous margins (brand reads "breathable")
for section in doc.sections:
    section.page_width = Inches(8.5)
    section.page_height = Inches(11)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.1)   # slightly wider than top/bottom — more chalk on the sides
    section.right_margin = Inches(1.1)
```

## Brand color helper

```python
from docx.shared import RGBColor

SF = {
    "INK":              RGBColor(0x1A, 0x1A, 0x1A),
    "INK_60":           RGBColor(0x5C, 0x5C, 0x5C),
    "INK_30":           RGBColor(0xA8, 0xA8, 0xA8),
    "CHALK":            "FAF6EF",  # cell-fill format (no '#')
    "MORNING_SKY":      "BDD7E5",
    "MORNING_SKY_DEEP": RGBColor(0x7D, 0xA8, 0xBD),
    "CLAY":             "C9A582",
    "VANILLA":          "F5E9DD",
    "PINK_SUGAR":       RGBColor(0xFC, 0x88, 0xAB),
    "PINK_GUAVA":       RGBColor(0xB4, 0x4F, 0x65),
    "ACCENT_BLUE":      RGBColor(0x3C, 0x5A, 0x78),
    "MUTED_BORDER":     "E5E5EB",
}

FONT = "Avenir Next"   # safest cross-platform fallback for Futura PT
FONT_DISPLAY = "Cormorant Garamond"  # editorial italic accent
```

## Cover page

```python
def add_cover(doc, title, subtitle, author, date, doc_type="MARKETING INTELLIGENCE"):
    # Top eyebrow
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f"SUMMER FRIDAYS  ·  {doc_type}")
    run.font.name = FONT
    run.font.size = Pt(9)
    run.font.color.rgb = SF["INK_60"]
    run.font.bold = False
    _set_letter_spacing(run, 120)   # +1.2pt

    # ~5 inches of vertical space (the title sits low-mid)
    for _ in range(8):
        doc.add_paragraph()

    # Title
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(title)
    run.font.name = FONT
    run.font.size = Pt(36)
    run.font.color.rgb = SF["INK"]
    run.font.bold = False

    # Subtitle
    if subtitle:
        p = doc.add_paragraph()
        run = p.add_run(subtitle)
        run.font.name = FONT_DISPLAY
        run.font.size = Pt(18)
        run.font.italic = True
        run.font.color.rgb = SF["INK_60"]

    # Morning-sky rule (1.5" wide, 2pt) — using a paragraph with bottom border
    p = doc.add_paragraph()
    _add_short_bottom_border(p, color="BDD7E5", width_pt=2, paragraph_width_inches=1.5)

    # Footer block
    for _ in range(12):
        doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run(f"{author}   ·   {date}   ·   Confidential — Internal Working Document")
    run.font.name = FONT
    run.font.size = Pt(9)
    run.font.color.rgb = SF["INK_60"]
    _set_letter_spacing(run, 50)

    doc.add_page_break()
```

## Headings

Define explicit styles up front rather than relying on Word's defaults:

```python
def setup_styles(doc):
    styles = doc.styles

    # H1
    h1 = styles["Heading 1"]
    h1.font.name = FONT
    h1.font.size = Pt(22)
    h1.font.bold = False
    h1.font.color.rgb = SF["INK"]
    h1.paragraph_format.space_before = Pt(24)
    h1.paragraph_format.space_after = Pt(12)
    _set_letter_spacing(h1.font, 50)

    # H2
    h2 = styles["Heading 2"]
    h2.font.name = FONT
    h2.font.size = Pt(16)
    h2.font.bold = False
    h2.font.color.rgb = SF["INK"]
    h2.paragraph_format.space_before = Pt(18)
    h2.paragraph_format.space_after = Pt(8)

    # H3 — uppercase, MORNING_SKY_DEEP
    h3 = styles["Heading 3"]
    h3.font.name = FONT
    h3.font.size = Pt(12)
    h3.font.bold = False
    h3.font.color.rgb = SF["MORNING_SKY_DEEP"]
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)
    _set_letter_spacing(h3.font, 120)
    # H3 text should be uppercased at insertion time, not via style

    # Body
    body = styles["Normal"]
    body.font.name = FONT
    body.font.size = Pt(11)
    body.font.color.rgb = SF["INK"]
    body.paragraph_format.line_spacing = 1.55
    body.paragraph_format.space_after = Pt(8)
```

## Tables — the brand-correct pattern

```python
def add_branded_table(doc, headers, rows, notes_col=None):
    """
    headers: list[str]
    rows:    list[list[str]]
    notes_col: int | None — index of a column to render in italic INK_60 9pt
    """
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_ALIGN_PARAGRAPH.CENTER
    table.autofit = False

    # Header row
    hdr = table.rows[0]
    for i, label in enumerate(headers):
        cell = hdr.cells[i]
        _shade_cell(cell, SF["MORNING_SKY"])
        p = cell.paragraphs[0]
        run = p.add_run(label.upper())
        run.font.name = FONT
        run.font.size = Pt(10)
        run.font.bold = False
        run.font.color.rgb = SF["INK"]
        _set_letter_spacing(run, 80)

    # Data rows — alternating CHALK on even rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            if r_idx % 2 == 1:
                _shade_cell(cell, SF["CHALK"])
            p = cell.paragraphs[0]
            run = p.add_run(str(val))
            run.font.name = FONT
            if notes_col is not None and c_idx == notes_col:
                run.font.size = Pt(9)
                run.font.italic = True
                run.font.color.rgb = SF["INK_60"]
            else:
                run.font.size = Pt(10)
                run.font.color.rgb = SF["INK"]

    # Hairline borders in MUTED_BORDER
    _set_table_borders(table, color=SF["MUTED_BORDER"], width_pt=0.5)
    return table
```

## Callout box (one-cell shaded paragraph)

Use this to lift recommendations or "watch this signal" notes off the page.

```python
def add_callout(doc, title, body, tone="sky"):
    """tone: 'sky' | 'vanilla' | 'clay' | 'pink' — picks the fill."""
    fills = {
        "sky":     "BDD7E5",
        "vanilla": "F5E9DD",
        "clay":    "C9A582",
        "pink":    "FC88AB",
    }
    table = doc.add_table(rows=1, cols=1)
    cell = table.rows[0].cells[0]
    _shade_cell(cell, fills.get(tone, "BDD7E5"))
    cell.paragraphs[0].text = ""

    # Title
    p = cell.add_paragraph()
    run = p.add_run(title.upper())
    run.font.name = FONT
    run.font.size = Pt(10)
    run.font.bold = False
    run.font.color.rgb = SF["INK"]
    _set_letter_spacing(run, 120)

    # Body
    p = cell.add_paragraph()
    run = p.add_run(body)
    run.font.name = FONT
    run.font.size = Pt(11)
    run.font.color.rgb = SF["INK"]
    p.paragraph_format.line_spacing = 1.5

    # Cell padding (~12pt all sides)
    _set_cell_margins(cell, top=200, bottom=200, left=240, right=240)
```

## Pull quote

```python
def add_pull_quote(doc, quote, attribution=None):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.right_indent = Inches(0.5)
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    # Left border in MORNING_SKY
    _add_left_border(p, color="BDD7E5", width_pt=3)

    run = p.add_run(f"“{quote}”")
    run.font.name = FONT_DISPLAY    # Cormorant Garamond italic
    run.font.size = Pt(18)
    run.font.italic = True
    run.font.color.rgb = SF["INK"]

    if attribution:
        p2 = doc.add_paragraph()
        p2.paragraph_format.left_indent = Inches(0.5)
        run = p2.add_run(f"— {attribution}")
        run.font.name = FONT
        run.font.size = Pt(9)
        run.font.color.rgb = SF["INK_60"]
        _set_letter_spacing(run, 80)
```

## Header & footer (page 2+)

The cover page itself gets no header/footer. Subsequent pages do — use Word's "different first page" setting.

```python
def add_running_header_footer(section, doc_title):
    section.different_first_page_header_footer = True

    header = section.header
    p = header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(f"SUMMER FRIDAYS   ·   {doc_title.upper()}")
    run.font.name = FONT
    run.font.size = Pt(8)
    run.font.color.rgb = SF["INK_60"]
    _set_letter_spacing(run, 120)
    _add_bottom_border(p, color="BDD7E5", width_pt=0.75)

    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.add_run("Summer Fridays  ·  Confidential")
    # Add tab to right side + page number
    _add_right_aligned_page_number(p)
    for r in p.runs:
        r.font.name = FONT
        r.font.size = Pt(8)
        r.font.color.rgb = SF["INK_60"]
```

## Document patterns by document type

### Marketing intelligence brief
1. Cover (MORNING_SKY accent)
2. Executive summary (lead paragraph + 3–5 bullets)
3. H1 + H2 sections per topic
4. Tables for any quantified comparison
5. Callouts for "growth hypothesis" boxes (use SKY tone)
6. Pull quote for the brand voice / founder reference
7. Sources section at end (numbered, with hyperlinks in ACCENT_BLUE)

### Campaign brief
1. Cover (PINK_SUGAR accent if lip campaign; VANILLA if fragrance; MORNING_SKY if skincare)
2. Objectives (3 bullets max)
3. Audience persona (table or rich bullets)
4. Channel + creative table
5. KPIs + measurement plan (table)
6. Callout: "What success looks like" (CLAY tone)
7. Timeline table

### Executive memo
1. No cover — header block instead: TO / FROM / DATE / SUBJECT
2. Lead recommendation in 13pt body lead
3. Supporting paragraphs in body
4. Callout for the decision point or ask
5. Optional appendix tables

## Helper utilities (the underscored functions referenced above)

These are the OOXML helpers you'll need — implement them once and reuse. Cribbed-and-adapted from python-docx community patterns:

```python
def _shade_cell(cell, hex_no_hash):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:fill'), hex_no_hash)
    tcPr.append(shd)

def _set_letter_spacing(font_or_run, twentieths_of_a_point):
    # 20 = 1pt; +1.2pt = 24
    rPr = font_or_run._element.get_or_add_rPr() if hasattr(font_or_run, '_element') else font_or_run.element.get_or_add_rPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:val'), str(twentieths_of_a_point))
    rPr.append(spacing)

def _add_bottom_border(paragraph, color, width_pt):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(int(width_pt * 8)))   # eighths of a point
    bottom.set(qn('w:color'), color)
    pBdr.append(bottom)
    pPr.append(pBdr)

def _add_left_border(paragraph, color, width_pt):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), str(int(width_pt * 8)))
    left.set(qn('w:color'), color)
    pBdr.append(left)
    pPr.append(pBdr)

def _set_cell_margins(cell, top, bottom, left, right):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for side, val in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        node = OxmlElement(f'w:{side}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)
```

## Final QA before delivering

- [ ] Cover page uses CHALK background or generous whitespace (no `#FFF` page color)
- [ ] All body copy is in the brand font with the fallback chain
- [ ] No Calibri, no Times New Roman anywhere
- [ ] Headings follow size hierarchy (no random `bold 14pt` paragraphs)
- [ ] Tables use MORNING_SKY headers with `CHALK` zebra striping
- [ ] Callouts use the four sanctioned tones (sky / vanilla / clay / pink), not random fills
- [ ] Hyperlinks render in ACCENT_BLUE (`#3C5A78`)
- [ ] Footer carries page number + "Summer Fridays" mark on every page from page 2
- [ ] Sources section at end with [Title](URL) format
- [ ] File saved to the project folder under a sensible path, then surfaced via present_files
