# Infrastructure — databases, deploys, gates, secrets

The proven stack (hard-coded by design; swap only when a client mandates otherwise):
**Next.js 14+ on Vercel · Supabase (Postgres + RLS) · waivelabs-secure-demo gate ·
Railway for agent control planes · GoDaddy DNS for waivelabs.ai.** Deploys and provisioning
are autonomous on standing WaiveLabs accounts; net-new recurring spend gets a `commercial`
Linear issue.

## Databases (Supabase MCP)

- **Pre-signature (demo gate):** use the shared `waivelabs` Supabase project. The
  secure-demo gate uses the shared `vail_*` schema scoped per demo
  (`demo = {client-slug}`) — one project serves all demos; access rows are per-demo,
  per-person. Do NOT create a new project just for a demo gate.
- **Post-signature (S8 data foundation):** create a **dedicated Supabase project per
  client** via the Supabase MCP (`create_project`; check `get_cost`/`confirm_cost` first —
  paid tier = `commercial` issue). Apply the base schema via `apply_migration`, enable RLS
  from the first table, run `get_advisors` (security + performance) before calling the
  foundation done, and record project ref + URLs in the client manifest.
- Use `list_tables` before schema changes; migrations for DDL, `execute_sql` for data.

## Gated demo deploys (waivelabs-secure-demo)

Follow the waivelabs-secure-demo skill for mechanics. Operational facts from the SF deploy:

- Wrap the demo in Next.js: `middleware.ts` gate → `app/login` → static app served from
  `public/` byte-identical, watermark injected at render.
- Vercel project per client (`vercel` CLI or Vercel MCP), prod domain
  `{client}.waivelabs.ai`.
- **DNS is manual:** waivelabs.ai has no wildcard record — add the per-client CNAME at
  GoDaddy pointing to `cname.vercel-dns.com`. Do it at deploy time, verify with the Vercel
  domain check, note it in the Linear issue. (SF's deploy sat behind this one hand step.)
- Access motion: create per-person codes (`WL-{CLIENT}-######`) via `/vadmin` or WaiveBoard
  › Demos; watermarked login binds identity; instant revoke + device reset. Codes are
  STAGED at deploy; issuing them to client viewers is G1.
- Honest posture (say it this way): screen capture can't be blocked — the gate makes leaks
  *attributable* and access *disposable*.
- **MCP deploy-tool ceilings are real:** inline file-tree deploy tools cap per-call payload
  well below a typical multi-file demo (~hundreds of KB). Probe with one file first; for the
  real deploy use the CLI/git path or the secure-demo pipeline. Never route a deploy through
  an interactive web login — agents must stop and report at any auth wall.
- **Transcription ceiling (all model tiers):** no agent can hand-transcribe ~50KB+ of
  byte-exact file content into an inline tool parameter — it degrades to placeholders. For
  multi-file demo payloads use channels that read bytes from disk directly: browser
  file-input upload into the platform's drop/import UI (works while the operator's browser
  session is authenticated), CLI with a token, or git. Splitting data files into <25KB-read
  chunks helps agents READ them but does not fix inline WRITE transcription.
- **Autonomy prerequisite:** keep a standing, pre-authorized deploy path (scoped CLI token in
  the gitignored `.deploy-secrets.local.md`, pre-created project) so the deploy slice needs
  zero human interaction. Until that exists, deploys are STAGED-by-default and the demo ships
  locally runnable.

## Secrets discipline (SF lessons, now rules)

- Tokens/keys never appear in chat, commits, or docs. Store per-project in a gitignored
  `.deploy-secrets.local.md`; reference by name everywhere else.
- Anything that was ever pasted in a conversation or committed is **burned — rotate it**
  (SF: Vercel + GitHub tokens shared in chat during deploy, flagged for rotation).
- Master/owner access codes must be bound to an identity, never left floating.
- Broker pattern for model keys: server-side broker holds the credential; the browser never
  sees it (SF `agent/server.mjs`).

## Dependency hygiene

Pin and check the framework version at deploy time (`npm audit`, release notes). SF shipped
Next.js 14.2.15 with a known advisory under demo time pressure — acceptable for a
short-lived gated demo ONLY if logged as a Linear issue with an upgrade-by date; never
acceptable for anything post-signature.

## Client-mandated platforms (e.g., Microsoft Fabric)

When the client's RFP mandates a platform outside our stack:
1. The demo stays on our stack, framed as a vision prototype (see proposal-legal.md).
2. Build the **simulation + hands-on lab** for their platform (data-simulation.md) to prove
   the migration path pre-contract.
3. Scope ownership cleanly in the proposal: client IT owns the platform; WaiveLabs owns the
   app + agent layer that reads from it.
4. Check platform access realities early — trials, capacity SKUs, tenant restrictions (SF:
   free Fabric trial unavailable on fresh tenants; paid F2 capacity ~$0.36/hr was the
   unblock → `commercial` issue).

## Live-agent broker (demo-day option)

`agent/` pattern from SF: Node broker (`server.mjs`) on localhost, `run.sh` one-command
launch, MOCK mode with no key as stage insurance, real model via env key. Every agent action
rendered as propose → human Approve. This demonstrates the governance story live and is
worth the extra day when the buyer's objection is control.

## Post-signature agent plane (S10)

WaiveBoard-validated pattern (2026-07-02): Railway-hosted langgraph control plane + agent
inbox, x-api-key auth; 4 starter specialists (Data/Insights, Sales & Marketing, Ops,
Engineering); memory schema in the client's Supabase; approval gates on write/spend/send;
audit logging on from day one.
