# Cortana Skill Registry

The shared skill library for the Cortana agency. This repo is the canonical
source of the skills Cortana agents draw on — trading skills, dev skills, and
the two platform skills (`cortana-memory`, `paperclip-triage`).

It is a **standalone git repo**, checked out and mounted **read-only** into the
Paperclip container. Skills load via Paperclip's standard skill discovery — no
Paperclip source-tree modification (STEP-48).

## Why it is its own repo

The registry is operator-managed and version-controlled independently of the
platform tree so it can be shared, imported via a GitHub URL, and updated
without touching `platform-v2/`. Per the operator's decision it lives in a
**private** GitHub repo. Creation + push is operator-gated (GitHub auth is
theirs); this tree is scaffolded ready for `git init`.

## Structure

```
cortana-skill-registry/
  README.md              ← this file
  .gitignore
  skills/
    <skill-id>/
      SKILL.md           ← the manifest + skill body (see "Manifest format")
      scripts/           ← skill helper scripts (filled in by agents over time)
      references/        ← optional deep-dive docs (carry-overs use these)
```

Each immediate subdirectory of `skills/` that contains a `SKILL.md` is one
discoverable skill. The directory name is the skill id.

### Skills in this registry

| Skill id | Kind | Purpose |
| --- | --- | --- |
| `markets-research` | trading (stub) | Market + signal research |
| `indicator-build` | trading (stub) | Building trading indicators (Pine Script / charting) |
| `backtest-run` | trading (stub) | Running + analyzing backtests |
| `risk-rules` | trading (stub) | Position sizing, drawdown, risk checks |
| `data-fetch` | trading (stub) | Market data retrieval |
| `code-review` | dev (stub) | Code review checklist + standards |
| `test-runner` | dev (stub) | Test + smoke harness |
| `cortana-memory` | platform | Memory pillar reference (carried from v1, intact) |
| `paperclip-triage` | platform | Incident-grade Paperclip/Cortana debugging (carried from v1, intact) |

The seven trading/dev skills are **stubs**: each ships a complete `SKILL.md`
(name, trigger-friendly description, usage) and placeholder `scripts/`. The
owning agent fills in script bodies as it masters the skill.

## Manifest format (what Paperclip actually discovers)

Paperclip discovers a skill by scanning `skills/` for any subdirectory
containing a `SKILL.md`. **The YAML frontmatter of `SKILL.md` is the manifest** —
there is no separate authoring `skill.json`. Verified against the v2 Paperclip
source: `listPaperclipSkillEntries` /
`packages/adapter-utils/src/server-utils.ts` reads `SKILL.md` frontmatter; the
`.paperclip-materialized-skill.json` file referenced internally is a runtime
sentinel Paperclip writes, not an authoring input.

> Note: STEP-48 §3.6 phrased this as `skills/<name>/skill.json`. That was
> aspirational shorthand; the implemented discovery contract is `SKILL.md`
> frontmatter. This registry follows the implemented contract.

Frontmatter fields:

| Field | Required | Meaning |
| --- | --- | --- |
| `name` | yes | Skill name; must match the directory id. |
| `description` | yes | Trigger-friendly summary — when the skill should fire. |
| `required` | no (default `true`) | `false` marks the skill optional (loaded on demand, not auto-injected). |
| `version` | no | Semantic version of the skill content. |

Minimal example:

```markdown
---
name: markets-research
description: Use when researching a market, ticker, or trading signal...
required: false
version: 0.1.0
---

# Markets Research
...usage...
```

## How skills are consumed

1. **Registry → company library.** The operator imports skills into the Cortana
   Paperclip company via the company-skills import surface, using this repo's
   GitHub URL (or `org/repo/skill-id` key form). Example:
   `POST /api/companies/$COMPANY_ID/skills/import` with
   `{"source": "https://github.com/<org>/cortana-skill-registry"}`.
2. **Company library → agent.** Skills are assigned to agents via
   `desiredSkills` at hire/create, or `POST /api/agents/<id>/skills/sync`.
3. **Read-only mount.** The repo is mounted read-only into the Paperclip
   container; agents read skills but never mutate the registry from inside a run.
   Registry edits go through git on the operator's side.

## Skill-mastery convention (STEP-49 §2.1)

A skill in this registry is *shared, static* knowledge. An agent's *fluency*
with a skill — its accumulated preferences, gotchas, and worked shortcuts — is
**agent-private** and lives in that agent's Cortana vault, not here:

```
state/cortana-memory/<agent-uuid>/skill-mastery/<skill-id>.md
```

- One mastery note per skill the agent has used repeatedly. The filename's
  `<skill-id>` matches the registry directory id (e.g. `backtest-run.md`).
- The note records *this agent's* learned specifics: preferred parameters,
  recurring pitfalls, links to its own past runs — not a copy of the SKILL.md.
- Mastery notes are part of the agent's portable identity (STEP-49 §2.1: the
  skill-mastery layer). On harness migration they travel with the soul + memory
  (STEP-49 §5 step 5); the registry itself does not move with the agent.
- The registry is the *what*; the mastery note is the *how this agent does it*.

This separation keeps the registry clean and shareable while letting each agent
build private fluency over the same shared skills.
