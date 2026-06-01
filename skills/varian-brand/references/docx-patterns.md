# Varian Brand — Word Document (docx) Code Patterns

These are tested, production-ready patterns for the `docx` npm package (v9.6.1+). Copy them directly — every hex value, spacing number, and margin has been validated across 25+ page documents.

## Table of Contents

1. [Constants & Imports](#1-constants--imports)
2. [Helper Functions](#2-helper-functions)
3. [Document Styles](#3-document-styles)
4. [Cover Page](#4-cover-page)
5. [Header & Footer](#5-header--footer)
6. [Budget Table Builder](#6-budget-table-builder)
7. [Callout Box (Tier Summary)](#7-callout-box-tier-summary)
8. [Risk Table](#8-risk-table)
9. [Recommendation Block](#9-recommendation-block)
10. [Rich Bullet Pattern](#10-rich-bullet-pattern)
11. [Complete Document Skeleton](#11-complete-document-skeleton)

---

## 1. Constants & Imports

```javascript
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
  TabStopType, TabStopPosition,
} = require("docx");

// ── BRAND PALETTE ─────────────────────────────────────────────
const PETROL      = "009999";
const DARK_PETROL = "007A7A";
const ORANGE      = "EC6602";
const AMBER       = "F59E0B";
const DARK        = "1A1A2E";
const DARK2       = "16213E";
const WHITE       = "FFFFFF";
const LIGHT_GRAY  = "F5F5F5";
const MID_GRAY    = "E8E8E8";
const TEXT_DARK    = "2C2C2C";
const TEXT_MED     = "555555";
const ACCENT_BLUE  = "2563EB";

// ── LAYOUT ────────────────────────────────────────────────────
const DXA_INCH = 1440;
const PAGE_W = 12240;   // US Letter width
const PAGE_H = 15840;   // US Letter height
const MARGIN = DXA_INCH; // 1 inch
const CONTENT_W = PAGE_W - 2 * MARGIN; // 9360 DXA
```

## 2. Helper Functions

```javascript
const b = (style = BorderStyle.SINGLE, size = 1, color = "CCCCCC") =>
  ({ style, size, color });
const borders = { top: b(), bottom: b(), left: b(), right: b() };
const noBorders = {
  top: b(BorderStyle.NONE, 0), bottom: b(BorderStyle.NONE, 0),
  left: b(BorderStyle.NONE, 0), right: b(BorderStyle.NONE, 0),
};
const cellMargins = { top: 80, bottom: 80, left: 120, right: 120 };

function headerCell(text, width, color = DARK_PETROL) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: color, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({
      spacing: { after: 0 },
      children: [new TextRun({
        text, bold: true, font: "Arial", size: 20, color: WHITE
      })]
    })],
  });
}

function cell(text, width, opts = {}) {
  const { bold, color, fill, align, font_size } = {
    bold: false, color: TEXT_DARK, fill: null,
    align: AlignmentType.LEFT, font_size: 20, ...opts
  };
  const shadingObj = fill ? { fill, type: ShadingType.CLEAR } : undefined;
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: shadingObj,
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({
      spacing: { after: 0 },
      alignment: align,
      children: [new TextRun({
        text, bold, font: "Arial", size: font_size || 20, color
      })]
    })],
  });
}

function row(cells) {
  return new TableRow({ children: cells });
}

function table(columnWidths, rows) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths,
    rows,
  });
}

function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({
    heading: level,
    children: [new TextRun(text)]
  });
}

function para(text, opts = {}) {
  const { bold, italic, color, size, spacing, align } = {
    bold: false, italic: false, color: TEXT_DARK, size: 22,
    spacing: { after: 200 }, align: AlignmentType.LEFT, ...opts
  };
  return new Paragraph({
    spacing,
    alignment: align,
    children: [new TextRun({
      text, bold, italics: italic, font: "Arial", size, color
    })]
  });
}

function richPara(runs, opts = {}) {
  return new Paragraph({
    spacing: { after: 200, ...opts.spacing },
    alignment: opts.align || AlignmentType.LEFT,
    children: runs,
  });
}

function bulletItem(text, ref = "bullets", level = 0) {
  return new Paragraph({
    numbering: { reference: ref, level },
    spacing: { after: 100 },
    children: [new TextRun({
      text, font: "Arial", size: 22, color: TEXT_DARK
    })]
  });
}

function richBullet(runs, ref = "bullets", level = 0) {
  return new Paragraph({
    numbering: { reference: ref, level },
    spacing: { after: 100 },
    children: runs,
  });
}

function spacer(pts = 100) {
  return new Paragraph({ spacing: { after: pts }, children: [] });
}
```

## 3. Document Styles

```javascript
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22 } }
    },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: DARK_PETROL },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: DARK_PETROL },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 }
      },
      {
        id: "Heading3", name: "Heading 3",
        basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: ORANGE },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 }
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0, format: LevelFormat.BULLET, text: "\u2022",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          },
          {
            level: 1, format: LevelFormat.BULLET, text: "\u2013",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1080, hanging: 360 } } }
          },
        ]
      },
      {
        reference: "numbers",
        levels: [
          {
            level: 0, format: LevelFormat.DECIMAL, text: "%1.",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } }
          },
        ]
      },
    ],
  },
  // sections: [ ... ]
});
```

## 4. Cover Page

The cover page is the first section, with no header/footer.

```javascript
{
  properties: {
    page: {
      size: { width: PAGE_W, height: PAGE_H },
      margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN }
    },
  },
  children: [
    spacer(600),
    // Organization line with wide letter-spacing
    new Paragraph({
      spacing: { after: 0 },
      children: [new TextRun({
        text: "SIEMENS HEALTHINEERS  |  VARIAN",
        font: "Arial", size: 20, color: TEXT_MED, characterSpacing: 80
      })]
    }),
    spacer(200),
    // Main title with petrol underline
    new Paragraph({
      spacing: { after: 0 },
      border: { bottom: {
        style: BorderStyle.SINGLE, size: 6, color: PETROL, space: 8
      }},
      children: [new TextRun({
        text: "DOCUMENT TITLE",
        font: "Arial", size: 72, bold: true, color: DARK_PETROL
      })]
    }),
    // Subtitle in orange
    new Paragraph({
      spacing: { after: 0 },
      children: [new TextRun({
        text: "Subtitle Line",
        font: "Arial", size: 36, color: ORANGE
      })]
    }),
    spacer(300),
    // Document type
    new Paragraph({
      spacing: { after: 80 },
      children: [new TextRun({
        text: "Document Type", font: "Arial", size: 28, bold: true, color: TEXT_DARK
      })]
    }),
    // Scope line
    new Paragraph({
      spacing: { after: 80 },
      children: [new TextRun({
        text: "Scope or phase description",
        font: "Arial", size: 24, color: TEXT_MED
      })]
    }),
    spacer(400),
    // Metadata
    new Paragraph({ spacing: { after: 80 }, children: [new TextRun({
      text: "Classification: Confidential", font: "Arial", size: 20, color: TEXT_MED
    })] }),
    new Paragraph({ spacing: { after: 80 }, children: [new TextRun({
      text: "Date: April 2026", font: "Arial", size: 20, color: TEXT_MED
    })] }),
    new Paragraph({ spacing: { after: 80 }, children: [new TextRun({
      text: "Version: 1.0", font: "Arial", size: 20, color: TEXT_MED
    })] }),
    spacer(200),
    // Prepared-for with top rule
    new Paragraph({
      border: { top: {
        style: BorderStyle.SINGLE, size: 2, color: MID_GRAY, space: 8
      }},
      spacing: { after: 0 },
      children: [new TextRun({
        text: "Prepared for: Varian Executive Leadership",
        font: "Arial", size: 20, italic: true, color: TEXT_MED
      })]
    }),
  ],
}
```

## 5. Header & Footer

Applied to the main body section (not the cover).

```javascript
{
  properties: {
    page: {
      size: { width: PAGE_W, height: PAGE_H },
      margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN }
    },
  },
  headers: {
    default: new Header({ children: [
      new Paragraph({
        spacing: { after: 0 },
        border: { bottom: {
          style: BorderStyle.SINGLE, size: 2, color: PETROL, space: 4
        }},
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          new TextRun({
            text: "Document Title",
            font: "Arial", size: 16, color: DARK_PETROL, bold: true
          }),
          new TextRun({
            text: "\tConfidential",
            font: "Arial", size: 16, color: TEXT_MED, italics: true
          }),
        ],
      }),
    ]}),
  },
  footers: {
    default: new Footer({ children: [
      new Paragraph({
        spacing: { after: 0 },
        border: { top: {
          style: BorderStyle.SINGLE, size: 1, color: MID_GRAY, space: 4
        }},
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          new TextRun({
            text: "Siemens Healthineers | Varian",
            font: "Arial", size: 16, color: TEXT_MED
          }),
          new TextRun({
            text: "\tPage ", font: "Arial", size: 16, color: TEXT_MED
          }),
          new TextRun({
            children: [PageNumber.CURRENT],
            font: "Arial", size: 16, color: TEXT_MED
          }),
        ],
      }),
    ]}),
  },
  children: [
    // Body content goes here
  ],
}
```

## 6. Budget Table Builder

Reusable function for any cost/comparison table with the standard 5-column layout.

```javascript
function budgetTable(title, items, titleColor = DARK_PETROL) {
  // items: [{ category, lean, moderate, full, notes, bold? }]
  const cw = [3200, 1340, 1540, 1540, 1740]; // sum = 9360
  const hdr = row([
    headerCell("Category", 3200, titleColor),
    headerCell("Lean", 1340, titleColor),
    headerCell("Moderate", 1540, titleColor),
    headerCell("Full Send", 1540, titleColor),
    headerCell("Notes", 1740, titleColor),
  ]);
  const dataRows = items.map((it, i) => {
    const fill = i % 2 === 0 ? LIGHT_GRAY : null;
    return row([
      cell(it.category, 3200, { fill, bold: it.bold }),
      cell(it.lean, 1340, { fill, align: AlignmentType.RIGHT }),
      cell(it.moderate, 1540, { fill, align: AlignmentType.RIGHT }),
      cell(it.full, 1540, { fill, align: AlignmentType.RIGHT }),
      cell(it.notes || "", 1740, { fill, font_size: 18, color: TEXT_MED }),
    ]);
  });
  return [
    para(title, { bold: true, size: 24, color: titleColor }),
    table(cw, [hdr, ...dataRows]),
    spacer(150),
  ];
}

// Usage: spread into children array
// ...budgetTable("Year 1 Total Program Budget", [ ... ]),
```

## 7. Callout Box (Tier Summary)

Three colored cells side by side for executive-summary tier comparisons.

```javascript
(() => {
  const cw = [3120, 3120, 3120];
  return table(cw, [
    row([
      new TableCell({
        borders,
        width: { size: 3120, type: WidthType.DXA },
        shading: { fill: "E8F5E9", type: ShadingType.CLEAR }, // soft green
        margins: { top: 120, bottom: 120, left: 160, right: 160 },
        children: [
          new Paragraph({ spacing: { after: 60 }, alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "LEAN", bold: true, font: "Arial", size: 28, color: DARK_PETROL
            })]
          }),
          new Paragraph({ spacing: { after: 40 }, alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "$1.8M incremental", bold: true, font: "Arial", size: 22, color: "2E7D32"
            })]
          }),
          new Paragraph({ spacing: { after: 40 }, alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "$4.1M total program", font: "Arial", size: 18, color: TEXT_MED
            })]
          }),
          new Paragraph({ spacing: { after: 0 }, alignment: AlignmentType.CENTER,
            children: [new TextRun({
              text: "Description of this tier.",
              font: "Arial", size: 18, color: TEXT_MED
            })]
          }),
        ]
      }),
      // Moderate cell: fill "E3F2FD", accent ACCENT_BLUE
      // Full Send cell: fill "FFF3E0", accent ORANGE, title color ORANGE
      // (same structure, different colors)
    ]),
  ]);
})()
```

## 8. Risk Table

Standard 4-column layout for risk registers.

```javascript
const cw = [2400, 2200, 2200, 2560]; // sum = 9360
table(cw, [
  row([
    headerCell("Risk", 2400),
    headerCell("Likelihood", 2200),
    headerCell("Impact", 2200),
    headerCell("Mitigation", 2560),
  ]),
  row([
    cell("Risk description", 2400, { bold: true }),
    cell("High", 2200, { color: "C62828" }),   // red for high risk
    cell("Med\u2013High", 2200),
    cell("Mitigation strategy description", 2560),
  ]),
  // ... alternating LIGHT_GRAY fills on even rows
]);
```

## 9. Recommendation Block

Italic editorial note with bold label.

```javascript
richPara([
  new TextRun({
    text: "Recommendation: ",
    bold: true, italic: true, font: "Arial", size: 20, color: TEXT_MED
  }),
  new TextRun({
    text: "The descriptive recommendation text goes here...",
    font: "Arial", size: 20, italic: true, color: TEXT_MED
  }),
])
```

## 10. Rich Bullet Pattern

Bold lead term followed by description — the standard pattern for agent/feature lists.

```javascript
richBullet([
  new TextRun({
    text: "Feature name: ",
    bold: true, font: "Arial", size: 22
  }),
  new TextRun({
    text: "Description of the feature and what it does.",
    font: "Arial", size: 22
  }),
])
```

## 11. Complete Document Skeleton

Putting it all together:

```javascript
const doc = new Document({
  styles: { /* See Section 3 */ },
  numbering: { /* See Section 3 */ },
  sections: [
    // Section 1: Cover page (no header/footer)
    { /* See Section 4 */ },
    // Section 2: Main body (with header/footer)
    {
      properties: { /* See Section 5 */ },
      headers: { /* See Section 5 */ },
      footers: { /* See Section 5 */ },
      children: [
        heading("1. Section Title"),
        para("Body paragraph text..."),
        bulletItem("Standard bullet point"),
        richBullet([
          new TextRun({ text: "Bold lead: ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "Description text.", font: "Arial", size: 22 }),
        ]),
        heading("1.1 Subsection", HeadingLevel.HEADING_2),
        heading("Detail Heading", HeadingLevel.HEADING_3),
        ...budgetTable("Cost Summary", [
          { category: "Line Item", lean: "$100K", moderate: "$200K", full: "$400K", notes: "Details" },
          { category: "TOTAL", lean: "$100K", moderate: "$200K", full: "$400K", bold: true },
        ]),
        new Paragraph({ children: [new PageBreak()] }),
        // Continue with more sections...
      ],
    },
  ],
});

const buf = await Packer.toBuffer(doc);
require("fs").writeFileSync("output.docx", buf);
```
