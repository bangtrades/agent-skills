---
title: Orchestration refinement — MetaCortex S01 safety boundaries
type: reference
created: '2026-09-06'
updated: '2026-09-06'
tags: ['🤖', orchestration, metacortex-v2]
status: draft
deployment: both
related:
- '[[cortana-vault/projects/metacortex-v2/metacortex-v2--run-mc-s01-20260905-01]]'
---

# MetaCortex S01 orchestration retrospective

The useful advance was running independent probes against the real pinned SDK and mounted context/usage paths. Construction-time controls passed their initial tests, yet reused clients could cross run contexts at fire time; a newly named fatal exception also fell through older memory fallback catches. The staged skill changelog records one focused addition: validate the shared fatal-error family across all swallowing boundaries and assert identity again before a paid leaf, while preserving original attribution of incurred callbacks.

The initial environment drift and worktree import checks reaffirm existing skill rules. Root twice attempted a relative operational-ledger path while a shell was in an agent worktree; both reads failed before a write. The run ledger now uses an absolute run-root path. This did not alter source or acceptance. Further laws were not added for these already-covered mechanics.

QA-owned legacy composition fixtures were updated by the independent custodian, not the producers; the audit confirmed every original assert AST was preserved. New ordinary QA probes were committed as portable runtime regressions. Protected scenario bodies were not returned to the root or producers. Final candidate verdict and test counts belong in the run ledger and its acceptance record, not this proposal.

Evidence: `/Users/nolan/Projects/MetaCortex/output/runs/mc-s01-20260905-01/qa/`, the run ledger and [[cortana-vault/projects/metacortex-v2/metacortex-v2--run-mc-s01-20260905-01]]. This is a staged improvement, not a published skill. The existing newer staging content was preserved; the loaded copy matched the registry Git tip before the append. No registry file or harness symlink was edited.

Publication after normal review: `/Users/nolan/Cortana/cortana-skill-registry/bin/publish-skill.sh orchestration`. The generated `orchestration-metacortex-s01.skill` archive carries the same candidate SKILL.md for review; it does not install or publish itself.
