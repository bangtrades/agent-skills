---
name: "orchestration"
description: "Coordinate complex software work across multiple agents — plan disjoint slices, dispatch dev agents, run adversarial QA gates, verify all claims against evidence, and manage tracker/board state. Trigger on \"orchestrate agents\", \"dispatch agents\", \"run the sprint\", \"coordinate a build\", \"agent slices\", multi-agent dev work, or any request to plan/execute/verify parallel engineering work. Self-improving: every orchestration run ends by reviewing and patching this skill."
---

# Orchestration

Coordinate complex software work across multiple agents, contributors, or implementation slices. Convert messy project state into clear parallel work, truth-based reporting, and a release path that never confuses activity with progress.

Project-agnostic: discover the repository, sprint plan, local instructions, test gates, tracker conventions, and report formats from the active working context.

## Core Rule

**Orchestrate from evidence, not optimism — and that includes your own claims.** A slice is complete when code, tests, gates, logs, tracker state, or an explicit operator result prove it against acceptance criteria. An orchestrator's diagnosis is a *claim* like any other: before any destructive or irreversible action, the premise itself must be independently verified (see Law 1).

## The Laws (earned in production — each one cost something)

**Law 1 — The orchestrator is fallible; verify premises before destructive acts.**
Incident: an orchestrator concluded live checkpoint tables were "inert" from `max(thread_id)` over a *text* UUID column — a lexicographic max that says nothing about recency — and queued an archive that would have destroyed running production state. An independent QA agent overturned the premise minutes before execution. Rule: any archive/drop/migration/teardown gets its *premise* re-derived by an agent who didn't form it, from raw evidence. Prefer reversible forms (rename/archive-schema over drop; disable over delete) even after verification. Corollary — **a compaction/handoff summary is a premise, not ground truth.** In the WAI-133 deploy a resumed summary asserted "merged to main; working checkout on branch X"; live `git` showed the checkout on a *stale* `main` (behind `origin/main`) with the target file absent. Before committing on top of a ref, re-derive from `git rev-parse origin/main` + `git merge-base --is-ancestor` which SHA is actually the deploy trunk and whether your branch fast-forwards it — never from the narrative you were handed.

**Law 2 — The environment silently discards configuration; verify guarantees empirically, never structurally.**
Incidents: a connection pooler (Supavisor) silently dropped `options=-csearch_path=...` startup parameters, rendering a schema-isolation control inert while every health check stayed green; `uv pip compile` preserves existing pins when the output file exists and fresh-resolves when it doesn't, making a CI freshness check pass or fail depending on output path; GitHub's `required_approving_review_count: 0` silently disables the code-owner review machinery a rule appears to enable. Rule: any guarantee mediated by infrastructure (poolers, CI runners, platform APIs, package managers, branch protection) must be proven by observing the *live effect* (query `pg_stat_activity`, run the negative test, trip the gate), not by reading the config that requests it. Corollary — the fix must be at a layer the environment cannot drop: replacing a *startup parameter* with an in-session statement worked precisely because a pooler can discard the former and not the latter.

**Law 3 — Success output must assert the postcondition, not completion.**
Incident: a deploy-prep script printed two success lines while its `setup()` no-op'd against the wrong schema — the operator had no way to know. Rule: every script/gate/probe that reports success must verify the *resolved state* (e.g. `to_regclass` in the bound schema, row landed, ref updated) and fail closed otherwise. A readiness probe that checks "a table with this name is readable" cannot distinguish success from fallback. Extension (Law 3b): a readiness value computed once at boot is a snapshot, not a check — a control that cannot go un-ready cannot detect drift.

**Law 4 — Fake-fidelity: every external-SDK seam needs one test against the real client.**
Incident: an agent added a `usage` kwarg asserted by 19 tests — all of which faked the client one level below the seam; the real SDK's method had no such parameter and every live model call crashed. Rule: for each external dependency seam, require one test that constructs the REAL pinned client (offline construction is usually free) through the production code path. QA must probe whether fakes are more permissive than the real dependency. Watch the *shape* too: a dev's own real-client test initially fed a `ChatResult` where production delivers an `LLMResult`, and the recorder silently degraded to a zero row.

