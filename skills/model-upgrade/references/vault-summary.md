# Vault Summary Note (Cortana)

After writing the full handoff into the project, file a compact summary into the Cortana vault so
all handoffs are discoverable from one place. Default vault root: `~/Cortana/cortana-vault/`
(adjust only if the operator has said otherwise this session).

Path: `cortana-vault/handoffs/<YYYY-MM-DD>-<project-slug>.md` (lowercase, hyphens — e.g.
`2026-06-09-platform-v2.md`). Date collision for the same project → suffix `-2`.

The summary is an **index card, not a mirror**: someone scanning the handoffs folder should learn
in 20 seconds what the session was, where it left off, and where the full handoff lives. If the
full handoff ever changes, the vault note's pointer still works; duplicated content would rot.

## Format

```markdown
---
title: "<Project> — Session Handoff (<YYYY-MM-DD>)"
type: session
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags: [<emoji>, handoff, model-upgrade, <project-slug>]
status: completed
sources:
  - "<absolute path to the full handoff doc>"
related:
  - "[[projects/<project>/<project>]]"   # only if that vault page exists
---

# <Project> — Session Handoff (<YYYY-MM-DD>)

> Full handoff: `<absolute path>` — paste-able first message for the new session.
> Models: <session model> → <target model>

**Session arc:** <1–2 sentences — what this session set out to do and what it actually did.>

**Delivered:** <one line per major deliverable, with path.>

**Frontier:** <where work stopped, exactly.>

**Open questions:** <the unanswered items the new session must raise first.>

**Constraints added/changed this session:** <only new or modified operator rules; "none" is fine.>
```

Emoji tag: exactly one, first in the tags array, by domain — 🎯 trading, 🤖 AI/agents/platform,
💼 business/clients, 🔧 infrastructure, 📚 research, 📊 reports. Pick by the project's primary
domain.

## log.md entry

Append to `cortana-vault/log.md` in its existing style:

```markdown
## [<YYYY-MM-DD>] handoff | <Project> session handoff (<session model> → <target model>)

- **type**: handoff
- **source**: model-upgrade skill, end of Cowork session
- **details**: <2–3 sentences: session arc, where the frontier is, top open question.>
- **pages touched**: [[handoffs/<YYYY-MM-DD>-<project-slug>]]
```

Do not refresh dashboards or run vault lint from this skill — those belong to the vault's own
maintenance cycle (obsidian / obsidian-review skills). Write the two files, nothing else.
