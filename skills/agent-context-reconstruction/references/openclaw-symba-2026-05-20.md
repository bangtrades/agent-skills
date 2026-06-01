# OpenClaw/Symba Context Reconstruction — 2026-05-20

## Trigger

The user asked whether `/Users/symba/.openclaw` was visible locally, then asked to review all content there to build context for the previous OpenClaw-Symba agent.

## Useful pattern

A good reconstruction pass combined:

1. Safe top-level inventory with secret/dependency/media exclusions.
2. Redacted config summary of `openclaw.json` and agent model/provider config.
3. Reading the agent restart files: `SOUL.md`, `AGENTS.md`, `MEMORY.md`, `HEARTBEAT.md`, `TASK_QUEUE.json`, `ACTIVE_TASKS.md`, `BACKLOG.md`, `progress_dashboard.md`.
4. Structural SQLite inspection for memory, task runs, flow registry, and trading library DBs.
5. Log-tail extraction for current operational issues.
6. Project/topic/review/flush memory scan to map durable channel and project context.
7. Writing a durable brief outside the legacy tree.

## Key findings from that session

- Previous OpenClaw home: `/Users/symba/.openclaw`.
- Main workspace: `/Users/symba/.openclaw/workspace`.
- Canonical Lion’s Den / Mission Control app root: `/Volumes/Data/Apps/mission-control`.
- The Data-root Mission Control app was canonical when workspace mirrors diverged.
- OpenClaw gateway was configured on local loopback port `18789`.
- Discord integration, ACP/acpx dispatch, and multiple named agents were configured.
- Prior Symba identity emphasized autonomous executive/operator behavior, heartbeat loops, blocker escalation, and evidence-based status truth.
- File-backed MOS structure was central: daily notes, flushes, reviews, project memory, topic memory, and long-term memory.
- Important workstreams recovered: Lion’s Den / Mission Control, Den CE Migration, Chart CIP, Gemma/Yoda/CIP/CE, Research system, Trading library, Textbook.AI, Matrix skills engine, OpenBB market-intel.

## Current-state issues found in logs

These should be treated as session/current-state observations, not durable tool limitations:

- Progress reporter attempted 15-minute LD status updates but Discord delivery failed with `env: node: No such file or directory`.
- Agent sync repeatedly hit Python union-syntax failure (`dict | None`) consistent with an older Python runtime.
- Trading library ingest logged `sqlite3.OperationalError: unable to open database file`.
- Gateway logs showed historical context-overflow/rate-limit/security warnings.

## Output produced

A durable brief was written at:

`/Users/symba/.hermes/openclaw_symba_context_brief_2026-05-20.md`

Future sessions should prefer loading that brief before re-scanning the full OpenClaw tree.
