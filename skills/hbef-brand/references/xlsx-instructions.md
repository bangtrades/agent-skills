# HBEF Excel Workbook (.xlsx) Instructions

How to apply the HBEF **2026** brand system to Excel workbooks. Pair with the `xlsx` skill (which provides `openpyxl` mechanics) and `assets/brand-tokens.json`.

> **Type rule for spreadsheets:** **Aleo Bold** is used only for the sheet title in row 1 and for oversized stat/KPI numbers. **Everything else is Lato** — section headers, sub-headers, data cells, totals, notes, chart axes, chart legends. Never set a whole table in Aleo; the slab serif is a display face.

## Workbook architecture

A standard HBEF spreadsheet has at least these tabs:

1. **Cover** — workbook title, scope, author, date, classification
2. **Summary** — KPI strip + a chart or two
3. **Data sheets** — the actual tables (one per topic)
4. **Notes** — methodology, definitions, sources, data refresh dates

For Investment Committee workbooks, additional standard tabs:
- **Portfolio Holdings**
- **Allocation vs Target**
- **Performance vs Benchmark**
- **Quarterly Returns Time-Series**

## Cover tab

Layout:

| Row | Content | Style |
|---|---|---|
| 1 | (HBEF logo embedded, ~2" wide) | Image anchored A1 — `assets/logos/HBEF-Secondary_Lockup-RGB@2x.png` |
| 2 | (blank) | — |
| 3 | `HERMOSA BEACH EDUCATION FOUNDATION` | 9pt Lato Bold `HBEF_WET_SAND` (`#98989A`) UPPERCASE |
| 4 | Workbook title | 16pt **Aleo** Bold `HBEF_NAVY` (`#0C3B5D`) |
| 5 | Subtitle | 11pt Lato Regular `HBEF_TEAL` (`#186892`) |
| 6 | (blank — 3pt `HBEF_VIEW` `#FFCD00` border-bottom on row 5) | — |
| 8 | `Author: [Name]` | 10pt Lato Regular `HBEF_ASPHALT` (`#515962`) |
| 9 | `Period: [e.g., Q1 2026]` | 10pt Lato Regular `HBEF_ASPHALT` |
| 10 | `Generated: [Date]` | 10pt Lato Regular `HBEF_ASPHALT` |
| 11 | `Classification: HBEF Board Working — Confidential` | 9pt Lato Italic `HBEF_WET_SAND` |
| ... | (rest of sheet: empty, or contains a TOC) | — |

- Column A width: 30 (gives generous left margin)
- Hide gridlines on cover tab (`ws.sheet_view.showGridLines = False`)
- Sheet tab color: `HBEF_NAVY` (`#0C3B5D`)
- Logo is the **light** (standard-color) lockup because the cover sheet background is White. Only use `HBEF-Secondary_Lockup-Dark_Mode-RGB@2x.png` if you fill the header rows with Navy or Teal.
- For a donor-facing workbook, add the mandatory tax line at the bottom of the cover in 8pt Lato Italic `HBEF_WET_SAND`:
  *"HBEF is a registered 501(c)(3) non-profit organization. Contributions are tax-deductible to the extent allowed by law. Federal tax identification number (EIN): 33-0522270"*

## Sheet tab colors

Tab colors signal sheet type at a glance:

| Sheet type | Tab color |
|---|---|
| Cover | `HBEF_NAVY` (`#0C3B5D`) |
| Summary / KPIs | `HBEF_VIEW` (`#FFCD00`) |
| Data (raw) | `HBEF_TEAL` (`#186892`) |
| Charts / dashboard | `HBEF_TURQUOISE` (`#129FDA`) |
| Notes / methodology | `HBEF_WET_SAND` (`#98989A`) |
| Internal / scratch | `HBEF_SKY` (`#B8D8EB`) |

Never tab-color with Valley `#EE7623` — reserve Valley for attention accents inside the sheets (variance flags, the headline chart series) so it keeps its signal value.

## Data sheet pattern

### Header rows (rows 1–2)

- **Row 1 (sheet title):** Merged A1:[last col]. Fill = `WHITE` (`#FFFFFF`). **16pt Aleo Bold `HBEF_NAVY`.** Title case — do **not** uppercase Aleo and do not letterspace it; the slab serif carries the emphasis on its own. Row height 34.
- **Row 2 (sheet subtitle):** Merged. Fill = `WHITE`. 9pt Lato Italic `HBEF_WET_SAND`. Row height 22.
- **Row 3:** spacer, height 8, no fill.

### Section header (banner row inside a long sheet)

- Fill: `HBEF_NAVY` (`#0C3B5D`)
- Font: **12pt Lato Bold `WHITE`** UPPERCASE, letter-spacing is not available in Excel — use a single space between letters only if the label is 3 words or fewer, otherwise leave it plain
- Row height: 26

### Sub-header (grouping row beneath a section header)

- Fill: `HBEF_SKY` (`#B8D8EB`)
- Font: **11pt Lato Bold `HBEF_NAVY`**
- Row height: 22
- Use for column-group spanners ("Q1", "Q2", "FY Total") and for sub-totals that are not the grand total.

### Table header (row 4)

- Fill: `HBEF_NAVY` (`#0C3B5D`)
- Font: **12pt Lato Bold `WHITE`** UPPERCASE
- Horizontal align: left for text columns, right for numeric columns, center for date columns
- Vertical align: center
- Border: all sides 1px `WHITE` (creates separation between header cells)
- Row height: 30
- Freeze panes: row 5 (so header stays visible on scroll)
- Wide tables that need a second header tier: put the tier-1 spanner in `HBEF_SKY` sub-header style and the tier-2 column labels in the Navy table-header style directly beneath it.

### Data rows (row 5+)

- Default font: **10pt Lato Regular `HBEF_ASPHALT` (`#515962`)** — body copy is Asphalt, never black
- Text cells: left-aligned
- Numeric cells: right-aligned, number format `#,##0` or `$#,##0.00`
- Date cells: center-aligned, format `mmm d, yyyy`
- Percentage cells: right-aligned, format `0.0%`
- Zebra stripe: even rows fill = `SURFACE_ZEBRA` (`#F7FAFC`)
- Cell borders: bottom 0.5px `MUTED_BORDER` (`#D9D9D9`) — no internal vertical borders
- Cell notes / inline annotations inside a data block: **9pt Lato Italic `HBEF_WET_SAND` on `WHITE`**

### Total / summary row

- Fill: `SURFACE_TOTAL` (`#E8F1F7`) — the pale Sky tint, **not** Sky itself; Sky `#B8D8EB` belongs to sub-headers
- Font: **11pt Lato Bold `HBEF_NAVY`**
- Top border: 1.5px `HBEF_NAVY`
- Bottom border: 1.5px `HBEF_NAVY` (double-border feel)

### Conditional formatting

- **Positive variance (good):** font color `SUCCESS` (`#4A8B5C`)
- **Negative variance (bad):** font color `RISK` (`#B23A2D`)
- **At-or-near target (within ±2%):** font color `HBEF_WET_SAND` (`#98989A`)
- **Attention flag (needs a human to look, not necessarily bad):** font color `HBEF_VALLEY` (`#EE7623`) bold
- **Heat-map for ranking data:** 3-color scale `RISK` `#B23A2D` → `WHITE` `#FFFFFF` → `SUCCESS` `#4A8B5C` (don't use rainbow)
- **Data bars:** `HBEF_TEAL` (`#186892`) solid fill, no gradient, no border
- Never conditional-format with Yellow `#FFCD00` as a *text* color — it fails contrast. Use it as a **fill** with `HBEF_NAVY` bold text on top when you need a highlighted cell.

## Column widths

- Identifier / ID columns: 12
- Short label columns (name, category): 24
- Date columns: 14
- Currency columns: 14
- Percent columns: 12
- Long-text / notes columns: 40+

Use `worksheet.column_dimensions['A'].width = 24` in openpyxl.

## Chart styling (embedded in workbook)

When inserting Excel charts:

- **Chart background:** `WHITE` (`#FFFFFF`)
- **Plot area:** `WHITE`
- **Gridlines:** primary y-axis only, `MUTED_BORDER` (`#D9D9D9`) 0.5pt dashed
- **Axes:** `HBEF_WET_SAND` (`#98989A`) 9pt **Lato**; remove top and right axis lines (open frame)
- **Data labels:** 9pt Lato Regular, color = same as data series, format `$#,##0` or `0.0%`
- **Title:** **12pt Lato Bold `HBEF_NAVY`** UPPERCASE — or, for a hero chart on a dashboard tab, 16pt **Aleo** Bold `HBEF_NAVY` in title case
- **Series colors:** in palette order:
  1. `HBEF_NAVY` (`#0C3B5D`)
  2. `HBEF_VALLEY` (`#EE7623`)
  3. `HBEF_TEAL` (`#186892`)
  4. `HBEF_VISTA` (`#FFA400`)
  5. `HBEF_TURQUOISE` (`#129FDA`)
  6. `HBEF_WET_SAND` (`#98989A`)
- **Single-series charts:** `HBEF_NAVY` for financials / endowment / IC reporting · `HBEF_VALLEY` for fundraising, donor and participation metrics · `HBEF_TEAL` for community, program and student-impact metrics
- **Benchmark / target lines:** dashed, `HBEF_WET_SAND` (`#98989A`), 1pt
- **Legend:** bottom, 10pt Lato Regular `HBEF_WET_SAND`, no border, no fill
- **Chart type defaults:** bar/column for comparison, line for trend, donut for share, scatter for correlation. **Never pie (use donut).** Never 3D, no shadows, no gradients.

## KPI strip (Summary tab)

Three to five merged blocks across the top of the Summary tab, each 3 rows tall:

| Row in block | Content | Style |
|---|---|---|
| Label | `2024–25 GRANT` | 9pt Lato Bold `HBEF_WET_SAND` UPPERCASE, centered |
| Value | `$1,265,000` | **16pt Aleo Bold `HBEF_NAVY`**, centered — this is the one place a big number gets Aleo |
| Caption | `Contributed to HBCSD` | 9pt Lato Italic `HBEF_WET_SAND`, centered |

- Block fill `WHITE`, with a 3pt top border in the deliverable's accent color (`HBEF_VIEW` for donor-facing, `HBEF_VALLEY` for events, `HBEF_TEAL` for IC/TAB, `HBEF_NAVY` for governance) and a 0.5pt `MUTED_BORDER` outline on the other three sides.
- Leave one empty narrow column (width 2) between blocks as the gutter.

## Investment Committee workbook addendum

For endowment/IC workbooks, additional conventions:

- **Numbers:** display in `$ Millions` (`$#,##0.0,, "M"`) for portfolio totals; `$ Thousands` (`$#,##0, "K"`) for sub-balances; raw `$#,##0.00` only for trade-level detail
- **Returns:** always display with sign and basis (e.g., `+1.2%` not `1.2%`)
- **Vs. benchmark column:** always show as `Difference` from benchmark — positive in `SUCCESS` (`#4A8B5C`), negative in `RISK` (`#B23A2D`)
- **Allocation tables:** show Target / Current / Difference columns explicitly, even when one is calculable
- **Time-series sheet:** date column A in `mmm yyyy` format, quarterly columns to the right, last row = trailing 12-month and trailing 3-year summary
- **Accent color for IC workbooks is Teal `#186892`** — KPI top borders, data bars, chart single-series accents. Keep View yellow out of IC material; it reads as a donor CTA.
- **Footnote sheet:** always include a tab named "Notes" with: data sources, custodian, benchmark composition, methodology for any computed values
- IC workbooks drop the parent voice entirely — peer-level internal authorship, no donor framing.

## Technology Advisory Board workbook addendum

- Same Teal `#186892` accent as IC.
- Typical tabs: **Tool Inventory**, **Cost & Renewal**, **Data Hygiene**, **Vendor Evaluation**, **Notes**.
- Vendor-evaluation scoring: score cells 1–5 with the `RISK → WHITE → SUCCESS` 3-color scale; never a rainbow scale.
- Renewal-date column: conditional format < 60 days out in `HBEF_VALLEY` (`#EE7623`) bold.
- No donor register, no parent-audience preamble.

## Annual Giving / fundraising workbook addendum

For donor-tracking and event workbooks:

- **Donor name column:** wide (28+), left-aligned
- **Gift amount column:** $-formatted, right-aligned
- **Tier column:** colored cell fill matching the tier, 10pt Lato Bold. Tier names are exact — don't rename or merge:

  | Tier | Threshold | Fill | Text color |
  |---|---|---|---|
  | Brighter Benefactor | $25K+ | `HBEF_NAVY` `#0C3B5D` | `WHITE` |
  | Diamond | $15K+ | `HBEF_TEAL` `#186892` | `WHITE` |
  | Platinum | $10K+ | `HBEF_TURQUOISE` `#129FDA` | `WHITE` |
  | Gold | $6K+ | `HBEF_VISTA` `#FFA400` | `HBEF_NAVY` |
  | Silver | $3.5K+ | `HBEF_WET_SAND` `#98989A` | `WHITE` |
  | Bronze | $1.5K+ | `HBEF_VALLEY` `#EE7623` | `WHITE` |

- **Payment status column:** conditional formatting — Received = `SUCCESS` (`#4A8B5C`), Pledged = `HBEF_WET_SAND` (`#98989A`), Past due = `RISK` (`#B23A2D`)
- **Always include a "Participation" column** showing whether the family donated, regardless of amount — HBEF's headline KPI is 100% participation, not just dollars
- Accent color for donor-facing workbooks is **View `#FFCD00`** (KPI top borders, highlighted cells with Navy text)

## `openpyxl` setup snippet

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, NamedStyle
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image

# ---- HBEF 2026 brand colors (openpyxl uses ARGB hex, no leading '#') ----
HBEF_NAVY      = "FF0C3B5D"
HBEF_TEAL      = "FF186892"
HBEF_TURQUOISE = "FF129FDA"
HBEF_VIEW      = "FFFFCD00"
HBEF_VISTA     = "FFFFA400"
HBEF_VALLEY    = "FFEE7623"
HBEF_SKY       = "FFB8D8EB"
HBEF_SAND      = "FFDDC9A3"
HBEF_WET_SAND  = "FF98989A"
HBEF_ASPHALT   = "FF515962"
WHITE          = "FFFFFFFF"

# Surfaces & functional
SURFACE_ZEBRA  = "FFF7FAFC"   # alternating data rows
SURFACE_TOTAL  = "FFE8F1F7"   # total-row fill
MUTED_BORDER   = "FFD9D9D9"
SUCCESS        = "FF4A8B5C"
WARNING        = "FFFFA400"   # reuses Vista
RISK           = "FFB23A2D"

# Chart series, in required order
CHART_SERIES = [HBEF_NAVY, HBEF_VALLEY, HBEF_TEAL, HBEF_VISTA, HBEF_TURQUOISE, HBEF_WET_SAND]

# ---- Fonts: Aleo for the sheet title / hero stat only, Lato for everything else ----
HEADING_FONT = "Aleo"
BODY_FONT    = "Lato"

wb = Workbook()

# Sheet title (row 1) — the only Aleo in a normal data sheet
title_style = NamedStyle(name="hbef_sheet_title")
title_style.font = Font(name=HEADING_FONT, size=16, bold=True, color=HBEF_NAVY)
title_style.fill = PatternFill("solid", fgColor=WHITE)
title_style.alignment = Alignment(horizontal="left", vertical="center")
wb.add_named_style(title_style)

# Section header — Lato 12 Bold, white on Navy
section_style = NamedStyle(name="hbef_section")
section_style.font = Font(name=BODY_FONT, size=12, bold=True, color=WHITE)
section_style.fill = PatternFill("solid", fgColor=HBEF_NAVY)
section_style.alignment = Alignment(horizontal="left", vertical="center")
wb.add_named_style(section_style)

# Table header — same Lato 12 Bold on Navy, with white separators
header_style = NamedStyle(name="hbef_header")
header_style.font = Font(name=BODY_FONT, size=12, bold=True, color=WHITE)
header_style.fill = PatternFill("solid", fgColor=HBEF_NAVY)
header_style.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
header_style.border = Border(
    left=Side(style="thin", color=WHITE),
    right=Side(style="thin", color=WHITE),
    bottom=Side(style="thin", color=WHITE),
)
wb.add_named_style(header_style)

# Sub-header — Lato 11 Bold, Navy on Sky
subheader_style = NamedStyle(name="hbef_subheader")
subheader_style.font = Font(name=BODY_FONT, size=11, bold=True, color=HBEF_NAVY)
subheader_style.fill = PatternFill("solid", fgColor=HBEF_SKY)
subheader_style.alignment = Alignment(horizontal="left", vertical="center")
wb.add_named_style(subheader_style)

# Data cell — Lato 10 Regular, Asphalt on White
cell_style = NamedStyle(name="hbef_cell")
cell_style.font = Font(name=BODY_FONT, size=10, color=HBEF_ASPHALT)
cell_style.fill = PatternFill("solid", fgColor=WHITE)
cell_style.alignment = Alignment(horizontal="left", vertical="center")
cell_style.border = Border(bottom=Side(style="hair", color=MUTED_BORDER))
wb.add_named_style(cell_style)

# Zebra variant of the data cell
zebra_style = NamedStyle(name="hbef_cell_zebra")
zebra_style.font = Font(name=BODY_FONT, size=10, color=HBEF_ASPHALT)
zebra_style.fill = PatternFill("solid", fgColor=SURFACE_ZEBRA)
zebra_style.alignment = Alignment(horizontal="left", vertical="center")
zebra_style.border = Border(bottom=Side(style="hair", color=MUTED_BORDER))
wb.add_named_style(zebra_style)

# Total row — Lato 11 Bold, Navy on pale Sky tint, navy rules top and bottom
total_style = NamedStyle(name="hbef_total")
total_style.font = Font(name=BODY_FONT, size=11, bold=True, color=HBEF_NAVY)
total_style.fill = PatternFill("solid", fgColor=SURFACE_TOTAL)
total_style.border = Border(
    top=Side(style="medium", color=HBEF_NAVY),
    bottom=Side(style="medium", color=HBEF_NAVY),
)
wb.add_named_style(total_style)

# Cell note — Lato 9 Italic, Wet Sand on White
note_style = NamedStyle(name="hbef_note")
note_style.font = Font(name=BODY_FONT, size=9, italic=True, color=HBEF_WET_SAND)
note_style.fill = PatternFill("solid", fgColor=WHITE)
note_style.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
wb.add_named_style(note_style)
```

### Applying a data sheet

```python
ws = wb.active
ws.title = "Annual Giving"
ws.sheet_properties.tabColor = HBEF_TEAL[2:]      # tabColor takes RGB, not ARGB
ws.sheet_view.showGridLines = False

# Row 1 — sheet title (Aleo 16 Bold Navy)
ws.merge_cells("A1:F1")
ws["A1"] = "Annual Giving 2025–26"
ws["A1"].style = "hbef_sheet_title"
ws.row_dimensions[1].height = 34

# Row 2 — subtitle (Lato 9 Italic Wet Sand)
ws.merge_cells("A2:F2")
ws["A2"] = "Family-level pledges and payments · refreshed nightly"
ws["A2"].style = "hbef_note"
ws.row_dimensions[2].height = 22

# Row 4 — table header
headers = ["Family", "School", "Pledge", "Received", "Status", "Participation"]
for i, h in enumerate(headers, start=1):
    c = ws.cell(row=4, column=i, value=h.upper())
    c.style = "hbef_header"
    if h in ("Pledge", "Received"):
        c.alignment = Alignment(horizontal="right", vertical="center")
ws.row_dimensions[4].height = 30
ws.freeze_panes = "A5"

# Rows 5+ — data with zebra striping
for r, row in enumerate(rows, start=5):
    style = "hbef_cell_zebra" if r % 2 == 0 else "hbef_cell"
    for i, v in enumerate(row, start=1):
        c = ws.cell(row=r, column=i, value=v)
        c.style = style
        if i in (3, 4):
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '$#,##0'

# Column widths
for col, w in zip("ABCDEF", [28, 16, 14, 14, 14, 14]):
    ws.column_dimensions[col].width = w
```

### Conditional formatting

```python
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule, DataBarRule

# Positive / negative variance
ws.conditional_formatting.add(
    "G5:G200",
    CellIsRule(operator="greaterThan", formula=["0"],
               font=Font(name=BODY_FONT, size=10, bold=True, color=SUCCESS)),
)
ws.conditional_formatting.add(
    "G5:G200",
    CellIsRule(operator="lessThan", formula=["0"],
               font=Font(name=BODY_FONT, size=10, bold=True, color=RISK)),
)

# Ranking heat map — Risk → White → Success (never rainbow)
ws.conditional_formatting.add(
    "H5:H200",
    ColorScaleRule(
        start_type="min",  start_color=RISK[2:],
        mid_type="percentile", mid_value=50, mid_color="FFFFFF",
        end_type="max",    end_color=SUCCESS[2:],
    ),
)

# Data bars in Teal, flat fill
ws.conditional_formatting.add(
    "I5:I200",
    DataBarRule(start_type="num", start_value=0, end_type="max",
                color=HBEF_TEAL[2:], showValue=True, minLength=None, maxLength=None),
)
```

### Chart styling

```python
from openpyxl.chart import BarChart, Reference, Series
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText
from openpyxl.drawing.text import (
    RichTextProperties, Paragraph, ParagraphProperties, CharacterProperties
)
from openpyxl.drawing.line import LineProperties

chart = BarChart()
chart.type = "col"
chart.style = None                      # kill Excel's built-in theme styling
chart.title = "ANNUAL GIVING BY SCHOOL"
chart.gapWidth = 60
chart.overlap = -10

data = Reference(ws, min_col=3, min_row=4, max_col=5, max_row=40)
cats = Reference(ws, min_col=1, min_row=5, max_row=40)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

# Series colors in HBEF palette order
for series, color in zip(chart.series, CHART_SERIES):
    series.graphicalProperties = GraphicalProperties(solidFill=color[2:])
    series.graphicalProperties.line.noFill = True

# Axis text: Lato 9pt Wet Sand
axis_txt = RichText(
    bodyPr=RichTextProperties(),
    p=[Paragraph(pPr=ParagraphProperties(
        defRPr=CharacterProperties(latin="Lato", sz=900, solidFill=HBEF_WET_SAND[2:])
    ))],
)
chart.x_axis.txPr = axis_txt
chart.y_axis.txPr = axis_txt

# Open frame: no top/right axis lines, faint dashed y gridlines only
chart.x_axis.majorGridlines = None
chart.y_axis.majorGridlines.spPr = GraphicalProperties(
    ln=LineProperties(solidFill=MUTED_BORDER[2:], w=6350, prstDash="dash")
)
chart.x_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill=MUTED_BORDER[2:]))
chart.y_axis.spPr = GraphicalProperties(ln=LineProperties(noFill=True))

