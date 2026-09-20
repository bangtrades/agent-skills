# HBEF — Long-Form Colors & Fonts Reference (2026 System)

The complete token system for the **HBEF 2026 identity**. The summary in `SKILL.md` covers ~80% of jobs — read this when you need every shade, every CMYK build, every contrast ratio, every exact size and line-height for precise programmatic generation.

## Source of Truth

All values here come from **`HBEF Brand Guidelines 2026`** — the foundation's own guidelines document — plus the released logo, typeface, and letterhead asset library at `/Users/nolan/Projects/HBEF/HBEF BRANDING/`. Machine-readable mirror: **`assets/brand-tokens.json`** (v2.0.0). CSS mirror: **`assets/brand-palette.css`**.

**Everything from the pre-2026 system is retired.** If you are looking at a file that uses Montserrat, BauhausBold, `#0B4261`, `#F79B32`, or `#75C4B9`, you are looking at legacy work — see `references/legacy-brand.md` and the retired-token map at the bottom of this file.

**Never improvise a hex value from memory.** Copy it from a table here or from `brand-tokens.json`.

---

## 1. Full Color Token Table

### 1.1 Core Coastal Colors

| Token | Name | Hex | RGB | CMYK (approx.) | Usage |
|---|---|---|---|---|---|
| `HBEF_NAVY` | Navy | `#0C3B5D` | 12, 59, 93 | 87 / 37 / 0 / 64 | **Primary brand element.** Dominant backgrounds, major text, H1s, table headers, cover hero bands, structural rules, chart series 1. |
| `HBEF_TEAL` | Teal | `#186892` | 24, 104, 146 | 84 / 29 / 0 / 43 | Primary brand element and supporting headers. The mid-depth ocean blue. H2s, IC/TAB accent rules, section rules, chart series 3. |
| `HBEF_TURQUOISE` | Turquoise | `#129FDA` | 18, 159, 218 | 92 / 27 / 0 / 15 | Energetic graphic elements, iconography, links, wave motifs. The "EDUCATION FOUNDATION" line in the wordmark. Chart series 5. |

### 1.2 School Colors & Warm Accents

The three warm accents are named for the three Hermosa Beach schools — **Hermosa View, Hermosa Vista, Hermosa Valley**. Use the color *name*, not just the hex, when writing for an internal audience.

| Token | Name | Hex | RGB | CMYK (approx.) | Usage |
|---|---|---|---|---|---|
| `HBEF_VIEW` | View (Yellow) | `#FFCD00` | 255, 205, 0 | 0 / 20 / 100 / 0 | **The primary CTA color.** Calls-to-action, "Donate" buttons, highlights, cover footer band, pull-quote left borders. Fill only — never small text on white. |
| `HBEF_VISTA` | Vista (Golden Yellow) | `#FFA400` | 255, 164, 0 | 0 / 36 / 100 / 0 | Secondary highlights, energetic details, CTA hover state, chart series 4. Doubles as the `WARNING` functional color. |
| `HBEF_VALLEY` | Valley (Orange) | `#EE7623` | 238, 118, 35 | 0 / 50 / 85 / 7 | Accent points that must draw immediate attention. Event-deliverable accent rule, donor-facing chart headline, chart series 2. |

### 1.3 Neutrals & Backgrounds

| Token | Name | Hex | RGB | CMYK (approx.) | Usage |
|---|---|---|---|---|---|
| `HBEF_SKY` | Sky | `#B8D8EB` | 184, 216, 235 | 22 / 8 / 0 / 8 | Light backgrounds and spacious layouts. **The default tinted section fill.** Section-divider bands, XLSX sub-headers, eyebrow text on Navy. |
| `HBEF_SAND` | Sand | `#DDC9A3` | 221, 201, 163 | 0 / 9 / 26 / 13 | Warm secondary background, for contrast against Sky. Pick Sky *or* Sand per document — never both fighting. |
| `HBEF_WET_SAND` | Wet Sand | `#98989A` | 152, 152, 154 | 1 / 1 / 0 / 40 | Secondary text, metadata, captions, footers, eyebrows, subtle borders, chart series 6 / "other". |
| `HBEF_ASPHALT` | Asphalt | `#515962` | 81, 89, 98 | 17 / 9 / 0 / 62 | **Primary body copy.** A softer alternative to pure black. Never use `#000000` for type. |
| `WHITE` | White | `#FFFFFF` | 255, 255, 255 | 0 / 0 / 0 / 0 | Content-card and page background. Reversed type on Navy/Teal. |

### 1.4 Functional colors (documents only — not part of the public brand)

| Token | Hex | RGB | CMYK (approx.) | Role |
|---|---|---|---|---|
| `SUCCESS` | `#4A8B5C` | 74, 139, 92 | 47 / 0 / 34 / 45 | Positive variance, grant approved, "on track." Muted civic green, never neon. |
| `WARNING` | `#FFA400` | 255, 164, 0 | 0 / 36 / 100 / 0 | Caution — deliberately reuses Vista so the document palette stays inside the brand. |
| `RISK` | `#B23A2D` | 178, 58, 45 | 0 / 67 / 75 / 30 | Material risk flags in IC / budget reporting. Grounded brick red, never fire-engine bright. |
| `MUTED_BORDER` | `#D9D9D9` | 217, 217, 217 | 0 / 0 / 0 / 15 | Table cell borders, card outlines, chart gridlines at 0.75pt. |

### 1.5 Derived surfaces

| Token | Hex | RGB | CMYK (approx.) | Role |
|---|---|---|---|---|
| `SURFACE_PAGE` | `#FFFFFF` | 255, 255, 255 | 0 / 0 / 0 / 0 | Page background (= `WHITE`). |
| `SURFACE_TINT` | `#B8D8EB` | 184, 216, 235 | 22 / 8 / 0 / 8 | Tinted section band (= `HBEF_SKY`). |
| `SURFACE_WARM` | `#DDC9A3` | 221, 201, 163 | 0 / 9 / 26 / 13 | Warm alternate section band (= `HBEF_SAND`). |
| `SURFACE_HERO` | `#0C3B5D` | 12, 59, 93 | 87 / 37 / 0 / 64 | Cover-page hero band (= `HBEF_NAVY`). |
| `SURFACE_ACCENT` | `#FFCD00` | 255, 205, 0 | 0 / 20 / 100 / 0 | Cover footer band / CTA fill (= `HBEF_VIEW`). |
| `SURFACE_ZEBRA` | `#F7FAFC` | 247, 250, 252 | 2 / 1 / 0 / 1 | Spreadsheet alternating-row fill. |
| `SURFACE_TOTAL` | `#E8F1F7` | 232, 241, 247 | 6 / 2 / 0 / 3 | Spreadsheet total-row fill. |

