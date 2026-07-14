# WaiveLabs — Spreadsheet Spec (.xlsx)

Pairs with the **`xlsx`** skill (mechanics). Models, dashboards, trackers, capacity/pricing
calculators, data deliverables.

## Master look

- **Title row:** sheet title in **Sora**-equivalent (Montserrat) 16pt `--ink`; a `--blue` fill
  banner or a thin blue rule beneath. Logo (small) top-left if it's a client-facing deliverable.
- **Header row:** `--blue-deep` `#0D43AA` fill, white bold text, frozen pane. Subtotals/section
  headers get a `--dawn-2` `#F4F7FD` fill.
- **Body:** **Inter**-equivalent (Inter/Arial/Calibri) 10–11pt, `--ink-body`. Generous row height,
  hairline borders only (light gray `--line`), no heavy gridlines.
- **Numbers:** right-aligned, tabular; currency/percent formatted; thousands separators. Negative
  values in `--bad` `#DC2626`, positives can use `--good` `#16A34A` where signal matters.
- **Accent discipline:** blue for structure/headers; orange `#E65100` for ONE highlighted KPI cell
  or a single callout — never flood. Conditional formatting uses the brand state colors
  (good/warn/bad) AND a non-color cue (icon/data-bar) for the color-blind profile.

## Patterns

- **Dashboard:** KPI cards across the top (big tabular number + delta), a couple of native charts
  (brand blue + amber series — or blue/vermillion if a color-blind-safe version is requested),
  a clean data table below. One summary sentence in plain English at the top.
- **Model (pricing/capacity):** inputs block (tinted, labeled), calc block, outputs block; document
  assumptions in a notes column; never expose secrets or real client PII.
- **Tracker / CRM export:** frozen header, filters on, status column using brand state colors +
  glyphs, dates ISO `YYYY-MM-DD`.

## Charts

Series colors from the palette: primary `--blue #3179F5`, secondary `--amber #FFB454` (swap to
vermillion `#D55E00` for the color-blind-safe variant). Minimal chrome, no 3D, no heavy gridlines,
labels in Inter. Title in Montserrat. Let the data carry it.

## Rules

Fictional/sample data is labeled as such; real client data honors the security baseline (no
secrets, RLS-respecting exports, no PII in shared copies). No public pricing leakage. Verify the
*i* in WaiveLabs on any visible branding.
