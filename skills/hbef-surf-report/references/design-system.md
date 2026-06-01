# HBEF Surf Report — Design System Reference

The visual design conventions of the HVS Surf Report, documented for two purposes:

1. **Understanding what HVPTO will do with HBEF's submitted text** — so you can predict how your article will render.
2. **Building a standalone HBEF email blast in the same beloved style** — when HBEF needs to send its own urgent communication outside the Surf Report cycle.

Note: HBEF does not control the Surf Report's banner, masthead, or chrome. The conventions below describe what HVPTO actually does each week. For HBEF-standalone emails, see the "Standalone HBEF Email" section at the end of this file.

## Surf Report visual anatomy

### 1. Email subject line
Format: `HVPTO Surf Report MM.DD.YY`
- Example: `HVPTO Surf Report 05.17.26`
- Surf Report Extras: `Memorial Day Parking Lot Fundraiser` (topic-only, no "Surf Report" in subject)

### 2. Sender display name
`HVPTO Surf Report`

### 3. Banner (top of email body)
- **Image:** Stylized illustration — light blue sky, yellow/orange sun disc behind silhouetted palm trees, ocean horizon, beach lifeguard tower, sand strip across the bottom
- **Wordmark:** "HVS SURF REPORT" in large white serif/display lettering with subtle textured background patches
- **Underbar:** Navy-blue strip (`#0B4261` approximate) running below the illustration, white text reading "News from Hermosa View, Vista, & Valley Parent Teacher Organization"
- **Width:** Full-width within the email container (~600px on mobile, 700–800px desktop)

This banner is HVPTO's. HBEF doesn't recreate it for HBEF-standalone emails.

### 4. Date line
- Right-aligned, below the banner, light gray italic text
- Format: `May 17th, 2026` (uses ordinal date — 17th, 24th, etc., not "May 17, 2026")
- For Surf Report Extra: omitted or replaced with `Surf Report Extra` centered blue label