chart.legend.position = "b"
chart.legend.overlay = False

ws.add_chart(chart, "H4")
```

### Placing the logo on the cover tab

```python
from openpyxl.drawing.image import Image

cover = wb.create_sheet("Cover", 0)
cover.sheet_properties.tabColor = HBEF_NAVY[2:]
cover.sheet_view.showGridLines = False
cover.column_dimensions["A"].width = 30

logo = Image("assets/logos/HBEF-Secondary_Lockup-RGB@2x.png")
logo.width, logo.height = 288, 72        # ~2" wide at 144 dpi; scale proportionally only
cover.add_image(logo, "A1")
```

## Font availability note

Excel does **not** embed fonts. If the recipient does not have Aleo and Lato installed, Excel substitutes — Aleo falls to a serif, Lato to a sans, and the workbook still reads correctly because the fallback chains are `Aleo → Roboto Slab → Zilla Slab → Rockwell → Georgia → serif` and `Lato → Helvetica Neue → Helvetica → Arial → sans-serif`.

- Both families are SIL OFL and free from Google Fonts; the TTFs are bundled in `assets/fonts/`. Recommend recipients install them once.
- When a workbook is going to an unknown recipient and typographic fidelity matters, **export a PDF alongside it** (see `references/pdf-instructions.md`) — PDFs embed both faces.
- Never substitute Montserrat or BauhausBold. Those are retired.

## Final checks (before sharing)

1. Cover tab present with logo, Aleo title, classification, and (if donor-facing) the EIN line.
2. Every sheet has an appropriate tab color from the table above.
3. Frozen panes set on data sheets (row 5).
4. Header rows fill = `HBEF_NAVY` `#0C3B5D`, font = Lato 12 Bold `WHITE`.
5. Sub-headers on `HBEF_SKY` `#B8D8EB`; total rows on `#E8F1F7` with Navy rules.
6. Body cells are Lato 10 `HBEF_ASPHALT` `#515962` — no black text, no Montserrat.
7. Zebra fill is `#F7FAFC`, borders `#D9D9D9`.
8. Charts: series in Navy → Valley → Teal → Vista → Turquoise → Wet Sand order, Lato axes, no 3D, no pie, axes cleaned up.
9. Notes tab with data sources, definitions, and refresh dates.
10. Test print preview to ensure print layout works.
11. Sensitive data (donor PII, exact gift amounts) — verify whether the recipient should see it before sharing.
12. Grep the finished file for retired values: no `Montserrat`, no `BauhausBold`, no `0B4261`, `124362`, `F79B32`, `75C4B9`, `74C4B9`, `417987`, `FAEF7A`, `E7E7E7`, `1A1A1A`, `5C5C5C`, `CCCCCC`.
