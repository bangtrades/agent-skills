---
name: waivelabs-secure-demo
description: >-
  Deploy a client demo app to a private, watermarked, revocable subdomain on the
  WaiveLabs site (e.g. summerfridays.waivelabs.ai) behind WaiveLabs' shared
  signed-cookie access gate. Use whenever bang wants to put a prospect/client demo
  "behind a login on waivelabs", issue or revoke per-person demo access, set up a
  gated demo subdomain, watermark a demo, or send a private build to a named viewer
  (Varian, Summer Fridays, CopperJoint, any prospect). Trigger on: "host the demo on
  waivelabs", "put it behind a login", "secure demo subdomain", "issue a demo code",
  "revoke their access", "gated client preview", "watermark the demo". Client-agnostic
  and reusable across every WaiveLabs engagement. Pairs with the client's brand skill
  for visual styling and with frontend-design/Next.js for the demo app itself.
license: Proprietary — WaiveLabs internal.
---

# WaiveLabs Secure Demo

Stand up a **private, per-recipient, instantly-revocable** client demo on a WaiveLabs
subdomain. This is the repeatable motion for sending impressive product demos to prospects
while keeping the IP private and every viewing attributable.

> [!warning] Honest security posture — say this to the client, and to yourself
> You **cannot** technically prevent screen-capture or recording of anything shown in a
> browser. This gate does the things that actually deter theft: it makes every leak
> **attributable** (identity watermark) and access **disposable** (per-person codes,
> instant silent revocation, single-session/device binding, auto-expiry). Pitch it that
> way; never claim capture is "blocked."

## What you get
- A client demo at `client.waivelabs.ai` (its own Vercel project + subdomain).
- A branded **login** (access code, not a shared password).
- **Per-recipient codes** with: instant silent revoke, single-session/device binding,
  auto-expiry, an identity **watermark** (name · org · timestamp tiled on every screen),
  and right-click/copy friction.
- Two ways to manage codes against ONE shared store:
  - **WaiveBoard › Demos** (`waiveboard.vercel.app/app/demos`) — the **primary console**: issue /
    revoke / reset codes across *all* clients + usage analytics (views, logins, activity feed),
    behind bang's existing magic-link admin login.
  - **Per-demo `/vadmin`** on each client subdomain — standalone fallback (works even if WaiveBoard
    is down; gated by the admin secret directly).
- One **shared Supabase access-control schema** serves all client demos; each code is
  **scoped to one demo** so a Summer Fridays code can't open the VAIL demo.
- An **owner code** with `unbound = true` (no expiry, no device-lock) for bang's own viewing.

## Architecture (one diagram in words)
```
WaiveBoard /app/demos ──┐  (issue/revoke/usage — primary console, behind admin login)
client /vadmin ─────────┤──► shared Supabase access schema (project waivelabs)
                        │      vail_admin_create / _revoke / _reset / _list / _events
                        │      vail_login / vail_check   (SECURITY DEFINER; admin secret DB-side)
client demo (Next.js, its own Vercel project)
  └─ subdomain client.waivelabs.ai  (GoDaddy CNAME → cname.vercel-dns.com)
  └─ middleware gate  ── per-navigation liveness check ──► Supabase RPCs (instant revoke)
        • signed httpOnly cookie (HMAC)
        • DEMO_SCOPE enforces code↔demo match
  └─ /login, identity watermark; /vadmin standalone fallback
```
The gate code is **portable**: drop the files from `references/gate-files.md` into any
Next.js (App Router) client demo, set 4 env vars, deploy. The Supabase schema in
`references/access-schema.sql` is provisioned **once** (project `waivelabs`,
`frkfayhxtgcereutdyap`) and reused by every demo.

---

## Runbook

### 0. Prereqs (one-time, already done for WaiveLabs)
- Supabase access-control schema applied to the `waivelabs` project (see
  `references/access-schema.sql`). Admin secret hash stored in `public.vail_admin`.
- You have: the Vercel token (or dashboard access), GoDaddy DNS access for `waivelabs.ai`,
  the Supabase **publishable** key + project URL, and the **admin secret** (password manager).

### 1. Have the demo app
Any Next.js 14 App Router app. If starting fresh, build it with the client's brand skill +
`frontend-design`. The gate is brand-neutral (inline styles + a few CSS vars with fallbacks);
it adopts the client's palette if you pass brand vars.

### 2. Drop in the gate
Copy these into the demo app (full source in `references/gate-files.md`):
- `lib/auth/session.ts` — Web-Crypto HMAC signed cookie (edge + node safe)
- `lib/auth/supa.ts` — Supabase RPC caller (publishable key, server-side only)
- `middleware.ts` — gates all pages; re-checks code liveness every navigation (→ instant revoke); enforces `DEMO_SCOPE`
- `app/login/page.tsx` — branded access-code screen
- `app/api/auth/{login,logout,me}/route.ts`
- `app/vadmin/page.tsx` + `app/api/vadmin/route.ts` — admin console
- `components/Watermark.tsx` — identity watermark + capture friction
- Mount `<Watermark/>` in the layout/shell when authenticated; render `/login` and `/vadmin` without the app chrome.

