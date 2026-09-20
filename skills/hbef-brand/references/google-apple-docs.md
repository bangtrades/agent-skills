# HBEF — Google Docs, Sheets, Slides & Apple Pages, Numbers, Keynote (2026 System)

How to apply the **HBEF 2026 brand system** in cloud and Apple-native formats, where the Office binary tooling (`python-docx`, `openpyxl`, `python-pptx`) doesn't apply. Two paths:

1. **Export from a generated Office file** — best fidelity, recommended for most deliverables
2. **Manual paste-in styling** — when the deliverable must originate in the cloud/native format

This file documents both paths, plus the font-availability rules that differ sharply between the two ecosystems.

---

## The headline change in 2026: Google can now use the real brand fonts

**Both Aleo and Lato are native Google Fonts.** This is a genuine improvement over the retired system, where Montserrat was available but BauhausBold was a custom face that could never be used in Google Workspace at all.

| Ecosystem | Aleo | Lato | Consequence |
|---|---|---|---|
| **Google Docs / Sheets / Slides** | ✅ Native, via "More fonts" | ✅ Native, via "More fonts" | **Use the real brand fonts. No substitution is acceptable.** |
| **Apple Pages / Numbers / Keynote** | ⚠ Must be installed locally from `assets/fonts/` | ⚠ Must be installed locally from `assets/fonts/` | Install first, or the document silently substitutes Helvetica |

Practical rule: **a Google deliverable set in Arial is a defect, not a compromise.** There is no scenario where Google Workspace cannot render HBEF's typography correctly.

### Adding Aleo and Lato in Google Workspace

Do this once per Google account; the fonts then appear in the font dropdown for every Doc, Sheet, and Slide.

1. Open any Google Doc, Sheet, or Slide.
2. Click the **font-name dropdown** in the toolbar (it will say "Arial" by default).
3. At the top of the list, click **"More fonts"** (in Sheets, the same control reads **"More fonts"** at the top of the font menu; in Slides it is at the bottom of the dropdown).
4. In the search box, type **`Aleo`**. Click the `Aleo` result — it moves to the "My fonts" column on the right.
5. Clear the search, type **`Lato`**. Click the `Lato` result.
6. Click **OK**.
7. Both now appear in the toolbar dropdown, permanently, for this account.

**Weights.** Google's font picker exposes weights through the toolbar's bold control and, for the extended weights, through the "More fonts" dialog's *Show:* filter set to "All fonts" and *Sort:* "Popularity."

- **Aleo** ships Regular 400, Bold 700, Italic, Bold Italic — everything HBEF needs.
- **Lato** ships Light 300, Regular 400, Italic, Bold 700, Bold Italic, Black 900. In Google Docs, Light and Black appear in the font dropdown as separate entries — **`Lato Light`** and **`Lato Black`** — once added via "More fonts." Add all three entries (`Lato`, `Lato Light`, `Lato Black`) if the deliverable needs the cover subtitle (Light 300) or a large-format CTA label (Black 900).
- If `Lato Light` does not appear as a separate dropdown entry, Google Slides will render Light as Regular. Accept Regular rather than faking it — never simulate Light by reducing opacity or switching to a gray.

**Sharing gotcha:** fonts added via "More fonts" are attached to *your* account, but the *document* stores the font name. A collaborator who hasn't added Aleo will see the document render in a fallback until they add it themselves. For board-wide documents, either (a) tell recipients to add Aleo + Lato once, or (b) share a PDF export instead.

### Installing Aleo and Lato for Apple iWork

Pages, Numbers, and Keynote read from the system font library — they have no equivalent of Google's "More fonts." The TTFs **must be installed on the Mac before authoring.**

**Bundled files** (`assets/fonts/` in this skill):
```
Aleo-Regular.ttf      Lato-Light.ttf
Aleo-Bold.ttf         Lato-Regular.ttf
Aleo-Italic.ttf       Lato-Italic.ttf
Aleo-BoldItalic.ttf   Lato-Bold.ttf
Aleo-OFL.txt          Lato-BoldItalic.ttf
                      Lato-Black.ttf
                      Lato-OFL.txt
```