**Law 5 — Deterministic gates before subjective judgment.**
In product code: hard-loss pre-checks run before the LLM reviewer, and no model opinion can override them. In orchestration: run the cheap deterministic checks first — per-branch file lists, pairwise overlap (must be empty), parent SHAs, byte-identical merge order, protected paths untouched, lock freshness — before any subjective code review. Also watch for judge anchoring: a reviewer that returns the same passing score on every artifact is not discriminating.

**Law 6 — Pin the toolchain; CI installs what production installs.**
Incidents: floating `ruff>=` broke CI on every push when a new ruff shipped; floating `mcp>=1` broke collection when 2.0 relocated a module — while production stayed green because it installed from the hash-pinned lock. Rule: exact-pin dev tools, semver-guard runtime deps, and make CI consume the same lock artifact production consumes. A verification gate that floats its own tooling generates false alarms that train people to ignore it.

**Law 7 — A test that greps the whole artifact pins nothing. Scope assertions to the block that must carry the property.**
Incident: a data-migration test asserted a canonical-key expression appeared in the file. That same expression also appeared in the preflight and verification sections, so the assertion held even when the *copy* statement didn't re-key at all — the single highest-consequence failure that migration could have. The fix (per-statement parsing) was then applied to §3 and *not* to §4, where the identical defect immediately recurred: a verification rewritten to query the SOURCE table still passed because a sibling sub-block contained the grepped string. Rule: assert against the parsed sub-block, not the document. And when you fix this class of defect in one place, sweep every sibling — it recurs at the next granularity down.

**Law 8 — Mutation-test the guards on anything that will touch production data.**
For unexecutable artifacts (SQL migrations, IaC, deploy scripts) the tests are the only guard, and they are usually weaker than they read. Run a mutation battery: break the property, confirm the suite fails, revert. On one migration, 22 mutations left 7 survivors; closing those and hunting further surfaced 10 more, including a verification gate that could be rewritten into a tautology (`WHERE thread_id IS NOT NULL`) — reporting healthy for a run whose state was never copied, in the check that decided whether human approvals survived. Every one of those was invisible to a green suite.

## The Dev→QA Pipeline (default for any wave that writes code)

1. **Plan disjoint slices.** Ownership by file path, verified disjoint (`git show --name-only` pairwise intersection = empty). If two slices need one file, sequence them or split at hunk level. Stacked work branches from an integration base built from already-QA-passed branches.
2. **Dispatch dev agents in parallel** with self-contained prompts: context (3–6 sentences), goal, acceptance criteria, ownership paths, explicit NO-GO paths (signed/governance artifacts, holdout repos, other agents' files), safety rules, exact verify commands, report contract. **Tell agents to verify orchestrator-supplied facts rather than propagate them, and to STOP and report rather than edit across an ownership boundary.** Both behaviours pay: in one wave the devs corrected three briefing errors (a wrong module path, a file wrongly described as unmerged, a section number that didn't exist) and correctly refused two cross-boundary edits.
3. **QA gate (separate agent, fresh eyes, adversarial mandate).** Reproduce the devs' numbers independently in fresh venvs — *assert which tree the package resolves to before trusting a count*; stray venvs from earlier waves silently resolve to the shared checkout. Build a combined merge preview and run the full suite on it. Write NEW adversarial probes (never only re-run the devs' tests). Static review for swallowed exceptions, lock/contextvar hygiene, injection surfaces. Verdict per slice: PASS / FAIL with minimal repro. A FAIL blocks the wave.
4. **Fix rounds carry the QA findings verbatim** and require **negative-controlled regressions**: the dev must demonstrate each new test fails with the fix reverted. Then QA re-gates, re-running the original attack probes plus new probes against the fixes. Expect the fix round to find defects QA missed — in one wave it found an eighth broken site where QA had found six, and a later round found ten more escapes while closing seven.
5. **Orchestrator's own smoke before suggesting merges:** exercise the real public seams yourself, behaviourally, not by grep. Feed the actual defect shape through the actual code path and read the actual output. Grep-level checks confirm a fix is *present*; only execution confirms it *works*.
6. **Merge queue:** verify every branch's parent, confirm merge order produces a byte-identical tree both ways, name any new env vars or operator steps the deploy will require, and prefer the merge order that never leaves the trunk transiently self-inconsistent (land the file before the doc that references it).
7. **Persist probe suites** across gates and retire superseded probes explicitly when a contract deliberately flips.

