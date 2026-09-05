# Share the Cortana skills registry across harnesses

The registry owns `skills/<id>/SKILL.md`. Local harnesses discover that same source through symlinked skill folders. Existing package edits are visible through the links; new or retired IDs need synchronization. Restart a harness session if its index is cached.

## Local commands

Run from this clone:

```bash
./sync-skills.sh check
./sync-skills.sh plan
./sync-skills.sh sync
```

No argument means `sync`. `check` is read-only and exits 1 for drift, 2 for invalid configuration or operational errors. Sync preserves replaced entries in trash outside skill discovery, records restoration paths, and verifies the result. Native-only skills and system folders remain. It never publishes skills or pushes git.

The implementation is `bin/sync-harnesses.py` (Python 3.9+). Configuration is `~/.config/cortana/skill-harnesses.json`; receipts are `~/.config/cortana/receipts/`. The default targets are `~/.claude/skills`, `~/.codex/skills`, and `~/.hermes/skills`. `--config PATH` selects another config. Explicit `CANONICAL` and `<HARNESS>_SKILLS` environment overrides remain supported for one invocation; an empty harness override skips it.

A whole-root symlink to this clone's `skills/` is recognized as already synchronized. Per-package links let native/system skills coexist. When a native category shares a registry skill ID, its contents remain and the registry package uses `_cortana-registry/<id>` within the discovery tree. Backups must never live inside a harness skill-discovery directory.

## Register another harness

Confirm its real discovery path and support for symlinked `SKILL.md` folders, then:

```bash
./sync-skills.sh add my-agent "$HOME/.my-agent/skills"
./sync-skills.sh plan
./sync-skills.sh sync
./sync-skills.sh check
```

The path above is an example. Registration only writes configuration; review the plan before applying it. Same-ID native packages are preserved in trash and replaced with canonical links. Nested local-only subskills may require explicit reconciliation. Native libraries with different IDs remain available.

If a harness offers an external skills-root setting, point it to this clone's **`skills/`**, not the repository root, and verify precedence against local/project copies. Merely mentioning a path in a prompt does not enable discovery. A harness that does not follow links needs its supported root setting or a tested export adapter.

Current Codex documentation uses `~/.agents/skills` for user skills and supports symlinked folders. The installed desktop app also exposes legacy `.codex` paths. Verify your runtime; do not mirror the entire registry into both directories by default. Preserve `.codex/skills/.system` and reconcile any existing `.agents` duplicates first. [Official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills)

The September 5 distribution repairs are versioned with this registry. Other machines need their own registry clone/configuration. Containers need a reachable mount. Local links do not publish to Claude account/Cowork cloud stores or company mirrors.

## Hooks and publication

This local clone already has `core.hooksPath=hooks`. Merge, checkout, rewrite and commit hooks invoke `_resync`, which reads the registered harnesses dynamically. Failures now surface with a pointer to `.sync.log`. A new clone does not inherit local git configuration; inspect and preserve any pre-commit/custom hook chain before integrating these hooks. Manual `sync` after pulling is always available.

**The `post-commit` hook also runs `bin/sync-downstream.sh`, which pushes origin and synchronizes/commits/pushes the WaiveLabs mirror.** It exports committed `HEAD`, refuses a dirty mirror, moves changed/stale paths to external trash with restoration receipts, and copies without deletion. For an authorized batch, set `CORTANA_DEFER_DOWNSTREAM=1` while running the publisher, then run `bin/sync-downstream.sh` once afterward. Local link sync and validation hooks still run on each commit. `SKILL_MIRROR` selects a clean mirror clone for one run; `git config cortana.skillMirror /absolute/path` persists that selection for this registry clone. This machine uses `~/.local/share/cortana/mirrors/waivelabs-agent-skills`, preserving the unrelated work in the old project checkout. Failures return nonzero and are recorded in `.sync-state`; a failed mirror commit never triggers a mirror push. Without deferral, omitting `--push` does not prevent publication through the commit hook. Obtain applicable publication authorization; retain validation hooks. The local sync command has no remote side effects.

Skill changes stage in `../cortana-vault/_inbox/skills/<id>/` for operator-authorized publication. Do not edit a harness symlink as if it were a private copy: it writes the registry source. Use the reviewed publisher, preserve unrelated dirty work, record published revisions, and refresh the Cortana skill catalog after publication. The September 5 batch of 28 refinements was approved and published through the overlay publisher; archived stage copies and exact commit/hash receipts are retained in Cortana.

The legacy `bin/check-drift.sh` compares a narrower normalized inventory and can pass when only entries are missing. Use the new `check` for local harness drift; validate manifest YAML and invocation behavior separately.

## Agent routing and recovery

Cortana's current groups, typed relationships, selection rules, and publication evidence are in:

- `../cortana-vault/projects/claude-skills/claude-skills--skills-registry.md`
- `../cortana-vault/projects/claude-skills/claude-skills--agent-skill-routing.md`
- `../cortana-vault/projects/claude-skills/claude-skills--harness-distribution.md`

Give new harnesses these persistent instruction pointers. Load one primary workflow and relevant support, not every skill. Stage skill edits; keep brand authority and project memory in Cortana.

For rollback, inspect a receipt's `path`, `restore_from` and action state. Preserve newer content, move replacement links to fresh trash, then restore recorded originals. An interrupted receipt requires comparing disk with its completed/pending actions. Never delete native or system skills to make the inventory agree.
