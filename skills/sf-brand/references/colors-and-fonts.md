# Summer Fridays — Full Color & Font Reference

The expanded version of the palette + typography system summarized in SKILL.md. Read this when you need the long-form spec — e.g., building a complete design-system tokens file, configuring a new tool with the full palette, or answering a question about a specific shade.

## Provenance

| Source type | Where it came from | Trust |
|---|---|---|
| **Observed in source CSS** | Hex values appearing literally in summerfridays.com page source (e.g. product variant swatches) | High — these are the exact values shipped to users |
| **Inferred from named token + rendering** | Theme uses `--ink`, `--chalk`, `--clay`, `--morning-sky` etc. but their hex is server-side-injected; values calibrated to match observable rendering | Medium-high — within 1–2 shades of true value |
| **Calibrated to brand aesthetic** | Functional/extended values not present on the brand surface but designed to complement the observed palette | Author judgment — adjust if first-party brand assets become available |

If/when bang gets first-party access to the SF brand guide or theme settings_data.json, prioritize updating the INK / CHALK / MORNING_SKY / CLAY hexes — those four anchor the system.

## Confirmed font

- **Futura PT** — Adobe Typekit kit ID `ljq5ufs`, loaded on every page of summerfridays.com
- Weights in use: `n5` (regular 500) and `i5` (italic 500)
- Body weight: `font-weight: 450` (intentionally lighter than the loaded 500 for a softer rendering)
- Letter-spacing on body: `0.013rem` (subtle)
- Site CSS exposes named font vars: `--font-primary`, `--font-secondary`, `--font-body`, `--font-expressa`, `--font-pinyon`
  - `--font-pinyon` is **Pinyon Script** — used very sparingly for editorial flourishes
  - `--font-expressa` is a custom or licensed editorial typeface (mood: Cormorant Garamond / Playfair)

For document generation where Futura PT can't be embedded, the canonical fallback chain is:

```css
font-family: "Futura PT", Futura, "Avenir Next", Avenir, "Helvetica Neue", Helvetica, Arial, sans-serif;
```

## Complete shade library

### Brand neutrals (the document workhorse)
```
INK              #1A1A1A   Primary text
INK_60           #5C5C5C   Secondary text
INK_30           #A8A8A8   Tertiary text, thin rules
CHALK            #FAF6EF   Page background — warm off-white
WHITE            #FFFFFF   Inset cards only
```

### Brand accents
```
MORNING_SKY      #BDD7E5   The signature Jet Lag blue
MORNING_SKY_DEEP #7DA8BD   Type-on-blue, chart contrast
CLAY             #C9A582   Warm sand
VANILLA          #F5E9DD   Soft cream (LBB signature, observed in CSS)
```

### Product shades — sweet pastel range (Lip Butter Balm)
```
PINK_SUGAR       #FC88AB   Rosy pink
PINK_GUAVA       #B44F65   Muted berry
CHERRY           #A84544   Cherry red
POPPY            #A43062   Deep raspberry
SWEET_MINT       #A4C089   Soft sage
```

### Product shades — warm deep range (Lip Liner / coffee taxonomy)
```
TOFFEE           #C1947F   Warm toffee
LATTE            #997970   Milky brown
PECAN            #8D5A54   Reddish brown
CINNAMON         #9B6E53   Cinnamon stick
HOT_COCOA        #6B3D2E   Deep cocoa
ESPRESSO         #674736   Near-black coffee
```

### Product shades — warm bright range (Blush + Color)
```
SOFT_STRAWBERRY  #FE99A8   Light pink
PINK_SUNSET      #E45D50   Coral red
SWEET_ROSE       #EF426F   Vivid rose
TOASTED_TERRACOTTA #BD4F5C Earthy terracotta
SAND_NEUTRAL     #C9BBA0   Warm sand
```

### Functional UI
```
ACCENT_BLUE      #3C5A78   Links, citations, CTAs
SUCCESS          #7CA982   Positive variance
WARNING          #D9A06B   Caution
RISK             #A84544   Risk (= CHERRY, intentional reuse)
MUTED_BORDER     #E5E5EB   Cell borders, card outlines (observed)
MUTED_TEXT       #676986   Tertiary review-style meta (observed)
```

## Pairing matrices

