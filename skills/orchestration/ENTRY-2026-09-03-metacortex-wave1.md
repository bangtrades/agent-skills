# ENTRY 2026-09-03 — MetaCortex factory wave 1 (lineage-safe copy of the changelog entry)

Appended to the STAGED `SKILL.md` in this directory (which was newer than the session's loaded copy — 09-01, 08-31, 08-30b entries present here, absent there). **HOLD-2026-08-29 remains in force: do not publish.** This file exists so the entry survives even if the staged SKILL.md is overwritten by another session before the DetailAI-lineage merge.

## Additions

**(a) Law 1, third corollary — your own prior audit is a handoff summary.** Re-derive it from live git before dispatching against it. The 08-31 audit read a commit message's "(governance PR, branch-only)" as *unmerged* and planned a runbook step to write a PR that had landed four days earlier. `git merge-base --is-ancestor 74aec34 HEAD` refuted it in one line before any agent was briefed. A commit message is a claim about intent; ancestry is the evidence.

**(b) Classify a baseline failure as code-vs-environment from the traceback's last frame before recording it.** Two "pre-existing failures" were `PermissionError: unlink` from tests that snapshot→mutate→restore a source module; the FUSE mount refused the cleanup. Granting delete permission turned both green — true baseline was zero failures. Dangerous because they were `*_guard_is_load_bearing` tests: an environment red masks whether a real guard regression would show. They also leave `.orig-snapshot` residue in the source tree that `git add -A` would commit.

**(c) The permission classifier refusing a production write is a boundary, not a bug.** Railway `set-variables` / `update-service` were denied by auto-mode. Correct move: a paste-ready operator block via `send_user_message`, then continue every slice that did not depend on it (all of them). Do not reach for alternative write paths.

## Reconfirmed
- Catalog over instance: QA found 3 hardcoded-lane sites where the dev reported 1.
- A dev's "1 pre-existing EPERM failure" was refuted by the gate as a silently self-skipping *security* test; now fail-loud under `MC_SEAM_TEST_REQUIRED=1`.
- `uv python install 3.12` + hash-locked install = real interpreter for agents in <2 min; without it every "suite green" is unverifiable.
- `SendMessage` unavailable → fresh-agent micro-rounds with findings verbatim.
- FUSE mount: `git checkout -b` / explicit `git add` / `commit` all fine once delete permission cleared `index.lock`; no push creds → operator pushes. Never re-emit large source through your own output to `push_files`.

## Scoreboard
3 Opus dev slices · 1 Opus adversarial gate · 2 Opus micro-rounds · 2 orchestrator one-line edits. MetaCortex 4795→4821 green, ruff clean. WaiveBoard 433→436 green, tsc clean. 0 ownership violations. 3 guards proven non-vacuous by removal. 15 envelope attacks against the real Python verifier. 1 premise refuted before dispatch (a), 2 dev claims refuted by QA, 2 P2s fixed in micro-rounds, 1 P3 class filed (WAI-557). Branches: `claude/wai-497-498-499-factory-lane` @ a59d0cd, `claude/wai-487-seed-addendum` @ 75302bd (metacortex); `claude/wai-501-factory-exchange` @ a0f8e26 (waiveboard).
