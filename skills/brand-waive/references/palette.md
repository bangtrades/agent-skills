# WaiveLabs — Color System

The canonical palette, mirrored from the live site (`site/assets/site.css` — the source of truth).
Dawn = light, Dusk = dark. Both ship in production; pick by surface.

## 1 · Brand colors (theme-independent)

| Role | Name | Hex | RGB | Use |
|---|---|---|---|---|
| Primary | Ocean Blue | `#3179F5` | 49,121,245 | Waves, links, primary buttons, brand fields — the workhorse |
| Deep | Deep Blue | `#0D43AA` | 13,67,170 | Gradients, pressed/hover, headings on light, focus ring |
| Blue soft | Blue Mist | `#EAF1FE` | 234,241,254 | Icon tiles, soft fills on light |
| Accent | Sunset Orange | `#E65100` | 230,81,0 | The SPARK — sun, `.ai`, single CTAs. **Sparing.** |
| Sun | Bright Sun | `#FF7A1A` | 255,122,26 | Gradient stops, hero sun, warm glow |
| Amber | Amber | `#FFB454` | 255,180,84 | Tertiary warm; dark-mode swap for link/orange text |
| Ink | Near Black | `#0F172A` | 15,23,42 | Body text + wordmark (Tailwind slate-900) |
| Ink soft | Slate | `#44506A` | 68,80,106 | Secondary text on light |
| Ink-30 | Muted | `#94A3B8` | 148,163,184 | Captions, meta, disabled |
| Body | Reading Ink | `#1E2435` | 30,36,53 | Long-form article / legal body text |
| Cream | Dawn 1 | `#FFF8F1` | warm page base (light) |
| Morning | Dawn 2 | `#F4F7FD` | cool section fills (light) |
| Navy | Deep / Footer | `#0C1428` | footer + darkest anchor in BOTH themes |
| Good / Warn / Bad | state | `#16A34A` / `#D9870B` / `#DC2626` | success / caution / error |

CSS custom-property names (use these literally in any HTML/CSS deliverable):
`--blue --blue-deep --blue-soft --sun --orange --amber --ink --ink-soft --ink-30 --ink-body
--dawn-1 --dawn-2 --deep --good --warn --bad`.

## 2 · Dusk (dark mode) — slate base, computed for contrast

Page slate is hue **222°, S 27%, L 12%** — same hue family as the brand darks (ink, deep navy,
console `#0b1322`) but **desaturated**, so the product's dark consoles still read as glowing screens
*within* a dark page. Set on `html[data-theme="dark"]`.

```
--bg          #161B26   DUSK SLATE — page base
--bg-2 / paper #1D2433   surface (cards)
--bg-3        #252E40   elevated (hover, popovers)
--ink         #E9EEF7   body text · ≈14.6:1 on --bg (AAA)
--ink-body    #C9D4E6   long-form prose · ≈10:1
--ink-soft    #B3BFD3   ≈8.3:1 (AAA)
--ink-30      #8593AB   ≈5.1:1 (AA)
--blue-deep   #7AA7F8   (←#0D43AA fails on dark; this is ≈6:1)  ← link/heading blue on dark
--orange      #FFA45C   (←#E65100 fails on dark; ≈8:1)          ← accent text on dark
--good #4ADE80  --warn #FBBF24  --bad #F87171
--line        rgba(148,163,184,.14)
```

Dawn's warm radial glows survive into dusk at low alpha (`--glow-warm` .16 → .07) — dusk keeps the
brand's warmth. Footer `#0C1428` stays the darkest anchor in both themes. Product consoles, the
phone demo, and WaiveBoard cockpit are **dark-native — never re-skin their internals**; only the
page scaffold themes.

**Mechanism (how the site does it, reuse it):** define light defaults in `:root`, override the same
custom properties under `html[data-theme="dark"]`. Load the brand stylesheet *after* a page's own
styles so the property overrides re-skin without touching layout CSS. A ≤30-line no-flash head
snippet reads `localStorage.wl_theme` → falls back to `prefers-color-scheme` → sets `data-theme`
before first paint. Add `<meta name="color-scheme" content="light dark">`.

## 3 · Color-blind profile (opt-in, WaiveLabs ships this)

Two layers — match the site:
1. **Always-on (WCAG 1.4.1, no toggle):** every state carries a non-color signifier — ✓/⚠/✕ glyphs
   on badges, underlines on body links, labels/patterns on bars and status dots. Never communicate
   state by color alone.
2. **Opt-in high-legibility palette** (`html[data-cb="1"]`, persisted `localStorage.wl_cb`):
   remap to **Okabe-Ito** — good→`#0072B2`, warn→`#E69F00`, bad→`#D55E00`; chart series 1/2 →
   blue/vermillion (the default blue/amber pair is deuteranopia-risky). Dark variant lightens the
   vermillion. Charts read `var(--chart-1/2)`.

## 4 · Gradients & glows (signature atmosphere)

- **Headline gradient:** `linear-gradient(110deg, var(--sun), var(--orange) 55%, var(--blue-deep))`
  with `background-clip:text` (on dark, brighten end stop to `#7AA7F8`).
- **Hero CTA (orange):** `linear-gradient(120deg, var(--sun), var(--orange) 60%, #c33f00)`.
- **Primary CTA (blue):** `linear-gradient(120deg, var(--blue), var(--blue-deep))`.
- **Dawn page background:** warm radial top-left + faint blue radial top-right over a
  cream→morning vertical — calm, editorial, never flat.
- Soft shadows, hairline borders (`--line`), generous whitespace, one orchestrated staggered
  load-in. Atmosphere over flat fills.
