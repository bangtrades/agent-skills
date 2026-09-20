# Web, product UI, HTML, email

Load `assets/mezzanine-tokens.css` (or copy its `:root`). Live site tokens: `/Users/nolan/Projects/Mezzanine/site/src/styles/tokens.css` (Astro + Vercel; In Motion build in `site-motion/`).

## Fonts

```css
/* enable only after web-embed licence is confirmed; subset to Latin, WOFF2 */
@font-face{font-family:"Austin";src:url(/fonts/austin-roman.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Austin";src:url(/fonts/austin-light.woff2) format("woff2");font-weight:300;font-display:swap}
@font-face{font-family:"Soehne";src:url(/fonts/soehne-buch.woff2) format("woff2");font-weight:400;font-display:swap}
@font-face{font-family:"Soehne";src:url(/fonts/soehne-halbfett.woff2) format("woff2");font-weight:600;font-display:swap}
```
Ship at most four faces. Convert from the installed OTFs (`~/Library/Fonts/Austin/`, `/Library/Fonts/Söhne/`) with `pyftsubset --flavor=woff2` once web rights are confirmed. Fallback stacks are in the tokens file; Playfair Display and Inter may load from Google Fonts as stand-ins.

## Scale (desktop → mobile)

display 72→44 px Austin, lh 1.0 · h1 48→34 · h2 32→26 · h3 22→20 (Austin, lh 1.15) · body 16–18 Söhne, lh 1.5, max 68 ch · small 13 · eyebrow 12 caps +0.1 em. Spacing base 4 px; section padding 96/64 px. Max width 1440, reading column 800.

## Surfaces

Page `--paper`. Text `--ink`. Rules `--rule` 1 px. Cards flat, square, no shadow; optional `#FFFFFF` interior. One red field per view: hero band, act cover, footer, or a single display word. Dark sections: `--ink` ground, `--paper` text, red display type. Hover: red → `#8C1D06`; links underline in red, no colour change on hover. Focus ring 2 px red offset 2 px. Buttons: square, 1 px ink border, Söhne caps +0.1 em, fill ink on hover; primary button may be red fill with ink text at ≥ 16 px Halbfett.

## Logo in UI

Header: wordmark PNG or live Austin caps, ≤ 160 px wide desktop, ink on paper. Favicon and app icon: `icon-red.svg` on paper or `icon-white.svg` on red. Icon min 42 px; footer sign-off uses the icon alone at 48–64 px. Animated icon MP4 as a loader or intro only, once per session, respects `prefers-reduced-motion` (show static icon).

## Motion

Slow, architectural: 400–800 ms ease-out for reveals, no bounce, no parallax faster than 0.3× scroll. B&W at rest with colour on hover is an approved image treatment; do it in CSS, keep colour in the source.

## Email

Table layout, paper ground `#EBE5DD`, ink text, Georgia fallback for Austin and Arial for Söhne, wordmark PNG 320 px wide at top, red used once (a rule or the wordmark). No orange text.