### 5. Section dividers
- Centered text, **bright red** (`#D43A3A`-ish), bold, larger size (~24–28pt)
- Examples: `SPOTLIGHT`, `HVPTO`, `HBEF`, `HBCSD`, `YOUNG AT ART`, `COMMUNITY CONNECTIONS`, `CALENDAR`, `EDUCATIONAL PARTNERS`, `QUICK ORDER LINKS`, `FOLLOW US ON SOCIAL`
- One section header per content group; no rules above or below — just the colored text floating
- HBEF section always uses the literal text `HBEF` (not "Hermosa Beach Education Foundation" — that's too long for the centered visual rhythm)

### 6. Article block
Each article inside a section follows this consistent layout:
- **Article title:** Left-aligned, bold, blue (`#1E5A8A`-ish — slightly brighter than HBEF_NAVY), sans-serif, ~16–18pt
- **Body text:** Left-aligned, dark gray/black (`#1A1A1A`-ish), sans-serif, ~13–14pt, 1.4 line-height
- **Image (when included):** Right-aligned, occupying ~30% of column width, vertically aligned to the top of the body text or center
- **Bold mid-sentence:** key dates/dollars/codes — same dark color, just weight 700
- **Hyperlinks:** Underlined, blue (slightly brighter than article title — `#2E7AC9`-ish)
- **Vertical spacing:** ~24–32px between article blocks

### 7. Inline lists
- Bullet character: middle-dot `·` or filled-circle `●`
- Indent: ~16px from left
- Vertical spacing: ~6–8px between items
- Examples HBEF uses regularly:
  - Open volunteer positions
  - Multi-channel CTA stacks ("· Take the survey here. · View event photos here.")

### 8. Bonus / Inline callouts
- "Bonus for X!" style — orange or red bold lead-in, then the explanation
- Used within HBEF articles for sub-points or extra notes

### 9. Section footers (only on full Surf Reports, not Extras)
- **Calendar:** simple bulleted list of upcoming dates, centered, sub-headed `CALENDAR`
- **Educational Partners:** grid of partner logos (Mathnasium, Vistamar, similar)
- **Quick Order Links:** three colored circular CTA buttons (`CLICK TO DONATE HVS Sound Course / CLICK TO ORDER First Day Co-op / CLICK TO ORDER Middle School Crew Wear`) — these are HVPTO admin CTAs, HBEF doesn't add to them
- **Follow Us On Social:** Facebook + Instagram icons
- **Tail:** "SUBSCRIBE to the HVS Surf Report, a weekly publication produced by HVPTO" + hvpto.com + Constant Contact branded footer + Unsubscribe / Update Profile / Constant Contact Data Notice

### 10. Hashtag footer
- `#PoweredByHVPTO` — italicized, centered, in HVPTO's accent color (orange-ish), appears before the Constant Contact footer
- HBEF doesn't replicate this for HBEF-standalone emails

## Surf Report color palette (observed)

| Token | Hex (approx) | Use |
|---|---|---|
| `SURF_NAVY` | `#1A4470` | Banner underbar, primary brand-feel |
| `SURF_RED` | `#D43A3A` | Section dividers (SPOTLIGHT, HBEF, etc.) |
| `SURF_BLUE` | `#1E5A8A` | Article titles |
| `SURF_LINK_BLUE` | `#2E7AC9` | Hyperlinks |
| `SURF_INK` | `#1A1A1A` | Body text |
| `SURF_INK_GRAY` | `#5C5C5C` | Date line, footer text, captions |
| `SURF_ORANGE` | `#F79B32`-ish | "#PoweredByHVPTO" + accent — coincidentally matches HBEF orange |
| `SURF_SAND` | `#F5E9D8` | Subtle background tints in banner |
| `WHITE` | `#FFFFFF` | Background |

The Surf Report's navy/red/blue palette is close to HBEF's navy/orange/teal but distinct. **Don't conflate them.** When HBEF builds a standalone HBEF email, use HBEF's palette (`hbef-brand`), not the Surf Report's.

## Typography (observed)

The Surf Report uses generic web-safe sans-serif fallbacks (Verdana, Trebuchet MS, Tahoma, or system defaults). It is not branded around a specific custom typeface — Constant Contact's template defaults handle most of it.

For HBEF's article copy, this means: don't worry about font choice. Submit plain text with bold/link markup; HVPTO renders it through their template.

For HBEF-standalone emails, use `hbef-brand`'s Montserrat hierarchy.

## Image specs for HBEF article submissions

When HBEF submits an article with an image:
- **Format:** JPG (preferred) or PNG
- **Width:** 600px minimum (HVPTO will crop and resize)
- **Aspect ratio:** Square or 4:3 portrait work best — fits the right-column layout cleanly
- **Color:** Bright, simple compositions read best at the small rendered size
- **Watermark / branding:** HBEF logo can be embedded but don't make it the focal point
- **File naming:** Include topic — `counselor-okuda.jpg`, `strand-classic-promo.jpg`, `hoh-thanks.jpg`

## Standalone HBEF email (use case 2)

When HBEF needs to send an email outside the Surf Report cycle (e.g., an urgent Annual Giving closer, a Hearts ticket-on-sale alarm), build the email in HBEF brand using these conventions:

### Header / banner
- Use the **HBEF brand cover pattern** from `hbef-brand`:
  - HBEF_NAVY band at top with HBEF lockup centered (from `hbef-brand/assets/logos/hbef-secondary-lockup-dark.png`)
  - Eyebrow text below: `HERMOSA BEACH EDUCATION FOUNDATION · [EMAIL TOPIC]`
  - Right-aligned date

### Article blocks
- Mirror the Surf Report's left-text + right-image layout
- Article title: Montserrat 700 18pt HBEF_NAVY (uppercase optional, can be sentence-case for emails)
- Body: Montserrat 400 13pt INK
- Hyperlinks: HBEF_ORANGE underlined
- Image: right-aligned, ~30% column

### Section dividers
- Use HBEF orange or navy, not Surf Report red
- Centered, bold, uppercase, tracked

### Footer
- HBEF brand close: "Funding matters. Your donation, their future." italic navy
- "100% Volunteers | 100% Parents" tagline teal-muted bold tracked
- Address line + email + EIN
- Social icons linking to @hbef90254

### Email service
HBEF uses Givebutter for event-tied email, but for general HBEF blasts, the platform is Constant Contact (same as HVPTO) or Kindful (donation platform's built-in mailer). Match the platform's template constraints when building.

## Layout comparison cheat sheet

| Element | Surf Report (HVPTO) | Standalone HBEF email |
|---|---|---|
| Header banner | "HVS SURF REPORT" + palm illustration | HBEF lockup on navy band |
| Section dividers | Bright red, centered, uppercase | HBEF orange/navy, centered, uppercase |
| Article title color | Surf blue (`#1E5A8A`) | HBEF_NAVY (`#0B4261`) |
| Hyperlink color | Surf link blue (`#2E7AC9`) | HBEF_ORANGE (`#F79B32`) |
| Footer hashtag | `#PoweredByHVPTO` | None (use tagline instead) |
| Subject line | "HVPTO Surf Report MM.DD.YY" | "HBEF: [topic]" or event name |
| From | HVPTO Surf Report | Hermosa Beach Education Foundation |

## Constant Contact / Givebutter notes

Both platforms render emails via a templated HTML wrapper. Limits to be aware of:

- **Width:** ~600px desktop, fluid on mobile
- **Bullets:** Both render `·` and `●` correctly; avoid Unicode-rare bullets
- **Emoji:** Both render most palette emoji (📚, ❤️, ⛳, ☀️, 🚨) correctly via system fonts
- **Custom fonts:** Both fall back to web-safe — don't rely on Montserrat rendering perfectly in every email client (especially Outlook); design with the fallback in mind
- **Tables for layout:** Both use HTML tables under the hood for image-right layouts; if hand-coding HTML, use `<table>` not `<div>` for compatibility
- **Image hosting:** Upload to the platform's image host; don't link external images
- **Hyperlinks:** Use unambiguous link text — never "click here"

## HTML template (minimal)

A starter HTML scaffold for a standalone HBEF email mirroring the Surf Report layout, branded in HBEF colors, lives at `../assets/standalone-email-template.html`. Use as the starting point when HBEF needs a Surf-Report-style standalone blast.
