# Per-Entity Brand Skill Template

After the dossier is written, emit a fully populated `{slug}-brand` skill into `~/Cortana/cortana-vault/research/brand-recon/{slug}/{slug}-brand/`. This skill is the second compounding artifact — it's what makes every future deliverable for that entity stay on-brand without re-doing the research.

## Structure to emit

```
{slug}-brand/
├── SKILL.md                          ← main entry, copy from assets/brand-SKILL.skeleton.md
├── references/
│   ├── visual-tokens.md             ← from assets/visual-tokens.skeleton.md
│   ├── voice-and-tone.md            ← from assets/voice-and-tone.skeleton.md
│   ├── product-architecture.md      ← from assets/product-architecture.skeleton.md
│   ├── copy-archetypes.md           ← from assets/copy-archetypes.skeleton.md
│   └── positioning-and-claims.md    ← from assets/positioning-and-claims.skeleton.md
└── assets/
    ├── {slug}-tokens.css            ← from assets/tokens.css.skeleton
    └── {slug}-tokens.json           ← from assets/tokens.json.skeleton
```

This mirrors the CopperJoint brand skill exactly. The reference shape was vetted in the wild and produces deliverables that look like they came from the entity's own design system.

## Substitution rules

The skeletons use these placeholders. Substitute every occurrence in every file:

| Placeholder | Replace with |
|---|---|
| `{ENTITY_NAME}` | Human-readable brand name (e.g., `CopperJoint`, `Summer Fridays`) |
| `{slug}` | Kebab-case slug (e.g., `copperjoint`, `summer-fridays`) |
| `{SLUG_UPPER}` | Token prefix in uppercase for CSS vars (e.g., `CJ`, `SF`) — keep it 2–4 chars |
| `{tagline}` | The brand's own tagline if they have one, else the closest equivalent extracted from hero copy |
| `{founder_or_owner}` | Founder name + brief credential |
| `{advisor_name_credentialed}` | Named authority + full credentials |
| `{date}` | The dossier creation date in YYYY-MM-DD |

For visual tokens, replace every `#000000` / `#FFFFFF` placeholder with the entity's actual hex codes from Phase 1. For fonts, replace `Inter` (placeholder) with the actual primary font family.

## Description-field requirements

The brand skill's SKILL.md frontmatter description is the single most important field for triggering. Generic descriptions undertrigger. Follow the CopperJoint brand skill's pattern:

> [brand name] brand guide for generating consistent, on-brand documents and digital deliverables. Use this skill whenever creating Word documents (.docx), PowerPoint decks (.pptx), Excel workbooks (.xlsx), PDFs, HTML reports, web apps, charts, or any visual deliverable for [brand]. Also trigger when the user mentions [brand] branding, [signature colors], [signature fonts], [voice descriptor], or asks for a document "in the [brand] style." Trigger even when the user just says "make this on-brand," "apply the [brand] look," "use our palette," or names a [brand] product or sub-brand. This skill is the brand LAYER — it pairs with format-specific skills (pptx, docx, xlsx, pdf, canvas-design, frontend-design) which provide the file-format mechanics. Always read this SKILL.md AND the relevant format reference before generating output.

Customize the bracketed terms with the specific entity's signature colors, fonts, voice cues, and product / sub-brand names. The "pushy" qualifiers ("even when the user just says…") are deliberate — keep them.

## Validation checklist before declaring the brand skill done

1. **Self-sufficient.** A fresh agent reading only the brand skill (not the dossier) should be able to produce on-brand deliverables. The references should hold all the operational facts.
2. **Real color values.** No `#000000` placeholders. Every color is the entity's actual hex.
3. **Real font names.** No `Inter` placeholder. The actual font families.
4. **Voice with examples.** The voice-and-tone file includes real example phrases lifted from the entity's site copy, not generic platitudes.
5. **Claim discipline calibrated to the category.** Health/wellness brands need stricter claim hedging (FTC-aware) than B2B SaaS. The positioning-and-claims file should reflect this.
6. **Product architecture matches the actual catalog.** Don't carry over CopperJoint's three-line structure if the entity has one product or two lines.
7. **No CopperJoint residue.** Search the whole emitted skill for the substring `copperjoint` / `CopperJoint` — should return zero matches unless the entity literally is CopperJoint.

## Why split into so many reference files

Progressive disclosure. The brand skill's SKILL.md should be ≤200 lines so it stays cheap to load. The references load on demand based on what the agent is doing:
- Designing a deck? Load `visual-tokens.md` + `copy-archetypes.md`.
- Drafting a press release? Load `voice-and-tone.md` + `positioning-and-claims.md`.
- Building a product page? Load `product-architecture.md` + `voice-and-tone.md`.

This keeps token usage low across many deliverables and makes the brand skill genuinely useful at scale.

## After emission — register in the vault

Once the brand skill is written, append a one-line entry to `cortana-vault/index.md` under a "Brand Skills" section (create it if it doesn't exist):

```
- [[research/brand-recon/{slug}/{slug}-brand/SKILL.md|{ENTITY_NAME} Brand]]
```

This makes the skill discoverable from Obsidian's index page and surfaces it in graph view.

## Coordination with the obsidian skill

The brand skill emission counts as a vault write — the obsidian skill's conventions apply. After writing the brand skill, append a log entry to `cortana-vault/log.md`:

```
## [YYYY-MM-DD] brand-recon | {ENTITY_NAME} brand skill emitted

- **type**: brand-skill-emission
- **source**: brand-recon Phase 13
- **details**: Emitted {slug}-brand skill into research/brand-recon/{slug}/{slug}-brand/. Sibling to dossier.
- **pages touched**: [[research/brand-recon/{slug}/dossier.md]], [[research/brand-recon/{slug}/{slug}-brand/SKILL.md]]
```
