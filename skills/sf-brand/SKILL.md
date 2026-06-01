---
name: sf-brand
description: "Summer Fridays brand guide for generating consistent, on-brand documents and deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, charts, or any visual deliverable for the Summer Fridays marketing/distribution growth project. Also trigger when the user mentions Summer Fridays branding, SF brand styling, Jet Lag blue, Lip Butter Balm palette, Marianna Hewitt / Lauren Ireland brand voice, or asks for a document 'in the same style as' previous Summer Fridays deliverables. Trigger even when the user just says 'make this on-brand', 'apply the SF look', 'use our palette', or names a SF-coded color (morning sky, chalk, clay, ink, pink sugar, vanilla beige, hot cocoa, iced coffee). This skill is the brand LAYER — it pairs with format-specific skills (docx, pptx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output."
---

# Summer Fridays — Brand Skill

This skill defines the visual identity system, voice, and document-production patterns for Summer Fridays marketing deliverables produced inside bang's Summer Fridays project. Every color, font, layout convention, and component pattern has been calibrated against the live brand surface at summerfridays.com (theme version 450, Futura PT via Adobe Typekit kit `ljq5ufs`) and the product line as of May 2026.

The goal is for every PDF, deck, spreadsheet, and Word doc to feel like an extension of the brand — soft, sun-warmed, California-coded, sensorial, never corporate.

## When to read what

This SKILL.md is the brand-system core. For format-specific implementation, read the matching reference:

- **`references/docx-instructions.md`** — Read when creating Word documents (.docx). Cover page, headings, body, tables, callouts. Pair with the `docx` skill.
- **`references/pptx-instructions.md`** — Read when creating PowerPoint decks (.pptx). Slide layouts, cover, dividers, content patterns. Pair with the `pptx` skill.
- **`references/xlsx-instructions.md`** — Read when creating Excel workbooks (.xlsx). Sheet styling, tables, charts, dashboard tabs. Pair with the `xlsx` skill.
- **`references/pdf-instructions.md`** — Read when creating PDFs from HTML or Word source. Cover, watermarks, footer. Pair with the `pdf` skill.
- **`references/colors-and-fonts.md`** — Read for the full token system (every named color, every shade, every type style) when you need the long version. The summary below is sufficient for ~80% of jobs.

Read the brand SKILL.md first, then the format reference, then build. Don't improvise hex values from memory — copy them from the assets below.

---

## Brand DNA (1-paragraph north star)

Summer Fridays is **essential beauty formulations from California, for the skin and senses**. The brand voice is soft, sensorial, founder-led, and aspirational-but-attainable — California weekend energy bottled. Visual language is minimal, generous with whitespace, photographs well on iPhones, and built on a warm-pastel palette anchored by **Jet Lag blue** (the signature pale blue of the original face mask) and **vanilla cream**. Documents should feel like a Summer Friday morning — light, easy, never fussy. **If a layout feels corporate, it's wrong.**

---

## Brand Color Palette

The palette has three layers: **brand neutrals** (the document workhorse), **product shades** (used as accents and chart colors, sourced from the actual product line CSS swatches at summerfridays.com), and **functional UI** (status, data viz).

### Brand Neutrals (the document core)

| Token | Hex | Role | Source |
|---|---|---|---|
| `INK` | `#1A1A1A` | Primary text. Headlines, body, table text. The "almost-black" reads warmer than `#000`. | Inferred from site rendering of `--ink` |
| `INK_60` | `#5C5C5C` | Secondary text. Captions, footnotes, table notes, metadata. | Calibrated from `--ink-40` (40% on white) and rendered text |
| `INK_30` | `#A8A8A8` | Tertiary text + thin rules. Dividers, faint borders. | Calibrated |
| `CHALK` | `#FAF6EF` | Page background, soft-fill cards. Warm off-white — never use pure white as a section fill. | Inferred from site rendering of `--chalk` |
| `MORNING_SKY` | `#BDD7E5` | **The signature Jet Lag blue.** Cover accents, callout fills, chart series 1, hero band. | Inferred from `--morning-sky` rendering |
| `MORNING_SKY_DEEP` | `#7DA8BD` | Deeper variant of Jet Lag blue for type-on-blue legibility and chart contrast. | Calibrated |
| `CLAY` | `#C9A582` | Warm sand/beige accent. Section dividers, secondary callouts, chart series 2. | Inferred from `--clay` rendering |
| `VANILLA` | `#F5E9DD` | The vanilla cream — Lip Butter Balm signature. Soft fill panels, gourmand callouts. | **Observed in product swatch CSS** |
| `WHITE` | `#FFFFFF` | Reserved. Use sparingly — only inside cards on `CHALK` backgrounds, or as text on dark fills. |

