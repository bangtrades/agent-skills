---
name: agent-context-reconstruction
description: "Reconstruct context from a legacy/previous agent home directory without leaking secrets."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [agent-memory, context-reconstruction, migration, audit, handoff]
    related_skills: [hermes-agent, codebase-inspection]
---

# Agent Context Reconstruction

Use this when the user asks to review a previous agent's local home/workspace, build context from another agent runtime, migrate continuity, summarize an agent's memory, or understand what an autonomous agent was doing before.

This is **not** a codebase LOC pass. It is an operational reconstruction pass: identity, memory, tasks, runtime state, channels, logs, databases, blockers, and restart chain.

## Goals

- Build enough context to operate as a credible continuation of the previous agent.
- Preserve privacy and avoid leaking secrets or raw auth material.
- Distinguish canonical state from mirrors, logs, backups, and stale artifacts.
- Produce a durable brief that future sessions can load instead of re-scanning everything.

## Safety Rules

1. **Do not print secrets.** Treat `.env`, `secrets/`, `auth-*`, device identity files, cookies, API keys, OAuth profiles, and tokens as sensitive.
2. **Redact secret-like fields in configs.** Keys containing `token`, `secret`, `password`, `auth`, `credential`, `cookie`, or `apiKey` should be summarized but not reproduced.
3. **Do not encode transient setup failures as permanent doctrine.** Missing binaries, moved paths, or old runtime errors belong in the current-state section of the brief, not in long-term memory/skills unless the fix is durable.
4. **Prefer evidence over narrative.** Quote file paths, task IDs, table counts, and log signatures, but avoid dumping whole logs.
5. **Mark canonical roots explicitly.** If files say one root is canonical and another is a mirror, preserve that distinction.

## Procedure

### 1. Inventory safely

- List top-level directories and recent/key files.
- Exclude obvious dependency, binary, and secret-heavy directories from full-text scans (`.venv`, `node_modules`, `secrets`, browser caches, media blobs, large backups).
- Record file counts/sizes by top-level area to understand scale.

### 2. Read the agent's bootstrap/restart files

Look for files like:

- `AGENTS.md`, `CLAUDE.md`, `.cursorrules`
- `SOUL.md`, `IDENTITY.md`, `USER.md`, `MEMORY.md`
- `HEARTBEAT.md`, `TASK_QUEUE.json`, `ACTIVE_TASKS.md`, `BACKLOG.md`, `COMPLETED.md`
- `progress_dashboard.md`, `agent_status.json`, `team_roster.json`
- project/topic memory under `memory/projects/`, `memory/topics/`, `memory/reviews/`, `memory/flushes/`, `memory/daily/`

Extract:

- identity/persona and communication doctrine
- stop-work / safety / escalation rules
- active tasks and blockers
- canonical paths and “source of truth” hierarchy
- project-specific restart chains

### 3. Summarize config without leaking secrets

For config files (`*.json`, `*.yaml`, config DBs):

- Redact auth material.
- Capture providers/models, channels, gateway/server ports, enabled plugins/tools, agent roster, workspaces, scheduling/heartbeat config, and security warnings.
- Do not paste tokens, cookies, profile IDs if they identify credentials.

### 4. Inspect local databases structurally

For SQLite/local DBs:

- Summarize tables, row counts, and relevant column names.
- Sample only non-sensitive operational rows.
- Capture useful counts: tasks, flows, memories/chunks, documents, runs, queue entries.
- If vector extensions fail to load, still inspect normal tables where possible.

### 5. Review logs for current operational truth

Tail key logs and extract patterns:

- still-running reporters/heartbeats
- delivery failures
- repeated tracebacks
- rate/context/token-limit incidents
- daemon restart loops
- blocked tasks and stale run state

Keep this as **current observed issues**, not universal rules.

### 6. Build a durable context brief

Write a concise but complete handoff file outside the scanned legacy tree if appropriate. Include:

- source reviewed and redaction policy
- system shape and canonical roots
- agent identity/doctrine
- memory architecture
- channel/workstream map
- active/recent project truth
- current operational issues
- security/privacy notes
- recommended restart chain

Suggested path pattern:

```text
~/.hermes/<legacy-agent-name>_context_brief_<YYYY-MM-DD>.md
```

### 7. Report to the user

Reply with:

- where the brief was saved
- top recovered context
- important blockers/issues
- next restart chain

Do not overwhelm them with raw inventories unless they asked for exhaustive output.

## Useful Output Shape

```markdown
# <Agent> Context Brief — <date>

Source reviewed: `<path>`
Redaction: secrets/auth files not reproduced.

## System shape
## Core identity / operating doctrine
## Memory architecture
## Channel/workstream context
## Active / recent project truth
## Current observed operational issues
## Security/privacy notes
## Recommended restart chain
```

## Pitfalls

- **Do not treat file modification time alone as truth.** Logs may still be active while the agent runtime is otherwise stale.
- **Do not assume workspace mirrors are canonical.** Many agent ecosystems keep mirrors, backups, and Data-volume canonical roots side by side.
- **Do not dump raw session transcripts.** Extract task state and doctrine instead.
- **Do not make permanent negative claims from old logs.** Old `command not found`, credential, or version errors may already be fixed.
- **Do not skip memory files.** Agent identity and project truth are often in memory/review/flush files, not in config.

## References

- `references/openclaw-symba-2026-05-20.md` — session note from reconstructing a prior OpenClaw/Symba home directory.
