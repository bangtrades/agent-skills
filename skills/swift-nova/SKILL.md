---
name: swift-nova
description: This skill should be used when the user asks to work on the Novai, NovaKids, NovaCompanion, or Nova v2 classroom Swift/iPad app; asks for Novai agent coding prompts or slice reports; mentions Dashy, classroom UI, workbook lessons, lesson audio, trophies, or the Novai Xcode workspace.
version: 0.1.0
---

# Swift Nova

Project-specific execution guide for Novai Swift work. Use this with `senior-swift`; this skill supplies local product, repo, build, and workflow knowledge, while `senior-swift` supplies general Swift/SwiftUI correctness.

## Required Startup

1. Work only in `/Users/nolan/Projects/Novai` unless the task explicitly targets the Cortana vault or Codex skills.
2. Never touch `/Users/Nolan/Documents`.
3. Check `git status --short` before edits. Preserve unrelated dirty worktree changes.
4. Load only the reference needed for the task:
   - `references/build-and-test.md` for build, simulator, backend, and Xcode project membership.
   - `references/architecture.md` for app/package layout and product-specific runtime systems.
   - `references/audio.md` for lesson audio, Dashy narration, TTS, and speech bugs.
   - `references/slice-reporting.md` for Claude/Codex agent slice files.

## Default Build Command

Run this after Swift changes unless the user explicitly asks not to:

```bash
xcodebuild -workspace src/Nova.xcworkspace -scheme NovaKids -destination 'generic/platform=iOS Simulator' build CODE_SIGNING_ALLOWED=NO
```

Run `git diff --check` before or with the build.

## Project Ground Truth

- `NovaKids` is the current priority: iPad-first kids app, not Companion.
- Nova v2 baseline is an immersive 2.5D classroom, not a generic dashboard.
- The home classroom is the quality bar. Lesson reader, trophies, onboarding, loading/error, and Dashy surfaces should move toward the same standard.
- First implementation target is SwiftUI 2D/2.5D illustrated scenes, not SceneKit/RealityKit.

## Coding Rules

- Prefer established Novai files and patterns over new architectural inventions.
- Add new Swift files only when they reduce real coupling; register them in `src/Nova.xcodeproj/project.pbxproj` if Xcode does not pick them up automatically.
- Do not silently swallow user-visible failures in kid flows. Surface safe fallback states.
- Use local-first fallbacks for beta-critical child flows when backend/auth/TTS reliability is uncertain.
- Avoid force unwraps, `fatalError`, and crash-only fallback paths in beta code.
- Keep accessibility child-first: large touch targets, VoiceOver labels, reduced-motion handling, pre-reader affordances.

## When Assigning Agents

Always tell agents which skill to use. For Novai Swift implementation prompts, use `swift-nova` plus `senior-swift`; add `nova-design` when UI/UX or art direction is involved. Require a slice report in the Cortana vault for every assignment.