### Product-Shade Accent Palette (extracted from live site CSS)

These hex codes are pulled directly from the swatch markup on summerfridays.com. Use them when you need an accent color with brand provenance (e.g. chart series differentiation, callout box variants, section tabs in a multi-section report). Map them by mood — sweet/warm/deep — not just by name.

**Lip Butter Balm — sweet pastel range**
| Token | Hex | Shade |
|---|---|---|
| `PINK_SUGAR` | `#FC88AB` | Warm rosy pink |
| `PINK_GUAVA` | `#B44F65` | Muted berry pink |
| `CHERRY` | `#A84544` | Cherry red |
| `POPPY` | `#A43062` | Deep raspberry |
| `SWEET_MINT` | `#A4C089` | Soft sage green |

**Lip Liner / Coffee taxonomy — warm deep range**
| Token | Hex | Shade |
|---|---|---|
| `TOFFEE` | `#C1947F` | Warm toffee |
| `LATTE` | `#997970` | Milky brown |
| `PECAN` | `#8D5A54` | Reddish brown |
| `CINNAMON` | `#9B6E53` | Cinnamon stick |
| `HOT_COCOA` | `#6B3D2E` | Deep cocoa |
| `ESPRESSO` | `#674736` | Near-black coffee |

**Blush + Color — warm bright range**
| Token | Hex | Shade |
|---|---|---|
| `SOFT_STRAWBERRY` | `#FE99A8` | Light pink |
| `PINK_SUNSET` | `#E45D50` | Coral red |
| `SWEET_ROSE` | `#EF426F` | Vivid rose |
| `TOASTED_TERRACOTTA` | `#BD4F5C` | Earthy terracotta |
| `SAND_NEUTRAL` | `#C9BBA0` | Warm sand |

### Functional UI palette

| Token | Hex | Role |
|---|---|---|
| `ACCENT_BLUE` | `#3C5A78` | Hyperlinks, "Learn more" CTAs, citation references. |
| `SUCCESS` | `#7CA982` | Positive variance, opportunity tags |
| `WARNING` | `#D9A06B` | Caution, watchlist items |
| `RISK` | `#A84544` | Material risk flags — uses Cherry from the brand palette intentionally |
| `MUTED_BORDER` | `#E5E5EB` | Table cell borders, card outlines (extracted from site review widget) |
| `MUTED_TEXT` | `#676986` | Tertiary review-style metadata (extracted from site) |

### Color usage rules

- **One blue per page.** Use `MORNING_SKY` (light) or `MORNING_SKY_DEEP` (mid-tone), never both as accents on the same surface.
- **Chalk over white.** Default to `#FAF6EF` for page/section background; pure `WHITE` is for inset cards only.
- **Color stories travel together.** When you pull a Lip Butter Balm accent, the doc reads "sweet/gourmand." When you pull a Lip Liner accent, it reads "warm/grounded." Don't mix them in the same callout strip.
- **Never use saturated red, electric blue, neon, or pure black.** Those don't exist on the brand surface.

---

## Typography

### Font families

