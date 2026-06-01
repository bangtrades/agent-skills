// BT Stock Report — Canonical Template
// =====================================
//
// This is the canonical scaffolding for a BT Stock Report. The brand primitives
// (palette, AmberDots, makeCard, buildTable, hero layout, page structure) are stable
// across every report. You change ticker-specific content within the marked sections.
//
// To use:
//   1. Replace TICKER, COMPANY_NAME, EXCHANGE_NAME, REPORT_DATE
//   2. Fill in snapshotCard / quarterCard rows with current data
//   3. Edit coreViewText paragraph
//   4. Edit whyItMattersNow bullets (target 6 bullets)
//   5. Edit btRead paragraph
//   6. Edit workingStance / printSetupMap rows
//   7. Edit page2 (Variant Perception, Scenario PT, Capital Structure, Earnings Model)
//   8. Edit page3 (Business Overview, Tailwinds, Competitive Moat)
//   9. Edit page4 (Catalysts, Monitoring, Sentiment, Analyst PT migration)
//  10. Edit page5 (Risks, What Would Change My Mind, Trade Framework, Bottom Line)
//  11. Edit sources block
//
// Build:
//   npm install --silent
//   node build_report.js
//   python ~/.claude/skills/docx/scripts/office/soffice.py \
//     --headless --convert-to pdf TICKER-bt-stock-report.docx --outdir .

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, LevelFormat, TabStopType, BorderStyle, WidthType,
  ShadingType, PageBreak,
} = require('docx');

// ─── Palette (DO NOT CHANGE — brand primitives) ────────────────────────────
const COLOR = {
  ink:       '2F2F2F',
  subtle:    '8A8A8A',
  hairline:  'D6D3CC',
  card:      'F3F0E8',
  cardAlt:   'EFE7D2',
  amber:     'D4A017',
  amberDk:   'A07910',
  bull:      '2F7A4A',
  bear:      'B04A2F',
  base:      '6B6B6B',
};
const FONT = 'Helvetica Neue';
const SZ = { title: 44, tagline: 22, section: 26, sub: 22, body: 20, small: 18, micro: 16, nano: 14 };

// ─── Helpers (DO NOT CHANGE — brand primitives) ────────────────────────────
const SPACER = (after = 120) =>
  new Paragraph({ children: [new TextRun({ text: '' })], spacing: { after } });

const H1 = (text) =>
  new Paragraph({
    children: [new TextRun({ text, font: FONT, color: COLOR.ink, bold: true, size: SZ.section })],
    spacing: { before: 160, after: 80 },
    keepNext: true,
  });

const H2 = (text) =>
  new Paragraph({
    children: [new TextRun({ text, font: FONT, color: COLOR.ink, bold: true, size: SZ.sub })],
    spacing: { before: 120, after: 60 },
    keepNext: true,
  });

const Body = (text, opts = {}) =>
  new Paragraph({
    children: [new TextRun({ text, font: FONT, color: COLOR.ink, size: SZ.body, ...opts })],
    spacing: { after: 100, line: 280 },
  });

const Bullet = (text) =>
  new Paragraph({
    numbering: { reference: 'amber-bullets', level: 0 },
    spacing: { after: 80, line: 280 },
    children: [new TextRun({ text, font: FONT, color: COLOR.ink, size: SZ.body })],
  });

const cardRow = (label, value, opts = {}) => new Paragraph({
  tabStops: [{ type: TabStopType.RIGHT, position: 4300 }],
  spacing: { after: 60 },
  children: [
    new TextRun({ text: label, font: FONT, color: COLOR.ink, size: SZ.small, bold: true }),
    new TextRun({ text: '\t' + value, font: FONT, color: COLOR.ink, size: SZ.small, ...opts }),
  ],
});

const cardTitle = (label) => new Paragraph({
  spacing: { after: 100 },
  children: [new TextRun({ text: label, font: FONT, color: COLOR.ink, size: SZ.sub, bold: true })],
});

