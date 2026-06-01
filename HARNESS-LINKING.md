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

**Hermes / Paperclip** — Hermes agents run inside the Paperclip container and load
skills via Paperclip's standard discovery from a **read-only mount** of the
registry (the model the registry README already documents). In your
`docker-compose.yml` / container config, mount the canonical clone's `skills/`
read-only at the path Paperclip scans, e.g.:

```yaml
    volumes:
      - ~/Cortana/cortana-skill-registry/skills:/runtime/paperclip/skills:ro
```

Hermes contributes no distinct skill content of its own, so "linking Hermes" just
means making this shared registry the source its agents read.

## Running the helper

`link-harnesses.sh` automates the two symlinks (it backs up any existing skills
dir to `<dir>.bak-<timestamp>` first, and is safe to re-run):

```bash
# clone first run:
REPO_URL=git@github.com:<you>/cortana-skill-registry.git ./link-harnesses.sh
# subsequent runs (clone already present):
./link-harnesses.sh
```

Override any path inline, e.g. `CODEX_SKILLS=~/dev/.codex/skills ./link-harnesses.sh`.

## Updating skills later

1. Edit / add skills in the canonical clone (`~/Cortana/cortana-skill-registry`).
2. `git add -A && git commit && git push`.
3. On any other machine: `git -C ~/Cortana/cortana-skill-registry pull`.

All linked harnesses pick up the change automatically (symlinks) or on next
container restart (read-only mount).
