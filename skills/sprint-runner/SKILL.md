---
name: sprint-runner
description: Track solo indie sprints — scaffold sprint trackers, compose per-story run summaries from git log + test output, and maintain a rolling sprint-runs index. Use this skill whenever the user mentions sprints, sprint tracking, sprint planning, closing out a sprint, writing a run summary, documenting what shipped, or any `docs/SPRINT-N-tracker.md` / `docs/sprint-runs/` work in their repo. Also trigger when the user says "start a sprint", "new sprint", "finish sprint", "close sprint", "write up this run", "what shipped", "sprint summary", "retire debt", or references story IDs like S10-12 / S11-03. Prefer this skill over generic Jira/Atlassian tooling for solo-dev projects — it is purpose-built for bang's idiom (tracker + per-run summary + index, commits + tests as delivery artifacts, hours-to-days cadence).
---

# Sprint Runner

A skill for running bang's solo indie sprint idiom. Sprints ship as three coordinated artifacts living in the repo:

1. `docs/SPRINT-N-tracker.md` — the sprint's plan of record. Scoped at sprint start, updated in-place as decisions land, closed out with final status + epic summaries.
2. `docs/sprint-runs/SN-XX-<slug>.md` — one file per story that actually shipped. Dense technical prose, validation matrix, runbooks, curl cheat sheets, retired debt.
3. `docs/sprint-runs/index.md` — rolling ledger of all runs, sorted newest-first, with one-line meta per entry.

The tracker is the **forward-looking** document (what I committed to). The run summaries are the **backward-looking** truth (what actually landed, with what trade-offs). The index is the scanner's entry point.

This skill preserves bang's voice — it does NOT invent a new format. When generating documents, imitate the patterns in `references/bang-style-guide.md` exactly: em-dashes, "in-plan vs drift" framing, numbered architectural decisions with "why X over Y" rationale, sandbox-vs-Mac validation split, per-file changelogs with LOC counts.

## When this skill runs

**Trigger phrases that should make Claude reach for this skill:**

- "start sprint N" / "new sprint" / "scaffold a tracker"
- "finish sprint" / "close out" / "write up this run" / "what shipped"
- "retire debt" / "in-plan vs drift"
- "sprint index" / "sprint ledger" / "update the run list"
- Any reference to a story ID in bang's pattern (`S10-12`, `S11-03`, etc.)
- Any mention of `docs/SPRINT-N-tracker.md` or `docs/sprint-runs/`

If Claude is about to reach for `jira-expert`, `senior-pm`, or `scrum-master` for bang's Novai/trading/cowork work — use this skill instead. Those are for multi-team enterprise contexts; this skill is for solo indie cadence.

## Operations

This skill supports four operations. Pick the one that matches the user's intent.

### Operation 1: `new-sprint` — scaffold a new sprint tracker

**When to use:** User says "start Sprint N", "scaffold a new tracker", or explicitly references a future sprint number.

**Required inputs:**
- Sprint number (N)
- Goal statement (1–2 sentences)
- Velocity target (points)
- Start date (YYYY-MM-DD)
- Duration (default 2 weeks if not specified)

**Optional inputs:**
- Epic breakdown (epic name → story list). If user doesn't supply, ask once, then stub with a single "TBD" epic.
- Carry-in debt from prior sprint.

**Steps:**
1. Read the most recent `docs/SPRINT-*-tracker.md` to match style.
2. Run `scripts/new_sprint.py` with the inputs to generate the skeleton. It writes to `docs/SPRINT-N-tracker.md`.
3. Open the generated file and fill in Epic sections, Key Decisions (blank block), and initial story rows.

**Critical:** Do NOT invent velocity numbers or deadlines. If the user didn't give you a number, ask before running the script — better to pause than to anchor the sprint on hallucinated estimates.

### Operation 2: `update-sprint` — append to an open sprint

**When to use:** User says "we decided X", "carry this over", "add a story", "scope changed", or otherwise wants to modify an open tracker mid-sprint.

**Steps:**
1. Read the current `docs/SPRINT-N-tracker.md`.
2. Identify which section needs the edit:
   - **Story rows** — add to or modify the epic's table.
   - **Key Decisions** — append a numbered entry with rationale ("why X over Y").
   - **Scope changes** — add a "Scope change" line to the meta block, and mark moved stories with ↪ (moved to S{N+1}).
   - **Carry-in debt** — add to the "Carry-in from SN-1" section.
3. Use `Edit` tool with precise `old_string`/`new_string` — never rewrite the whole file.
4. Preserve existing formatting exactly (table alignment, blank lines, emoji status icons).

**Do not auto-update status icons.** Bang updates those manually during stand-ups or when closing stories. Only touch them if the user explicitly says "mark S10-05 as done".

### Operation 3: `finish-sprint` — generate per-story run summary + update tracker

**When to use:** User says "write up S10-12", "finish sprint", "document this run", "what shipped in this session", or "close out story X". This is the most common operation.

**Required inputs:**
- Story ID (e.g., `S10-12`)
- Git commit range (`--from <sha> --to <sha>` or branch name). If the user doesn't give you one, infer from recent commits matching the story ID in the message, but confirm before proceeding.

