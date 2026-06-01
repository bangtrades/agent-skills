# Novai Architecture Reference

## Apps

- `NovaKids`: iPad-first child app. Current v2 work targets this app first.
- `NovaCompanion`: parent app for URL intake, review, and progress. Do not prioritize unless requested.

## Packages

- `NovaCore`: shared models, API router/client, sync model types.
- `NovaVoice`: `SpeechSynthesizer`, `VoiceManager`, remote TTS client, speech recognition support.
- `NovaAuth`: auth, OAuth, token flows.
- `NovaStorage`: Core Data and local persistence.

## NovaKids Major Areas

- App setup: `src/Apps/NovaKids/Sources/App/NovaKidsApp.swift`
- Home/classroom: `src/Apps/NovaKids/Sources/Views/Home`, `src/Apps/NovaKids/Sources/Views/Classroom`
- Lessons/workbook: `src/Apps/NovaKids/Sources/Views/Flipbook`
- Lesson data: `src/Apps/NovaKids/Sources/ViewModels/FlipbookViewModel.swift`
- Trophies: `src/Apps/NovaKids/Sources/Views/Trophies`, `TrophyRoomViewModel.swift`
- Dashy: `src/Apps/NovaKids/Sources/Views/Dashy`, `DashyViewModel.swift`
- Shared classroom components: `Views/Common`, `NovaPalette.swift`

## Nova v2 Product Rules

- Nova is not a dashboard. Nova is a classroom that rearranges itself around the child.
- Home navigation should be object-based: chalkboard, bookshelf, trophy case, desk, mission board.
- Lessons should feel like a workbook or book on the child's desk, not floating cards.
- Dashy is a persistent guide/teacher, not just a tab.
- Parent-generated content should become classroom objects and books.
- Age progression:
  - 4-5: warm classroom.
  - 6-7: maker lab.
  - 8+: AI studio.

## Beta Reliability Rules

- Child-critical flows need local fallback states: lesson read-aloud, loading, trophies, navigation.
- Empty backend responses should not blank key screens.
- A crashed child app is worse than a degraded classroom fallback.
- Prefer visible kid-safe fallback UI over silent no-op behavior.
