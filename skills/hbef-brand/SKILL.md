---
name: hbef-brand
description: "Hermosa Beach Education Foundation (HBEF) brand guide for generating consistent, on-brand documents. Use this skill whenever creating Word (.docx), PowerPoint (.pptx), Excel (.xlsx), PDFs, HTML reports, charts, Google Docs/Sheets/Slides, or Apple Pages/Numbers/Keynote files for HBEF, Hearts of Hermosa, the Skechers Friendship Walk, Moms' Night Out, the Annual Giving Campaign, or the HBEF Endowment / Investment Committee. Trigger when the user mentions HBEF branding, HBEF navy/teal/orange, Montserrat + Bauhaus typography, or asks for a document 'in the same style as' previous HBEF deliverables. Trigger when the user just says 'make this on-brand', 'apply the HBEF look', 'use our palette', or names an HBEF event. This skill is the brand LAYER — it pairs with format skills (docx, pptx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Read this SKILL.md AND the matching format reference before generating output."
---

# Hermosa Beach Education Foundation — Brand Skill

This skill defines the visual identity system, voice, and document-production patterns for any deliverable produced on behalf of the Hermosa Beach Education Foundation (HBEF). Every color, font, layout rule, and component pattern in this guide has been calibrated against the live brand surface at **hbef.org** (theme `hbef-2023`, `main.css` v1.0.0, Montserrat from Google Fonts + custom BauhausBold display face).

The goal: every PDF, deck, spreadsheet, Word doc, Google Doc, and Apple Pages file should look and feel like an extension of the HBEF homepage — coastal, civic, optimistic, parent-led, never corporate.

## When to read what

This SKILL.md is the brand-system core. For format-specific implementation, read the matching reference:

- **`references/docx-instructions.md`** — Read when creating Word documents (.docx). Cover page, headings, body, tables, callouts. Pair with the `docx` skill.
- **`references/pptx-instructions.md`** — Read when creating PowerPoint decks (.pptx). Slide layouts, cover, dividers, content patterns. Pair with the `pptx` skill.
- **`references/xlsx-instructions.md`** — Read when creating Excel workbooks (.xlsx). Sheet styling, tables, charts, dashboard tabs. Pair with the `xlsx` skill.
- **`references/pdf-instructions.md`** — Read when creating PDFs from HTML or Word source. Cover, watermarks, footer. Pair with the `pdf` skill.
- **`references/google-apple-docs.md`** — Read when creating Google Docs / Sheets / Slides or Apple Pages / Numbers / Keynote files. How to substitute fonts, when to export PDF instead, manual-paste styling recipes.
- **`references/colors-and-fonts.md`** — Long-form token reference (every named color, every shade, every type style, exact line heights). The summary below is sufficient for ~80% of jobs.
- **`references/voice-and-content.md`** — Editorial voice, signature phrases, what to say and what to avoid in donor-facing copy.

Read the brand SKILL.md first, then the format reference, then build. **Don't improvise hex values from memory — copy them from `assets/brand-tokens.json` or the tables below.**

---

## Brand DNA (one-paragraph north star)

HBEF is **"100% Volunteers | 100% Parents"** — a community-funded education foundation that bridges the gap state funding leaves behind for K–8 Hermosa Beach students. The brand is **coastal civic warm**: deep ocean navy anchored by a friendly Pacific teal and a sunset orange CTA. Visual language draws from beach-town iconography (sail, surf, pier, strand) without falling into kitsch. Typography is confident: a tall, light, uppercase Montserrat display setting, paired with a heavy Bauhaus-style geometric headline for civic gravitas. Documents should feel like a warm pitch from a neighbor at a school picnic — earnest, organized, optimistic, never slick. **If a layout reads corporate, generic, or "Beverly Hills," it's wrong** (HBEF's whole positioning is that they are *not* a Basic Aid district).

---

## Brand Color Palette

