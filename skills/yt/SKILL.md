---
name: yt
description: Process a YouTube video into a Cortana vault wiki page. Use this skill whenever a user shares a YouTube URL (youtube.com, youtu.be), says "/youtube", mentions processing a video, or pastes a bare URL that looks like a YouTube link. Even without explicit instructions — if the message contains a YouTube URL, use this skill. Also trigger on "pull the transcript", "ingest this video", "watch this", or any reference to turning video content into vault knowledge. This skill handles the full pipeline: Firecrawl-first metadata, a four-rung transcript acquisition ladder (yt-dlp → Firecrawl → Chrome → paste), an opinionated wiki page with key takeaways and relevance analysis, source-integrity checking, raw transcript archival, index + MOC wiring, and a lint gate.
---

# YT — YouTube → Cortana Vault

You're turning a YouTube video into a permanent, searchable knowledge page in bang's Cortana
vault (an Obsidian wiki). Bang trades NQ futures, builds AI agent platforms, and runs an AI
consulting practice (WaiveLabs). Everything you write should be filtered through: **how does
this connect to trading edge, AI tooling, or the consulting business?**

The quality bar is high. A good page is one bang can find 6 months from now via Obsidian search
and immediately get value from. A bad page is a generic summary he could have gotten from ChatGPT.

**Vault root:** the workspace folder containing `cortana-vault/`. All paths below are relative to it.

---

## Step 0 — Dedupe before you do any work

The vault has 140+ video pages and multiple sessions write to it concurrently. Always check first:

```bash
cd <vault-root>
grep -rl "VIDEO_ID" --include=*.md youtube/ raw/ 2>/dev/null
```

- **Exact hit** → the video is already ingested. Report that, offer to refresh rather than duplicate.
- **Near-miss on topic** (a `research/topics/` page on the same subject from a *different* source) →
  not a duplicate. Write the new page and **cross-link both directions** (see Step 6).

Never create a second page for the same `video_id`.

---

## Step 1 — Acquire metadata and transcript (the tool ladder)

**Metadata and transcript are separate problems. Solve them separately.**

### 1a. Metadata — Firecrawl first

The sandbox IP is frequently bot-blocked by YouTube. Firecrawl runs from its own proxied IPs and
is the **default, authoritative** metadata source:

```
firecrawl_scrape url="https://www.youtube.com/watch?v=VIDEO_ID" formats=["markdown"]
```

Extract: **title, channel, publish date, duration, view count, description**. The description is
high-signal — creators often summarize the thesis there, and it is the fastest way to sanity-check
what the video actually claims (see Step 3).

If Firecrawl is unavailable in the session, fall through to `yt_extract.py` metadata (rung 2 below)
and note in your report that metadata came from the unproxied path.

### 1b. Transcript — climb the ladder, stop at the first rung that works

> **Firecrawl cannot scrape a YouTube transcript directly.** The transcript is not in the rendered
> DOM — it sits behind a "Show transcript" interaction and is served by the `timedtext` endpoint.
> Do not burn calls trying `firecrawl_scrape` on the watch URL expecting captions.

| Rung | Method | When |
|---|---|---|
| **1** | `python <skill-dir>/scripts/yt_extract.py "URL" --output-dir /tmp/yt-ingest` | Always try first. Best output: clean `[MM:SS]` timestamps. |
| **2** | Firecrawl two-hop: `firecrawl_scrape` with `formats=["rawHtml"]` → find `captionTracks[].baseUrl` in `ytInitialPlayerResponse` → `firecrawl_scrape` that URL | Rung 1 returns bot-block / empty transcript. Routes around the IP block. baseUrls are signed and short-lived — use immediately. |
| **3** | Chrome MCP: navigate → "...more" → "Show transcript" → `get_page_text` | Rungs 1–2 fail. The innertube endpoint throttles after a few automated requests; expect the panel to spin. |
| **4** | **Ask bang to paste it** | Everything else failed. This is the documented reliable fallback, not a defeat — say so plainly and move on. |

`yt_extract.py` writes `status.json` and uses distinct exit codes so you know which rung failed:

