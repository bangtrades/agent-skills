# HBEF — Long-Form Colors & Fonts Reference

The full token system. The summary in `SKILL.md` covers 80% of use cases — read this when you need every shade, every exact size, every line-height value for precise programmatic generation.

## Source of Truth

All color and typography tokens here were extracted from **`https://hbef.org/wp-content/themes/hbef-2023/assets/main.css?ver=1.0.0`** (the live HBEF theme stylesheet) on 2026-05-26. The Montserrat font is loaded by HBEF via Google Fonts; BauhausBold is loaded from HBEF's own theme directory at `/wp-content/themes/hbef/assets/`. The BauhausBold WOFF and TTF files are bundled in this skill under `assets/fonts/`.

---

## Full Color Token Table

### Primary Brand

| Token | Hex | RGB | Role | Live CSS reference |
|---|---|---|---|---|
| `HBEF_NAVY` | `#0B4261` | 11, 66, 97 | Signature brand color. Header bar, primary navigation, mobile submenu, all H2 subheadings. | `.site-header { background-color: #0b4261 }`, `.hbef-events-subheading { color: #0B4261 }` |
| `HBEF_NAVY_DEEP` | `#124362` | 18, 67, 98 | Footer body text — a touch deeper than HBEF_NAVY. | `.site-footer { color: #124362 }`, `.site-footer__column a { color: #124362 }` |
| `HBEF_ORANGE` | `#F79B32` | 247, 155, 50 | Primary CTA. Donate button background, hover-state links, primary in-content link color, form submit button. | `.site-header-donate-btn { background-color: #f79b32 }`, `#main a { color: #f79b32 }` |
| `HBEF_TEAL` | `#75C4B9` | 117, 196, 185 | Secondary brand. Footer background, mobile-menu background. | `.site-footer { background-color: #75c4b9 }`, `.mobile-menu { background-color: #75c4b9 }` |
| `HBEF_TEAL_DISPLAY` | `#74C4B9` | 116, 196, 185 | Hero display H1, event-title links. (One-digit variant of HBEF_TEAL — render as same color.) | `.hbef-events-heading { color: #74C4B9 }`, `.hbef-events-event-title-heading { color: #74C4B9 }` |
| `HBEF_TEAL_MUTED` | `#417987` | 65, 121, 135 | Inline emphasis links, italic event date. | `a.dark-n-bold { color: #417987 }` |
| `HBEF_TEAL_MUTED_2` | `#407987` | 64, 121, 135 | Variant of HBEF_TEAL_MUTED used on event date text — treat as same color. | `.hbef-events-event-date { color: #407987 }` |
| `HBEF_YELLOW` | `#FAEF7A` | 250, 239, 122 | "Give now" highlight in footer column list — soft sunlight yellow. Use sparingly. | `.site-footer__column ul li:last-of-type a { color: #faef7a }` |
| `HBEF_PAGE` | `#E7E7E7` | 231, 231, 231 | Site-wide page background behind all content cards. | `body { background-color: #e7e7e7 }` |
| `WHITE` | `#FFFFFF` | 255, 255, 255 | All content-card backgrounds. | `.hbef-events-container { background-color: #fff }` |

### Extended Functional

| Token | Hex | RGB | Role |
|---|---|---|---|
| `INK` | `#1A1A1A` | 26, 26, 26 | Default body-text color — slightly warmer than pure black. |
| `INK_80` | `#333333` | 51, 51, 51 | Heavy body emphasis (bold runs, key data). |
| `INK_60` | `#5C5C5C` | 92, 92, 92 | Secondary text — captions, footnotes, table notes, metadata. |
| `INK_40` | `#999999` | 153, 153, 153 | De-emphasized text (placeholder hints, expired-event labels). |
| `INK_30` | `#A8A8A8` | 168, 168, 168 | Tertiary text and thin rules. |
| `MUTED_BORDER` | `#CCCCCC` | 204, 204, 204 | Table cell borders, card outlines, soft divider strokes. |
| `SUCCESS` | `#5A9E78` | 90, 158, 120 | Positive variance, on-track status. Muted civic green — never neon. |
| `WARNING` | `#F79B32` | — | Reuses `HBEF_ORANGE` intentionally; the brand orange already carries urgency. |
| `RISK` | `#B23A2D` | 178, 58, 45 | Material risk flags only. Grounded brick red — never fire-engine bright. |

### Surfaces & Fills

