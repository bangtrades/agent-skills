# bang's voice guide for sprint docs

Read this before writing any prose in a tracker or run summary. The format of the document is the LLM-generated part; the voice is what makes it scannable week over week.

## Core voice conventions

**Em-dashes, not double hyphens.** `—` (U+2014), never `--`. Em-dashes are used to append a clause that elaborates or qualifies, e.g., "parsed the git log into structured records — didn't bother with merge-commit filtering since we don't rebase".

**Dense technical prose, not marketing copy.** Sentences are packed: what was built, why, what trade-off was accepted. No "we're excited to announce". No "great progress this sprint".

**Lowercase `bang` in running prose.** Proper noun in headings is fine ("Prerequisites bang must run on his Mac"), but mid-sentence references stay lowercase. Same for `Claude`, which is treated as a collaborator not a product name.

**Past tense for what happened, present tense for what's true now.** "Parsed the commit range" (happened). "The loader cache is keyed on file mtime" (still true).

## Structural conventions

### "In-plan vs drift" framing

Every sprint has scope. The tracker records intent; the run summaries record truth. When the truth diverges from the plan, call it **drift** explicitly rather than quietly editing the tracker to match.

Examples:
- "In plan: ship story-writer and quiz-maker in the same sprint. Drift: quiz-maker carried into S10-07 because the skill loader needed a redesign we didn't see in the spike."
- "Drifted ahead of plan — picked up S10-12 a day early because S10-11 landed clean."

Drift is not failure. Hidden drift is failure. Naming drift keeps the tracker honest.

### Numbered architectural decisions with "why X over Y"

Every non-trivial decision gets a numbered entry. The format:

> **N. <One-line decision statement>** — <What was chosen>. <Why it was chosen over the obvious alternative>. <Trade-off accepted>.

Example:

> **3. Handlebars over EJS for skill templates** — Handlebars' lack of arbitrary JS in templates was the point. Picked it over EJS because skill definitions should be declarative; baking JS into templates creates a second place where logic can hide. Trade-off: lost some flexibility for multi-line conditionals, which we work around with helpers.

The "why X over Y" part is what makes these useful three months later. Without it, you just have a list of choices you made, not a record of why those choices were defensible.

### Sandbox ✅ vs Mac 🟡 validation split

Claude runs in a sandbox that can execute some things (unit tests, typecheck, static analysis) but not others (database migrations, long-running integration tests, Dev Console UI flows). Every run summary's validation matrix makes this split explicit.

- ✅ = sandbox ran it and it passed.
- 🟡 = requires bang to run locally; documented but not yet validated in this session.
- ❌ = tried and failed (rare; usually means the run summary is premature).

The 🟡 rows block on "Prerequisites bang must run on his Mac" — always include that block when any Mac-only validation is required.

### Per-file changelogs with LOC counts

The "What shipped" section lists every file touched with `(status, LOC-delta)`. Status is `new`, `edited`, `deleted`, `renamed`. LOC delta is `+added/-removed` from `git diff --numstat`. For test files, bang often wants the test-count delta annotated inline: `(edited, +147/-2, +7 tests, 23 → 30)`.

### Runbooks with `# expect:` annotations

Every bash block in a runbook includes `# expect:` annotations after each command so a future reader (or bang three weeks from now) knows what success looks like without having to run it.

```bash
npm test -- skillRouter
# expect: 30 passing, 0 failing (up from 23)

curl -s localhost:3001/health | jq '.skillEngine'
# expect: "loaded"
```

### curl cheat sheets piped through jq

Every HTTP API gets a curl cheat sheet. Every curl is piped through `jq` with an explicit `# expected:` comment showing the shape (not necessarily the content) of what comes back. This turns the cheat sheet into an executable spec.

```bash
curl -s -X POST localhost:3001/api/skill/execute \
  -H 'content-type: application/json' \
  -d '{"skillId":"story-writer","args":{"age":7,"topic":"dragons"}}' | jq '{title, wordCount: (.body|split(" ")|length)}'
# expected: { "title": "...", "wordCount": 180 }  (story-writer targets ~180 words for age 7)
```

## What NOT to do

- **Don't pad.** If there are no feature flags, delete the Feature-flag matrix section. If no UI surface, delete the Dev Console walkthrough. Empty sections read as broken, not thorough.
- **Don't invent numbers.** If the script didn't give you a test count, don't make one up. Leave `(+? tests, ? → ?)` so bang knows to fill it in.
- **Don't auto-update story status.** The tracker's ⏸/⚡/✅ icons are bang's editorial call. The run summary landing is what evidences a ✅, but marking it is still manual.
- **Don't use "we" loosely.** "We decided X" usually means "bang and Claude in this session decided X". If a decision predates this session, name the source: "S9 set the precedent of X".
- **Don't over-commit in "What's next".** 1–3 bullets, each 1 line. This is a preview, not a plan. The plan lives in the next sprint's tracker.

## Example voice comparisons

### ❌ Wrong voice

> We're happy to announce that in this sprint we delivered the new skill engine! This was a major milestone for the team. We faced some challenges along the way, but we overcame them through great teamwork and dedication. The engine now supports all the features we set out to implement. We look forward to what comes next!

### ✅ Right voice

> Landed the skill engine — Handlebars-based definitions in `src/services/sparky/skills/`, per-atom routing in `skillRouter.ts`, retry-on-Zod-validation wired end to end. Drift from plan: the loader needed a redesign we didn't see in the spike, so quiz-maker slipped to S10-07 and carried in S10-08's modality-partial work. Retired S9-07 (flaky validation retries) in the process.

## Cross-reference conventions

- Prior runs: `[S10-11](./S10-11-teaching-strategy.md)`
- ADRs: `[ADR-0004 — Skill engine shape](../adrs/0004-skill-engine-shape.md)`
- Tracker: `[SPRINT-10](../SPRINT-10-tracker.md)`
- Upstream bug: use the external URL, don't paraphrase.

Links are always markdown, always lowercase for paths, and always relative to the current document.
