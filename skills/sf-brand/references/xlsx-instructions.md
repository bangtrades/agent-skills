# SF-Brand × Excel Workbooks (.xlsx)

Use this with the **`xlsx` skill** when producing Excel workbooks for the Summer Fridays project. The `xlsx` skill provides file mechanics; this file specifies brand-correct styling.

## When this applies
Any spreadsheet deliverable for the SF project — performance dashboards, creator-campaign trackers, content calendars in tabular form, budget allocations, retailer SKU velocity tracking, financial models, KPI reporting, scenario analysis.

## Toolchain
- **Python:** `openpyxl` (canonical for styled xlsx)
- **Heavy formula/chart work:** `xlsxwriter` (write-only but richer charting)
- **Pandas → Excel:** use `df.to_excel(..., engine='openpyxl')` then apply styles in a second pass

## Brand tokens for Excel

```python
from openpyxl import Workbook
from openpyxl.styles import (
    PatternFill, Font, Alignment, Border, Side, NamedStyle
)

SF = {
    "INK":              "FF1A1A1A",   # ARGB format
    "INK_60":           "FF5C5C5C",
    "INK_30":           "FFA8A8A8",
    "CHALK":            "FFFAF6EF",
    "WHITE":            "FFFFFFFF",
    "MORNING_SKY":      "FFBDD7E5",
    "MORNING_SKY_DEEP": "FF7DA8BD",
    "CLAY":             "FFC9A582",
    "VANILLA":          "FFF5E9DD",
    "PINK_SUGAR":       "FFFC88AB",
    "PINK_GUAVA":       "FFB44F65",
    "HOT_COCOA":        "FF6B3D2E",
    "ACCENT_BLUE":      "FF3C5A78",
    "MUTED_BORDER":     "FFE5E5EB",
    "SUCCESS":          "FF7CA982",
    "RISK":             "FFA84544",
}

FONT = "Avenir Next"   # Futura PT fallback chain
```

## Named styles — define once, apply everywhere

