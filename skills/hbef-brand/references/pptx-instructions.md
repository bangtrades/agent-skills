# HBEF PowerPoint (.pptx) Instructions

How to apply the **HBEF 2026 brand system** to PowerPoint decks. Pair with the `pptx` skill (which provides `python-pptx` mechanics) and `assets/brand-tokens.json`.

> **Rebrand note.** Everything below is the 2026 system: **Aleo** (titles, dividers, display, stats) + **Lato** (body, bullets, labels, footers), Navy `#0C3B5D`, Teal `#186892`, Turquoise `#129FDA`, View `#FFCD00`, Valley `#EE7623`. Montserrat, BauhausBold, `#0B4261`, `#F79B32`, `#75C4B9`, `#417987`, `#E7E7E7`, and the `INK*` tokens are retired. If you are updating an old HBEF deck, replace them — don't leave a single legacy slide in the file.

## Fonts — bundled and embeddable

Both families are **SIL Open Font License 1.1** and ship in this skill:

- `assets/fonts/Aleo-{Regular,Bold,Italic,BoldItalic}.ttf` — slide titles, dividers, cover titles, stats, pull quotes
- `assets/fonts/Lato-{Light,Regular,Italic,Bold,BoldItalic,Black}.ttf` — body, bullets, labels, captions, footers
- Licenses: `assets/fonts/Aleo-OFL.txt`, `assets/fonts/Lato-OFL.txt`

Because they are OFL you may **install them on the build machine and embed them in the .pptx**, which the pre-2026 system could not legally do with its proprietary display face. Embed via *File → Options → Save → Embed fonts in the file* (choose "Embed all characters" for decks others will edit). `python-pptx` cannot embed fonts itself, so either (a) build on a machine with Aleo and Lato installed and re-save from PowerPoint with embedding on, or (b) export a PDF for distribution.

**Fallbacks:** Aleo → `Aleo, "Roboto Slab", "Zilla Slab", Rockwell, Georgia, serif` (**always a slab or serif, never a sans**). Lato → `Lato, "Helvetica Neue", Helvetica, Arial, sans-serif`.

## Slide setup

- **Layout:** 16:9 (13.333" × 7.5", or 10" × 5.625" for compact decks)
- **Default fonts:** **Aleo** for titles/display, **Lato** for everything else — set on every text frame, and in the Slide Master
- **Background:** `WHITE` (default) — never pure black, never gradient
- **Body color:** `HBEF_ASPHALT` `#515962` — never pure black, never `#1A1A1A`
- **Slide accent:** every content slide has a 0.05" `HBEF_NAVY` top accent bar (see below)

### Type scale (exact — do not invent sizes)

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Cover title | Aleo | 54pt | Bold | `HBEF_NAVY` on White, or `WHITE` on `HBEF_NAVY` |
| Cover subtitle | Lato | 20pt | Light (300) | `HBEF_TEAL` (or `HBEF_SKY` on navy) |
| Section divider title | Aleo | 40pt | Bold | `WHITE` on `HBEF_NAVY` fill |
| Slide title | Aleo | 28pt | Bold | `HBEF_NAVY` |
| Slide subtitle | Lato | 14pt | Regular | `HBEF_WET_SAND` |
| Body / bullet | Lato | 16pt / 14pt | Regular | `HBEF_ASPHALT` |
| Pull-out stat | Aleo | 60pt | Bold | `HBEF_NAVY` or `HBEF_VALLEY` |
| Stat label | Lato | 11pt | Regular | `HBEF_WET_SAND` |
| Footer | Lato | 9pt | Regular | `HBEF_WET_SAND` |

Everything else on a slide reuses a value from this scale — eyebrows and card labels take **11pt** (the stat-label size), pull quotes take **28pt** (the slide-title size), secondary card headings take **16pt** (the body size). Do not introduce a size that isn't in this table.