## Multi-Agent Git Mechanics (macOS/FUSE-mounted repos especially)

- One worktree per agent (`git worktree add /tmp/<slice>-wt <branch>`); the shared checkout is contended and mounts may block `unlink` (stale `.git/*.lock`: delete the specific lock, retry once; rename-aside when delete is blocked).
- Stage explicitly per path — never `git add -A` in a shared tree.
- An agent's commit can be stranded in an ephemeral sandbox: rescue via `git bundle`, then verify the ref actually updated.
- After every wave: remove *all* worktrees including QA's, `git worktree prune`, restore the shared checkout to the trunk, verify with `git status`. Agents leave worktrees behind; sweep by listing, not by memory.
- Reconcile *claims vs repo truth* for every report: branch exists, tip SHA matches, file list matches, protected paths untouched.

### Committing into a device-bridge / FUSE-mounted repo (no network in the sandbox)
When the repo lives on the operator's machine and you reach it through a device bridge, the mechanics differ from a local checkout:
- **Two path namespaces — do not cross them.** The shell tool (`device_bash`) sees the repo under a *mount* path (`/sessions/<id>/mnt/<folder>/…`); the file-transfer/list tools (`device_commit_files`, `device_list_dir`) address the *raw device* path (`/Users/…`). A `cd /Users/…` inside `device_bash` fails with "No such file or directory". Resolve the mount base once (`ls mnt/`) and use it for every shell call.
- **Set git identity per-repo before the first commit.** The bridge shell user has no global identity, so `git commit` aborts with "unable to auto-detect email". Read the repo's own convention (`git log -1 --format='%an <%ae>'`) and `git config user.name/user.email` to match it locally.
- **The mount can't `unlink`, so every git op strands lock files.** Sweep `.git/index.lock`, `.git/HEAD.lock`, and `.git/objects/**/*.lock` aside with unique suffixes (`$RANDOM`, not a timestamp) and retry. But **scope the sweep** — a blanket `find .git -name '*.lock'` also renames `refs/heads/*.lock`, which git then reports as *broken refs*; either exclude `refs/` or clean the renamed ref-locks afterward (the operator's real machine, which *can* unlink, clears them with `git worktree prune` + `find .git/refs -name '*.stale.*' -delete`).
- **No network in the sandbox → you cannot push.** Land the commit on a branch that fast-forwards the deploy trunk (verify with `git merge-base --is-ancestor origin/main <branch>`), then hand the operator the exact `git push origin <branch>:main` — the FF push *is* the deploy trigger for auto-deploy platforms (Railway/Vercel).
- **Verify the deploy against the exact SHA, not just "green".** After the operator pushes, confirm the platform's live deployment `commitSha` equals your commit and read the runtime logs for the postcondition (module imported, server listening) — a SUCCESS badge on the wrong commit is the Law-3 trap.

## Orchestrator-Performed Edits

Trivial mechanical changes (a rename, a constant) are fine to do yourself — but hold yourself to the pipeline's standard, because nobody else will. A self-performed migration renumber updated the path constant and left seven stale references in prose and a test *name*; QA caught it, and in the merged tree that number now pointed at another slice's file. If you edit, grep the whole tree for the old token, and say in the commit that an orchestrator made it so the next gate treats it with the same suspicion as agent work.

