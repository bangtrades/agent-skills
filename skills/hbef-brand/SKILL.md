---
name: "hbef-brand"
description: "Hermosa Beach Education Foundation (HBEF) brand guide — the 2026 identity system. Use when creating Word, PowerPoint, Excel, PDF, HTML, charts, Google Docs/Sheets/Slides, or Apple Pages/Numbers/Keynote for HBEF, Hearts of Hermosa, the Skechers Friendship Walk, The Strand Classic, Moms' Night Out, Annual Giving, or the HBEF Endowment / Investment Committee / Technology Advisory Board. Covers the sunburst logo system, the Coastal Colors palette (Navy #0C3B5D, Teal #186892, Turquoise #129FDA, View #FFCD00, Vista #FFA400, Valley #EE7623, Sky, Sand, Wet Sand, Asphalt), Aleo + Lato typography, letterhead, and print/digital specs. Trigger on HBEF branding, HBEF navy/teal/turquoise, Aleo or Lato type, the sunburst mark, \"same style as\" prior HBEF work, \"make this on-brand\", \"apply the HBEF look\", \"use our palette\", or any named HBEF event. Brand LAYER — pair with format skills (docx, pptx, xlsx, pdf, canvas-design, frontend-design). Read this plus the matching format reference before generating output."
---

# Hermosa Beach Education Foundation — Brand Skill

This skill defines the visual identity system, voice, and document-production patterns for any deliverable produced on behalf of the Hermosa Beach Education Foundation (HBEF).

**Source of truth: `HBEF Brand Guidelines 2026`** — the foundation's own guidelines document, plus the released logo, typeface, and letterhead asset library. Master assets live at `/Users/nolan/Projects/HBEF/HBEF BRANDING/`. Working copies of the files you will need most are bundled in `assets/` inside this skill.

> ### ⚠ REBRAND NOTICE — read this first
>
> HBEF completed a full identity refresh in 2026. **Everything from the previous system is retired.** If you produce a deliverable using any of the following, it is wrong:
>
> | Retired (do NOT use) | Replaced by |
> |---|---|
> | Montserrat, BauhausBold | **Aleo** (headings) + **Lato** (body) |
> | Navy `#0B4261` | Navy `#0C3B5D` |
> | Teal `#75C4B9` / `#74C4B9` | Teal `#186892` (structural) · Sky `#B8D8EB` (light fills) |
> | Orange `#F79B32` | Valley `#EE7623` · Vista `#FFA400` · View `#FFCD00` |
> | Yellow `#FAEF7A`, page gray `#E7E7E7` | View `#FFCD00`, Sand `#DDC9A3` / Sky `#B8D8EB` |
> | Old sail/wordmark logo, "HBEF_stacked" files | Sunburst-over-wave lockups in `assets/logos/` |
>
> The folder `HBEF BRANDING/Z PRIOR BRANDING - DO NOT USE/` holds the 2021 and pre-2021 marks for archival identification only. Never pull an asset from it. See `references/legacy-brand.md` if you need to recognize or migrate an old deliverable.

The goal: every PDF, deck, spreadsheet, Word doc, Google Doc, and Apple Pages file should look like it came out of the same studio that made the letterhead — coastal, sunlit, civic, parent-led, never corporate.

---

## When to read what

This SKILL.md is the brand-system core. For format-specific implementation, read the matching reference:

- **`references/docx-instructions.md`** — Word documents (.docx). Letterhead, cover page, headings, body, tables, callouts. Pair with the `docx` skill.
- **`references/pptx-instructions.md`** — PowerPoint decks (.pptx). Slide layouts, cover, dividers, content patterns. Pair with the `pptx` skill.
- **`references/xlsx-instructions.md`** — Excel workbooks (.xlsx). Sheet styling, tables, charts, dashboard tabs. Pair with the `xlsx` skill.
- **`references/pdf-instructions.md`** — PDFs from HTML or Word source. Cover, footer, font embedding, CMYK print export. Pair with the `pdf` skill.
- **`references/google-apple-docs.md`** — Google Docs / Sheets / Slides, Apple Pages / Numbers / Keynote. Font handling, when to export PDF instead.
- **`references/colors-and-fonts.md`** — Long-form token reference (every named color, CMYK builds, tint ramps, WCAG contrast ratios, every type style). The summary below covers ~80% of jobs.
- **`references/voice-and-content.md`** — Editorial voice, signature phrases, what to say and what to avoid in donor-facing copy.
- **`references/legacy-brand.md`** — The retired pre-2026 system, for recognizing and migrating old files only.

