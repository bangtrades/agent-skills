# WaiveLabs — Logos & Marks

## The bundled files (in this skill's `assets/`)

| File | Variant | Background | Use on |
|---|---|---|---|
| `waivelabs-logo.png` | Full color — dark wordmark + colored mark | transparent | **Light** surfaces: site header, letterhead, light docs, light slides |
| `waivelabs-logo-light.png` | White wordmark + colored mark | transparent | **Dark** surfaces: login card, dark footers, dark slides, the dusk theme |
| `icon-512.png` | Symbol-only mark, 512² | transparent | App icon, social avatar, large favicon, stamp |
| `favicon.ico` | Multi-size favicon | — | Browser tab |

Canonical web copies live in the site repo at `WaiveLabs/site/assets/` (same filenames). The full
asset registry (vector mark, Keynote wordmark source, exploration renders) is in the vault at
`cortana-vault/projects/waivelabs/waivelabs--brand-assets.md`. Prefer the **vector mark**
(`brand_assets/waivelabs-mark.svg`) when infinite scaling is needed (large print, signage).

## The mark — what it means

A **sunrise** (orange rays) cresting **blue waves that dissolve into a circuit / data-flow pattern**
(nodes + traces). One glyph carries the whole positioning: coastal South Bay dawn + the incoming AI
wave + agentic data plumbing. Wordmark: `WaiveLabs` in near-black, `.ai` in sunset orange.

## Lockups

- **Primary horizontal** — symbol left, `WaiveLabs.ai` wordmark right. Default for site header,
  letterhead, deck title bars, doc headers.
- **Symbol only** — square contexts where the wordmark won't read (favicon, avatar, stamp).
- **Stacked** — symbol above wordmark, for narrow/centered placements (cover slides, mobile).

## Usage rules

- **Clear space:** margin equal to the height of the "W" on all sides.
- **Minimum size:** 180 px digital / 1.25 in print.
- **Approved modes:** full color on white · reversed (white wordmark) on dark · one-color dark.
- **On dark backgrounds always use `waivelabs-logo-light.png`** — never the dark-wordmark file.
- **Transparency gotcha (learned the hard way):** ship logos with a TRUE transparent background,
  not a white fill. A white-filled PNG — even one *with* an alpha channel — renders as a white box
  over dark sections (it broke the live header once). The bundled files are clean transparent
  exports; if you're ever handed a white-bg file, matte it out before use.

## Don't

Stretch / distort · rotate · recolor the mark or wordmark · add drop shadows or effects · place
full-color on a busy or low-contrast background · rebuild the wordmark in a different typeface ·
ship a wordmark reading "WaveLabs" (verify the *i* in Wa·i·ve).
