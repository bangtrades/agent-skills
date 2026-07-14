# waive-proposal — improvement log

Newest first. After every use of this skill, append a dated entry: the engagement, what was
learned/changed, and the concrete rule for next time. Promote durable lessons into
`references/proposal-playbook.md` or `SKILL.md` so they become default behavior.

---

## 2026-06-16 — Summer Fridays (first use; skill created from this engagement)

- **Lean beat thorough, decisively.** The client wanted requirements → plan → timeline → cost,
  ~6 pages. A 16-page governance-rich draft (v0.3) was rejected as overkill; the trimmed 6-page
  v0.4 is what got sent. → **Rule:** default lean; depth sections only if the RFP demands them and
  they're in scope. (Now baked into the playbook.)
- **Kill the boxes.** Cover subtitle paragraph, footer tagline, "how to read the demo" callout,
  "companion documents" callout, and a "How We Work / Why Us" section were all explicitly cut. →
  **Rule:** no callout/quote boxes by default; `callout()` is opt-in only. (Baked in.)
- **Scope & ownership is the highest-leverage section.** The engagement flipped to "WaiveLabs owns
  the app + agents; client IT owns the data platform." Stating that split plainly up front is what
  made the doc coherent. → **Rule:** Scope & Ownership table is section 2, always.
- **Confirm commercial wording before writing it.** The deposit/closure payment schedule needed a
  cleaner phrasing and implied a committed term (not "monthly/cancellable"). Confirming the exact
  split + term with the user first avoided a rework. → **Rule:** verify payment schedule arithmetic
  and align the Term row to it.
- **Brand:** slogan is **"Ride the Waive."** (a prior draft had "Ride the AI wave." — wrong).
- **Build system:** parameterized `wlstyle.COVER` + `CLIENT` so the cover/header are per-engagement
  config, not hardcoded. Worked example = SF v0.4.
