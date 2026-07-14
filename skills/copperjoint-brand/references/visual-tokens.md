# CopperJoint Visual Tokens

Extracted from copperjoint.com via Firecrawl branding analysis on 2026-05-27. Authoritative for any deliverable.

## Color Palette

### Primary Brand Colors

| Token | Hex | Use |
|---|---|---|
| `ink` (primary) | `#1A2332` | Dominant brand color. Headings, primary buttons (text), logos, dark surfaces, headers. **This is the brand**, not copper. |
| `copper` (secondary) | `#B87333` | The accent that names the brand. Use for highlights, icons, single-element accents — never as a wash. ~10% surface area max. |
| `gold` (accent) | `#BA9731` | Warm gold for links, hover states, "as seen on" stripes, secondary CTAs. |
| `chalk` (background) | `#F2F2F2` | Default page background. Warm off-white. **Never use pure `#FFFFFF` as a primary background** — it reads sterile-clinical and breaks the warmth. |
| `text-primary` | `#000000` | Body copy on chalk. |
| `text-inverse` | `#F2F2F2` | Body copy on ink. |

### Supporting Tones (extracted from in-context use)

| Token | Hex | Use |
|---|---|---|
| `slate` | `#1A1C1C` | Secondary heading or alt-dark text |
| `mist` | `#F9F9F9` | Secondary button background, subtle cards |
| `clay` | `#D8C3B4` | Border on secondary buttons; subtle warm divider |
| `iron` | `#6B7280` | Form field borders, muted helper text |

### Functional Colors

| Token | Hex | Use |
|---|---|---|
| `success` | `#3B7A57` | Trust signals, "verified" badges (use sparingly) |
| `warn` | `#B87333` | Re-use copper as warning — keep palette tight |
| `danger` | `#8B2E2E` | Error states only |

## Typography

### Font Families

- **Primary: Montserrat** — Used for all headings AND body. The brand owns this typeface end-to-end.
- **Secondary: Epilogue** — Used only for clinical callouts (e.g., "Epilogue Clinical Grade" badge). Reserve for product-spec lockups or scientific-credibility flourishes.
- **Fallback stack:** `Montserrat, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

### Type Scale (web)

| Level | Size | Weight | Letter-spacing |
|---|---|---|---|
| Display | 56px / 64px | 700 | -0.02em |
| H1 | 40px / 48px | 700 | -0.01em |
| H2 | 28px / 36px | 600 | -0.01em |
| H3 | 20px / 28px | 600 | 0 |
| Body | 16px / 24px | 400 | 0 |
| Small | 14px / 20px | 400 | 0 |
| Eyebrow / Label | 12px / 16px | 600 | 0.08em (uppercase) |

(Note: the live site's CSS uses tighter sizes — 14/17.5 — because it's optimized for mobile-dense product browsing. For pitches, decks, and dashboards, use the scale above.)

### Type Use Rules

- **Eyebrows are uppercase, 12px, gold (`#BA9731`).** Used over section headings.
- **Headings are Ink (`#1A2332`).**
- **Body is black on chalk, never gray-on-gray.**
- **Numbers (stats, percentages) are headline-weight Ink, never copper** — keep statistics serious.

## Spacing & Layout

- **Base unit:** 4px (everything is a multiple of 4)
- **Grid:** 12-column on desktop, 4-column on mobile
- **Section vertical rhythm:** 96px (desktop), 48px (mobile)
- **Card padding:** 24px (desktop), 16px (mobile)
- **Max content width:** 1200px

## Components

### Buttons

**Primary button** (call-to-action):
- Background: `#1A2332` (Ink) — NOT chalk despite what the live site does
- Text: `#F2F2F2` (Chalk)
- Border radius: `50px` (pill)
- Padding: `14px 28px`
- Hover: background lightens to `#2A3344`

**Secondary button**:
- Background: `#F9F9F9` (Mist)
- Text: `#1A1C1C` (Slate)
- Border: `1px solid #D8C3B4` (Clay)
- Border radius: `3.75px` (subtle)
- Padding: `12px 24px`

**Tertiary / text link**:
- Color: `#BA9731` (Gold)
- Underline on hover
- No background

### Cards

- Background: `#FFFFFF` (one of the few places true white is acceptable — interior surface only)
- Border: `1px solid rgba(26, 35, 50, 0.08)`
- Border radius: `8px`
- Shadow: `0 1px 3px rgba(26, 35, 50, 0.08), 0 4px 12px rgba(26, 35, 50, 0.04)`
- Padding: `24px`

### Inputs

- Background: `#FFFFFF`
- Border: `1px solid #6B7280` (Iron)
- Border radius: `0` (deliberately square for clinical feel)
- Padding: `10px 12px`
- Focus border: `#B87333` (Copper)

### Icons

- Use **Material Symbols** ligature icons (the live site uses these: `stethoscope`, `grid_view`, `air`, `biotech`, `palette`, `eco`, `bolt`, `compress`, `verified`, `shield_moon`, `medical_services`).
- Icon color: Ink default, Copper for emphasis.
- Icon size: 24px standard, 32px for hero cards.

## Logo Usage

- **Wordmark only.** No icon mark exists; do not invent one.
- **Color:** Ink on chalk backgrounds. Chalk on ink backgrounds. Never use copper-on-anything as the logo color.
- **Clearspace:** Minimum padding of `x-height of the wordmark` on all sides.
- **Minimum size:** 80px wide on screen, 0.75 inch in print.
- **File reference:** Pull from `https://www.copperjoint.com/cdn/shop/files/Logo_no_background.png`

## Photography & Imagery Style

- **Lifestyle, in-motion, real bodies.** Hero photography shows actual people in actual activities (runners on roads, nurses in scrubs, older adults on a hike, kitchen-counter pain-relief moments). Avoid studio-on-model "fitness brand" photography.
- **Natural daylight.** Warm tones, soft shadows. Never harsh studio strobe.
- **Hands and joints close-up.** Product-detail shots prioritize how the garment fits the body, not stylized product-on-pedestal.
- **Avoid stock-photo athletic models in matching workout sets.** That's the Copper Fit/Tommie Copper aesthetic and we're deliberately not them.
- **Clinical visuals are diagrams, not microscopy.** Use clean line illustrations of muscles, joints, compression zones — not stock-looking science photos.

## Iconography & UI Pattern Library

- **Material Symbols** for all UI iconography
- **Pill-shaped primary buttons + square-cornered inputs** — this is deliberate dual-shape and creates the "clinical but approachable" tension that defines the brand
- **Use the `verified` ligature for trust badges** (Orthopedic Verified, Medical Advisory Board Verified, etc.)
- **Eyebrow labels are uppercase gold** above section titles

## Accessibility

- Body text against chalk must meet WCAG AA (4.5:1) — black on `#F2F2F2` ≈ 19:1 ✓
- Ink button text against ink button background must meet AA — chalk on ink ≈ 17:1 ✓
- Gold links on chalk must meet AA — `#BA9731` on `#F2F2F2` ≈ 3.2:1 ✗ for body text → use gold ONLY for non-body link emphasis, never as standalone paragraph text
- Always include alt text on product imagery
- Material Symbols are decorative; use `aria-hidden="true"` and provide text labels
