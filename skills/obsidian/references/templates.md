# Page Templates

Use these templates when creating wiki pages. Fill in the sections — don't leave placeholders
or empty sections. If a section genuinely doesn't apply, omit it rather than leaving it blank.

---

## Project Overview

Use when creating a new project.

```markdown
---
title: "{{title}}"
type: project
created: {{date}}
updated: {{date}}
tags: [{{emoji}}]   # 🎯🤖📺💼🔧📚 — pick one category emoji, then add text tags
status: active
sources: []
related: []
---

# {{title}}

## Summary
<!-- What is this project and why does it matter? -->

## Architecture
<!-- Key technical decisions, stack, structure -->

## Current Status
<!-- Where things stand right now -->

## Key Decisions
<!-- Important choices made and their rationale -->

## Open Questions
<!-- Unresolved issues, next steps -->

## Session History
<!-- Links to session summaries, most recent first -->
```

---

## Session Summary

Use when processing a work session transcript.

```markdown
---
title: "{{title}}"
type: session
created: {{date}}
updated: {{date}}
tags: [{{emoji}}]   # 🎯🤖📺💼🔧📚 — pick one category emoji, then add text tags
status: completed
project: "[[projects/slug/slug|Project Name]]"
session_id: ""
sources: []
related: []
---

# {{title}}

## What We Did
<!-- High-level summary of the session -->

## Key Outcomes
<!-- Concrete deliverables, decisions, or artifacts produced -->

## Technical Details
<!-- Important implementation details, code changes, architecture decisions -->

## Insights & Takeaways
<!-- What did we learn? What's the implication for the broader work? -->

## Next Steps
<!-- What follows from this session? -->
```

---

## Research Curriculum

Use when generating a learning path from a topic or URL.

```markdown
---
title: "{{title}}"
type: curriculum
created: {{date}}
updated: {{date}}
tags: [{{emoji}}]   # 🎯🤖📺💼🔧📚 — pick one category emoji, then add text tags
status: draft
source_url: ""
estimated_hours: 0
related: []
---

# {{title}}

## Why This Matters
<!-- Connection to bang's trading/AI work — be specific and opinionated -->

## Prerequisites
<!-- What you should know before starting -->

## Learning Path

### Module 1: {{module_title}}
**Time estimate:** {{hours}}
**Objective:** {{what you'll be able to do after this module}}

#### Resources
- {{specific article, video, paper, or tool with URL}}

#### Exercises
- {{hands-on exercise tied to bang's actual projects}}

---

### Module 2: {{module_title}}
<!-- repeat pattern, 3-7 modules total -->

---

## Connections to Current Work
<!-- How this knowledge applies to active projects — reference specific vault pages -->

## Progress Tracker
- [ ] Module 1
- [ ] Module 2
```

---

## YouTube Transcript

Use when processing a YouTube video.

```markdown
---
title: "{{title}}"
type: youtube
created: {{date}}
updated: {{date}}
tags: [{{emoji}}]   # 🎯🤖📺💼🔧📚 — pick one category emoji, then add text tags
status: processed
url: "{{youtube_url}}"
channel: "{{channel_name}}"
duration: "{{HH:MM:SS}}"
published: "{{YYYY-MM-DD}}"
relevance: high | medium | low
related: []
---

# {{title}}

## Key Takeaways
<!-- 5-8 bullet summary of the most important points -->

## Relevance to Our Work
<!-- How does this connect to trading, AI tooling, or active projects? -->

## Action Items
<!-- Features to evaluate, techniques to try, ideas to explore -->

## Detailed Notes
<!-- Structured notes organized by topic -->

## Full Transcript
<details>
<summary>Click to expand full transcript</summary>

{{raw_transcript}}

</details>
```

---

## Directory Overview (Tier 1 Ingestion)

Use when ingesting a directory. This is the compact summary page.

```markdown
---
title: "{{title}}"
type: project
created: {{date}}
updated: {{date}}
tags: [{{tags}}]
status: active
source_dir: "{{original_dirname}}"
total_files: {{count}}
archive: "raw/ingested/{{dirname}}"
sources: ["{{dirname}}"]
related: []
---

# {{title}}

> {{one_liner}}

**Source:** `inbox/{{dirname}}/` ({{count}} files) | **Archived:** `raw/ingested/{{dirname}}/` | **Ingested:** {{date}}

## Overview

{{2-4 paragraph summary}}

## Categories

- **{{category_name}}** ({{count}} items) — {{standout items}}

## Highlights

- {{highlight with brief why}}

## Relevance

{{connection to trading/AI work}}

## Recommended Deep Dives

- {{specific item worth a full page}}

> [!tip] On-demand deep dives
> Full source archived at `raw/ingested/{{dirname}}/`.
> ```bash
> python scripts/deep-dive.py "{{dirname}}" --search "keyword"
> python scripts/deep-dive.py "{{dirname}}" "path/to/item"
> ```

## Directory Structure

\```
{{tree}}
\```

## Search Keywords

{{comma-separated searchable terms}}
```

---

## Deep Dive Page (Tier 2 Materialization)

Use when materializing a specific item from an archive.

```markdown
---
title: "{{item_title}}"
type: source
created: {{date}}
updated: {{date}}
tags: [deep-dive, {{project-slug}}]
status: active
source_file: "raw/ingested/{{archive}}/{{rel_path}}"
project: "[[projects/{{slug}}/{{slug}}|{{Project Name}}]]"
related: []
---

# {{item_title}}

> **Source:** `{{rel_path}}` from `{{archive}}/` | **Deep dive:** {{date}}

## Summary
<!-- One paragraph — what is this and why does it matter -->

## Details
<!-- Thorough explanation of contents, purpose, usage -->

## Key Takeaways
<!-- Bullet points — the things worth remembering -->

## Relevance
<!-- How this connects to trading/AI development -->

## Related
<!-- [[wikilinks]] to connected concepts and projects -->
```
