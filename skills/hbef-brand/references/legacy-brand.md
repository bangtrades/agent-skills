# HBEF — Retired Pre-2026 Brand System

> ## ⛔ IDENTIFICATION AND MIGRATION ONLY
>
> **Every value, typeface, and asset on this page is RETIRED. None of it may appear in new work.**
>
> HBEF completed a full identity refresh in 2026. This file exists for exactly two purposes:
>
> 1. **Recognition** — so you can look at an old poster, deck, spreadsheet, or Word file and correctly identify it as pre-2026 rather than assuming it's a valid reference.
> 2. **Migration** — so you can map every old value to its 2026 replacement when updating an existing deliverable.
>
> **Do not** copy a hex from this page into a new document. **Do not** set type in Montserrat, BauhausBold, or AmsiPro. **Do not** pull an asset from `/Users/nolan/Projects/HBEF/HBEF BRANDING/Z PRIOR BRANDING - DO NOT USE/`. If you catch yourself reaching for a value here to *build* something, stop — go to `SKILL.md` and `references/colors-and-fonts.md` instead.
>
> If a user asks for something "in the old HBEF style" or "matching last year's flyer," the correct response is to build it in the **2026** system and say why. The rebrand is not optional and there is no grandfather clause for new work.

---

## 1. Why this system was retired

The pre-2026 identity was never a formally documented brand system. It was a set of conventions accreted across three logo generations (pre-2021, 2021, 2021–2023) and reverse-engineered from the live WordPress theme at `hbef.org/wp-content/themes/hbef-2023/assets/main.css`. Colors were extracted from CSS rules, not from a guidelines document. Two near-identical teals (`#75C4B9` / `#74C4B9`) and two near-identical muted teals (`#417987` / `#407987`) coexisted because they were typos in the stylesheet, not deliberate tokens.

The 2026 refresh replaced this with an actual **`HBEF Brand Guidelines 2026`** document, a released logo library with RGB/CMYK/dark-mode/black variants, an official letterhead template, and a named palette tied to the three Hermosa Beach school names (View, Vista, Valley).

**Practical upshot:** anything that cites the hbef-2023 theme CSS as its source is legacy. Anything that cites `HBEF Brand Guidelines 2026` is current.

---

## 2. The retired palette

Contrast ratios below are vs. White `#FFFFFF`, computed per WCAG 2.x — included because several of these colors were accessibility problems, which is part of why they went away.

### 2.1 Primary brand (retired)

| Retired token | Hex | RGB | Old role | Contrast vs White |
|---|---|---|---|---|
| `HBEF_NAVY` | `#0B4261` | 11, 66, 97 | Signature brand color. Site header bar, primary navigation, mobile submenu, all H2 subheadings. | 10.68:1 |
| `HBEF_NAVY_DEEP` | `#124362` | 18, 67, 98 | Footer body text — a hair deeper than the main navy. A distinction nobody could see. | 10.47:1 |
| `HBEF_ORANGE` | `#F79B32` | 247, 155, 50 | **The old primary CTA.** Donate button, hover-state links, in-content link color, form submit. | 2.17:1 ❌ |
| `HBEF_TEAL` | `#75C4B9` | 117, 196, 185 | Secondary brand. Footer background, mobile-menu background. A mint/seafoam, **not** a deep ocean blue. | 2.03:1 ❌ |
| `HBEF_TEAL_DISPLAY` | `#74C4B9` | 116, 196, 185 | Hero display H1, event-title links. One-digit variant of the above — a stylesheet typo, rendered as the same color. | 2.03:1 ❌ |
| `HBEF_TEAL_MUTED` | `#417987` | 65, 121, 135 | Inline emphasis links, italic event dates. | 4.87:1 |
| `HBEF_TEAL_MUTED_2` | `#407987` | 64, 121, 135 | Variant of the above used on event-date text. Also a typo. | 4.88:1 |
| `HBEF_YELLOW` | `#FAEF7A` | 250, 239, 122 | "Give now" highlight in the footer column list. Soft sunlight yellow. | 1.19:1 ❌ |
| `HBEF_PAGE` | `#E7E7E7` | 231, 231, 231 | **Site-wide gray page background** behind all white content cards. | 1.24:1 |
| `WHITE` | `#FFFFFF` | 255, 255, 255 | All content-card backgrounds. | 1.00:1 |