Read this SKILL.md first, then the format reference, then build. **Never improvise hex values from memory — copy them from `assets/brand-tokens.json` or the tables below.**

---

## Brand DNA (one-paragraph north star)

HBEF raises funds and awareness for the educational programs and students of Hermosa Beach public schools. The brand is **coastal civic warm**: a sunburst rising over an ocean wave, deep Navy structure, a sunlit yellow-to-orange accent family, and generous white space. The voice is **professional, community-focused, inspiring, and approachable**. Typography blends a sturdy academic slab serif (Aleo) with a warm, highly legible sans (Lato) — "established but friendly," not "institutional." Documents should feel like a warm, organized pitch from a neighbor at a school picnic. **If a layout reads corporate, generic, or luxury-branded, it's wrong** — HBEF's whole positioning is a volunteer, parent-run foundation closing a public-funding gap.

---

## The Logo System

Four lockups. All are built from the same sunburst-over-wave mark. Files are in `assets/logos/`; the full master library (including `.ai`, `.eps`, and `@4x`) is at `HBEF BRANDING/LOGOS/`.

| Lockup | When to use | Bundled file (light / dark-mode) |
|---|---|---|
| **Primary Lockup** (stacked) | **The default.** Use on most brand communications. | `HBEF-Primary_Lockup-RGB@2x.png` / `HBEF-Primary_Lockup-Dark_Mode-RGB@2x.png` |
| **Primary Lockup + Tagline** | When space allows and the mission needs stating — covers, posters, letterhead, first slide. | `HBEF-Primary_Lockup_Tag-RGB@2x.png` / `HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png` |
| **Secondary Lockup** (horizontal) | Wide, short spaces where the stacked lockup doesn't fit — email headers, banners, slide footers, letterhead. | `HBEF-Secondary_Lockup-RGB@2x.png` / `HBEF-Secondary_Lockup-Dark_Mode-RGB@2x.png` |
| **Logomark** (mark alone) | Highly restricted spaces only — merch, social avatars, favicons, spreadsheet corner marks. | `HBEF-Logomark.png`, `HBEF-Logomark-space.png` (padding built in) |

**Tagline (exact wording):** *Funding matters. Your donation, their future.*

### Color variations & formats

- **Standard color** — for light backgrounds. Use **RGB** files for digital screens, **CMYK** files for professional printing (CMYK lives in the master library only).
- **Dark Mode / solid white** — for dark backgrounds, i.e. anything placed on Navy `#0C3B5D` or Teal `#186892`. Never place the standard-color logo on a dark fill.
- **Black** — solid black version, strictly for grayscale print. Never for screen.
- **Raster vs vector** — `@1x` / `@2x` PNG for screen and Office documents; `.eps` / `.ai` from the master library for print, large format, and vendor hand-off.

### Clear space & sizing

- **Clear space = the height of the "HBEF" lettering**, maintained on all four sides. `HBEF-Logomark-space.png` has this padding pre-baked.
- **Never stretch, distort, rotate, recolor, add effects to, or reconstruct the logo.** Scale proportionally only.
- **Minimum sizes:** Primary/Secondary lockup ≥ 1.25" (120 px) wide; Logomark ≥ 0.4" (32 px). Below that, use the Logomark.
- Do not place the logo on a busy photograph without a solid or heavily scrimmed panel behind it.

---

## Brand Color Palette

Inspired by the coastal community. **Consistent use of these exact codes is required.** Source: HBEF Brand Guidelines 2026.

### Core Coastal Colors

| Token | Name | Hex | Usage |
|---|---|---|---|
| `HBEF_NAVY` | Navy | `#0C3B5D` | Primary brand element. Dominant backgrounds, major text, headings, table headers, structure. |
| `HBEF_TEAL` | Teal | `#186892` | Primary brand element and supporting headers. The mid-depth ocean blue. |
| `HBEF_TURQUOISE` | Turquoise | `#129FDA` | Energetic graphic elements and iconography. Also the "EDUCATION FOUNDATION" color in the wordmark. |

