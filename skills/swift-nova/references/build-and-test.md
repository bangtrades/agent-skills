# Novai Build and Test Reference

## Paths

- Repo: `/Users/nolan/Projects/Novai`
- Workspace: `/Users/nolan/Projects/Novai/src/Nova.xcworkspace`
- Xcode project: `/Users/nolan/Projects/Novai/src/Nova.xcodeproj/project.pbxproj`
- Kids app source: `/Users/nolan/Projects/Novai/src/Apps/NovaKids/Sources`
- Kids app assets: `/Users/nolan/Projects/Novai/src/Apps/NovaKids/Resources/Assets.xcassets`
- Backend: `/Users/nolan/Projects/Novai/src/Backend`

## Standard Validation

Run from repo root:

```bash
git diff --check
xcodebuild -workspace src/Nova.xcworkspace -scheme NovaKids -destination 'generic/platform=iOS Simulator' build CODE_SIGNING_ALLOWED=NO
```

For simulator smoke testing:

```bash
xcrun simctl list devices booted
xcrun simctl install booted /Users/nolan/Library/Developer/Xcode/DerivedData/Nova-eqrmsusyotfhzscnujfcyfphwfpi/Build/Products/Debug-iphonesimulator/NovaKids.app
xcrun simctl launch booted com.nova.kids
```

DerivedData path can change. If install fails, locate the product:

```bash
find /Users/nolan/Library/Developer/Xcode/DerivedData -path '*Build/Products/Debug-iphonesimulator/NovaKids.app' -maxdepth 8 -print
```

## Local Backend

Start the local service from the backend directory:

```bash
cd /Users/nolan/Projects/Novai/src/Backend
npm run dev
```

Backend package script: `dev` runs `tsx watch src/server.ts`.

## Xcode Project Membership

This project is not fully folder-synced. New Swift files may compile locally only after manual project registration.

When adding a new Swift file under `src/Apps/NovaKids/Sources`, verify:

- `PBXFileReference` exists.
- `PBXBuildFile` exists.
- The file reference is listed in the `NovaKids` group children.
- The build file is listed in the `NovaKids` `PBXSourcesBuildPhase`.

Symptom of missing registration: other files compile, but the compiler reports missing members/types defined in the new file.

## Dirty Worktree Rules

- Never revert changes that were not made in the current task.
- If unrelated modified files exist, ignore them unless they affect the current build.
- If the same files are touched by previous agent work, read them carefully and work with the existing changes.