### 2.2 Extended functional (retired)

| Retired token | Hex | RGB | Old role | Contrast vs White |
|---|---|---|---|---|
| `INK` | `#1A1A1A` | 26, 26, 26 | Default body text — slightly warmer than pure black. | 17.40:1 |
| `INK_80` | `#333333` | 51, 51, 51 | Heavy body emphasis (bold runs, key data). | 12.63:1 |
| `INK_60` | `#5C5C5C` | 92, 92, 92 | Secondary text — captions, footnotes, table notes, metadata. | 6.69:1 |
| `INK_40` | `#999999` | 153, 153, 153 | De-emphasized text (placeholder hints, expired-event labels). | 2.85:1 ❌ |
| `INK_30` | `#A8A8A8` | 168, 168, 168 | Tertiary text and thin rules. | 2.38:1 ❌ |
| `MUTED_BORDER` | `#CCCCCC` | 204, 204, 204 | Table cell borders, card outlines, soft dividers. | 1.61:1 |
| `SUCCESS` | `#5A9E78` | 90, 158, 120 | Positive variance, on-track status. | 3.18:1 ❌ |
| `WARNING` | `#F79B32` | 247, 155, 50 | Reused `HBEF_ORANGE` intentionally. | 2.17:1 ❌ |
| `RISK` | `#B23A2D` | 178, 58, 45 | Material risk flags. Grounded brick red. | 5.94:1 |

### 2.3 Retired surfaces

| Retired token | Hex | Old role |
|---|---|---|
| `SURFACE_PAGE` | `#E7E7E7` | Page-frame background (= `HBEF_PAGE`), under white content cards |
| `SURFACE_CARD` | `#FFFFFF` | Content-card background |
| `SURFACE_SOFT` | `#F2F2F2` | Spreadsheet sub-header fill, alt-row zebra |
| `SURFACE_ZEBRA` | `#FAFAFA` | Lightest alt-row fill for dense tables |
| `SURFACE_TOTAL` | `#E7E7E7` | Table total rows |
| `SURFACE_HERO` | `#0B4261` | Cover-page hero band |
| `SURFACE_FOOTER` | `#75C4B9` | Footer-band fill (mint teal) |

### 2.4 Retired chart series order

`#0B4261` → `#F79B32` → `#75C4B9` → `#417987` → `#124362` → `#5C5C5C`

Note the old order used *two navies and two teals* — three of the six series were blue-family, which is why old HBEF charts were hard to read in grayscale and under color-vision deficiency. The 2026 order (Navy → Valley → Teal → Vista → Turquoise → Wet Sand) alternates cool and warm deliberately.

### 2.5 How to spot the retired palette at a glance

- **A gray page background** (`#E7E7E7`) with white content cards floating on it. The 2026 system has no gray page frame — content sits on White.
- **A mint/seafoam teal** (`#75C4B9`). If the teal looks like a beach towel, it's legacy. The 2026 Teal (`#186892`) is a deep, structural ocean blue.
- **An orange donate button** (`#F79B32`). The 2026 CTA is **yellow** — View `#FFCD00` with Navy text.
- **Orange body links.** The old site set in-content links in `#F79B32` at 2.17:1.
- **A pale lemon yellow** (`#FAEF7A`). The 2026 yellow is saturated (`#FFCD00`).
- **Near-black body copy** (`#1A1A1A`). The 2026 body color is Asphalt `#515962`.

The old Navy `#0B4261` and the new Navy `#0C3B5D` are only 1.09:1 apart — **you cannot reliably tell them apart by eye.** Always check the actual hex in a color picker rather than trusting a visual judgment on navy.

---

## 3. The retired typefaces

### 3.1 Montserrat — the retired primary

A geometric sans-serif, loaded from Google Fonts. Used for **everything**: headings, body, tables, UI, captions.

```css
/* RETIRED — do not use */
font-family: 'Montserrat', 'Avenir Next', 'Helvetica Neue', Arial, sans-serif;
```

The old system leaned on Montserrat's full weight range, and the weight choices are themselves a legacy fingerprint:

