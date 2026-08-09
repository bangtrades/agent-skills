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
Incident: an orchestrator concluded live checkpoint tables were "inert" from `max(thread_id)` over a *text* UUID column — a lexicographic max that says nothing about recency — and queued an archive that would have destroyed running production state. An independent QA agent overturned the premise minutes before execution. Rule: any archive/drop/migration/teardown gets its *premise* re-derived by an agent who didn't form it, from raw evidence. Prefer reversible forms (rename/archive-schema over drop; disable over delete) even after verification. Corollary: a compaction/handoff summary is itself an unverified premise — re-derive branch/merge state from live git before committing on a resumed session's word.

**Law 2 — The environment silently discards configuration; verify guarantees empirically, never structurally.**
Incidents: a connection pooler (Supavisor) silently dropped `options=-csearch_path=...` startup parameters, rendering a schema-isolation control inert while every health check stayed green; `uv pip compile` preserves existing pins when the output file exists and fresh-resolves when it doesn't; GitHub's `required_approving_review_count: 0` silently disables the review machinery a rule appears to enable. Rule: any guarantee mediated by infrastructure must be proven by observing the *live effect*, not by reading the config that requests it. Corollary: the fix must sit at a layer the environment cannot drop — an in-session statement beats a startup option.

**Law 3 — Success output must assert the postcondition, not completion.**
Incident: a deploy-prep script printed two success lines while its `setup()` no-op'd against the wrong schema. Rule: every script/gate/probe that reports success must verify the *resolved state* and fail closed otherwise. Extensions: a readiness value computed once at boot is a snapshot, not a check (3b); a verdict past its staleness bound reads un-ready (3c); and for data migrations the postcondition ladder is *structural parity → copy-count identity against recorded preflight numbers → a live-run probe with the source proven frozen* — the last rung (source count unchanged while the new path grows under real traffic) is the only one that proves the cutover rather than the copy (3d).

**Law 4 — Fake-fidelity: every external-SDK seam needs one test against the real client.**
Incident: an agent added a `usage` kwarg asserted by 19 tests — all faking the client one level below the seam; the real SDK's method had no such parameter and every live model call crashed. Rule: one test per seam constructs the REAL pinned client through the production code path. Watch shape (`ChatResult` vs `LLMResult`) and watch *library value-laundering*: a pinned client that back-fills absent fields with zeros can convert "no evidence" into "affirmative zero" one level below your check.

**Law 5 — Deterministic gates before subjective judgment.**
Hard-loss pre-checks run before the LLM reviewer; no model opinion overrides them. In orchestration: file lists, pairwise overlap, parent SHAs, byte-identical merge order, protected paths, lock freshness — before any subjective review. Watch for judge anchoring (a reviewer returning the same score every time is not discriminating).

**Law 6 — Pin the toolchain; CI installs what production installs.**
Floating dev tools broke CI on upstream releases while production stayed green on the hash-pinned lock. Exact-pin dev tools, semver-guard runtime deps, CI consumes the production lock artifact.

**Law 7 — A test that greps the whole artifact pins nothing. Scope assertions to the block that must carry the property.**
Incident: a migration's re-key assertion was satisfied by sibling sections even when the copy didn't re-key; fixed in §3, immediately recurred in §4. Extension: in layered defenses, *position the poison where only the guard under test can stop it* — a charset assertion whose control characters sit past the length clamp is satisfied by the length clamp alone. When a dev self-reports replacing a vacuous test, verify the replacement bites.

**Law 8 — Mutation-test the guards on anything that will touch production data.**
38 mutations on one migration → 17 initial survivors including a verification gate rewritable into a tautology. For governance *scans*, also mutation-test the loosening direction (over-harvest controls): pin the false-positive boundary too.

**Law 9 — QA findings are claims; the fix round's first act is to reproduce them.**
Incident: a re-gate reported a P2 fd leak with a measured repro. The fix-round agent reproduced it first and found the measurement was an artifact — the blackhole listener lived *in-process*, so every accepted connection added a server-side fd to the same process's count; a true out-of-process blackhole leaked nothing. The prescribed restructure was built, measured, and shown to move nothing. Rule: a QA repro's *measurement method* is part of the claim. Ship the stronger regression test anyway when the class of gap is real; record the refutation so the finding doesn't resurface.

## The Dev→QA Pipeline (default for any wave that writes code)

