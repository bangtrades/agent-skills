# Client-Safe Language Rules

The reader is a prospective client's executive. Every term that raises a question they can't
answer themselves ("what's simulated data?", "is a prototype less than an app?") stalls the sale
and invites doubt about everything else in the document. The fix is never a euphemism — it's
choosing the true statement that doesn't need a footnote.

## The rules

| Never write | Write instead | Why |
|---|---|---|
| the client's name, products, retailers, founders | "a high-growth omnichannel consumer brand" (adjust category) | confidentiality is part of the pitch — leaking a name proves we'd leak theirs |
| prototype, proof-of-concept, POC, demo app | application, platform, build | "prototype" reads as unfinished; what shipped is real, deployed, and secured |
| simulated / mock / synthetic / dummy data | data; "a two-year commerce dataset engineered to the exact export formats of the systems a modern brand already runs" | true, specific, and reads as rigor instead of fakery |
| "AI wrote the code" framing | "the WaiveLabs agentic build process" | the buyer is buying WaiveLabs' process and accountability, not a model |
| revenue/profit impact claims | estimated hours saved, anchored to FTE fractions | hours are defensible; revenue claims we don't hold violate the honesty rule |
| point estimates ("15 weeks", "847 hours") | ranges and rounded figures ("14–16 weeks", "800+ hrs"), prefixed "Est." where applicable | precision implies measurement we didn't do; ranges read as experienced judgment |
| jargon: SSE, serverless, medallion, bronze layer, RPC, middleware | plain effect: "recommendations stream with their reasoning", "organized so it wires directly into your live systems" | page 4 may name real tech (Next.js, Vercel, Supabase, GPT-4o) — but every mention carries a plain-English "why it matters" |

## Words that are fine

Agent, AI, governed, human-approved, deployed, secured, calibrated, engineered, estimated,
confidential. "Simulation/practice scenario" is acceptable ONLY as a training-feature name (the
Academy coach runs practice scenarios) — prefer "practice scenarios" anyway so the lint stays
quiet.

## Mechanics

The engine lints all config strings against `forbidden_terms` (defaults cover the table above)
plus `client_terms`. Always populate `client_terms` per engagement: brand name (each word),
hero product names, named retailers/partners, founder names. After rendering, re-scan the PDF
text itself (`pdftotext | grep`) — the lint can't catch what's baked into images or added later.

## Tone check (brand-waive voice)

Confident, never hypey. Concrete numbers beat adjectives — "seven agents, 800+ hours" beats
"powerful transformative AI". Prose over bullets in narrative sections. End the document on a
question, not a pitch. Email CTA, never a calendar link. Verify the *i* in WaiveLabs.