| Weight | Old use |
|---|---|
| 200 Extra Light | Display H0 hero — **the signature thin-and-tall look**. Also large pull-out stats. |
| 300 Light | Cover subtitles |
| 400 Regular | Body, default |
| 500 Medium | Submenu links, light emphasis |
| 600 Semibold | Primary navigation |
| 700 Bold | All headings, buttons, table headers, emphasis |
| 900 Black | Donate-button label |

**The tell:** enormous 54–60pt type at weight 200, uppercase, with +1.0 to +2.0pt tracking. That "airy thin hero" treatment was the most recognizable feature of the old system and it is **completely gone** in 2026 — pull-out stats are now heavy slab (Aleo Bold), not thin sans.

### 3.2 BauhausBold — the retired display face

A geometric heavy display face, self-hosted from HBEF's own theme directory (`/wp-content/themes/hbef/assets/`) rather than from a font service. Used for cover titles and major section dividers, always paired with Montserrat 200.

```css
/* RETIRED — do not use */
font-family: 'BauhausBold', 'ITC Avant Garde Gothic', 'Century Gothic', 'Futura', 'Montserrat', sans-serif;
font-weight: 700;
```

**The tell:** heavy, perfectly circular bowls; a geometric, near-monoline construction; distinctive single-story forms. If a cover title looks like a 1980s corporate logotype, it is BauhausBold.

BauhausBold was never a licensed or documented brand asset in the way Aleo and Lato are — it was a file in a theme folder. That, plus the fact that no cloud or Apple app could render it without a manual install, was part of the case for replacing it.

### 3.3 AmsiPro — the pre-2021 display family

Two generations back. Eight OTFs (Black, Black Italic, Bold, Bold Italic, Italic, Light, Light Italic, Regular) from the foundry Stawix, archived at:

```
/Users/nolan/Projects/HBEF/HBEF BRANDING/Z PRIOR BRANDING - DO NOT USE/Pre 2021-2022 Logo/fonts/
```

**Commercially licensed** — unlike Aleo and Lato, these cannot be freely embedded or redistributed. Another reason the 2026 system moved to SIL OFL faces. If you find AmsiPro in a file, that file predates 2021 and is two full identity generations out of date.

### 3.4 Retired type-pairing conventions

These rules governed the old system. They are all void:

- ~~BauhausBold + Montserrat 200 Light~~ — the signature heavy-over-thin cover pairing
- ~~Montserrat 700 + Montserrat 400~~ — the workhorse heading/body pairing
- ~~Montserrat 700 *italic*~~ for event dates and pull quotes (bold italic, not regular italic)
- ~~"HBEF doesn't use serifs"~~ — **this rule inverted completely.** The 2026 primary typeface *is* a slab serif.
- ~~All-uppercase headings with positive tracking~~ — 2026 headings are sentence case with zero tracking.

---

## 4. Retired type scales

Kept for identification only. If you measure a legacy document and the numbers match these, you've confirmed it's pre-2026.

### 4.1 Retired document hierarchy (Word / PDF)

| Element | Family | Size | Weight | Tracking | Color | Line height |
|---|---|---|---|---|---|---|
| Cover title | BauhausBold / Montserrat | 42 | 700/900 | +1.5pt, UPPER | `#0B4261` | 1.1 |
| Display H0 hero | Montserrat | 54 | **200** | +1.0pt, UPPER | `#75C4B9` | 1.05 |
| H1 | Montserrat | 28 | 700 | +0.8pt, UPPER | `#0B4261` | 1.15 |
| H2 | Montserrat | 18 | 700 | +0.5pt, UPPER | `#0B4261` | 1.2 |
| H3 | Montserrat | 13 | 700 | +1.2pt, UPPER | `#417987` | 1.3 |
| Lead | Montserrat | 13 | 400 | 0 | `#1A1A1A` | 1.5 |
| Body | Montserrat | 11 | 400 | 0 | `#1A1A1A` | **1.55** |
| Body bold | Montserrat | 11 | 700 | 0 | `#333333` | 1.55 |
| Caption | Montserrat | 9 | 400 italic | 0 | `#5C5C5C` | 1.4 |
| Pull quote | Montserrat | 16 | 400 italic | 0 | `#0B4261` | 1.4 |
| Footnote | Montserrat | 8 | 400 | 0 | `#5C5C5C` | 1.3 |
| Table header | Montserrat | 10 | 700 | +0.8pt, UPPER | White on `#0B4261` | 1.2 |
| Table cell | Montserrat | 10 | 400 | 0 | `#1A1A1A` | 1.3 |
| Event date | Montserrat | 13 | **700 italic** | 0 | `#417987` | 1.4 |

