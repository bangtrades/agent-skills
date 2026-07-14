---
name: model-upgrade
description: >-
  Wrap up the current Cowork session into a complete, paste-able handoff document so work can
  continue in a fresh session on a newer model (e.g., Opus 4.8 → Fable). Reviews the entire
  conversation AND the associated project on disk, then writes a dated session-handoff file into
  the project's docs/ folder AND files a summary note into the Cortana vault
  (~/Cortana/cortana-vault/handoffs/). Trigger aggressively whenever the user says "model-upgrade",
  "/model-upgrade", "prep a handoff", "handoff doc", "wrap up this session", "close out this
  session", "migrate this session to the new model", "new model just dropped", "I'm restarting
  this in Fable", "session handoff", or any request to preserve session context for a future
  session or a different model, including near context limits. Do NOT trigger for git commit
  summaries, sprint close-outs (use sprint-runner), or vault log entries (use obsidian) — this
  skill's output is a first-message prompt for a brand-new session with zero context.
---

# Model Upgrade — Session Handoff Generator

Produce a handoff document that lets a **brand-new session on a newer model pick up exactly where
this one leaves off**. The new model has read NOTHING: not this conversation, not your memory of
it, not the unstated context in the operator's head. The handoff document is the only bridge.

The governing principle: **capture what exists only in this conversation; point to what exists on
disk.** Files survive the session — decisions, corrections, constraints, open questions, and
"why we did it this way" often do not. Those are the payload. Don't paste whole documents into the
handoff; link them in a read-first list instead.

## Workflow

### Step 1 — Mine the session (the part that dies with this context window)

Walk back through the entire conversation and extract:

- **What was asked and what was delivered** — every deliverable with its absolute file path.
- **Decisions and their reasons** — especially choices between alternatives, and anything the
  operator corrected you on. A correction is a constraint the new model will otherwise re-violate.
- **Operator-set constraints** — rules the user stated ("never X", "always Y", "don't touch Z").
  Preserve these **verbatim** in a dedicated section. Paraphrasing loses force and nuance.
- **Open questions** — anything you asked that was never answered, and anything the user said
  they'd decide later. These are the new session's first conversational moves.
- **In-flight work** — tasks started but unfinished, with exact resume points ("the loop is at
  Phase B3; the QA-1 block has not been handed over yet").
- **Gotchas discovered the hard way** — environment quirks, failed approaches, things that look
  fine but aren't (stale lock files, a UI that corrupts config on save, an endpoint on an
  unexpected port). These are the most expensive knowledge to lose.
- **Session metadata** — which model ran this session, today's date, what tools/MCPs/skills were
  actually used (the new session should verify they're still connected).

If your context was compacted and early conversation is fuzzy, check for a session transcript
tool (e.g., `mcp__session_info__read_transcript`) and re-read what you've lost before writing.
Never reconstruct from guesswork — a confidently wrong handoff is worse than a gap flagged as a gap.

### Step 2 — Review the project on disk

Ground the handoff in current file reality, not your memory of it:

1. Identify the project root(s) this session worked in.
2. Read the project's own state docs if present: `CLAUDE.md`, `README`, sprint ledgers/trackers,
   prior handoff docs, ADRs. The handoff should agree with them — where it doesn't, say which is
   newer and why.
3. Check git state if the project is a repo: branch, last commit, dirty files. Uncommitted work
   produced this session is a top-tier handoff item.
4. List files created or modified during this session (mtime since session start is a good
   filter) and reconcile against Step 1 — anything on disk you didn't remember producing, and
   anything you remember producing that isn't on disk, both need investigating.
5. Build the **read-these-first list**: the 3–7 documents, in order, that a fresh session should
   read before doing anything. Annotate each with one line on why it matters. Use **absolute
   paths** — a fresh session has no working directory context, and a relative path forces it to
   guess the project root before it has read anything.

### Step 3 — Write the handoff document

Read `references/handoff-template.md` and follow it. The template is **adaptive**: a platform
project with containers and SQL gets every section; a brand-collateral or writing session drops the
sections that don't apply (commands, IDs, architecture) rather than emitting empty headers. Keep
the section ORDER stable for the sections you do use — the operator runs this across many sessions
and scans them by shape.

Rules that make the document actually work as a first message:

- **Self-containment test**: could a fresh Claude execute "First moves" item 1 without asking a
  question this document could have answered? If not, the document isn't done.
- **Absolute everything**: absolute paths, absolute dates (never "yesterday" or "last week"),
  full command blocks that can be pasted and run as-is.
- **Verified vs. believed**: mark anything you couldn't confirm on disk this session as
  unverified, and tell the new session how to verify it. Don't launder uncertainty into fact.
- **No secrets**: never inline tokens, keys, passwords, or seed phrases. Reference where they
  live (`platform-v2/.env`, mode 600) instead. The handoff will be pasted into a fresh context
  and may be stored loosely.
- **Lean but lossless**: every sentence should either (a) exist nowhere on disk, or (b) be a
  pointer to where it does. If you're transcribing a document that's already in the read-first
  list, cut it.

### Step 4 — Save, verify, file to vault, present

1. **Output path** — auto-detect, in this order:
   - `<project-root>/docs/` if it exists →  `docs/session-handoff-<YYYY-MM-DD>.md`
   - else `<project-root>/session-handoff-<YYYY-MM-DD>.md`
   - If the session spanned multiple projects, write it under the primary project and say so in
     the header. If a handoff with today's date already exists, do not overwrite — suffix with
     `-2` (or the target model name, e.g. `-fable`).
2. **Verification pass** — re-read the finished document as if you were the new model: check every
   path exists on disk (read-first paths must be absolute), every command is pasteable,
   constraints are verbatim, no secrets leaked, the self-containment test passes.
3. **File a summary to the Cortana vault** — the vault is the operator's cross-session index;
   the per-project handoff is findable only if you already know the project, the vault entry is
   how all handoffs are found. Write a compact summary (not a copy) to
   `~/Cortana/cortana-vault/handoffs/<YYYY-MM-DD>-<project-slug>.md` following
   `references/vault-summary.md` (frontmatter per vault SCHEMA, ~15–30 line body, absolute
   pointer to the full handoff), and append a matching entry to the vault's `log.md` in its
   existing format. If the vault path is not mounted/accessible in this session, skip this step
   and say so explicitly in your final response — never silently drop it, and never write the
   summary somewhere else "as a fallback."
4. **Present** the handoff file to the user, and close with the two or three things they should
   know: where it was saved, that the vault summary was filed (or why not), any open question the
   handoff surfaces as the new session's first move, and anything you could not verify.

## Example invocations

**Example 1**
User: "model-upgrade — Fable just dropped, wrap this session up"
→ Full workflow; note "Session ran on: claude-opus-4-8 · Target: claude-fable-5" in the header;
save to the project's docs/; present.

**Example 2**
User: "prep a handoff doc, I'll continue this brand work in a new session next week"
→ Same workflow; the brand project likely drops the commands/IDs/architecture sections; in-flight
deliverables and voice/brand decisions made in-conversation are the payload.
