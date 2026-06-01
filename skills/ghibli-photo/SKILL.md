---
name: ghibli-photo
description: Transform real photos into cohesive, warm, hand-painted storybook illustrations inspired by classic Japanese animated-film aesthetics while preserving the source image's identity, composition, people, clothing, signage, logos, numbers, setting, and emotional tone. Use this skill for photo-to-illustration workflows, storybook image series, travel scenes, family or friends memories, sports tournament scenes, city scenes, restaurant scenes, landmarks, and image prompts that ask for warm watercolor anime storybook styling with high source fidelity.
---

# Ghibli-Photo Skill

## Purpose

Transform real photos into cohesive, warm, hand-painted storybook illustrations inspired by classic Japanese animated-film aesthetics, while preserving the source image's identity, composition, and key visual facts.

This skill is designed for photo-to-illustration workflows where the output should feel like a polished page from a travel, family, sports, school, adventure, or memory book.

## Core Objective

Create an image that feels:

- Hand-painted
- Warm and nostalgic
- Cinematic but gentle
- Whimsical without becoming fantasy unless requested
- Faithful to the source photo
- Cohesive across a multi-image storybook series

The result should enhance the original scene, not replace it.

## Default Visual Style

Use a soft watercolor / painterly anime storybook style:

- Warm golden light
- Soft atmospheric shading
- Gentle outlines
- Expressive but natural faces
- Painterly texture
- Slightly idealized environment
- Cozy cinematic framing
- Clear emotional storytelling
- Rich background detail without clutter

Avoid harsh photorealism, plastic 3D rendering, overly glossy surfaces, or generic cartoon simplification.

## Source Fidelity Rules

Always preserve the source image's core facts.

### Must Preserve

- Number of people
- Approximate ages
- Relative positions
- Main poses and body language
- Clothing colors and major outfit details
- Hairstyles and visible accessories
- Important objects, bags, props, vehicles, signs, buildings, scenery
- General setting and location cues
- Emotional tone of the moment

### Do Not Alter

If the source image contains recognizable text, signage, logos, brands, team marks, jersey numbers, bag designs, or words:

- Preserve spelling exactly
- Preserve the design intent
- Preserve relative placement
- Preserve important typography hierarchy when possible
- Do not invent alternate brand names
- Do not "correct" signs unless explicitly instructed

If exact rendering is difficult, simplify only slightly while keeping it recognizable and readable.

## Creative Enhancement Rules

The agent may add tasteful accents that improve storytelling, atmosphere, and beauty.

Good additions include:

- Warm sunlight
- Soft sky/clouds
- Reflections on floors or windows
- Small travel tags
- Sports-related details
- Environmental posters
- Subtle local scenery
- Cozy background characters
- Flowers, plants, street details, lights
- Slightly more cinematic framing
- Small visual motifs that connect the story

Do not add distracting fantasy creatures, random characters, incorrect locations, unrelated props, or visual jokes unless requested.

The enhancement should feel like the scene was lovingly illustrated, not rewritten.

## Series Consistency

When creating multiple images for a storybook, maintain visual continuity:

- Same watercolor/anime storybook rendering style
- Similar line weight
- Similar warmth and lighting philosophy
- Similar face stylization
- Similar color grading
- Similar level of background detail
- Similar texture and brushwork
- Same aspect ratio unless the user asks otherwise

When prior generated images are available, use them as style anchors.

## Prompt Construction Pattern

Use this structure when prompting an image model.

```text
Create a hand-painted anime storybook illustration based on the provided photo.

The photo is the source reference. Preserve the number of people, their approximate ages, relative positions, clothing colors, hairstyles, poses, key objects, signage, logos, and the main setting. Keep all visible words, brands, signs, and numbers spelled and designed as close to the source as possible.

Render the scene in a warm watercolor / Ghibli-inspired storybook aesthetic with soft outlines, gentle painterly texture, expressive natural faces, warm cinematic light, and charming environmental detail.

Enhance the scene creatively but faithfully: add tasteful accents that support the story, atmosphere, and location, while keeping the core visual elements distinguishable. Do not replace the original moment or change the meaning of the scene.

The final image should feel like a polished page from a cohesive illustrated storybook.

End
```

## Context-Specific Additions

These are context-specific descriptions a user may choose to provide.

### Travel Scene

Add subtle travel-story details:

Include small travel accents such as luggage tags, airport signage, route hints, boarding-pass details, destination cues, reflections, and soft terminal lighting.

### Sports Tournament Scene

Add subtle sports-story details:

Include tasteful tournament cues such as team backpacks, water bottles, volleyball gear, athletic clothing, or small event details, without overcrowding the scene.

### City / Restaurant / Landmark Scene

Preserve the landmark or sign:

Keep the building, mural, sign, logo, and visible text recognizable and correctly spelled. Enhance the street scene with warm sunlight, plants, reflections, or subtle local atmosphere.

### Family / Friends Memory Scene

Focus on connection:

Emphasize friendship, warmth, body language, and shared adventure. Keep faces expressive, wholesome, and natural.
