# SF-Brand × PDFs

Use this with the **`pdf` skill** (and frequently the `docx` or HTML-to-PDF route) when producing branded PDFs for the Summer Fridays project.

## When this applies
Any PDF deliverable for the SF project — finalized reports for stakeholders, partnership decks exported as PDF, one-pagers, conference handouts, board reports, anything sent to people outside the working session.

## Choosing your source path

PDFs aren't usually authored directly — they're rendered from a source. Pick the right source for the job:

| Source | Best for | Render path |
|---|---|---|
| **Word (.docx)** | Long-form reports, briefs, memos with running headers/footers | Open in Word/LibreOffice → Export to PDF; or use `docx2pdf` (mac) / `unoconv` (linux) |
| **HTML/CSS** | Cinematic one-pagers, dashboards, data-heavy reports, anything where you want full control | `weasyprint` (canonical), `playwright` headless print-to-PDF, or `puppeteer` |
| **PowerPoint (.pptx)** | When the deck is the deliverable | PowerPoint export → PDF, or `unoconv -f pdf` |
| **ReportLab native** | Receipts, certificates, table-heavy operational docs | Programmatic, but harder to make brand-elegant |

For SF deliverables, **prefer the HTML/WeasyPrint route** for any one-pager or report where layout matters. The brand reads "editorial," and HTML+CSS gives you the most editorial control.

## HTML + WeasyPrint pattern (recommended for SF)

WeasyPrint supports CSS Paged Media, custom fonts, page breaks, headers, footers — all the editorial controls you need.

### The brand CSS stylesheet

```css
/* sf-brand.css — drop into your HTML <head> via <link> or inline */

@import url("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400;1,500&display=swap");

@font-face {
  font-family: "Futura PT";
  src: local("Futura PT"), local("Avenir Next"), local("Avenir"), local("Helvetica Neue");
  font-weight: 400 500;
}

:root {
  --ink: #1A1A1A;
  --ink-60: #5C5C5C;
  --ink-30: #A8A8A8;
  --chalk: #FAF6EF;
  --white: #FFFFFF;
  --morning-sky: #BDD7E5;
  --morning-sky-deep: #7DA8BD;
  --clay: #C9A582;
  --vanilla: #F5E9DD;
  --pink-sugar: #FC88AB;
  --pink-guava: #B44F65;
  --hot-cocoa: #6B3D2E;
  --accent-blue: #3C5A78;
  --muted-border: #E5E5EB;
  --font-body: "Futura PT", "Avenir Next", Avenir, "Helvetica Neue", Helvetica, Arial, sans-serif;
  --font-display: "Cormorant Garamond", Georgia, serif;
}

/* ---- Page setup ---- */
@page {
  size: Letter;
  margin: 1in 1.1in 1in 1.1in;
  background: var(--chalk);

  @bottom-left {
    content: "Summer Fridays  ·  Confidential";
    font-family: var(--font-body);
    font-size: 8pt;
    color: var(--ink-60);
  }
  @bottom-right {
    content: "Page " counter(page) " of " counter(pages);
    font-family: var(--font-body);
    font-size: 8pt;
    color: var(--ink-60);
  }
}

@page :first {
  /* Cover gets no footer */
  @bottom-left { content: none; }
  @bottom-right { content: none; }
}

/* ---- Base typography ---- */
html, body {
  font-family: var(--font-body);
  font-size: 11pt;
  line-height: 1.55;
  color: var(--ink);
  background: var(--chalk);
  font-weight: 450;
  letter-spacing: 0.013em;
}

h1 {
  font-size: 22pt;
  font-weight: 500;
  margin: 24pt 0 12pt;
  letter-spacing: 0.025em;
}

h2 {
  font-size: 16pt;
  font-weight: 500;
  margin: 20pt 0 10pt;
}

h3 {
  font-size: 12pt;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--morning-sky-deep);
  margin: 16pt 0 8pt;
}

.lead {
  font-size: 13pt;
  line-height: 1.5;
}

p { margin: 0 0 8pt; }

a { color: var(--accent-blue); text-decoration: none; border-bottom: 0.5pt solid var(--accent-blue); }

blockquote {
  font-family: var(--font-display);
  font-size: 18pt;
  font-style: italic;
  color: var(--ink);
  border-left: 3pt solid var(--morning-sky);
  padding-left: 0.5in;
  margin: 18pt 0;
}

/* ---- Cover page ---- */
.cover {
  page-break-after: always;
  height: 9in;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.cover .eyebrow {
  font-size: 10pt;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--ink-60);
}

.cover .title {
  font-size: 36pt;
  font-weight: 500;
  line-height: 1.1;
  letter-spacing: 0.02em;
  margin: 0.4in 0 0.15in;
}

.cover .subtitle {
  font-family: var(--font-display);
  font-size: 18pt;
  font-style: italic;
  color: var(--ink-60);
}

.cover .accent-rule {
  width: 1.5in;
  height: 2pt;
  background: var(--morning-sky);
  margin: 0.25in 0;
}

.cover .meta {
  font-size: 9pt;
  color: var(--ink-60);
  letter-spacing: 0.05em;
}

/* ---- Section dividers ---- */
.section-divider {
  page-break-before: always;
  margin-top: 3in;
}
.section-divider .eyebrow { font-size: 10pt; color: var(--ink-60); letter-spacing: 0.12em; }
.section-divider h1 { font-size: 32pt; margin: 0.2in 0 0.1in; }
.section-divider hr { border: none; border-top: 1pt solid var(--morning-sky); width: 100%; margin: 0; }

/* ---- Tables ---- */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 12pt 0;
  font-size: 10pt;
}
thead th {
  background: var(--morning-sky);
  color: var(--ink);
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 8pt 10pt;
  text-align: left;
  border-bottom: 1pt solid var(--morning-sky-deep);
}
tbody td {
  padding: 6pt 10pt;
  border-bottom: 0.5pt solid var(--muted-border);
  vertical-align: top;
}
tbody tr:nth-child(even) td { background: var(--chalk); }
tbody tr:nth-child(odd) td { background: var(--white); }
tfoot td { background: var(--vanilla); font-weight: 600; border-top: 1pt solid var(--morning-sky-deep); }

/* ---- Callout boxes ---- */
.callout {
  padding: 16pt 20pt;
  margin: 12pt 0;
  border-radius: 2pt;
}
.callout--sky     { background: var(--morning-sky); }
.callout--vanilla { background: var(--vanilla); }
.callout--clay    { background: var(--clay); color: var(--ink); }
.callout--pink    { background: var(--pink-sugar); }

.callout .label {
  font-size: 9pt;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--ink);
  font-weight: 500;
  margin-bottom: 6pt;
}
.callout .body {
  font-size: 11pt;
  color: var(--ink);
  line-height: 1.5;
  margin: 0;
}

/* ---- Stat block (big number) ---- */
.stat {
  text-align: center;
  margin: 18pt 0;
}
.stat .value {
  font-size: 48pt;
  font-weight: 300;
  color: var(--morning-sky-deep);
  line-height: 1;
}
.stat .label {
  font-size: 10pt;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--ink-60);
  margin-top: 6pt;
}

/* ---- Sources footer ---- */
.sources {
  font-size: 9pt;
  color: var(--ink-60);
  border-top: 0.5pt solid var(--ink-30);
  padding-top: 12pt;
  margin-top: 24pt;
}
.sources a { color: var(--accent-blue); }
```

