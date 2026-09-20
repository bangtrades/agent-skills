# Visual Tokens

## Visual thesis

James & Gable should look like a steady healthcare risk advisor: institutional without feeling bureaucratic, clinical without looking like a hospital system, and connected to Trucordia without losing the legacy specialist name. The current site’s strongest signals are deep blue fields, white space, serif authority headings, geometric sans-serif body text, and healthcare photography.

## Color system

| Token | Value | Role |
|---|---:|---|
| J&G blue | `#00539F` | Primary fields, key headings, links, high-emphasis actions |
| J&G blue dark | `#003D76` | Accessible hover/pressed state, deep text accent |
| Light blue | `#BADEFF` | Soft panels, hover cue, diagrams, supporting data fills |
| Muted olive gray | `#A5AA8F` | Observed border/detail color; use sparingly |
| UI gray | `#6C757D` | Secondary metadata and inactive controls |
| Ink | `#000000` | Primary copy |
| White | `#FFFFFF` | Canvas and reversed copy |
| Error | `#A33A3A` | Validation only; never a brand accent |

Use J&G blue as the recognizable anchor. Do not introduce bright healthcare teal or gradients as a substitute. Light blue works best as a quiet evidence or explainer surface, not as a dominant field.

## Typography

- **Display:** Merriweather, 900. Use for H1–H3, major numbers, and short editorial statements.
- **Body/UI:** Montserrat, 400 and 700. Use for paragraphs, navigation, labels, buttons, and tables.
- **Fallbacks:** Georgia for display; Arial or system sans-serif for body.
- **Observed scale:** approximately 36px for H1/H2 and major hero copy; approximately 20px for body copy.
- **Recommended responsive scale:** H1 `clamp(2.25rem, 4vw, 3.75rem)`; H2 `clamp(1.875rem, 3vw, 2.75rem)`; body `1.125rem–1.25rem`; small copy `0.875rem–1rem`.

Keep headings short. Merriweather becomes heavy in dense blocks. Use Montserrat for all technical detail and tables.

## Spacing and geometry

- Base unit: `4px`.
- Standard content rhythm: `8 / 12 / 16 / 24 / 32 / 48 / 64 / 96px`.
- Content maximum: `1180px`; long-form reading width: `720px`.
- Standard radius: `4px`.
- Pill CTA radius: `18.5px` only for compact contact actions, matching the observed email treatment.
- Borders: `1px solid #A5AA8F` or a low-opacity J&G blue.
- Shadows: minimal. Prefer separation through white space, border, and color field.

## Layout grammar

1. White navigation with the combined James & Gable / Trucordia mark.
2. One decisive healthcare image or evidence graphic in the hero.
3. Large blue section fields for positioning and major transitions.
4. Alternating white evidence sections with generous margins.
5. Clear service pathways grouped by client decision, not a wall of coverage names.
6. A restrained contact band that identifies the licensed-human next step.

Use asymmetry and data artifacts to modernize the existing centered brochure layout, while keeping the overall composition calm.

## Photography and graphics

Prefer:

- real healthcare environments and operational moments;
- clinicians, risk leaders, facilities, and teams shown with dignity;
- detail crops that imply systems, coordination, and care;
- approved charts, renewal timelines, risk maps, and anonymized case-study diagrams.

Avoid:

- generic handshakes, staged call-center smiles, fear imagery, surgical gore, and crisis spectacle;
- client logos without permission;
- visuals that imply a particular patient, claim, diagnosis, or protected health information;
- decorative AI imagery.

Blue overlays may be used when they improve text contrast, but should not erase the specificity of the image.

## Logo handling

The observed lockup pairs the James & Gable wordmark with Trucordia. Preserve its proportions and clear space. Do not reconstruct, recolor, separate, or imply endorsement by extracting only one mark unless current brand governance explicitly permits it. On first-touch pages, add copy that explains the relationship rather than asking the logo alone to do that work.

## Accessibility

- Use dark J&G blue `#003D76` for small links or hover states when contrast requires it.
- Maintain at least WCAG AA contrast for text and controls.
- Never place body text over unquiet photography without a solid or sufficiently opaque overlay.
- Do not encode risk status through color alone.
- Tables and charts require text labels, source dates, and accessible summaries.

