# BT Equity Report — Brand Guide

The BT Stock Report aesthetic is a minimalist Pages-style template. Quiet, dense,
opinionated, easy to scan. Every primitive in this guide is already implemented in
`assets/build_report.js` — this document is the reference so you can reason about why
each piece is the way it is, and so you don't accidentally drift.

## Color Palette

| Token       | Hex      | Usage |
|-------------|----------|-------|
| `ink`       | `2F2F2F` | Body text, headings — slightly softer than pure black |
| `subtle`    | `8A8A8A` | Subtitles, section taglines, source-block prose |
| `hairline`  | `D6D3CC` | Dividers, card borders, table grid lines |
| `card`      | `F3F0E8` | Snapshot/Quarter card fill — warm off-white |
| `cardAlt`   | `EFE7D2` | Alt card fill (rarely needed; reserved for emphasis) |
| `amber`     | `D4A017` | The signature accent — dots, bullets, ascending headlines |
| `amberDk`   | `A07910` | Darker amber for hover/active states (rare in PDF) |
| `bull`      | `2F7A4A` | Bull-case PT cells, +% returns |
| `bear`      | `B04A2F` | Bear-case PT cells, −% returns, danger flags |
| `base`      | `6B6B6B` | Base-case PT cells, neutral middle ground |

**Usage discipline:** amber is the only accent color used decoratively. Never use it for
body text. Bull/Bear/Base appear only in the Scenario PT table and analyst PT cells.

## Typography

- **Font:** `Helvetica Neue` (across the stack — title, body, tables, footer)
- **No serif body.** Slab serifs feel "research-y" but break the minimalist Pages look.
- **No condensed weights.** The default Helvetica Neue weights handle the hierarchy.

### Size scale (docx half-points)

| Token   | Half-pts | Render | Usage |
|---------|----------|--------|-------|
| title   | 44       | 22pt   | The big "VIAV" / "P" / "CAR" ticker block |
| section | 26       | 13pt   | H1 — page section headers |
| sub     | 22       | 11pt   | H2 — subsection / card title |
| tagline | 22       | 11pt   | Subtitle line under the ticker |
| body    | 20       | 10pt   | Body paragraphs |
| small   | 18       | 9pt    | Card row labels/values, table cells |
| micro   | 16       | 8pt    | Sources block, disclaimer |
| nano    | 14       | 7pt    | Reserved (rarely used) |

The build template (`assets/build_report.js`) defines these as a `SZ` object. Don't
introduce new sizes — pick from the existing scale.

## Layout primitives

### The amber-dot row

Three amber dots, descending size (28/22/18 half-points). Appears at the top of every
page above the ticker. Defined as `AmberDots()` in the template. **This is the brand
mark.** Never replace with a logo, never recolor, never reorder.

```js
new TextRun({ text: '●', font: FONT, color: COLOR.amber, size: 28 }),
new TextRun({ text: '  ', font: FONT, size: 16 }),
new TextRun({ text: '●', font: FONT, color: COLOR.amber, size: 22 }),
new TextRun({ text: '  ', font: FONT, size: 16 }),
new TextRun({ text: '●', font: FONT, color: COLOR.amber, size: 18 }),
```

### The ticker block

Big, bold, character-spaced (60). The ticker is the page identity.

```js
new TextRun({
  text: ticker, font: FONT, bold: true, color: COLOR.ink, size: SZ.title,
  characterSpacing: 60,
})
```

### The subtitle hairline

A subtle gray line of subtitle text with a hairline border underneath. Sets the page
context (e.g., "Variant perception · scenario price targets · capital structure").

### The card

Snapshot and Quarter cards on page 1. Hairline-bordered table cell with `F3F0E8` fill
and 200/200/240/240 margins. Inside: a card title in `sub` size, then `cardRow(label, value)`
rows with right-aligned values via tab stops at position 4300.

### The two-column hero

Page 1 is built around a borderless 2-column table:

- Left column (5280 DXA): Core View paragraph
- Right column (4800 DXA): Snapshot card + spacer + Quarter card

The hero table row uses `cantSplit: true` to keep both columns on the same page. **Don't
put bullets inside the hero columns** — bullets break ungracefully across pages. Put
bullet sections (Why It Matters Now) BELOW the hero, full-width.

### Tables

All structured data uses `buildTable({ rows, columnWidths, header })`:

- Top + bottom borders only (hairline)
- Header row has `cardAlt` fill, bold text
- All rows use `cantSplit: true` to prevent mid-row page breaks
- Body cells have 80/80/100/100 margins
- First column auto-bolds (it's the row label/key)

### Amber bullets

Bullets render as amber `•` glyphs via docx's `numbering` config — NOT unicode bullets
in the text. The numbering reference is `amber-bullets`, level 0, indent 360 / hanging 220.

```js
const Bullet = (text) =>
  new Paragraph({
    numbering: { reference: 'amber-bullets', level: 0 },
    spacing: { after: 80, line: 280 },
    children: [new TextRun({ text, font: FONT, color: COLOR.ink, size: SZ.body })],
  });
```

### Page transitions

**Use `pageBreakBefore: true`** on the AmberDots paragraph at the start of each new
section page (pages 2–5). **Do not** use standalone `new PageBreak()` paragraphs — they
create blank pages when prior content already overflows naturally.

### Headers (H1, H2)

Both have `keepNext: true` so they don't orphan from the content below. H1 has 160
before / 80 after spacing; H2 has 120 / 60.

## Page geometry

- **Page size:** US Letter (12240 × 15840 DXA = 8.5" × 11")
- **Margins:** 1080 DXA top/right/bottom/left (~0.75")

## What NOT to do

- **No emoji in headings or body.** The amber dots are the only graphic accent.
- **No drop caps.** Pages-style is clean; no decorative typography.
- **No mid-page section dividers.** Hairline rules appear only under the subtitle and
  above the sources block.
- **No icons or charts inside the PDF.** If you need to show data, use a table. (Charts
  are fine in the markdown companion if it helps Obsidian readers.)
- **No color shifts mid-section.** A bull-case anchor stays bull-color throughout the row;
  don't mix bull-color and ink-color in the same cell.

## Why the brand looks like this

- **Dense + minimal** — the audience is bang and people he sends reports to. They are
  numerate, time-poor, and skim. White space + amber accents direct the eye to the
  variant perception, scenario PT, and capital structure tables.
- **Pages-style** rather than Bloomberg-Terminal-style — this is meant to feel
  thoughtful, not market-data-noisy. The aesthetic signals: this is a thesis, not a
  data dump.
- **Single accent color** — amber works because it's warm, distinctive, not corporate.
  The hairline grays carry the structural work.
