---
name: memory-keeper
description: >
  Maintain the dated memories branch of the Cortana vault (cortana-vault/memories/) —
  create or update today's daily memory page, close out a day, promote durable memories,
  and roll up months. Trigger on: "memory-keeper", "log today", "write today's memory",
  "close out the day", "close out yesterday", "promote this memory", "remember this
  permanently", "what did we do on <date>", "month rollup", or any request to record
  daily activity into the memories branch. Also invoked by the 3:30 AM scheduled
  close-out run. Do NOT use for raw operation logging (log.md, handled by obsidian
  skill), project session summaries (obsidian skill), or trade capture (trade-capture).
---

# Memory Keeper — Cortana Dated Memory Branch

You maintain `cortana-vault/memories/` — the time-indexed memory of bang's and Claude's
daily work. One page per day, chained prev/next; month rollups; durable memories promoted
into `promoted/`. The branch answers two questions months later: *what happened on day X*
and *where did memory Y come from*.

Obsidian root: `~/Cortana/`; content root: `~/Cortana/cortana-vault/`. Read `cortana-vault/memories/start-here.md`, then `SCHEMA.md` before writing. The
`log.md` operations log is SEPARATE and append-only — link to it, never replace it.

## Tree

```
memories/
├── memories.md                        # hub — recent days, months, promoted index
├── daily/YYYY/YYYY-MM/YYYY-MM-DD.md   # one page per day
├── monthly/YYYY-MM.md                 # month rollup
└── promoted/
    ├── promoted.md                    # index of promoted memories
    └── <topic-slug>.md                # one durable memory per file
```

## Operations

### 1. DAILY — create or update today's page

1. Compute today's date (local). Path: `memories/daily/YYYY/YYYY-MM/YYYY-MM-DD.md`.
   Create year/month dirs as needed.
2. If the page exists, APPEND/UPDATE sections — never overwrite prior content.
3. If new:
   - Find the most recent prior daily page (walk back through `daily/`). Set this page's
     `prev:` to its wikilink path and update that page's `next:` (frontmatter AND inline
     nav line) to point here. This maintains the time chain.
   - If the month file `monthly/YYYY-MM.md` doesn't exist, create it from the monthly
     template and add it to the hub's Months list.
4. Fill sections from the session context: What Happened, Decisions, Insights & Candidate
   Memories, Sessions & Links. Wikilink every project, topic, and report touched.
5. Add the day's row to `monthly/YYYY-MM.md` Days table and to the hub's Recent Days
   table (keep hub table to the 14 most recent days; older days live in the rollups).
6. Update `updated:` dates on touched pages.

### 2. CLOSE-OUT — finalize a day (3:30 AM run targets YESTERDAY)

1. Open the target day's page. If it doesn't exist and `log.md` shows activity for that
   date, create it from log entries; if no activity, do nothing (no empty pages).
2. Review `log.md` and any session evidence for that date; fill gaps in What Happened.
3. Review "Insights & Candidate Memories": promote any that meet the bar (see PROMOTE),
   list the rest as context.
4. Set `status: completed` only for the completed daily document; record the true `run_outcome` and any capture gaps. Do not claim a 3:30 AM run occurred without a receipt.
5. Verify prev/next chain integrity for the day and its neighbors.

### 3. PROMOTE — qualified, scoped memory out of the daily stream

Promotion requires a specific assertion, scope, direct evidence and a review date. Follow `memories/memory-contract.md` and the executable `scripts/vault-contract.json` rather than duplicating a template here. A lesson inferred from a source is `testing`, not an accepted universal procedure.

1. Explicit operator corrections take the immediate path; do not wait for the nightly job.
2. Use `scripts/memctl remember --file /private/tmp/qualified-memory.json`, with `--expected-sha256` when revising. Supply the complete current evidence and lifecycle fields. The command preserves prior revisions and creates the index read path.
3. Keep source-day links and add the promoted link to the relevant day, project and rollup. Never manufacture a daily source for a direct correction.
4. Automatic session receipts live in `.cortana-memory/` at the Obsidian root. They are private draft evidence. Background extraction cannot turn a reported summary into verified fact or an instruction.
5. Preserve `harness_outcome` separately from `run_outcome`. A completed turn or completed report does not prove the work succeeded.

### 4. ROLLUP — month close (first close-out run of a new month)

1. Open `monthly/YYYY-MM.md` for the finished month.
2. Write Month Summary: themes, major decisions, project arcs, promoted memories.
3. Set `status: completed`. Ensure every day of the month appears in the Days table.
4. Ensure the hub's Months list links it.

### 5. TRACE — answering "what did we do on <date> / when did X happen"

1. Direct date → open the daily page. Range/topic → scan month rollups, then days.
2. Follow prev/next chains and promoted backlinks to reconstruct the narrative.
3. Answer with wikilinks to the pages used.

## Daily Page Template

```markdown
---
title: "Daily Memory — YYYY-MM-DD"
type: memory-daily
date: YYYY-MM-DD
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [🤖, memories, daily, <project-tags>]
status: active            # → completed at close-out
projects: [<slugs>]
prev: "[[memories/daily/.../<prev-date>]]"   # null for first page
next: null                                    # set when next day's page is created
promoted: []
related: ["[[memories/memories|Memories Hub]]", "[[memories/monthly/YYYY-MM|YYYY-MM Rollup]]"]
---

# 🧠 YYYY-MM-DD

**[[<prev>|⬅ prev]]** · **[[memories/monthly/YYYY-MM|month]]** · **[[<next>|next ➡]]**

## What Happened
## Decisions
## Insights & Candidate Memories
## Sessions & Links
## End-of-Day Status
- [ ] Closed out by 3:30 AM run
```

## Rules

- Emoji tag `🤖` first on every memories page (it's a memory-system page), then text tags.
- Never modify `log.md` beyond appending; never delete or rewrite a past day's recorded
  content — append corrections with a dated note.
- No empty pages: a day with zero activity gets no page.
- Link density: every project/topic/report named gets a `[[wikilink]]`.
- Log every memory-keeper operation to `log.md` per SCHEMA log format.
- Quality bar: useful to bang 6 months from now via search; opinionated, specific.