const makeCard = (children, fill = COLOR.card, w = 4700) => new Table({
  width: { size: w, type: WidthType.DXA },
  columnWidths: [w],
  rows: [new TableRow({
    children: [new TableCell({
      width: { size: w, type: WidthType.DXA },
      shading: { fill, type: ShadingType.CLEAR, color: 'auto' },
      margins: { top: 200, bottom: 200, left: 240, right: 240 },
      borders: {
        top:    { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
        bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
        left:   { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
        right:  { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
      },
      children,
    })],
  })],
});

// Three-amber-dot brand mark (also used as page-2+ header with pageBreakBefore)
const AmberDots = (pageBreakBefore = false) => new Paragraph({
  spacing: { after: 100 },
  pageBreakBefore,
  children: [
    new TextRun({ text: '●', font: FONT, color: COLOR.amber, size: 28 }),
    new TextRun({ text: '  ', font: FONT, size: 16 }),
    new TextRun({ text: '●', font: FONT, color: COLOR.amber, size: 22 }),
    new TextRun({ text: '  ', font: FONT, size: 16 }),
    new TextRun({ text: '●', font: FONT, color: COLOR.amber, size: 18 }),
  ],
});

const TickerTitle = (ticker) => new Paragraph({
  spacing: { after: 40 },
  children: [new TextRun({
    text: ticker, font: FONT, bold: true, color: COLOR.ink, size: SZ.title,
    characterSpacing: 60,
  })],
});

const Subtitle = (text) => new Paragraph({
  spacing: { after: 120 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline, space: 8 } },
  children: [new TextRun({ text, font: FONT, color: COLOR.subtle, size: SZ.tagline })],
});

// Generic table builder — used for every structured section
function buildTable({ rows, columnWidths, header = null, totalWidth = 9360, fillFirstCol = null, headerFill = COLOR.cardAlt }) {
  const allRows = [];
  if (header) {
    allRows.push(new TableRow({
      tableHeader: true,
      children: header.map((h, i) => new TableCell({
        width: { size: columnWidths[i], type: WidthType.DXA },
        shading: { fill: headerFill, type: ShadingType.CLEAR, color: 'auto' },
        margins: { top: 80, bottom: 80, left: 100, right: 100 },
        borders: {
          top: { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
          bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
          left: { style: BorderStyle.NONE },
          right: { style: BorderStyle.NONE },
        },
        children: [new Paragraph({
          children: [new TextRun({ text: h, font: FONT, color: COLOR.ink, bold: true, size: SZ.small })],
        })],
      })),
    }));
  }
  rows.forEach((row) => {
    allRows.push(new TableRow({
      cantSplit: true,
      children: row.map((cellVal, ci) => {
        const isFirst = ci === 0;
        const cellChildren = Array.isArray(cellVal)
          ? cellVal
          : [new Paragraph({
              children: [new TextRun({
                text: String(cellVal), font: FONT, color: COLOR.ink, bold: isFirst, size: SZ.small,
              })],
            })];
        return new TableCell({
          width: { size: columnWidths[ci], type: WidthType.DXA },
          shading: fillFirstCol && isFirst
            ? { fill: fillFirstCol, type: ShadingType.CLEAR, color: 'auto' }
            : undefined,
          margins: { top: 80, bottom: 80, left: 100, right: 100 },
          borders: {
            top: { style: BorderStyle.NONE },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: COLOR.hairline },
            left: { style: BorderStyle.NONE },
            right: { style: BorderStyle.NONE },
          },
          children: cellChildren,
        });
      }),
    }));
  });
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline },
      left: { style: BorderStyle.NONE },
      right: { style: BorderStyle.NONE },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: COLOR.hairline },
      insideVertical: { style: BorderStyle.NONE },
    },
    rows: allRows,
  });
}

const colorRun = (text, color, opts = {}) =>
  new TextRun({ text, font: FONT, color, size: SZ.small, ...opts });
const colorPara = (runs) => new Paragraph({ children: runs });

// ═══════════════════════════════════════════════════════════════════════════
//   EDIT BELOW THIS LINE — TICKER-SPECIFIC CONTENT
// ═══════════════════════════════════════════════════════════════════════════

