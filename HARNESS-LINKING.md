# Harness Linking

How the three Cortana agent harnesses (Codex, Claude/Cowork, Hermes) consume the
consolidated skill registry.

## Recommended model: one canonical clone + per-harness symlink

```
                 GitHub (private)
          cortana-skill-registry.git
                      │  git pull
                      ▼
   ~/Cortana/cortana-skill-registry/        ← single canonical clone (source of truth)
                      │ skills/
        ┌─────────────┼──────────────────────────┐
   symlink        symlink                    read-only mount
        ▼             ▼                            ▼
 ~/.codex/skills  ~/.claude/skills      Paperclip container :/runtime/skills (Hermes + Codex agents)
```

Why this model (vs git submodules or N independent clones):

- **Single source of truth.** Edit a skill once in the canonical clone; every
  harness sees it immediately — no per-harness copy to keep in sync.
- **One update command.** `git -C ~/Cortana/cortana-skill-registry pull` refreshes
  all harnesses at once.
- **No submodule bookkeeping.** Submodules pin a commit per consumer and need
  `submodule update --remote` everywhere; that's the right tool only if you want
  different harnesses on *different* skill versions. You want consolidation, so a
  shared symlink target is simpler and matches the registry's existing
  read-only-mount design (STEP-48).

## Per-harness wiring

**Codex** — Codex discovers skills under its home `skills/` directory. Point that
at the canonical clone:

```bash
ln -s ~/Cortana/cortana-skill-registry/skills ~/.codex/skills
```

(If your Codex home is elsewhere, set `CODEX_SKILLS` when running
`link-harnesses.sh`.)

**Claude / Cowork** — Claude Code/Cowork discovers skills under `~/.claude/skills`:

```bash
ln -s ~/Cortana/cortana-skill-registry/skills ~/.claude/skills
```

**Hermes / Paperclip** — Hermes (and the in-container Codex/Claude adapters) run
inside the Paperclip container, which provisions skills through Paperclip's own
**company-skills import surface**, keyed by this repo's GitHub URL — this is the
platform-native path the registry README documents, and the reason the GitHub
push must happen first. After the repo is pushed:

```bash
# Import the registry into the Cortana Paperclip company by GitHub URL:
COMPANY_ID=<your-cortana-company-id>
curl -X POST "http://localhost:${PAPERCLIP_PORT:-4201}/api/companies/$COMPANY_ID/skills/import" \
  -H 'Content-Type: application/json' \
  -d '{"source":"https://github.com/<you>/cortana-skill-registry"}'
# Then assign to an agent (or set desiredSkills at hire):
curl -X POST "http://localhost:${PAPERCLIP_PORT:-4201}/api/agents/<agent-id>/skills/sync"
```

Alternatively, for a quick read-only bind (bypasses the import surface), add a
volume to the `paperclip` service in `platform-v2/docker-compose.yml` pointing at
each adapter home's skills dir, e.g.
`- /Users/nolan/Cortana/cortana-skill-registry/skills:/state/codex-home/skills:ro`
(repeat for `/state/claude-home/skills` and `/state/hermes-home/skills`). Prefer
the import API — the bind can collide with Paperclip's per-company materialization.

Hermes contributes no distinct skill content of its own, so "linking Hermes" just
means making this shared registry the source its agents read.

## Running the helper

`sync-skills.sh` wires all three harnesses and installs the git hooks. It is
idempotent and safe to re-run; it backs up any real skill dirs it replaces.

```bash
cd ~/Cortana/cortana-skill-registry
./sync-skills.sh
```

It uses these defaults (override any inline, e.g.
`HERMES_SKILLS=/Volumes/symba/.hermes/skills ./sync-skills.sh`):

- `CODEX_SKILLS`  = `~/.codex/skills`            (MIRROR)
- `CLAUDE_SKILLS` = `~/.claude/skills`           (MIRROR)
- `HERMES_SKILLS` = `/Volumes/symba/.hermes/skills` (FILL) — falls back to `~/.hermes/skills`

**MIRROR** (Codex, Claude): every registry skill becomes a per-skill symlink;
real dirs are backed up to `<skills>/.pre-consolidation-backup-<ts>`; harness
internals (`.system`, `codex-primary-runtime`, etc.) are left alone.

**FILL** (Hermes): only adds top-level symlinks for registry skills Hermes
doesn't already have (nested ones counted), so Hermes's curator-managed library
and category layout stay intact. Its native skills remain curator-owned; the
cross-harness shared set is mirrored in alongside them.

## Auto-sync (how "sync on every change" works)

1. **Editing an existing shared skill** → propagates instantly. Codex/Claude
   read through symlinks; Hermes too for the filled-in shared skills. No step.
2. **Adding/removing skills** → the installed git hooks (`post-merge`,
   `post-checkout`, `post-commit`, `post-rewrite`, under `hooks/`, wired via
   `core.hooksPath`) re-run `sync-skills.sh` automatically on every commit and
   every `git pull`, so new skills get linked into all harnesses with no manual
   step. (Output is appended to `.sync.log`.)
3. **Across machines** → `git pull` triggers the hook → all harnesses resync.

### Optional: true file-watch auto-commit

The hooks resync on git events. If you also want a *local edit* to auto-commit
and push (so other machines pick it up without you running git), add a watcher:

```bash
brew install fswatch
fswatch -o ~/Cortana/cortana-skill-registry/skills | while read; do
  git -C ~/Cortana/cortana-skill-registry add -A \
  && git -C ~/Cortana/cortana-skill-registry commit -m "auto: skill change $(date)" \
  && git -C ~/Cortana/cortana-skill-registry push
done
```

Wrap that in a launchd agent to run at login if you want it always on. (Left
opt-in — auto-push is a standing automation you should enable deliberately.)

## Updating skills later

1. Edit / add skills in the canonical clone (`~/Cortana/cortana-skill-registry`).
2. `git add -A && git commit && git push` — the `post-commit` hook resyncs.
3. On any other machine: `git pull` — the `post-merge` hook resyncs there.