1. **Plan disjoint slices.** Ownership by file path, verified disjoint. Sequence or hunk-split shared files. Stacked work branches from an integration base of QA-passed branches.
2. **Dispatch dev agents in parallel** with self-contained prompts: context, goal, acceptance criteria, ownership + explicit NO-GO paths, safety rules, verify commands, report contract. **Brief the property to restore, not the code change to make** — devs honoring the property over the prescription have out-reasoned the brief repeatedly, confirmed by QA. Tell agents to verify orchestrator-supplied facts and to STOP at ownership boundaries.
3. **QA gate (separate agent, fresh eyes, adversarial mandate).** Independent repro in fresh venvs — *assert which tree the package resolves to first; the stale-venv trap has caught the orchestrator too*. Combined merge preview + full suite. NEW adversarial probes. PASS/FAIL per slice; FAIL blocks. "PASS with defects" is a normal verdict — rank and route them. When QA's mandate is read-only and its scope is the untouched remainder of the repo, run it CONCURRENTLY with dev — enforce with a written "you may not modify a single line of code, findings go in the report" clause. When two slices build against one contract in parallel, gate the SEAM explicitly, not just each side: diff the keys one side emits against the fields the other actually reads, and hand-check any field one side derives rather than receives.
4. **Fix rounds go back to the same dev** with findings verbatim, subject to Law 9: reproduce first, refute if refutable, fix what survives. Negative-controlled regressions, then re-gate. Grant cross-boundary ownership explicitly per round.
5. **Micro-rounds for small post-gate defects:** tight single-file briefs; orchestrator does the final verification itself instead of a third full gate — proportionate process beats ritual process.
6. **Orchestrator's own smoke before suggesting merges:** behavioural, on the real seams, on the merged tree.
7. **Merge queue:** parents verified, byte-identical tree both orders, exact operator commands, new env vars / operator steps named up front, order chosen so the trunk is never transiently self-inconsistent.
8. **Persist probe suites**; retire superseded probes explicitly when a contract deliberately flips.

## Operator-Runbook Execution (orchestrator-performed production changes)

When the operator gates open a runbook (data cutover, credential rotation, infra change), the orchestrator may execute it directly — held to the same standard as a code wave:

- **Discover live state before following the plan.** The plan's dominant risk may have expired: a cutover runbook built around in-flight-run safety was executed in a window where in-flight = 0 because the scheduler had been off for a day — discovered, not scheduled. Conversely a mid-sequence surprise (the fail-closed build deployed *before* its data migration, refusing readiness for 28h) can be benign, self-announcing state rather than an incident — a fail-closed design makes deploy-order mistakes survivable, which is part of why you build them.
- Execute gate by gate, asserting each postcondition in a *separate statement* (data-modifying-CTE snapshots lie about their own effects), recording preflight numbers before the change and comparing after.
- End with the Law 3d ladder: live traffic through the new path, source frozen, and an audit row recording what was done and why.
- Restore ambient state you changed for the probe (re-disable the job you enabled), and say so.

## Multi-Agent Git Mechanics (macOS/FUSE-mounted repos especially)

- One worktree per agent; the shared checkout is contended and mounts may block `unlink` (stale `.git/*.lock`: delete the specific lock, retry once). On some FUSE mounts *any* index-touching git command — including `git status` — leaves an undeletable `index.lock`; use `find`/`ls`/`diff` for state and let the operator own every git invocation there.
- Stage explicitly per path — never `git add -A` in a shared tree.
- Rescue stranded commits via `git bundle`; verify the ref updated.
- Committing into a device-bridge/FUSE-mounted repo: mind the two-path namespace (mount path for the shell vs raw device path for file-transfer tools), per-repo git identity, scoped lock-sweeps that don't turn `refs/heads/*.lock` into broken refs, push-is-deploy handoffs, and verify-the-exact-SHA closes.
- After every wave: remove ALL worktrees including QA's, `git worktree prune`, shared checkout back to trunk, `git status` clean.
- Reconcile claims vs repo truth for every report: branch exists, tip matches, file list matches, protected paths untouched.

## Orchestrator-Performed Edits

Trivial mechanical changes are fine to self-perform — held to the pipeline's standard. Grep the whole tree for the old token after a rename; mark orchestrator-made commits as such so the next gate treats them with the same suspicion as agent work.