const TICKER         = 'XXXX';                  // <-- REPLACE
const COMPANY_NAME   = 'Company Name, Inc.';    // <-- REPLACE
const EXCHANGE_NAME  = 'NYSE';                  // <-- REPLACE (NYSE / NASDAQ / NYSE American)
const REPORT_DATE    = 'YYYY-MM-DD';            // <-- REPLACE
const REPORT_SUBTITLE = `${COMPANY_NAME} · BT Stock Report — [theme summary in one breath]`;

// ─── PAGE 1 — Hero / Snapshot / BT Read ────────────────────────────────────

const snapshotCard = makeCard([
  cardTitle('Snapshot · ' + REPORT_DATE),
  cardRow('Price',           '$XX.XX'),
  cardRow('Market Cap',      '~$X.XB'),
  cardRow('Shares Out',      '~XXXM'),
  cardRow('Float',           '~XXXM'),
  cardRow('Avg Vol',         '~X.XM'),
  cardRow('Short % Float',   '~X%'),
  cardRow('52W Range',       '$XX.XX–$XX.XX'),
  cardRow('Bucket',          '[Bucket label]'),
]);

const quarterCard = makeCard([
  cardTitle('QX FY[YY] ([Mon \'YY])'),
  cardRow('Revenue',           '$XXXM'),
  cardRow('YoY Growth',        '+X%'),
  cardRow('[Segment 1]',       '$XXXM (+X%)'),
  cardRow('[Segment 2]',       '$XXM (+X%)'),
  cardRow('Non-GAAP Op Margin','XX.X%'),
  cardRow('Non-GAAP EPS',      '$X.XX'),
  cardRow('Operating CF',      '$XXM'),
  cardRow('Free Cash Flow',    '$XXM'),
  cardRow('Cash + ST Inv.',    '$XXXM'),
  cardRow('Q[N+1] Guide',      '$XXXM'),
]);

const coreViewText = [
  new Paragraph({
    spacing: { after: 120, line: 280 },
    children: [new TextRun({
      text: '[Replace with 4–6 sentence Core View paragraph. State the convergence in one breath. What are the 3 vectors? What is the gating event? Why now?]',
      font: FONT, color: COLOR.ink, size: SZ.body,
    })],
  }),
];

const heroTable = new Table({
  width: { size: 10080, type: WidthType.DXA },
  columnWidths: [5280, 4800],
  borders: {
    top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
    left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
    insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE },
  },
  rows: [new TableRow({
    cantSplit: true,
    children: [
      new TableCell({
        width: { size: 5280, type: WidthType.DXA },
        margins: { top: 0, bottom: 0, left: 0, right: 240 },
        borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
        children: [
          new Paragraph({
            spacing: { after: 120 },
            children: [new TextRun({ text: 'Core View', font: FONT, bold: true, color: COLOR.ink, size: SZ.section })],
          }),
          ...coreViewText,
        ],
      }),
      new TableCell({
        width: { size: 4800, type: WidthType.DXA },
        margins: { top: 0, bottom: 0, left: 100, right: 0 },
        borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE } },
        children: [
          snapshotCard,
          new Paragraph({ spacing: { after: 160 }, children: [new TextRun('')] }),
          quarterCard,
        ],
      }),
    ],
  })],
});

const whyItMattersNow = [
  new Paragraph({
    spacing: { before: 200, after: 120 },
    children: [new TextRun({ text: 'Why It Matters Now', font: FONT, bold: true, color: COLOR.ink, size: SZ.section })],
  }),
  Bullet('[Bullet 1 — most important load-bearing fact. Lead with the catalyst date or hard number.]'),
  Bullet('[Bullet 2 — supporting evidence with specifics. Avoid generic claims.]'),
  Bullet('[Bullet 3 — quantified mix shift / segment trend / customer concentration.]'),
  Bullet('[Bullet 4 — macro / thematic tailwind with hard numbers (TAM revisions, unit forecasts).]'),
  Bullet('[Bullet 5 — capital structure / cash position / buyback note.]'),
  Bullet('[Bullet 6 — sell-side disagreement / variance signal / contrarian read.]'),
];

const btRead = [
  H1('BT Read'),
  Body('[Replace with 4–6 sentence BT Read paragraph. This is the synthesis quote. Druckenmiller framing if relevant: own the regime, but pre-commit to disconfirming evidence.]'),
];