| Token | Hex | Role |
|---|---|---|
| `SURFACE_PAGE` | `#E7E7E7` | Page-frame background (= `HBEF_PAGE`). Use under white content cards. |
| `SURFACE_CARD` | `#FFFFFF` | Content-card background (= `WHITE`). All body content sits here. |
| `SURFACE_SOFT` | `#F2F2F2` | Sub-header fill in spreadsheets, alt-row zebra. |
| `SURFACE_ZEBRA` | `#FAFAFA` | Lightest alt-row fill for dense tables. |
| `SURFACE_TOTAL` | `#E7E7E7` | Table total rows (= `HBEF_PAGE` — visually anchors the eye). |
| `SURFACE_HERO` | `#0B4261` | Cover-page hero band (= `HBEF_NAVY`). |
| `SURFACE_FOOTER` | `#75C4B9` | Footer-band fill (= `HBEF_TEAL`). |

---

## Full Typography Specification

### Font families (priority order)

**Primary text / UI:**
```
font-family: 'Montserrat', 'Avenir Next', 'Helvetica Neue', Arial, sans-serif;
```

**Display / cover / hero (BauhausBold first, geometric fallbacks):**
```
font-family: 'BauhausBold', 'ITC Avant Garde Gothic', 'Century Gothic', 'Futura', 'Montserrat', sans-serif;
font-weight: 700;
```

**Italic editorial moments (event dates, pull quotes):**
```
font-family: 'Montserrat', 'Avenir Next', sans-serif;
font-style: italic;
font-weight: 700; /* hbef.org pairs italic with bold weight, not regular */
```

### Weight scale (Montserrat)

HBEF uses Montserrat's full weight range. Key weights:

| Weight | CSS value | Use |
|---|---|---|
| Extra Light | 200 | Display H0 hero — *the* signature thin-and-tall HBEF hero look |
| Light | 300 | Cover subtitles, large pull-out stats |
| Regular | 400 | Body, default |
| Medium | 500 | Submenu link items (de-emphasized navigation), light emphasis |
| Semibold | 600 | Primary navigation items |
| Bold | 700 | All headings, buttons, table headers, emphasis |
| Black | 900 | Donate-button label (`.site-header-donate-btn` is `font-weight: 900`) |

### Document hierarchy (precise spec — Word/PDF)

| Element | Family | Size (pt) | Weight | Tracking | Color | Line height | Space before | Space after |
|---|---|---|---|---|---|---|---|---|
| Cover title | BauhausBold or Montserrat | 42 | 700/900 | +1.5pt, UPPERCASE | `HBEF_NAVY` | 1.1 | — | 12pt |
| Display H0 hero | Montserrat | 54 | 200 | +1.0pt, UPPERCASE | `HBEF_TEAL` | 1.05 (56pt) | — | 18pt |
| H1 | Montserrat | 28 | 700 | +0.8pt, UPPERCASE | `HBEF_NAVY` | 1.15 | 24pt | 12pt |
| H2 | Montserrat | 18 | 700 | +0.5pt, UPPERCASE | `HBEF_NAVY` | 1.2 | 18pt | 9pt |
| H3 | Montserrat | 13 | 700 | +1.2pt, UPPERCASE | `HBEF_TEAL_MUTED` | 1.3 | 14pt | 6pt |
| Lead paragraph | Montserrat | 13 | 400 | 0 | `INK` | 1.5 (~19.5pt) | 0 | 12pt |
| Body | Montserrat | 11 | 400 | 0 | `INK` | 1.55 (~17pt) | 0 | 8pt |
| Body bold | Montserrat | 11 | 700 | 0 | `INK_80` | 1.55 | 0 | 8pt |
| Bullet | Montserrat | 11 | 400 | 0 | `INK` | 1.5 | 0 | 4pt |
| Caption | Montserrat | 9 | 400 italic | 0 | `INK_60` | 1.4 | 0 | 4pt |
| Pull quote | Montserrat | 16 | 400 italic | 0 | `HBEF_NAVY` | 1.4 | 12pt | 12pt |
| Footnote | Montserrat | 8 | 400 | 0 | `INK_60` | 1.3 | 0 | 2pt |
| Table header | Montserrat | 10 | 700 | +0.8pt, UPPERCASE | `WHITE` on `HBEF_NAVY` | 1.2 | — | — |
| Table cell | Montserrat | 10 | 400 | 0 | `INK` | 1.3 | — | — |
| Table notes | Montserrat | 9 | 400 italic | 0 | `INK_60` | 1.3 | — | — |
| Event date | Montserrat | 13 | 700 italic | 0 | `HBEF_TEAL_MUTED` | 1.4 | — | 6pt |

### Presentation hierarchy (PPTX)