**Install (macOS):**
1. Open `assets/fonts/` in Finder.
2. Select all ten `.ttf` files (⌘A, then deselect the two `-OFL.txt` license files).
3. Double-click → **Font Book** opens → click **Install Font**. Or drag the files onto the Font Book window.
4. **Quit and relaunch Pages / Numbers / Keynote.** iWork caches the font list at launch; a running app will not see newly installed fonts.
5. Verify: in Pages, Format → Style → font dropdown → type "Aleo". You should see Aleo with Regular/Bold/Italic/Bold Italic in the typeface submenu, and Lato with Light/Regular/Italic/Bold/Bold Italic/Black.

Command line alternative:
```bash
cp assets/fonts/Aleo-*.ttf assets/fonts/Lato-*.ttf ~/Library/Fonts/
```

**Homebrew alternative** (installs the full Google Fonts releases):
```bash
brew install --cask font-aleo font-lato
```

**License:** both families are **SIL Open Font License 1.1**. Installing them, embedding them in a PDF, and redistributing them with a document are all explicitly permitted. There is no cost and no approval needed.

### If the fonts are NOT installed (Apple fallback)

iWork substitutes silently — it does **not** warn you. A Pages document authored on a machine without Aleo will open showing Helvetica, and the font name in the inspector may still read "Aleo" with a "missing font" badge you have to look for.

**Fallback order, in preference:**

| Aleo unavailable → | Where it comes from | Notes |
|---|---|---|
| 1. **Roboto Slab** | Google Fonts (`brew install --cask font-roboto-slab`) | Closest match in tone and weight |
| 2. **Zilla Slab** | Google Fonts | Correct category, quirkier |
| 3. **Rockwell** | Microsoft Office for Mac install | Heavier geometric slab; acceptable |
| 4. **Georgia** | **Preinstalled on every Mac** | Not a slab, but a sturdy bracketed serif. **This is the realistic Apple fallback** — it needs no install. |
| ✗ Never | Helvetica, Arial, Avenir, Futura, any sans | Aleo must fall back to a slab or serif. A sans headline over a sans body destroys the pairing. |

| Lato unavailable → | Where it comes from | Notes |
|---|---|---|
| 1. **Helvetica Neue** | Preinstalled on every Mac | Neutral; loses Lato's warmth but sets cleanly |
| 2. **Helvetica** | Preinstalled | |
| 3. **Arial** | Preinstalled | Last resort |
| ✗ Never | Calibri, Times New Roman, Comic Sans, Papyrus, script faces | |

**Checking for missing fonts in iWork:** Pages/Keynote/Numbers → **Format → Advanced → (or) the yellow "Missing Fonts" banner** that appears at the top of the document on open. Click **Replace Fonts…** and map to the fallbacks above rather than letting the app pick.

**If you cannot install fonts on the target machine, export a PDF instead** — fonts are embedded and the typography survives regardless of what the recipient has. See §"When to export PDF instead."

---

## Path 1: Export from Office (recommended)

Generate the file using the Word/Excel/PowerPoint pattern from this skill, then:

| Target format | Export path | Fidelity |
|---|---|---|
| **Google Docs** | Upload `.docx` to Drive → right-click → "Open with Google Docs" | High — preserves styles, tables, images. Aleo/Lato names carry over; add the fonts once and they render correctly. |
| **Google Sheets** | Upload `.xlsx` to Drive → "Open with Google Sheets" | High — preserves formulas and fills. Tab colors transfer. Charts usually need a restyle. |
| **Google Slides** | Upload `.pptx` to Drive → "Open with Google Slides" | Medium — layout drift on complex slides, and full-bleed Navy bands sometimes inset. Verify every slide. |
| **Apple Pages** | Open `.docx` directly in Pages | High — Pages handles docx well. Watch table header fills. Fonts must be installed first. |
| **Apple Numbers** | Open `.xlsx` directly in Numbers | Medium — Numbers re-flows a grid into floating tables. Charts almost always need rebuilding. |
| **Apple Keynote** | Open `.pptx` directly in Keynote | Medium — fonts and full-bleed fills shift. Verify each slide. |

