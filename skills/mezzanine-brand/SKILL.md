---
name: mezzanine-brand
description: >-
  Mezzanine visual identity — palette, Austin + Söhne type, wordmark and maze icon rules — for every
  Mezzanine deliverable: website and product UI, HTML demos, Word/PDF documents, Excel workbooks,
  PowerPoint or Keynote decks, social tiles, email. Trigger whenever the user names Mezzanine,
  mezzanine.nyc, Gillian Williams, The Upper Deck, Talent Advisory, the red/paper/ink palette
  (#C72A09 / #EBE5DD / #141313), Austin or Söhne, the maze "MZ" icon, or asks for something
  "on-brand", "in the Mezzanine style", "with our logo/palette" — even without the word "brand".
  This is the brand LAYER: pair it with the format skill (pptx, docx, xlsx, pdf, frontend-design,
  epic-design, canvas-design). Read this file, then the one references/ file for your format.
---

# Mezzanine — brand layer

NYC recruitment and advisory firm for consumer brands in motion. Founder Gillian Williams. Look: quiet editorial, closer to a fashion house than a search firm. One red, warm paper, near-black ink. Serif display over grotesk body. Flat surfaces, square corners, no shadows, no decoration.

Source of truth: `Mezzanine_brandguideline.pdf` (©2025) and the logo kit in `/Users/nolan/Projects/Mezzanine/assets/`. Guide summary and gap review: `/Users/nolan/Projects/Mezzanine/docs/brand-identity.md`.

## Use

1. Read this file.
2. Read the reference for your format: `references/web.md` (site, app, HTML, email), `references/documents.md` (docx, pdf), `references/deck.md` (pptx), `references/spreadsheet.md` (xlsx), `references/imagery.md` (photos, generated plates, video).
3. Read the format skill for mechanics. This skill decides the look only.
4. Use logos from `assets/logo/`. Never redraw either mark.
5. Voice, claims discipline and service architecture live in the research skill `cortana-vault/research/brand-recon/mezzanine/mezzanine-brand/references/`. Read `positioning-and-claims.md` before any copy that names clients or results.

## Colour

| Token | HEX | RGB | CMYK | PMS | Role |
|---|---|---|---|---|---|
| Red | `#C72A09` | 199 42 9 | 15 96 6 100 | 7626 C | Signature. Wordmark, one display moment per surface, full-bleed panels |
| Orange | `#D9662E` | 217 102 46 | 11 72 96 1 | 7578 C | Accent only. Hover, rules, chart series. Never text on paper |
| Paper | `#EBE5DD` | 235 229 221 | 7 7 11 0 | Warm Gray 1 C | Default page ground |
| Ink | `#141313` | 20 19 19 | 73 67 66 81 | Black 6 C | Text; dark surfaces |

Support tones (derived, web only): rule `#DDD5C9`, muted text `#6E6862`, red-hover `#8C1D06`, lifted ink `#2B2828`, light paper `#F4F0EA`. Interior card surfaces may be `#FFFFFF`; page ground never is. Pure `#000000` is never used.

Pairings (WCAG ratio): ink on paper 14.8 (all text) · paper on ink 14.8 · red on paper 4.5 (display and text ≥ 18 px; 16 px body is borderline, avoid) · ink on red 3.3 (display ≥ 24 px or bold ≥ 19 px) · orange on ink 5.2 (small text on dark only) · orange on paper 2.9 (no text) · orange on red 1.6 (never).

Rule: red is a statement, not a wash. One dominant red field per page, slide or screen. Everything else sits on paper or ink.

## Type

**Austin** (Commercial Type) — editorial serif. Headlines, statements, narrative, long-form, pull quotes. Weights: Light, Roman, Medium, Semibold, Bold, Extrabold, Fat, Ultra + italics. Default: Roman or Light; Medium for dense decks.

**Söhne** (Klim) — grotesk. Body, UI, captions, labels, tables, numbers. Weights (German names): Extraleicht 200, Leicht 300, Buch 400, Kräftig 500, Halbfett 600, Dreiviertelfett 700, Fett 800, Extrafett 900 + Kursiv. Default: Buch; Halbfett for emphasis; Leicht for large supporting text.

Installed on the Mac: `~/Library/Fonts/Austin/` and `/Library/Fonts/Söhne/` (OTF; Office, Keynote, Pages, Numbers and Illustrator can use them directly). Source zips: `/Users/nolan/Projects/Mezzanine/assets/Header Font-*.zip`, `Body Font-*.zip`. Desktop licence confirmed for Austin (EULA in zip); web-embed rights unconfirmed for both. Until confirmed, web builds ship fallbacks and keep `@font-face` slots commented.

Fallbacks: Austin → Playfair Display → Georgia. Söhne → Inter → system sans. Never a slab, geometric display, or rounded face.

Tracking: default (0). Adjust only for balance; eyebrows and nav in Söhne caps at +0.1 em. Leading scales with size: display 0.95–1.05, headings 1.1–1.2, body 1.5. Guide reference pair: Austin Roman 90 pt / 95% with Söhne Light 35 pt / 120%.

Wordmark is MEZZANINE in Austin caps. Eyebrows are Söhne caps, 11–12 px, +0.1 em, muted or red.

## Logos

Two marks, bundled in `assets/logo/`: wordmark (`wordmark-ink|red|white.png`, 1600×308) and the maze icon (`icon-ink|red|white.svg` and `.png` 512). Motion: `assets/motion/icon-red-on-ink.mp4` and `icon-ink-on-red.mp4` (1920×1080, 5.25 s, icon draws in as one stroke; background baked in). Master files (AI, EPS, PDF, 8000 px JPG): `/Users/nolan/Projects/Mezzanine/assets/• VISUAL IDENTITY/`.

- Colour by ground: ink on paper, ink on red, white or paper on ink, red on paper. Ink icon on red is the guide's own closing mark.
- Wordmark clear space: `x` on all sides, x = stem width of the M (50.8 px at 3216 px width, about 1.6% of wordmark width). Give more when possible.
- Icon minimum: 42 px tall on screen, 10 mm in print. Give the icon clear space equal to its bar thickness.
- Never alter, outline, stretch, recolour outside the palette, add effects, or reconstruct either mark. No wordmark in any face but Austin.
- Wordmark leads; icon is the secondary mark (favicon, corner sign-off, blind deboss, animation). Do not lock them up side by side; place one per zone.

## Layout habits

Paper ground, generous margins, narrow left rail for small Söhne notes, content set right or centred, thin `#DDD5C9` rules instead of boxes, square corners, no drop shadows. Red arrives as one panel, one word, or the wordmark. Dark mode is ink ground with paper text and red display type.

## Checks before delivery

Palette only (no off-palette greys, blues, gradients). Austin for display, Söhne for everything else. One red field per surface. Icon ≥ 42 px. Wordmark untouched. No client names or outcome claims without the claims register. Spelling: Mezzanine, mezzanine.nyc, Söhne with umlaut. Zero typos; this client reads everything.