## Triage Before New Slices

When gates disagree or tests loop: stop generating slices, isolate the failing layer (static/config → runtime health → task delivery → tool lifecycle → canonical audit evidence → semantic response → gate truth → release decision), patch only the proven-defective layer. Cheap canonical evidence beats a rerun.

## Holdout / Eval Hygiene

Fresh-context grader, zero implementation context; orchestrator and producers never see scenario contents; results-only commits; scores back, never cases. Honor a NO-GO by filing remediation. What a reviewer actually grades may be a *docstring* — dead governance code with a confident docstring is what anchors them.

## Board / Tracker Discipline

- In Progress at dispatch; evidence comment + state change at completion; status update at wave end.
- File incidental findings as issues at the moment of discovery; batch minor ones into a themed issue.
- Evidence comments record what was *attacked and held*, what remains unverified, and refutations (Law 9) so disproved findings don't resurface.
- Operator-only actions become dedicated issues with exact steps. Placeholders get pasted literally once. No inline `#` comments in zsh paste-blocks. Credentials that travel SQL→URL→shell must be alphanumeric; test them at a psql prompt before they enter a URL.

## Reporting Format

1. **Current Verdict** — what is true now. 2. **Evidence** — commands, reports, gates, ids. 3. **Slices** — prompts / ownership matrix. 4. **Dependencies** — parallel vs sequential. 5. **Risks** — misreports, stale evidence, shared-file conflicts. 6. **Next Action** — the smallest useful move.

## Anti-Patterns

- More agents to compensate for unclear root cause.
- Two agents writing one shared file in the same wave.
- Accepting screenshots/agent comments without corroboration when release truth matters.
- Re-running expensive live tests before checking whether the last run already contains proof.
- Mixing runtime fixes, gate-truth fixes, docs, and release commits without naming scope.
- Burying "remaining defect" under a green headline — or a green system under an un-actioned defect list.
- Destructive action on an unverified orchestrator premise (Law 1) — or a fix built on an unreproduced QA premise (Law 9).
- Declaring done on a green suite when the production-touching artifact has never executed (Law 8).
- Executing a runbook against the state it was written for instead of the state that exists (Operator-Runbook rule 1).
- Publishing a staged skill copy without checking it against BOTH the registry tip and the account store (see 2026-08-08c).

## Self-Improvement Loop (mandatory — this is what keeps the skill alive)

**Every orchestration run ends with a retro that patches THIS skill.** Not optional — every run:

1. Ask: What moved the project? Which slices mis-scoped? Which reports/gates misled — including QA's? What did the environment do that code-reading couldn't predict? Did the orchestrator err, and would a written rule have prevented it?
2. Distill at most 1–3 crisp additions. If nothing genuinely new was learned, append only a changelog line saying so — resist ritual bloat.
3. **Patch this skill via the skill-publish gate** — never write the registry directly. Append a dated Changelog entry, stage the updated skill dir to `~/Cortana/cortana-vault/_inbox/skills/orchestration/`, and hand the operator `~/Cortana/cortana-skill-registry/bin/publish-skill.sh orchestration`. Persist the same content to the account store (save the skill in-session, or deliver a `.skill` file). Before staging, diff against the registry TIP and the loaded copy — a stale staged dir published over a newer registry is a regression (2026-08-08c).
4. Prune: fold never-fired or superseded rules into tighter laws; note consolidations. Sharper, not longer.

## Eval-Wave Rules (blind identification / grading waves)

- **The blind spec is itself a gate artifact — version it.** A transcription ambiguity in the orchestrator's sanitized spec (a candle-count/clock contradiction) suppressed calls two agents demonstrably saw; patch + bump the version the moment a wave exposes the defect (don't let a known-bad gate keep firing), and record which agents ran on which version.
- **Instruct agents to record suppressed candidates in notes.** Signals seen-but-vetoed become recoverable adjudication evidence; without them a spec defect is indistinguishable from agent blindness.
- **Rotate or overlap day/case blocks across agents.** A 0/4 block score is confounded with block difficulty unless another agent sees the same block; rotation is the load-bearing control for any re-test.
- **QA must not certify recoveries it adjudicated past a threshold.** A verdict that crosses the gate only via its own adjudication is a re-test trigger, not a pass.

## Changelog

