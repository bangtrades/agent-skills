# Handoff Document Template (adaptive)

The canonical shape, derived from the operator's proven idiom (`session-handoff-2026-06-09.md`,
Cortana v2). Sections marked **[core]** appear in every handoff. Sections marked **[if relevant]**
are included only when the project has that dimension — drop them entirely rather than emitting
empty headers. Keep the order stable for the sections you use.

Why this shape works: the new model reads top-to-bottom. Identity and mission first (so it knows
who it's working for and what the thing is), then reading list (so it can self-orient from disk),
then deltas and state (what changed, where the frontier is), then guardrails (before it acts),
then reference material (when it acts), then explicit first moves (so the first response is useful
instead of "how can I help?").

---

```markdown
# <Project> — Session Handoff (<YYYY-MM-DD>)

> Hand-off prompt for a fresh Claude (<target model>) Cowork session continuing <project>.
> Session ran on: <model id> · Generated: <YYYY-MM-DD>
> Paste everything below the line as the first message of the new session.

---

You are continuing work on **<project>** — <one-sentence what-it-is>. The operator is
**<name/handle>** (<role, working style, output preferences — e.g. "wants run-sheets over
narratives, pasteable code blocks">). <Environment constraints: what YOU can/can't do — e.g.
"You do NOT have docker access; the operator runs commands and pastes output back.">

## What this project is                                                        [core]

<2–6 sentences: mission, key concepts/vocabulary the project uses, what the value-add is.
Define project-specific terms a fresh reader can't infer (an "agent" is X; a "harness" is Y).>

## Read these first (in order)                                                 [core]

1. `<absolute path>` — <why this matters / what's in it>
2. ...
<3–7 items. Order = reading order. The single best state doc goes first.>

## What the LAST session did                                                   [core]

<Short narrative of the session arc, then deliverables. Every deliverable gets a path.>

**Delivered (all on disk):**
- **<Deliverable>** → `<path>` <one-line description; status: applied / drafted-not-applied>
- ...

**Gotchas to know:**
- <Things discovered the hard way: environment quirks, failed approaches, traps. Include the
  workaround inline.>

## Current state                                                               [core]

- **<Frontier item>:** <exact position — what phase/sprint/step, what's done, what's next>
- **Open questions never answered:** <verbatim — these are the new session's first asks>
- ...

## Operator-gated items still outstanding                                      [if relevant]

<Pasteable command block(s) for things only the operator's machine can do. Label each lettered
item with the finding/ticket it closes. Include cautions inline as comments.>

```bash
# A. <what + why>
<commands>
```

## Standing constraints — DO NOT VIOLATE (verbatim, operator-set)              [core]

- <Each constraint exactly as the operator stated it. No paraphrase. Include constraints from
  prior handoffs that still stand — these accumulate across sessions.>

## Architecture / domain cheatsheet                                            [if relevant]

<Dense reference: stack, ports, containers, data flow, quirks ("the router is NOT a router —
it's the memory bridge"). For non-technical projects this becomes a domain cheatsheet: brand
palette decisions, voice rules, audience, naming. Only what's needed to act without re-derivation.>

## Critical IDs / values                                                       [if relevant]

- <name>: `<value>`
<UUIDs, account IDs, ticket numbers, port numbers — anything the new session would otherwise
have to hunt for. NEVER secrets — reference their on-disk location instead.>

## Useful skills / tools in this environment                                   [if relevant]

- `<skill-name>` — <when to reach for it in this project>
<Also note MCPs the session depended on (e.g., tradingview, supabase) so the new session
verifies they're connected before relying on them.>

## First moves in the new session                                              [core]

1. <Concrete first action — usually: read the top state doc and confirm reality matches this handoff.>
2. <The standing open question to ask the operator, verbatim, with the branch: "if yes → X; if no → Y.">
3. ...
<3–6 numbered moves. Each one actionable without further clarification. End with the standing
next-up objective once current work clears.>
```

---

## Section-level guidance

**The intro paragraph** carries the operator's working style. This is what makes the new model
feel like a continuation rather than a reset — tone, depth, format preferences, division of labor.

**"What the LAST session did"** is a delta, not a history. If this is session N of many, summarize
older history in one line and link the prior handoff; detail only the most recent session.

**"Standing constraints"** is the highest-stakes section. A violated constraint costs operator
trust; a verbatim list is cheap insurance. When a constraint has a non-obvious reason, keep the
reason attached ("changing POSTGRES_PASSWORD via env breaks the running DB — Postgres only honors
it on first volume init").

**"First moves"** turns the handoff from a briefing into a program. The worst first message from
a new session is a generic greeting; the best is "I've read the handoff. Confirming state: <X>.
The open question is <Y> — which way do you want to go?"

**Length calibration:** a heavy platform project lands ~150–250 lines; a light creative project
~40–80. If you're under 40, you probably lost session-only knowledge; if you're over 300, you're
probably transcribing documents that should be links.
