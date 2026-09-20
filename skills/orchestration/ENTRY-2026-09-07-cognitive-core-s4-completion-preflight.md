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
  - "[[docs/cortana-cognition/s4-completion-2026-09-07/model-preflight/README]]"
---

# Cognitive Core S4 completion preflight retrospective

Staged proposal only. Publication, model adoption, model loading and embedding
calls remain separate actions.

The fresh 57-issue manifest had zero drift, yet a readiness invocation at the
new HEAD rejected three accepted S2/S3 receipts. The cause was the optional
`--base-sha` argument: the validator interprets it as exact equality with each
receipt's original dispatch base. The normal dependency path omits that
comparison. The brief generator resolves and records the new attempt base for
idempotency while validating prerequisite receipts under their own recorded
and Git-resolvable identities.

Reusable rule: when an old prerequisite appears invalid only after rebasing a
new attempt, inspect the actual readiness and brief validators before creating
closure receipts or rerunning the earlier sprint. Distinguish an optional
same-base diagnostic from normal dependency readiness. Never manufacture a
fresh receipt from ancestry alone. A dependency becoming ready also does not
satisfy an independent operator gate; the Nomic adoption decision remained
pending throughout this preflight.

Authoritative run evidence and the exact command interpretation are linked in
the related preflight index above.

Lineage guard: the staged `SKILL.md` preimage was 121,976 bytes with SHA-256
`68bb512af268d2aad69007e311057ff74b33e7841249739e1b6db1a34251a1be`.
That richer staged superset was preserved and amended in place. The canonical
registry and account-loaded copies were read-only, and no publication occurred.
