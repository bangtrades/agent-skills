# Nova SwiftUI Design Patterns

## Scene Composition

Use 2.5D scene assets as atmosphere and SwiftUI overlays for interaction.

Good:

- Full classroom background image.
- Transparent tappable hotspot overlays.
- Dynamic labels rendered in SwiftUI.
- Separate interactive state assets for buttons, tiles, page turns, and rewards.

Avoid:

- Floating rounded rectangles over a blank background.
- In-app paragraphs explaining what to do.
- Text baked into generated art.
- Large panels that look like web dashboards.

## Home

Home should feel like the child is seated at a desk looking at the room.

Object positions:

- Chalkboard centered and dominant.
- Trophy case hanging on the wall.
- Bookshelf standing on the floor.
- Mission board as a smaller classroom board.
- Dashy's desk low/foreground.

## Lesson Reader

Lessons should feel like a workbook or picture book on the desk.

Required patterns:

- A large, persistent read-aloud control.
- Page turn controls that feel like paper/book controls.
- Story pages as picture-book pages.
- Concept pages as chalk diagrams or classroom explainers.
- Quiz pages as magnetic tiles or sticky notes.
- Experiment pages as tabletop manipulatives.
- Voice pages as a microphone/listening object.

## Touch and Accessibility

- Primary child controls should be at least 64 pt, ideally 88 pt or larger.
- Use VoiceOver labels for every classroom object and stateful control.
- Respect Reduce Motion; pulse/float effects must have static alternatives.
- Do not rely on color alone for correct/incorrect states.
- Make the audio path obvious; pre-readers should not need to decode a small icon.

## Component Tone

Prefer:

- chalkboards;
- books;
- shelves;
- wood frames;
- sticky notes;
- magnets;
- sticker badges;
- workbook pages;
- classroom signs.

Avoid:

- generic cards;
- glassmorphism;
- abstract gradients;
- marketing hero sections;
- thin desktop-style controls;
- small icon-only controls for core child actions.
