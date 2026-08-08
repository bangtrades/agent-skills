---
name: orchestration
description: Coordinate complex software work across multiple agents — plan disjoint slices, dispatch dev agents, run adversarial QA gates, verify all claims against evidence, and manage tracker/board state. Trigger on "orchestrate agents", "dispatch agents", "run the sprint", "coordinate a build", "agent slices", multi-agent dev work, or any request to plan/execute/verify parallel engineering work. Self-improving - every orchestration run ends by reviewing and patching this skill.
---

# Orchestration

Coordinate complex software work across multiple agents, contributors, or implementation slices. Convert messy project state into clear parallel work, truth-based reporting, and a release path that never confuses activity with progress.

Project-agnostic: discover the repository, sprint plan, local instructions, test gates, tracker conventions, and report formats from the active working context.

## Core Rule

**Orchestrate from evidence, not optimism — and that includes your own claims.** A slice is complete when code, tests, gates, logs, tracker state, or an explicit operator result prove it against acceptance criteria. An orchestrator's diagnosis is a *claim* like any other: before any destructive or irreversible action, the premise itself must be independently verified (see Law 1).

## The Laws (earned in production — each one cost something)

**Law 1 — The orchestrator is fallible; verify premises before destructive acts.**
Incident: an orchestrator concluded live checkpoint tables were "inert" from `max(thread_id)` over a *text* UUID column — a lexicographic max that says nothing about recency — and queued an archive that would have destroyed running production state. An independent QA agent overturned the premise minutes before execution. Rule: any archive/drop/migration/teardown gets its *premise* re-derived by an agent who didn't form it, from raw evidence. Prefer reversible forms (rename/archive-schema over drop; disable over delete) even after verification.

**Law 2 — The environment silently discards configuration; verify guarantees empirically, never structurally.**
Incidents: a connection pooler (Supavisor) silently dropped `options=-csearch_path=...` startup parameters, rendering a schema-isolation control inert while every health check stayed green; `uv pip compile` preserves existing pins when the output file exists and fresh-resolves when it doesn't, making a CI freshness check pass or fail depending on output path; GitHub's `required_approving_review_count: 0` silently disables the code-owner review machinery a rule appears to enable. Rule: any guarantee mediated by infrastructure (poolers, CI runners, platform APIs, package managers, branch protection) must be proven by observing the *live effect* (query `pg_stat_activity`, run the negative test, trip the gate), not by reading the config that requests it.

**Law 3 — Success output must assert the postcondition, not completion.**
Incident: a deploy-prep script printed two success lines while its `setup()` no-op'd against the wrong schema — the operator had no way to know. Rule: every script/gate/probe that reports success must verify the *resolved state* (e.g. `to_regclass` in the bound schema, row landed, ref updated) and fail closed otherwise. A readiness probe that checks "a table with this name is readable" cannot distinguish success from fallback.

**Law 4 — Fake-fidelity: every external-SDK seam needs one test against the real client.**
Incident: an agent added a `usage` kwarg asserted by 19 tests — all of which faked the client one level below the seam; the real SDK's method had no such parameter and every live model call crashed. Rule: for each external dependency seam, require one test that constructs the REAL pinned client (offline construction is usually free) through the production code path. QA must probe whether fakes are more permissive than the real dependency.

**Law 5 — Deterministic gates before subjective judgment.**
In product code: hard-loss pre-checks run before the LLM reviewer, and no model opinion can override them. In orchestration: run the cheap deterministic checks first — per-branch file lists, pairwise overlap (must be empty), parent SHAs, byte-identical merge order, governance/holdout paths untouched, lock freshness — before any subjective code review. Also watch for judge anchoring: a reviewer that returns the same passing score on every artifact is not discriminating; deterministic gates are what's actually protecting you.

**Law 6 — Pin the toolchain; CI installs what production installs.**
Incidents: floating `ruff>=` broke CI on every push when a new ruff shipped; floating `mcp>=1` broke collection when 2.0 relocated a module — while production stayed green because it installed from the hash-pinned lock. Rule: exact-pin dev tools, semver-guard runtime deps, and make CI consume the same lock artifact production consumes. A verification gate that floats its own tooling generates false alarms that train people to ignore it.

## The Dev→QA Pipeline (default for any wave that writes code)