**Aleo is never uppercased and never letterspaced.** Its slab serifs collapse when tracked out. Caps and tracking belong to the Lato-set elements only — eyebrows, labels, footers, button text.

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
[HBEF_NAVY (#0C3B5D) band: top 30% of slide, full-bleed]
  [assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png, centered, 4" wide]

[White background: lower 70%]
  [Eyebrow, 11pt Lato Bold HBEF_WET_SAND UPPERCASE +1.2pt]
  HERMOSA BEACH EDUCATION FOUNDATION

  [Title, 54pt Aleo Bold, HBEF_NAVY, sentence or title case, no tracking]
  The Deck Title

  [Subtitle, 20pt Lato Light, HBEF_TEAL, sentence case]
  A short descriptive subtitle

  [HBEF_VIEW (#FFCD00) rule, 3pt, 2" wide, centered]

  [Metadata, 11pt Lato HBEF_WET_SAND]
  [Author] · [Date] · [Classification]

[HBEF_VIEW (#FFCD00) bottom band, 0.3" tall, full-bleed]
```

Rotate the cover rule + bottom band per deliverable type, matching the cover-page pattern in SKILL.md: donor-facing → `HBEF_VIEW`; event promo/recap → `HBEF_VALLEY`; IC / endowment / TAB → `HBEF_TEAL`; board governance → `HBEF_NAVY`.

Always use the **Dark Mode** lockup on the navy band. Never place the standard-color logo on a dark fill.

### 2. Section divider

```
[Full-bleed HBEF_NAVY (#0C3B5D) background]
  [Eyebrow, 11pt Lato Bold HBEF_SKY UPPERCASE +1.2pt]
  PART 02

  [Section title, 40pt Aleo Bold WHITE, sentence or title case]
  Section Title

  [Accent rule, 4pt, 3" wide, left-aligned with title]
```

Use `HBEF_SKY` `#B8D8EB` for the eyebrow on navy rather than white-at-60%-opacity — the 2026 system uses real tints, not transparency.

Accent color rotation across sections: `HBEF_VIEW` → `HBEF_TEAL` → `HBEF_VALLEY` → `HBEF_TURQUOISE`, then loop.

### 3. Content slide

```
[Top accent bar: 0.05" tall, full-bleed HBEF_NAVY at y=0]

[Title, 28pt Aleo Bold HBEF_NAVY, sentence or title case]
Slide Title

[Subtitle, 14pt Lato HBEF_WET_SAND sentence case]
Optional context line beneath the title

[Body area — single column at 0.7" left margin, or 2-column split at 0.7" + 7" left]
  16pt Lato HBEF_ASPHALT body
  · 14pt Lato HBEF_ASPHALT bullets
  · Use chevron-arrows (›) or right-pointing markers, not round bullets

[Footer bar at y=7.2": 0.3" tall HBEF_SKY (#B8D8EB) fill]
  Left: 9pt Lato HBEF_ASPHALT — "Hermosa Beach Education Foundation · hbef.org"
  Right: 9pt Lato Bold HBEF_NAVY — slide number
```

The footer bar is `HBEF_SKY`, not gray. On Sky, drop footer type to `HBEF_ASPHALT` so it stays legible; `HBEF_WET_SAND` is the footer color when the footer sits directly on white.

### 4. Stat slide

```
[Top accent bar, HBEF_NAVY]

[Eyebrow, 11pt Lato Bold HBEF_WET_SAND UPPERCASE +1.2pt]
THE HEADLINE METRIC

[Pull-out stat, 60pt Aleo Bold HBEF_NAVY (or HBEF_VALLEY for donor/fundraising metrics)]
$1,265,000

[Stat label / caption, 11pt Lato HBEF_WET_SAND sentence case]
contributed to HBCSD for the 2024–25 school year

[Optional supporting bullets, 14pt Lato HBEF_ASPHALT]
```

The 2026 stat treatment is **weight contrast, not weight absence**: a heavy Aleo Bold number against a small, quiet Lato label, with a lot of white space around it. (The pre-2026 signature was a 120pt hairline sans — that look is retired along with Montserrat. Do not simulate it by stretching Aleo Regular.) Give the number generous margins; the airiness now comes from the whitespace, not the stroke.

Single-series accent by domain: `HBEF_NAVY` for financials / endowment / IC · `HBEF_VALLEY` for fundraising, donor and participation numbers · `HBEF_TEAL` for community, program and student-impact numbers.

### 5. Quote / pull-out slide

```
[White background, generous whitespace]

[Quote, 28pt Aleo Italic HBEF_NAVY, line-height 1.3, centered, max 80% width]
"Funding matters. Your donation, their future."

[HBEF_VIEW (#FFCD00) rule, 3pt, 1" wide, centered]

[Attribution, 11pt Lato Bold HBEF_WET_SAND UPPERCASE +1pt]
HBEF MISSION TAGLINE
```

For a testimonial on a color field, invert: `HBEF_NAVY` full-bleed background, quote in `WHITE` Aleo Italic, rule in `HBEF_VIEW`, attribution in `HBEF_SKY`.

### 6. Closing / ask slide

```
[HBEF_NAVY half (left), WHITE half (right)]

[Left half, navy]
  [assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png, 3" wide, centered]

[Right half, white background]
  [Title, 40pt Aleo Bold HBEF_NAVY, sentence or title case]
  Join us

  [CTA card — HBEF_VIEW (#FFCD00) button-style rectangle]
  [Inside button: 16pt Lato Bold HBEF_NAVY UPPERCASE +2pt]
  DONATE NOW · hbef.org/donate-now

  [Contact block, 11pt Lato HBEF_ASPHALT]
  admin@hbef.org · hbef.org · @hbef90254

  [Tax footer, 9pt Lato Italic HBEF_WET_SAND]
  HBEF is a registered 501(c)(3) non-profit organization. Contributions are
  tax-deductible to the extent allowed by law. Federal tax identification
  number (EIN): 33-0522270
```

**Button text on `HBEF_VIEW` must be `HBEF_NAVY`, not white.** Yellow-and-white fails contrast badly. If the CTA has to shout harder than View can, switch the button fill to `HBEF_VALLEY` `#EE7623` with `WHITE` text — but only one CTA color per deck.

The full tax sentence is mandatory on any donor-facing deck. Don't abbreviate it to "EIN: 33-0522270" on a solicitation.

## Color usage per slide

- **One brand color carries the slide.** Pick the slide's accent by content domain — financials/endowment = `HBEF_NAVY`, donations/CTA = `HBEF_VIEW`, fundraising urgency = `HBEF_VALLEY`, community/events/programs = `HBEF_TEAL`. Use it consistently on that slide's title underline, accent bar, and any callout.
- **Backgrounds:** `WHITE` for content; `HBEF_NAVY` for section dividers and the cover band; `HBEF_SKY` `#B8D8EB` for tinted "breather" slides and footer bars; `HBEF_TEAL` `#186892` for full-bleed "community moment" slides (sparing — max 1–2 per deck). `HBEF_SAND` `#DDC9A3` is the warm alternate to Sky; pick one per deck, don't alternate them.
- **Charts:** follow the chart palette from `SKILL.md` — `HBEF_NAVY` → `HBEF_VALLEY` → `HBEF_TEAL` → `HBEF_VISTA` → `HBEF_TURQUOISE` → `HBEF_WET_SAND`.
- **Hyperlinks / URLs on slides:** `HBEF_TURQUOISE` `#129FDA`, no underline (PowerPoint's default underline is ugly).
- **Teal and Turquoise are not interchangeable.** Teal is structural (bars, rules, headers); Turquoise is graphic and energetic (icons, links, wave motifs).
- **Never:** pure black type, neon, gradients across brand colors, drop shadows on text, 3D, or any hex not in `assets/brand-tokens.json`.

## Component patterns

### Tier card (for sponsor prospectus decks)

Six cards in a 3×2 or 2×3 grid, one per sponsor tier. **Tier names are exact — don't rename or merge them.**

- Card background: `WHITE`, 1pt `MUTED_BORDER` `#D9D9D9` outline
- Top accent bar: 0.05" full-width, color per tier:

  | Tier | Threshold | Accent |
  |---|---|---|
  | Brighter Benefactor | $25K+ | `HBEF_NAVY` `#0C3B5D` |
  | Diamond | $15K+ | `HBEF_TURQUOISE` `#129FDA` |
  | Platinum | $10K+ | `HBEF_TEAL` `#186892` |
  | Gold | $6K+ | `HBEF_VIEW` `#FFCD00` |
  | Silver | $3.5K+ | `HBEF_WET_SAND` `#98989A` |
  | Bronze | $1.5K+ | `HBEF_VALLEY` `#EE7623` |

- Card content:
  - Tier name: 16pt Aleo Bold `HBEF_NAVY` (sentence/title case)
  - $ threshold: 14pt Lato `HBEF_WET_SAND`
  - 3 benefits: 11pt Lato `HBEF_ASPHALT`
- **No drop shadow.** Use the 1pt `MUTED_BORDER` outline instead — the 2026 system is flat.

### Stat card (3-up KPI strip)

Three cards side-by-side, each 1/3 slide width:

- Card background: `WHITE` with 1pt `MUTED_BORDER` `#D9D9D9` outline (or `HBEF_SKY` fill with no outline)
- Top accent bar: 0.05" `HBEF_NAVY` (or the slide's domain color)
- Big number: 40pt Aleo Bold, color = the card's accent
- Label: 11pt Lato Bold `HBEF_WET_SAND` UPPERCASE +1pt

### Funding-gap explainer chart

The "where the money comes from" story is core to the HBEF deck repertoire. Recommended:

- **Donut chart** showing HBCSD revenue sources (state LCFF, federal, local, HBEF, other)
- HBEF slice: `HBEF_VALLEY` `#EE7623` — pulled out 5% from center for emphasis
- All other slices: the cool structural palette (`HBEF_NAVY`, `HBEF_TEAL`, `HBEF_TURQUOISE`, `HBEF_WET_SAND`)
- Center label: "HBEF funds 5% of the budget" — 16pt Lato Bold `HBEF_NAVY`
- Gridlines/axes elsewhere in the deck: `MUTED_BORDER` `#D9D9D9` at 0.75pt; axis labels 9pt Lato `HBEF_WET_SAND`; no top or right axis lines
- No 3D, no shadows, no rainbow gradients, no pie chart with more than 5 slices

### Logo placement quick reference

| Placement | File |
|---|---|
| Cover navy band, closing navy half | `assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png` |
| White or Sky slide, stacked space | `assets/logos/HBEF-Primary_Lockup-RGB@2x.png` |
| White or Sky slide, wide short space (footer, header strip) | `assets/logos/HBEF-Secondary_Lockup-RGB@2x.png` |
| Navy or Teal band, wide short space | `assets/logos/HBEF-Secondary_Lockup-Dark_Mode-RGB@2x.png` |
| Corner mark, < 1.25" wide | `assets/logos/HBEF-Logomark.png` |

Clear space = the height of the "HBEF" lettering on all four sides. Lockups ≥ 1.25" wide; Logomark ≥ 0.4". Never stretch, rotate, recolor, or reconstruct the mark.

## `python-pptx` setup snippet

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

# --- HBEF 2026 brand colors -------------------------------------------
HBEF_NAVY      = RGBColor(0x0C, 0x3B, 0x5D)   # #0C3B5D
HBEF_TEAL      = RGBColor(0x18, 0x68, 0x92)   # #186892
HBEF_TURQUOISE = RGBColor(0x12, 0x9F, 0xDA)   # #129FDA
HBEF_VIEW      = RGBColor(0xFF, 0xCD, 0x00)   # #FFCD00  CTA / highlight
HBEF_VISTA     = RGBColor(0xFF, 0xA4, 0x00)   # #FFA400
HBEF_VALLEY    = RGBColor(0xEE, 0x76, 0x23)   # #EE7623
HBEF_SKY       = RGBColor(0xB8, 0xD8, 0xEB)   # #B8D8EB
HBEF_SAND      = RGBColor(0xDD, 0xC9, 0xA3)   # #DDC9A3
HBEF_WET_SAND  = RGBColor(0x98, 0x98, 0x9A)   # #98989A
HBEF_ASPHALT   = RGBColor(0x51, 0x59, 0x62)   # #515962  body copy
WHITE          = RGBColor(0xFF, 0xFF, 0xFF)
MUTED_BORDER   = RGBColor(0xD9, 0xD9, 0xD9)   # #D9D9D9

# --- Type families -----------------------------------------------------
HEADING_FONT = "Aleo"   # titles, dividers, stats, pull quotes
BODY_FONT    = "Lato"   # body, bullets, labels, footers

CHART_SERIES = [HBEF_NAVY, HBEF_VALLEY, HBEF_TEAL,
                HBEF_VISTA, HBEF_TURQUOISE, HBEF_WET_SAND]

DIVIDER_ROTATION = [HBEF_VIEW, HBEF_TEAL, HBEF_VALLEY, HBEF_TURQUOISE]

TAX_LANGUAGE = (
    "HBEF is a registered 501(c)(3) non-profit organization. Contributions are "
    "tax-deductible to the extent allowed by law. Federal tax identification "
    "number (EIN): 33-0522270"
)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Blank layout
blank = prs.slide_layouts[6]


def add_rect(slide, x, y, w, h, color, line=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if line is None:
        shape.line.fill.background()
    else:
        shape.line.color.rgb = line
        shape.line.width = Pt(1)
    shape.shadow.inherit = False          # 2026 system is flat — no shadows
    return shape


def add_accent_bar(slide, color=HBEF_NAVY, y=0, height=Inches(0.05)):
    """The 0.05in top accent bar on every content slide."""
    return add_rect(slide, 0, y, prs.slide_width, height, color)


def set_text(tf, text, size=Pt(16), bold=False, italic=False,
             color=HBEF_ASPHALT, font=BODY_FONT, align=PP_ALIGN.LEFT,
             spacing=None):
    """spacing = letter-spacing in points (Lato elements only)."""
    tf.text = text
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.runs[0]
    run.font.name = font
    run.font.size = size
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    if spacing is not None:
        run.font._rPr.set('spc', str(int(spacing * 100)))   # EMU-free: 1/100 pt
    return run


def add_title(slide, text, left=Inches(0.7), top=Inches(0.5),
              width=Inches(11.9), height=Inches(0.9)):
    """Slide title — Aleo Bold 28pt HBEF_NAVY. No caps, no tracking."""
    box = slide.shapes.add_textbox(left, top, width, height)
    set_text(box.text_frame, text, size=Pt(28), bold=True,
             color=HBEF_NAVY, font=HEADING_FONT)
    return box


def add_eyebrow(slide, text, left=Inches(0.7), top=Inches(0.25),
                width=Inches(11.9), color=HBEF_WET_SAND):
    """Eyebrow — Lato Bold 11pt UPPERCASE +1.2pt."""
    box = slide.shapes.add_textbox(left, top, width, Inches(0.3))
    set_text(box.text_frame, text.upper(), size=Pt(11), bold=True,
             color=color, font=BODY_FONT, spacing=1.2)
    return box


def add_footer(slide, page_no, on_sky=True):
    """Footer bar — HBEF_SKY band with Asphalt/Navy type."""
    y = Inches(7.2)
    if on_sky:
        add_rect(slide, 0, y, prs.slide_width, Inches(0.3), HBEF_SKY)
    left = slide.shapes.add_textbox(Inches(0.7), y, Inches(7), Inches(0.3))
    set_text(left.text_frame, "Hermosa Beach Education Foundation · hbef.org",
             size=Pt(9), color=HBEF_ASPHALT if on_sky else HBEF_WET_SAND)
    right = slide.shapes.add_textbox(Inches(11.5), y, Inches(1.2), Inches(0.3))
    set_text(right.text_frame, str(page_no), size=Pt(9), bold=True,
             color=HBEF_NAVY, align=PP_ALIGN.RIGHT)


def add_stat(slide, number, label, accent=HBEF_NAVY):
    """Pull-out stat — Aleo Bold 60pt + Lato 11pt label."""
    num = slide.shapes.add_textbox(Inches(0.7), Inches(2.4),
                                   Inches(11.9), Inches(1.6))
    set_text(num.text_frame, number, size=Pt(60), bold=True,
             color=accent, font=HEADING_FONT)
    cap = slide.shapes.add_textbox(Inches(0.7), Inches(4.1),
                                   Inches(11.9), Inches(0.5))
    set_text(cap.text_frame, label, size=Pt(11), color=HBEF_WET_SAND)


def add_cta_button(slide, text, x, y, w=Inches(4.6), h=Inches(0.7),
                   fill=HBEF_VIEW, text_color=HBEF_NAVY):
    """CTA — View fill with NAVY text (never white on yellow)."""
    btn = add_rect(slide, x, y, w, h, fill)
    set_text(btn.text_frame, text.upper(), size=Pt(16), bold=True,
             color=text_color, font=BODY_FONT, align=PP_ALIGN.CENTER,
             spacing=2.0)
    return btn


def add_cover(prs, title, subtitle, eyebrow, meta, rule_color=HBEF_VIEW):
    slide = prs.slides.add_slide(blank)
    band_h = Inches(2.25)                                  # top 30%
    add_rect(slide, 0, 0, prs.slide_width, band_h, HBEF_NAVY)
    slide.shapes.add_picture(
        "assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png",
        left=int((prs.slide_width - Inches(4)) / 2),
        top=Inches(0.45), width=Inches(4),
    )
    add_eyebrow(slide, eyebrow, top=Inches(2.8))

    t = slide.shapes.add_textbox(Inches(0.7), Inches(3.2),
                                 Inches(11.9), Inches(1.2))
    set_text(t.text_frame, title, size=Pt(54), bold=True,
             color=HBEF_NAVY, font=HEADING_FONT)

    s = slide.shapes.add_textbox(Inches(0.7), Inches(4.4),
                                 Inches(11.9), Inches(0.6))
    sub = set_text(s.text_frame, subtitle, size=Pt(20), color=HBEF_TEAL)
    sub.font.bold = False                                   # Lato Light 300

    add_rect(slide, Inches(0.7), Inches(5.2), Inches(2), Pt(3), rule_color)

    m = slide.shapes.add_textbox(Inches(0.7), Inches(5.6),
                                 Inches(11.9), Inches(0.4))
    set_text(m.text_frame, meta, size=Pt(11), color=HBEF_WET_SAND)

    add_rect(slide, 0, prs.slide_height - Inches(0.3),
             prs.slide_width, Inches(0.3), rule_color)
    return slide
```

> **Lato Light (300):** `python-pptx` has no weight axis — set `run.font.name = "Lato Light"` when the 300 weight is genuinely needed (cover subtitle) and the face is installed under that name; otherwise use `"Lato"` with `bold=False` and accept Regular. Never fake Light by lowering opacity.

## Final checks (before sharing)

1. Cover loaded with the **Dark Mode** lockup on the navy band; title in Aleo Bold 54pt, sentence/title case, no tracking.
2. Every content slide has the 0.05" `HBEF_NAVY` accent bar at top.
3. Section dividers placed between major content sections, with the accent rotation `HBEF_VIEW` → `HBEF_TEAL` → `HBEF_VALLEY` → `HBEF_TURQUOISE`.
4. At least one stat slide and one quote slide for visual rhythm.
5. Closing/ask slide with donate URL, contact block, and the **full** tax sentence (EIN 33-0522270).
6. Slide numbers visible in the footer bar.
7. Fonts: **Aleo on titles/dividers/stats, Lato everywhere else** — verify in the Slide Master, and confirm no Montserrat or BauhausBold survives anywhere in the file.
8. No pure black text — body is `HBEF_ASPHALT` `#515962`.
9. No retired hex values: search the deck for `0B4261`, `124362`, `F79B32`, `75C4B9`, `74C4B9`, `417987`, `FAEF7A`, `E7E7E7`, `1A1A1A`, `5C5C5C`, `CCCCCC`.
10. `HBEF_VIEW` `#FFCD00` used only as fill/rule/band — never as small type, and never with white text on it.
11. Charts: palette in the correct order (Navy → Valley → Teal → Vista → Turquoise → Wet Sand); no 3D, no shadows.
12. Flat throughout — no drop shadows on cards, text, or shapes.
13. Fonts embedded (re-save from PowerPoint with embedding on), or export to PDF for distribution, and verify rendering.
