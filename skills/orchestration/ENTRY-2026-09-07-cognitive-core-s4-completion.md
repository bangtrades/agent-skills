---
type: reference
created: 2026-09-07
updated: 2026-09-07
status: draft
tags:
  - "🤖"
  - orchestration
  - skill-improvement
deployment: personal
related:
  - "[[docs/cortana-cognition/s4-completion-2026-09-07/README]]"
---

# Cognitive Core S4 completion retrospective

Staged process evidence only. It does not claim G4 acceptance: the measured
latency and retrieval-quality gates failed, lexical remained the default, and
the final independent report was still pending when this entry was written.

Reusable lessons:

1. Validate a canonical receipt against its schema before moving a Linear issue
   to review. A successful run and a human-readable report do not repair a
   malformed acceptance record.
2. Keep runtime identities separate. The assigned GPT-5.6 Sol agent identity,
   the approved embedding model artifact, its loaded service identifier, and
   the embedding-space manifest are different evidence fields.
3. Measure through the public composed path. A direct vector-candidate
   microbenchmark missed the lexical connection lifecycle that recreated the
   SQLite WAL and defeated process-cache reuse.
4. A retained SQLite observer can cross worker boundaries through cache
   eviction, invalidation, or shutdown. Configure only that retained connection
   for cross-thread close, serialize its lifecycle, and test the raw connection
   is actually closed from a different thread; removing a cache entry is not
   proof of cleanup.
5. Freeze a quiet Git worktree before a long benchmark. Preserve an aborted run
   when shared-tree drift appears (this run stopped after 193 rows), then restart
   from a pinned quiet tree rather than interpreting mixed-source measurements.
6. Normal dependency readiness omits the optional exact `--base-sha` receipt
   diagnostic. Inspect the actual brief/readiness validator before inventing
   closure failures or rerunning completed prerequisite sprints.

Authoritative run evidence is rooted at
`.cortana-memory/orchestrator/runs/s4-approved-q8-20260907T2231Z-sol/` and the
linked completion index provides its governed read path.

Lineage guard: the staged `SKILL.md` preimage was 124,541 bytes with SHA-256
`84be7838f69d0aa87dca45e37fedc7f8602f433ec8a715d79dea8c3fa2851eaa`.
That full staged preimage was preserved byte-for-byte and this retrospective was
appended. The canonical registry remained read-only and no publication occurred.