**Verification step (do not skip):** open the converted file and confirm three things — (1) headings are Aleo, not a serif fallback; (2) body is Lato, not Arial/Helvetica; (3) Navy renders as `#0C3B5D`, not a re-quantized neighbor. Then PDF-export and eyeball the result.

---

## Path 2: Manual paste-in styling (native authoring)

### Google Docs

**Page setup** (File → Page setup):
- Letter (8.5" × 11"), portrait
- Margins: **1"** left/right/bottom; **2"** top if you are reproducing letterhead, 1" otherwise
- Page color: **White** (`#FFFFFF`) — the 2026 system has **no gray page frame**

**Define paragraph styles** (apply the formatting to a paragraph, then Format → Paragraph styles → *[style]* → "Update *[style]* to match"):

| Google style | Font | Size | Weight | Color | Other |
|---|---|---|---|---|---|
| Title | **Aleo** | 40 | Bold | `#0C3B5D` | **Sentence/title case, no letter-spacing** |
| Subtitle | **Lato Light** | 18 | Regular | `#186892` | Sentence case |
| Heading 1 | **Aleo** | 24 | Bold | `#0C3B5D` | Line spacing 1.2; 24pt before, 8pt after |
| Heading 2 | **Aleo** | 16 | Bold | `#186892` | Line spacing 1.25; 18pt before, 6pt after |
| Heading 3 | **Lato** | 12 | Bold | `#0C3B5D` | UPPERCASE (type it uppercase — Docs has no text-transform) |
| Heading 4 (eyebrow) | **Lato** | 9 | Bold | `#98989A` | UPPERCASE |
| Normal text | **Lato** | 11 | Regular | `#515962` | **Line spacing 1.5**, 8pt after |
| Normal (lead) | **Lato** | 13 | Regular | `#515962` | Line spacing 1.45, 12pt after |

**Custom colors:** click any color control → **Custom** → **+** → paste the hex **without** the `#`, e.g. `0C3B5D`. Google saves it to the "Custom" swatch row for the rest of the session. Build the row once at the start in this order so you can click rather than retype:

```
0C3B5D  186892  129FDA  FFCD00  FFA400  EE7623  B8D8EB  DDC9A3  98989A  515962
```

**Add the HBEF logo:** Insert → Image → Upload from computer → `assets/logos/HBEF-Secondary_Lockup-RGB@2x.png` for a light header, or `HBEF-Secondary_Lockup-Dark_Mode-RGB@2x.png` if it sits on a Navy shape. Wrap "In line with text," ~3.5" wide, at the top of page 1. Keep clear space equal to the height of the "HBEF" lettering.

**Tables:** Insert → Table. Then select row 1 → Format → Table → Table properties → **Cell background color `#0C3B5D`**; set the row text to **Lato 10 Bold, White, uppercase**. Body cells: Lato 10 Regular `#515962`. Cell borders: **0.5pt `#D9D9D9`**. For a total row, fill `#E8F1F7` with Navy `#0C3B5D` bold text.

**Pull quote:** paragraph in **Aleo 15 Italic `#0C3B5D`**, indent 0.4", then Format → Paragraph styles → Borders and shading → **Left border 3pt `#FFCD00`**.

**Section band:** Insert → Drawing (or a single-cell table) filled `#B8D8EB` (Sky), 0.4" tall, full width.

**CTA:** Google Docs has no button element. Use a single-cell table filled **View `#FFCD00`** with centered **Lato Bold 11 `#0C3B5D`** text. **Never yellow text on white** — see `references/colors-and-fonts.md` §4.4.