### School Colors & Warm Accents

| Token | Name | Hex | Usage |
|---|---|---|---|
| `HBEF_VIEW` | View (Yellow) | `#FFCD00` | **Calls-to-action, highlights, buttons.** The primary CTA color. |
| `HBEF_VISTA` | Vista (Golden Yellow) | `#FFA400` | Secondary highlights and energetic details. |
| `HBEF_VALLEY` | Valley (Orange) | `#EE7623` | Accent points that must draw immediate attention. |

> View, Vista and Valley are the three Hermosa Beach school names — Hermosa View, Hermosa Vista, Hermosa Valley. Use the color name, not just the hex, when writing for an internal audience.

### Neutrals & Backgrounds

| Token | Name | Hex | Usage |
|---|---|---|---|
| `HBEF_SKY` | Sky | `#B8D8EB` | Light backgrounds and spacious layouts. The default tinted section fill. |
| `HBEF_SAND` | Sand | `#DDC9A3` | Warm secondary background, for contrast against Sky. |
| `HBEF_WET_SAND` | Wet Sand | `#98989A` | Secondary text, metadata, subtle borders. |
| `HBEF_ASPHALT` | Asphalt | `#515962` | **Primary body copy** — a softer alternative to pure black. |
| `WHITE` | White | `#FFFFFF` | Content-card and page background. |

### Chart / Series Palette (categorical, max 6)

Use this order:

1. `HBEF_NAVY` `#0C3B5D` — series 1, headline metric
2. `HBEF_VALLEY` `#EE7623` — series 2
3. `HBEF_TEAL` `#186892` — series 3
4. `HBEF_VISTA` `#FFA400` — series 4
5. `HBEF_TURQUOISE` `#129FDA` — series 5
6. `HBEF_WET_SAND` `#98989A` — series 6 / "other"

**Single-series accent:** `HBEF_NAVY` for financials, endowment, IC reporting · `HBEF_VALLEY` for fundraising / donor / participation metrics · `HBEF_TEAL` for community / program / student-impact metrics.

### Functional colors (documents only — not part of the public brand)

| Token | Hex | Role |
|---|---|---|
| `SUCCESS` | `#4A8B5C` | Positive variance, grant approved, "on track." Muted civic green, never neon. |
| `WARNING` | `#FFA400` | Caution — reuses Vista. |
| `RISK` | `#B23A2D` | Material risk flags in IC / budget reporting. Grounded brick red. |
| `MUTED_BORDER` | `#D9D9D9` | Table cell borders, card outlines. |

### Contrast — the rule that gets broken most

Measured WCAG ratios on white: Navy 11.67:1 ✅ · Asphalt 7.11:1 ✅ · Teal 6.12:1 ✅ · Turquoise 3.00:1 (large text / underlined links only) · Valley 2.90:1 ❌ · Vista 1.99:1 ❌ · View 1.50:1 ❌ · Wet Sand 2.88:1 ❌ (metadata at 9pt+ only, never body copy).

- **View, Vista and Valley are fill colors, not text colors.** Navy on View is 7.77:1 ✅ AAA — that is the mandated CTA button treatment. Never set yellow or orange type on white.
- **On Sand `#DDC9A3`, set body copy in Navy, not Asphalt** (Asphalt on Sand is 4.38:1 — fails AA for normal text).
- **Underline Turquoise links** in HTML; color alone is not a sufficient cue at 3.00:1.

### Color usage rules

