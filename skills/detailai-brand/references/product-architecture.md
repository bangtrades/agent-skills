# DetailAI — Product Architecture

## SKUs (flat, two only — "Two ways in. No tiers, no meters.")

1. **The Agent — $499/mo, no setup fee.** AI lead-response + instant quoting + booking. Channels: missed-call text-back (primary wedge), inbound SMS, web chat. Pipeline: lead arrives → instant text-back → vehicle classification → quote generated from the shop's uploaded menu (services × tiers × vehicle classes, trained on the shop's voice) → appointment booked, quote "subject to confirmation by the shop."
2. **The Agent + Studio Site — $699/mo, $999 build fee (waived on 6-month commitment).** Everything above plus a DetailAI-built, hosted premium website with the agent native to it; written for local search and AI answer engines (AEO).

Pricing principles: flat monthly, month-to-month, no per-booking fees, no meters, no per-user fees. Never introduce tiered/metered framing in any deliverable.

## Target customer

Premium auto-detailing studios: ceramic coating, paint correction, PPF. Average tickets $2,000+. Owner-operator craftsmen. Explicit anti-market: volume car washes, $39 washes. Demo form qualifies on monthly revenue ($20K–$150K+ bands).

## Roadmap framing (public)

"Quoting is the first movement. Reputation, lifecycle, social, search, and analytics follow — same platform, same rate." Frame future modules as movements of one composition, not add-ons or upsells.

## MVP build scope (internal, from dossier Vector 1)

Missed-call/SMS webhook → vehicle classification → menu-priced quote → booking hold. Hard core: shop-menu ingestion (price sheet → agent). Companion instrumentation: recovered-revenue ledger per shop (leads answered after-hours, quotes sent, bookings closed) — this ledger is the retention artifact and case-study generator.

## Demo persona

**Apex Studio** — the current owner-selected demo identity (September 18, 2026). Earlier Meridian Detail Studio examples are historical; preserve them as history, not current configuration. Do not use fictional studio details as a carrier-registration legal identity. Sample inventory consistent with persona: ceramic coating packages, paint correction stages, interior detail tiers, SUV/sedan/coupe vehicle classes.

## Company facts

Nashville, TN · hello@detailai.ai · © 2026 · Tennessee governing law · prototype-stage, demo-gated ("Founding shops only"), built by WaiveLabs.


## Evidence scope — September 20 reconciliation

Public positioning and August research describe intended product promises. They are not fresh company, pricing, deployment or acceptance evidence. See the platform current-state document for actual limits, including paused photo classification and incomplete custom vehicle-class interpretation. Do not claim a quoted latency, automatic booking capability or persona enforcement as verified without workflow evidence. Owner-confirmed Apex branding supersedes older Meridian-only instructions.