1. **Plan disjoint slices.** Ownership by file path, verified disjoint (`git show --name-only` pairwise intersection = empty). If two slices need one file, sequence them or split at hunk level and verify hunks don't share context lines. Stacked work branches from an integration base built from already-QA-passed branches.
2. **Dispatch dev agents in parallel** with self-contained prompts: context (3–6 sentences), goal, acceptance criteria, primary ownership paths, explicit NO-GO paths (governance/signed artifacts, holdout repos, other agents' files), safety rules, exact verify commands, report contract. Tell agents to *verify orchestrator-provided facts* (SHAs, file claims) rather than propagate them — agents have corrected orchestrator briefing errors and must be licensed to.
3. **QA gate (separate agent, fresh eyes, adversarial mandate).** Reproduce the devs' numbers independently in fresh venvs; build a combined merge preview and run the full suite on it; write NEW adversarial probes (never only re-run the devs' tests) targeting the specific guarantees each slice claims; static review for swallowed exceptions, contextvar/lock hygiene, injection surfaces. Verdict per slice: PASS / FAIL with minimal repro. A FAIL blocks the wave.
4. **Fix rounds go back to the same dev** (context retention), with the QA findings verbatim. Require **negative-controlled regressions**: the dev must demonstrate each new test fails with the fix reverted. Then QA re-gates, re-running the original attack probes plus new probes against the fixes themselves.
5. **Orchestrator's own smoke before suggesting commits/merges:** exercise the real public seams yourself (not the agents' tests) — the SSRF guard with real blocked addresses, the auth layer with real status codes, the secret with a real `repr()`.
6. **Merge queue:** verify every branch's parent, confirm merge order produces a byte-identical tree both ways, hand the operator exact commands, and name any env vars or operator steps the deploy will newly require *before* they hit them (a fail-closed feature that needs a new secret will 503 by design — say so up front).
7. **Persist probe suites** across gates (e.g. `/tmp/qa-probes/`) and do the bookkeeping when a contract deliberately flips: retire superseded probes explicitly, never let stale assertions rot into noise.

## Multi-Agent Git Mechanics (macOS/FUSE-mounted repos especially)

- One worktree per agent (`git worktree add /tmp/<slice>-wt <branch>`); the shared checkout is contended and mounts may block `unlink` (stale `.git/*.lock` files: delete the specific lock, retry once; a rename-aside also works when delete is blocked).
- Stage explicitly per path — never `git add -A` in a shared tree that carries other agents' WIP or operator leftovers.
- An agent's commit can be stranded in an ephemeral sandbox: rescue via `git bundle` and import into the durable repo, then verify the ref actually updated (ref-update failures under lock contention are silent-ish).
- After every wave: `git worktree prune`, restore the shared checkout to main, verify with `git status`.
- Reconcile *claims vs repo truth* for every agent report: branch exists, tip SHA matches, file list matches, protected paths untouched. A report with no matching commit is a reporting gap, not completion.

## Triage Before New Slices

When gates disagree, tests loop, or a tool "worked" but the tracker says failed — stop generating slices and isolate the failing layer first: static/config → runtime/service health → prompt/task delivery → tool execution lifecycle → canonical audit/log evidence → semantic final response → gate/reporting truth → release decision. Patch only the proven-defective layer. If a verifier misreports true success, fix the verifier separately from the runtime. Cheap canonical evidence (one SQL query, one log line, one `pg_stat_activity` row) beats a rerun.

## Holdout / Eval Hygiene

When acceptance is judged by holdout scenarios: the grader is a fresh-context agent with zero implementation context; the orchestrator and producing agents never see scenario contents; results are committed to the holdout repo only (verify the commit touches results paths exclusively); the grader reports scores/verdicts back — never cases. Honor a NO-GO: split its remediation into tracked issues rather than arguing with the examiner, and let the operator explicitly ratify any scope-out. Re-run the same suite after remediation for an honest close.

## Board / Tracker Discipline

- Issue → In Progress at dispatch; evidence comment + state change at completion; blockers commented honestly. Post a project status update at wave end.
- States must reflect reality: demote issues nobody is working, split "done but for one operator step" out with a `needs:operator`-style label + assignment, and file every incidental finding as its own issue *at the moment of discovery* — verification discoveries (defects in the checker, environment semantics, dead code) get filed, not just mentioned in chat.
- Operator-only actions (secrets, signing keys, 2FA-gated changes, data-destruction sign-off) become dedicated assigned issues with exact steps; agents never touch them. Operator placeholder traps: when handing commands with placeholders, expect them to be pasted literally once — design instructions so the failure is obvious and cheap.

## Reporting Format

1. **Current Verdict** — what is true now. 2. **Evidence** — commands, reports, gates, ids. 3. **Slices** — prompts / ownership matrix. 4. **Dependencies** — parallel vs sequential. 5. **Risks** — misreports, stale evidence, shared-file conflicts. 6. **Next Action** — the smallest useful move.

## Anti-Patterns

- More agents to compensate for unclear root cause.
- Any two agents writing one shared file in the same wave.
- Accepting screenshots/agent comments without log/gate corroboration when release truth matters.
- Re-running expensive live tests before checking whether the last run already contains canonical proof.
- Mixing runtime fixes, gate-truth fixes, docs, and release commits without naming scope.
- Burying "remaining defect" under a green headline — and its dual: burying a green system under an un-actioned defect list.
- Destructive action on an orchestrator-derived premise nobody independently checked (Law 1).

## Self-Improvement Loop (mandatory — this is what keeps the skill alive)

**Every orchestration run ends with a retro that patches THIS skill.** Not optional, not "when something big happens" — every run:

