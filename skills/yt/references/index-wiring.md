# Index wiring — the anchor-drift-safe recipe

## Why this file exists

Multiple agent sessions write to this vault at the same time. A scripted `str.replace()` against
an anchor you read earlier in the session **will** eventually fail, because another session edited
the anchor line in between (this has happened — a MOC assertion blew up because the anchor had
picked up a stray list prefix).

**Rule: grep the live anchor immediately before replacing, and assert on the string you just read.**

## The four wiring targets

### 1. `youtube/youtube-library.md`

Insert directly under the `## Recently Processed` anchor:

```markdown
- [[youtube/transcripts/<slug>|Video Title]] — Channel (MM:SS, relevance) — one-line summary
```

### 2. `log.md`

Insert directly under the `# Activity Log` anchor:

```markdown
## [YYYY-MM-DD] youtube | Video Title

- **type**: youtube
- **source**: URL
- **channel**: Channel Name
- **relevance**: high | medium | low
- **details**: One sentence on what it covers and why it matters
- **pages touched**: [[youtube/transcripts/<slug>]], [[youtube/youtube-library]], [[moc/agent-engineering-patterns]]
```

### 3. `moc/agent-engineering-patterns.md` — the high-value one

For any AI/agent video, append a row to the **Source Index** table. This is where patterns compound
across sources; an unwired page is effectively invisible to future synthesis.

```markdown
| [[youtube/transcripts/<slug>\|Title (Speaker)]] | Channel | **Pattern refs** — what this source adds that others don't. Name the mechanism. Note if it's the Nth source for a recurring pattern. |
```

Note the escaped pipe `\|` inside table cells — an unescaped one breaks the table.

If the video establishes or materially advances a *pattern*, also edit the relevant pattern section
in the body of the MOC, not just the index row.

### 4. Bidirectional cross-links

Forward-only linking creates orphans. If the video is high-relevance to a project or an existing
topic page, **edit that page to link back**. When two pages cover the same subject from different
sources, add a short callout to each explaining how they differ — that framing is usually more
valuable than either page alone.

## Safe scripted-edit pattern

```python
import io
p = "moc/agent-engineering-patterns.md"
s = io.open(p, encoding="utf-8").read()

# 1. Find the live anchor line — do NOT hardcode remembered text
anchor = [l for l in s.splitlines() if l.startswith("| [[youtube/transcripts/known-neighbor")]
assert anchor, "anchor row not found — re-grep, the file changed"
anchor_line = anchor[0]

# 2. Replace against the string just read, exactly once
newrow = "| [[youtube/transcripts/new-slug\\|Title]] | Channel | pattern notes |"
s = s.replace(anchor_line, anchor_line + "\n" + newrow, 1)

io.open(p, "w", encoding="utf-8").write(s)
```

Always `assert` before writing, always pass `1` as the replace count, always write UTF-8.

## Verify after wiring

```bash
cd <vault-root> && python3 scripts/vault-lint.py
```

Then confirm your page specifically added no breakage:

```bash
grep -oE '\[\[[^]|]+' youtube/transcripts/<slug>.md | sed 's/\[\[//' | sort -u | \
  while read t; do [ -f "$t.md" ] && echo "OK   $t" || echo "MISS $t"; done
```

The vault carries a standing count of `Reports/`-layer "broken" links — those are cross-layer and
expected. Judge yourself on the delta, not the absolute number.