```python
def register_sf_styles(wb):
    """Call once per workbook, then use named styles by name."""

    # Workbook title (merged cell at top of cover sheet)
    s = NamedStyle(name="sf_workbook_title")
    s.font = Font(name=FONT, size=18, color=SF["INK"], bold=False)
    s.alignment = Alignment(horizontal="left", vertical="center")
    s.fill = PatternFill("solid", fgColor=SF["CHALK"])
    wb.add_named_style(s)

    # Section header (separates blocks within a sheet)
    s = NamedStyle(name="sf_section_header")
    s.font = Font(name=FONT, size=12, color=SF["INK"], bold=False)
    s.fill = PatternFill("solid", fgColor=SF["MORNING_SKY"])
    s.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    s.border = thin_border(SF["MORNING_SKY_DEEP"], sides=("bottom",))
    wb.add_named_style(s)

    # Table header
    s = NamedStyle(name="sf_table_header")
    s.font = Font(name=FONT, size=10, color=SF["INK"], bold=False)
    s.fill = PatternFill("solid", fgColor=SF["MORNING_SKY"])
    s.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    s.border = thin_border(SF["MUTED_BORDER"])
    wb.add_named_style(s)

    # Body cell — text
    s = NamedStyle(name="sf_body")
    s.font = Font(name=FONT, size=9, color=SF["INK"])
    s.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    s.border = thin_border(SF["MUTED_BORDER"])
    wb.add_named_style(s)

    # Body cell — number (right-aligned, tabular)
    s = NamedStyle(name="sf_body_num")
    s.font = Font(name=FONT, size=9, color=SF["INK"])
    s.alignment = Alignment(horizontal="right", vertical="center")
    s.border = thin_border(SF["MUTED_BORDER"])
    s.number_format = "#,##0.00"
    wb.add_named_style(s)

    # Body cell — currency
    s = NamedStyle(name="sf_body_currency")
    s.font = Font(name=FONT, size=9, color=SF["INK"])
    s.alignment = Alignment(horizontal="right", vertical="center")
    s.border = thin_border(SF["MUTED_BORDER"])
    s.number_format = '_($* #,##0_);_($* (#,##0);_($* "-"_);_(@_)'
    wb.add_named_style(s)

    # Body cell — percent
    s = NamedStyle(name="sf_body_pct")
    s.font = Font(name=FONT, size=9, color=SF["INK"])
    s.alignment = Alignment(horizontal="right", vertical="center")
    s.border = thin_border(SF["MUTED_BORDER"])
    s.number_format = "0.0%"
    wb.add_named_style(s)

    # Zebra fill for alternating rows (apply on top of body style)
    s = NamedStyle(name="sf_body_zebra")
    s.font = Font(name=FONT, size=9, color=SF["INK"])
    s.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    s.fill = PatternFill("solid", fgColor=SF["CHALK"])
    s.border = thin_border(SF["MUTED_BORDER"])
    wb.add_named_style(s)

    # Total / summary row
    s = NamedStyle(name="sf_total")
    s.font = Font(name=FONT, size=10, color=SF["INK"], bold=True)
    s.fill = PatternFill("solid", fgColor=SF["VANILLA"])
    s.alignment = Alignment(horizontal="right", vertical="center")
    s.border = Border(
        top=Side(style="thin", color=SF["MORNING_SKY_DEEP"]),
        bottom=Side(style="medium", color=SF["MORNING_SKY_DEEP"]),
    )
    s.number_format = "#,##0"
    wb.add_named_style(s)

    # Footer / source note
    s = NamedStyle(name="sf_footer")
    s.font = Font(name=FONT, size=8, color=SF["INK_60"], italic=True)
    s.alignment = Alignment(horizontal="left", vertical="center")
    wb.add_named_style(s)

    # Risk flag
    s = NamedStyle(name="sf_risk")
    s.font = Font(name=FONT, size=9, color=SF["WHITE"], bold=False)
    s.fill = PatternFill("solid", fgColor=SF["RISK"])
    s.alignment = Alignment(horizontal="center", vertical="center")
    s.border = thin_border(SF["MUTED_BORDER"])
    wb.add_named_style(s)

    # Success flag
    s = NamedStyle(name="sf_success")
    s.font = Font(name=FONT, size=9, color=SF["WHITE"])
    s.fill = PatternFill("solid", fgColor=SF["SUCCESS"])
    s.alignment = Alignment(horizontal="center", vertical="center")
    s.border = thin_border(SF["MUTED_BORDER"])
    wb.add_named_style(s)


def thin_border(color, sides=("top", "bottom", "left", "right")):
    sd = {s: Side(style="thin", color=color) for s in sides}
    return Border(**{s: sd.get(s) for s in ("top", "bottom", "left", "right")})
```

## Cover sheet pattern

Every workbook gets a "Read Me" / cover tab as the first sheet.

