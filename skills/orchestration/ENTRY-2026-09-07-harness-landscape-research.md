---
title: Harness Landscape Research Fleet — Orchestration Retrospective
type: analysis
created: 2026-09-07
updated: 2026-09-07
tags: [🔧, orchestration, retrospective, research-fleet]
status: completed
related:
  - '[[cortana-vault/research/topics/harness-control-plane-landscape-2026-09]]'
  - '[[cortana-vault/youtube/transcripts/yc-harness-night-prime-agent-qm-jarvis]]'
---

# Harness Landscape Research Fleet — Orchestration Retrospective

Four Opus research agents owned disjoint slices of one video's claims (Prime Agent · QM · OpenJarvis · self-improving lineage + ARC-AGI numbers) under a write-early contract with explicit NO-GO topics and ~25-action budgets. One Opus adversarial QA agent re-verified 31 load-bearing claims read-only from primary sources. One fresh Opus resolution agent closed the three items the gate could not open. Synthesis went to a vault topic page and a WaiveLabs-branded self-contained HTML brief; raw slice files archived under `raw/ingested/harness-research-2026-09/`.

What moved the work: write-early files (every slice delivered on first dispatch — no research-without-write timeouts this time); slice reports with a fixed skeleton (identity / architecture / claim table / applicability / integrity flags / open questions / sources), which made the QA gate's job a table diff rather than a re-read; spending Opus on the gate — the P0 was invisible to the slice that wrote it and obvious to fresh eyes.

What misled: a column slide in a wide vendor table produced two confident, opposite conclusions from one cell; a slice quoted the paper extensively yet omitted the paper's own disclaimer of the headline it recommended for pitch use; two files used "verified" with incompatible meanings; a slice asserted a licence for a repository that has no LICENSE file (an inversion that matters for client reuse); a hardware-platform count was one short of the paper's own statement.

Environment: `developer.nvidia.com` refused Firecrawl for the gate agent and `web_fetch` deduped a prior session's fetch it could not see; a fresh agent's Firecrawl scrape returned 200 — resolution passes belong in fresh agents. The vault linter is now pinned to a Python 3.14 venv absent from this sandbox; per-file link verification stood in for it.

Three additions to Research-Fleet Discipline (column-header-carrying numbers + shared-row reconciliation; the author's-own-disclaimer field; a defined verification legend). No new law. The staged skill copy was newer than the session-loaded copy and was patched in place rather than overwritten; operator publishes via `bin/publish-skill.sh orchestration` after the three-way diff.