**Footer (mandatory on donor-facing docs):** Insert → Headers & footers → Footer → paste in **Lato 8 Italic `#515962`**:

> HBEF is a registered 501(c)(3) non-profit organization. Contributions are tax-deductible to the extent allowed by law. Federal tax identification number (EIN): 33-0522270

Multi-page footer pattern: left "Hermosa Beach Education Foundation · hbef.org", right "Page N", both **Lato 9 `#98989A`**, with a 1pt `#186892` top border.

### Google Sheets

**Tab colors:** right-click tab → Change color → **Custom** → paste hex:
- Cover tab → `0C3B5D` (Navy)
- Summary tab → `186892` (Teal)
- Data tab → `B8D8EB` (Sky)
- Notes / appendix tab → `98989A` (Wet Sand)

**Sheet title (row 1):** **Aleo 16 Bold `#0C3B5D`** on White. Row height 28.

**Section header row:** Fill `#0C3B5D` → text **White, Lato 12 Bold**. Row height 22.

**Sub-header row:** Fill `#B8D8EB` (Sky) → text `#0C3B5D`, **Lato 11 Bold**.

**Data cells:** **Lato 10 Regular `#515962`** on White. Row height 18.

**Zebra striping:** Format → Alternating colors → Custom → Header `#0C3B5D` / Color 1 `#FFFFFF` / Color 2 `#F7FAFC`.

**Total row:** Fill `#E8F1F7` → text `#0C3B5D` **Lato 11 Bold** → top border **1pt `#0C3B5D`**.

**Borders:** all interior gridlines **`#D9D9D9`**, thin.

**Conditional formatting** for variance columns (Format → Conditional formatting → Format cells if… → Custom formula):
- `=A1>0` → text color `#4A8B5C` (Success)
- `=A1<0` → text color `#B23A2D` (Risk)
- Add a `▲` / `▼` prefix in the number format so the cue is not color-only — e.g. custom format `▲ #,##0;▼ #,##0`.

**Charts:** Insert chart → Customize.
- Chart style → Background color **White**, Chart border color **None**, Font **Lato**
- Series colors, in order: `#0C3B5D`, `#EE7623`, `#186892`, `#FFA400`, `#129FDA`, `#98989A`
- Gridlines → **`#D9D9D9`**
- Axis text → **Lato 9 `#98989A`**
- Title → **Aleo 14 Bold `#0C3B5D`**
- Remove the right and top axis lines (open frame). No 3D, no shadows, no more than 5 pie slices.

### Google Slides

**Slide size:** File → Page setup → **Widescreen 16:9**.

**Theme setup** (Slide → Edit theme):
- Background: **White `#FFFFFF`**
- Title font: **Aleo**, 28, Bold, `#0C3B5D`
- Body font: **Lato**, 16, Regular, `#515962`
- Theme colors (Slide → Edit theme → Colors → Choose a theme color → Custom):
  - Text 1 `#515962` · Background 1 `#FFFFFF`
  - Text 2 `#FFFFFF` · Background 2 `#0C3B5D`
  - Accent 1 `#0C3B5D` · Accent 2 `#EE7623` · Accent 3 `#186892` · Accent 4 `#FFA400` · Accent 5 `#129FDA` · Accent 6 `#98989A`
  - Hyperlink `#129FDA`

Setting the accents in **chart-series order** means Sheets charts pasted into Slides pick up the correct palette automatically.

**Cover slide:** Layout: Blank → Insert → Shape → Rectangle covering the **top third**, fill `#0C3B5D`, no border → Insert → Image → `HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png`, centered in the band, ~2.5" wide. Below: eyebrow **Lato 9 Bold `#98989A`** uppercase; title **Aleo 54 Bold `#0C3B5D`**; subtitle **Lato Light 20 `#186892`**. Bottom edge: a 0.25" full-width rectangle filled **`#FFCD00`**.

**Section divider:** Blank layout → full-bleed rectangle `#0C3B5D` → title **Aleo 40 Bold White**, sentence case.

