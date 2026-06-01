# SF-Brand × PowerPoint Decks (.pptx)

Use this with the **`pptx` skill** when producing PowerPoint decks for the Summer Fridays project. The `pptx` skill provides the file-construction code patterns; this file specifies the brand-correct visual system.

## When this applies
Any presentation for the SF project — campaign decks, partnership pitch decks, performance reviews, board updates, internal kickoffs, creator strategy decks.

## Toolchain
- **Python:** `python-pptx` (canonical, widely supported)
- **Alternative:** `pptxgenjs` (Node, used when generating from a JS pipeline)

## Slide setup

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)   # 16:9
prs.slide_height = Inches(7.5)
```

## Brand color helper

```python
SF = {
    "INK":              RGBColor(0x1A, 0x1A, 0x1A),
    "INK_60":           RGBColor(0x5C, 0x5C, 0x5C),
    "INK_30":           RGBColor(0xA8, 0xA8, 0xA8),
    "CHALK":            RGBColor(0xFA, 0xF6, 0xEF),
    "WHITE":            RGBColor(0xFF, 0xFF, 0xFF),
    "MORNING_SKY":      RGBColor(0xBD, 0xD7, 0xE5),
    "MORNING_SKY_DEEP": RGBColor(0x7D, 0xA8, 0xBD),
    "CLAY":             RGBColor(0xC9, 0xA5, 0x82),
    "VANILLA":          RGBColor(0xF5, 0xE9, 0xDD),
    "PINK_SUGAR":       RGBColor(0xFC, 0x88, 0xAB),
    "PINK_GUAVA":       RGBColor(0xB4, 0x4F, 0x65),
    "HOT_COCOA":        RGBColor(0x6B, 0x3D, 0x2E),
    "ACCENT_BLUE":      RGBColor(0x3C, 0x5A, 0x78),
}

FONT = "Avenir Next"     # Futura PT fallback
FONT_DISPLAY = "Cormorant Garamond"
```

## Slide background helper

```python
def set_slide_bg(slide, color=SF["CHALK"]):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color
```

**Every slide defaults to `CHALK` background.** Pure white is only for inset cards. Dark slides (HOT_COCOA, ESPRESSO) are reserved for a single dramatic divider in long decks.

## Cover slide

```python
def add_cover_slide(prs, title, subtitle, author, date,
                    eyebrow="SUMMER FRIDAYS  ·  MARKETING INTELLIGENCE",
                    accent=SF["MORNING_SKY"]):
    slide = prs.slides.add_slide(prs.slide_layouts[6])   # blank
    set_slide_bg(slide, SF["CHALK"])

    # Eyebrow (top-left, ~0.6" from top, 0.7" from left)
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(0.5), Inches(8), Inches(0.3))
    tf = tb.text_frame
    tf.margin_left = 0
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = eyebrow
    run.font.name = FONT
    run.font.size = Pt(11)
    run.font.color.rgb = SF["INK_60"]
    # NOTE: python-pptx has no letter-spacing API — set via XML or accept default

    # Title (centered low-mid, large)
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(2.6), Inches(12), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.name = FONT
    run.font.size = Pt(60)
    run.font.color.rgb = SF["INK"]
    run.font.bold = False

    # Subtitle (Cormorant italic)
    if subtitle:
        tb = slide.shapes.add_textbox(Inches(0.7), Inches(4.2), Inches(12), Inches(0.6))
        tf = tb.text_frame
        p = tf.paragraphs[0]
        run = p.add_run()
        run.text = subtitle
        run.font.name = FONT_DISPLAY
        run.font.size = Pt(22)
        run.font.italic = True
        run.font.color.rgb = SF["INK_60"]

    # Morning-sky accent line (1.5" wide, 2pt tall, centered horizontally below subtitle)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(5.1), Inches(1.5), Pt(2.5))
    line.fill.solid()
    line.fill.fore_color.rgb = accent
    line.line.fill.background()   # no outline

    # Footer (bottom-left)
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(7), Inches(12), Inches(0.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = f"{author}   ·   {date}   ·   Confidential — Internal Working Document"
    run.font.name = FONT
    run.font.size = Pt(10)
    run.font.color.rgb = SF["INK_60"]

    return slide
```

## Section divider slide

```python
def add_section_divider(prs, eyebrow, title, accent=SF["MORNING_SKY"]):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, SF["CHALK"])

    # Eyebrow
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(3.0), Inches(12), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = eyebrow.upper()
    run.font.name = FONT
    run.font.size = Pt(12)
    run.font.color.rgb = SF["INK_60"]

    # Title
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(3.5), Inches(12), Inches(1.5))
    p = tb.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.name = FONT
    run.font.size = Pt(44)
    run.font.color.rgb = SF["INK"]

    # Accent rule below title — 100% width, thin
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  Inches(0.7), Inches(5.0), Inches(12), Pt(1))
    rule.fill.solid(); rule.fill.fore_color.rgb = accent
    rule.line.fill.background()

    return slide
```

**Color rotation for dividers** in long decks: MORNING_SKY → CLAY → VANILLA → MORNING_SKY_DEEP → MORNING_SKY (loop).

## Content slide layout — the universal grid

Every content slide:
- **Title** at `(x=0.7", y=0.45")`, width 12", 28pt INK
- **Subtitle / dek** at `(x=0.7", y=1.05")`, width 12", 14pt INK_60
- **Thin rule** at `(x=0.7", y=1.55")`, width 1.2", 0.75pt MORNING_SKY
- **Content area** from `y=1.85"` to `y=6.8"`
- **Footer** at `(x=0.7", y=7.05")` to `(x=12.6", y=7.3")`

```python
def add_content_slide(prs, title, subtitle=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, SF["CHALK"])

    # Title
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(0.45), Inches(12), Inches(0.6))
    p = tb.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.name = FONT
    run.font.size = Pt(28)
    run.font.color.rgb = SF["INK"]

    # Subtitle
    if subtitle:
        tb = slide.shapes.add_textbox(Inches(0.7), Inches(1.05), Inches(12), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = subtitle
        run.font.name = FONT
        run.font.size = Pt(14)
        run.font.color.rgb = SF["INK_60"]

    # Thin morning-sky rule
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  Inches(0.7), Inches(1.55), Inches(1.2), Pt(0.75))
    rule.fill.solid(); rule.fill.fore_color.rgb = SF["MORNING_SKY"]
    rule.line.fill.background()

    add_footer(slide, prs)
    return slide

