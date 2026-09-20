# ENTRY 2026-09-19 — Vault cleanup wave (lineage-safe changelog entry)

Not appended to the staged `SKILL.md` (per 08-19 / 09-05, entries stage as files for the merge). Program: nine memory close-out runs' operator-free flags → 5 Opus content slices by path ownership + 1 micro-round + 1 Opus read-only adversarial gate + orchestrator fix round; Fable orchestrator; ~50 min; no git (stale locks). Gate verdict: 4 PASS / 2 PASS-with-defects / 1 FAIL (P1) → fixed. See the `[2026-09-19] orchestration` entry in `log.md`.

## Additions (three)

**(a) Timestamp provenance is a gate attack, not a spot-check.** A session-window heading in a close-out ("15:52–15:57 — Apex demo account") was the audit *file's* mtime; one hop later the hub and two promoted memories asserted "approved at 15:57 PDT" as a business event. No audit recorded an approval clock. Content-vault waves whose evidence class is "source-reported from documents" must grep every asserted timestamp back to a machine-readable stamp *inside* a cited document; a time that exists only in `stat` output or a heading is not a claim any source makes (SCHEMA: mtime is never evidence). This is Law 12 for prose: the gate must read the source, not the summary that cites it.

**(b) Parallel slices that write cross-referencing facts need a seam gate, same as code.** Slice A revised two memories to say "the hub block is stale — read the daily page until refreshed" while slice B, in the same wave, refreshed that block. Both were correct against their briefs and wrong together. Rule already exists for contracts between code slices (pipeline step 3); extend it to content: when one slice's output is a *pointer* to state another slice changes, gate the pointer after both land, or serialize them.

**(c) A tool that writes a fixed body makes every post-write append invisible to its own receipt.** `memctl remember` journals the sha of the text it wrote; the workflow then hand-appends a `## Review` section, so all ten receipts from this wave are stale and the journal's anti-tamper column is decorative. Rule: when a wave's contract requires content the writing tool cannot emit, either extend the tool (proposed: `--review-file`) or stop claiming the receipt proves integrity — never both hand-append and cite the receipt.

## Retro notes (not new laws)

- Ownership-by-path parallelism worked again with zero collisions (08-08b confirmed); the gate's `find -newermt` sweep is the load-bearing control — keep the start-time stamp.
- The Agent tool ran the first slice alone because it was dispatched in its own message; parallel dispatch requires all invocations in one message. Mechanical, but it cost ~6 minutes.
- QA's "heading arithmetic does not close" finding was a counting error in the orchestrator's own log entry (nine vs ten), not a phantom entry — Law 9 applied in the fix round: reproduce before restructuring.