**Content slide:** title **Aleo 28 Bold `#0C3B5D`**, subtitle **Lato 14 `#98989A`**, body **Lato 16 `#515962`**, bullets **Lato 14**.

**Stat slide:** number **Aleo 60 Bold `#0C3B5D`** (or `#EE7623` for donor-facing), label **Lato 11 `#98989A`**.

**Footer on every slide:** master → **Lato 9 `#98989A`** — "Hermosa Beach Education Foundation · hbef.org" left, slide number right.

**Known drift to check after any `.pptx` upload:** full-bleed rectangles sometimes inset by a few pixels; Aleo's wider metrics can push a 54pt cover title to two lines; and PowerPoint's letter-spacing on eyebrows may not survive. Fix these manually.

### Apple Pages

**Install Aleo and Lato first.** See the install section above. Relaunch Pages afterward.

**Document setup** (Document inspector):
- Letter, portrait; margins 1" (2" top for letterhead)
- Body font: **Lato 11**, color `#515962`
- Paragraph spacing: **8pt after**, line spacing **1.5**

**Define paragraph styles** (Format inspector → Style → paragraph-style dropdown → **+** to add): mirror the Google Docs table above exactly — Title Aleo 40 Bold `#0C3B5D`, Heading 1 Aleo 24 Bold `#0C3B5D`, Heading 2 Aleo 16 Bold `#186892`, Heading 3 Lato 12 Bold `#0C3B5D` uppercase, Body Lato 11 `#515962`.

**Color picker:** Pages uses the macOS color panel. Click the color well → the **color wheel icon** → in the panel, click the **sliders** tab → set the dropdown to **RGB Sliders** → paste the hex into the **Hex Color #** field at the bottom (with or without the `#`). Drag the swatch into the bottom palette tray to reuse it — build the same ten-color row listed under Google Docs.

**HBEF logo:** drag the PNG from Finder into the document. Arrange inspector → **Text Wrap: In line with text** for a header logo, or **Stay on Page** for a cover placement. Never scale non-proportionally (hold ⇧ while resizing).

**Tables:** Format → Table → pick a plain style, then override: header row fill `#0C3B5D`, header text **White Lato 10 Bold uppercase**; body cells **Lato 10 `#515962`**; gridlines **0.5pt `#D9D9D9`**. Avoid Pages' built-in "Dark" table styles — they carry their own tinted alternating rows that fight the HBEF zebra `#F7FAFC`.

**Pull quote:** Aleo 15 Italic `#0C3B5D`, indent 0.4". Pages has no left-border paragraph control — draw a 3pt `#FFCD00` line shape and group it with the text box, or use a two-column single-row table with the left cell filled View and set to 3pt wide.

**Export to PDF:** File → Export To → PDF → Image quality **Best**. Pages embeds fonts correctly, so the recipient does not need Aleo or Lato installed.

### Apple Numbers

Numbers' model differs from Excel — a sheet holds multiple free-floating tables rather than one grid. For HBEF deliverables:

- **Sheet 1 "Cover"** — one table, 4 cols × 8 rows, holding the title block and metadata. Title cell **Aleo 16 Bold `#0C3B5D`**.
- **Sheet 2+ "Data"** — one table per topic, each with its own styled header row.

**Header row:** select row 1 → Format inspector → Cell → Fill Color `#0C3B5D` → text **White, Lato 12 Bold**.

**Sub-header:** fill `#B8D8EB`, text `#0C3B5D` **Lato 11 Bold**.

**Data cells:** **Lato 10 `#515962`**, White fill. Alternating row color → Format → Table → **Alternating Row Color** → set to `#F7FAFC`.

**Total row:** Format → Table → **Footer Rows: 1** → fill `#E8F1F7`, text `#0C3B5D` Lato 11 Bold.