- `0` — metadata + transcript both OK
- `10` — metadata OK, **transcript missing** → climb to rung 2
- `20` — metadata failed (bot-block) → use Firecrawl for metadata, then climb for transcript

For a pasted or Chrome-scraped transcript, normalize it instead of hand-editing:

```bash
python <skill-dir>/scripts/yt_extract.py --normalize raw.txt --url "URL" --output-dir /tmp/yt-ingest
```

This converts YouTube's bare `0:00 / text` paste format into canonical `[MM:SS] text` lines.

### 1c. If you cannot get a transcript at all

**Do not write a page from the description and your priors.** Fabricating takeaways poisons the
corpus — it will be read six months from now as if it were sourced. Either stop and ask for the
paste, or write a stub with `status: transcript-pending` and no Key Takeaways section.

---

## Step 2 — Read the FULL transcript

Read every line. Don't skim, don't sample. Transcripts in this vault run 400–3,500 lines; for
anything beyond a single tool call, read in chunks with offset/limit until you've covered it all.
A page written from the first 500 lines of a 2,600-line talk is detectably shallow.

As you read, track:

- The core thesis or argument
- Specific techniques, tools, frameworks, and **named systems**
- Anything directly applicable to NQ trading, agent development, or consulting delivery
- Contrarian takes or challenges to how we currently operate
- Concrete numbers, benchmarks, or results (these make takeaways credible)
- **Claims that sound impressive but were never demonstrated** (see Step 3)

---

## Step 3 — Source-integrity check (do this before writing)

This is what separates a vault page from a summary. Run three checks and surface the results
*in the page itself*:

