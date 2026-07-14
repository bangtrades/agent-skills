# Runbook checklist — new gated client demo

Replace `<client>` (e.g. `summer-fridays`) and `<CLIENT>` subdomain label throughout.

## A. Demo app
- [ ] Client demo app exists (Next.js 14 App Router). Build with the client's brand skill + frontend-design.
- [ ] Copy gate files from `gate-files.md` into the app (`lib/auth`, `middleware.ts`, `app/login`, `app/api/auth/*`, `app/vadmin`, `app/api/vadmin`, `components/Watermark.tsx`).
- [ ] Mount `<Watermark/>` in the authenticated shell; render `/login` + `/vadmin` chrome-free.
- [ ] Confirm admin route is `app/vadmin/` (NOT `_`-prefixed).

## B. Env (Vercel project · Production)
```bash
TOKEN=<vercel-token>
add(){ printf '%s' "$2" | npx vercel env add "$1" production --token $TOKEN --force; }
add WL_SUPA_URL "https://frkfayhxtgcereutdyap.supabase.co"
add WL_SUPA_KEY "sb_publishable_…"            # publishable key (server-side only)
add WL_SESSION_SECRET "$(openssl rand -hex 32)"
add WL_DEMO_SCOPE "<client>"                   # e.g. summer-fridays
```

## C. Build + deploy + smoke
```bash
npx next build                                  # must be clean
npx vercel deploy --prod --yes --token $TOKEN
# smoke (replace URL):
U=<deployment-url>
curl -s -o /dev/null -w "%{http_code}\n" "$U/"        # 307 -> /login
curl -s -o /dev/null -w "%{http_code}\n" "$U/login"   # 200
curl -s -o /dev/null -w "%{http_code}\n" "$U/vadmin"  # 200
```

## D. Subdomain + DNS
```bash
npx vercel domains add <client>.waivelabs.ai --token $TOKEN   # from linked project dir
```
GoDaddy (`waivelabs.ai` DNS): add **CNAME** Host `<client>` → Value `cname.vercel-dns.com`
(or **A** Host `<client>` → `76.76.21.21`). Cert auto-issues in minutes.

## E. Issue / revoke (per recipient)
At `https://<client>.waivelabs.ai/vadmin` (admin secret):
- [ ] Issue code → name, org, expiry. Copy `WL-XXX-######`, send to the named person.
- [ ] After they confirm they've viewed → **Revoke** (instant, silent).
- [ ] **Reset device** if a legit viewer must switch machines.

## F. Record + hygiene
- [ ] Log subdomain, `WL_SESSION_SECRET`, `WL_DEMO_SCOPE`, codes issued → vault / password manager.
- [ ] Admin secret stays in password manager only; rotate via `vail_admin` (see access-schema.sql).
- [ ] Rotate the Vercel token periodically.
- [ ] All demo data must be synthetic / non-confidential to the *other* clients.

## Quick verify of the access RPCs (any host)
```bash
S=<admin-secret>; U=https://<client>.waivelabs.ai
curl -s -X POST "$U/api/vadmin" -H 'content-type: application/json' -d "{\"action\":\"list\",\"secret\":\"$S\"}"
```