**Conditional highlighting:** Format inspector → Cell → **Conditional Highlighting** → "Greater than 0" → Custom Style → text `#4A8B5C`; "Less than 0" → text `#B23A2D`. Add a symbol in the cell format so the cue is not color-only.

**Charts:** Numbers charts are styled per-chart and per-series. Format → Style → Chart Colors → **Custom** → set each series manually in HBEF order (`#0C3B5D`, `#EE7623`, `#186892`, `#FFA400`, `#129FDA`, `#98989A`). Chart font: **Lato**; title **Aleo 14 Bold `#0C3B5D`**. Turn off the chart border and set the background to White.

**Export to PDF:** File → Export To → PDF → **Best (slow)**.

### Apple Keynote

**Install Aleo and Lato first.** Relaunch Keynote.

**Theme:** File → New → **"White"** (the plain one). Do not start from a styled theme — they carry gradients, shadows, and type that all violate the brand.

**Slide size:** Document inspector → Slide Size → **Widescreen (16:9), 1920 × 1080**.

**Edit Master Slides** (View → Edit Master Slides). Build six masters:

| # | Master | Build |
|---|---|---|
| 1 | **Title** | Navy `#0C3B5D` rectangle across the top third; `HBEF-Primary_Lockup_Tag-Dark_Mode-RGB@2x.png` centered in it. Title placeholder **Aleo 54 Bold `#0C3B5D`**; subtitle **Lato Light 20 `#186892`**. Bottom edge: 0.25" bar filled `#FFCD00`. |
| 2 | **Section** | Full-bleed `#0C3B5D`. Title placeholder **Aleo 40 Bold White**, sentence case. |
| 3 | **Content** | White. Top accent bar 0.05" `#186892`. Title **Aleo 28 Bold `#0C3B5D`**; subtitle **Lato 14 `#98989A`**; body **Lato 16 `#515962`**. |
| 4 | **Stat** | White. Centered number placeholder **Aleo 60 Bold `#0C3B5D`** (or `#EE7623` donor-facing); label **Lato 11 `#98989A`** beneath. |
| 5 | **Quote** | White or Sky `#B8D8EB`. **Aleo 32 Italic `#0C3B5D`**, with a 3pt `#FFCD00` rule to the left of the text box. Attribution **Lato 12 `#98989A`**. |
| 6 | **Closing** | Navy `#0C3B5D` full-bleed. Dark-mode lockup, tagline "Funding matters. Your donation, their future." in **Lato Light 20 `#B8D8EB`**, donate URL **hbef.org** in **Lato Bold 16 `#FFCD00`**. |

Every master gets a footer: **Lato 9 `#98989A`** (or `#B8D8EB` on Navy) — "Hermosa Beach Education Foundation · hbef.org" left, slide number right.

**Colors:** same macOS color panel and hex field as Pages. Build the palette tray once.

**Builds and transitions:** none, or **Dissolve** only. No Magic Move, no cube, no flip. HBEF decks are civic, not a product launch.

**Export:** File → Export To → **PDF** for review and email distribution (fonts embed); **PowerPoint (.pptx)** only when the recipient will edit it — and warn them they need Aleo + Lato installed.

---

## Document colophon note

When a deliverable will be forwarded to people outside the board, drop a small line into the colophon or final footer:

> *Set in Aleo and Lato, both free under the SIL Open Font License. If the typography looks different on your machine, install them from fonts.google.com/specimen/Aleo and fonts.google.com/specimen/Lato — the content is unchanged.*

For Google-native documents, the more useful version is:

> *This document uses Aleo and Lato. If they look wrong, open the font dropdown → "More fonts" → search for each and click OK. One-time setup per Google account.*

---

## When to export PDF instead

Choose PDF whenever font control, layout fidelity, or version discipline matters more than editability.

**Export PDF — do not send the native file — when:**

