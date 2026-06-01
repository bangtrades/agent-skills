# Nova Asset Workflow

## Asset Location

Store app assets in:

```text
/Users/nolan/Projects/Novai/src/Apps/NovaKids/Resources/Assets.xcassets
```

Use lowercase snake_case asset names.

## Generation Rules

- Generate isolated objects on pure white backgrounds if the background will be removed.
- Export cleaned alpha PNGs before importing to Xcode.
- Do not bake readable text into images.
- Keep tappable zones visually obvious and physically separated.
- Generate landscape first for iPad. Add portrait only when the screen needs it.
- Use full scene assets for atmosphere; split assets for interactive/animated parts.

## Current Canonical Asset Naming Families

Home/classroom:

- `classroom_home_45_landscape`
- `classroom_home_45_portrait`
- `classroom_home_67_landscape`
- `classroom_home_67_portrait`

Lesson/workbook:

- `lesson_workbook_45_landscape`
- `lesson_desktop_45_landscape`
- `lesson_storybook_frame_45_landscape`
- `lesson_storybook_page_45_landscape`
- `lesson_answer_tiles_45_landscape`
- `lesson_experiment_table_45_landscape`
- `lesson_voice_prompt_45`
- `lesson_read_aloud_45`
- `lesson_hint_note_45`
- `lesson_page_turn_45`
- `lesson_progress_dots_45`

## Prompt Prefix

Use this direction for new assets:

```text
Bright kid-safe educational iPad app asset, warm 2.5D classroom illustration style, saturated but controlled colors, clean focal point, deep navy outline accents, soft painterly texture, friendly for children ages 4-5, no brand/IP references, no readable text baked into image, pure white background for alpha matte cleanup.
```

For scene backgrounds, replace pure white background with:

```text
iPad landscape classroom scene, child seated perspective looking forward from a desk, clear tappable object zones, no readable text baked into image.
```

## Import Checklist

1. Clean alpha matte outside the repo if needed.
2. Place PNG in the matching `.imageset`.
3. Verify `Contents.json`.
4. Build NovaKids.
5. Check iPad landscape first, then portrait if relevant.
6. Do not delete old working assets until the replacement is visible in simulator.
