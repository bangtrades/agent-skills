# Tracker shape — annotated template

The sprint tracker is the forward-looking document: what bang committed to shipping this sprint. It lives at `docs/SPRINT-N-tracker.md`. It is created once at sprint start, updated in-place as decisions land and stories close, and transitions from 🟡 Open to ✅ Closed at sprint end.

This file annotates every section with "why it exists" so Claude knows what to preserve when editing.

## Full skeleton

```markdown
# Sprint N Tracker — <Theme>

**Sprint dates:** YYYY-MM-DD → YYYY-MM-DD
**Goal:** <1–2 sentences>
**Velocity target:** N pts
**Status:** 🟡 Open   (or ✅ Closed at sprint end)

## Carry-in from Sprint N-1

<Bullet list of debt/stories carried over, with brief rationale.>

## <EPIC-NAME> Epic — <Short description> (X pts)

| ID | Story | Pts | Status | Notes |
|----|-------|-----|--------|-------|
| SN-01 | <title> | 3 | ⏸ Pending | <notes> |
| SN-02 | <title> | 5 | ⚡ Partial | <notes + link to run summary> |

**<EPIC-NAME>: 8/X pts — <status phrase>**

## <ANOTHER EPIC> ...

## Sprint Summary

| Epic | Points | Complete | Pending |
|------|--------|----------|---------|
| EPIC-1 | 15 | 8 | 7 |
| EPIC-2 | 10 | 0 | 10 |
| **Total** | **25** | **8** | **17** |

**Completion: 32% — Sprint in progress.**

## Key Decisions

1. **<Decision>** — <What was chosen>. <Why over alternative>. <Trade-off>.
2. ...

## Files Changed

### SN-01 — <Story title>
- `path/to/file.ts` (new, +120)
- `path/to/other.ts` (edited, +47/-12)

## Run Summaries

- [SN-04 — <Title>](./sprint-runs/SN-04-slug.md)
- [SN-11 — <Title>](./sprint-runs/SN-11-slug.md)
```

## Section-by-section notes

### Meta block (top 4 lines)

The meta is a fixed-shape header so every tracker parses uniformly. Do NOT add or reorder fields. If you need extra context, add a prose paragraph after the meta block before the first `##` heading.

Status values:
- 🟡 Open — sprint is in progress
- ✅ Closed — sprint ended, all stories accounted for
- 🔴 Abandoned — rare, used if the sprint was scrapped mid-flight

### Carry-in from Sprint N-1

Optional section. Include only if debt actually carried. If included, each item names the original story ID and a one-line reason it slipped.

### Epic sections

One `## <EPIC> Epic — <Description> (<total_pts> pts)` per epic. The table is fixed-shape. Status icons:
- ⏸ Pending — not started
- 🔵 In progress — mid-flight
- ⚡ Partial — shipped with known gaps documented in the run summary
- ✅ Done — complete, run summary exists
- ↪ Moved — deferred to next sprint (name target: ↪ S{N+1})

The epic summary line (`**<Epic>: X/Y pts — STATUS**`) is updated every time a story status changes. Use `npm run sprint:refresh` if bang has that wired, otherwise update manually — the math is small.

### Sprint Summary table

Rolled-up totals across all epics. The bottom row is always `| **Total** | **<sum>** | ... |` with bold markers. Below the table, a one-line completion percentage.

### Key Decisions

The single most important section for future-bang. Every decision that took more than 10 minutes of thought gets a numbered entry. See `bang-style-guide.md` for the "why X over Y" format.

### Files Changed

Per-story sub-sections. Filled in as stories close. Each file gets `(status, +adds/-removes)` annotation. Large refactors can be summarized instead of line-item'd — use judgment, but err toward line-item.

### Run Summaries

Links to every closed story's run summary. Added as each story lands. Provides the scan-entry-point into the detailed docs.

## When to edit the tracker

- **Sprint start:** scaffold via `new_sprint.py`, fill in epics and story rows.
- **Mid-sprint decision landed:** append to Key Decisions.
- **Mid-sprint scope change:** update the story row, mark moved stories with ↪, and add a "Scope change" note in the meta area (NOT in the meta block — in a prose paragraph after it).
- **Story closed:** update status icon in the epic table, update the epic summary line, update Sprint Summary table, append per-story entry to Files Changed, add link to Run Summaries.
- **Sprint end:** flip Status to ✅ Closed, write a 1-paragraph retrospective below the Run Summaries section.

## When NOT to edit the tracker

- Don't rewrite history. If a decision got reversed, add a new numbered entry explaining the reversal — don't edit the old one out.
- Don't backfill dates. If a story actually shipped on day 8 of the sprint, the run summary says day 8 even if you're filling in the tracker on day 14.
- Don't auto-bump velocity targets. The velocity line is what bang committed to; final delivery vs target is its own lesson.
