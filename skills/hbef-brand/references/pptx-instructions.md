# HBEF PowerPoint (.pptx) Instructions

How to apply the HBEF brand system to PowerPoint decks. Pair with the `pptx` skill (which provides `python-pptx` mechanics) and `assets/brand-tokens.json`.

## Slide setup

- **Layout:** 16:9 (13.333" × 7.5", or 10" × 5.625" for compact decks)
- **Default font:** Montserrat (specify on every text frame)
- **Background:** `WHITE` (default) — never pure black, never gradient
- **Slide accent:** every content slide has a 0.05" `HBEF_NAVY` top accent bar (see below)

## Slide types

HBEF decks should use these six slide types:

1. **Title (cover) slide** — opens the deck
2. **Section divider** — between major sections
3. **Content slide** — the workhorse, 1–2 columns of body
4. **Stat slide** — single large number with context
5. **Quote / pull-out slide** — testimonial or signature phrase
6. **Closing / ask slide** — CTA, contact info, tax language

### 1. Title (cover) slide

```
[HBEF_NAVY band: top 30% of slide, full-bleed]
  [HBEF lockup, white-on-navy version, centered, 4" wide]

[White background: lower 70%]
  [Eyebrow, 14pt Montserrat 700 INK_60 UPPERCASE +1.5pt]
  HERMOSA BEACH EDUCATION FOUNDATION
  
  [Title, 60pt Montserrat 800 or BauhausBold, HBEF_NAVY, UPPER, +2pt]
  THE DECK TITLE
  
  [Subtitle, 22pt Montserrat 200 light, HBEF_TEAL, sentence case]
  A short descriptive subtitle
  
  [HBEF_ORANGE rule, 3pt, 2" wide, centered]
  
  [Metadata, 12pt Montserrat 400 INK_60]
  [Author] · [Date] · [Classification]

[HBEF_TEAL bottom band, 0.3" tall, full-bleed]
```

### 2. Section divider

```
[Full-bleed HBEF_NAVY background]
  [Eyebrow, 12pt Montserrat 700 WHITE @ 60% opacity UPPERCASE +1.2pt]
  PART 02
  
  [Section title, 44pt Montserrat 700 WHITE UPPERCASE +1pt]
  SECTION TITLE
  
  [HBEF_ORANGE rule, 4pt, 3" wide, left-aligned with title]
```

Accent color rotation across sections: `HBEF_ORANGE` → `HBEF_TEAL` → `HBEF_TEAL_MUTED` → `HBEF_NAVY_DEEP`, then loop.

### 3. Content slide

```
[Top accent bar: 0.05" tall, full-bleed HBEF_NAVY at y=0]

[Title, 28pt Montserrat 700 HBEF_NAVY UPPERCASE +0.8pt]
SLIDE TITLE

[Subtitle, 14pt Montserrat 400 INK_60 sentence case]
Optional context line beneath the title

[Body area — single column at 0.7" left margin, or 2-column split at 0.7" + 7" left]
  16pt Montserrat 400 INK body
  · 14pt Montserrat 400 bullets
  · Use chevron-arrows (›) or right-pointing markers, not round bullets

[Footer bar at y=7.2": 0.3" tall HBEF_PAGE (#E7E7E7) fill]
  Left: 9pt Montserrat 400 INK_60 — "Hermosa Beach Education Foundation"
  Right: 9pt Montserrat 700 HBEF_NAVY — slide number
```

### 4. Stat slide

```
[Top accent bar, HBEF_NAVY]

[Eyebrow, 12pt Montserrat 700 INK_60 UPPERCASE]
THE HEADLINE METRIC

[Massive number, 120pt Montserrat 200 light HBEF_NAVY or HBEF_ORANGE]
$1,265,000

[Caption, 18pt Montserrat 400 INK_60 sentence case]
contributed to HBCSD for the 2024–25 school year

[Optional supporting bullets, 12pt Montserrat 400 INK]
```

For HBEF, the killer stat slides use the brand's signature thin-200-weight type at 100pt+. The contrast between the tall, airy number and the small caption is the HBEF visual signature.

### 5. Quote / pull-out slide

```
[White background, generous whitespace]

[Quote, 32pt Montserrat 400 italic HBEF_NAVY, line-height 1.3, centered, max 80% width]
"Funding matters. Your donation, their future."

[HBEF_TEAL rule, 3pt, 1" wide, centered]

[Attribution, 14pt Montserrat 700 INK_60 UPPERCASE +1pt]
HBEF MISSION TAGLINE
```

### 6. Closing / ask slide