- **Navy carries the structure; the warm accents carry the action.** Headings, rules, dividers, table headers → Navy or Teal. CTAs, "Donate," "Register now" → **View `#FFCD00`**, with Valley `#EE7623` when the CTA must shout.
- **Teal and Turquoise are not interchangeable.** Teal `#186892` is structural (headers, rules). Turquoise `#129FDA` is graphic and energetic (icons, wave motifs, the wordmark's second line).
- **Sky and Sand are the tinted backgrounds.** Body content sits on White or Sky. Sand is the warm alternate — use one or the other in a given document, not both fighting each other.
- **Body text is Asphalt `#515962`,** not black. Reserve Navy for headings and emphasis.
- **One CTA color per surface.** Don't mix a View button and a Valley button on the same page.
- **Never use:** pure black `#000` for type, neon, hot pink, gradients across brand colors, drop shadows, or any color not in the tables above.

---

## Typography

Typography blends a sturdy, academic feel with modern, clean legibility.

### Primary typeface: **ALEO**

A contemporary slab serif — established, educational, friendly. Free via Google Fonts (`fonts.google.com/specimen/Aleo`). Bundled: `assets/fonts/Aleo-{Regular,Bold,Italic,BoldItalic}.ttf`.

**Usage:** all primary headings (H1, H2), prominent quotes, large display text, and the cover title.

### Secondary typeface: **LATO**

A warm, highly legible sans-serif. Free via Google Fonts (`fonts.google.com/specimen/Lato`). Bundled: `assets/fonts/Lato-{Light,Regular,Italic,Bold,BoldItalic,Black}.ttf`.

**Usage:** all body copy, paragraphs, website navigation, fine print, secondary subheadings, table cells, captions, and UI labels.

### Fallback chains

- **Aleo →** `Aleo, "Roboto Slab", "Zilla Slab", Rockwell, Georgia, serif` — always fall back to a **slab or serif**, never a sans.
- **Lato →** `Lato, "Helvetica Neue", Helvetica, Arial, sans-serif`.
- **Never use:** Times New Roman, Calibri, Comic Sans, script faces, Montserrat or BauhausBold (retired), or a monospace face outside a code/data block.

Both families are open-source (SIL OFL), so they can be installed and embedded freely in PDFs, HTML, and Office documents — a real change from the retired proprietary display face. Both are also native Google Fonts, so Google Docs/Slides/Sheets can use the real brand faces via the font picker's "More fonts" dialog.

> **Known variance:** HBEF's own letterhead template and the Strand Classic press release set body copy in **Aleo 12pt**, not Lato. The Brand Guidelines are authoritative — use **Aleo headings + Lato body** for new work. When editing one of those existing Word files in place, keep its native Aleo body so the document stays internally consistent, and note the variance to the requester.

### Document text hierarchy (Word / PDF — sizes in pt)

| Element | Font | Size | Weight | Color | Notes |
|---|---|---|---|---|---|
| Cover title | Aleo | 40 | Bold | `HBEF_NAVY` | Sentence or title case. Slab serif — do not letterspace. |
| Cover subtitle | Lato | 18 | Light (300) | `HBEF_TEAL` | Sentence case. |
| H1 section | Aleo | 24 | Bold | `HBEF_NAVY` | Space-before 24pt, space-after 8pt. |
| H2 sub-section | Aleo | 16 | Bold | `HBEF_TEAL` | Space-before 18pt, space-after 6pt. |
| H3 minor | Lato | 12 | Bold | `HBEF_NAVY` | Uppercase, letter-spacing +0.8pt. |
| Eyebrow / kicker | Lato | 9 | Bold | `HBEF_WET_SAND` | Uppercase, letter-spacing +1.2pt. |
| Body | Lato | 11 | Regular | `HBEF_ASPHALT` | Line-height 1.5. |
| Lead paragraph | Lato | 13 | Regular | `HBEF_ASPHALT` | First paragraph after H1; line-height 1.45. |
| Pull quote | Aleo | 15 | Italic | `HBEF_NAVY` | Indented 0.4"; 3pt `HBEF_VIEW` left border. |
| Caption / metadata | Lato | 9 | Italic | `HBEF_WET_SAND` | |
| Footnote / legal | Lato | 8 | Regular | `HBEF_WET_SAND` | |
| Table header | Lato | 10 | Bold | `WHITE` on `HBEF_NAVY` fill | Uppercase, letter-spacing +0.6pt. |
| Table cell | Lato | 10 | Regular | `HBEF_ASPHALT` | |
| Link | Lato | inherit | Regular | `HBEF_TURQUOISE` | Underlined in print-bound docs. |

### Presentation hierarchy (PPTX — sizes in pt)

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Cover title | Aleo | 54 | Bold | `HBEF_NAVY` on White, or `WHITE` on `HBEF_NAVY` |
| Cover subtitle | Lato | 20 | Light | `HBEF_TEAL` (or `HBEF_SKY` on navy) |
| Section divider title | Aleo | 40 | Bold | `WHITE` on `HBEF_NAVY` fill |
| Slide title | Aleo | 28 | Bold | `HBEF_NAVY` |
| Slide subtitle | Lato | 14 | Regular | `HBEF_WET_SAND` |
| Body / bullet | Lato | 16 / 14 | Regular | `HBEF_ASPHALT` |
| Pull-out stat | Aleo | 60 | Bold | `HBEF_NAVY` or `HBEF_VALLEY` |
| Stat label | Lato | 11 | Regular | `HBEF_WET_SAND` |
| Footer | Lato | 9 | Regular | `HBEF_WET_SAND` |

### Spreadsheet typography (XLSX — sizes in pt)

| Element | Font | Size | Weight | Color | Fill |
|---|---|---|---|---|---|
| Sheet title (row 1) | Aleo | 16 | Bold | `HBEF_NAVY` | `WHITE` |
| Section header | Lato | 12 | Bold | `WHITE` | `HBEF_NAVY` |
| Sub-header | Lato | 11 | Bold | `HBEF_NAVY` | `HBEF_SKY` |
| Data cell | Lato | 10 | Regular | `HBEF_ASPHALT` | `WHITE` (zebra `#F7FAFC`) |
| Total row | Lato | 11 | Bold | `HBEF_NAVY` | `#E8F1F7` |
| Cell note | Lato | 9 | Italic | `HBEF_WET_SAND` | `WHITE` |

---

## Letterhead (the canonical layout)

HBEF's official letterhead is the reference for every formal document. Master files: `HBEF BRANDING/LETTERHEAD/` (`.dotx` template, `.docx` sample, `.pdf` proof). Start from `HBEF Letterhead.dotx` whenever possible rather than rebuilding.

```
[Top margin 2.0" — header zone]

  LEFT (logo ≈ 3.5" wide)                RIGHT (right-aligned, Lato Bold 9pt, HBEF_NAVY)
  Secondary lockup, with the tagline      1645 Valley Drive
  set beneath the wordmark                Hermosa Beach, CA 90254
                                          (blank line)
                                          hbef.org
                                          @hbef90254

[Body — 1.0" left/right margins, generous leading]

[Footer, centered, Lato Italic 8pt, HBEF_ASPHALT]
HBEF is a registered 501(c)(3) non-profit organization. Contributions are
tax-deductible to the extent allowed by law. Federal tax identification
number (EIN): 33-0522270
```

- **Page:** US Letter 8.5 × 11", portrait. Top margin **2.0"** (clears the header block), other margins **1.0"**.
- **Letter body order:** date · recipient block · salutation · paragraphs · "Sincerely," · name · title · phone · email.
- The 501(c)(3)/EIN footer line is **mandatory on every letterhead page and every donor-facing document.**

---

## Cover page pattern (multi-page deliverables)

```
[HBEF_NAVY band — full bleed across top third of the page]

  [centered in the band]
  Primary Lockup + Tagline, DARK MODE, 2.5" wide
  assets/logos/HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png

[White background — remainder of page]

  [Eyebrow — Lato Bold 9pt, HBEF_WET_SAND, uppercase, +1.2pt tracking]
  HERMOSA BEACH EDUCATION FOUNDATION · [DOCUMENT TYPE]

  [Title — Aleo Bold 40pt, HBEF_NAVY]
  The Document Title

  [Subtitle — Lato Light 18pt, HBEF_TEAL, sentence case]
  A short editorial subtitle

  [3pt accent rule, 1.5" wide, centered — color varies, see below]

  [Bottom — Lato 9pt, HBEF_WET_SAND]
  [Author] · [Date] · [Confidential — Board Working Document]

[Footer band, 0.25" tall, HBEF_VIEW (#FFCD00) fill, no text]
```

**Accent rule color by deliverable type:**

| Deliverable | Rule color |
|---|---|
| Annual Giving / donor-facing (default) | `HBEF_VIEW` `#FFCD00` |
| Event promo / recap — Hearts of Hermosa, Friendship Walk, Strand Classic | `HBEF_VALLEY` `#EE7623` |
| Investment Committee / endowment | `HBEF_TEAL` `#186892` |
| Technology Advisory Board / internal ops | `HBEF_TEAL` `#186892` |
| Board governance / minutes | `HBEF_NAVY` `#0C3B5D` |

---

## Section dividers (universal)

```
[HBEF_SKY (#B8D8EB) full-width band, 0.4" tall]

[Eyebrow — Lato Bold 9pt, HBEF_WET_SAND, uppercase, +1.2pt tracking]
PART 02

[Title — Aleo Bold 16pt, HBEF_NAVY]
Section Title

[2pt rule, 100% width, 12pt below title]
```

Rule color rotation across a long document: `HBEF_VIEW` → `HBEF_TEAL` → `HBEF_VALLEY` → `HBEF_TURQUOISE`, then loop.

---

## Iconography, imagery & motifs

- **Iconography:** thin-line, 1.5–2px stroke, `HBEF_NAVY` or `HBEF_TURQUOISE` on light backgrounds. Phosphor, Tabler, or Lucide are good open-source matches. Never 3D, glossy, or multicolor-gradient icons.
- **Brand motifs, used sparingly:** the sunburst ray fan (as a cropped corner or edge element — never a second full sun competing with the logo) and the two-tone wave (as a section-break rule or footer edge). Draw both as flat single-stroke or flat-fill SVG in brand colors. **Never** recolor, rotate, or crop the actual logomark to make a motif.
- **Imagery:** event photography and HBCSD classroom shots. Credit `Jennifer Faulk Photography` where her work is identifiable — she is the board photographer.
- **Never:** starbursts other than the brand mark, drop shadows, bevels, 3D effects, stock-photo "diverse business team" imagery, or clip art.

---

## Data visualization

- **Palette order:** Navy → Valley → Teal → Vista → Turquoise → Wet Sand (see Chart/Series above).
- **Gridlines:** `MUTED_BORDER` `#D9D9D9` at 0.75pt — barely visible.
- **Axes / labels:** Lato 9pt `HBEF_WET_SAND`; no axis lines on top or right (open frame).
- **Chart background:** White, sitting on a White or Sky section.
- **Annotation:** headline data point in `HBEF_NAVY` bold; everything else `HBEF_WET_SAND`. For donor-facing decks, headline in `HBEF_VALLEY` bold.
- **Benchmark / target lines:** dashed, `HBEF_WET_SAND`, small right-edge label in Lato 9pt italic.
- **No 3D, no shadows, no rainbow gradients, no pie charts with more than 5 slices.**

---

## Digital & social

Use the official channels consistently.

| Channel | Value |
|---|---|
| Website | **hbef.org** |
| Instagram | **@hbef90254** — instagram.com/hbef90254 |
| Facebook | **@hbef90254** — facebook.com/HBEF90254 |
| Mailing address | 1645 Valley Drive, Hermosa Beach, CA 90254 |
| Social avatar | `assets/logos/HBEF-Logomark.png` (or `HBEF-Primary_Lockup-RGB-sq.png` for square crops) |

The handle `@hbef90254` is identical across Instagram and Facebook — write it that way in copy.

---

## Output specs — print & digital

**Canva is the production tool of record.** Most finished HBEF collateral is assembled or finished in Canva. Generate the content, layout logic, copy, and color/type specs here; hand off to Canva for final production unless the deliverable is natively a `.docx` / `.pptx` / `.xlsx` / `.pdf`. When handing off, state the exact hex codes, the Aleo/Lato roles, and which logo file to place.

### Standing digital sizes

| Size (px) | Use |
|---|---|
| **1080 × 1350** | The workhorse — web, Surf Report, Instagram/Facebook feed, general social |
| **1080 × 1920** | Stories / Reels |
| **2400 × 800** | Event-page banner and newsletter header |

### Print production

| Piece | Trim size | Notes |
|---|---|---|
| Laminated poster | 36" × 24" | Landscape; the large-format standard |
| Foam board | 24" × 36" | Portrait; event signage, oversized check presentations |
| Poster | 11" × 14" | Campus/window posting |
| Letterhead | 8.5" × 11" | Use the `.dotx` template |
| Street banner | per city spec | Confirm the current Hermosa Beach spec before laying out |
| Step-and-repeat | per vendor spec | Logomark or Secondary lockup tiled; hold full clear space between tiles |

**Print rules:** 0.125" bleed on every trimmed edge · live text ≥ 0.25" inside trim · **300 DPI** at final size for anything held in the hand, **150 DPI** at final size for anything read at distance · export print as **CMYK** PDF/X using the CMYK `.eps` logos, screen as **sRGB** PNG using the RGB files · logo clear space = the height of the "HBEF" lettering on all four sides.

---

## Working with format skills

This is a brand-LAYER skill. File-construction mechanics live in the format skills. The workflow is always:

1. **Read this SKILL.md** to load the brand system.
2. **Read the matching reference in `references/`** for the target format.
3. **Read the format skill** (`docx`, `pptx`, `xlsx`, `pdf`, `canvas-design`, `frontend-design`) for construction patterns.
4. **Apply tokens** from `assets/brand-tokens.json`.
5. **Place the correct logo** from `assets/logos/` — light lockup on light, dark-mode lockup on Navy/Teal.
6. **Verify** by opening and inspecting the produced file before sharing.

### Example invocations

> "Build a one-pager on Q1 endowment performance for the IC"
> → this SKILL.md + `references/pdf-instructions.md` + `pdf` skill → Navy cover band, Teal accent rule, IC voice, benchmark table

> "Sponsor pitch deck for a prospective Diamond partner"
> → this SKILL.md + `references/pptx-instructions.md` + `references/voice-and-content.md` + `pptx` skill → cover, funding-gap story, tier benefits, ask slide with a View `#FFCD00` CTA

> "Spreadsheet tracking Hearts of Hermosa auction donations"
> → this SKILL.md + `references/xlsx-instructions.md` + `xlsx` skill → cover tab, Navy table headers, Sky sub-headers, palette-ordered summary chart

> "Annual Giving solicitation letter as a Word doc"
> → this SKILL.md + `references/docx-instructions.md` + `references/voice-and-content.md` + `docx` skill → letterhead layout, parent voice, $1K-per-child anchor, signature block, mandatory EIN footer

---

## Final guardrails

- **Nothing from the pre-2026 system.** No Montserrat, no BauhausBold, no `#0B4261`, no `#F79B32`, no `#75C4B9`, no old logo. See the rebrand notice at the top.
- **If a deliverable doesn't look civic-warm and community-coded, it's wrong.** Add whitespace. Lean on Navy + White + Sky, with the warm accents used deliberately. The brand is *neighborhood*, not *boutique* or *bank*.
- **Tax language is mandatory** on any donor-facing document: *"HBEF is a registered 501(c)(3) non-profit organization. Contributions are tax-deductible to the extent allowed by law. Federal tax identification number (EIN): 33-0522270."*
- **Multi-page footer pattern:** left = "Hermosa Beach Education Foundation · hbef.org," right = "Page N." Both Lato 9pt `HBEF_WET_SAND`, with a 1pt `HBEF_TEAL` top border.
- **Investment Committee deliverables** drop the parent voice: IC-meeting register, benchmark attribution, target-vs-actual deltas, peer-level internal authorship.
- **Technology Advisory Board deliverables** (the operator's FY 2026–27 seat) use peer-level internal authorship with a technology/operations frame — tooling, tracking, data hygiene, content automation, vendor evaluation. No parent-audience preamble, no donor register.
- **Never assert an operator affiliation with a community partner.** Nolan Murtha has **no** affiliation with Nolan Capital or any other HBEF community partner; the earlier claim was a surname coincidence and is false. Do not state, imply, hedge, or raise it as an open question. (Nolan Capital *is* a genuine Community Partner and may appear in sponsor lists — just never as connected to the operator.)
- **Sponsor tier nomenclature is exact:** *Brighter Benefactor* ($25K+), *Diamond* ($15K+), *Platinum* ($10K+), *Gold* ($6K+), *Silver* ($3.5K+), *Bronze* ($1.5K+). Don't rename, don't merge.
- **Distinguish HBEF from HVPTO** whenever both could be relevant. HBEF funds *programs* (staff lines, instructional offerings); HVPTO funds *enhancements* (supplies, equipment, field-trip buses, teacher grants). Complementary, not competitive.
- **Brand questions escalate to Deni Mileski** (text 310.748.7390 / deni@denilampe.com), HBEF's brand contact of record per the 2026 Guidelines.
- **When in doubt, read the project context** at `/Users/nolan/Projects/HBEF/HBEF/HBEF-Context.md` for verified facts about the org, financials, board, partners, and calendar.