### 1.6 Chart / series palette (categorical, max 6)

Use in this exact order. Do not reorder to "look better" — consistency across HBEF reporting is the point.

| # | Token | Hex | Role |
|---|---|---|---|
| 1 | `HBEF_NAVY` | `#0C3B5D` | Series 1 / headline metric |
| 2 | `HBEF_VALLEY` | `#EE7623` | Series 2 |
| 3 | `HBEF_TEAL` | `#186892` | Series 3 |
| 4 | `HBEF_VISTA` | `#FFA400` | Series 4 |
| 5 | `HBEF_TURQUOISE` | `#129FDA` | Series 5 |
| 6 | `HBEF_WET_SAND` | `#98989A` | Series 6 / "other" |

**Single-series accent by subject:** Navy `#0C3B5D` for financials / endowment / IC · Valley `#EE7623` for fundraising / donor / participation · Teal `#186892` for community / program / student-impact.

---

## 2. CMYK for Print

> ### ⚠ These CMYK builds are APPROXIMATE — confirm against the CMYK `.eps` master files before a print run.
>
> Every CMYK value in this document is a **naive sRGB→CMYK conversion** (`K = 1 − max(R,G,B)`, then `C = (1−R−K)/(1−K)`, etc.), computed device-independently with no ICC profile, no black generation / UCR / GCR, and no press or stock profile applied. They are here so you can *specify intent* to a vendor and sanity-check a proof — they are **not** the production build.
>
> **Before any commercial print run:**
> 1. Pull the CMYK `.eps` logo masters from `/Users/nolan/Projects/HBEF/HBEF BRANDING/LOGOS/` and read the swatch values embedded in them — those are authoritative.
> 2. Ask the printer for their profile (typically US Web Coated SWOP v2 or GRACoL 2013) and convert from the sRGB hex under that profile.
> 3. Escalate to **Deni Mileski** (text 310.748.7390 / deni@denilampe.com) if a vendor proposes a Pantone substitution — HBEF has not published spot equivalents, and picking one ad hoc is a brand decision, not a production decision.

### 2.1 Consolidated CMYK build sheet

| Color | Hex | C | M | Y | K |
|---|---|---|---|---|---|
| Navy | `#0C3B5D` | 87 | 37 | 0 | 64 |
| Teal | `#186892` | 84 | 29 | 0 | 43 |
| Turquoise | `#129FDA` | 92 | 27 | 0 | 15 |
| View | `#FFCD00` | 0 | 20 | 100 | 0 |
| Vista | `#FFA400` | 0 | 36 | 100 | 0 |
| Valley | `#EE7623` | 0 | 50 | 85 | 7 |
| Sky | `#B8D8EB` | 22 | 8 | 0 | 8 |
| Sand | `#DDC9A3` | 0 | 9 | 26 | 13 |
| Wet Sand | `#98989A` | 1 | 1 | 0 | 40 |
| Asphalt | `#515962` | 17 | 9 | 0 | 62 |
| White | `#FFFFFF` | 0 | 0 | 0 | 0 |
| Success | `#4A8B5C` | 47 | 0 | 34 | 45 |
| Warning | `#FFA400` | 0 | 36 | 100 | 0 |
| Risk | `#B23A2D` | 0 | 67 | 75 | 30 |
| Muted Border | `#D9D9D9` | 0 | 0 | 0 | 15 |

### 2.2 Practical print notes

- **Navy `#0C3B5D` will look flat and weak** if a printer runs the naive build (87/37/0/64) — total ink is only 188%, and heavy K in a dark blue kills the richness. Ask for a **rich black-style navy** build (roughly 100/75/30/25, total ink ~230%) and proof it. This is the single most common HBEF print failure.
- **View `#FFCD00` and Vista `#FFA400` are outside the CMYK gamut** at full saturation. They will print duller than they appear on screen. If a piece depends on the yellow *singing* (poster, banner, step-and-repeat), discuss a spot color with the vendor rather than accepting a muddy process build.
- **Turquoise `#129FDA`** is also gamut-marginal — expect a slight shift toward navy on coated stock and a larger shift on uncoated.
- **Sand `#DDC9A3`** is a very light warm neutral; on uncoated stock it can disappear into the paper. Consider bumping it ~5% or dropping to White for uncoated jobs.
- Export print as **CMYK PDF/X** using the CMYK `.eps` logos; export screen as **sRGB PNG** using the RGB files. Never send an RGB PDF to a commercial printer.

---

## 3. Tint & Shade Ramps

For table fills, chart shading, sequential (non-categorical) data, zebra striping, and background bands. **All tints are computed as a linear sRGB-space blend against White** (`out = color × p + 255 × (1 − p)`) — the same math Word, PowerPoint, Excel, Google Sheets, and Keynote apply when you pick a "lighter %" swatch, so these values will match what those apps produce.

Use the ramps for *sequential* data (one metric, varying intensity). Use the **categorical chart palette** in §1.6 for *different* series. Never mix the two systems in one chart.

### 3.1 Navy ramp — `#0C3B5D` on White

| Token | Tint | Hex | RGB | Navy text on it | White text on it | Recommended use |
|---|---|---|---|---|---|---|
| `NAVY_10` | 10% | `#E7EBEF` | 231, 235, 239 | 9.74:1 ✅ AAA | 1.20:1 ❌ | Lightest table fill, zebra alternative, callout background |
| `NAVY_20` | 20% | `#CED8DF` | 206, 216, 223 | 8.07:1 ✅ AAA | 1.45:1 ❌ | Sub-header fill, sequential band 1 |
| `NAVY_30` | 30% | `#B6C4CE` | 182, 196, 206 | 6.54:1 ✅ AAA | 1.78:1 ❌ | Total-row fill, sequential band 2 |
| `NAVY_40` | 40% | `#9EB1BE` | 158, 177, 190 | 5.27:1 ✅ AA | 2.21:1 ❌ | Sequential band 3, chart shading |
| `NAVY_50` | 50% | `#869DAE` | 134, 157, 174 | 4.14:1 ⚠ AA large only | 2.82:1 ❌ | Chart shading, dividers. **Text danger zone — avoid type here.** |
| `NAVY_60` | 60% | `#6D899E` | 109, 137, 158 | 3.18:1 ❌ | 3.67:1 ⚠ AA large only | Chart shading only |
| `NAVY_70` | 70% | `#55768E` | 85, 118, 142 | 2.43:1 ❌ | 4.81:1 ✅ AA | Dark band, sequential band 5 |
| `NAVY_80` | 80% | `#3D627D` | 61, 98, 125 | 1.80:1 ❌ | 6.48:1 ✅ AA | Dark band, secondary hero |
| `NAVY_90` | 90% | `#244F6D` | 36, 79, 109 | 1.34:1 ❌ | 8.70:1 ✅ AAA | Near-Navy band, hover state |
| `HBEF_NAVY` | 100% | `#0C3B5D` | 12, 59, 93 | — | 11.67:1 ✅ AAA | Full brand Navy |

