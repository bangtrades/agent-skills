# WaiveLabs — Typography

Three-font system, all free Google Fonts (zero licensing friction, web + client deliverables).

## The fonts and their jobs

| Font | Weights | Job | Rule |
|---|---|---|---|
| **Sora** | 500–800 | Headings (H1–H4), hero lines, deck titles, UI labels, eyebrows | The *promise*. Short, declarative. |
| **Inter** | 400–700 | Body copy, captions, UI, ALL numerals + data | The *proof*. Highly legible. |
| **Fraunces** | italic, optical (`opsz`) | ONE editorial accent — a single hero word, an "AI brief" headline | Seasoning, never the meal. One characterful moment per view. |

**Never** set long body copy in Sora or Fraunces. **Never** rebuild the wordmark in another face.

## Web font loading (exact, from the site)

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Sora:wght@500;600;700;800&family=Fraunces:ital,opsz,wght@1,9..144,400;1,9..144,500&display=swap" rel="stylesheet" />
```

```css
body { font-family: "Inter", system-ui, sans-serif; line-height: 1.6; }
h1, h2, h3 { font-family: "Sora", sans-serif; line-height: 1.18; letter-spacing: -.01em; }
.accent { font-family: "Fraunces", Georgia, serif; font-style: italic; font-weight: 500; }
.eyebrow { font-family: "Sora", sans-serif; font-size: 11–12px; font-weight: 700;
           letter-spacing: .12em; text-transform: uppercase; }   /* section kickers */
```

Office/print equivalents (when Sora/Inter aren't embeddable): **Montserrat → Sora**,
**Inter/Helvetica/Arial → Inter**, serif italic → **Fraunces or Georgia italic**.

## Headline hierarchy + copy intent

| Level | Font / weight | Sample line (voice) | Use |
|---|---|---|---|
| H1 | Sora 800, clamp(2.1–3.8rem) | *"Make complexity simple."* / *"A model is a brain in a jar."* | Hero / cover |
| H2 | Sora 700–800, ~1.5–1.85rem | *"Smarter decisions, faster."* | Section openers |
| H3 | Sora 700, ~1.05–1.25rem | *"Built for momentum."* | Sub-sections, callouts |
| Eyebrow | Sora 700 uppercase, .12em | *"EXHIBIT 04 · SKILLS"* | Kickers above headlines |
| Body | Inter 400, 1.06–1.12rem, 1.6–1.75 lh | the explanation underneath | Paragraphs |
| Accent | Fraunces italic 500 | one word inside an H1 (e.g. *pocket.*) | Single editorial flourish |

**Pairing rule:** Sora for the promise (short headline), Inter for the proof (the body). Fraunces
italicizes exactly one word or one short editorial line — never a paragraph.

## Numerals

All numbers, KPIs, prices, and data render in **Inter** (often `font-variant-numeric: tabular-nums`
for aligned columns). Never set data in Sora.