```
[HBEF_NAVY half (left), WHITE half (right)]

[Left half, white text on navy]
  [HBEF lockup, 3" wide, centered in left half]
  
[Right half, white background]
  [Title, 36pt Montserrat 700 HBEF_NAVY UPPERCASE]
  JOIN US
  
  [CTA card — HBEF_ORANGE button-style rectangle]
  [Inside button: 16pt Montserrat 700 WHITE UPPERCASE +2pt]
  DONATE NOW · hbef.org/donate-now
  
  [Contact block, 11pt Montserrat 400 INK_60]
  admin@hbef.org · hbef.org · @hbef90254
  
  [Tax footer, 8pt Montserrat 400 italic INK_60]
  HBEF is a registered 501(c)(3). EIN: 33-0522270.
```

## Color usage per slide

- **One brand color carries the slide.** Pick the slide's accent (navy/orange/teal) based on content domain — financials = navy, donations/CTA = orange, community/events = teal. Use it consistently on that slide's title underline, accent bar, and any callout.
- **Backgrounds:** WHITE for content; HBEF_NAVY for section dividers and cover band; HBEF_TEAL for "community moment" full-bleed slides (sparing — max 1–2 per deck).
- **Charts:** follow chart palette from `SKILL.md` — `HBEF_NAVY` → `HBEF_ORANGE` → `HBEF_TEAL` → `HBEF_TEAL_MUTED` → `HBEF_NAVY_DEEP` → `INK_60`.
- **Hyperlinks / URLs on slides:** `HBEF_ORANGE`, no underline (PowerPoint default underlines are ugly).

## Component patterns

### Tier card (for sponsor prospectus decks)

Six cards in a 3×2 or 2×3 grid, one per sponsor tier:

- Card background: `WHITE`
- Top accent bar: 0.05" full-width, color rotates per tier:
  - Brighter Benefactor: `HBEF_NAVY`
  - Diamond: `HBEF_ORANGE`
  - Platinum: `HBEF_TEAL_MUTED`
  - Gold: `HBEF_TEAL`
  - Silver: `INK_60`
  - Bronze: `INK_30`
- Card content:
  - Tier name: 18pt Montserrat 700 HBEF_NAVY UPPERCASE
  - $ threshold: 12pt Montserrat 200 light INK_60
  - 3 benefits: 11pt Montserrat 400 INK
- Drop shadow: subtle, blur 8, opacity 0.15

### Stat card (3-up KPI strip)

Three cards side-by-side, each 1/3 slide width:

- Card background: `WHITE` with 1pt `MUTED_BORDER` outline
- Top accent bar: 0.05" `HBEF_NAVY` (or color domain)
- Big number: 48pt Montserrat 200 light, color = card's accent
- Label: 11pt Montserrat 700 INK_60 UPPERCASE +1pt

### Funding-gap explainer chart

The "where the money comes from" story is core to the HBEF deck repertoire. Recommended:

- **Donut chart** showing HBCSD revenue sources (state LCFF, federal, local, HBEF, other)
- HBEF slice: `HBEF_ORANGE` — pulled out 5% from center for emphasis
- All other slices: monochrome navy palette (`HBEF_NAVY`, `HBEF_NAVY_DEEP`, `HBEF_TEAL_MUTED`, `INK_60`)
- Center label: "HBEF funds 5% of the budget"

## `python-pptx` setup snippet

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Brand colors
HBEF_NAVY = RGBColor(0x0B, 0x42, 0x61)
HBEF_ORANGE = RGBColor(0xF7, 0x9B, 0x32)
HBEF_TEAL = RGBColor(0x75, 0xC4, 0xB9)
HBEF_TEAL_MUTED = RGBColor(0x41, 0x79, 0x87)
INK = RGBColor(0x1A, 0x1A, 0x1A)
INK_60 = RGBColor(0x5C, 0x5C, 0x5C)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
HBEF_PAGE = RGBColor(0xE7, 0xE7, 0xE7)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Blank layout
blank = prs.slide_layouts[6]

def add_accent_bar(slide, color=HBEF_NAVY, y=0, height=Inches(0.05)):
    bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, 0, y, prs.slide_width, height
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    return bar

def set_text(tf, text, size=Pt(16), bold=False, color=INK, font="Montserrat"):
    tf.text = text
    p = tf.paragraphs[0]
    run = p.runs[0]
    run.font.name = font
    run.font.size = size
    run.font.bold = bold
    run.font.color.rgb = color
```

## Final checks (before sharing)

1. Cover loaded with HBEF lockup; title in correct case and tracking.
2. Every content slide has an accent bar at top.
3. Section dividers placed between major content sections.
4. At least one stat slide and one quote slide for visual rhythm.
5. Closing/ask slide with donate URL, contact, tax language.
6. Slide numbers visible.
7. Fonts: Montserrat throughout (verify in Slide Master).
8. No pure black text — use `INK` (`#1A1A1A`).
9. Charts: palette in correct order; no 3D.
10. Export to PDF for distribution and verify rendering.