### 4.2 Retired presentation hierarchy (PPTX)

| Element | Family | Size | Weight | Color |
|---|---|---|---|---|
| Cover title | BauhausBold / Montserrat | 60 | 700/900, UPPER, +2pt | `#0B4261` |
| Cover subtitle | Montserrat | 22 | 200 | `#75C4B9` |
| Section divider | Montserrat | 44 | 700, UPPER, +1pt | White on `#0B4261` |
| Slide title | Montserrat | 28 | 700, UPPER, +0.8pt | `#0B4261` |
| Slide subtitle | Montserrat | 14 | 400 | `#5C5C5C` |
| Body | Montserrat | 16 | 400 | `#1A1A1A` |
| Pull-out stat | Montserrat | 60 | **200** | `#0B4261` or `#F79B32` |
| Stat label | Montserrat | 11 | 400, UPPER, +1pt | `#5C5C5C` |
| Footer | Montserrat | 9 | 400 | `#5C5C5C` |

### 4.3 Retired spreadsheet hierarchy (XLSX)

| Element | Family | Size | Weight | Color | Fill |
|---|---|---|---|---|---|
| Workbook title | Montserrat | 18 | 700 | `#0B4261` | White |
| Section header | Montserrat | 12 | 700 | White | `#0B4261` |
| Sub-header | Montserrat | 11 | 700 | `#0B4261` | `#F2F2F2` |
| Data | Montserrat | 10 | 400 | `#1A1A1A` | White |
| Data (zebra) | Montserrat | 10 | 400 | `#1A1A1A` | `#FAFAFA` |
| Total row | Montserrat | 11 | 700 | `#0B4261` | `#E7E7E7` |
| Cell note | Montserrat | 9 | 400 italic | `#5C5C5C` | White |

---

## 5. The retired logo lineage

**Archive location — read-only, never pull an asset from here:**

```
/Users/nolan/Projects/HBEF/HBEF BRANDING/Z PRIOR BRANDING - DO NOT USE/
```

Three generations sit in this folder. All three are retired.

### 5.1 Generation 3 — "2021 New HBEF Logo" (the most recent retired mark)

```
Z PRIOR BRANDING - DO NOT USE/2021 New HBEF Logo/
├── HBEF Color Codes.pptx                    ← the old color reference; superseded by Brand Guidelines 2026
├── logo_email signature.png
├── HVPTO NEW LOGO.png                       ← HVPTO's mark, not HBEF's — do not confuse the two orgs
├── FINAL LOGO IMAGES_digital, round, square/
│   ├── HBEF Logo reworked_17x17_FINAL.psd
│   ├── FINAL_HBEF Logo reworked_17x17.jpg
│   ├── HBEF Logo_HORIZ lettering.jpg        ← horizontal lettering variant
│   ├── HBEF YARD SIGN_14x14_FINAL.jpg/.psd
│   ├── HBEF Cling & decal_16.4_ diameter_ no background.png/.psd
│   └── Google drive from JFP_June 2022/     ← Jennifer Faulk Photography hand-off, empty locally
└── working drafts/
    ├── HBEF LOGO final_dark blue border_30x19.jpg
    ├── HBEF LOGO final_lt aqua border_30x19.jpg
    ├── HBEF LOGO final_orange border_30x19.jpg
    ├── HBEF LOGO final_yellow border_30x19.jpg
    ├── HBEF LOGO_vector SQUARE_17x17.jpg
    └── all color combos with notes_corrected copy.jpg
```

**Identifying features:** a round/square badge construction with a colored border ring. The four border-color drafts (dark blue, light aqua, orange, yellow) map directly onto the retired palette — `#0B4261`, `#75C4B9`, `#F79B32`, `#FAEF7A`. Delivered as raster PSD/JPG/PNG, with only a "vector SQUARE" JPG standing in for vector — **there was no proper `.ai`/`.eps` master**, which is exactly what the 2026 library fixed.

This mark appears on yard signs, window clings, and decals still physically in circulation around Hermosa Beach. **Physical items already produced do not need to be destroyed or recalled** — but nothing new gets produced with this mark, and no digital deliverable may use it.