const workingStance = [
  H2('Working stance'),
  buildTable({
    columnWidths: [1900, 7460],
    rows: [
      ['Bucket',     '[Bucket label]'],
      ['Character',  '[Compounder / squeeze / pre-revenue / etc.]'],
      ['Horizon',    '[6–24 months thesis]'],
      ['Style',      '[Core position / fade chasing / tactical add on confirmation]'],
      ['Edge',       '[Where consensus is wrong]'],
    ],
  }),

  H1('Q[N] Print Setup Map · [date]'),
  Body('Pre-commit to what bullish vs bearish prints look like before the tape moves.'),
  buildTable({
    columnWidths: [3120, 3120, 3120],
    header: ['Disclosure to watch', 'Bull-case print', 'Bear-case print'],
    rows: [
      ['[Metric 1]',           '[Bull threshold]',  '[Bear threshold]'],
      ['[Metric 2]',           '[Bull threshold]',  '[Bear threshold]'],
      ['[Metric 3]',           '[Bull threshold]',  '[Bear threshold]'],
      ['[Metric 4]',           '[Bull threshold]',  '[Bear threshold]'],
      ['[Metric 5]',           '[Bull threshold]',  '[Bear threshold]'],
    ],
  }),
];

// ─── PAGE 2 — Variant Perception, Scenario PTs, Capital Structure ──────────

const page2 = [
  AmberDots(true),  // pageBreakBefore: true
  TickerTitle(TICKER),
  Subtitle('Variant perception · scenario price targets · capital structure'),

  H1('Variant Perception'),
  Body('Where consensus and BT diverge. Each delta is testable inside the next two earnings prints.'),
  buildTable({
    columnWidths: [3120, 3120, 3120],
    header: ['Consensus says', 'BT says', 'Why we differ'],
    rows: [
      ['[Consensus view 1]', '[BT view 1]', '[Why we differ — testable]'],
      ['[Consensus view 2]', '[BT view 2]', '[Why we differ]'],
      ['[Consensus view 3]', '[BT view 3]', '[Why we differ]'],
      ['[Consensus view 4]', '[BT view 4]', '[Why we differ]'],
      ['[Consensus view 5]', '[BT view 5]', '[Why we differ]'],
    ],
  }),

  H1('Scenario Price Targets · 12-month'),
  Body('Three weighted scenarios. Implied returns shown vs. spot $XX.XX. Probability-weighted EV is the BT base case.'),
  buildTable({
    columnWidths: [1700, 1500, 1500, 1900, 2760],
    header: ['Scenario', 'Price', 'Probability', 'Implied Return', 'Anchor / Multiple'],
    rows: [
      [[colorPara([colorRun('Bull', COLOR.bull, { bold: true })])],
       [colorPara([colorRun('$XX', COLOR.bull, { bold: true })])],
       'XX%',
       [colorPara([colorRun('+X%', COLOR.bull)])],
       '[Bull anchor — multiple × earnings × catalyst]'],
      [[colorPara([colorRun('Base', COLOR.base, { bold: true })])],
       [colorPara([colorRun('$XX', COLOR.base, { bold: true })])],
       'XX%',
       [colorPara([colorRun('+X%', COLOR.base)])],
       '[Base anchor — consensus catch-up logic]'],
      [[colorPara([colorRun('Bear', COLOR.bear, { bold: true })])],
       [colorPara([colorRun('$XX', COLOR.bear, { bold: true })])],
       'XX%',
       [colorPara([colorRun('-X%', COLOR.bear)])],
       '[Bear anchor — what breaks the thesis]'],
      [[colorPara([colorRun('Probability-Weighted', COLOR.ink, { bold: true })])],
       [colorPara([colorRun('$XX', COLOR.ink, { bold: true })])],
       '100%',
       [colorPara([colorRun('+X%', COLOR.ink, { bold: true })])],
       'Asymmetry [bull-skewed / balanced / bear-tilted]'],
    ],
  }),

  H1('Capital Structure & Capital Return'),
  buildTable({
    columnWidths: [3120, 1400, 4840],
    header: ['Item', 'Value', 'Note'],
    rows: [
      ['Cash + Short-term Investments',   '$XXXM',   '[Note]'],
      ['Total Debt',                      '~$XXXM',  '[Note — recent paydowns / converts]'],
      ['Net Debt / Net Cash',             '~$XXXM',  '[Net leverage trajectory]'],
      ['Stockholders\' Equity',           '$XXXM',   '[Note]'],
      ['Buyback Authorization',           '$XXXM',   '[Authorization total + recent execution pace]'],
      ['Subscription / Recurring Revenue','$XXXM',   '[Note — % of total, growth rate]'],
      ['Operating Margin',                'XX%',     '[Trend + composition]'],
      ['Free Cash Flow (TTM est.)',       '~$XXXM',  '[Conversion vs non-GAAP NI]'],
    ],
  }),

  H1('Earnings Model · BT vs. Guide vs. Street'),
  buildTable({
    columnWidths: [2400, 1700, 1700, 1700, 1860],
    header: ['Metric', 'FY[YY-1]A', 'FY[YY] Guide', 'BT FY[YY]E', 'BT FY[YY+1]E'],
    rows: [
      ['Revenue ($B)',           'X.XX', 'X.XX', 'X.XX', 'X.XX'],
      ['[Segment 1] ($B)',       'X.XX', 'X.XX', 'X.XX', 'X.XX'],
      ['[Segment 2] ($B)',       'X.XX', 'X.XX', 'X.XX', 'X.XX'],
      ['Non-GAAP Op Margin',     'XX%',  'XX%',  'XX.X%','XX–XX%'],
      ['Non-GAAP EPS',           '$X.XX','$X.XX','$X.XX','$X.XX'],
      ['Free Cash Flow ($M)',    '$XXX', '$XXX', '$XXX', '$XXX'],
    ],
  }),
];

