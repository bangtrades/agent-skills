---
name: brand-waive
description: >-
  WaiveLabs brand guide for consistent, on-brand deliverables in every format. Use whenever creating
  any WaiveLabs-branded output — Word docs (.docx), decks (.pptx), Excel (.xlsx), PDFs, HTML/web,
  marketing-site work, insights articles, proposals, pitch decks, reports, one-pagers, email, or
  social. Also trigger on mentions of WaiveLabs branding, the Dawn/Dusk theme, dusk slate #161B26,
  Ocean Blue / Sunset Orange palette, Sora/Inter/Fraunces type, the sunrise-over-circuit mark, "ride
  the AI wave," or requests to make something "on-brand," "in the WaiveLabs style," "use our
  palette/logo," or naming a WaiveLabs surface (The Lab, WaiveBoard, Build-your-Agent-OS configurator,
  /for pages, /insights). This is the brand LAYER — it pairs with the format skills (pptx, docx, xlsx,
  pdf, frontend-design, canvas-design, client-pitch) that supply file mechanics. Always read this
  SKILL.md plus the relevant references/ file before generating output.
---

# WaiveLabs — Brand Skill (`brand-waive`)

> The single operating brand layer for **WaiveLabs.ai** — an agentic-AI consultancy that turns an
> AI-beginner small business into an AI power user in 90 days. Everything that ships under the
> WaiveLabs name pulls its colors, type, logo rules, voice, and build specs from here.

## How to use this skill

1. **Read this SKILL.md first** (the at-a-glance brand core below).
2. **Read the matching `references/` file** for the format you're producing:
   - Web / HTML / site / article / landing page → `references/web-build.md`
   - Any color question, dark mode, color-blind profile → `references/palette.md`
   - Type scale, font loading, headline hierarchy → `references/typography.md`
   - Copy, slogans, naming, voice, do/don't → `references/voice.md`
   - Logo files, lockups, clear space, usage rules → `references/logos.md`
   - Pitch deck / sales deck / proposal deck (.pptx) → `references/deck.md`
   - Reports, letters, memos, SOWs, one-pagers (.docx/.pdf) → `references/documents.md`
   - Spreadsheets, models, dashboards (.xlsx) → `references/spreadsheet.md`
3. **Read the format skill too.** This skill is the brand LAYER. It does NOT replace `pptx`,
   `docx`, `xlsx`, `pdf`, `frontend-design`, or `canvas-design` — it tells those skills what to
   make it look like. Read both: this for the *look*, the format skill for the *mechanics*.
4. **Bundled logos** live in `assets/` of this skill — use them directly; never rebuild the
   wordmark in another typeface.

## The brand in one breath

**Positioning:** A new tech wave is coming; WaiveLabs helps small businesses learn to ride it —
agentic workflows, real results, and *graduation* (you leave an AI power user, not a dependent).

**Tagline:** *Ride the AI wave.*
**Offer line:** *In 90 days, we turn your scattered business data into one organized brain, build
the apps and AI agents that run on it, and teach your team to keep building.*
**Dependency chain (sacred):** Data → Visibility → Agents → Apps/Autonomy → Graduation.

**The mark:** a **sunrise** (orange rays) cresting **blue waves that dissolve into a circuit /
data-flow pattern**. Coastal South Bay dawn + the incoming AI wave + agentic data plumbing, in one
glyph. Wordmark: `WaiveLabs` in near-black with `.ai` in sunset orange. **Canonical spelling has the
*i* in Wa·i·ve — always verify before shipping (an early export read "WaveLabs").**

**Theme system — "Dawn / Dusk":** light mode is *dawn* (warm cream → cool morning blue); dark mode
is *dusk* (the same world after sunset, on a slate base `#161B26`). Both ship on the live site;
every deliverable should respect whichever is appropriate to its surface.

## Color core (full system in `references/palette.md`)

```
PRIMARY   Ocean Blue     --blue        #3179F5   waves · links · primary buttons · the workhorse
DEEP      Deep Blue      --blue-deep   #0D43AA   gradients, pressed states, headings on light
ACCENT    Sunset Orange  --orange      #E65100   the SPARK — sun, ".ai", single CTAs (use sparingly)
SUN       Bright Sun     --sun         #FF7A1A   gradient stops, hero sun, warm glows
AMBER     Amber          --amber       #FFB454   tertiary warm accent, dark-mode link/orange swap
INK       Near Black     --ink         #0F172A   body text + wordmark (slate-900)
DAWN-1    Cream          --dawn-1      #FFF8F1   warm page base (light)
DAWN-2    Morning Blue   --dawn-2      #F4F7FD   cool section fills (light)
DEEP/NAVY Footer Navy    --deep        #0C1428   footer + darkest anchor (both themes)
DUSK      Dusk Slate     --bg          #161B26   dark-mode page base (hue 222° / S27%)
GOOD/WARN/BAD            green/amber/red #16A34A / #D9870B / #DC2626
```

Discipline: **blue is the workhorse, orange is the spark.** Keep orange high-signal — the sun, the
`.ai`, one CTA per view. Never flood a layout with orange.

## Type core (full scale in `references/typography.md`)

- **Sora** (500–800) — headings, hero lines, deck titles, UI labels. The *promise*.
- **Inter** (400–700) — body, captions, all numerals + data. The *proof*.
- **Fraunces** (italic, optical) — ONE characterful editorial accent (a single hero word, an "AI
  brief" headline). Seasoning, never the meal. Never set body copy in Sora or Fraunces.

All three are free Google Fonts — zero licensing friction for web or client deliverables.

## Voice core (full guide in `references/voice.md`)

Practical · Coastal · Modern · Trustworthy · Forward-looking. Write like a knowledgeable local
who's done the work: plain words over jargon, outcomes over features, "we'll show you" over "we'll
do it for you." Confident, never hypey. No slop. The surf metaphor is seasoning. Concrete numbers
beat adjectives. End persuasive pieces on a question, not a pitch.

## Hard rules (violate none)

- Spelling is **WaiveLabs.ai** — verify the *i*.
- **No pricing on public marketing surfaces** (programs shown as tiers, no dollar figures).
- **Email CTAs, not calendar booking** (`mailto:hello@waivelabs.ai`) — the operator finds calendars
  impersonal.
- **Security-first**: never put secrets client-side; demo data is always fictional and badged
  "sample data"; honor the security baseline on anything touching real data.
- **Honesty**: never claim a certification, partnership, or result WaiveLabs doesn't hold.
- Orange stays sparing. Logos stay transparent-background. Never recolor or restretch the mark.