```python
def add_cover_sheet(wb, title, subtitle, author, date,
                    sources=None, sheet_index=None):
    ws = wb.create_sheet("README", 0)
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 110

    # Column widths
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 90
    for row in range(1, 40):
        ws.row_dimensions[row].height = 22

    # Eyebrow
    ws["B2"] = "SUMMER FRIDAYS  ·  MARKETING INTELLIGENCE"
    ws["B2"].font = Font(name=FONT, size=10, color=SF["INK_60"])

    # Title (large, on chalk)
    ws.merge_cells("B5:G7")
    cell = ws["B5"]
    cell.value = title
    cell.style = "sf_workbook_title"
    cell.font = Font(name=FONT, size=24, color=SF["INK"])
    ws.row_dimensions[5].height = 30
    ws.row_dimensions[6].height = 30
    ws.row_dimensions[7].height = 30

    # Subtitle
    ws["B9"] = subtitle
    ws["B9"].font = Font(name=FONT, size=14, color=SF["INK_60"], italic=True)

    # Morning-sky accent rule (using a row with bg fill)
    for col in ("B", "C", "D"):
        ws[f"{col}11"].fill = PatternFill("solid", fgColor=SF["MORNING_SKY"])
    ws.row_dimensions[11].height = 4

    # Meta block
    ws["B13"] = "Author"
    ws["B13"].font = Font(name=FONT, size=9, color=SF["INK_60"], bold=True)
    ws["B14"] = author
    ws["B14"].font = Font(name=FONT, size=10, color=SF["INK"])

    ws["B16"] = "Date"
    ws["B16"].font = Font(name=FONT, size=9, color=SF["INK_60"], bold=True)
    ws["B17"] = date
    ws["B17"].font = Font(name=FONT, size=10, color=SF["INK"])

    ws["B19"] = "Classification"
    ws["B19"].font = Font(name=FONT, size=9, color=SF["INK_60"], bold=True)
    ws["B20"] = "Confidential — Internal Working Document"
    ws["B20"].font = Font(name=FONT, size=10, color=SF["INK"])

    # Sheet index
    if sheet_index:
        ws["B23"] = "What's in this workbook"
        ws["B23"].font = Font(name=FONT, size=11, color=SF["INK"], bold=True)
        for i, (name, desc) in enumerate(sheet_index, start=25):
            ws[f"B{i}"] = f"{name}"
            ws[f"B{i}"].font = Font(name=FONT, size=10, color=SF["ACCENT_BLUE"], bold=True)
            ws[f"C{i}"] = desc
            ws[f"C{i}"].font = Font(name=FONT, size=9, color=SF["INK_60"])

    # Sources
    if sources:
        start = 25 + (len(sheet_index) if sheet_index else 0) + 3
        ws[f"B{start}"] = "Sources"
        ws[f"B{start}"].font = Font(name=FONT, size=11, color=SF["INK"], bold=True)
        for i, src in enumerate(sources, start=start+2):
            ws[f"B{i}"] = src
            ws[f"B{i}"].font = Font(name=FONT, size=9, color=SF["ACCENT_BLUE"], italic=True)

    # Background fill for the whole visible area — CHALK
    for row in ws.iter_rows(min_row=1, max_row=50, min_col=1, max_col=12):
        for cell in row:
            if not cell.fill.fgColor.value or cell.fill.fgColor.value == "00000000":
                cell.fill = PatternFill("solid", fgColor=SF["CHALK"])
```

## Data sheet pattern

```python
def add_data_sheet(wb, sheet_name, headers, rows, totals_row=None,
                   freeze_panes="A2", widths=None):
    ws = wb.create_sheet(sheet_name)
    ws.sheet_view.showGridLines = False

    # Column widths
    if widths:
        for col_letter, width in widths.items():
            ws.column_dimensions[col_letter].width = width

    # Headers
    for col_idx, label in enumerate(headers, start=1):
        cell = ws.cell(row=1, column=col_idx, value=label)
        cell.style = "sf_table_header"
    ws.row_dimensions[1].height = 28

    # Body rows
    for r_idx, row in enumerate(rows, start=2):
        zebra = r_idx % 2 == 0
        for c_idx, val in enumerate(row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            if isinstance(val, (int, float)) and c_idx > 1:
                cell.style = "sf_body_num"
                if zebra:
                    cell.fill = PatternFill("solid", fgColor=SF["CHALK"])
            else:
                cell.style = "sf_body_zebra" if zebra else "sf_body"
        ws.row_dimensions[r_idx].height = 20

    # Totals row
    if totals_row:
        r = len(rows) + 2
        for c_idx, val in enumerate(totals_row, start=1):
            cell = ws.cell(row=r, column=c_idx, value=val)
            cell.style = "sf_total"
        ws.row_dimensions[r].height = 24

    # Freeze
    ws.freeze_panes = freeze_panes
```

## Charts

When embedding charts in xlsx, use the brand palette via explicit series fills. `xlsxwriter` is more chart-flexible than `openpyxl`.

