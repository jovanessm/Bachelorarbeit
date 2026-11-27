# Experiments

## Configurations ✅
9 configurations: unprotected baseline, 4 single mechanisms, 4 client × server pairs (budget+deadline, budget+shedding, breaker+deadline, breaker+shedding). Same-side pairs are not tested. Plus 2 controls (no trigger, no retry).

## Grid and run counts (estimates)
| Part | Runs | Time |
|---|---|---|
| Simulator main grid ✅: 11 × 5 loads (50, 60, 70, 80, 90%) × 6 slowdown durations (1, 2, 5, 10, 20, 40 s) × 10 seeds, k = 2 | 3,300 | < 1 h parallel |
| Simulator extended 10 min runs | ~900 | ~20–30 min |
| Simulator guide check | ~30 | minutes |
| Testbed calibration | | 1–2 h |
| Testbed main: 11 × 3 scenarios (mild, boundary, severe) × 5 reps | 165 | ~9.5 h (~3.5 min/run) |
| Testbed extended runs | ~10 | ~2 h |
| Testbed CPU robustness check ✅: 2 scenarios (clearly stuck, near boundary) × 3 configurations (baseline, no-retry, budget + deadline drop) × 3 reps; own short calibration so capacity ≈ sleep version | ~18 | ~1 h + 30 min calibration |
| Positive controls ✅ (simulator + testbed, before main runs) | ~4 scenarios × 3 reps | minutes / ~1 h |
| Testbed guide check | ~20 | ~1.2 h |

Total ≈ 15 h machine time, 2 to 3 nights. Plan one full rerun. If short on time: testbed reps 5 → 3. Do not add more dimensions (timeouts, R, trigger strength) → future work.

Role split: **simulator draws the map**, **testbed checks it** at selected points, especially near boundaries.

## Testbed scenarios ✅
The 3 testbed scenarios are taken from the **simulator's map of the unprotected baseline** (calibrated values), by a rule fixed in advance, then frozen before the main testbed runs:
| Scenario | Rule | Example (k = 2) | Needed for |
|---|---|---|---|
| A: mild | All baseline seeds recover, middle load | 60% load, 2 s | H5 (single mechanism enough), no false alarms |
| B: boundary | ~30–70% of baseline seeds stuck | 70% load, 5 s | Where the guide's recommendations change |
| C: severe | All baseline seeds stuck, N ≥ 3 × μT at end of slowdown | 80% load, 20 s | H2, H3, H5 |
All 11 configurations run in each scenario. Optional 4th scenario near a single mechanism's boundary: candidate for the guide check.

## Positive controls ✅
One scenario per mechanism where it should clearly work; part of mechanism verification, not of the main runs (weeks 3–4, double as pilot runs):
| Mechanism | Scenario | Must happen |
|---|---|---|
| Retry budget | Moderate load, short slowdown | Amplification near 1 + ratio, recovers |
| Deadline drop | Large stale backlog | Expired/hopeless requests dropped, queue empties within seconds |
| Load shedding | No retries, short burst above 100% load | Queue at limit, accepted requests within timeout |
| Circuit breaker | Backend fails hard (errors) | Opens, fails fast, probe closes it later |

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

## Comparisons at the end ✅
**1. Mitigations against each other (main results, RQ1–RQ3).** Mostly from the simulator across the whole grid, confirmed by the testbed at the 3 scenarios. Feeds the decision guide.
| Compared | Metrics |
|---|---|
| Baseline vs. no-retry control | Stuck vs. recovered: retries cause the failure (RQ1, H1) |
| Baseline across load × slowdown | Recovery boundary (RQ1) |
| The 4 single mitigations | Outcome, time to recovery, retry amplification, wasted work (RQ2, H2, H3) |
| Mitigations in normal operation | Goodput, p99 request latency, rejection rate = healthy-state cost (H4) |
| Pairs vs. their single mitigations | Outcome, time to recovery (RQ3, H5) |

**2. Model, simulator and testbed against each other (validation).** Shows the answers can be trusted.
| Compared | Where | Metrics |
|---|---|---|
| Model vs. simulator | All grid cells | Outcome, boundary D*, backlog, attempt rate, time to recovery |
| Simulator vs. testbed | 3 testbed scenarios | Outcome class (≥ 80% validation criterion); time to recovery and other metrics as supporting evidence |
| All three | 3 testbed scenarios | Outcome, backlog, attempt rate, time to recovery |

**What each source produces**
| Quantity | Model | Simulator | Testbed |
|---|---|---|---|
| Stuck or recovers | ✅ | ✅ | ✅ |
| Recovery boundary (D*) | ✅ exact formula | ✅ all grid cells | ⚠️ only at 3 scenarios |
| Backlog at end of slowdown | ✅ | ✅ | ✅ |
| Attempt rate when stuck | ✅ | ✅ | ✅ |
| Time to recovery | ✅ rough estimate | ✅ | ✅ |
| Spread across runs | ❌ (no randomness) | ✅ seeds | ✅ repetitions |
| Goodput and queue over time | ❌ | ✅ | ✅ |
| p99 latency, rejection rate (healthy-state cost) | ❌ | ✅ | ✅ |
| Wasted work | ⚠️ rough | ✅ | ✅ |
| Mechanism telemetry | ❌ | ✅ | ✅ |
| Real overheads (CPU, generator lag, memory) | ❌ | ❌ | ✅ |

Only the core quantities overlap across all three. The model has no spread, time series, latency or telemetry; only the testbed has real overheads (CPU, generator lag, memory).
