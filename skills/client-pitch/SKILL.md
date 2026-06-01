---
name: client-pitch
description: Create client-specific AI/agentic transformation pitch packages with branded PowerPoint and matching PDF outputs. Use when Codex is asked to make a client pitch deck, consulting proposal deck, AI Director/Agent Director proposal, agentic AI roadmap, executive AI transformation narrative, or repeatable PPTX/PDF sales package that should pair with a separate client brand skill.
---

# Client Pitch

## Overview

Create a concise executive pitch package: an editable `.pptx` and a visually matching `.pdf`. The deck uses a repeatable agentic-AI transformation narrative, but the design, vocabulary, examples, and proof objects must be adapted to the client’s brand skill.

This skill is a workflow layer. Pair it with:
- The relevant client brand skill, such as `$sf-brand`, for palette, typography, voice, and layout cues.
- The `Presentations` skill for PPTX construction and preview/contact-sheet QA.
- The `imagegen` skill when the deck needs custom bitmap visuals.

## Required References

Read only what is needed:
- `references/narrative-spine.md` before writing the slide outline.
- `references/visual-system.md` before generating images or diagrams.
- `references/output-qa.md` before final export.

Use `assets/deck-manifest-template.json` as a copyable planning scaffold when building a substantial deck.

## Output Contract

Produce:
1. A branded, editable PowerPoint deck with a specific filename, not `deck.pptx`.
2. A PDF generated from the final rendered deck so it visually matches the PPTX.
3. Preview renders or a contact sheet for QA.
4. A short final note with file links and verification results.

Default to 8-9 slides unless the user asks for a different length. Keep slides talk-track friendly: strong visual structure, short claims, minimal body copy.

## Workflow

1. **Load the brand layer.** Read the client-specific brand skill first. If no brand skill is provided, ask for the brand source or use a lightweight visual direction only after saying the brand layer is missing.
2. **Extract the pitch context.** Identify the client, audience, desired role/offer, current operating pain, proposed AI stack, and the most relevant agent use cases.
3. **Lock the narrative.** Use the slide spine in `references/narrative-spine.md`. Keep the story consistent; localize examples and terminology to the client.
4. **Plan the contact sheet.** Vary macro layouts. Avoid repeated title + card-grid cadence. The deck should read as authored at thumbnail size.
5. **Generate visuals.** Use imagegen for text-free editorial visuals, then overlay labels in editable PowerPoint text. Do not rely on generated text inside images.
6. **Build the PPTX.** Prefer artifact-tool presentation JSX through the `Presentations` skill. Keep text and diagrams editable wherever possible.
7. **Export the PDF.** Use the final PPTX renderer or final slide preview PNGs. The PDF must be page-for-page identical in visual appearance.
8. **QA before delivery.** Run archive integrity checks, page/slide count checks, rendered preview review, and phrase checks for known requested replacements.

## Hard Rules

- Pair with the client brand skill; do not reuse Summer Fridays styling unless Summer Fridays is the client.
- Keep wording concise. The presenter should talk over the deck.
- Use client-specific workflows, systems, channels, and commercial examples.
- Do not invent official logos, partner marks, or brand assets.
- Keep generated visuals free of readable text; all meaningful text belongs in editable slide objects.
- Include a build scenarios slide when pitching retained AI/agentic consulting, especially when the ask involves ongoing ownership or handoff.
- If a prior deck exists, update the editable source first, then rebuild both PPTX and PDF from the same final render path.