// ─── PAGE 3 — Business Quality, AI/Macro Tailwind, Competitive Moat ────────

const page3 = [
  AmberDots(true),
  TickerTitle(TICKER),
  Subtitle('Business quality · AI/macro thesis · competitive moat'),

  H1('Business Overview'),
  Body('[Replace with single-paragraph plain-language description of what the company does, segments, end markets, customer profile.]'),

  H1('[Tailwind / Theme Section Title]'),
  Bullet('[Specific, quantified tailwind point with hard number]'),
  Bullet('[Adoption / forecast / TAM revision with source]'),
  Bullet('[Customer behavior shift with timeline]'),
  Bullet('[Why this name vs the obvious mega-cap proxy]'),
  Bullet('[Competitive consolidation / structural moat]'),

  H1('Competitive Moat'),
  buildTable({
    columnWidths: [2120, 1900, 1900, 1900, 1540],
    header: ['Competitor', 'Scale', 'Strength vs. ' + TICKER, 'Weakness', 'Net'],
    rows: [
      ['[Competitor 1]', '[Scale]', '[Their strength]', '[Their weakness]', '[Co-leader / Adjacent / Falling behind / Niche]'],
      ['[Competitor 2]', '[Scale]', '[Their strength]', '[Their weakness]', '[Net]'],
      ['[Competitor 3]', '[Scale]', '[Their strength]', '[Their weakness]', '[Net]'],
      ['[Competitor 4]', '[Scale]', '[Their strength]', '[Their weakness]', '[Net]'],
      ['[Competitor 5]', '[Scale]', '[Their strength]', '[Their weakness]', '[Net]'],
    ],
  }),
  Body('[One sentence on what the moat actually is — share gains vs system economics vs vertical integration vs etc.]'),
];

// ─── PAGE 4 — Catalysts, Monitoring, Sentiment & Positioning ───────────────

