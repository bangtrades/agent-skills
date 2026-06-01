---
name: yt
description: >
  Process a YouTube video into a Cortana vault wiki page. Use this skill whenever a user shares
  a YouTube URL (youtube.com, youtu.be), says "/youtube", mentions processing a video, or pastes
  a bare URL that looks like a YouTube link. Even without explicit instructions — if the message
  contains a YouTube URL, use this skill. Also trigger on "pull the transcript", "ingest this video",
  "watch this", or any reference to turning video content into vault knowledge. This skill handles
  the full pipeline: transcript extraction via yt-dlp, metadata pull, opinionated wiki page with
  key takeaways and relevance analysis, raw transcript archival, and vault index updates.
---

# YT — YouTube → Cortana Vault

You're turning a YouTube video into a permanent, searchable knowledge page in bang's Cortana
vault (an Obsidian wiki). Bang trades NQ futures, builds AI agent platforms, and runs an AI
consulting practice. Everything you write should be filtered through: **how does this connect
to trading edge, AI tooling, or the consulting business?**

The quality bar is high. A good page is one bang can find 6 months from now via Obsidian search
and immediately get value from. A bad page is a generic summary he could have gotten from ChatGPT.

---

## Vault Location

The vault root is the workspace folder (typically mounted at the path containing `cortana-vault/`).
All paths below are relative to the vault root.

---

## Step 1 — Extract transcript and metadata

Run the bundled extraction script:

```bash
python <this-skill-dir>/scripts/yt_extract.py "VIDEO_URL" --output-dir /tmp/yt-ingest
```

This produces:
- `/tmp/yt-ingest/metadata.json` — title, channel, duration, upload_date, views, video_id, url
- `/tmp/yt-ingest/transcript.txt` — timestamped lines in `[MM:SS] text` format

If yt-dlp isn't installed: `pip install yt-dlp --break-system-packages`

If the URL contains extra parameters (like `&t=1761s`), pass it through as-is — yt-dlp handles it.

---

## Step 2 — Read the FULL transcript

Read every line. Don't skim, don't sample. For long transcripts that exceed tool limits, read
in chunks with offset/limit until you've covered the whole thing.

As you read, track:
- The core thesis or argument
- Specific techniques, tools, or frameworks mentioned
- Anything directly applicable to NQ trading, agent development, or consulting delivery
- Contrarian takes or challenges to how we currently operate
- Concrete numbers, benchmarks, or results (these make takeaways credible)

---

## Step 3 — Write the wiki page

**Path:** `youtube/transcripts/<descriptive-slug>.md`

The slug should be a concise, descriptive kebab-case version of the video's topic — not just
the video title verbatim. Keep it under 60 characters.

### Page template

```markdown
---
title: "Video Title"
type: youtube
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [4-8 relevant tags]
status: processed
url: "full-youtube-url"
channel: "Channel Name"
duration: "MM:SS"
published: "YYYY-MM-DD"
relevance: high | medium | low
related: ["[[projects/relevant-project/relevant-project]]"]
---

# Video Title

## Key Takeaways

## Relevance to Our Work

## Action Items

## Detailed Notes

## Full Transcript
<details>
<summary>Click to expand full transcript (N lines, Xm)</summary>

See raw transcript at: raw/ingested/yt-VIDEO_ID-transcript.txt

</details>
```

### Section guidance

**Key Takeaways** (5-8 bullets)

These are insights, not summaries. Each bullet should stand alone as something worth knowing.
Include specific numbers, quotes, or results — not "the speaker discussed X."

Bad: "The speaker discussed the importance of context windows in AI agents."
Good: "Agent.md files burn ~944 tokens per turn whether needed or not. Skills use progressive
disclosure — only 50 tokens (name + description) until triggered. For a 1000-line config,
that's 18x token savings per conversation turn."

**Relevance to Our Work**

The most important section. Connect the video's content to bang's actual projects and tools.
Use `[[wikilinks]]` to reference vault pages. Be opinionated — say HOW and WHY and WHAT
specifically we should do differently. If the video isn't relevant, say so and explain why
it's still worth having in the vault.

**Action Items** (checkbox format)

Concrete next steps: "Evaluate X for our trading setup." "Test Y approach in the Wick App."
"Create a research curriculum on Z." Use `- [ ]` format.

**Detailed Notes**

Organized by topic (not chronologically). Group related ideas under sub-headers. Include
timestamps for key moments: `(12:34)`. This section is for someone who wants to go deeper
on a specific topic without rewatching the whole video.

### Relevance rating

- **high** — Directly applicable to trading, our platforms, or active projects. Contains
  techniques/tools we should evaluate or adopt.
- **medium** — Relevant domain (AI, trading, engineering) but no immediate action items.
  Good background knowledge.
- **low** — Tangentially related or mostly entertainment. Still worth having for search.

### Tags

Use 4-8 tags. Include: primary topic, specific technologies/tools mentioned, the domain
(trading, ai-agents, skill-creation, web-design, etc.), and any vault project connections.

---

## Step 4 — Archive the raw transcript

```bash
cp /tmp/yt-ingest/transcript.txt <vault-root>/raw/ingested/yt-VIDEO_ID-transcript.txt
```

---

## Step 5 — Update vault indexes

### youtube-library.md

Add to the "Recently Processed" section at the top:

```markdown
- [[youtube/transcripts/<slug>|Video Title]] — Channel (duration, relevance) — one-line summary
```

### log.md

Append a log entry:

```markdown
## [YYYY-MM-DD] youtube | Video Title

- **type**: youtube
- **source**: URL
- **channel**: Channel Name
- **relevance**: high | medium | low
- **details**: One sentence on what the video covers and why it matters
- **pages touched**: [[youtube/transcripts/<slug>]], [[youtube/youtube-library]]
```

### Cross-references

If the video is high-relevance to a specific project, add a note to that project's overview
page linking back to the transcript. This enriches the vault graph.

---

## Step 6 — Report to the user

Give a concise summary:

1. Title and channel
2. Relevance rating + one-sentence justification
3. Top 3 takeaways (not all 5-8)
4. Any urgent action items
5. Link to the wiki page

Keep it tight. The user can read the full page for details.