> [!warning] Route naming gotcha
> The admin route MUST be `app/vadmin/` — NOT `app/__vadmin/`. The Next.js App Router treats
> any folder starting with `_` as **private (non-routable)** → it 404s.

### 3. Env vars (Vercel project · Production)
| Var | Value |
|---|---|
| `WL_SUPA_URL` | `https://frkfayhxtgcereutdyap.supabase.co` |
| `WL_SUPA_KEY` | the Supabase **publishable** key (`sb_publishable_…`) — safe server-side |
| `WL_SESSION_SECRET` | a fresh `openssl rand -hex 32` per demo |
| `WL_DEMO_SCOPE` | this demo's scope, e.g. `summer-fridays` (codes must match) |

Admin secret is **not** an env var — it lives as a bcrypt hash in `public.vail_admin` and is
verified DB-side by the RPCs.

### 4. Deploy + subdomain
```bash
# from the demo app dir
npx vercel deploy --prod --yes --token <TOKEN>
npx vercel domains add client.waivelabs.ai --token <TOKEN>   # from the linked project dir
```
Then add ONE DNS record at GoDaddy for `waivelabs.ai`:
- **CNAME** · Host `client` · Value `cname.vercel-dns.com` (or A `client` → `76.76.21.21`).
Vercel auto-issues TLS within minutes of the record resolving.

### 5. Issue / revoke (the daily motion)
**Primary: WaiveBoard › Demos** — `waiveboard.vercel.app/app/demos` (behind bang's magic-link admin login). One console for *every* client demo + usage analytics. Requires env `VAIL_ADMIN_SECRET` on the WaiveBoard Vercel project (server-side only; the page inherits WaiveBoard's admin gate, so the secret is never in the browser).
1. **Issue** — recipient name + org + **demo scope** (vail / summer-fridays / …) + expiry → copy code (e.g. `WL-SF-481922`), send it.
2. They log in at `<demo>.waivelabs.ai/login`, view the demo (watermarked with their name).
3. Confirm they've viewed → **Revoke**. Bounced to login on their next click, no warning.
4. **Reset device** if a legitimate viewer must switch machines (single-session binding).
5. Watch the **activity feed** + per-code view counts to see who viewed, when, from where.

**Fallback: per-demo `/vadmin`** — `client.waivelabs.ai/vadmin`, enter the admin secret directly. Same actions, scoped to that one demo; use if WaiveBoard is unavailable.

**Owner login:** mint one code with `unbound = true` (use `vail_admin_create2(..., p_unbound => true)` or set the column) — no expiry, no device-lock — for bang's own viewing across devices (e.g. `WL-BANG-MASTER`).

### 6. Hand-off note to bang
Record per-demo in the vault / password manager: subdomain, `WL_SESSION_SECRET`, `WL_DEMO_SCOPE`,
admin console URL, and the codes issued. Reuse the one admin secret across demos (or set a
distinct one per demo by storing multiple hashes — see schema notes).

---

## Reusing for a new client (the 10-minute version)
1. Demo app exists (brand skill + frontend-design).
2. Copy the gate files (`references/gate-files.md`), set `WL_DEMO_SCOPE=<client>`.
3. `vercel deploy` → `vercel domains add <client>.waivelabs.ai` → GoDaddy CNAME.
4. Issue a code in `/vadmin` scoped to `<client>`. Send. Revoke when done.

## Troubleshooting
- **`/vadmin` 404** → folder was `_`-prefixed; rename to `app/vadmin`.
- **Login says `in_use`** → single-session binding; "Reset device" in admin, or the viewer is on a new network.
- **Cert pending** → DNS record not resolving yet; recheck the GoDaddy CNAME.
- **All logins fail `invalid`** → wrong `WL_SUPA_URL/KEY`, or code's `demo` ≠ `WL_DEMO_SCOPE`.
- **Admin `unauthorized`** → wrong admin secret (verified against `vail_admin` hash).

## Files
- `references/gate-files.md` — portable gate source (copy-paste).
- `references/access-schema.sql` — the shared Supabase schema + RPCs (idempotent; incl. `unbound` + events).
- `references/waiveboard-demos-module.md` — the WaiveBoard `/app/demos` issuance + analytics console (primary).
- `references/runbook-checklist.md` — the tight ops checklist + commands.

## Reference deployment
First use: **VAIL** (Varian/Siemens) at `vail.waivelabs.ai`. Code/IP and full build live in the
Healthcare Context Engine project; this skill is the generalized, client-agnostic motion extracted
from it.