- **Primary brand typeface: Futura PT** (Adobe Typekit kit `ljq5ufs`, weights 500 + italic 500). This is what summerfridays.com uses for all on-site copy. Body weight is `450` (slightly lighter than regular).
- **Document fallback:** Most users don't have Futura PT licensed locally for Word/PowerPoint. The official fallback chain is **`Futura PT, Futura, "Avenir Next", Avenir, "Helvetica Neue", Helvetica, Arial, sans-serif`**.
- **For docx + pptx generated programmatically** (where embedded fonts aren't trivial): use **`Avenir Next`** if available on the target machine, else **`Helvetica Neue`**, else **`Arial`**. Document the fallback in the file's metadata so the user knows.
- **Editorial / accent display:** for cover headings or pull quotes that need extra warmth, use a serif companion — **`Cormorant Garamond`** or **`Playfair Display`** (Google Fonts, free). Use sparingly. The brand site itself uses a custom typeface called Expressa for some headings — Cormorant approximates the mood.
- **Never use:** Times New Roman, Comic Sans, Calibri (too corporate), Brush Script, anything mono unless it's a code/data block in a developer-facing deliverable.

### Document text hierarchy (Word / PDF — sizes in pt)

| Element | Font | Size | Weight | Color | Notes |
|---|---|---|---|---|---|
| Document title (cover) | Futura PT/Avenir Next | 36 | Light (300) or Regular (450) | INK | Letter-spacing +1.5pt |
| H1 section | Futura PT/Avenir Next | 22 | Regular (500) | INK | Letter-spacing +0.5pt, space-before 24pt |
| H2 sub-section | Futura PT/Avenir Next | 16 | Medium (500) | INK | Space-before 18pt |
| H3 minor | Futura PT/Avenir Next | 12 | Medium (500) | MORNING_SKY_DEEP | Uppercase, letter-spacing +1.2pt |
| Body | Futura PT/Avenir Next | 11 | Regular (450) | INK | Line-height 1.55 |
| Lead paragraph | Futura PT/Avenir Next | 13 | Regular (450) | INK | First-paragraph after H1; line-height 1.5 |
| Caption / metadata | Futura PT/Avenir Next | 9 | Regular (450) | INK_60 | Often italic |
| Pull quote | Cormorant Garamond (or italic Futura) | 18 | Italic | INK | Indented 0.5", `MORNING_SKY` left border 2pt |
| Footnote | Futura PT/Avenir Next | 8 | Regular | INK_60 | |
| Table header | Futura PT/Avenir Next | 10 | Medium | INK on MORNING_SKY fill | Uppercase, letter-spacing +0.8pt |
| Table cell | Futura PT/Avenir Next | 10 | Regular | INK | |
| Table notes column | Futura PT/Avenir Next | 9 | Italic | INK_60 | |

### Presentation text hierarchy (PPTX — sizes in pt)

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Cover title | Futura PT/Avenir Next | 60 | Light/Regular | INK on CHALK |
| Cover subtitle | Cormorant Garamond Italic | 22 | Italic | INK_60 |
| Section divider title | Futura PT/Avenir Next | 44 | Regular | INK on MORNING_SKY fill |
| Slide title | Futura PT/Avenir Next | 28 | Medium | INK |
| Slide subtitle | Futura PT/Avenir Next | 14 | Regular | INK_60 |
| Body | Futura PT/Avenir Next | 16 | Regular | INK |
| Bullet | Futura PT/Avenir Next | 14 | Regular | INK |
| Pull-out stat (large number) | Futura PT/Avenir Next | 56 | Light (300) | MORNING_SKY_DEEP |
| Caption | Futura PT/Avenir Next | 10 | Regular | INK_60 |
| Footer | Futura PT/Avenir Next | 9 | Regular | INK_60 |

---

## Brand Voice (for any document with prose)

Match the founders' editorial register from summerfridays.com:

- **Sensorial vocabulary:** dewy, cushion, soothing, luminous, gentle, butter, cloud, soft, warm
- **Lifestyle metaphors:** ease, light, golden hour, weekend, ritual, glow, every day a Summer Friday
- **Founder-narrated cadence:** "we," "our community," "what we love about…" — not "the company" or "the brand"
- **Avoid:** consultancy speak ("leverage," "synergy," "actionable insights"), hype ("game-changing," "revolutionary"), beauty-industry jargon that sounds clinical ("active ingredient delivery system")
- **Hold:** numeric precision in reports. "10.5% share of Sephora skincare" is more on-brand than "leading share." Soft voice ≠ vague facts.
- **Honorifics:** "Marianna Hewitt and Lauren Gores Ireland" (full first reference); "Marianna and Lauren" (subsequent). Never just "Hewitt" — they're a creator brand, names go together.
- **Brand mark in text:** "Summer Fridays" (two words, both capitalized, no logo glyph in body copy). Never "SummerFridays" or "summer fridays."
- **Product mark conventions:** Hero SKUs carry trademark glyphs on first reference — **Jet Lag™ Mask**, **Cloud Dew®**, **Sunlit Vanilla™**, **Jet Lag™ Eye Patches**. Drop the glyph in subsequent references.

---

## Cover page pattern (universal across formats)

Every multi-page deliverable opens with a cover that reads:

```
[CHALK background — fills the whole page]

[top-left, 9pt, INK_60, letter-spacing +1.2pt, uppercase]
SUMMER FRIDAYS  ·  MARKETING INTELLIGENCE

[centered vertically in upper-mid third]
[Title in 36pt Futura/Avenir, INK]
The Document Title

[Subtitle in 18pt Cormorant Garamond Italic, INK_60]
A short editorial subtitle that sets the scene

[2pt MORNING_SKY horizontal rule, 1.5" wide, centered]

[Bottom of page, 9pt, INK_60]
[Author] · [Date] · [Confidential — Internal Working Document]
```

Variant: replace the rule with a tiny VANILLA-filled rectangle (0.5" × 0.08") for fragrance/gourmand briefs, or MORNING_SKY for skincare/Jet Lag briefs, or PINK_SUGAR for lip-franchise briefs. The accent color signals the content domain.

---

## Section dividers (universal)

Between major sections in long documents:

```
[CHALK background, full bleed]

[Tiny eyebrow, 9pt, INK_60, uppercase, letter-spacing +1.2pt]
PART 02

[Title in 22pt Futura/Avenir, INK]
Section Title

[Single 1pt MORNING_SKY rule, 100% width, 12pt below title]
```

Section divider color rotation across a long doc: MORNING_SKY → CLAY → VANILLA → MORNING_SKY_DEEP, then loop. This gives visual rhythm without inventing colors.

---

## Iconography & illustration

- **Iconography:** thin-line, 1px–1.5px stroke, INK or INK_60 on light. Phosphor Icons, Tabler, Lucide (in priority order) are good open-source matches. Never use 3D, glossy, or color-filled icons.
- **Imagery:** prefer real product / lifestyle photography from summerfridays.com CDN when illustrating a point. Pull URLs from the brief at `/Users/nolan/Projects/Summer Fridays/00_context/SF_brand_intelligence_2026-05-17.md` if needed.
- **Decorative accents:** soft circles, blurred edges, subtle gradients (CHALK → VANILLA, or WHITE → MORNING_SKY at 20% opacity). Never hard geometric shapes or starbursts.

---

## Data visualization

When charting numbers in any format:

- **Chart palette order (categorical):** `MORNING_SKY_DEEP` → `CLAY` → `PINK_GUAVA` → `HOT_COCOA` → `SWEET_MINT` → `INK_60`. This is a max-6-series progression that holds together visually.
- **Single-series accent:** always `MORNING_SKY_DEEP` for skincare/business metrics; switch to `PINK_GUAVA` for lip-franchise metrics; `CLAY` for fragrance.
- **Gridlines:** `MUTED_BORDER` (#E5E5EB) at 0.75pt — barely visible, never dominant.
- **Axes / labels:** `INK_60` 9pt, no axis lines on top/right (open frame).
- **Background:** `CHALK` for embedded chart blocks; `WHITE` only when the chart sits inside a card with chalk surround.
- **No 3D, no shadows, no rainbow gradients.** Categorical only.
- **Annotation pattern:** highlight the headline data point in `INK` bold; everything else stays in `INK_60`. Let the eye land where it should.

---

## Asset files (in this skill)

Bundled assets the format references will pull from:

- **`assets/brand-tokens.json`** — machine-readable token file. Use this when programmatically generating CSS, Word doc styles, Excel cell fills, etc. Every named token (INK, CHALK, MORNING_SKY, PINK_SUGAR, …) maps to its hex value, plus typography settings.
- **`assets/brand-palette.css`** — copy-paste CSS variables block. Use for any HTML deliverable (dashboards, reports, presentations rendered to HTML before PDF).
- **`assets/color-swatches.html`** — visual reference. Open this in a browser to see every color rendered. Send to the user when they ask "what do the colors look like?"

---

## Working with format skills

This is a brand-LAYER skill. The mechanics of building each file format live in their dedicated skills. The workflow is always:

1. **Read this SKILL.md** to load the brand system into context.
2. **Read the matching reference in `references/`** for the format you're producing.
3. **Read the format skill** (`docx`, `pptx`, `xlsx`, `pdf`, etc.) for the file-construction code patterns.
4. **Apply the brand tokens** from `assets/brand-tokens.json` to the format skill's templates.
5. **Verify** the output by reading the produced file before sharing.

### Example invocation patterns

> "Build me a one-pager on Q1 Sephora performance"
> → read sf-brand SKILL.md + `references/pdf-instructions.md` + the `pdf` skill → produce branded PDF cover + body + footer

> "Create a deck for our partnership pitch with [airline]"
> → read sf-brand SKILL.md + `references/pptx-instructions.md` + the `pptx` skill → produce cover slide, section dividers, content slides

> "Make a spreadsheet that tracks creator campaign performance"
> → read sf-brand SKILL.md + `references/xlsx-instructions.md` + the `xlsx` skill → produce styled sheets with cover tab, brand-fill headers, chart palette

> "Write up the H1 IG reformat plan as a doc"
> → read sf-brand SKILL.md + `references/docx-instructions.md` + the `docx` skill → produce cover + sections + callout box recommendation

---

## Final guardrails

- **If a deliverable doesn't look California-warm and breathable, it's wrong.** Add whitespace before adding content.
- **Match the brief, not the trend.** SF voice is older/softer than Rhode (which is sharper/younger). Don't borrow Rhode's neon-coded confidence.
- **Numbers stay precise.** Soft voice doesn't mean fuzzy data. "Sephora skincare share: 10.5%" not "leading."
- **Always cite sources in research-style deliverables.** Match the [Title](URL) format used in `00_context/SF_brand_intelligence_2026-05-17.md`.
- **When in doubt, read the source-of-truth brief** at `/Users/nolan/Projects/Summer Fridays/00_context/SF_brand_intelligence_2026-05-17.md` — it has the verified facts about the brand, business, and strategy hypotheses (H1–H8) you'll be writing about.