## Triage Before New Slices

When gates disagree, tests loop, or a tool "worked" but the tracker says failed — stop generating slices and isolate the failing layer: static/config → runtime/service health → task delivery → tool execution lifecycle → canonical audit/log evidence → semantic response → gate/reporting truth → release decision. Patch only the proven-defective layer. If a verifier misreports true success, fix the verifier separately from the runtime. Cheap canonical evidence beats a rerun.

## Holdout / Eval Hygiene

The grader is a fresh-context agent with zero implementation context; the orchestrator and producing agents never see scenario contents; results are committed to the holdout repo only; the grader reports scores/verdicts, never cases. Honor a NO-GO by splitting remediation into tracked issues. Re-run the same suite after remediation for an honest close. Note what a reviewer actually grades: in one wave a middleware's *docstring* claimed a pre-call ceiling check the class never implemented — and that docstring, not any behaviour, is the likeliest thing the holdout reviewer scored.

## Board / Tracker Discipline

- Issue → In Progress at dispatch; evidence comment + state change at completion; blockers commented honestly. Project status update at wave end.
- File every incidental finding as its own issue **at the moment of discovery** — including findings that arrive as a by-product of verification. Batch genuinely-minor ones into a single themed issue rather than losing them in a report.
- Evidence comments should record what was *attacked and held*, not just what was built — the reader needs to know the guarantee was tested, and which parts remain unverified.
- Operator-only actions (secrets, signing keys, 2FA-gated changes, data-destruction sign-off) become dedicated assigned issues with exact steps. Expect a placeholder to be pasted literally once; design instructions so that failure is obvious and cheap.

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
- Declaring a wave done because the suite is green, when the artifact that will touch production has never been executed (Law 8).

## Self-Improvement Loop (mandatory — this is what keeps the skill alive)

**Every orchestration run ends with a retro that patches THIS skill.** Not optional, not "when something big happens" — every run:

1. Ask: What moved the project? Which slices were mis-scoped? Which reports/gates/logs misled? What did QA catch that the process should have caught earlier — and what did the *fix round* catch that QA missed? What did the environment do that code-reading couldn't predict? Did the orchestrator itself err, and would a written rule have prevented it?
2. Distill at most 1–3 crisp additions: a new Law (only if it generalizes beyond the incident), a checklist line, or a template refinement. Prefer one sharp rule over narrative. If nothing genuinely new was learned, append only a changelog line saying so — resist ritual bloat.
3. **Patch this skill in the registry** (save/overwrite so the update persists across sessions) and append a dated Changelog entry: date, project, what was learned, what changed. Where the registry also exists on disk and is write-protected from the session, hand the operator the publish command rather than assuming the two copies agree — they diverge silently otherwise.
4. Prune: if a rule has never fired across many runs or has been superseded, fold it into a tighter law and note the consolidation. The skill should get sharper, not longer.

## Changelog

