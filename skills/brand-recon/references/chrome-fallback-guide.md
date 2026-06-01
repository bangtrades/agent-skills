# Chrome Fallback Guide

Firecrawl is the default. It is fast, gives clean markdown, and supports the `branding` format which is uniquely valuable. **But firecrawl is blocked on several high-value sources** — particularly Meta-owned properties (Facebook, Instagram, Threads) and Pinterest. When that happens, fall through to Claude in Chrome.

## When to use Chrome MCP

Use Chrome MCP for:

1. **Meta properties** — Facebook, Instagram, Threads. Firecrawl returns "we do not support this site."
2. **Pinterest** — Same blocked status as Meta.
3. **LinkedIn pages and profiles** — Firecrawl returns rendered shells with no real content because LinkedIn is JS-heavy and auth-gated.
4. **Sites that JS-render their meaningful content** — symptom is firecrawl returns a page shell, a loading spinner, "enable JavaScript", or boilerplate navigation with no body content. Switch to Chrome to actually render the page.
5. **Any source where firecrawl returns 403 / 429 / "blocked"** after a reasonable retry — don't retry forever, escalate.
6. **Pages behind a login the user is already signed into in their browser** — like a private SaaS dashboard the user wants you to read. Chrome inherits their session.

Do NOT use Chrome for:
- Pages firecrawl can return in markdown form — Chrome is slower and noisier.
- Sources that require bypassing a paywall — capture what's visible on the public shell and stop.
- The first attempt at anything — try firecrawl first, escalate only on real failure.

## The access flow

Chrome MCP tools live under `mcp__Claude_in_Chrome__*`. They are typically deferred at session start. Load them all in one shot:

```
ToolSearch({ query: "chrome", max_results: 20 })
```

That returns the entire toolkit in a single call. Don't load tools one by one — that wastes round-trips.

Before any Chrome action, the user's Chrome extension must be connected. If it isn't, ask the user to install the Claude in Chrome extension rather than silently failing.

## The minimal Chrome scrape pattern

For socials (Facebook, Instagram, Pinterest, LinkedIn), this pattern is enough 90% of the time:

```
mcp__Claude_in_Chrome__navigate({ url: "https://www.facebook.com/{handle}" })
mcp__Claude_in_Chrome__get_page_text()
```

`get_page_text` returns the rendered DOM text — readable, no need to parse HTML. From the returned text, capture:
- Follower count / page likes
- Page category (e.g., "Sporting Goods Store")
- Verified badge presence
- Recent post snippets (first 3–5 posts)
- Date of most recent post (post cadence proxy)

For Instagram specifically:
```
mcp__Claude_in_Chrome__navigate({ url: "https://www.instagram.com/{handle}/" })
mcp__Claude_in_Chrome__get_page_text()
```
Capture: follower count, following count, post count, bio text, recent post captions visible above the fold.

For Pinterest:
```
mcp__Claude_in_Chrome__navigate({ url: "https://www.pinterest.com/{handle}/" })
mcp__Claude_in_Chrome__get_page_text()
```
Capture: monthly views, follower count, board names + sizes.

For LinkedIn:
```
mcp__Claude_in_Chrome__navigate({ url: "https://www.linkedin.com/company/{slug}/" })
mcp__Claude_in_Chrome__get_page_text()
```
Capture: employee headcount band (LinkedIn shows "11–50 employees" etc.), recent posts, activity cadence, company headline.

## Screenshots when text isn't enough

If `get_page_text` returns degenerate text (heavy iconography, JS not rendered, etc.), fall back to:

```
mcp__Claude_in_Chrome__computer({ action: "screenshot" })
```

Then visually inspect the screenshot. Useful for capturing visual brand cues directly from a competitor's site that firecrawl couldn't render properly.

## Rate-limit awareness

If you do many Chrome scrapes in a single run, the platforms will start serving you logged-out states, captchas, or rate-limit pages. Three guidelines:

1. **Cap at ~6 social scrapes per run.** Across FB/IG/Pinterest/TikTok/LinkedIn/YouTube — one each, no more.
2. **Don't scroll deep.** The first viewport is enough for follower count + cadence. Don't load infinite-scroll feeds.
3. **Don't click links.** Per Cowork's link safety rules, never click web links in Chrome with computer-use-style tools. Open new URLs with `navigate` instead.

## When Chrome itself is unavailable

If the Chrome extension is not installed or not connected in the current session, do NOT silently fail. Instead:

1. Tell the user in chat: "Chrome MCP isn't connected — I can install it via the extension, or fall back to WebSearch for approximate follower counts."
2. If they decline, fall through to WebSearch:
   ```
   WebSearch({ query: "{Entity} Facebook followers Instagram official social media stats" })
   ```
3. Mark each social source as `quality: low, access: search-only` in the playbook update — this is degraded but acceptable data.

## Capturing the Chrome run in the playbook

Every Chrome use should be noted in the Phase 14 playbook entry with `access: chrome` so the source-catalog file accumulates evidence over time. If a source consistently requires Chrome over many runs, that's a stable fact worth knowing — and a candidate for an alternative API-based MCP if one becomes available.
