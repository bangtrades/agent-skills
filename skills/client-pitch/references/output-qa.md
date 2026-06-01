# Client Pitch Output QA

## Required Files

Final package should include:
- `.pptx` editable deck
- `.pdf` generated from the final rendered deck
- rendered slide previews or a contact sheet in the working directory

Use client-specific filenames:
- `<Client>_Agent_Director_Pitch.pptx`
- `<Client>_Agent_Director_Pitch.pdf`

If the user requested another title, use it.

## PPTX QA

Verify:
- PPTX archive integrity: `unzip -t <deck.pptx>`
- expected slide count
- no stale requested phrases after edits
- no obvious rendered text collisions in previews
- title and footer numbering align after inserted/deleted slides

When using the Presentations skill, run the layout checker. Some text-image overlap warnings are acceptable only when text intentionally overlays a full-slide background image and the rendered preview is readable.

## PDF QA

The PDF must be visually identical to the final deck render.

Preferred methods:
1. Export directly from the final PPTX if a trustworthy renderer is available.
2. Otherwise, create the PDF from the final slide preview PNGs used for contact-sheet QA.

Verify:
- page count equals PPTX slide count
- every page has 16:9 dimensions
- PDF timestamp is newer than final deck rebuild

When the PDF is assembled from preview PNGs, mention that it is visually matched/rasterized rather than editable text.

## Final Response

Keep the handoff short:
- link PPTX
- link PDF
- list key verification checks
- mention any material caveat, such as intentional image-overlay layout warnings or rasterized PDF output