### 3.2 Teal ramp — `#186892` on White

| Token | Tint | Hex | RGB | Navy text on it | White text on it | Recommended use |
|---|---|---|---|---|---|---|
| `TEAL_10` | 10% | `#E8F0F4` | 232, 240, 244 | 10.12:1 ✅ AAA | 1.15:1 ❌ | Lightest table fill, IC/TAB callout background |
| `TEAL_20` | 20% | `#D1E1E9` | 209, 225, 233 | 8.70:1 ✅ AAA | 1.34:1 ❌ | Sub-header fill (softer alternative to Sky) |
| `TEAL_30` | 30% | `#BAD2DE` | 186, 210, 222 | 7.43:1 ✅ AAA | 1.57:1 ❌ | Total-row fill, sequential band 1 |
| `TEAL_40` | 40% | `#A3C3D3` | 163, 195, 211 | 6.28:1 ✅ AAA | 1.86:1 ❌ | Sequential band 2 |
| `TEAL_50` | 50% | `#8CB4C8` | 140, 180, 200 | 5.27:1 ✅ AA | 2.22:1 ❌ | Sequential band 3, chart shading |
| `TEAL_60` | 60% | `#74A4BE` | 116, 164, 190 | 4.33:1 ⚠ AA large only | 2.69:1 ❌ | Chart shading. **Text danger zone.** |
| `TEAL_70` | 70% | `#5D95B3` | 93, 149, 179 | 3.57:1 ❌ | 3.27:1 ⚠ AA large only | Chart shading only — worst-of-both-worlds band, avoid for type entirely |
| `TEAL_80` | 80% | `#4686A8` | 70, 134, 168 | 2.91:1 ❌ | 4.01:1 ⚠ AA large only | Chart shading, decorative band |
| `TEAL_90` | 90% | `#2F779D` | 47, 119, 157 | 2.36:1 ❌ | 4.95:1 ✅ AA | Near-Teal band, hover state |
| `HBEF_TEAL` | 100% | `#186892` | 24, 104, 146 | — | 6.12:1 ✅ AA | Full brand Teal |

### 3.3 Shades (darker than 100%)

Computed as a multiply toward black (`out = color × p`). Use only for hover/pressed states and shadowless depth cues on screen — **never in print**, where they crush.

| Base | 90% | 80% | 70% |
|---|---|---|---|
| Navy `#0C3B5D` | `#0B3554` | `#0A2F4A` | `#082941` |
| Teal `#186892` | `#165E83` | `#135375` | `#114966` |

### 3.4 Ramp usage rules

- **Sequential charts:** use 3–5 steps from one ramp, widest spacing available (e.g. `NAVY_20 / NAVY_40 / NAVY_60 / NAVY_80 / HBEF_NAVY`). Skipping to adjacent tints (`NAVY_40 / NAVY_50`) produces bands nobody can tell apart.
- **Table fills:** stay at or below 30%. Above 30% the Navy/Teal body text starts failing.
- **Never tint the warm accents.** Tinted View/Vista/Valley read as washed-out beige and collide with Sand. If you need a light warm surface, use Sand `#DDC9A3`.
- **Never tint Sky or Sand.** They are already the light end of the system.
- The stock HBEF spreadsheet fills (`SURFACE_ZEBRA #F7FAFC`, `SURFACE_TOTAL #E8F1F7`) are *not* on these ramps — they are cooler and lighter by design. Use them for XLSX; use the ramps for charts and document tables.

---

## 4. WCAG Contrast Reference

All ratios below are computed per **WCAG 2.x relative luminance** (sRGB, `(L1 + 0.05) / (L2 + 0.05)`).

**Thresholds:** AA normal text ≥ **4.5:1** · AA large text (≥18pt, or ≥14pt bold) ≥ **3:1** · AAA normal text ≥ **7:1** · AAA large text ≥ **4.5:1** · Non-text UI/graphics ≥ **3:1**.

### 4.1 Every brand color as text on White `#FFFFFF`

| Color | Hex | Ratio vs White | Normal text (AA) | Large text (AA) | Verdict |
|---|---|---|---|---|---|
| Navy | `#0C3B5D` | **11.67:1** | ✅ Pass (AAA) | ✅ Pass | Safe everywhere — headings and body |
| Asphalt | `#515962` | **7.11:1** | ✅ Pass (AAA) | ✅ Pass | Safe everywhere — the body-copy default |
| Teal | `#186892` | **6.12:1** | ✅ Pass (AA) | ✅ Pass | Safe for headings and body; AAA only at large sizes |
| Risk | `#B23A2D` | **5.94:1** | ✅ Pass (AA) | ✅ Pass | Safe for risk labels and negative figures |
| Success | `#4A8B5C` | **4.09:1** | ❌ **Fail** | ✅ Pass | ⚠ Use ≥14pt bold, or pair with an icon/symbol |
| Turquoise | `#129FDA` | **3.00:1** | ❌ **Fail** | ✅ Pass (just) | ⚠ Links and large display only — underline links |
| Valley | `#EE7623` | **2.90:1** | ❌ **Fail** | ❌ **Fail** | Fill/graphic only. Not text on white. |
| Wet Sand | `#98989A` | **2.88:1** | ❌ **Fail** | ❌ **Fail** | ⚠ Captions/footers only, and only where the info is non-essential |
| Vista | `#FFA400` | **1.99:1** | ❌ **Fail** | ❌ **Fail** | **Fill only. Never text on white.** |
| Sand | `#DDC9A3` | **1.62:1** | ❌ **Fail** | ❌ **Fail** | Background only |
| View | `#FFCD00` | **1.50:1** | ❌ **Fail** | ❌ **Fail** | **Fill only. Never text on white.** |
| Sky | `#B8D8EB` | **1.49:1** | ❌ **Fail** | ❌ **Fail** | Background only |
| Muted Border | `#D9D9D9` | **1.41:1** | ❌ **Fail** | ❌ **Fail** | Hairlines only — also fails the 3:1 non-text minimum, so never use it as the *only* indicator of a boundary |