### 5.2 Generation 2 — "2021–2023 Logo — Erin Smith"

```
Z PRIOR BRANDING - DO NOT USE/2021-2023 Logo - Erin Smith/
├── HBEF_stacked LOGO.png
├── HBEF_stacked LOGO(1).png
├── Copy of HBEF Logo_HORIZ lettering.jpg
├── HBEF Cling_17.25x17.25_ no background.psd
├── LOGOS_HBEF_FINAL_stacked and wide.docx    ← old lockup sheet
├── LOGOS_HBEF_FINAL_stacked and wide(1).docx
├── postcard_side 1v4_4 inch white space.jpg
└── postcard_side 2v3.jpg
```

**Identifying features:** the **`HBEF_stacked`** filename is the giveaway — the SKILL.md rebrand notice calls out "HBEF_stacked files" by name as retired. Stacked and wide (horizontal) lockups, distributed inside a Word document rather than as a proper asset library.

If a deliverable references `HBEF_stacked LOGO.png`, it is legacy. Replace with `assets/logos/HBEF-Primary_Lockup-RGB@2x.png` (stacked) or `HBEF-Secondary_Lockup-RGB@2x.png` (horizontal).

### 5.3 Generation 1 — "Pre 2021–2022 Logo"

```
Z PRIOR BRANDING - DO NOT USE/Pre 2021-2022 Logo/
├── HBEF_primaryCMYKWhitebg.png
├── hbef_logo_white_white_tagline.png         ← white lockup with tagline
├── hermosa beach logo.png
├── Copy of hbef_logos.pptx
├── HBEF letterhead with tax ID (footer).docx  ← the ancestor of the current letterhead
└── fonts/
    └── Stawix - AmsiPro-{Black,BlackItalic,Bold,BoldItalic,Italic,Light,LightItalic,Regular}.otf
```

**Identifying features:** the old sail/wordmark mark referenced in the SKILL.md rebrand notice. Set in **AmsiPro**, a commercially licensed family. The letterhead `.docx` in this folder is the direct ancestor of today's letterhead — it already carried the 501(c)(3)/EIN footer, which is the one element that survived every rebrand unchanged.

### 5.4 What replaced all of it

The 2026 system is a **sunburst-over-wave** mark in four lockups, with proper RGB/CMYK, light/dark-mode/white/black variants, and `.ai`/`.eps` vector masters:

| 2026 lockup | Bundled file (light / dark-mode) |
|---|---|
| Primary Lockup (stacked) | `HBEF-Primary_Lockup-RGB@2x.png` / `HBEF-Primary_Lockup-Dark_Mode-RGB@2x.png` |
| Primary Lockup + Tagline | `HBEF-Primary_Lockup_Tag-RGB@2x.png` / `HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png` |
| Secondary Lockup (horizontal) | `HBEF-Secondary_Lockup-RGB@2x.png` / `HBEF-Secondary_Lockup-Dark_Mode-RGB@2x.png` |
| Logomark | `HBEF-Logomark.png`, `HBEF-Logomark-space.png` |

Master library: `/Users/nolan/Projects/HBEF/HBEF BRANDING/LOGOS/`. Bundled working copies: `assets/logos/`.

**Tagline:** *Funding matters. Your donation, their future.* (The pre-2021 mark also carried a tagline — check that any migrated file uses this exact current wording.)

---

## 6. One-to-one migration map

Every retired value and its 2026 replacement. Read the **Notes** column — several mappings are *not* mechanical, because the rebrand changed a color's job, not just its value.

### 6.1 Colors