### HTML structure pattern

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Document Title</title>
  <link rel="stylesheet" href="sf-brand.css">
</head>
<body>

  <!-- Cover page -->
  <section class="cover">
    <div>
      <div class="eyebrow">Summer Fridays  ·  Marketing Intelligence</div>
    </div>
    <div>
      <div class="title">Document Title</div>
      <div class="subtitle">A short editorial subtitle that sets the scene</div>
      <div class="accent-rule"></div>
    </div>
    <div>
      <div class="meta">Cortana · 17 May 2026 · Confidential — Internal Working Document</div>
    </div>
  </section>

  <!-- Body -->
  <h1>Executive summary</h1>
  <p class="lead">The lead paragraph carries the headline insight in slightly larger type.</p>
  <p>Subsequent paragraphs are standard body. Light, easy, breathable — match the brand's reading rhythm.</p>

  <div class="callout callout--sky">
    <div class="label">Recommendation</div>
    <p class="body">The thing we should do, stated plainly.</p>
  </div>

  <h2>Section heading</h2>
  <p>Body content.</p>

  <h3>Sub-section in morning-sky-deep uppercase</h3>
  <p>More content.</p>

  <table>
    <thead><tr><th>Metric</th><th>Value</th><th>Source</th></tr></thead>
    <tbody>
      <tr><td>Sephora skincare share</td><td>10.5%</td><td>BoF / WWD</td></tr>
      <tr><td>Annual retail revenue</td><td>$244M</td><td>Double V Consulting</td></tr>
    </tbody>
  </table>

  <blockquote>
    "Every day should feel like a Summer Friday."
  </blockquote>

  <!-- Section divider -->
  <section class="section-divider">
    <div class="eyebrow">Part 02</div>
    <h1>Section Title</h1>
    <hr>
  </section>

  <p>Next section content.</p>

  <!-- Sources -->
  <div class="sources">
    <strong>Sources</strong><br>
    1. <a href="https://summerfridays.com">summerfridays.com</a><br>
    2. <a href="https://www.businessoffashion.com/articles/beauty/summer-fridays-vanilla-fragrance-lip-balm/">BoF — Summer Fridays Vanilla Fragrance</a>
  </div>

</body>
</html>
```

### Render to PDF

```python
from weasyprint import HTML, CSS
HTML("input.html").write_pdf(
    "output.pdf",
    stylesheets=[CSS(filename="sf-brand.css")],
)
```

## Working from a Word source

If the deliverable starts as a Word doc (because it'll be edited by humans), follow the `docx-instructions.md` patterns first, then convert:

```bash
# On macOS, using LibreOffice headless (preferred for fidelity)
soffice --headless --convert-to pdf:writer_pdf_Export source.docx --outdir ./output/

# Or with docx2pdf if Word is installed
python -c "from docx2pdf import convert; convert('source.docx', 'output.pdf')"
```

## Pattern checklist before sending a PDF

- [ ] Cover page on its own page, no footer/header
- [ ] Body pages have "Summer Fridays · Confidential" left-footer and page numbers
- [ ] Brand font renders (test on the target machine — embed fonts in PDF if portability matters)
- [ ] All hex colors come from the brand palette — no random reds, blues
- [ ] Tables use MORNING_SKY headers, CHALK zebra
- [ ] Hyperlinks render in ACCENT_BLUE
- [ ] Sources section at the end, linked
- [ ] File size reasonable (compress images if >5MB)
- [ ] Filename pattern: `SF_<topic>_<YYYY-MM-DD>.pdf`
- [ ] Saved to project folder, presented via present_files
