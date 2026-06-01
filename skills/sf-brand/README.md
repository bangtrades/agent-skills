# sf-brand — Summer Fridays brand skill

A custom skill for producing on-brand documents, decks, spreadsheets, and PDFs for the Summer Fridays project.

## Contents

```
sf-brand/
├── SKILL.md                            # Master skill — colors, fonts, voice, routing
├── README.md                           # This file
├── references/
│   ├── colors-and-fonts.md             # Full long-form palette + type reference
│   ├── docx-instructions.md            # Word document brand patterns (pairs with `docx` skill)
│   ├── pptx-instructions.md            # PowerPoint deck brand patterns (pairs with `pptx` skill)
│   ├── xlsx-instructions.md            # Excel workbook brand patterns (pairs with `xlsx` skill)
│   └── pdf-instructions.md             # PDF brand patterns (HTML+WeasyPrint route preferred)
├── assets/
│   ├── brand-tokens.json               # Machine-readable token file for scripts
│   ├── brand-palette.css               # Drop-in CSS variables + utility classes
│   └── color-swatches.html             # Visual palette reference — open in browser
└── examples/
    └── example-deliverable-types.md    # The 6 canonical SF deliverable types
```

## What this skill does

- Provides the **brand layer** for any deliverable in the Summer Fridays project
- Pairs with the existing format skills (`docx`, `pptx`, `xlsx`, `pdf`, `canvas-design`, `frontend-design`, `epic-design`)
- Loads brand tokens (every color, every font, every voice rule) so any subsequent deliverable Claude produces is consistent
- Triggers aggressively on any SF-project deliverable language

## Triggering

The skill auto-triggers when the user mentions:
- Summer Fridays branding, SF brand styling
- Any sanctioned color name (Jet Lag blue, Morning Sky, Chalk, Vanilla, Pink Sugar, Hot Cocoa, etc.)
- A request to produce a PDF, Word doc, Excel, or PowerPoint inside the SF project
- Phrases like "make it on-brand," "apply the SF look," "use our palette"

## How to install (manual, current method)

This skill lives in the SF project folder so it's version-controlled with the project. To make it available to Claude across all sessions:

**Option A — Symlink into Claude's plugin skills directory:**

```bash
ln -s "/Users/nolan/Projects/Summer Fridays/skills/sf-brand" \
      "/var/folders/30/8pm8ptj55qd3njppvd_cbvw00000gn/T/claude-hostloop-plugins/8a9cdc36de4afb03/skills/user/sf-brand"
```

(Caveat: the Claude plugin path is a temp folder and may rotate. Re-symlink if it disappears.)

**Option B — Copy into a stable user skills location** (if Claude.ai/Cowork ever supports a stable user-skills directory in the future, copy the folder there).

**Option C — Reference inline** (most reliable today): At the start of any SF-project session, tell Claude: *"Use the SF-Brand skill at `/Users/nolan/Projects/Summer Fridays/skills/sf-brand/SKILL.md` for all deliverables in this session."* Claude will then `Read` the SKILL.md and the relevant reference files as needed.

## Usage example

```
User: "Build me a PDF one-pager on the H1 IG reformat plan."

Claude:
  1. Reads /Users/nolan/Projects/Summer Fridays/skills/sf-brand/SKILL.md (brand layer)
  2. Reads /Users/nolan/Projects/Summer Fridays/skills/sf-brand/references/pdf-instructions.md (format-specific patterns)
  3. Reads the `pdf` skill (file-construction mechanics)
  4. Reads the source brief at /Users/nolan/Projects/Summer Fridays/00_context/SF_brand_intelligence_2026-05-17.md
  5. Produces /Users/nolan/Projects/Summer Fridays/H1_IG_reformat_plan_2026-05-17.pdf
  6. Surfaces via present_files
```

## Calibration notes

The neutral palette (INK / CHALK / MORNING_SKY / CLAY) is calibrated from observable site rendering — the actual hex values are server-injected via Shopify's `settings_data.json` which isn't public. If you ever get first-party brand assets from Summer Fridays themselves (a brand book, a Figma library, or the official theme settings), update the four neutrals in:

1. `SKILL.md` → Brand Color Palette section
2. `references/colors-and-fonts.md` → Brand neutrals section
3. `assets/brand-tokens.json` → colors.neutrals + colors.brand_accents
4. `assets/brand-palette.css` → :root variables
5. `assets/color-swatches.html` → swatch styles (they reference brand-palette.css)

The **product-shade palette** (Pink Sugar, Hot Cocoa, etc.) is extracted directly from the live site CSS and is exact.

The **typography** (Futura PT confirmed via Adobe Typekit kit `ljq5ufs`) is exact.

## Version history

- **v1.0 — 2026-05-17** — Initial build. Calibrated from summerfridays.com theme version 450.
