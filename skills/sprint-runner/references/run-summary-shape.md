# Run-summary shape — annotated template

A run summary is the backward-looking truth of a single story's delivery. One file per story. Lives at `docs/sprint-runs/SN-XX-<slug>.md`. Written at the moment the story lands, referencing exact commits + test output.

Every section in the template exists for a reason. This file names the reason so Claude knows what to write, cut, or expand when filling placeholders.

## Full skeleton (with reasons)

```markdown
# SN-XX — <Story title> Run Summary

**Sprint:** N
**Story:** SN-XX (P pts)
**Retires:** SM-YY, SM-ZZ   (optional — only if this closes carry-in debt)
**Landed:** YYYY-MM-DD
**Status:** ✅ Done | ⚡ Partial

<1-paragraph opening — 2–4 sentences setting context.>
```

**Why the meta block is fixed-shape:** scripts parse these fields to build the rolling index. Adding fields breaks the index parser; reordering fields makes diff hunks across sprints look like rewrites.

**Why an opening paragraph:** when someone lands on this file cold (from a grep or an index link), the first paragraph has to answer: what is this, why did we do it, what was happening before it. Link to prior runs so the reader can trace the thread.

### `## What shipped`

```markdown
## What shipped

- `src/services/sparky/skillRouter.ts` (new, +312)
- `src/services/sparky/skills/story-writer/prompt.md` (new, +89)
- `tests/sparky/skillRouter.test.ts` (new, +147, 7 tests)

The skill engine routes each atom through a skill definition — skillRouter.ts
is the dispatch layer, story-writer is the first concrete skill. Tests cover
the routing matrix plus per-skill Zod validation retry.
```

**Why this structure:** the bulleted file list is the mechanical record (git diff --numstat can't lie). The prose paragraph below it is the *interpretation* — how do these files cluster, what's the narrative? A reader should be able to scan the list, then read two sentences, and understand the shape of the change.

### `## Architectural decisions`

```markdown
## Architectural decisions

1. **Per-atom skill routing over single-pipeline-per-request** — Each atom
   decides its own skill, so a mixed-content response (e.g., a story with
   an embedded quiz) can route atoms through story-writer and quiz-maker
   independently. Picked this over a single-pipeline-per-request model
   because response composition is orthogonal to skill selection; baking
   them together would have forced us to duplicate the dispatch layer
   for every new composition pattern. Trade-off: slightly more per-request
   overhead, which we measured at ~4ms/atom (acceptable).

2. **Zod validation with single retry, not N retries** — ...
```

**Why this matters more than any other section:** three months from now, bang will want to know why the code looks the way it does. Git blame tells you who, this section tells you why. Every decision has three parts: what was chosen, why it beat the alternative, what trade-off was accepted.

If there are no non-trivial decisions, delete this section. Padding it is worse than omitting it.

### `## Quick-start runbook (bang's Mac)`

```markdown
## Quick-start runbook (bang's Mac)

```bash
cd ~/Projects/Novai/src/Backend
npm run dev
# expect: Server listening on :3001 with "skillEngine: loaded" in startup logs

curl -s localhost:3001/api/skills | jq '.[].id'
# expect: array containing "story-writer" and "quiz-maker"

npm test -- skillRouter
# expect: 7 passing, 0 failing
```
```

**Why this section exists:** after bang context-switches off this work for a week, he needs a 30-second path to "yes this still works on my machine". `# expect:` annotations make it executable-as-spec — if the output diverges, bang knows immediately.

### `## Validation matrix`

```markdown
## Validation matrix

| Check | Where | Status | Notes |
|-------|-------|--------|-------|
| TypeScript compiles | sandbox | ✅ | `tsc --noEmit` clean |
| Unit tests | sandbox | ✅ | 646/646 green |
| Skill loader smoke test | sandbox | ✅ | `curl /dev/skills` returns expected shape |
| Dev Console "Skills" tab | bang's Mac | 🟡 | UI change, requires browser validation |
| Full pipeline with real DB | bang's Mac | 🟡 | sandbox has no Postgres |

### Prerequisites bang must run on his Mac

```bash
cd ~/Projects/Novai/src/Backend
npm run migrate
# expect: migrations applied, no errors

npm run dev
# then open http://localhost:3001/dev and click "Skills" tab
# expect: story-writer and quiz-maker both listed with green "loaded" badges
```
```

**Why the sandbox/Mac split:** the sandbox is honest about what it can and can't validate. If bang merges a run summary that claims ✅ on something the sandbox couldn't actually run, that's a lie-by-omission. 🟡 is the honest marker for "this needs bang to run it locally". The Prerequisites block makes that follow-up mechanical.

### `## End-to-end Dev Console walkthrough` (optional)

Include if the feature has a UI surface. Numbered steps a tester would follow. Each step says what to click + what state should result. Omit entirely if there's no UI.

### `## curl cheat sheet` (optional)

Include if there's an HTTP API surface. Every command piped through `jq` with an `# expected:` shape comment. See `bang-style-guide.md` for the pattern. Omit entirely if there's no HTTP surface.

### `## Feature-flag matrix` (optional)

Include only if flags were added or changed in this run.

```markdown
| Flag | Default | Effect when on | Effect when off |
|------|---------|----------------|-----------------|
| `skillEngine.enabled` | on (prod) | route through skillRouter | fall back to legacy cardGenerator |
```

### `## Debt retired` (optional)

If this run closed carry-in from a prior sprint, one short section per retired story. Format:

```markdown
### S9-07 — Retry-on-Zod-validation
The old pipeline silently passed malformed LLM output downstream. Skill engine
now wraps every LLM call in a Zod validate + single retry — if the retry also
fails, the atom bubbles up with a typed error instead of a partial response.
```

### `## What's next`

1–3 bullets. Each bullet is 1 line. Preview, not plan.

### `## Cross-references`

Links out — to prior runs, ADRs, external bugs. Keep to actually-relevant references. Don't link the entire sprint's worth of docs.

### Trailer

The script appends a trailer line with git range and LOC totals. Leave it in — it's the mechanical proof that the meta block matches reality.

## Editing rules

- **Fill placeholders with narrative, not checklist items.** The `<!-- FILL: ... -->` comments explain what the section should contain. Replace them with actual prose, don't leave the comment in.
- **Delete optional sections that don't apply.** An empty "Feature-flag matrix" is worse than no matrix.
- **Preserve the meta block exactly.** Scripts parse it.
- **Never paraphrase git log.** The commit list at the bottom is the evidence; prose above can interpret but shouldn't invent.
