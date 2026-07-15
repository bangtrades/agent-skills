# Sense Neuro — Visual Tokens

Extracted 2026-06-18 via live computed-style inspection of senseneuro.com (Divi 4.24.1 build by Node Creative).

## Color palette

| Token | Hex | Role | Usage rule |
|---|---|---|---|
| `--sn-blue` | `#008ED1` | Primary brand blue (bright medical cyan-blue) | Primary accent, links, key UI, chart series 1 |
| `--sn-blue-deep` | `#004D71` | Deep blue | Section headers, dark accents, chart series 2 |
| `--sn-navy` | `#002A3A` | Darkest navy | Dark section backgrounds, heavy headings, footer |
| `--sn-blue-mid` | `#0073AA` | Mid blue | Secondary fills, hovers |
| `--sn-orange` | `#F39119` | CTA accent (warm orange) | **Primary buttons ONLY** — keep rare and intentional |
| `--sn-ink` | `#222222` | Heading text on light | H1–H4 |
| `--sn-body` | `#666666` | Body text gray | Paragraphs |
| `--sn-bg` | `#FFFFFF` | Page background | Default |
| `--sn-bg-alt` | `#F9F9F9` | Alt section background | Zebra sections |
| `--sn-hairline` | `#EEEEEE` | Dividers / borders | Hairlines, table rules |
| `--sn-white` | `#FFFFFF` | Reverse text | Text on blue/navy/orange |

**Discipline:** Blue is the system; orange is the exception. A page should read 90% blue/white/gray with orange appearing only on the single most important action. Never use orange for body text or large fills.

### Suggested chart ramp
`#002A3A` → `#004D71` → `#0073AA` → `#008ED1` → `#5FBDEE` (tint), with `#F39119` reserved to highlight a single "hero" data point.

## Typography

| Element | Font | Weight | Treatment |
|---|---|---|---|
| Headings (H1–H4) | **Open Sans**, Arial, sans-serif | 500 | Sentence case or Title Case; `#222222` on light, `#FFFFFF` on dark |
| Body / UI | **Nunito Sans**, Helvetica, Arial, sans-serif | 400 | `#666666`, ~16px, generous line-height (1.6) |
| Buttons | Open Sans | 700 | **UPPERCASE**, letter-spacing 1px |
| Eyebrow/labels | Open Sans | 600–700 | UPPERCASE, letter-spacing, often in `#008ED1` |

Fallback if Open Sans / Nunito Sans unavailable (e.g., in docx/pptx defaults): **Open Sans** → Calibri/Arial; **Nunito Sans** → Calibri/Arial. Prefer installing the real Google fonts for web/PDF.

## Components

**Primary button (signature element):**
- Background `#F39119`, text `#FFFFFF`, weight 700, UPPERCASE, letter-spacing 1px
- **Border-radius: 100px (full pill)**, padding 12px 36px, no border
- Hover: darken orange ~8% or shift to `#004D71`

**Secondary button:** outline style — 1–2px `#008ED1` border, `#008ED1` text, transparent bg, same pill radius.

**Section divider:** small decorative underline graphic sits under section titles (the site uses `div.png` rule marks). In rebuilds, a 48px × 3px `#008ED1` underline reproduces the effect.

**Cards / stats:** white card, hairline `#EEEEEE` border or soft shadow, blue checkmark or icon, large numeral in `#004D71`. The site's "2.5 seconds / 360 data points / entire cranial vault" stat row is the canonical pattern.

## Logo
Blue "Sense Neuro" wordmark (`Sense-Neuro-logo.png`). Keep clear space; place on white or very light backgrounds; use a white/reversed version on navy. Favicon = "Sense" icon mark.

## Imagery
Clinical + field photography (device on patient, ED/ambulance/military settings), brain/RF abstract motion for hero. Avoid stocky "smiling doctor" clichés; favor real device + setting. Blue-graded, high-clarity.