1. **Does the video match its title/framing?** Reuploads and clickbait retitles are common. If the
   title claims something the speaker never says, say so explicitly and identify what the talk
   actually is. (Precedent: a talk mislabeled as an Anthropic "no loops" video was a 2024 LangGraph
   conference talk — naming that turned a bad source into a genuine corpus insight about how the
   same author's thinking changed over two years.)
2. **Are the headline numbers demonstrated or asserted?** Marketing percentages ("73% fewer
   hallucinations", "72% win rate") are usually asserted with no methodology. Flag them as
   undemonstrated rather than repeating them as fact.
3. **For any backtest or benchmark: is there contamination or survivorship risk?** LLM trading
   results on well-known tickers are frequently contaminated by training data. Say it.

Being wrong is fine; being credulous is not. A page that flags its source's weaknesses is more
useful than one that launders them.

---

## Step 4 — Write the wiki page

**Path:** `youtube/transcripts/<descriptive-slug>.md` — concise kebab-case, under 60 chars, describing
the *topic* not the verbatim title. Prefer including the speaker when they're the draw
(`kyle-mistele-loop-engineering-control-theory`).

```markdown
---
title: "Video Title"
type: youtube
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [📺, <domain emoji>, 4-8 topical tags]
status: processed
url: "full-youtube-url"
channel: "Channel Name"
duration: "MM:SS"
published: "YYYY-MM-DD"
relevance: high | medium | low
deployment: personal | enterprise | both
related:
  - "[[moc/agent-engineering-patterns|Agent-Engineering Patterns MOC]]"
  - "[[projects/relevant-project/relevant-project|Readable Label]]"
sources:
  - https://www.youtube.com/watch?v=VIDEO_ID
---

# Video Title

<1–2 sentence opinionated framing: what this is, and why it earns a place in the vault.>

## Key Takeaways
## Relevance to Our Work
## Action Items
## Detailed Notes
## Full Transcript
```

### Frontmatter rules (lint-enforced — get these right)

- **`tags` must lead with an emoji category.** `📺` for every video, plus a domain emoji:
  `🤖` AI/agents · `🎯` trading · `💼` WaiveLabs/consulting · `📚` research. The linter audits this.
- **`deployment:` is required.** Which lane does this knowledge serve?
  `personal` (bang's own tooling/trading) · `enterprise` (client-deliverable) · `both`.
  This is how the corpus stays queryable by lane — do not omit it.
- **Wikilinks never carry a `.md` suffix.** `[[research/topics/loop-engineering]]`, never
  `[[research/topics/loop-engineering.md]]` — the latter resolves to `...md.md` and breaks the lint.
- **Never wikilink a skill name.** Skills aren't vault pages; use backticks: `` `client-build-package` skill ``.

### Section guidance

**Key Takeaways** (5–8 bullets) — insights, not summaries. Each stands alone as something worth
knowing. Include specific numbers, direct quotes, results. Mark the best 1–3 with 🔥.

> Bad: "The speaker discussed the importance of context windows in AI agents."
> Good: "Agent.md files burn ~944 tokens per turn whether needed or not. Skills use progressive
> disclosure — only 50 tokens (name + description) until triggered. For a 1000-line config,
> that's 18x token savings per conversation turn."

**Relevance to Our Work** — the most important section. Use `## ###` sub-headers, one per connection.
Connect to bang's actual projects with `[[wikilinks]]`. Be opinionated: say HOW, WHY, and WHAT we
should do differently. Name the pattern if it recurs across sources ("this is the 5th source for
generator ≠ verifier"). If the video *isn't* relevant, say so and explain why it's still worth having.

**Action Items** — `- [ ]` checkboxes. Concrete and assignable: "Adopt `ast-grep` as the structural
sensor for hygiene loops," not "consider looking into tooling."

**Detailed Notes** — organized by topic, not chronology. Sub-headers with timestamp ranges: `(04:05–06:30)`.
For someone who wants to go deeper without rewatching.

**Full Transcript** — collapsible pointer, never inline:

```markdown
<details>
<summary>Click to expand full transcript (N lines, Xm)</summary>

See raw transcript at: `raw/ingested/yt-VIDEO_ID-transcript.txt`

</details>
```

### Relevance rating

- **high** — directly applicable to trading, our platforms, or active projects; contains techniques we should evaluate or adopt
- **medium** — relevant domain, no immediate action items; good background
- **low** — tangential or entertainment; still worth having for search

---

## Step 5 — Archive the raw transcript

```bash
cp /tmp/yt-ingest/transcript.txt <vault-root>/raw/ingested/yt-VIDEO_ID-transcript.txt
```

Always archive — including pasted and Chrome-scraped transcripts. The page links to this path.

---

## Step 6 — Wire the indexes

Read `references/index-wiring.md` for the anchor-drift-safe recipe. Three targets, plus cross-links:

1. **`youtube/youtube-library.md`** — insert under the `## Recently Processed` anchor
2. **`log.md`** — insert under the `# Activity Log` anchor
3. **`moc/agent-engineering-patterns.md`** — for any AI/agent video, add a **Source Index row**.
   This is the highest-value step and the one most often skipped. The MOC is where patterns
   accumulate across sources; a page that isn't wired into it is effectively invisible.
4. **Bidirectional cross-links** — if the video is high-relevance to a project or an existing topic
   page, add a link *from that page back to the transcript*, not just forward. One-way links leave
   orphans in the graph.

> **Concurrency warning.** Multiple sessions edit this vault simultaneously. Anchor text drifts.
> Always `grep` the live anchor line immediately before a scripted replace, and assert on the
> string you just read — never on a string you remember from earlier in the session.

---

## Step 7 — Verify (required)

```bash
cd <vault-root> && python3 scripts/vault-lint.py
```

The vault carries known cross-layer links into the sibling `~/Cortana/Reports/` directory, which
the linter reports as broken by design. **Don't chase those.** What you must verify is that *your*
page added zero new breakage:

```bash
grep -oE '\[\[[^]|]+' youtube/transcripts/<slug>.md | sed 's/\[\[//' | sort -u | \
  while read t; do [ -f "$t.md" ] && echo "OK   $t" || echo "MISS $t"; done
```

Every target must resolve. Fix any `MISS` before reporting done.

---

## Step 8 — Report

Keep it tight — bang reads the page for details:

1. Title and channel
2. Relevance rating + one-sentence justification
3. Top 3 takeaways (not all 5–8)
4. Any source-integrity flags raised in Step 3
5. Urgent action items
6. Path to the page

---

## References

- `references/vault-conventions.md` — frontmatter, emoji tags, deployment lanes, naming, link rules
- `references/index-wiring.md` — anchor-drift-safe index/MOC update recipe
- `references/quality-bar.md` — worked examples of good vs. bad takeaways and relevance sections
