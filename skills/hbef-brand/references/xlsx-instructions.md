# HBEF Excel Workbook (.xlsx) Instructions

How to apply the HBEF brand system to Excel workbooks. Pair with the `xlsx` skill (which provides `openpyxl` mechanics) and `assets/brand-tokens.json`.

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
| 1 | (HBEF logo embedded, ~2" wide) | Image anchored A1 |
| 2 | (blank) | — |
| 3 | `HERMOSA BEACH EDUCATION FOUNDATION` | 10pt Montserrat 700 `INK_60` UPPERCASE |
| 4 | Workbook title | 24pt Montserrat 800 `HBEF_NAVY` |
| 5 | Subtitle | 14pt Montserrat 200 `HBEF_TEAL` |
| 6 | (blank — 3pt `HBEF_ORANGE` border-bottom on row 5) | — |
| 8 | `Author: [Name]` | 11pt Montserrat 400 `INK_60` |
| 9 | `Period: [e.g., Q1 2026]` | 11pt Montserrat 400 `INK_60` |
| 10 | `Generated: [Date]` | 11pt Montserrat 400 `INK_60` |
| 11 | `Classification: HBEF Board Working — Confidential` | 11pt Montserrat 400 italic `INK_60` |
| ... | (rest of sheet: empty, or contains a TOC) | — |

- Column A width: 30 (gives generous left margin)
- Hide gridlines on cover tab
- Sheet tab color: `HBEF_NAVY`

## Sheet tab colors

Tab colors signal sheet type at a glance:

| Sheet type | Tab color |
|---|---|
| Cover | `HBEF_NAVY` (`#0B4261`) |
| Summary / KPIs | `HBEF_ORANGE` (`#F79B32`) |
| Data (raw) | `HBEF_TEAL` (`#75C4B9`) |
| Notes / methodology | `INK_60` (`#5C5C5C`) |
| Internal / scratch | `HBEF_PAGE` (`#E7E7E7`) |

## Data sheet pattern

### Header rows (rows 1–2)

- **Row 1 (sheet title):** Merged A1:[last col]. Fill = `WHITE`. 18pt Montserrat 700 `HBEF_NAVY` UPPERCASE. Row height 36.
- **Row 2 (sheet subtitle):** Merged. Fill = `WHITE`. 11pt Montserrat 200 italic `INK_60`. Row height 24.

### Table header (row 4)

- Fill: `HBEF_NAVY` (`#0B4261`)
- Font: 11pt Montserrat 700 `WHITE` UPPERCASE
- Horizontal align: left for text columns, right for numeric columns, center for date columns
- Vertical align: center
- Border: all sides 1px `WHITE` (creates separation between header cells)
- Row height: 30
- Freeze panes: row 5 (so header stays visible on scroll)

### Data rows (row 5+)

- Default font: 10pt Montserrat 400 `INK`
- Text cells: left-aligned
- Numeric cells: right-aligned, number format `#,##0` or `$#,##0.00`
- Date cells: center-aligned, format `mmm d, yyyy`
- Percentage cells: right-aligned, format `0.0%`
- Zebra stripe: even rows fill = `SURFACE_ZEBRA` (`#FAFAFA`)
- Cell borders: bottom 0.5px `MUTED_BORDER` (`#CCCCCC`) — no internal vertical borders

### Total / summary row

- Fill: `SURFACE_TOTAL` / `HBEF_PAGE` (`#E7E7E7`)
- Font: 11pt Montserrat 700 `HBEF_NAVY`
- Top border: 1.5px `HBEF_NAVY`
- Bottom border: 1.5px `HBEF_NAVY` (double-border feel)

### Conditional formatting

- **Positive variance (good):** font color `SUCCESS` (`#5A9E78`)
- **Negative variance (bad):** font color `RISK` (`#B23A2D`)
- **At-or-near target (within ±2%):** font color `INK_60`
- **Heat-map for ranking data:** 3-color scale `RISK` → `WHITE` → `SUCCESS` (don't use rainbow)

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

- **Chart background:** `WHITE`
- **Plot area:** `WHITE`
- **Gridlines:** primary y-axis only, `MUTED_BORDER` (`#CCCCCC`) 0.5pt dashed
- **Axes:** `INK_60` 9pt Montserrat; remove top and right axis lines
- **Data labels:** 9pt Montserrat 400, color = same as data series, format `$#,##0` or `0.0%`
- **Title:** 14pt Montserrat 700 `HBEF_NAVY` UPPERCASE
- **Series colors:** in palette order:
  1. `HBEF_NAVY` (`#0B4261`)
  2. `HBEF_ORANGE` (`#F79B32`)
  3. `HBEF_TEAL` (`#75C4B9`)
  4. `HBEF_TEAL_MUTED` (`#417987`)
  5. `HBEF_NAVY_DEEP` (`#124362`)
  6. `INK_60` (`#5C5C5C`)
- **Legend:** bottom, 10pt Montserrat 400 `INK_60`, no border, no fill
- **Chart type defaults:** bar/column for comparison, line for trend, donut for share, scatter for correlation. **Never pie (use donut).** Never 3D.

## Investment Committee workbook addendum

For endowment/IC workbooks, additional conventions:

- **Numbers:** display in `$ Millions` (`$#,##0.0,, "M"`) for portfolio totals; `$ Thousands` (`$#,##0, "K"`) for sub-balances; raw `$#,##0.00` only for trade-level detail
- **Returns:** always display with sign and basis (e.g., `+1.2%` not `1.2%`)
- **Vs. benchmark column:** always show as `Difference` from benchmark — positive in `SUCCESS`, negative in `RISK`
- **Allocation tables:** show Target / Current / Difference columns explicitly, even when one is calculable
- **Time-series sheet:** date column A in `mmm yyyy` format, quarterly columns to the right, last row = trailing 12-month and trailing 3-year summary
- **Footnote sheet:** always include a tab named "Notes" with: data sources, custodian, benchmark composition, methodology for any computed values

## Annual Giving / fundraising workbook addendum

For donor-tracking and event workbooks:

- **Donor name column:** wide (28+), left-aligned
- **Gift amount column:** $-formatted, right-aligned
- **Tier column:** colored cell fill matching tier color (Brighter Benefactor = `HBEF_NAVY`, Diamond = `HBEF_ORANGE`, etc.) with white bold text
- **Payment status column:** conditional formatting — Received = `SUCCESS`, Pledged = `INK_60`, Past due = `RISK`
- **Always include a "Participation" column** showing whether the family donated, regardless of amount — HBEF's headline KPI is 100% participation, not just dollars

## `openpyxl` setup snippet

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment, NamedStyle
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image

# Brand colors (openpyxl uses ARGB hex without #)
HBEF_NAVY = "FF0B4261"
HBEF_ORANGE = "FFF79B32"
HBEF_TEAL = "FF75C4B9"
HBEF_TEAL_MUTED = "FF417987"
HBEF_NAVY_DEEP = "FF124362"
HBEF_PAGE = "FFE7E7E7"
SURFACE_ZEBRA = "FFFAFAFA"
SURFACE_SOFT = "FFF2F2F2"
MUTED_BORDER = "FFCCCCCC"
WHITE = "FFFFFFFF"
INK = "FF1A1A1A"
INK_60 = "FF5C5C5C"

wb = Workbook()

# Define named styles for reuse
header_style = NamedStyle(name="hbef_header")
header_style.font = Font(name="Montserrat", size=11, bold=True, color=WHITE)
header_style.fill = PatternFill("solid", fgColor=HBEF_NAVY)
header_style.alignment = Alignment(horizontal="left", vertical="center")
header_style.border = Border(
    bottom=Side(style="thin", color=MUTED_BORDER),
)
wb.add_named_style(header_style)

cell_style = NamedStyle(name="hbef_cell")
cell_style.font = Font(name="Montserrat", size=10, color=INK)
cell_style.alignment = Alignment(horizontal="left", vertical="center")
wb.add_named_style(cell_style)

total_style = NamedStyle(name="hbef_total")
total_style.font = Font(name="Montserrat", size=11, bold=True, color=HBEF_NAVY)
total_style.fill = PatternFill("solid", fgColor=HBEF_PAGE)
total_style.border = Border(
    top=Side(style="medium", color=HBEF_NAVY[2:]),
    bottom=Side(style="medium", color=HBEF_NAVY[2:]),
)
wb.add_named_style(total_style)
```

## Final checks (before sharing)

1. Cover tab present with logo, title, classification.
2. Every sheet has appropriate tab color.
3. Frozen panes set on data sheets (row 5).
4. Header rows fill = HBEF_NAVY, font = WHITE.
5. Total rows distinct fill (HBEF_PAGE).
6. Charts: brand palette, no 3D, axes cleaned up.
7. Notes tab with data sources and methodology.
8. Test print preview to ensure print layout works.
9. Sensitive data (donor PII, exact gift amounts) — verify whether the recipient should see it before sharing.
