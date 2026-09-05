---
name: schedule
description: Use when the user requests a reminder, recurring task, monitor, or change to an existing schedule. Discover the runtime scheduler and preserve existing task identity and preferences.
version: 0.2.0
---

# Scheduler adapter

Use the purpose-built scheduling tool available in the current runtime. In Codex, discover the automation tool and follow its current schema; other harnesses may expose different scheduler APIs. Never assume a tool exists because an older skill names it.

1. Identify whether the request creates, updates, pauses, resumes, or removes a schedule. Search existing automations before creating a duplicate.
2. Resolve timezone, timing, objective, sources, completion condition, and notification preference from the request and existing context. Ask only for required missing timing.
3. Write a self-contained prompt with explicit source locations, output expectations, and meaningful-change notification behavior for monitors. Preserve unchanged fields when updating.
4. Submit through the scheduler tool and verify its returned identity/state. Do not replace a failed scheduler call with an improvised cron job.
5. Report the actual result. A drafted prompt is not a saved schedule.

## Runtime and maintenance

Read the current project hub and applicable local instructions. Discover available tools and verify their input schema; skill names do not prove an API exists. Record what was executed, what was checked, and what remains unverified. Stage skill improvements in Cortana’s inbox; never rewrite the installed registry.
