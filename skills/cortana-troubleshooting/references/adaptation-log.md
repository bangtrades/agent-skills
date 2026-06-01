# Cortana Troubleshooting Adaptation Log

Append durable lessons here after significant Cortana incidents. Keep entries
short and operational.

## 2026-05-01 Initial Lessons

### Task Completion Loop

Symptom: a Paperclip issue repeatedly dispatched the same router task after
successful Anthropic responses.

Root cause class: lifecycle contract mismatch between successful router
completion and Paperclip issue terminal state.

Rule: every successful one-shot router completion needs a terminal task signal
or an explicit continuation contract. Add regression tests at the lifecycle
boundary, not only provider/router tests.

### Duplicate Chat Return

Symptom: issue detail page rendered both the full router run result and a
truncated duplicate comment.

Root cause class: UI dedupe missed historical comments where the run id was
stored as `createdByRunId` instead of `runId`.

Rule: router-result UI dedupe must use all durable run-link fields. Browser
evidence is required after UI fixes because DB rows can be correct while the
projection is wrong.

### Budget Drift

Symptom: Symba budget page displayed `$0.00` while router ledger contained real
provider spend.

Root cause class: Paperclip budget read model did not include router
`llm_cost_ledger` spend.

Rule: budget truth comes from the ledger. UI budget cards must reconcile to
ledger rows by agent/provider/model and period.

### Missing Task Instruction

Symptom: router dispatch refused with `no task instruction was supplied`.

Root cause class: adapter payload extraction produced an empty provider prompt.

Rule: the shim must refuse before spend when instruction text is empty. The fix
belongs in payload extraction or task creation, not in the provider.

### Skills Are Not Yet Execution

Symptom: skills appear in Paperclip but `cortana_llm_router` reports tracked-only
or no direct skill sync.

Root cause class: skill manifests/tool schemas exist before the full tool
execution dispatcher.

Rule: do not claim agents can read files or memory until a tool call has
round-tripped through the dispatcher and the handler result is visible to the
model.