- **2026-08-08c · Lineage merge (this revision).** The skill had forked three ways: the account/loaded copy carried Laws 7–9 (compressed), Operator-Runbook Execution, and Eval-Wave Rules; the registry carried the 07-28 BT Journal entry, the WaiveBoard deploy entry, and updated slice-templates; a stale staged dir (from 08-04) was then published over the newer registry tip, regressing it. This revision is the verified superset of all three. New rule (folded into Self-Improvement step 3 and Anti-Patterns): **a staged skill dir is itself a premise — before publishing, diff staging against the registry TIP and the loaded/account copy; check-drift is three-way, not two-way.**
- **2026-08-08b · P1 vault remediation wave (4 parallel dev + QA; all slices first-gate PASS).** Learnings: (1) **Content-vault waves parallelize on path ownership alone** — no worktrees needed when slices are disjoint by directory and nobody commits; the QA gate's ownership-matrix check (every modified path maps to exactly one slice) is the load-bearing control. (2) **Read-path indexes double as drift detectors** — the act of enumerating a folder against its hub exposed a same-morning exporter/hub divergence no one was looking for; indexes are cheap sensors, not just navigation. (3) **Name cross-deliverable interactions at dispatch:** a staleness sweep that deliberately preserves `updated:` and a sync script that rewrites `updated:` from mtime are mutually clobbering if applied in the same wave — the dev agent caught it and the apply was deferred; check each slice's postconditions against every OTHER slice's planned side effects before running batch normalizers.
- **2026-08-08 · P0 vault remediation wave (2 dev + 1 QA + orchestrator runbook).** Learnings: (1) **Law 7 mechanism catalogued: a bash heredoc clobbers piped stdin** — the orchestrator's own pre-commit YAML guard read `''` from stdin and passed everything while its sibling guards worked; per-guard poison probes (QA testing each guard in isolation) caught what a single combined probe would have missed. Guards written and tested by the same party stay vacuous. (2) **Cowork sandbox silently blocks `unlink`** until `allow_cowork_file_delete` is granted — git init half-fails with stale index.lock + thousands of tmp objects; the clean recovery is delete-permission → `rm -rf .git` → re-init, not lock surgery. (3) "Recoverable via baseline commit" is a *claim requiring the file be tracked* — a path gitignored before the baseline is not in the baseline; verify with `git ls-tree` before promising recoverability of a planned deletion (Law 1 corollary).
- **2026-08-07 · Obsidian multi-agent vault research wave (4 Firecrawl research agents + 1 Explore auditor, fully parallel).** Learnings: (1) **Law 1 applies to audits, not just destructive acts** — the vault auditor's first pass computed a 5× wrong broken-link rate by trusting the vault's own SCHEMA.md for the root path; it self-corrected only by re-deriving the premise from live config (`.obsidian` mtimes). Rule: an audit's frame-of-reference (roots, scopes, exclusion lists) must be discovered from live state, never from the subject's documentation. (2) **Research slices partition cleanly by question-domain with explicit NO-GO topics** — zero overlap across 4 agents on adjacent subject matter; the "suppressed candidates" report section (from Eval-Wave Rules) transferred well to research waves as adjudication evidence. (3) Load-bearing external claims that post-date orchestrator knowledge (here: Obsidian CLI) get one primary-source re-verification by the orchestrator before entering the deliverable — cheap, and it upgraded a hearsay-grade claim to verified.
- **2026-08-06 · NYO EOB Phase-1 blind identification wave (4 Opus identifiers + QA over TradingView MCP).** Added Eval-Wave Rules. Key learnings: spec-authoring defects dominated agent error 9-to-2 in adjudication; agent-recorded suppressed candidates recovered 3 matches; a Saturday phantom row in the label DB proved no-trade labels are absence-of-log artifacts (labels need positive confirmation); TV MCP scroll/screenshot APIs broke and ui_evaluate data-first extraction outperformed vision anyway.
- **2026-07-30 · MetaCortex WAI-124 cutover (operator-gated runbook, orchestrator-executed).** Added the **Operator-Runbook Execution** section and **Law 3d** (the postcondition ladder for data migrations: structural parity → copy-count identity → live-run probe with source frozen). Key learnings: discover live state before following the plan — the runbook's dominant risk (in-flight HITL orphaning) had expired (0 in-flight, scheduler off), making the window ideal rather than risky; a fail-closed build deployed ahead of its data migration refused readiness for 28h *harming nothing* — deploy-order mistakes are survivable precisely because the design fails closed; the scheduler hydrates jobs at boot, so enabling a job requires a restart to take effect. Execution: 268/318/863 rows copied with all gates green, probe run succeeded with checkpoints in the workspace schema and source frozen — the WAI-124 saga (discovered Jul 29 by QA overturning an archive premise, fixed through 2 gates + mutation rounds, cut over Jul 30) closed end to end.
- **2026-07-29d · WaiveBoard WAI-133 langgraph SOW-parse/triage — QA re-gate + dual-repo deploy** *(relabeled from 07-29c during the 2026-08-08 lineage merge; the account lineage used 07-29c for WAI-125/126/127).* No new Law; sharpened two. Extended **Law 1** with the handoff-summary-is-an-unverified-premise corollary — a resumed summary claimed "merged to main" while the working checkout sat on a stale `main` with the target file absent. Added the **device-bridge/FUSE commit** subsection (two-path namespace, per-repo identity, scoped lock-sweeps, push-is-deploy, verify-the-exact-SHA). Confirmed a Law-2/4 habit paid: verified two new deps were *declared in the manifest*, not merely imported, before calling a deploy ready. Scoreboard: 4 security holes (SSRF, DoS cap, magic-byte routing, token leak) closed with negative-controlled tests + 0 mutation survivors; both deploys verified live against exact SHAs; 2 incidental findings filed; 1 handoff-premise error caught before a bad commit.
- **2026-07-29c · WAI-125/126/127 wave.** Law 9 (reproduce QA findings — measurement method is part of the claim); Law 3 staleness, Law 4 value-laundering, Law 7 poison-positioning, Law 8 over-harvest controls; brief properties not prescriptions; micro-rounds; QA-recommended redesigns can dissolve findings four at a time. Stale-venv trap caught the orchestrator. Scoreboard: 1 unauthenticated-wedge caught pre-merge, 1 QA finding refuted, 11 evasion spellings closed, 3 vacuous guards replaced.
- **2026-07-29b · MetaCortex WAI-124/WAI-123 wave.** Laws 7–8 (original incidents: whole-artifact greps pin nothing — the re-key assertion satisfied by sibling sections, recurring one granularity down after the fix; 22 mutations → 7 survivors → 10 more, incl. a tautology-rewritable verification gate); Orchestrator-Performed Edits (a self-made rename left seven stale references QA caught); pipeline hardening (assert package resolution before trusting suite counts; STOP at ownership boundaries; behavioural smoke; sweep all worktrees incl. QA's; merge order that never leaves trunk self-inconsistent). Scoreboard: 1 blocking defect caught by QA, 1 more by the fix round, 17 guard gaps closed by mutation, 3 orchestrator briefing errors corrected by dev agents.
- **2026-07-29a · MetaCortex build cycle (6 orchestrations).** Laws 1–6; Dev→QA pipeline; git mechanics; holdout hygiene; board discipline; this loop. Scoreboard: ~10 would-be production defects caught pre-merge, 2 post-deploy by live evidence, 1 orchestrator error caught by QA.
- **2026-07-29 · skill-publish gate adopted.** Registry writes flow through the staged publish process (`_inbox/skills/<name>/` → `bin/publish-skill.sh`, operator diff+confirm), converging the disk registry, account store, and staging copy that had drifted three ways.
- **2026-07-28 · BT Journal agent-registry wave (3 agents parallel: 2 dev + 1 QA-concurrent).** Two additions earned. **(a) Run QA CONCURRENTLY with dev when its mandate is read-only and its scope is the untouched remainder of the repo** — the audit found a P0 (wildcard CORS + zero auth → proven journal read + API-key exfiltration chain, reproduced on the operator's exact pinned FastAPI) while feature slices were still being written, so the fix shipped inside the same wave. Enforce with a written "you may not modify a single line of code" clause. **(b) When two slices build against one contract in parallel, gate the SEAM explicitly**: diff the keys the backend actually emits against the fields the frontend actually reads, and hand-check any field one side derives rather than receives. **Environment:** on a FUSE-mounted repo, *any* index-touching git command — including `git status` — can leave an undeletable `.git/index.lock`; use `find`/`ls`/`diff` for state and let the operator own git invocations there.
