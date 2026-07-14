# Build system — branded proposal PDF

ReportLab-based. Two files do the work: `wlstyle.py` (design system) and a build script
(`build_proposal_template.py`, a runnable worked example).

## Run

```bash
# 1. deps
pip install reportlab pypdf --break-system-packages

# 2. fonts — wlstyle.py loads fonts from /tmp/fonts
mkdir -p /tmp/fonts && cp assets/fonts/* /tmp/fonts/

# 3. build dir with both py files
mkdir -p /build && cp templates/wlstyle.py templates/build_proposal_template.py /build/
cd /build

# 4. edit the CONFIG block at the top of build_proposal_template.py:
#    - CLIENT, OUT (absolute path), and the COVER dict (draft tag, title, prepared_for)
#    then edit the section CONTENT for the engagement.

# 5. build
python3 build_proposal_template.py        # prints "built <OUT>"

# 6. verify
python3 - <<'PY'
from pypdf import PdfReader
r=PdfReader("<OUT>"); t="\n".join((p.extract_text() or "") for p in r.pages)
print("pages:", len(r.pages))   # expect ~5–7 for a lean proposal
PY
```

## Helper API (in `wlstyle.py`)

- `section(num, title, kicker_suffix="")` → returns flowables for a numbered section header
  (orange kicker + blue title + rule). `kicker_suffix` shows e.g. "DELIVERABLE 4".
- `data_table(header, rows, widths, header_bg=BLUE, note=None, sub=None)` → striped table; `note`
  adds a small gray footnote; `sub` adds a bold subheading above it. Cells accept HTML strings
  (`<b>`, `&amp;`).
- `field_table(title, pairs)` → 2-col "Field / Detail" table with an INK header (used for
  per-item cards).
- `bullets(items)` → orange-tick bullet paragraphs (HTML allowed).
- `callout(title, body, accent=BLUE)` → boxed callout. **Default to NOT using this** (see
  playbook anti-patterns); it exists for the rare genuinely-important aside.
- `S[...]` paragraph styles: `body`, `lede`, `sub`, `tnote`, etc. `CW` = content width.
- `make_doc(path)` → BaseDocTemplate with Cover + Body page templates. Build with
  `doc.build(story)` where `story` starts `[NextPageTemplate("Body"), PageBreak()]`.

## Per-engagement config

`wlstyle.CLIENT` (running header) and the `wlstyle.COVER` dict (draft tag, title, subtitle,
slogan, prepared_for, doc_title, footer_conf) are overridden in the build script's CONFIG block
before `make_doc()`. Mutate via `wlstyle.CLIENT = ...` and `wlstyle.COVER.update({...})` (because
`make_doc`/cover read the live module globals).

## Gotchas

- **Fonts must be at `/tmp/fonts`** or registration fails. Re-copy each session (sandboxes reset).
- **`OUT` must be an absolute path** to a writable location.
- **Mounted-filesystem note:** on some mounts the post-build `.next`/temp unlink can EPERM for
  other toolchains, but ReportLab writes a single PDF and is unaffected. If a path under a mount
  errors, build to `/tmp` and copy the PDF to the destination.
- **Bump the cover draft version each iteration** (V0.1 → V0.2 …) so versions don't collide; write
  each version to its own filename (`..._v0_2.pdf`) to preserve history.
- Escape `&` as `&amp;` inside table/paragraph HTML strings. Avoid stray apostrophes inside
  single-quoted Python ternaries used in f-strings.
