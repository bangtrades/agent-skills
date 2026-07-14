# Client Manifest — {Client Name}

> Single source of truth for this engagement. Every agent reads it before starting a slice;
> only bang edits the Commercials block (G2). Keep it current — stale manifests recreate the
> figure-drift problem this file exists to prevent.

## Identity
- **Client:** {legal name} ({slug})
- **Motion:** Enterprise co-dev | White-label partner | SMB/DTC
- **Decision-maker:** {name, role}
- **Champion(s):** {names}
- **Product name (LOCKED):** {e.g. "AI Growth Desk" — one name, never renamed mid-engagement}
- **Client folder:** ~/Projects/{Client}/
- **Linear project:** {url}
- **Dossier:** {path} · **Brand skill:** {name/path}

## Phase status
| Phase | Status | Exit artifact | Date |
|---|---|---|---|
| P0 Signal | | scorecard verdict: | |
| P1 Recon | | dossier + brand skill | |
| P2 Position | | thesis + demo spec | |
| P3 Demo | | gated URL: | |
| P4 Pitch | | deck + pricing (G2) | |
| P5 Close | | signed + paid | |
| P6–P8 | | | |

## Commercials (G2 — bang only edits this block)
- **Pricing model:** {tiers / monthly / milestone}
- **Figures:** {e.g. $60,000 total — $10k execution / $20k mo-1 / $20k mo-2 / $10k final; net-15}
- **Rate basis:** {e.g. 60 hrs/mo @ $350}
- **Term:** {e.g. 3-month initial}
- **Client-furnished:** {LLM API subs, DB, credentials, SME time, …}
- **Supersession note:** {e.g. "SOW No. 1 supersedes proposal v0.8 commercials"}

## Gate log (G1 sends / G2 approvals)
| Date | Gate | What | Approved by |
|---|---|---|---|

## Infrastructure
- **Demo URL:** https://{slug}.waivelabs.ai · DNS CNAME added: {y/n}
- **Vercel project:** {name} · **Supabase:** shared `waivelabs` (demo) / {client project ref} (delivery)
- **Secrets file:** {client folder}/.deploy-secrets.local.md (gitignored) · Rotation due: {}
- **Known-risk log:** {e.g. framework advisory + upgrade-by date}

## Open threads
- {running list of unresolved questions, client asks, follow-up cadence position}
