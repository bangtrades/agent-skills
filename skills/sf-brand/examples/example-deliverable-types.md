# Example deliverables — what the SF-Brand skill produces

These are intended outputs that the skill should be able to drive consistently. Use them as visual targets when iterating on the skill.

## 1. Quarterly Marketing Intelligence Brief (PDF, 8–15 pages)

**Source:** HTML → WeasyPrint
**Cover accent:** MORNING_SKY (skincare/business default)
**Sections:**
- Cover with Cormorant italic subtitle
- Executive summary (lead paragraph + 3 sky callouts: top wins / top risks / top opportunity)
- §1 Business snapshot (table + stat callouts)
- §2 Channel performance (per-channel sub-sections, each with one chart)
- §3 Competitive movement (positioning table)
- §4 Recommendations (sky callouts, one per H1–H8 hypothesis)
- Sources

## 2. Campaign Brief (Word, 4–6 pages)

**Source:** docx via python-docx
**Cover accent:** matches campaign (PINK_SUGAR for lip; VANILLA for fragrance; MORNING_SKY for skincare; CLAY for travel/retail)
**Sections:**
- Cover with campaign title + dates
- Objectives (3 bullets)
- Audience persona (rich bullets)
- Channel + creative table
- KPIs table
- Pull quote (founder/community POV)
- Timeline table
- Approvals row at end

## 3. Creator Campaign Tracker (Excel, 4 sheets)

**Source:** xlsx via openpyxl
**Sheets:**
- README (cover + sheet index + sources)
- Roster (creator handle, tier, market, rate, status with success/risk conditional fill)
- Performance (one row per post, with EMV calculation column)
- Pivot summary (rolled up by tier × market, with embedded bar chart in MORNING_SKY_DEEP)

## 4. Partnership Pitch Deck (PPTX, 10–14 slides)

**Source:** pptx via python-pptx
**Cover accent:** CLAY (for travel/lifestyle partnerships) or matches partner brand
**Slides:**
- Cover (60pt title, Cormorant italic subtitle)
- SF in 60 seconds (3 stat callouts: $244M / 10.5% Sephora / 1 LBB every 17s)
- The partner in 60 seconds
- Why now (chart slide)
- Section divider — The Idea (CLAY)
- The big idea (one slide, large type)
- Activation plan (3-card layout)
- Brand fit + audience overlap (Venn / overlap visual)
- Section divider — Measurement (MORNING_SKY)
- KPIs + measurement plan
- Timeline
- Ask + next step
- Thank you closing slide

## 5. Marketing Performance Snapshot (HTML dashboard, single page)

**Source:** HTML + brand-palette.css + Chart.js or embedded SVG
**Layout:**
- Eyebrow + title at top
- 4-up KPI cards (MORNING_SKY_DEEP big numbers)
- 2-up chart row (trend + share)
- 2-up table row (top creators + top SKUs)
- Footer with refresh date + sources

## 6. One-Pager / Memo (PDF, 1 page)

**Source:** HTML → WeasyPrint or markdown → docx → PDF
**Layout:**
- Top eyebrow + title + one-line subtitle + thin MORNING_SKY rule
- Lead paragraph (the headline insight)
- Three short paragraphs OR one sky callout + supporting paragraph
- Sources at bottom (small, INK_60)
- Single page, generous chalk margins

---

## What good looks like

A successful SF brand-deliverable:

1. **Reads like a magazine, not a McKinsey deck.** Editorial whitespace, soft palette, italic Cormorant subtitle.
2. **Stays factually precise.** Numbers cited with sources. No "leading" — use the actual share %.
3. **Honors the founders' voice.** First-person plural ("we"), sensorial vocabulary, no consultancy jargon.
4. **Uses one accent story per page.** Don't mix Pink Sugar + Hot Cocoa in the same callout row.
5. **Always cites sources.** Markdown-style [Title](URL) at the end.
6. **Never uses pure white as a full-page background.** Always CHALK.
7. **Looks effortless.** If it took 200 layout fixes, it doesn't look on-brand.

## What bad looks like

- Calibri or Times anywhere
- Random reds and blues from a default chart palette
- "Leveraging actionable insights to optimize Q4 spend"
- Pure white page with grey 10pt Arial — feels like a tax form, not a beauty brief
- Cherry red callout next to Pink Sugar callout next to Sky callout — visual chaos
- Logos copy-pasted from Google image search at 72dpi
- Stock photography of generic skincare jars that aren't SF products