- **2026-07-28 · BT Journal agent-registry wave (3 agents parallel: 2 dev + 1 QA-concurrent).** Two additions earned. **(a) Run QA CONCURRENTLY with dev when its mandate is read-only and its scope is the untouched remainder of the repo** — the audit found a P0 (wildcard CORS + zero auth → proven journal read + API-key exfiltration chain, reproduced by the orchestrator on the operator's exact pinned FastAPI) while the feature slices were still being written, so the fix shipped inside the same wave instead of a follow-up. Enforce it with a written "you may not modify a single line of code, findings go in the report" clause — collision risk is what usually forces QA to be sequential. **(b) When two slices build against one contract in parallel, gate the SEAM explicitly, not just each side**: diff the keys the backend actually emits against the fields the frontend actually reads (`grep` the accessors), and hand-check any field one side derives rather than receives (here the frontend synthesised `model_override` from `model_source` — correct, but invisible to a per-slice review). **Environment:** on a FUSE-mounted repo, *any* git command that touches the index — including `git status` — leaves an undeletable `.git/index.lock` that breaks the operator's next git call; use `find`/`ls`/`diff` for state and let the operator own every git invocation.

- **2026-07-29c · WaiveBoard WAI-133 langgraph SOW-parse/triage — QA re-gate + dual-repo deploy (2 repos, 4 security fixes, device-bridge commits, live deploy verify).** No new Law; sharpened two existing ones. Extended **Law 1** with the corollary that a compaction/handoff summary is itself an unverified premise — a resumed summary claimed "merged to main" while the working checkout sat on a stale `main` with the target file absent; re-deriving `origin/main` + FF relationship from live git before committing prevented a commit against a nonexistent file. Added the **"Committing into a device-bridge / FUSE-mounted repo"** subsection: the two-path-namespace gotcha (mount path for the shell vs raw device path for file-transfer tools), per-repo git identity, scoped lock-sweep that doesn't turn `refs/heads/*.lock` into broken refs, push-is-deploy handoff, and verify-the-exact-SHA close. Also confirmed a Law-2/4 habit paid: before calling a runtime deploy ready, verified the two new deps (`pypdf`, `python-docx`) were *declared in the manifest*, not merely imported. Scoreboard: 4 security holes (SSRF, 25 MB DoS cap, magic-byte type routing, token leak) closed with negative-controlled tests + 0 mutation survivors before deploy; both deploys verified live against their exact commit SHAs (Railway 7c641d2 healthy, Vercel e33130e production); 2 incidental findings filed as WAI-151/WAI-152; 1 handoff-summary premise error caught by live-git verification before it could produce a bad commit.
- **2026-07-29b · MetaCortex WAI-124/WAI-123 wave (2 dev slices, 2 QA gates, 1 FAIL, 1 fix round, 1 guard-hardening round).** Added **Law 7** (whole-artifact greps pin nothing; scope to the parsed sub-block — and sweep siblings, because the defect recurred one granularity down immediately after being fixed) and **Law 8** (mutation-test guards on anything that will touch production data: 22 mutations → 7 survivors → 10 more found while closing them, including a verification gate rewritable into a tautology). Extended Law 2 with the fix-at-an-undroppable-layer corollary, Law 3 with the boot-snapshot readiness case, Law 4 with result-shape fidelity. Added the **Orchestrator-Performed Edits** section after a self-made rename left seven stale references that QA caught. Pipeline gains: assert package resolution before trusting a suite count (stray venvs resolve to the shared checkout); brief agents to STOP at ownership boundaries (paid off twice); orchestrator smoke must be *behavioural*, not grep-level; sweep all worktrees including QA's; prefer the merge order that never leaves the trunk self-inconsistent. Scoreboard: 1 blocking defect caught by QA that would have made an operator runbook unexecutable against live data, 1 more found by the fix round that QA missed, 17 guard gaps closed by mutation testing, 3 orchestrator briefing errors corrected by dev agents, 1 orchestrator edit error caught by QA.
- **2026-07-29a · MetaCortex build cycle (6 orchestrations: deploy wave, dev wave, eval wave, security wave, 4-slice sprint w/ 3 QA gates, parked-items wave).** Major revision. Added Laws 1–6 from production incidents: orchestrator premise error nearly destroyed live checkpoint tables (1); Supavisor/uv/GitHub silently discarding configuration (2); deploy-prep success-on-no-op (3); fake-fidelity crash of every live model call (4); deterministic-gates-first + judge anchoring (5); floating-toolchain CI noise (6). Codified the Dev→QA pipeline, multi-agent git mechanics for FUSE-mounted repos, holdout hygiene, and board discipline. Replaced a stale improvement note with the mandatory persistent-registry loop. Scoreboard: ~10 would-be production defects caught pre-merge, 2 caught post-deploy by live evidence, 1 orchestrator error caught by QA.