### 4.2 Every brand color as text on Navy `#0C3B5D`

| Color | Hex | Ratio vs Navy | Normal text (AA) | Large text (AA) | Verdict |
|---|---|---|---|---|---|
| White | `#FFFFFF` | **11.67:1** | ✅ Pass (AAA) | ✅ Pass | The default reversed type |
| Muted Border | `#D9D9D9` | **8.27:1** | ✅ Pass (AAA) | ✅ Pass | Reversed hairlines read cleanly |
| Sky | `#B8D8EB` | **7.81:1** | ✅ Pass (AAA) | ✅ Pass | **The brand-correct reversed secondary** — eyebrows and subtitles on Navy |
| View | `#FFCD00` | **7.77:1** | ✅ Pass (AAA) | ✅ Pass | Excellent reversed CTA/accent text on Navy |
| Sand | `#DDC9A3` | **7.20:1** | ✅ Pass (AAA) | ✅ Pass | Warm reversed secondary |
| Vista | `#FFA400` | **5.87:1** | ✅ Pass (AA) | ✅ Pass | Reversed accent text |
| Wet Sand | `#98989A` | **4.05:1** | ❌ **Fail** | ✅ Pass | ⚠ Don't reverse Wet Sand at body size — swap to Sky |
| Valley | `#EE7623` | **4.03:1** | ❌ **Fail** | ✅ Pass | Large reversed accent only |
| Turquoise | `#129FDA` | **3.89:1** | ❌ **Fail** | ✅ Pass | Large reversed accent only |
| Success | `#4A8B5C` | **2.86:1** | ❌ **Fail** | ❌ **Fail** | Never on Navy — use White + a "▲" marker |
| Risk | `#B23A2D` | **1.97:1** | ❌ **Fail** | ❌ **Fail** | Never on Navy — use View `#FFCD00` for reversed alerts |
| Teal | `#186892` | **1.91:1** | ❌ **Fail** | ❌ **Fail** | Navy and Teal are too close — never layer them as fg/bg |
| Asphalt | `#515962` | **1.64:1** | ❌ **Fail** | ❌ **Fail** | Never on Navy |

### 4.3 Other pairs you will actually use

| Foreground | Background | Ratio | Verdict |
|---|---|---|---|
| White `#FFFFFF` | Teal `#186892` | **6.12:1** | ✅ AA all sizes — table headers on Teal are safe |
| Navy `#0C3B5D` | Sky `#B8D8EB` | **7.81:1** | ✅ AAA — the standard tinted-section combination |
| Navy `#0C3B5D` | Sand `#DDC9A3` | **7.20:1** | ✅ AAA — the warm-section equivalent |
| Navy `#0C3B5D` | View `#FFCD00` | **7.77:1** | ✅ AAA — **the mandated CTA button treatment** |
| Navy `#0C3B5D` | Vista `#FFA400` | **5.87:1** | ✅ AA — CTA hover state |
| Navy `#0C3B5D` | Valley `#EE7623` | **4.03:1** | ⚠ Large/bold only — for a Valley button use ≥14pt bold Navy |
| Navy `#0C3B5D` | `SURFACE_ZEBRA #F7FAFC` | **11.13:1** | ✅ AAA |
| Navy `#0C3B5D` | `SURFACE_TOTAL #E8F1F7` | **10.20:1** | ✅ AAA — total rows are safe |
| Asphalt `#515962` | `SURFACE_ZEBRA #F7FAFC` | **6.78:1** | ✅ AA — body text on zebra rows is safe |
| Asphalt `#515962` | `SURFACE_TOTAL #E8F1F7` | **6.21:1** | ✅ AA |
| Asphalt `#515962` | Sky `#B8D8EB` | **4.76:1** | ✅ AA (just) — body copy on a Sky band works, but Navy is safer |
| Asphalt `#515962` | Sand `#DDC9A3` | **4.38:1** | ❌ Fails AA normal — **on Sand, set body copy in Navy, not Asphalt** |
| Teal `#186892` | View `#FFCD00` | **4.07:1** | ⚠ Large only — prefer Navy on View |
| Teal `#186892` | Sky `#B8D8EB` | **4.09:1** | ⚠ Large only — Teal H2s on a Sky band must be ≥18pt |
| Wet Sand `#98989A` | Navy `#0C3B5D` | **4.05:1** | ⚠ Large only — see §4.2 |

### 4.4 The yellow rule — state this explicitly in every hand-off

> **View `#FFCD00` (1.50:1) and Vista `#FFA400` (1.99:1) FAIL WCAG as text on white at every size — normal *and* large.** They are not "use carefully" colors; they are **fill-only** colors.
>
> **Correct:** View as a solid button fill with **Navy `#0C3B5D` text on top** (7.77:1 ✅ AAA). View as a 3pt rule, underline, cover footer band, pull-quote left border, or highlight block. Vista as the hover fill for that button (Navy text, 5.87:1 ✅).
>
> **Wrong:** yellow headline text on white. Yellow body copy anywhere. Yellow small caps. Yellow on Sky or Sand. Yellow icon strokes that carry meaning on their own. A yellow-on-white CTA link.
>
> Valley `#EE7623` (2.90:1) fails as text on white too — it is *marginally* better than the yellows but still below the 3:1 large-text floor. Treat it as fill-only as well; if it must be type, put it on White at ≥24pt bold and accept that it is decorative, not informational.

### 4.5 Accessibility working rules