- **The recipient is outside the HBEF board or staff.** Donors, sponsors, vendors, district administrators, and press should never receive an editable file. PDF embeds Aleo and Lato so it renders correctly regardless of what they have installed.
- **The deliverable is final.** Annual reports, solicitation letters, sponsor decks after the pitch, IC memos, board minutes once approved.
- **You cannot install fonts on the target machine** and the deliverable is Apple-native. A Pages file authored with a Georgia fallback is a compromise; a PDF exported from a machine that *does* have Aleo is not.
- **The layout is fragile** — full-bleed Navy bands, precise logo clear space, a cover with a 0.25" View footer strip. Google Slides and Keynote both drift on these.
- **It is going to print.** Export **CMYK PDF/X** using the CMYK `.eps` logos from the master library, with 0.125" bleed. See `references/colors-and-fonts.md` §2.
- **It contains donor data, financial detail, or IC content.** A PDF with restricted sharing is a smaller surface than a live collaborative document.

**Keep it native — do not flatten to PDF — when:**

- **Multiple board members will edit simultaneously** (fundraising tracker, volunteer signup, event budget). Google Sheets, styled manually per the recipes above.
- **The document is a living record** revised across meetings (working minutes, running task list).
- **Someone will present it live from a Mac** — Keynote's presenter display beats a PDF.
- **The recipient explicitly asked for an editable file** and is internal.

| Scenario | Recommended path |
|---|---|
| One-off letter, memo, brief | Generate `.docx` → export PDF → send PDF |
| Recurring board document (minutes, treasurer report) | Generate `.docx` → open in Google Docs for collaborative editing |
| Live-collab fundraising / auction tracker | Native Google Sheets, manual styling |
| Sponsor pitch deck, presented in person on a Mac | Generate `.pptx` → open in Keynote (fonts installed) → present |
| Sponsor pitch deck, emailed to a prospect | Generate `.pptx` → export **PDF** → send PDF |
| Annual report (final, print-ready) | Generate `.docx` → export **CMYK PDF/X** |
| Email-attachment one-pager | Generate PDF directly (HTML→PDF path) |
| Anything a donor or vendor will open | **PDF, always** |

---

## Final guardrails

- **Don't accept default fonts.** Aleo and Lato are both free and both available in Google Workspace natively — an HBEF Google Doc in Arial means someone skipped a two-minute setup step. Fix it before publishing.
- **Aleo must never fall back to a sans.** If Aleo is unavailable, the fallback is Georgia (or Roboto Slab / Zilla Slab / Rockwell if installed) — never Helvetica, Arial, or Avenir. The slab-over-sans contrast is the pairing.
- **Verify brand color codes after conversion.** Some apps re-quantize hex to a nearby palette swatch. After uploading a `.docx` to Google Docs, click a Navy heading and confirm it reads `0C3B5D` — not `0B4261` (that's the *retired* navy) and not a neighboring value.
- **No gray page background.** The retired system framed content on `#E7E7E7`. The 2026 system sits content on **White**, with **Sky `#B8D8EB`** or **Sand `#DDC9A3`** as the tinted band. If you see a gray page frame, it's a legacy file — see `references/legacy-brand.md`.
- **No yellow text.** View `#FFCD00` (1.50:1) and Vista `#FFA400` (1.99:1) fail WCAG contrast on white at every size. Yellow is a **fill** with Navy text on top. This applies identically in Docs, Slides, Sheets, Pages, Numbers, and Keynote.
- **Logo files travel with the doc** in all six apps — Pages, Keynote, Numbers, Docs, Slides, and Sheets all embed images. No need to re-link. But do check that a light-background lockup didn't end up on a Navy fill; swap to the `Dark_Mode` file if so.
- **Confidentiality:** Google Drive can default to broad link sharing. Set permission to **Restricted** or to specific board addresses before sharing donor data, sponsor negotiations, or IC memos. Check this every time — not once.
- **Tax language is mandatory** on any donor-facing document, in every format: *"HBEF is a registered 501(c)(3) non-profit organization. Contributions are tax-deductible to the extent allowed by law. Federal tax identification number (EIN): 33-0522270."*
