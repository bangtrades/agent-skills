# WaiveBoard "Demos" module — the primary issuance + analytics console

The recommended home for issuing/revoking codes across **all** client demos and watching usage,
since WaiveBoard (`waiveboard.vercel.app/app`, repo `bangtrades/waiveboard`) already runs on the
same Supabase project (`frkfayhxtgcereutdyap`) and is behind a magic-link admin allowlist.

## Why here (vs per-demo `/vadmin`)
- One console for every client demo (VAIL, Summer Fridays, …) — not one per subdomain.
- Inherits WaiveBoard's existing admin auth → the admin secret lives **server-side only**
  (`VAIL_ADMIN_SECRET` env), never in the browser.
- Usage analytics: views per code + a cross-demo access-activity feed (logins/denials/revokes).
- `/vadmin` on each demo remains a standalone fallback.

## What was built (in `bangtrades/waiveboard`)
- `src/app/app/demos/page.tsx` — server component: KPIs (active codes, total codes, total views,
  logins-24h), an **issue** form (recipient · org · **demo scope** select · expiry), a codes table
  with Revoke / Restore / Reset-device, and a recent **access-activity feed**. Uses WaiveBoard's
  Tailwind theme (`navyline`, `deep2`, `ondeepsoft`, `sun`, `blue`, `font-sora`).
- `src/app/app/demos/actions.ts` — `'use server'` actions calling the shared RPCs via the
  existing `getSupabaseServer()` client: `vail_admin_list/_create/_revoke/_unrevoke/_reset_session`,
  with `VAIL_ADMIN_SECRET` from env. `revalidatePath('/app/demos')` after writes.
- `src/app/app/layout.tsx` — added a **Demos** nav link.
- Page reads the activity feed via `vail_admin_events(p_admin, p_limit)`.

## Setup
1. Env on the WaiveBoard Vercel project (Production): `VAIL_ADMIN_SECRET = <the admin secret>`.
   (No new Supabase env needed — WaiveBoard already has `NEXT_PUBLIC_SUPABASE_URL` + anon key.)
2. Commit + push `bangtrades/waiveboard`; Vercel deploys.
3. Open `waiveboard.vercel.app/app/demos`.

## To replicate for another agency cockpit
Drop the same two files + nav link into any admin-gated Next.js app on the shared Supabase, set
`VAIL_ADMIN_SECRET`, done. The RPCs are demo-agnostic; the issue form's `demo` field scopes each
code to the right subdomain (a code's `demo` must match that demo app's `WL_DEMO_SCOPE`).

## Owner login
Mint one `unbound = true` code (e.g. `WL-BANG-MASTER`) — no expiry, no device-lock — for bang's
own viewing across devices. The Demos table shows it as "owner · persistent".