1. Ask: What moved the project? Which slices were mis-scoped? Which reports/gates/logs misled? What did QA catch that the process should have caught earlier? What did the *environment* do that code-reading couldn't predict? Did the orchestrator itself err, and would a written rule have prevented it?
2. Distill at most 1–3 crisp additions: a new Law (only if it generalizes beyond the incident), a checklist line, or a template refinement. Prefer one sharp rule over narrative. If nothing genuinely new was learned, append only a changelog line saying so — resist ritual bloat.
3. **Patch this skill via the skill-publish gate** — never write the registry directly. Append a dated entry to the Changelog below (date, project, what was learned, what changed), stage the updated skill dir to `~/Cortana/cortana-vault/_inbox/skills/orchestration/`, and hand the operator the one-liner `~/Cortana/cortana-skill-registry/bin/publish-skill.sh orchestration`. Persist the same content to the account store (save the skill in-session, or deliver a `.skill` file for the operator to save). See the `skill-publish` skill for the full loop.
4. Prune: if a rule has never fired across many runs or has been superseded, fold it into a tighter law and note the consolidation in the changelog. The skill should get sharper, not longer.

## Changelog


- **2026-08-08b · P1 vault remediation wave (4 parallel dev + QA; all slices first-gate PASS).** Learnings: (1) **Content-vault waves parallelize on path ownership alone** — no worktrees needed when slices are disjoint by directory and nobody commits; the QA gate's ownership-matrix check (every modified path maps to exactly one slice) is the load-bearing control. (2) **Read-path indexes double as drift detectors** — the act of enumerating a folder against its hub exposed a same-morning exporter/hub divergence no one was looking for; indexes are cheap sensors, not just navigation. (3) **Name cross-deliverable interactions at dispatch:** a staleness sweep that deliberately preserves `updated:` and a sync script that rewrites `updated:` from mtime are mutually clobbering if applied in the same wave — the dev agent caught it and the apply was deferred; check each slice's postconditions against every OTHER slice's planned side effects before running batch normalizers.
- **2026-08-08 · P0 vault remediation wave (2 dev + 1 QA + orchestrator runbook).** Learnings: (1) **Law 7 mechanism catalogued: a bash heredoc clobbers piped stdin** — the orchestrator's own pre-commit YAML guard read `''` from stdin and passed everything while its sibling guards worked; per-guard poison probes (QA testing each guard in isolation) caught what a single combined probe would have missed. Guards written and tested by the same party stay vacuous. (2) **Cowork sandbox silently blocks `unlink`** until `allow_cowork_file_delete` is granted — git init half-fails with stale index.lock + thousands of tmp objects; the clean recovery is delete-permission → `rm -rf .git` → re-init, not lock surgery. (3) "Recoverable via baseline commit" is a *claim requiring the file be tracked* — a path gitignored before the baseline is not in the baseline; verify with `git ls-tree` before promising recoverability of a planned deletion (Law 1 corollary).
- **2026-08-07 · Obsidian multi-agent vault research wave (4 Firecrawl research agents + 1 Explore auditor, fully parallel).** Learnings: (1) **Law 1 applies to audits, not just destructive acts** — the vault auditor's first pass computed a 5× wrong broken-link rate by trusting the vault's own SCHEMA.md for the root path; it self-corrected only by re-deriving the premise from live config (`.obsidian` mtimes). Rule: an audit's frame-of-reference (roots, scopes, exclusion lists) must be discovered from live state, never from the subject's documentation. (2) **Research slices partition cleanly by question-domain with explicit NO-GO topics** — zero overlap across 4 agents on adjacent subject matter; the "suppressed candidates" report section (from Eval-Wave Rules) transferred well to research waves as adjudication evidence. (3) Load-bearing external claims that post-date orchestrator knowledge (here: Obsidian CLI) get one primary-source re-verification by the orchestrator before entering the deliverable — cheap, and it upgraded a hearsay-grade claim to verified.
- **2026-07-29 · MetaCortex build cycle (6 orchestrations: deploy wave, dev wave, eval wave, security wave, 4-slice sprint w/ 3 QA gates, parked-items wave).** Major revision. Added Laws 1–6 from production incidents: orchestrator premise error nearly destroyed live checkpoint tables (Law 1); Supavisor/uv/GitHub silently discarding configuration (Law 2); deploy-prep success-on-no-op (Law 3); fake-fidelity crash of every live model call (Law 4); deterministic-gates-first + judge anchoring (Law 5); floating-toolchain CI noise (Law 6). Codified the Dev→QA pipeline (adversarial gates, fix rounds with negative controls, orchestrator smoke, probe-suite persistence), multi-agent git mechanics for FUSE-mounted repos (worktrees, lock protocol, bundle rescue), holdout hygiene (fresh-context grader, results-only commits, honor the NO-GO), and board discipline (file findings at discovery; operator placeholder traps). Replaced the old improvement note (which pointed at a stale path and a manual prompt) with this mandatory persistent-registry loop. Scoreboard for the cycle: ~10 would-be production defects caught pre-merge by the pipeline, 2 caught post-deploy by live evidence, 1 orchestrator error caught by QA.
- **2026-07-29 · skill-publish gate adopted.** Registry writes now flow through the staged publish process (`_inbox/skills/<name>/` → `bin/publish-skill.sh`, operator diff+confirm). Replaced the ad-hoc mirror-copy instruction in Self-Improvement step 3; this revision converges the disk registry, account store, and staging copy that had drifted three ways.