const page4 = [
  AmberDots(true),
  TickerTitle(TICKER),
  Subtitle('Catalyst path · monitoring KPIs · sentiment & positioning'),

  H1('Catalyst Path'),
  buildTable({
    columnWidths: [4200, 1500, 1400, 2260],
    header: ['Catalyst', 'When', 'Probability', 'Impact'],
    rows: [
      ['[Q earnings + guide]',                 '[Date]',   'Beat XX%',     'High — gating event'],
      ['[Strategic announcement category]',    '[Window]', 'XX%',          'High'],
      ['[User conference / investor day]',     '[Date]',   '85%',          'Med'],
      ['[Customer / contract win]',            '[Window]', 'XX%',          'High'],
      ['[Macro / sector tide]',                '[Window]', 'Variable',     'High (macro)'],
      ['[Hyperscaler / customer CapEx prints]','Quarterly','Variable',     'High (macro)'],
    ],
  }),

  H1('Quarterly Monitoring Dashboard'),
  Bullet('[KPI 1 — base case threshold to watch]'),
  Bullet('[KPI 2]'),
  Bullet('[KPI 3]'),
  Bullet('[KPI 4]'),
  Bullet('[KPI 5]'),
  Bullet('[KPI 6]'),
  Bullet('[KPI 7]'),
  Bullet('[KPI 8 — tail risk / leading indicator]'),

  H1('Sentiment & Positioning Dashboard'),
  buildTable({
    columnWidths: [3120, 2400, 3840],
    header: ['Vector', 'Reading', 'Interpretation'],
    rows: [
      ['Stock vs. ATH',                  '$XX vs. $XX (-X%)',         '[Setup interpretation]'],
      ['52W return',                     '+XX% / -XX%',                '[Theme interpretation]'],
      ['Sell-side rating',               'N analysts: Buy / Hold',     'Avg PT $XX — implies +XX% / -XX%'],
      ['Latest analyst PT moves',        '[Firm A] $XX (raise); [Firm B] $XX (cut)', '[What variance signals]'],
      ['Insider activity (90d)',         'XXk sh / $XM',               '[Routine 10b5-1 / pre-rerate / tell]'],
      ['Buyback program',                '$XXM auth (~X% of mkt cap)', '[Execution pace]'],
      ['Volume dynamics',                '~X.XM (avg X.XM)',           '[Above/below average — accumulation or distribution]'],
      ['Beta',                           'X.XX',                       '[Behavior in regime context]'],
      ['Retail / X / Stocktwits',        '[Tone descriptor]',          '[Memetic risk or signal]'],
      ['Customer concentration',         '[Top customer = X% est.]',   '[Concentration risk vs validation tradeoff]'],
    ],
  }),

  H1('Analyst Price Target Migration'),
  buildTable({
    columnWidths: [3120, 1500, 1500, 1500, 1740],
    header: ['Firm', 'Old PT', 'New PT', 'Date', 'Rating'],
    rows: [
      ['[Firm 1]',          '$XX',     '$XX',     '[Date]',     '[Rating]'],
      ['[Firm 2]',          '$XX',     '$XX',     '[Date]',     '[Rating]'],
      ['[Firm 3]',          '$XX',     '$XX',     '[Date]',     '[Rating]'],
      ['Consensus average', '—',       '$XX',     '[Date]',     '[Buy / Hold]'],
      ['High target',       '—',       '$XX',     '[Date]',     '—'],
      ['Low target',        '—',       '$XX',     '[Date]',     '—'],
    ],
  }),
];

// ─── PAGE 5 — Risks, What Would Change My Mind, Trade Framework, Bottom Line ─

