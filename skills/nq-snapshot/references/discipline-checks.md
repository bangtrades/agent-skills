# Discipline Checks — R1–R6 Pre-Trade Sanity

Every snapshot must close with an explicit R3/R5/R1 verdict. Without it, the snapshot is incomplete.

> Source authority: `~/Cortana/cortana-vault/research/topics/discipline-rules-nq.md`

## The Six Rules — Current Values

| Rule | Cap / Trigger | Source |
|---|---|---|
| **R1 — Position size cap** | Trend: $20/pt = 10 micros (or 1 mini); Range: $10/pt = 5 micros. **Provisional tightening from May 7-11 data: cap at $4/pt = 2 micros until 60+ 4-micro trades show sustained edge.** | discipline-rules-nq.md §R1 |
| **R2 — Revenge cooldown** | No entry within 2 min of a losing trade exit (5 min on range days) | §R2 |
| **R3 — Daily loss limit** | Hard stop at −$200 intraday OR 0.5 × smallest prop firm DLL, whichever is smaller. Range-day cap shrinks to −$80. | §R3 |
| **R4 — Minimum hold** | Targets at entry; no panic exits. **Hard 60s floor from May 12 data.** | §R4 |
| **R5 — Time-of-day filter** | **No trades**: 04:00–06:00 ET (London), 08:00–10:00 ET, 15:00–16:00 ET. Reduced size 1 contract exception with written pre-market plan. | §R5 |
| **R6 — Off-playbook** | Every trade must come from a documented setup in the matching archetype's playbook | §R6 |

## How to Run the Checks

### R5 — Time-of-Day (PRIMARY check, output first)

Get current ET time. Check against the table:

| Window (ET) | Status | Notes |
|---|---|---|
| 04:00–06:00 | **NO TRADE** | London open historic loss (-$278 in May 7-11) |
| 06:00–07:00 | **SWEET SPOT** | Best hour in May 7-11 (+$305 / 80% WR / 10 trades) |
| 07:00–08:00 | **TRADE** | Pre-NY-open buildup |
| 08:00–10:00 | **NO TRADE** | Historic losing window (-$678 Mar 2026 / -$130 May 7-11) |
| 10:00–10:10 | **CAUTION** | IB completing |
| 10:10–11:00 | **PRIMARY** | Post-IB primary window |
| 11:00–13:00 | **REDUCED** | Lunch chop — 1-contract textbook setup only |
| 13:00–14:30 | **TRADE** | Afternoon push window |
| 14:30–15:00 | **CAUTION** | Pre-3PM reversal |
| 15:00–16:00 | **NO TRADE** | Historic losing window (-$374 Mar 2026) |
| 16:00–18:00 | **NO TRADE** | Post-RTH dead window + Globex break (17-18 ET) |
| 18:00–04:00 | **REDUCED** | Globex / Asia / pre-London — 1-micro only on textbook setups |

**Output verbatim in the snapshot:**

```markdown
## R5 — Time-of-Day Verdict

Current time: HH:MM ET

Status: [NO TRADE / CAUTION / TRADE / REDUCED / SWEET SPOT / PRIMARY]

[If NO TRADE]: "Wait for next sanctioned window at HH:MM ET. No trades regardless of setup quality."
[If CAUTION]: "Trade only on textbook setups. Reduced size: 1-micro max."
[If TRADE / PRIMARY / SWEET SPOT]: "Window is sanctioned. Standard R1/R3 caps apply."
[If REDUCED]: "1-micro max, textbook setups only, pre-planned exits."
```

### R1 — Position Size Cap (output second)

State the cap for any trade taken right now:

```markdown
## R1 — Position Size Cap

Default cap: $4/point = 2 micros MNQ (provisional, May 7-11 tightening)
Range-day cap: $4/point = 2 micros (no further reduction yet — would need confirmation)
Today's cap given the archetype: [STATE THE CAP]

Anti-doubling rule: next trade's $/point cannot exceed prior losing trade's $/point.
```

### R3 — Daily Loss Limit (output third)

State today's effective cap:

```markdown
## R3 — Daily Loss Limit

Intraday cap: −$200 (default) OR −$80 (if Archetype 1)
Hit −$200 → kill the platform. No more trades today.
Honor at the trigger level — May 11 case study cost $430 from R3 violation.
```

### R6 — Off-Playbook (output fourth)

If the snapshot identifies a LIVE setup, the trade must come from that setup. State this:

```markdown
## R6 — Off-Playbook Check

Setups currently sanctioned: [list LIVE / IMMINENT setups by ID]
Any trade not matching one of these setup IDs is an R6 violation.
```

## Net Verdict

Close the discipline section with a single bottom-line verdict:

| Conditions | Output |
|---|---|
| R5 sanctions a trade window + a LIVE setup + R3 budget intact + R1 cap doable | **TRADE PERMITTED — [setup ID] with [size] cap [risk]** |
| R5 sanctions but no LIVE setup | **WAIT — no LIVE setup; watch [zone] for [setup]** |
| R5 blocks | **STAND ASIDE — R5 ([reason]). Next window at HH:MM ET.** |
| LIVE setup but R5 blocks | **TEMPTATION DETECTED — setup is LIVE but R5 blocks. STAND ASIDE. Snapshot for calibration only.** |
| R3 near violation | **DEFENSIVE MODE — within 1.5R of daily cap. Reduce to 1 micro or stop.** |

The verdict line is the single most important sentence in the snapshot.

## Why These Rules Exist

Each rule has a documented cost basis from prior performance data:

- **R1**: Sizing cliff at 3 micros in May 7-11 data (−$318 / 71% WR — losers bigger than winners)
- **R2**: Revenge trades −$108 in May 7-11 (30% WR), −$162.50 in May 11-12 (38% WR)
- **R3**: May 11 case study — breached R3 at 05:30 ET, cost $430 of the day's −$655
- **R4**: Sub-1-min trades −$999.50 in May 7-11 (33% of trades, ~100% of losses)
- **R5**: 04-06 ET (−$278), 08-10 ET (−$130 to −$678), 15-16 ET (−$374 historical)
- **R6**: May 11-12 — off-playbook trades lost $213, setup-tagged trades made $1,118

When the user violates these in good moments (e.g., R1 violation on a strong-trend day) and profits, **do NOT relax the rule.** One profitable violation doesn't override the cost data. The rule changes only after sustained sample-size evidence.

## R5 Sweet Spot Override

If current time is in the 06:00–07:00 ET window AND a LIVE T1 setup is forming, this is the **highest-probability moment in the dataset**. Tell the user.

## After-Hours Snapshot Note

For snapshots outside RTH (overnight, weekend), R5 will almost always block. State this and treat the snapshot as **calibration-only** (`outcome: "calibration-only"` in frontmatter).