| Retired token | Retired hex | → 2026 token | New hex | Notes |
|---|---|---|---|---|
| `HBEF_NAVY` | `#0B4261` | `HBEF_NAVY` | `#0C3B5D` | Straight swap. Same role. Visually near-identical (1.09:1 apart) — you must check the hex, not your eye. |
| `HBEF_NAVY_DEEP` | `#124362` | `HBEF_NAVY` | `#0C3B5D` | The footer-text variant collapses into the single new Navy. |
| `HBEF_ORANGE` | `#F79B32` | **depends on job** | — | ⚠ **Not mechanical.** If it was a **CTA / donate button / link** → `HBEF_VIEW` `#FFCD00` with Navy text on top. If it was an **attention accent, chart series, or rule** → `HBEF_VALLEY` `#EE7623`. Read every instance in context. |
| `HBEF_TEAL` | `#75C4B9` | `HBEF_SKY` | `#B8D8EB` | ⚠ **Not mechanical.** The old mint teal was a *light fill* (footer, mobile menu). Its replacement is **Sky, not the new Teal.** Mapping it to `#186892` will produce a document that's far too dark. |
| `HBEF_TEAL_DISPLAY` | `#74C4B9` | `HBEF_SKY` | `#B8D8EB` | Typo variant of the above; same replacement. But if it was **hero display *text***, the correct new value is `HBEF_TEAL` `#186892` — Sky fails contrast as text. |
| `HBEF_TEAL_MUTED` | `#417987` | `HBEF_TEAL` | `#186892` | The true structural-teal ancestor. Straight swap. |
| `HBEF_TEAL_MUTED_2` | `#407987` | `HBEF_TEAL` | `#186892` | Typo variant; same replacement. |
| `HBEF_YELLOW` | `#FAEF7A` | `HBEF_VIEW` | `#FFCD00` | Soft lemon → saturated CTA yellow. Same **fill-only** restriction: never as text on white. |
| `HBEF_PAGE` | `#E7E7E7` | `WHITE` (+ `HBEF_SKY` / `HBEF_SAND` bands) | `#FFFFFF` (+ `#B8D8EB` / `#DDC9A3`) | ⚠ **Delete the gray page frame entirely.** 2026 content sits on White; tinted bands are Sky or Sand. Do not substitute a light gray. |
| `WHITE` | `#FFFFFF` | `WHITE` | `#FFFFFF` | Unchanged. |
| `INK` | `#1A1A1A` | `HBEF_ASPHALT` | `#515962` | Body copy is now warm-cool gray, not near-black. This lightens the whole document — intended. |
| `INK_80` | `#333333` | `HBEF_NAVY` | `#0C3B5D` | Heavy emphasis is now Navy, not darker gray. |
| `INK_60` | `#5C5C5C` | `HBEF_WET_SAND` | `#98989A` | ⚠ The new value is **lighter** (6.69:1 → 2.88:1 on white). Anything load-bearing that was `INK_60` should move to **Asphalt `#515962`**, not Wet Sand. |
| `INK_40` | `#999999` | `HBEF_WET_SAND` | `#98989A` | |
| `INK_30` | `#A8A8A8` | `HBEF_WET_SAND` | `#98989A` | Three old grays collapse into one. |
| `MUTED_BORDER` | `#CCCCCC` | `MUTED_BORDER` | `#D9D9D9` | Lighter hairline. |
| `SUCCESS` | `#5A9E78` | `SUCCESS` | `#4A8B5C` | Deeper, more civic green. Contrast improves 3.18:1 → 4.09:1. |
| `WARNING` | `#F79B32` | `WARNING` | `#FFA400` | Now reuses Vista instead of the retired brand orange. |
| `RISK` | `#B23A2D` | `RISK` | `#B23A2D` | **Unchanged.** The only color that survived the rebrand intact. |
| `SURFACE_PAGE` | `#E7E7E7` | `SURFACE_PAGE` | `#FFFFFF` | |
| `SURFACE_CARD` | `#FFFFFF` | `SURFACE_PAGE` | `#FFFFFF` | The card/page distinction disappears with the gray frame. |
| `SURFACE_SOFT` | `#F2F2F2` | `HBEF_SKY` | `#B8D8EB` | XLSX sub-header fill is now Sky, with Navy bold text. |
| `SURFACE_ZEBRA` | `#FAFAFA` | `SURFACE_ZEBRA` | `#F7FAFC` | Neutral gray → cool blue-white. |
| `SURFACE_TOTAL` | `#E7E7E7` | `SURFACE_TOTAL` | `#E8F1F7` | |
| `SURFACE_HERO` | `#0B4261` | `SURFACE_HERO` | `#0C3B5D` | |
| `SURFACE_FOOTER` | `#75C4B9` | `SURFACE_ACCENT` | `#FFCD00` | The footer band changes from mint teal to a View yellow strip. |
| *(none)* | — | `HBEF_TURQUOISE` | `#129FDA` | **New in 2026.** No legacy ancestor — icons, links, wave motifs, wordmark line 2. |
| *(none)* | — | `HBEF_VISTA` | `#FFA400` | **New in 2026.** |
| *(none)* | — | `HBEF_SAND` | `#DDC9A3` | **New in 2026.** The old system had no warm neutral. |

