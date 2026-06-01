# Novai Audio Reference

## Current Audio Stack

- `SpeechSynthesizer` in `NovaVoice` wraps `AVSpeechSynthesizer`.
- `VoiceManager` routes speech:
  - remote TTS through backend when configured;
  - local AVSpeech fallback when remote fails or when `preferLocal: true`.
- `DashyHintSheet` uses direct local `SpeechSynthesizer`, which is why help notes can work even when lesson TTS fails.
- Lesson card views historically used `VoiceManager` and swallowed errors with `try?`, creating silent audio failures.

## Beta Lesson Read-Aloud Rule

Lesson page audio should be local-first until the backend TTS proxy, auth token path, and simulator playback path are verified end-to-end.

Preferred call for beta lesson page narration:

```swift
try await voiceManager.speak(text: text, preferLocal: true)
```

Remote voices can be used for Dashy chat and future premium narration after reliability is proven.

## UX Contract for Children

- Every lesson page needs a primary, obvious audio affordance.
- The button should be large enough for a 4-year-old and visible at the workbook shell level.
- Tapping once reads the page.
- Tapping while reading stops the audio.
- Turning pages stops the current page audio.
- If no text is available, show a friendly unavailable state rather than doing nothing.

## Text Fallback Order

Generated cards are inconsistent. Use a centralized fallback resolver instead of each view guessing.

Recommended order:

- Story: `voiceScript`, `narrativeText`, `bodyText`, `title`
- Concept: `voiceScript`, `explanation`, `bodyText`, `title`
- Quiz: `voiceScript`, then question plus options, then `bodyText`, `title`
- Experiment: `voiceScript`, `instructions`, `bodyText`, `title`
- Voice: `voiceScript`, `promptText`, `bodyText`, `title`
- Video: `voiceScript`, `bodyText`, `title`

## Common Failure Modes

- Remote TTS or auth fails but view swallows the error with `try?`.
- Button state flips back to idle before AVSpeech finishes.
- New audio helper file is not registered in `project.pbxproj`.
- Multiple synthesizers fight over the audio session.
- Page changes leave old narration playing.