### Safe color pairings for callouts / dividers / section accents
```
MORNING_SKY  on CHALK   ✓ default
VANILLA      on CHALK   ✓ gourmand/fragrance briefs
CLAY         on CHALK   ✓ retail/distribution briefs
PINK_SUGAR   on CHALK   ✓ lip-franchise briefs
WHITE        on CHALK   ✓ insets and cards (with INK_30 border)
WHITE        on MORNING_SKY ✓ cover hero band
INK          on CHALK   ✓ all text
INK          on VANILLA ✓ pull quotes
INK          on MORNING_SKY ✓ headlines on cover
WHITE        on HOT_COCOA   ✓ deep-tone dark cards (rare; for dramatic divider only)
WHITE        on ESPRESSO    ✓ deepest dark card
```

### Pairings to avoid
```
MORNING_SKY  on WHITE          ✗ too washed out
MORNING_SKY  on VANILLA        ✗ two pastels fight
PINK_SUGAR   on PINK_GUAVA     ✗ same family clash
CHERRY       on PINK_SUNSET    ✗ red-on-red
Any saturated accent on saturated accent ✗
Pure WHITE on CHALK            ✗ no contrast value
```

## Type sizing — full reference

### For Word documents (sizes in pt; line-height as multiplier)
```
Cover title           36pt / 1.1     Light or Regular
Cover subtitle        18pt / 1.3     Italic (Cormorant)
Cover meta             9pt / 1.4     Regular, letter-spacing +1.2pt, uppercase
H1                    22pt / 1.2     Regular, letter-spacing +0.5pt
H2                    16pt / 1.3     Medium
H3                    12pt / 1.3     Medium, uppercase, letter-spacing +1.2pt, MORNING_SKY_DEEP
Body lead             13pt / 1.5     Regular
Body                  11pt / 1.55    Regular
Caption                9pt / 1.4     Regular, INK_60
Pull quote            18pt / 1.4     Italic, INK
Footnote               8pt / 1.35    Regular, INK_60
Table header          10pt / 1.3     Medium, uppercase, letter-spacing +0.8pt
Table cell            10pt / 1.4     Regular
Table notes            9pt / 1.4     Italic, INK_60
```

### For PowerPoint (sizes in pt)
```
Cover title           60pt           Light or Regular
Cover subtitle        22pt           Italic (Cormorant)
Section divider       44pt           Regular
Slide title           28pt           Medium
Slide subtitle        14pt           Regular, INK_60
Body                  16pt           Regular
Bullet                14pt           Regular
Big stat              56pt           Light, MORNING_SKY_DEEP
Caption               10pt           Regular, INK_60
Footer                 9pt           Regular, INK_60
```

### For Excel (sizes in pt)
```
Worksheet title       16pt           Medium (in merged cell)
Section header        12pt           Medium, MORNING_SKY fill, INK text
Table header          10pt           Medium, MORNING_SKY fill, INK text, uppercase
Body cell              9pt           Regular
Numeric cell           9pt           Regular, right-aligned, tabular numerals
Footer / source        8pt           Italic, INK_60
```

## Hex → RGB → HSL conversion table (for tools that need them)

| Token | Hex | RGB | HSL |
|---|---|---|---|
| INK | `#1A1A1A` | `26, 26, 26` | `0, 0%, 10%` |
| INK_60 | `#5C5C5C` | `92, 92, 92` | `0, 0%, 36%` |
| INK_30 | `#A8A8A8` | `168, 168, 168` | `0, 0%, 66%` |
| CHALK | `#FAF6EF` | `250, 246, 239` | `38, 50%, 96%` |
| MORNING_SKY | `#BDD7E5` | `189, 215, 229` | `201, 41%, 82%` |
| MORNING_SKY_DEEP | `#7DA8BD` | `125, 168, 189` | `200, 31%, 62%` |
| CLAY | `#C9A582` | `201, 165, 130` | `30, 38%, 65%` |
| VANILLA | `#F5E9DD` | `245, 233, 221` | `30, 52%, 91%` |
| PINK_SUGAR | `#FC88AB` | `252, 136, 171` | `342, 96%, 76%` |
| ACCENT_BLUE | `#3C5A78` | `60, 90, 120` | `210, 33%, 35%` |

(Tools like matplotlib, python-pptx, openpyxl take hex strings directly — RGB/HSL only needed for edge cases.)