const page5 = [
  AmberDots(true),
  TickerTitle(TICKER),
  Subtitle('Risk framing · what would change my mind · trade framework'),

  H1('Key Risks'),
  Bullet('[Specific thesis-tied risk 1 — engages with the bull case directly]'),
  Bullet('[Specific risk 2]'),
  Bullet('[Specific risk 3]'),
  Bullet('[Valuation / multiple compression risk if applicable]'),
  Bullet('[Macro / regime risk]'),
  Bullet('[Customer concentration / single-name exposure]'),
  Bullet('[Operational / execution risk]'),
  Bullet('[Regulatory / FX / geographic risk]'),

  H1('What Would Change My Mind'),
  Body('Druckenmiller-style: pre-commit to the disconfirming evidence so it gets respected when it shows up.'),
  Bullet('[Specific disconfirming trigger 1 — testable inside next 1–2 earnings prints]'),
  Bullet('[Trigger 2 — quantitative, falsifiable]'),
  Bullet('[Trigger 3]'),
  Bullet('[Trigger 4]'),
  Bullet('[Trigger 5]'),
  Bullet('[Trigger 6]'),
  Bullet('[Trigger 7 — insider behavior change]'),
  Bullet('[Trigger 8 — customer concentration shift]'),

  H1('Trade Framework'),
  Bullet('Core thesis: [how to think about position type and horizon]'),
  Bullet('Position sizing: [pre-print posture and full allocation trigger]'),
  Bullet('Tactical: [defined-risk option structure if relevant]'),
  Bullet('Hedge: [pair candidates for sector or factor isolation]'),
  Bullet('Stops: thesis-stop, not price-stop. Re-rate down only on a thesis trigger above.'),
  Bullet('Exits: [trim levels and long-tail preservation logic]'),

  H1('Position Sizing — Kelly Sketch'),
  Body('Probability-weighted EV: P(bull) × $bull + P(base) × $base + P(bear) × $bear = $XX (PWM). At spot $XX.XX that is +X% expected return over 12 months. Asymmetry [bull-skewed / balanced / bear-tilted]: bull tail (+X%) vs. bear tail (−X%). Kelly sizing on these inputs implies [position size band]; couple with defined-risk options into the next print to capture additional gamma.'),

  H1('Bottom Line'),
  Body('[Replace with 4–6 sentence Bottom Line synthesis. The quote that gets pulled. Lead with what the company has just become; close with what would falsify it.]'),
];

// ─── Sources / footer ──────────────────────────────────────────────────────

const sources = [
  new Paragraph({
    spacing: { before: 200, after: 60 },
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: COLOR.hairline, space: 6 } },
    children: [new TextRun({ text: 'Sources', font: FONT, bold: true, color: COLOR.subtle, size: SZ.micro })],
  }),
  new Paragraph({
    spacing: { line: 240, after: 80 },
    keepLines: true,
    children: [new TextRun({
      text: '[Replace with italic prose listing of every source consulted. Press releases, transcripts, analyst notes, trade publications. Each citation should be enough that the reader can find the source again — name the publication and approximate date. Aggregators are fine but flag them as such.]',
      font: FONT, color: COLOR.subtle, size: SZ.micro, italics: true,
    })],
  }),
  new Paragraph({
    spacing: { before: 80 },
    keepLines: true,
    children: [new TextRun({
      text: 'Prepared ' + REPORT_DATE + ' — [optional context: "N trading days ahead of QX earnings" / "post-rebrand" / etc.]. Research + synthesis only. Not investment advice. Probability weights, scenario PTs and earnings-model figures are author estimates derived from cited public data.',
      font: FONT, color: COLOR.subtle, size: SZ.micro,
    })],
  }),
];

// ─── Document assembly ──────────────────────────────────────────────────────

const doc = new Document({
  creator: 'BT Reports',
  title: TICKER + ' — BT Stock Report',
  description: COMPANY_NAME + ' BT Stock Report (' + REPORT_DATE + ')',
  styles: {
    default: { document: { run: { font: FONT, size: SZ.body, color: COLOR.ink } } },
  },
  numbering: {
    config: [{
      reference: 'amber-bullets',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '•',
        alignment: AlignmentType.LEFT,
        style: {
          paragraph: { indent: { left: 360, hanging: 220 } },
          run: { color: COLOR.amber, font: FONT, size: 24 },
        },
      }],
    }],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },                        // US Letter
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }, // ~0.75"
      },
    },
    children: [
      // ─── PAGE 1 ─────────────────────────────────────────────────────
      AmberDots(),
      TickerTitle(TICKER),
      Subtitle(REPORT_SUBTITLE),
      heroTable,
      ...whyItMattersNow,
      SPACER(160),
      ...btRead,
      SPACER(120),
      ...workingStance,

      // ─── PAGES 2–5 ──────────────────────────────────────────────────
      ...page2,
      ...page3,
      ...page4,
      ...page5,

      // Sources footer
      ...sources,
    ],
  }],
});

Packer.toBuffer(doc).then(buf => {
  const out = process.argv[2] || `${REPORT_DATE}-${TICKER.toLowerCase()}-bt-stock-report.docx`;
  fs.writeFileSync(out, buf);
  console.log('Wrote', out, 'size:', buf.length);
});