**Retired chart order → 2026 chart order:**

| Position | Retired | 2026 |
|---|---|---|
| 1 | `#0B4261` Navy | `#0C3B5D` Navy |
| 2 | `#F79B32` Orange | `#EE7623` Valley |
| 3 | `#75C4B9` Teal | `#186892` Teal |
| 4 | `#417987` Teal Muted | `#FFA400` Vista |
| 5 | `#124362` Navy Deep | `#129FDA` Turquoise |
| 6 | `#5C5C5C` INK_60 | `#98989A` Wet Sand |

### 6.2 Typefaces

| Retired | → 2026 | Notes |
|---|---|---|
| **BauhausBold** (display) | **Aleo Bold** | ⚠ Category change, not a swap. Geometric heavy sans → slab serif. Re-typeset; do not find-and-replace. |
| **Montserrat 700** (H1/H2) | **Aleo Bold** | For headings above 12pt. |
| **Montserrat 700** (H3, eyebrows, table headers) | **Lato Bold 700** | For 12pt and below. The size boundary decides which family. |
| **Montserrat 400** (body) | **Lato Regular 400** | Straight swap. |
| **Montserrat 200 Extra Light** (hero, stats) | **Aleo Bold** (stats) / **Lato Light 300** (cover subtitle) | ⚠ The thin-and-tall hero look is **retired entirely**. Pull-out stats invert from weight 200 to weight 700. |
| **Montserrat 300 Light** | **Lato Light 300** | Cover subtitles only, ≥16pt. |
| **Montserrat 500 Medium** | **Lato Regular 400** | No Medium equivalent in the 2026 system. |
| **Montserrat 600 Semibold** | **Lato Bold 700** | |
| **Montserrat 900 Black** | **Lato Black 900** | Large-format print only now — not for documents. |
| **Montserrat 700 Italic** (event dates, pull quotes) | **Aleo Italic 400** (pull quotes) / **Lato Italic 400** (captions, dates) | ⚠ The weight drops from 700 to 400. "Bold italic for editorial moments" is retired. |
| **AmsiPro** (pre-2021, all weights) | **Aleo Bold** | Two generations back. Also swaps a commercial license for SIL OFL. |
| Fallbacks: Avenir Next, ITC Avant Garde Gothic, Century Gothic, Futura | Aleo → Roboto Slab, Zilla Slab, Rockwell, Georgia, serif · Lato → Helvetica Neue, Helvetica, Arial, sans-serif | Old chains were geometric-sans; the new heading chain is slab/serif. |

### 6.3 Retired conventions → 2026 conventions

| Retired convention | 2026 convention |
|---|---|
| UPPERCASE headings with +0.5 to +2.0pt tracking | **Sentence/title case, zero tracking** on all Aleo headings. Tracking is a Lato-uppercase tool only (H3 +0.8pt, eyebrow +1.2pt, table header +0.6pt). |
| Body line-height 1.55 | Body line-height **1.5**; lead **1.45** |
| Orange CTA button, weight 900, +3pt tracking | **View `#FFCD00` fill with Navy `#0C3B5D` Lato Bold text**, +0.06em |
| Orange in-content links | **Turquoise `#129FDA`**, underlined; Navy underlined in print-bound docs |
| Gray `#E7E7E7` page frame with white cards | White page; **Sky `#B8D8EB`** or **Sand `#DDC9A3`** tinted bands |
| Mint teal `#75C4B9` footer band | **View `#FFCD00`** 0.25" accent strip |
| "HBEF doesn't use serifs" | The primary typeface **is** a slab serif |
| Color extracted from theme CSS | Color specified by **HBEF Brand Guidelines 2026** |
| Raster-only logo assets | RGB/CMYK, light/dark/white/black, `.ai`/`.eps` vector masters |

---

## 7. How to migrate an existing deliverable

Work in this order. Steps 2 and 3 are where the time goes — the rest is mechanical.