def add_footer(slide, prs, page_num=None):
    tb = slide.shapes.add_textbox(Inches(0.7), Inches(7.05), Inches(12), Inches(0.25))
    p = tb.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = "Summer Fridays  ·  Confidential"
    run.font.name = FONT
    run.font.size = Pt(9)
    run.font.color.rgb = SF["INK_60"]
```

## Card component

The fundamental SF content block is a `WHITE` or `VANILLA` rectangle on the `CHALK` background, with a thin `MORNING_SKY` top rule.

```python
def add_card(slide, x, y, w, h, title, body, accent=SF["MORNING_SKY"], fill=SF["WHITE"]):
    # Card body
    card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    card.fill.solid(); card.fill.fore_color.rgb = fill
    card.line.color.rgb = SF["INK_30"]
    card.line.width = Pt(0.5)
    # No shadow — SF aesthetic is flat, not floating

    # Top accent rule
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, Pt(2.5))
    rule.fill.solid(); rule.fill.fore_color.rgb = accent
    rule.line.fill.background()

    # Title
    tb = slide.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), w - Inches(0.5), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    run = p.add_run()
    run.text = title
    run.font.name = FONT
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = SF["INK"]

    # Body
    tb = slide.shapes.add_textbox(x + Inches(0.25), y + Inches(0.7), w - Inches(0.5), h - Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = body
    run.font.name = FONT
    run.font.size = Pt(12)
    run.font.color.rgb = SF["INK"]
```

## Stat callout (big number)

For "10.5%" or "$244M" moments. The brand voice supports precise numbers — they earn the spotlight.

```python
def add_stat_callout(slide, x, y, w, big_number, label, accent=SF["MORNING_SKY_DEEP"]):
    # Big number
    tb = slide.shapes.add_textbox(x, y, w, Inches(1.2))
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = big_number
    run.font.name = FONT
    run.font.size = Pt(56)
    run.font.color.rgb = accent
    run.font.bold = False

    # Label below
    tb = slide.shapes.add_textbox(x, y + Inches(1.25), w, Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = label.upper()
    run.font.name = FONT
    run.font.size = Pt(11)
    run.font.color.rgb = SF["INK_60"]
```

## Chart slide

When embedding a chart on a slide, use the brand chart palette (see SKILL.md). Set the chart background to transparent so the slide CHALK shows through; never let matplotlib/Excel chart white "stick out."

```python
# Example: matplotlib chart saved to PNG, then inserted
import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.family": "Avenir Next",
    "axes.facecolor": "#FAF6EF",
    "figure.facecolor": "#FAF6EF",
    "axes.edgecolor":  "#E5E5EB",
    "axes.labelcolor": "#5C5C5C",
    "xtick.color":     "#5C5C5C",
    "ytick.color":     "#5C5C5C",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})
SF_CHART_COLORS = ["#7DA8BD", "#C9A582", "#B44F65", "#6B3D2E", "#A4C089", "#5C5C5C"]
```

Then insert the PNG with `slide.shapes.add_picture(path, x, y, w, h)`.

## Deck patterns by deck type

### Strategy / intelligence deck
1. Cover (MORNING_SKY accent)
2. "What you'll see" agenda (5 bullets max)
3. Section divider — Context
4. 3–5 content slides on market context
5. Section divider — Opportunity (CLAY accent)
6. 3–5 content slides on the opportunity
7. Section divider — Recommendation (PINK_SUGAR if lip topic; MORNING_SKY otherwise)
8. 2–4 recommendation slides with stat callouts
9. Closing thank-you slide

### Partnership pitch deck (e.g., airline x Jet Lag)
1. Cover (CLAY accent for travel/lifestyle)
2. SF in 60 seconds (one slide, 3 stat callouts: $244M / 10.5% Sephora / 1 every 17 sec LBB)
3. The partner in 60 seconds
4. Why now — cultural moment / data
5. The big idea (one slide, large type, minimal)
6. Activation plan (3-card layout)
7. Brand fit + audience overlap
8. KPIs + measurement
9. Timeline
10. Ask + next step

### Campaign retro / performance deck
1. Cover (matching the campaign's accent)
2. TL;DR — single slide with 3 stat callouts
3. What we set out to do
4. What happened (chart-heavy slides)
5. What worked
6. What didn't
7. So what now (recommendations)

## Final QA before delivering

- [ ] Every slide background is CHALK (or sanctioned dark accent for divider)
- [ ] Pure WHITE never appears as a full-slide background
- [ ] Title 28pt, subtitle 14pt, thin MORNING_SKY rule — every content slide
- [ ] Cards use INK_30 hairline border, no shadows
- [ ] Charts use brand palette (no rainbow defaults from matplotlib)
- [ ] Stat callouts use MORNING_SKY_DEEP for general; PINK_GUAVA for lip; CLAY for fragrance
- [ ] Footer "Summer Fridays · Confidential" on every content slide
- [ ] No Calibri (PPT default), no Comic Sans, no Times
- [ ] Section dividers rotate accent color in the sanctioned sequence
