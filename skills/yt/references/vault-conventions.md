# Vault conventions for YouTube pages

These are lint-enforced or lint-adjacent. Getting them wrong creates cleanup debt that someone
(usually a later session) has to pay.

## Frontmatter contract

```yaml
---
title: "Video Title"          # quoted; the real title, not the slug
type: youtube                 # always
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [📺, 🤖, topical, tags] # emoji category FIRST — see below
status: processed             # or transcript-pending if no transcript was obtainable
url: "https://www.youtube.com/watch?v=VIDEO_ID"
channel: "Channel Name"
duration: "MM:SS"
published: "YYYY-MM-DD"
relevance: high | medium | low
deployment: personal | enterprise | both
related:                      # list form, with readable labels after the pipe
  - "[[moc/agent-engineering-patterns|Agent-Engineering Patterns MOC]]"
sources:
  - https://www.youtube.com/watch?v=VIDEO_ID
---
```

## Emoji category tags

`vault-lint.py` audits for a missing emoji tag. Every video page starts with `📺`, then adds the
domain emoji:

| Emoji | Domain |
|---|---|
| `📺` | YouTube source (always present on video pages) |
| `🤖` | AI / agents / tooling |
| `🎯` | Trading (NQ, futures, strategy, orderflow) |
| `💼` | WaiveLabs / consulting / client work |
| `📚` | Research, papers, curricula |

A video can carry two (`[📺, 🤖, ...]`). Topical tags follow — 4–8 total, lowercase kebab-case.

## The `deployment:` lane

Answers "who is this knowledge *for*?" It is what makes the corpus queryable by lane:

- **`personal`** — bang's own trading, tooling, or vault infrastructure
- **`enterprise`** — client-deliverable; feeds WaiveLabs engagements and pitch material
- **`both`** — a pattern that applies in both contexts (most agent-engineering content)

When genuinely unsure, `both` is the safe default — but prefer to make the call, since the whole
point is discrimination.

## Naming

`youtube/transcripts/<slug>.md`, kebab-case, under 60 characters, describing the *topic*.
Include the speaker when they're the draw:

- ✅ `kyle-mistele-loop-engineering-control-theory`
- ✅ `agent-evals-workshop-financial-analyst-arize`
- ❌ `loop-engineering-from-first-principles-kyle-mistele-ai-engineer-conference-2026`
- ❌ `video-3`

## Link rules (each of these has actually broken the lint)

1. **No `.md` suffix in wikilinks.** `[[a/b/c]]` not `[[a/b/c.md]]` — the latter resolves to `c.md.md`.
2. **Never wikilink a skill name.** Skills aren't vault pages. Use backticks: `` `brand-recon` skill ``.
3. **Don't wikilink literal example text.** If you're documenting the `[[x.md]]` bug in prose, the
   linter will flag your example. De-link it into code formatting.
4. **`~/Cortana/Reports/` links are cross-layer.** They live outside the vault and resolve via
   `file://`. The linter reports them as broken *by design* — never "fix" them by deleting.

## Where things live

| Content | Path |
|---|---|
| Video page | `youtube/transcripts/<slug>.md` |
| Raw transcript | `raw/ingested/yt-VIDEO_ID-transcript.txt` |
| Video index | `youtube/youtube-library.md` |
| Activity log | `log.md` |
| Pattern MOC | `moc/agent-engineering-patterns.md` |
| Topic pages | `research/topics/<topic>.md` |
| Papers | `research/papers/<paper>.md` |
