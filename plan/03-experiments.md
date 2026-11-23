# Experiments

## Configurations ✅
9 configurations: unprotected baseline, 4 single mechanisms, 4 client × server pairs (budget+deadline, budget+shedding, breaker+deadline, breaker+shedding). Same-side pairs are not tested. Plus 2 controls (no trigger, no retry).

## Grid and run counts (estimates)
| Part | Runs | Time |
|---|---|---|
| Simulator main grid: 11 × 5 loads (50–90%) × 5 durations × 10 seeds 🟡 | 2,750 | ~20–30 min parallel |
| Simulator extended 10 min runs | ~900 | ~20–30 min |
| Simulator guide check | ~30 | minutes |
| Testbed calibration | | 1–2 h |
| Testbed main: 11 × 3 scenarios (mild, boundary, severe) × 5 reps | 165 | ~9.5 h (~3.5 min/run) |
| Testbed extended runs | ~10 | ~2 h |
| Testbed CPU robustness check | ~15 | ~1 h |
| Testbed guide check | ~20 | ~1.2 h |

Total ≈ 15 h machine time, 2 to 3 nights. Plan one full rerun. If short on time: testbed reps 5 → 3. Do not add more dimensions (timeouts, R, trigger strength) → future work.

Role split: **simulator draws the map**, **testbed checks it** at selected points, especially near boundaries.

## Machine and protocol ✅
- Main testbed batch on one **dedicated Linux machine** (old laptop with Ubuntu, else cheap cloud VM). Develop and pilot on the Mac.
- All compared runs on the same machine; calibrate on that machine; report specs.
- Runs strictly sequential; **randomized order**; automatic flagging (host CPU, generator lag, idle latency) and rerun of flagged runs.

## Data reduction ✅
per request → per second → **per run summary** → **per cell** (config × load × duration: share recovered, median TTR, spread) → **decision table**. Raw data stays out of Git (archive at the end).

## Decision guide ✅
- Built from the per-cell results. Inputs: load level, expected trigger length, which side you control, accepted healthy-state cost.
- Mark uncertain zones where simulator and testbed disagree.
- **Validated** on 2 to 3 new scenarios not used to build it.