| Element | Family | Size (pt) | Weight | Color | Notes |
|---|---|---|---|---|---|
| Cover title | BauhausBold or Montserrat | 60 | 700/900 | `HBEF_NAVY` on `WHITE` (or `WHITE` on `HBEF_NAVY`) | Uppercase, +2pt tracking |
| Cover subtitle | Montserrat | 22 | 200 | `HBEF_TEAL` | Sentence case |
| Section divider title | Montserrat | 44 | 700 | `WHITE` on `HBEF_NAVY` fill | Uppercase, +1pt tracking |
| Slide title | Montserrat | 28 | 700 | `HBEF_NAVY` | Uppercase, +0.8pt tracking |
| Slide subtitle | Montserrat | 14 | 400 | `INK_60` | Sentence case |
| Body | Montserrat | 16 | 400 | `INK` | 1.4 line height |
| Bullet | Montserrat | 14 | 400 | `INK` | 1.35 line height |
| Pull-out stat | Montserrat | 60 | 200 (light) | `HBEF_NAVY` or `HBEF_ORANGE` | Letterforms tall and airy |
| Stat label | Montserrat | 11 | 400 | `INK_60` | Uppercase, +1pt tracking |
| Footer | Montserrat | 9 | 400 | `INK_60` | |
| Page number | Montserrat | 9 | 700 | `HBEF_NAVY` | |

### Spreadsheet hierarchy (XLSX)

| Element | Family | Size (pt) | Weight | Color | Fill |
|---|---|---|---|---|---|
| Workbook title | Montserrat | 18 | 700 | `HBEF_NAVY` | `WHITE` |
| Section header | Montserrat | 12 | 700 | `WHITE` | `HBEF_NAVY` |
| Sub-header | Montserrat | 11 | 700 | `HBEF_NAVY` | `SURFACE_SOFT` (`#F2F2F2`) |
| Data | Montserrat | 10 | 400 | `INK` | `WHITE` |
| Data (zebra) | Montserrat | 10 | 400 | `INK` | `SURFACE_ZEBRA` (`#FAFAFA`) |
| Total row | Montserrat | 11 | 700 | `HBEF_NAVY` | `SURFACE_TOTAL` (`#E7E7E7`) |
| Negative number | Montserrat | 10 | 400 | `RISK` | (cell fill) |
| Positive variance | Montserrat | 10 | 400 | `SUCCESS` | (cell fill) |
| Cell note | Montserrat | 9 | 400 italic | `INK_60` | `WHITE` |

---

## Type-pairing rules

- **BauhausBold + Montserrat 200 light.** This is the signature HBEF combo — heavy-and-geometric over thin-and-airy. Use for cover pages and major section dividers.
- **Montserrat 700 + Montserrat 400.** The workhorse pairing for headings + body across docx / pptx / xlsx.
- **Montserrat 700 italic + Montserrat 400.** Reserve italic for event dates and pull quotes — not running emphasis.
- **Never:** mix Montserrat with another sans-serif (Helvetica, Arial, Open Sans) on the same surface. The fallback chain only kicks in when Montserrat literally isn't available.
- **Never:** pair Montserrat with a serif body face. HBEF doesn't use serifs.

---

## Tracking / letter-spacing conventions

| Surface | Tracking |
|---|---|
| All UPPERCASE headings | +0.5 to +1.5pt depending on size (larger = less tracking) |
| Body running text | 0 (default) |
| All-caps captions / eyebrows | +1.2pt minimum |
| Donate-button label / CTA | +3pt (matches hbef.org `letter-spacing: 3px` on `.site-header-donate-btn`) |
| Display H0 hero | +1.0pt — keeps the 200-weight readable at 54pt+ |

---

## Color-blindness & accessibility notes

- `HBEF_NAVY` on `WHITE`: AAA contrast at all sizes — safe for all body text and headings.
- `HBEF_ORANGE` on `WHITE`: ~3.5:1 contrast — *fails* WCAG AA for body text. Use `HBEF_ORANGE` only on UI elements ≥14pt bold (buttons, headings), never for paragraph copy on white.
- `HBEF_TEAL` on `WHITE`: ~2.5:1 — *fails* AA. Use teal text only at ≥18pt for hero displays. Don't use teal for body text.
- `WHITE` on `HBEF_NAVY`: AAA — safe for all sizes.
- `INK_60` on `WHITE`: AA at body sizes (~7:1).
- For inline links on white, prefer `HBEF_NAVY` with underline over `HBEF_ORANGE` (hbef.org's choice of orange links is a brand quirk — it works on the site because of large font sizes, but in a document context navy reads better).