```python
# xlsxwriter example
chart = workbook.add_chart({"type": "column"})
chart.add_series({
    "name":       "=Sheet1!$B$1",
    "categories": "=Sheet1!$A$2:$A$13",
    "values":     "=Sheet1!$B$2:$B$13",
    "fill":       {"color": "#7DA8BD"},   # MORNING_SKY_DEEP
    "border":     {"none": True},
})
chart.set_title({"name": "Title", "name_font": {"name": "Avenir Next", "size": 12, "color": "#1A1A1A", "bold": False}})
chart.set_x_axis({"line": {"color": "#E5E5EB"}, "num_font": {"name": "Avenir Next", "size": 9, "color": "#5C5C5C"}})
chart.set_y_axis({"line": {"none": True}, "major_gridlines": {"line": {"color": "#E5E5EB"}}, "num_font": {"name": "Avenir Next", "size": 9, "color": "#5C5C5C"}})
chart.set_legend({"position": "bottom", "font": {"name": "Avenir Next", "size": 9, "color": "#5C5C5C"}})
chart.set_chartarea({"fill": {"color": "#FAF6EF"}, "border": {"none": True}})
chart.set_plotarea({"fill": {"color": "#FFFFFF"}, "border": {"color": "#E5E5EB"}})
```

**Series color order for multi-series charts:**
```python
SF_CHART_COLORS = ["#7DA8BD", "#C9A582", "#B44F65", "#6B3D2E", "#A4C089", "#5C5C5C"]
```

## Conditional formatting — brand-correct

For positive/negative variance, opportunity scoring, etc:

```python
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule

# Positive variance — chalk → success
rule = ColorScaleRule(
    start_type='min', start_color="FAF6EF",
    end_type='max',   end_color="7CA982",
)
ws.conditional_formatting.add("D2:D100", rule)

# Risk flagging — anything above threshold
rule = CellIsRule(operator="greaterThan", formula=["0.5"],
                  fill=PatternFill("solid", fgColor=SF["RISK"]),
                  font=Font(name=FONT, size=9, color=SF["WHITE"]))
ws.conditional_formatting.add("E2:E100", rule)
```

## Workbook patterns by deliverable type

### Performance dashboard
1. README cover sheet with sheet index
2. KPI sheet — single column of big numbers (use merged cells, large fonts, MORNING_SKY_DEEP for the metric values)
3. One sheet per channel (IG, TikTok, YouTube, Email, SMS, Amazon, Sephora)
4. Trend charts embedded on each channel sheet
5. Notes sheet with assumptions, source URLs, and last-refresh date

### Creator campaign tracker
1. README cover
2. Roster sheet (creator handle, tier, market, rate, status — with success/risk conditional formatting)
3. Performance sheet (one row per post — date, platform, views, engagement, EMV, code, attributed sales)
4. Pivot summary (rolled up by tier × market)
5. Charts: spend vs. EMV scatter, performance by tier bar, market split donut

### Budget / financial model
1. README cover with scenario summary
2. Inputs sheet (yellow-fill cells for editable inputs, INK_60 for derived)
3. Calculations sheet (formulas, formatted with sf_body_num / sf_body_currency)
4. Outputs sheet (totals + variance + chart embeds)
5. Scenario comparison sheet (lean / moderate / aggressive columns side-by-side)

## Final QA before delivering

- [ ] README cover sheet exists and is sheet #1
- [ ] No gridlines visible on any sheet (`sheet_view.showGridLines = False`)
- [ ] Default font is Avenir Next on every cell (no Calibri leaking through)
- [ ] Headers in MORNING_SKY, totals in VANILLA, alternating CHALK on body
- [ ] All numbers right-aligned with appropriate number_format
- [ ] Currency uses brand-correct format string (parentheses for negatives, dash for zero)
- [ ] Charts have transparent/CHALK background, brand color series
- [ ] Conditional formatting uses SF success/risk palette, not Excel red/green default
- [ ] Freeze panes at A2 (or A3 if header is two rows)
- [ ] Last sheet is "Sources & Notes" with citation URLs and refresh date
