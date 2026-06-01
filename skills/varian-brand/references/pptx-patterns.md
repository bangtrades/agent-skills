# Varian Brand — Presentation (pptx) Code Patterns

Tested patterns for `pptxgenjs` (v3.x+). These produce the dark-mode executive deck style validated across a 13-slide CEO pitch deck.

## Table of Contents

1. [Constants & Setup](#1-constants--setup)
2. [Icon Rendering Pipeline](#2-icon-rendering-pipeline)
3. [Card Component](#3-card-component)
4. [Stat Card Component](#4-stat-card-component)
5. [Title Slide](#5-title-slide)
6. [Content Slide Template](#6-content-slide-template)
7. [Timeline / Multi-Card Slide](#7-timeline--multi-card-slide)
8. [Hub-and-Spoke Diagram](#8-hub-and-spoke-diagram)
9. [Domain Color Assignments](#9-domain-color-assignments)

---

## 1. Constants & Setup

```javascript
const pptxgen = require("pptxgenjs");

// ── DARK MODE PALETTE ─────────────────────────────────────────
const DARK = "0A1628", DARK2 = "0F1F3D", DARK3 = "162A50";
const PETROL = "009999", PETROL_LIGHT = "00CCCC";
const ORANGE = "EC6602", ORANGE_LIGHT = "FF8534";
const WHITE = "FFFFFF", GRAY = "8A9BB5", LIGHT = "C5D3E8";
const GREEN = "2DD4A8", PURPLE = "A855F7", BLUE_BRIGHT = "3B82F6";
const CARD_BG = "111D35";
const AMBER = "F59E0B";

const P = new pptxgen();
P.layout = "LAYOUT_16x9";
P.author = "Siemens Healthineers | Varian";
P.title = "Presentation Title";
```

## 2. Icon Rendering Pipeline

Uses `react-icons` rendered to SVG, then converted to PNG via `sharp` for embedding in slides.

```javascript
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const { FaRobot, FaBrain, FaChartLine /* etc */ } = require("react-icons/fa");

function renderIconSvg(IC, color = "#000000", size = 256) {
  return ReactDOMServer.renderToStaticMarkup(
    React.createElement(IC, { color, size: String(size) })
  );
}

async function icon(IC, color, size = 256) {
  const svg = renderIconSvg(IC, color, size);
  return "image/png;base64," +
    (await sharp(Buffer.from(svg)).png().toBuffer()).toString("base64");
}

// Pre-render all icons at build time:
const I = {};
const defs = [
  ["robot", FaRobot, PETROL_LIGHT],
  ["brain", FaBrain, PURPLE],
  ["chart", FaChartLine, GREEN],
  // ... etc
];
for (const [n, c, col] of defs) I[n] = await icon(c, `#${col}`, 256);
```

## 3. Card Component

The fundamental container. A dark rectangle with an accent-colored top bar and drop shadow.

```javascript
const mkSh = () => ({
  type: "outer", blur: 8, offset: 3, angle: 135,
  color: "000000", opacity: 0.3
});

function card(slide, x, y, w, h, accentColor = PETROL) {
  // Background
  slide.addShape("rect", {
    x, y, w, h,
    fill: { color: CARD_BG },
    shadow: mkSh()
  });
  // Accent bar (top edge)
  slide.addShape("rect", {
    x, y, w, h: 0.04,
    fill: { color: accentColor }
  });
}
```

## 4. Stat Card Component

Card with a large metric value and label. Used for KPI rows.

```javascript
function statCard(slide, x, y, w, h, stat, label, accentColor = PETROL) {
  card(slide, x, y, w, h, accentColor);
  // Large stat value
  slide.addText(stat, {
    x, y: y + 0.12, w, h: 0.5,
    fontSize: 30, fontFace: "Calibri",
    color: accentColor, bold: true,
    align: "center", valign: "middle", margin: 0
  });
  // Label below
  slide.addText(label, {
    x, y: y + 0.62, w, h: 0.35,
    fontSize: 10, fontFace: "Calibri",
    color: GRAY,
    align: "center", valign: "top", margin: 0
  });
}
```

## 5. Title Slide

```javascript
let s = P.addSlide();
s.background = { color: DARK };

// Left accent bar (full height)
s.addShape("rect", {
  x: 0, y: 0, w: 0.06, h: 5.625,
  fill: { color: PETROL }
});

// Bottom accent line
s.addShape("rect", {
  x: 0, y: 5.2, w: 10, h: 0.06,
  fill: { color: ORANGE, transparency: 40 }
});

// Organization line
s.addText("SIEMENS HEALTHINEERS  |  VARIAN", {
  x: 0.7, y: 0.5, w: 8.5, h: 0.35,
  fontSize: 12, fontFace: "Calibri", color: GRAY,
  charSpacing: 4, margin: 0
});

// Main title (two-color split)
s.addText([
  { text: "Title Line One", options: {
    fontSize: 44, fontFace: "Calibri", color: WHITE, bold: true, breakLine: true
  }},
  { text: "Title Line Two", options: {
    fontSize: 44, fontFace: "Calibri", color: PETROL_LIGHT, bold: true
  }},
], { x: 0.7, y: 1.3, w: 6, h: 2, valign: "top", margin: 0 });

// Tagline
s.addText("Subtitle or description text", {
  x: 0.7, y: 3.1, w: 6, h: 0.4,
  fontSize: 16, fontFace: "Calibri", color: LIGHT, margin: 0
});

// Orange divider rule
s.addShape("rect", {
  x: 0.7, y: 3.65, w: 1.8, h: 0.04,
  fill: { color: ORANGE }
});

// Metadata line
s.addText("Date  |  Classification  |  Audience", {
  x: 0.7, y: 3.85, w: 5, h: 0.35,
  fontSize: 11, fontFace: "Calibri", color: GRAY, margin: 0
});

// Hero icon (large faded background + sharp foreground)
s.addImage({ data: I.brainW, x: 6.8, y: 1.2, w: 2.5, h: 2.5, transparency: 85 });
s.addImage({ data: I.brain, x: 7.2, y: 1.6, w: 1.8, h: 1.8 });

// Bottom bar
s.addShape("rect", {
  x: 0, y: 5.25, w: 10, h: 0.375,
  fill: { color: DARK2 }
});
s.addText("Domain 1  |  Domain 2  |  Domain 3  |  Domain 4  |  Domain 5", {
  x: 0.5, y: 5.27, w: 9, h: 0.35,
  fontSize: 10, fontFace: "Calibri", color: GRAY, margin: 0
});
```

## 6. Content Slide Template

Every content slide follows this base pattern:

```javascript
s = P.addSlide();
s.background = { color: DARK };

// Top accent bar (section-colored)
s.addShape("rect", {
  x: 0, y: 0, w: 10, h: 0.04,
  fill: { color: PETROL } // or ORANGE, AMBER, etc.
});

// Slide title
s.addText("Slide Title", {
  x: 0.7, y: 0.3, w: 8, h: 0.5,
  fontSize: 28, fontFace: "Calibri", color: WHITE, bold: true, margin: 0
});

// Subtitle
s.addText("Supporting context or description.", {
  x: 0.7, y: 0.85, w: 8.5, h: 0.4,
  fontSize: 13, fontFace: "Calibri", color: GRAY, margin: 0
});

// Content area starts at y ≈ 1.2–1.5
// ... cards, stat cards, text blocks, etc.
```

## 7. Timeline / Multi-Card Slide

Cards laid out horizontally with equal spacing:

```javascript
const items = [
  { label: "Q3 2025", title: "Title\nLine 2", desc: "Description text.", color: BLUE_BRIGHT, icon: "robot" },
  { label: "Q4 2025", title: "Title\nLine 2", desc: "Description text.", color: AMBER, icon: "code" },
  { label: "Q1 2026", title: "Title\nLine 2", desc: "Description text.", color: GREEN, icon: "dna" },
  { label: "NOW",     title: "Our\nOpportunity", desc: "Description.", color: ORANGE, icon: "rocket" },
];

items.forEach((e, i) => {
  const x = 0.5 + i * 2.3, y = 1.5;
  card(s, x, y, 2.1, 2.7, e.color);

  // Badge/label
  s.addText(e.label, {
    x, y: y + 0.12, w: 2.1, h: 0.25,
    fontSize: 10, fontFace: "Calibri", color: e.color,
    bold: true, align: "center", margin: 0
  });

  // Icon
  s.addImage({ data: I[e.icon], x: x + 0.75, y: y + 0.4, w: 0.55, h: 0.55 });

  // Card title
  s.addText(e.title, {
    x: x + 0.1, y: y + 1.0, w: 1.9, h: 0.5,
    fontSize: 12, fontFace: "Calibri", color: WHITE,
    bold: true, align: "center", margin: 0
  });

  // Card description
  s.addText(e.desc, {
    x: x + 0.1, y: y + 1.5, w: 1.9, h: 1.0,
    fontSize: 9.5, fontFace: "Calibri", color: GRAY,
    align: "center", margin: 0
  });
});
```

## 8. Hub-and-Spoke Diagram

Central oval with surrounding domain cards:

```javascript
// Central hub
s.addShape("oval", {
  x: 3.8, y: 2.2, w: 2.4, h: 1.4,
  fill: { color: DARK3 },
  line: { color: PETROL, width: 2 }
});
s.addText([
  { text: "Hub", options: { fontSize: 13, color: PETROL_LIGHT, bold: true, breakLine: true } },
  { text: "Title", options: { fontSize: 13, color: PETROL_LIGHT, bold: true } },
], { x: 3.8, y: 2.3, w: 2.4, h: 1.2, align: "center", valign: "middle", margin: 0 });

// Surrounding cards (positioned manually around hub)
const domains = [
  { x: 0.3, y: 1.1, title: "Sales", desc: "...", ic: "chart", color: GREEN },
  { x: 7.2, y: 1.1, title: "Marketing", desc: "...", ic: "target", color: ORANGE },
  // ... etc
];
domains.forEach(d => {
  card(s, d.x, d.y, 2.5, 1.3, d.color);
  s.addImage({ data: I[d.ic], x: d.x + 0.15, y: d.y + 0.15, w: 0.45, h: 0.45 });
  s.addText(d.title, {
    x: d.x + 0.7, y: d.y + 0.15, w: 1.6, h: 0.35,
    fontSize: 14, fontFace: "Calibri", color: WHITE, bold: true, margin: 0
  });
  s.addText(d.desc, {
    x: d.x + 0.7, y: d.y + 0.5, w: 1.6, h: 0.7,
    fontSize: 9, fontFace: "Calibri", color: GRAY, margin: 0
  });
});
```

## 9. Domain Color Assignments

Each business domain has a consistent accent color:

| Domain | Accent Color | Hex |
|--------|-------------|-----|
| Sales | GREEN | `#2DD4A8` |
| Marketing | ORANGE | `#EC6602` |
| Engineering | AMBER | `#F59E0B` |
| Operations | BLUE_BRIGHT | `#3B82F6` |
| Cancer Research | PURPLE | `#A855F7` |
| General / Platform | PETROL | `#009999` |

Use the domain color for:
- Card accent bars on that domain's slides
- Stat card values related to that domain
- Top accent bar on domain-specific slides
- Icon fills for that domain's representative icons

## File Output

```javascript
P.writeFile({ fileName: "output.pptx" });
// or
const buffer = await P.write({ outputType: "nodebuffer" });
require("fs").writeFileSync("output.pptx", buffer);
```
