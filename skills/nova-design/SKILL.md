---
name: nova-design
description: This skill should be used when the user asks for Novai or NovaKids design, classroom UI, 2.5D art direction, asset prompts, SwiftUI UI polish, kid UX, Dashy branding, workbook lesson screens, trophy screens, onboarding visuals, or beta visual readiness.
version: 0.1.0
---

# Nova Design

Product and UI direction for Nova Kids v2. Use this with `ui-design-system` for design systems and with `swift-nova` plus `senior-swift` when implementing SwiftUI.

## Required Startup

1. Treat the NovaKids home classroom as the quality benchmark.
2. Load only the reference needed:
   - `references/brand-and-product.md` for thesis, audience, age progression, and design principles.
   - `references/swiftui-patterns.md` for implementation patterns and anti-patterns.
   - `references/assets.md` for asset naming, generation, and import workflow.
   - `references/beta-readiness.md` for page-by-page beta quality criteria.
3. Keep designs child-first for ages 4-8, with ages 4-5 as the first beta target.

## Product Thesis

Nova is not a dashboard. Nova is a classroom that rearranges itself around the child.

The interface should feel like a child is sitting at a desk, looking forward into a classroom. Lessons, trophies, books, hints, and audio controls should appear as familiar classroom objects, not abstract app cards.

## Visual Direction

- Saturated but controlled classroom palette.
- Chalkboard green is an anchor, not the whole theme.
- Warm wood, paper cream, sky blue, schoolhouse red, sunny yellow, deep ink navy, and leaf green should balance the scene.
- Favor 2.5D illustrated scenes and objects over flat SwiftUI containers.
- Use SwiftUI for live text, state, hit targets, accessibility, and dynamic data.
- Use generated bitmap assets for atmosphere, physical materials, and emotional appeal.

## Non-Negotiables

- Do not copy ABCmouse. Nova's differentiator is an AI classroom that changes when parents add content and when the child grows.
- Do not build floating dashboard panels and call them classroom objects.
- Do not bake readable text into images.
- Do not use generic cards where a book, chalkboard, shelf, desk, sticky note, tile, trophy case, or workbook page would be more understandable to a child.
- Do not ship beta surfaces that a 4-year-old can only use by reading instructions.
