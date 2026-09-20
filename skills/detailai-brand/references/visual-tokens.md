# DetailAI — Visual Tokens

Source: firecrawl branding extraction of https://www.detailai.ai/ (2026-08-10, confidence 0.9).

## Palette

| Token | Hex | Role |
|---|---|---|
| `--dai-black` | `#0A0A0A` | Canvas/background everywhere; primary-button TEXT color |
| `--dai-cream` | `#F4EDE2` | Primary text on dark; light-mode paper color |
| `--dai-gold` | `#C9A36A` | Accent: primary CTA fill, ◆ bullets, key numerals. SCARCE (≤10% surface) |
| `--dai-stone` | `#BEB7A9` | Links, muted/secondary text |
| `--dai-input-bg` | `#111110` | Input/card fill |
| `--dai-input-border` | `#1D1914` | Input/card border |
| `--dai-bronze` | `#564730` | Secondary-button border |

Functional colors (extension for app UI — not on marketing site): success `#7BA05B` (sage, keep warm), warn `#C9A36A` (reuse gold), danger `#B05C4A` (terracotta, never pure red).

## Typography

- **Display/headings:** Cormorant Garamond (fallback Playfair Display → Georgia → serif). Weight 500–600. High contrast, large: h2/display ~60px desktop, tight leading (~1.05), slight negative tracking.
- **Body/UI:** Inter (→ -apple-system stack). 20px body on marketing, 14–16px in app UI.
- **Eyebrow:** Inter, 12–14px, uppercase, letter-spacing 0.08–0.12em, color `--dai-stone` or `--dai-gold`.
- **Signature move:** small eyebrow (the site's literal h1 is 16px) above a huge serif display line. Reuse this hierarchy in decks and docs: tiny uppercase kicker → giant serif statement.
- Self-host or embed fonts; never load Google Fonts at runtime in shipped surfaces.

## Components

- **Primary button:** gold fill `#C9A36A`, black text, pill (border-radius 9999px), no shadow. Label style: "Request private demo".
- **Secondary button:** black fill, cream text, 1px bronze `#564730` border, pill.
- **Containers/sections:** 0px radius, hard edges, generous vertical whitespace (4px base unit; sections 96px+ apart).
- **Inputs/cards:** `#111110` fill, `#1D1914` border, 8px radius.
- **Lists:** gold diamond ◆ bullets, not discs or dashes.
- **No shadows anywhere.** Depth via contrast and spacing only.
- **Motion (web):** slow, scroll-driven reveals; animated SMS thread as the canonical proof device.

## Layout

- Max width 1200px, content column ~800px, 4px spacing base (scale 4/8/12/16/24/32/48/64/96).
- Dark canvas default. Light variant = cream `#F4EDE2` paper, `#0A0A0A` text, gold scarce.

## Logo

Wordmark only: "DetailAI" set in the display serif (Cormorant Garamond, weight 500-600), cream on black or black on cream. No icon mark or favicon exists yet — do not invent one ad hoc; flag to bang if a mark is needed. OG image: https://detailai.ai/og-image.png (1200×630).

## Office-format translations (pptx/docx/xlsx)

- Slide/page background: `#0A0A0A`; text `#F4EDE2`; accents/numerals `#C9A36A`.
- Fonts: Cormorant Garamond → if unavailable in the render environment, Playfair Display, then Georgia. Body: Inter → Calibri as last resort.
- Tables: no gridlines; hairline rules in `#1D1914`; header row text in gold, uppercase Inter.
- Charts: cream/stone series, single gold series for THE number; dark plot background; no gradients.
