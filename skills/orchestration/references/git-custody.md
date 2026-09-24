# Git Custody

Read only the relevant section. The entrypoint controls execution budgets, context renewal and dispatch; this reference preserves detailed verification rules.

## Multi-Agent Git Mechanics (macOS/FUSE-mounted repos especially)

- **In multi-worktree waves sharing one `.git`, agents NEVER use `git stash` and NEVER run `git worktree prune` — put both bans verbatim in every dev AND QA brief.** `refs/stash` is a single shared ref: two agents stashing concurrently cross-talked and momentarily reverted a third's tracked-file edits (2026-08-28). And a prune executed from a sandbox that cannot see host-side worktree paths deregisters ALL of them — one QA prune silently deregistered ~26 host worktrees (files intact; recovery `git worktree repair <paths>` on the host). Corollary: **a standing operator rule that lives only in the orchestrator's head does not bind agents** — the orchestrator knew the no-bare-prune rule and omitted it from the QA brief; transcribing every known landmine into each brief is part of dispatch, not optional context.
- One worktree per agent; the shared checkout is contended and mounts may block `unlink` (stale `.git/*.lock`: delete the specific lock, retry once). On some FUSE mounts *any* index-touching git command — including `git status` — leaves an undeletable `index.lock`; use `find`/`ls`/`diff` for state and let the operator own every git invocation there.
- Stage explicitly per path — never `git add -A` in a shared tree.
- Rescue stranded commits via `git bundle`; verify the ref updated.
- Committing into a device-bridge/FUSE-mounted repo: mind the two-path namespace (mount path for the shell vs raw device path for file-transfer tools), per-repo git identity, scoped lock-sweeps that don't turn `refs/heads/*.lock` into broken refs, push-is-deploy handoffs, and verify-the-exact-SHA closes.
- At completed closeout, remove only disposable worktrees whose useful work is committed and retained elsewhere, via an explicitly named `git worktree remove`. Preserve unfinished, dirty, interrupted and user-owned worktrees and the original checkout. Never force cleanup to obtain a clean status; never prune. Persist useful probe suites before retiring scratch branches.
- Reconcile claims vs repo truth for every report: branch exists, tip matches, file list matches, protected paths untouched.