**Optional inputs:**
- Test count before/after (if not supplied, script attempts to parse vitest/jest output from the user's last paste or from a provided log path).
- Retired debt items (stories this run closes out that were carry-in).

**Steps:**
1. Run `scripts/run_summary.py --story <ID> --from <sha> --to <sha>` to gather:
   - `git log --oneline` between the refs
   - `git diff --stat` aggregated by file
   - Commit message parsing to pull out `feat(scope):` / `fix(scope):` grouping
   - LOC counts per file
2. The script emits a **structured draft** to `docs/sprint-runs/SN-XX-<slug>.md` with prose placeholders in `<!-- FILL: ... -->` HTML comments. Claude's job is to replace those placeholders with actual technical narrative.
3. Read `references/run-summary-shape.md` for the template sections and voice guidance.
4. Fill in:
   - Opening paragraph (context — link to prior runs, why this story mattered)
   - Numbered Architectural decisions (with "why X over Y" rationale — this is the single most important section)
   - Validation matrix (sandbox ✅ vs 🟡 Mac-only blocked)
   - Quick-start runbook with `# expect:` annotations
   - End-to-end Dev Console walkthrough (if the feature has a UI surface)
   - curl cheat sheet (if there's an HTTP API) — always pipe through `jq` with expected output annotations
   - Feature-flag matrix (if any flags were touched)
   - Retired debt section (if this run closes out carry-in)
   - What's next (1–3 bullet preview of the next logical step)
   - Cross-references (links to prior runs, related ADRs, upstream PRs)
5. After the run summary is written, update `docs/SPRINT-N-tracker.md`:
   - Mark the story ✅ Done in the epic table
   - Update the Sprint Summary percentage line
   - Add a link to the new run summary from the story's Notes column
6. Run Operation 4 (`sprint-index`) to regenerate the rolling ledger.

**Voice rules when filling placeholders:**
- Use em-dashes (`—`), not double-hyphens.
- Explain trade-offs — every architectural decision must answer "why this over the alternative".
- Split validation between sandbox ✅ (what ran here) and 🟡 Mac-only (what needs bang to run locally).
- Include a "Prerequisites bang must run on his Mac" bash block if there are Mac-only validation steps.
- Never pad. If there's nothing to say for a section, delete it rather than writing filler.

### Operation 4: `sprint-index` — regenerate the rolling ledger

**When to use:** After any `finish-sprint` operation, or when the user explicitly says "update the index" / "rebuild sprint-runs index".

**Steps:**
1. Run `scripts/sprint_index.py` which scans `docs/sprint-runs/S*.md`, parses the meta block from each, and regenerates `docs/sprint-runs/index.md`.
2. The index is sorted newest-first (by Landed date from meta block).
3. Format: markdown table with columns `| Run | Story | Landed | Status | One-line summary |`.
4. Include a short preamble paragraph explaining the ledger's purpose (copy from the existing index if present).

The script is idempotent — safe to run any time.

## Scripts — what they do

- `scripts/new_sprint.py` — renders `templates/tracker.md.hbs` with user inputs, writes to `docs/SPRINT-N-tracker.md`. Fails fast if the file already exists (prevents accidental overwrite).
- `scripts/run_summary.py` — parses git log + diff stat, renders `templates/run-summary.md.hbs`, writes to `docs/sprint-runs/SN-XX-<slug>.md`. Leaves `<!-- FILL: ... -->` placeholders for Claude to replace.
- `scripts/sprint_index.py` — scans `docs/sprint-runs/`, parses meta blocks, regenerates `docs/sprint-runs/index.md`.

All scripts accept `--repo-root <path>` (default: current working directory, auto-detected by walking up to find `.git`). They work from anywhere in the repo tree.

## Templates — the source of truth for format

Read these before filling in any document. Templates encode the exact shape bang expects; deviating breaks the muscle memory of scanning the docs week over week.

- `templates/tracker.md.hbs` — sprint tracker skeleton (meta block, epic tables, sprint summary, key decisions, files changed)
- `templates/run-summary.md.hbs` — per-story run summary (meta block, what shipped, runbook, validation matrix, curl cheat sheet, retired debt, what's next, cross-references)
- `templates/index.md.hbs` — rolling ledger preamble + table

## References — read these for voice and detail

- `references/bang-style-guide.md` — voice conventions (em-dashes, "in-plan vs drift", numbered decisions, sandbox-vs-Mac split, curl/jq pattern). **Read this before writing any prose.**
- `references/tracker-shape.md` — annotated tracker template with "why this section exists" callouts.
- `references/run-summary-shape.md` — annotated run-summary template with section-by-section guidance.

## Why this skill exists (and what it intentionally does NOT do)

Jira, Linear, and shared backlogs are the wrong abstraction for solo indie work on hours-to-days cadence. bang's source of truth is his git log + the markdown docs in his repo. This skill formalizes the pattern he's already running — it does not try to replace it with enterprise ceremony.

**What this skill does NOT do:**
- Does not create Jira tickets, Linear issues, or external project-management artifacts.
- Does not try to enforce story-point calibration or Fibonacci sizing — bang's points are directional, not actuarial.
- Does not auto-update story status icons — those are bang's editorial call.
- Does not invent test counts, LOC numbers, or timing data. If the data isn't in git + test output, leave the placeholder.

**What this skill does:**
- Preserves bang's exact document shape week over week so scanning stays fast.
- Collapses the mechanical work (git log parsing, diff stats, index regeneration) into scripts so Claude spends its tokens on the narrative.
- Makes the "in-plan vs drift" distinction explicit — the tracker shows intent, the run summary shows truth, and drift is called out not hidden.
