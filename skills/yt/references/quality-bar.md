# Quality bar — worked examples

The difference between a vault page and a summary is **judgment applied to the source**. These are
real examples from the corpus.

---

## Key Takeaways

A takeaway is an insight that survives being read alone, six months later, by someone who never
watched the video. It carries the mechanism, not just the label.

**❌ Summary voice — says a thing was discussed**

> The speaker discussed the importance of context windows and how compaction affects agents.

**✅ Insight voice — states the mechanism and its consequence**

> 🔥 **A rule in the context window is a rule with a TTL.** In the Meta inbox demo, compaction
> evicted the safety instruction and the agent then did the thing it had been told not to do. The
> fix isn't a firmer prompt — it's moving the rule into code: data contracts as Pydantic schemas,
> action contracts as `BeforeToolCall` hooks, authority contracts as IdP tokens.

**Why the second works:** names the failure, cites the concrete instance, and gives the structural
remedy. Someone can act on it without the video.

### Mechanics

- 5–8 bullets. Mark the best 1–3 with 🔥.
- Lead with a **bolded claim**, then the evidence.
- Quote the speaker directly when the phrasing is the value — *"never send an agent to do
  deterministic code's job."*
- Keep real numbers: `200 samples @ 3% → CI 0.6–5.4%`, `660 tokens / 38 skills`, `4% → 24%`.
- **Count recurrences.** "This is the 5th source for generator ≠ verifier" is more valuable than
  the observation itself, because it tells bang the pattern is load-bearing.

---

## Relevance to Our Work

The section that earns the page its existence. Structure it as numbered `###` sub-sections, one
per real connection. Each should name a project, say what changes, and be specific enough to argue with.

**❌ Generic**

> This is relevant to our agent work and could be useful for the trading system.

**✅ Specific and opinionated**

> ### 3. 🔥 It reframes the NQ Backtest Lab as a control loop
>
> The [[projects/nq-backtest-lab/nq-backtest-lab|NQ Lab]] *already is* one, and naming it sharpens
> it: **set-point** = target equity-curve shape; **sensor** = DuckDB metrics + regime segmentation;
> **controller** = which parameter variation to try next (currently bang's judgment — could be
> telemetry-driven, à la Mistele's APM heuristic: prioritize where the current config bleeds most);
> **actuator** = config change + 1s fill sim.

**Why it works:** maps the source's framework onto a real system component-by-component, and ends
with a concrete change to make.

### Say so when it isn't relevant

A `low` rating with an honest paragraph on why it's still worth having for search is a good page.
Padding a weak source into false relevance is worse than skipping it.

---

## Source integrity — flag, don't launder

The corpus is only as trustworthy as its weakest uncritical page. Three checks, surfaced *in the page*:

**Undemonstrated numbers.** Marketing percentages are usually asserted with no methodology.

> ⚠️ The talk's headline "73% / 89% / 92%" improvement figures are stated on a slide with no
> methodology, dataset, or baseline given, and nothing in the demo measures them. Treat as
> directional marketing, not evidence.

**Mislabeled sources.** Reuploads and clickbait retitles are common — and naming the mismatch can
turn a bad source into a real insight.

> ⚠️ **Source integrity.** This is titled as an Anthropic talk about abandoning loops; it is
> actually a 2024 LangGraph conference talk by the same speaker arguing the *opposite* (constrain
> the control flow). Useful precisely for that: read against his 2026 Anthropic talk, it's a
> two-point timeline of how one practitioner's thinking moved as models got stronger.

**Backtest contamination.** LLM results on well-known tickers are frequently contaminated.

> ⚠️ The framework is evaluated on AAPL over a period inside the model's training window. The model
> plausibly knows what the stock did. The reported returns are not evidence of generalizable edge.

---

## Action Items

Concrete, assignable, and scoped. Checkbox format.

- ❌ `- [ ] Consider looking into better verification approaches`
- ✅ `- [ ] Adopt `ast-grep` as the structural sensor for hygiene loops (Wick, AOS, Paperclip) — language-agnostic and out-of-band from configs the agent can disable`

If an item is a genuine build, say what the first slice is. If it's an evaluation, say what would
make it a yes.

---

## Detailed Notes

Organized **by topic, not chronology**. Sub-headers carry timestamp ranges so someone can jump
back to the video: `### Building the control loop (06:30–13:20)`. This section is for the reader
who wants depth on one thread without rewatching 18 minutes.
