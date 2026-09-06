# RECOVERY — `orchestration` changelog entry dropped by the 2026-08-08c lineage merge

**Status:** open · needs operator (registry write) · found by daily vault review 2026-08-10

## What happened

The 2026-08-08c "lineage merge" published a verified superset of the three `orchestration`
forks — with one gap. The **2026-08-04 · WAI-157 universal killswitch** changelog entry was
dropped. The published/registry changelog now jumps `2026-07-30` → `2026-08-06`.

Verified 2026-08-10: the string `WAI-157` appears in **exactly one file** across
`cortana-vault/` and `cortana-skill-registry/` — the superseded fork in this directory. The
entry is not recorded under any other date, section, or wording.

Everything *else* unique to the fork was reflow/compression, not loss: the published copy is a
strict structural superset (adds Operator-Runbook Execution, Orchestrator-Performed Edits,
Eval-Wave Rules; Laws 7–9 deliberately compressed).

## Why it matters

The lost entry carries three production-earned rules that no other entry states:

1. **Law 7 sharpened** — assertions that grep a raw file or `inspect.getsource()` are satisfiable
   by comments and string literals. Assert against comment-stripped executable text or captured
   call kwargs; the comment-stripper must be quote/dollar-quote-aware.
2. **Law 10, cross-repo** — one artifact is the single source of truth for a credential's entire
   privilege set; sibling repos ship zero grant statements and say so.
3. **Law 2 instance** — Vercel serverless pools × Supavisor *session* mode camps on session slots
   until reaped. Web-tier pools use transaction mode (`:6543`); unjam live with
   `pg_terminate_backend` on the idle set.

This is also a live instance of the very rule 08-08c added ("a staged skill dir is itself a
premise — diff three-way before publishing"): the three-way diff was run, but the changelog union
was not verified line-for-line.

## Operator action (one step)

Fold the verbatim entry in `ENTRY-2026-08-04-wai157.md` (this directory) into the `## Changelog`
section of the registry skill, in date order between the `2026-07-30` and `2026-08-06` entries:

```
cortana-skill-registry/skills/orchestration/SKILL.md
```

Then re-publish via the normal gate (`_inbox/skills/skill-publish/scripts/publish-skill.sh`).
Per the vault contract this pass does **not** write the registry directly.

## Files here

| File | What it is |
|------|-----------|
| `ENTRY-2026-08-04-wai157.md` | The dropped entry, verbatim — paste this in |
| `SUPERSEDED-2026-08-08-fork.md` | The full superseded fork, kept for provenance. **Not** named `SKILL.md` on purpose, so `publish-skill.sh` cannot pick it up and re-regress the registry. |

> [!warning] Do not publish `SUPERSEDED-2026-08-08-fork.md`. It predates Operator-Runbook
> Execution, Orchestrator-Performed Edits, and Eval-Wave Rules. Its only unique value is the one
> changelog entry extracted alongside it.