- **Never encode meaning in color alone.** Every risk/success/warning cue needs a word, an icon, or a symbol (▲ ▼ ●) alongside the color. `MUTED_BORDER #D9D9D9` at 1.41:1 cannot carry a boundary by itself either — pair thin borders with spacing or a fill change.
- **Body copy is Asphalt `#515962` on White (7.11:1 AAA).** Do not "improve" it to pure black — HBEF's system deliberately avoids `#000000`.
- **Links on white: Turquoise `#129FDA` at 3.00:1 fails normal-text AA.** In HTML, always underline them (WCAG's non-color-cue requirement) and consider Teal `#186892` (6.12:1) for dense body-copy links. In print-bound documents, use Navy underlined.
- **Wet Sand captions (2.88:1) fail AA.** This is an accepted brand quirk for decorative metadata (page numbers, photo credits, dates). Never put load-bearing information — an amount, a deadline, a disclaimer — in Wet Sand on white. The mandatory 501(c)(3)/EIN footer at 8pt Lato is the borderline case: keep it Asphalt in any donor-facing document where it functions as a legal notice.
- **Color-blind check:** Navy / Valley / Teal / Vista / Turquoise / Wet Sand is the chart order specifically because Navy↔Valley and Teal↔Vista are separable under deuteranopia and protanopia. Adjacent pairs Vista↔View and Vista↔Valley are *not* well separated — never put those two side by side as the only distinction in a chart. Add a pattern, a label, or a luminance step.

---

## 5. Type Specimen

### 5.1 The two families

Both families are **open-source under the SIL Open Font License 1.1** — licenses ship alongside the TTFs at `assets/fonts/Aleo-OFL.txt` and `assets/fonts/Lato-OFL.txt`. That means they can be **embedded freely in PDFs, HTML, and Office documents**, self-hosted on hbef.org, handed to a print vendor, and installed on any board member's machine at no cost. There is no licensing reason to substitute.

#### **ALEO** — primary typeface (headings)

A contemporary slab serif. Established, educational, friendly — the "academic" half of the pairing.

- **Google Fonts:** `https://fonts.google.com/specimen/Aleo`
- **Bundled TTFs:** `assets/fonts/Aleo-Regular.ttf`, `Aleo-Bold.ttf`, `Aleo-Italic.ttf`, `Aleo-BoldItalic.ttf`

| Style | File | CSS | Role |
|---|---|---|---|
| Regular | `Aleo-Regular.ttf` | `font-weight: 400; font-style: normal` | Rarely used alone. Large display text where Bold is too heavy; pull-quote base weight. |
| **Bold** | `Aleo-Bold.ttf` | `font-weight: 700; font-style: normal` | **The workhorse.** Cover title, H1, H2, slide titles, section-divider titles, pull-out stats, XLSX sheet titles. |
| *Italic* | `Aleo-Italic.ttf` | `font-weight: 400; font-style: italic` | Pull quotes. The one place Aleo Regular earns its keep. |
| ***Bold Italic*** | `Aleo-BoldItalic.ttf` | `font-weight: 700; font-style: italic` | Emphasis *inside* an Aleo heading only. Never for running text. |

**Usage:** all primary headings (H1, H2), prominent quotes, large display text, the cover title, big stat numbers. **Never** for body copy, table cells, captions, or UI labels.

**Do not letterspace Aleo.** Slab serifs already carry visual weight in the serifs; positive tracking makes them look broken. Tracking on Aleo is always `0`.

#### **LATO** — secondary typeface (body & UI)

A warm, highly legible humanist sans-serif. The "approachable" half of the pairing.

- **Google Fonts:** `https://fonts.google.com/specimen/Lato`
- **Bundled TTFs:** `assets/fonts/Lato-Light.ttf`, `Lato-Regular.ttf`, `Lato-Italic.ttf`, `Lato-Bold.ttf`, `Lato-BoldItalic.ttf`, `Lato-Black.ttf`

| Style | File | CSS | Role |
|---|---|---|---|
| Light (300) | `Lato-Light.ttf` | `font-weight: 300` | Cover subtitles only, at ≥18pt. **Never below 16pt** — Light disintegrates at small sizes and in print. |
| Regular (400) | `Lato-Regular.ttf` | `font-weight: 400` | **The default.** Body copy, lead paragraphs, bullets, table cells, slide body, footnotes, UI labels, nav. |
| *Italic (400)* | `Lato-Italic.ttf` | `font-weight: 400; font-style: italic` | Captions, metadata, photo credits, the letterhead legal footer, cell notes. |
| **Bold (700)** | `Lato-Bold.ttf` | `font-weight: 700` | H3, eyebrows/kickers, table headers, XLSX section headers, total rows, button labels, inline emphasis. |
| ***Bold Italic (700)*** | `Lato-BoldItalic.ttf` | `font-weight: 700; font-style: italic` | Rare. Emphasis inside a caption or an italic legal line. |
| Black (900) | `Lato-Black.ttf` | `font-weight: 900` | Reserved. Oversized CTA labels on large-format print (banners, foam board) where 700 doesn't hold at distance. Not for documents. |

**Usage:** all body copy, paragraphs, website navigation, fine print, secondary subheadings (H3), table cells, captions, UI labels, footers.

### 5.2 The pairing rules

- **Aleo Bold + Lato Regular** is the system. Slab-serif heading over humanist-sans body.
- **Aleo Bold + Lato Light 300** is the cover treatment — big slab title, airy light subtitle in Teal.
- **Aleo Italic + Lato Regular** is the pull-quote treatment.
- **Never set body copy in Aleo.** (One documented exception below.)
- **Never set a heading in Lato above 12pt.** H3 at Lato Bold 12pt uppercase is the ceiling — anything larger reads as a slide caption, not a heading.
- **Never introduce a third family.** No Montserrat, no BauhausBold, no Times New Roman, no Calibri, no Comic Sans, no script faces. No monospace outside a genuine code or fixed-width data block.

> **Known variance:** HBEF's own letterhead template and the Strand Classic press release set body copy in **Aleo 12pt**, not Lato. The Brand Guidelines are authoritative — use **Aleo headings + Lato body** for new work. When editing one of those existing Word files in place, keep its native Aleo body so the document stays internally consistent, and note the variance to the requester.

### 5.3 Fallback chains

Declare these verbatim. The fallback only fires when the real font genuinely isn't installed.

**Aleo — must fall back to a slab or serif, never a sans:**
```css
font-family: "Aleo", "Roboto Slab", "Zilla Slab", Rockwell, Georgia, serif;
```
| Rank | Face | Availability | Notes |
|---|---|---|---|
| 1 | **Aleo** | Bundled / Google Fonts | The real thing |
| 2 | **Roboto Slab** | Google Fonts, common on Android/Chrome OS | Closest metric and tone match |
| 3 | **Zilla Slab** | Google Fonts | Slightly quirkier, still correct category |
| 4 | **Rockwell** | Microsoft Office install | Geometric slab, heavier — acceptable on Windows |
| 5 | **Georgia** | Universal (macOS, Windows, iOS, Android) | Not a slab, but a sturdy bracketed serif — the reliable last stop |
| 6 | `serif` | Universal | Generic |

**Lato:**
```css
font-family: "Lato", "Helvetica Neue", Helvetica, Arial, sans-serif;
```
| Rank | Face | Availability | Notes |
|---|---|---|---|
| 1 | **Lato** | Bundled / Google Fonts | The real thing |
| 2 | **Helvetica Neue** | macOS, iOS, modern Office | Neutral; loses Lato's warmth but sets cleanly |
| 3 | **Helvetica** | macOS, most Adobe installs | |
| 4 | **Arial** | Universal | Last-resort |
| 5 | `sans-serif` | Universal | Generic |

**Never fall back to:** Times New Roman, Calibri, Comic Sans, Papyrus, any script face, Montserrat or BauhausBold (both retired), or a monospace face.

### 5.4 Weight & size floors

| Rule | Floor |
|---|---|
| Lato Light 300 | ≥ 16pt (18pt+ preferred). Below this, use Regular 400. |
| Lato Black 900 | Large-format print only. Not in documents. |
| Aleo any weight | ≥ 12pt. Below that Aleo's serifs fill in — use Lato. |
| Any reversed (white-on-Navy) type | ≥ 9pt, and never Light 300 — reversed light weights vanish in print. |
| Footnote / legal | ≥ 8pt. Never smaller, even to fit. |

---

## 6. Exact Type Scales

Copied from `SKILL.md` / `assets/brand-tokens.json`. These are the authoritative numbers — do not round or "adjust for balance."

### 6.1 Document hierarchy (Word / PDF — sizes in pt)

| Element | Font | Size | Weight | Style | Color | Line height | Tracking | Space before | Space after |
|---|---|---|---|---|---|---|---|---|---|
| Cover title | Aleo | 40 | Bold 700 | — | `HBEF_NAVY` `#0C3B5D` | 1.15 (46pt) | 0 | — | 12pt |
| Cover subtitle | Lato | 18 | Light 300 | — | `HBEF_TEAL` `#186892` | 1.35 (24.5pt) | 0 | 6pt | 18pt |
| Eyebrow / kicker | Lato | 9 | Bold 700 | UPPERCASE | `HBEF_WET_SAND` `#98989A` | 1.3 (12pt) | **+1.2pt** | — | 6pt |
| H1 section | Aleo | 24 | Bold 700 | Sentence/Title case | `HBEF_NAVY` `#0C3B5D` | 1.2 (29pt) | 0 | **24pt** | **8pt** |
| H2 sub-section | Aleo | 16 | Bold 700 | Sentence case | `HBEF_TEAL` `#186892` | 1.25 (20pt) | 0 | **18pt** | **6pt** |
| H3 minor | Lato | 12 | Bold 700 | UPPERCASE | `HBEF_NAVY` `#0C3B5D` | 1.3 (15.5pt) | **+0.8pt** | 14pt | 4pt |
| Lead paragraph | Lato | 13 | Regular 400 | — | `HBEF_ASPHALT` `#515962` | **1.45** (19pt) | 0 | 0 | 12pt |
| Body | Lato | 11 | Regular 400 | — | `HBEF_ASPHALT` `#515962` | **1.5** (16.5pt) | 0 | 0 | 8pt |
| Body bold | Lato | 11 | Bold 700 | — | `HBEF_NAVY` `#0C3B5D` | 1.5 | 0 | 0 | 8pt |
| Bullet | Lato | 11 | Regular 400 | — | `HBEF_ASPHALT` `#515962` | 1.5 | 0 | 0 | 4pt |
| Pull quote | Aleo | 15 | Regular 400 | *Italic* | `HBEF_NAVY` `#0C3B5D` | 1.4 (21pt) | 0 | 12pt | 12pt |
| Caption / metadata | Lato | 9 | Regular 400 | *Italic* | `HBEF_WET_SAND` `#98989A` | 1.4 (12.5pt) | 0 | 0 | 4pt |
| Footnote / legal | Lato | 8 | Regular 400 | — | `HBEF_WET_SAND` `#98989A` | 1.3 (10.5pt) | 0 | 0 | 2pt |
| Table header | Lato | 10 | Bold 700 | UPPERCASE | `WHITE` on `HBEF_NAVY` fill | 1.2 (12pt) | **+0.6pt** | — | — |
| Table cell | Lato | 10 | Regular 400 | — | `HBEF_ASPHALT` `#515962` | 1.3 (13pt) | 0 | — | — |
| Table note | Lato | 9 | Regular 400 | *Italic* | `HBEF_WET_SAND` `#98989A` | 1.3 | 0 | — | — |
| Link | Lato | inherit | Regular 400 | Underlined in print-bound docs | `HBEF_TURQUOISE` `#129FDA` | inherit | 0 | — | — |
| Page footer | Lato | 9 | Regular 400 | — | `HBEF_WET_SAND` `#98989A` | 1.3 | 0 | — | — |

**Pull quote geometry:** indent 0.4", 3pt `HBEF_VIEW` `#FFCD00` left border.
**Page footer pattern:** left = "Hermosa Beach Education Foundation · hbef.org", right = "Page N", 1pt `HBEF_TEAL` `#186892` top border.

### 6.2 Presentation hierarchy (PPTX — sizes in pt)

| Element | Font | Size | Weight | Color | Line height | Tracking |
|---|---|---|---|---|---|---|
| Cover title | Aleo | 54 | Bold 700 | `HBEF_NAVY` on White, or `WHITE` on `HBEF_NAVY` | 1.1 (59pt) | 0 |
| Cover subtitle | Lato | 20 | Light 300 | `HBEF_TEAL` (or `HBEF_SKY` on Navy) | 1.3 (26pt) | 0 |
| Section divider title | Aleo | 40 | Bold 700 | `WHITE` on `HBEF_NAVY` fill | 1.15 (46pt) | 0 |
| Slide title | Aleo | 28 | Bold 700 | `HBEF_NAVY` `#0C3B5D` | 1.2 (34pt) | 0 |
| Slide subtitle | Lato | 14 | Regular 400 | `HBEF_WET_SAND` `#98989A` | 1.35 (19pt) | 0 |
| Body | Lato | 16 | Regular 400 | `HBEF_ASPHALT` `#515962` | 1.4 (22pt) | 0 |
| Bullet | Lato | 14 | Regular 400 | `HBEF_ASPHALT` `#515962` | 1.35 (19pt) | 0 |
| Pull-out stat | Aleo | 60 | Bold 700 | `HBEF_NAVY` or `HBEF_VALLEY` | 1.0 (60pt) | 0 |
| Stat label | Lato | 11 | Regular 400 | `HBEF_WET_SAND` `#98989A` | 1.3 | +1.0pt if uppercase |
| Slide eyebrow | Lato | 9 | Bold 700 | `HBEF_WET_SAND` (or `HBEF_SKY` on Navy) | 1.3 | **+1.2pt**, UPPERCASE |
| Footer | Lato | 9 | Regular 400 | `HBEF_WET_SAND` `#98989A` | 1.3 | 0 |
| Page number | Lato | 9 | Bold 700 | `HBEF_NAVY` `#0C3B5D` | 1.3 | 0 |

Slide size: **16:9, 13.333" × 7.5"** (or 12192000 × 6858000 EMU).

### 6.3 Spreadsheet hierarchy (XLSX — sizes in pt)

| Element | Font | Size | Weight | Style | Color | Fill |
|---|---|---|---|---|---|---|
| Sheet title (row 1) | Aleo | 16 | Bold 700 | — | `HBEF_NAVY` `#0C3B5D` | `WHITE` `#FFFFFF` |
| Section header | Lato | 12 | Bold 700 | — | `WHITE` `#FFFFFF` | `HBEF_NAVY` `#0C3B5D` |
| Sub-header | Lato | 11 | Bold 700 | — | `HBEF_NAVY` `#0C3B5D` | `HBEF_SKY` `#B8D8EB` |
| Data cell | Lato | 10 | Regular 400 | — | `HBEF_ASPHALT` `#515962` | `WHITE` `#FFFFFF` |
| Data cell (zebra) | Lato | 10 | Regular 400 | — | `HBEF_ASPHALT` `#515962` | `SURFACE_ZEBRA` `#F7FAFC` |
| Total row | Lato | 11 | Bold 700 | — | `HBEF_NAVY` `#0C3B5D` | `SURFACE_TOTAL` `#E8F1F7` |
| Positive variance | Lato | 10 | Regular 400 | — | `SUCCESS` `#4A8B5C` | inherit |
| Negative variance | Lato | 10 | Regular 400 | — | `RISK` `#B23A2D` | inherit |
| Cell note | Lato | 9 | Regular 400 | *Italic* | `HBEF_WET_SAND` `#98989A` | `WHITE` `#FFFFFF` |

Row heights: title row 28pt · header rows 22pt · data rows 18pt. Borders: `MUTED_BORDER` `#D9D9D9` hairline; total row gets a 1pt `HBEF_NAVY` top border.

### 6.4 Web / HTML scale

| Element | Family | Size | Weight | Line height | Color |
|---|---|---|---|---|---|
| `body` | Lato | 16px | 400 | **1.5** | `#515962` |
| `.lead` | Lato | 18.4px (1.15rem) | 400 | **1.45** | `#515962` |
| `h1` | Aleo | 40px (2.5rem) | 700 | **1.2** | `#0C3B5D` |
| `h2` | Aleo | 28px (1.75rem) | 700 | **1.2** | `#186892` |
| `h3` / `h4` | Lato | 16px / 14px | 700, UPPERCASE, `letter-spacing: 0.05em` | 1.3 | `#0C3B5D` |
| `.eyebrow` | Lato | 12px (0.75rem) | 700, UPPERCASE, `letter-spacing: 0.12em` | 1.3 | `#98989A` |
| `.pull-quote` | Aleo | 20px (1.25rem) | 400 italic | 1.4 | `#0C3B5D`, 3px `#FFCD00` left border |
| `.legal` | Lato | 11.2px (0.7rem) | 400 italic | 1.4 | `#98989A` |
| `a` | inherit | inherit | 400 | inherit | `#129FDA`, underline on hover → `#186892` |

**Google Fonts embed:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Aleo:ital,wght@0,400;0,700;1,400&family=Lato:ital,wght@0,300;0,400;0,700;0,900;1,400&display=swap" rel="stylesheet">
```

### 6.5 Tracking / letter-spacing conventions

| Surface | Tracking |
|---|---|
| Aleo — **any** size, any weight | **0.** Never letterspace the slab serif. |
| Lato body running text | 0 |
| Lato H3 (uppercase, 12pt) | +0.8pt |
| Lato eyebrow / kicker (uppercase, 9pt) | +1.2pt |
| Lato table header (uppercase, 10pt) | +0.6pt |
| Lato stat label (uppercase, 11pt) | +1.0pt |
| Lato CTA button label (uppercase) | +0.06em (≈ +0.7pt at 11pt) |
| Web equivalents | `0.05em` for h3/h4, `0.12em` for `.eyebrow` |

Rule of thumb: **tracking is a Lato-uppercase tool only.** If the text is Aleo, or lowercase, tracking is 0.

---

## 7. Retired Tokens → 2026 Replacements

Complete one-to-one migration map. Full context on the old system lives in `references/legacy-brand.md`. **Nothing in the left column may appear in new work.**

### 7.1 Colors

| Retired token | Retired hex | → 2026 replacement | New hex | Notes |
|---|---|---|---|---|
| `HBEF_NAVY` (old) | `#0B4261` | `HBEF_NAVY` | `#0C3B5D` | Same role, slightly deeper and cooler. Straight swap. |
| `HBEF_NAVY_DEEP` | `#124362` | `HBEF_NAVY` | `#0C3B5D` | The old footer-text variant collapses into the single new Navy. |
| `HBEF_ORANGE` | `#F79B32` | `HBEF_VALLEY` | `#EE7623` | For attention accents. **But if it was a CTA/donate button, use `HBEF_VIEW` `#FFCD00` with Navy text** — the CTA color changed category, not just value. |
| `HBEF_TEAL` (old) | `#75C4B9` | `HBEF_SKY` | `#B8D8EB` | The old mint teal was a *light fill* (footer/menu background). Its replacement is Sky, **not** the new Teal. |
| `HBEF_TEAL_DISPLAY` | `#74C4B9` | `HBEF_SKY` | `#B8D8EB` | One-digit variant of the above; same replacement. |
| `HBEF_TEAL_MUTED` | `#417987` | `HBEF_TEAL` | `#186892` | This is the true structural-teal ancestor. |
| `HBEF_TEAL_MUTED_2` | `#407987` | `HBEF_TEAL` | `#186892` | Variant of the above; same replacement. |
| `HBEF_YELLOW` | `#FAEF7A` | `HBEF_VIEW` | `#FFCD00` | Soft sunlight yellow → saturated CTA yellow. Same fill-only restriction applies. |
| `HBEF_PAGE` | `#E7E7E7` | `WHITE` / `HBEF_SKY` / `HBEF_SAND` | `#FFFFFF` / `#B8D8EB` / `#DDC9A3` | **The gray page frame is gone.** The 2026 system sits content on White, with Sky or Sand as the tinted band. Do not reintroduce a gray page background. |
| `INK` | `#1A1A1A` | `HBEF_ASPHALT` | `#515962` | Body copy is now warm-cool gray, not near-black. |
| `INK_80` | `#333333` | `HBEF_NAVY` | `#0C3B5D` | Heavy emphasis is now Navy, not darker gray. |
| `INK_60` | `#5C5C5C` | `HBEF_WET_SAND` | `#98989A` | Captions/metadata. Note the new value is lighter — check contrast (§4.5). |
| `INK_40` | `#999999` | `HBEF_WET_SAND` | `#98989A` | De-emphasized text. |
| `INK_30` | `#A8A8A8` | `HBEF_WET_SAND` | `#98989A` | Tertiary text and thin rules. Three old grays collapse into one. |
| `MUTED_BORDER` (old) | `#CCCCCC` | `MUTED_BORDER` | `#D9D9D9` | Lighter hairline. |
| `SUCCESS` (old) | `#5A9E78` | `SUCCESS` | `#4A8B5C` | Deeper, more civic green. |
| `WARNING` (old) | `#F79B32` | `WARNING` | `#FFA400` | Now reuses Vista instead of the old brand orange. |
| `RISK` | `#B23A2D` | `RISK` | `#B23A2D` | **Unchanged** — the only color that survived the rebrand intact. |
| `SURFACE_PAGE` | `#E7E7E7` | `SURFACE_PAGE` | `#FFFFFF` | |
| `SURFACE_CARD` | `#FFFFFF` | `SURFACE_PAGE` | `#FFFFFF` | Card/page distinction disappears with the gray frame. |
| `SURFACE_SOFT` | `#F2F2F2` | `HBEF_SKY` | `#B8D8EB` | XLSX sub-header fill is now Sky. |
| `SURFACE_ZEBRA` | `#FAFAFA` | `SURFACE_ZEBRA` | `#F7FAFC` | Neutral gray → cool blue-white. |
| `SURFACE_TOTAL` | `#E7E7E7` | `SURFACE_TOTAL` | `#E8F1F7` | |
| `SURFACE_HERO` | `#0B4261` | `SURFACE_HERO` | `#0C3B5D` | |
| `SURFACE_FOOTER` | `#75C4B9` | `SURFACE_ACCENT` | `#FFCD00` | The footer band changed from mint teal to the View yellow accent strip. |
| — (no equivalent) | — | `HBEF_TURQUOISE` | `#129FDA` | **New in 2026.** No legacy ancestor. |
| — (no equivalent) | — | `HBEF_VISTA` | `#FFA400` | **New in 2026.** |
| — (no equivalent) | — | `HBEF_SAND` | `#DDC9A3` | **New in 2026.** The old system had no warm neutral. |

### 7.2 Typefaces

| Retired | → 2026 replacement | Notes |
|---|---|---|
| **BauhausBold** (display) | **Aleo Bold** | Geometric heavy display → slab serif. This is the single biggest visual change in the rebrand. Category change, not a swap — re-typeset, don't find-and-replace. |
| **Montserrat 700** (headings) | **Aleo Bold** (H1/H2) or **Lato Bold** (H3, eyebrows, table headers) | Depends on the level. Aleo above 12pt, Lato at 12pt and below. |
| **Montserrat 400** (body) | **Lato Regular 400** | Straight swap. |
| **Montserrat 200 Extra Light** (hero/stats) | **Aleo Bold** (stats) or **Lato Light 300** (cover subtitle) | The "thin-and-tall" hero look is **retired entirely.** Pull-out stats are now heavy slab, not airy thin. |
| **Montserrat 300 Light** | **Lato Light 300** | Cover subtitles only, ≥16pt. |
| **Montserrat 500 Medium** | **Lato Regular 400** | The Medium weight has no 2026 equivalent. |
| **Montserrat 600 Semibold** | **Lato Bold 700** | |
| **Montserrat 900 Black** | **Lato Black 900** | Large-format print only in the new system. |
| **Montserrat 700 Italic** | **Aleo Italic 400** (pull quotes) or **Lato Italic 400** (captions) | Note the weight drops — the old "bold italic for editorial moments" convention is retired. |
| Avenir Next / Century Gothic / Futura / ITC Avant Garde (old fallbacks) | Roboto Slab, Zilla Slab, Rockwell, Georgia (Aleo) · Helvetica Neue, Helvetica, Arial (Lato) | Old fallback chains were geometric-sans; new chains are slab-serif for headings. |
| AmsiPro (pre-2021 display family, `.otf`) | **Aleo Bold** | Two generations retired. Files remain only in the archive folder. |

### 7.3 Type-scale changes worth knowing

| Element | Old (pre-2026) | New (2026) | Change |
|---|---|---|---|
| Cover title | Montserrat/Bauhaus 42pt, UPPERCASE, +1.5pt tracking | Aleo 40pt Bold, **sentence/title case, 0 tracking** | Case and tracking both change |
| Display H0 hero | Montserrat 54pt weight 200 | **Removed** | No 2026 equivalent |
| H1 | Montserrat 28pt, UPPERCASE, +0.8pt | Aleo 24pt Bold, sentence case, 0 | Smaller, no caps, no tracking |
| H2 | Montserrat 18pt Navy, UPPERCASE | Aleo 16pt Bold **Teal**, sentence case | Color changes to Teal |
| H3 | Montserrat 13pt, uppercase, Teal-muted | Lato 12pt Bold, uppercase, **Navy**, +0.8pt | Stays uppercase — the one survivor |
| Body | Montserrat 11pt, line-height 1.55, `INK` | Lato 11pt, **line-height 1.5**, `HBEF_ASPHALT` | Tighter leading, lighter color |
| Lead | Montserrat 13pt, 1.5 | Lato 13pt, **1.45** | |
| Pull quote | Montserrat 16pt italic | **Aleo** 15pt italic + 3pt View left border | Family and ornament change |
| PPTX cover title | 60pt uppercase +2pt | Aleo 54pt Bold, sentence case, 0 | |
| PPTX stat | Montserrat 60pt **weight 200** | Aleo 60pt **Bold 700** | Weight inverts completely |
| XLSX workbook title | Montserrat 18pt | Aleo 16pt Bold | |

### 7.4 Migration checklist for a color/type sweep

1. Find-and-replace hexes using §7.1 — but **read each `#F79B32` in context first** (CTA → View, accent → Valley) and each `#75C4B9` (light fill → Sky, structural → Teal).
2. Replace fonts using §7.2 — this is a re-typesetting job, not a swap. Aleo's slab serifs need more leading than Montserrat at the same size, and Aleo runs wider, so headings will re-wrap.
3. **Remove all uppercase transforms from Aleo headings** and zero out their tracking.
4. **Delete the gray page frame.** Content sits on White now.
5. Re-check contrast against §4 — the new Wet Sand is lighter than the old `INK_60`, and Asphalt on Sand fails AA.
6. Swap logo files. See `references/legacy-brand.md` §5.
7. Confirm the 501(c)(3)/EIN footer is present and current.