The palette has three layers: **primary brand** (the document workhorse anchored by hbef.org's header/footer/CTA), **extended accents** (functional UI, status), and **chart/series** (data-viz progression). Every hex below is sourced directly from `main.css` on hbef.org unless noted otherwise.

### Primary Brand Colors (the document core)

| Token | Hex | Role | Source |
|---|---|---|---|
| `HBEF_NAVY` | `#0B4261` | Primary brand color. Site header bar, primary navigation, mobile menu submenu, all subheading text. The signature HBEF deep ocean navy. | `main.css` — `.site-header` background, used 5× in core CSS |
| `HBEF_NAVY_DEEP` | `#124362` | Slightly deeper navy variant for footer body text. Use for high-density body text on white when default INK feels too soft. | `main.css` — `.site-footer` text color |
| `HBEF_ORANGE` | `#F79B32` | **Primary CTA / accent color.** Donate buttons, hover states, primary link color on white, form submit. The "Give Now" sunset orange. | `main.css` — `.site-header-donate-btn`, link hover, submit button — used 8× |
| `HBEF_TEAL` | `#75C4B9` | Secondary brand color. Footer background, mobile menu background, large-display H1 color. The Pacific teal that signals "community / coastal." | `main.css` — `.site-footer` background, `.mobile-menu` background |
| `HBEF_TEAL_DISPLAY` | `#74C4B9` | Identical-in-spirit teal used for event display headings (H1 at 54pt light) and event title links. Treat as alias for `HBEF_TEAL`. | `main.css` — `.hbef-events h1.hbef-events-heading`, h3 event titles |
| `HBEF_TEAL_MUTED` | `#417987` | Muted blue-teal for inline link emphasis (the "dark-n-bold" anchor style) and italic event date text. The grown-up cousin of HBEF_TEAL. | `main.css` — `a.dark-n-bold`, event date color (`#407987` rounding) |
| `HBEF_YELLOW` | `#FAEF7A` | Soft sunlight yellow. Reserved for "Give"-style highlight links and very sparing in-content sparkle. Never as a body fill. | `main.css` — footer "give" highlight |
| `HBEF_PAGE` | `#E7E7E7` | Page-frame background. The soft warm gray that sits behind every white content card on hbef.org. Use as section background under white cards. | `main.css` — `body { background-color }` |
| `WHITE` | `#FFFFFF` | Content-card background. All content blocks sit on white cards on top of `HBEF_PAGE`. | `main.css` — `.hbef-events-container` |

### Extended Functional Palette

| Token | Hex | Role |
|---|---|---|
| `INK` | `#1A1A1A` | Primary body text. Default paragraph color. (Slightly warmer than pure black.) |
| `INK_60` | `#5C5C5C` | Secondary text. Captions, footnotes, metadata, table notes. |
| `INK_30` | `#A8A8A8` | Tertiary text + thin rules. Dividers, faint borders. |
| `MUTED_BORDER` | `#CCCCCC` | Table cell borders, card outlines. |
| `SUCCESS` | `#5A9E78` | Positive variance (endowment YTD return beat benchmark), grant approval, "on track." A muted civic green — not neon. |
| `WARNING` | `#F79B32` | Caution flags reuse `HBEF_ORANGE` intentionally — the brand orange already carries CTA-urgency weight. |
| `RISK` | `#B23A2D` | Material risk flags in IC reports / budget overruns. A grounded brick red, never bright fire-engine red. |

### Chart / Series Palette (categorical, max 6)

Use this order — it holds together visually and respects the brand sequence:

1. `HBEF_NAVY` (`#0B4261`) — series 1, headline metric
2. `HBEF_ORANGE` (`#F79B32`) — series 2
3. `HBEF_TEAL` (`#75C4B9`) — series 3
4. `HBEF_TEAL_MUTED` (`#417987`) — series 4
5. `HBEF_NAVY_DEEP` (`#124362`) — series 5
6. `INK_60` (`#5C5C5C`) — series 6 / "other"

**Single-series accent:** always `HBEF_NAVY` for financials, endowment, IC reporting; `HBEF_ORANGE` for fundraising / donor / participation metrics; `HBEF_TEAL` for community / program-level / student-impact metrics.

### Color usage rules

- **Navy carries the structure, orange carries the action.** Headings, rules, dividers, table headers → `HBEF_NAVY`. CTAs, donate buttons, "register now" → `HBEF_ORANGE`. Don't swap them.
- **Teal is editorial, not structural.** Use `HBEF_TEAL` for hero display moments (cover H1, event title cards), not for table headers or paragraph emphasis.
- **One CTA color per page.** Don't mix orange CTA buttons with teal or navy CTAs on the same surface.
- **Cards on warm-gray.** Page background = `HBEF_PAGE` (#E7E7E7). Content sits inside `WHITE` cards. This is the hbef.org pattern — never put body content directly on the warm-gray background.
- **Never use:** pure black (`#000`), Beverly Hills gold, neon, electric blue, pink (HBEF is not a beauty brand), saturated red except for `RISK` flags.

---

## Typography

### Font families

- **Primary brand typeface: Montserrat** (Google Fonts, free, 100/200/300/400/500/600/700/800/900). Used everywhere on hbef.org for navigation, body, headings.
- **Display / civic-gravitas typeface: BauhausBold** (custom font included on hbef.org at `/wp-content/themes/hbef/assets/`). Geometric, heavy, used for the footer column headlines. This is **HBEF's signature display face** — equivalent to a brand's wordmark when used at scale.
- **Document fallback chain** (when Montserrat or BauhausBold aren't embeddable in the target format): `Montserrat, "Avenir Next", "Helvetica Neue", Arial, sans-serif`. For BauhausBold display moments use **`ITC Avant Garde Gothic`**, **`Century Gothic`**, or **`Futura`** as the closest geometric heavy fallback — never substitute a serif.
- **For programmatically generated docx/pptx/xlsx where embedding is complex:** specify **Montserrat** in styles. Most modern Windows/Mac installs have it. If unavailable, the chain falls through to Avenir Next / Helvetica Neue / Arial cleanly.
- **Never use:** Times New Roman, Calibri (too corporate-default), Comic Sans, any script face, any monospaced face unless it's a code/data block.

The BauhausBold font is included in this skill at `assets/fonts/` — copy it into any HTML/PDF build that needs to render headlines accurately on machines that don't have it installed.

### Document text hierarchy (Word / PDF — sizes in pt)

These mirror the hbef.org rendered hierarchy (`.hbef-events-heading` 54pt, `.hbef-events-subheading` 36pt, body 16px).

| Element | Font | Size | Weight | Color | Notes |
|---|---|---|---|---|---|
| Document title (cover) | BauhausBold *or* Montserrat 800 | 42 | Heavy | `HBEF_NAVY` | Uppercase, letter-spacing +1.5pt |
| Display H0 (hero) | Montserrat | 54 | Light (200) | `HBEF_TEAL` | Uppercase, letter-spacing +1.0pt — direct hbef.org H1 equivalent |
| H1 section | Montserrat | 28 | Bold (700) | `HBEF_NAVY` | Uppercase, letter-spacing +0.8pt, space-before 24pt |
| H2 sub-section | Montserrat | 18 | Bold (700) | `HBEF_NAVY` | Uppercase, letter-spacing +0.5pt, space-before 18pt |
| H3 minor | Montserrat | 13 | Bold (700) | `HBEF_TEAL_MUTED` | Uppercase, letter-spacing +1.2pt |
| Body | Montserrat | 11 | Regular (400) | `INK` | Line-height 1.55 |
| Lead paragraph | Montserrat | 13 | Regular (400) | `INK` | First paragraph after H1; line-height 1.5 |
| Caption / metadata | Montserrat | 9 | Italic | `INK_60` | |
| Pull quote | Montserrat | 16 | Italic | `HBEF_NAVY` | Indented 0.5", `HBEF_TEAL` left border 3pt |
| Footnote | Montserrat | 8 | Regular | `INK_60` | |
| Table header | Montserrat | 10 | Bold | `WHITE` on `HBEF_NAVY` fill | Uppercase, letter-spacing +0.8pt |
| Table cell | Montserrat | 10 | Regular | `INK` | |
| Table notes column | Montserrat | 9 | Italic | `INK_60` | |
| Event date (editorial) | Montserrat | 13 | Bold Italic | `HBEF_TEAL_MUTED` | Matches hbef.org event card styling |

### Presentation text hierarchy (PPTX — sizes in pt)

| Element | Font | Size | Weight | Color |
|---|---|---|---|---|
| Cover title | BauhausBold *or* Montserrat 800 | 60 | Heavy | `HBEF_NAVY` on `WHITE`, or `WHITE` on `HBEF_NAVY` |
| Cover subtitle | Montserrat | 22 | Light (200) | `HBEF_TEAL` |
| Section divider title | Montserrat | 44 | Bold | `WHITE` on `HBEF_NAVY` fill |
| Slide title | Montserrat | 28 | Bold | `HBEF_NAVY` |
| Slide subtitle | Montserrat | 14 | Regular | `INK_60` |
| Body | Montserrat | 16 | Regular | `INK` |
| Bullet | Montserrat | 14 | Regular | `INK` |
| Pull-out stat (large number) | Montserrat | 60 | Light (200) | `HBEF_NAVY` or `HBEF_ORANGE` |
| Stat label | Montserrat | 11 | Regular | `INK_60` |
| Footer | Montserrat | 9 | Regular | `INK_60` |

### Spreadsheet typography (XLSX — sizes in pt)

| Element | Font | Size | Weight | Color | Fill |
|---|---|---|---|---|---|
| Sheet title (row 1) | Montserrat | 16 | Bold | `HBEF_NAVY` | `WHITE` |
| Section header | Montserrat | 12 | Bold | `WHITE` | `HBEF_NAVY` |
| Sub-header | Montserrat | 11 | Bold | `HBEF_NAVY` | `#F2F2F2` |
| Data cell | Montserrat | 10 | Regular | `INK` | `WHITE` (zebra: `#FAFAFA`) |
| Total row | Montserrat | 11 | Bold | `HBEF_NAVY` | `#E7E7E7` (`HBEF_PAGE`) |
| Cell note | Montserrat | 9 | Italic | `INK_60` | `WHITE` |

---

## Brand Voice (any document with prose)

Match the homepage voice. Concrete phrasings live in `references/voice-and-content.md`. The short version:

- **Tagline anchors:** *"Funding matters. Your donation, their future."* · *"100% Volunteers | 100% Parents."* · *"It takes a village of 100%."* · *"Funding education. Empowering students. Strengthening community."*
- **Audience first.** Default audience = Hermosa Beach families and local-business sponsors. Speak like a neighbor at a school picnic, not a development officer in a board room.
- **Participation > amount.** 100% family participation is treated as a *moral* KPI on par with total dollars raised. Always include the participation framing alongside dollar asks.
- **Story of the gap.** When explaining the cause, lead with the structural funding gap (Hermosa is a Revenue Limit district, ~$6K per-student gap, ~5% of district budget covered by HBEF) — not with feelings.
- **Inclusive ask.** "Every dollar makes a real, tangible difference." Suggested family gift = $1,000 per enrolled child, but any amount welcomed. Never shame small donors.
- **HBEF vs HVPTO.** Anywhere a parent might be confused, distinguish: HBEF funds *programs* (staff lines, instructional offerings), HVPTO funds *enhancements* (supplies, equipment, field-trip buses, teacher grants). Complementary, not competitive.
- **Internal IC voice.** For Investment Committee outputs (endowment, allocation, performance), drop the parent voice and use peer-level portfolio-management register — benchmarks, allocations vs targets, attribution, peer comparison.
- **Never use:** "leverage," "synergy," "impactful" (just say "what it pays for"), "thoughts and prayers" energy, "rich district" framing (HBEF's whole identity is that they're not).

---

## Cover page pattern (universal across formats)

Every multi-page deliverable opens with a cover that reads:

```
[HBEF_NAVY band — full bleed across top third of page]

[centered horizontally in the navy band]
[HBEF wordmark — assets/logos/hbef-secondary-lockup-dark.png — 2.5" wide]

[White background — fills remainder of page]

[Centered, 9pt, INK_60, letter-spacing +1.2pt, uppercase]
HERMOSA BEACH EDUCATION FOUNDATION  ·  [DOCUMENT TYPE]

[Title in 42pt Montserrat Bold or BauhausBold, HBEF_NAVY]
The Document Title

[Subtitle in 22pt Montserrat Light, HBEF_TEAL]
A short editorial subtitle in sentence case

[3pt HBEF_ORANGE horizontal rule, 1.5" wide, centered]

[Bottom of page, 9pt, INK_60]
[Author] · [Date] · [Confidential — Board Working Document]

[Footer band, 0.25" tall, HBEF_TEAL fill, no text]
```

**Variant by deliverable type — accent rule color rotates:**
- **Annual Giving / donor-facing:** `HBEF_ORANGE` rule (default)
- **Investment Committee / endowment:** `HBEF_NAVY_DEEP` rule
- **Event recap / Hearts of Hermosa / Walk:** `HBEF_TEAL` rule
- **Board governance / minutes:** `HBEF_NAVY` rule

---

## Section dividers (universal)

Between major sections in long documents:

```
[HBEF_PAGE (#E7E7E7) full-width band, 0.4" tall]

[Tiny eyebrow, 9pt Montserrat, INK_60, uppercase, letter-spacing +1.2pt]
PART 02

[Title in 18pt Montserrat Bold, HBEF_NAVY, uppercase]
SECTION TITLE

[Single 2pt HBEF_ORANGE rule, 100% width, 12pt below title]
```

Section accent color rotation across a long doc: `HBEF_ORANGE` → `HBEF_TEAL` → `HBEF_TEAL_MUTED` → `HBEF_NAVY_DEEP`, then loop. Gives visual rhythm without inventing colors.

---

## Iconography & illustration

- **Iconography:** thin-line, 1.5px stroke, `HBEF_NAVY` or `INK_60` on light. Phosphor Icons, Tabler Icons, Lucide (in priority order) are good open-source matches. Never use 3D, glossy, or rainbow-colored icons.
- **Imagery:** prefer event photography from hbef.org's Photo Galleries when illustrating community moments; product/program shots from inside HBCSD classrooms when illustrating impact. Always credit `Jennifer Faulk Photography` if you can identify her work — she's the board photographer.
- **Decorative accents:** thin horizontal rules in brand colors; subtle wave/surf line motifs at section breaks (kept simple — single-stroke SVG, not photorealistic). Never starbursts, drop-shadows, or 3D effects.
- **Logos to use** (in this skill at `assets/logos/`):
  - `hbef-secondary-lockup-dark.png` — primary horizontal lockup, dark mode (for navy backgrounds)
  - `hbef-logo-vertical-dark.png` — vertical lockup with tagline (for square-ish placements like spreadsheet covers, footer)
  - `hbef-favicon.png` — circular favicon mark (for tiny placements only)

---

## Data visualization

When charting numbers in any format:

- **Chart palette order** (categorical, see Chart/Series above): `HBEF_NAVY` → `HBEF_ORANGE` → `HBEF_TEAL` → `HBEF_TEAL_MUTED` → `HBEF_NAVY_DEEP` → `INK_60`.
- **Single-series accent:** `HBEF_NAVY` for financials/endowment; `HBEF_ORANGE` for fundraising/participation; `HBEF_TEAL` for community/student-impact.
- **Gridlines:** `MUTED_BORDER` (`#CCCCCC`) at 0.75pt — barely visible.
- **Axes / labels:** `INK_60` 9pt, no axis lines on top/right (open frame).
- **Background:** `WHITE` chart background sitting on `HBEF_PAGE` section background.
- **No 3D, no shadows, no rainbow gradients.** Categorical only.
- **Annotation pattern:** highlight the headline data point in `HBEF_NAVY` bold; everything else stays `INK_60`. For donor-facing decks, highlight the headline in `HBEF_ORANGE` bold to reinforce CTA energy.
- **Benchmark / target lines:** dashed, `INK_30`, with a small label at the right edge in `INK_60` italic.

---

## Asset files (in this skill)

Bundled assets the format references will pull from:

- **`assets/brand-tokens.json`** — machine-readable token file. Every named color (`HBEF_NAVY`, `HBEF_ORANGE`, `HBEF_TEAL`, …) maps to its hex value, plus typography settings (font family chain, sizes, weights, line heights). Use when programmatically generating CSS, Word doc styles, Excel cell fills, etc.
- **`assets/brand-palette.css`** — copy-paste CSS variables block. Use for any HTML deliverable (dashboards, reports, presentations rendered to HTML before PDF).
- **`assets/color-swatches.html`** — visual reference. Open this in a browser to see every color rendered. Send to the user when they ask "what do the colors look like?"
- **`assets/logos/`** — Three HBEF logo files (primary lockup, vertical lockup, favicon). PNGs at 2× resolution.
- **`assets/fonts/`** — BauhausBold display face (`.woff` + `.ttf`). HBEF's custom font, downloaded from hbef.org. Embed in HTML/PDF; reference but-do-not-embed in docx/pptx (Office can't ship custom fonts safely).

---

## Working with format skills

This is a brand-LAYER skill. The mechanics of building each file format live in their dedicated skills. The workflow is always:

1. **Read this SKILL.md** to load the brand system into context.
2. **Read the matching reference in `references/`** for the format you're producing.
3. **Read the format skill** (`docx`, `pptx`, `xlsx`, `pdf`, etc.) for the file-construction code patterns.
4. **Apply the brand tokens** from `assets/brand-tokens.json` to the format skill's templates.
5. **Embed the logo** from `assets/logos/` on cover and footer where appropriate.
6. **Verify** the output by reading the produced file (open and inspect) before sharing.

### Example invocation patterns

> "Build me a one-pager on Q1 endowment performance for the IC"
> → read hbef-brand SKILL.md + `references/pdf-instructions.md` + the `pdf` skill → produce branded PDF with HBEF_NAVY cover band, HBEF_NAVY_DEEP rule, IC voice, performance vs benchmark table

> "Create a sponsor pitch deck for a prospective Diamond partner"
> → read hbef-brand SKILL.md + `references/pptx-instructions.md` + `references/voice-and-content.md` + the `pptx` skill → produce cover, the funding-gap story, tier benefits, ROI for sponsor, ask slide in HBEF_ORANGE

> "Spreadsheet that tracks Hearts of Hermosa auction donations"
> → read hbef-brand SKILL.md + `references/xlsx-instructions.md` + the `xlsx` skill → produce cover tab, donor table with HBEF_NAVY headers, totals row with HBEF_PAGE fill, summary chart in palette order

> "Annual Giving solicitation letter as a Word doc"
> → read hbef-brand SKILL.md + `references/docx-instructions.md` + `references/voice-and-content.md` + the `docx` skill → produce letterhead cover, parent-voice ask, $1K-per-child anchor, signature block, tax language footer

> "Put together a Google Doc agenda for the next board meeting"
> → read hbef-brand SKILL.md + `references/google-apple-docs.md` → produce manually-paste-ready styling, font-family fallback notes, exported-PDF option

---

## Final guardrails

- **If a deliverable doesn't look civic-warm and community-coded, it's wrong.** Add whitespace. Lean into navy + teal. The brand is *neighborhood*, not *boutique* or *bank*.
- **Tax language is mandatory** on any donor-facing document: *"HBEF is a registered 501(c)(3) non-profit organization. Contributions are tax-deductible to the extent allowed by law. Federal tax identification number (EIN): 33-0522270."*
- **Footer pattern** on multi-page docs: left = "Hermosa Beach Education Foundation · hbef.org," right = "Page N." Both in Montserrat 9pt `INK_60`, with a 1pt `HBEF_TEAL` top border.
- **Investment Committee deliverables** drop parent voice; use IC-meeting register with benchmark attribution and target-vs-actual deltas. The user (Nolan Murtha) sits on IC — treat IC outputs as peer authorship.
- **Sponsor recognition** lists must keep the tiered nomenclature exact: *Brighter Benefactor* ($25K+), *Diamond* ($15K+), *Platinum* ($10K+), *Gold* ($6K+), *Silver* ($3.5K+), *Bronze* ($1.5K+). Don't rename, don't merge tiers.
- **Distinguish HBEF from HVPTO** whenever both could be relevant. Common parent confusion point — clarify explicitly.
- **When in doubt, read the project context** at `/Users/nolan/Projects/HBEF/HBEF/HBEF-Context.md` for verified facts about the org, financials, board, partners, and calendar.