**1. Confirm it's actually legacy.**
Open a color picker on a navy element. `#0B4261` = legacy. `#0C3B5D` = already migrated. Check the body font: Montserrat/BauhausBold/AmsiPro = legacy; Aleo/Lato = current. Don't judge by eye — the two navies are indistinguishable.

**2. Re-typeset, don't find-and-replace.**
Swap the families per §6.2, then fix what breaks:
- **Aleo runs wider and needs more leading than Montserrat at the same size.** Every heading will re-wrap. Budget for it.
- **Remove every uppercase transform from Aleo headings** and zero their tracking. This is the single most visible legacy tell that survives a careless migration.
- **Re-map by level, not by weight.** Montserrat 700 becomes Aleo Bold above 12pt and Lato Bold at 12pt and below.
- **Invert the stats.** Any Montserrat 200 pull-out number becomes Aleo Bold 700 — it will look completely different, and that's correct.
- Drop bold-italic to regular-italic for pull quotes and dates.

**3. Re-map colors in context, not by rule.**
Run §6.1, but stop and read each instance of:
- **`#F79B32`** — CTA → View `#FFCD00`; accent → Valley `#EE7623`
- **`#75C4B9`** — light fill → Sky `#B8D8EB`; display text → Teal `#186892`
- **`#5C5C5C`** — decorative metadata → Wet Sand `#98989A`; load-bearing text → Asphalt `#515962`

**4. Delete the gray page frame.**
Set the page/background to White. Convert any "white card on gray" construction to plain content on White, with a Sky or Sand band where the design needs separation. Pick Sky *or* Sand for the whole document, not both.

**5. Swap every logo file.**
Replace anything from `Z PRIOR BRANDING - DO NOT USE/` — including `HBEF_stacked LOGO.png`, the round-badge marks, and the pre-2021 sail/wordmark — with the correct 2026 lockup from `assets/logos/`. Match orientation (stacked → Primary, horizontal → Secondary) and background (light lockup on light, **Dark_Mode lockup on Navy or Teal**). Restore clear space = the height of the "HBEF" lettering on all four sides. Check the minimums: lockup ≥ 1.25" / 120px, logomark ≥ 0.4" / 32px.

**6. Re-check contrast.**
Run the migrated palette against `references/colors-and-fonts.md` §4. Two traps specifically:
- **Asphalt `#515962` on Sand `#DDC9A3` is 4.38:1 — it fails AA.** On Sand, body copy must be Navy.
- **Wet Sand `#98989A` (2.88:1) is lighter than the old `INK_60` (6.69:1).** Anything that mattered in `INK_60` needs Asphalt, not Wet Sand.
- And confirm no yellow ended up as text: View and Vista are **fill-only**.

**7. Update the surrounding system, not just the pixels.**
- Confirm the **tagline** reads exactly *"Funding matters. Your donation, their future."*
- Confirm the **501(c)(3)/EIN footer** is present and current on every letterhead page and every donor-facing document: *"HBEF is a registered 501(c)(3) non-profit organization. Contributions are tax-deductible to the extent allowed by law. Federal tax identification number (EIN): 33-0522270."*
- Confirm handles: **hbef.org**, **@hbef90254** (identical on Instagram and Facebook), 1645 Valley Drive, Hermosa Beach, CA 90254.
- Confirm **sponsor tier names** if present: Brighter Benefactor ($25K+), Diamond ($15K+), Platinum ($10K+), Gold ($6K+), Silver ($3.5K+), Bronze ($1.5K+).
- Check for stale claims — old sponsor lists, prior-year figures, retired program names.

**8. Verify before shipping.**
Open the produced file. Confirm: headings render in Aleo (not a serif fallback), body in Lato, navy reads `0C3B5D`, no gray page frame, no yellow text, correct logo variant for its background. PDF-export and look at it once more.

**9. Note the exception.**
HBEF's own letterhead template and the Strand Classic press release set body copy in **Aleo 12pt**, not Lato. That is a documented variance in the *current* system, not a legacy artifact. When editing those files in place, keep their native Aleo body and flag the variance to the requester.

**Escalation:** brand questions during a migration go to **Deni Mileski** (text 310.748.7390 / deni@denilampe.com), HBEF's brand contact of record per the 2026 Guidelines. Anything about a Pantone substitution, a logo modification, or reusing an archived mark is a Deni decision, not a production decision.
