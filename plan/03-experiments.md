# Experiments

## Configurations ✅
**Core ✅ (2026-11-27, Prof. feedback): 6 configurations**: unprotected baseline, retry budget, deadline drop, retry budget + deadline drop, plus 2 controls (no trigger, no retry).
**Phase 2 (only after go at end of week 4):** + circuit breaker, load shedding and their pairs (budget + shedding, breaker + deadline drop, breaker + shedding) = 5 configurations. Same-side pairs are not tested.

## Grid and run counts (estimates, core)
| Part | Runs | Time |
|---|---|---|
| Simulator main grid ✅: 6 configurations × 5 loads (50, 60, 70, 80, 90%) × 6 slowdown durations (1, 2, 5, 10, 20, 40 s) × 10 seeds, k = 2 | 1,800 | < 30 min parallel |
| Simulator extended 10 min runs (only runs not recovered within 120 s) | ~500 | ~15 min |
| Simulator guide check | ~20 | minutes |
| Positive controls (simulator + testbed, before main runs): 2 mechanisms × 3 reps, plus nominal vs. true S check (~10 seeds) | ~20 | minutes / ~30 min |
| Testbed calibration | | 1–2 h |
| Testbed main: 6 × 3 scenarios (mild, boundary, severe) × 5 reps | 90 | ~5.3 h (~3.5 min/run) |
| Testbed extended runs | ~6 | ~1 h |

Total core ≈ 8–9 h machine time, 1–2 nights. Plan one full rerun.

**Phase 2 (after go):** simulator same grid, 1,500 runs (< 30 min), plus shedding-limit sweep for H3 (L ∈ {0.5, 1, 2, 5}·μT, 2 scenarios × 10 seeds = 80 runs). Testbed only if week 6 leaves time: 5 × 3 scenarios × 3 reps = 45 runs, ~2.6 h.

**Only if time (after the guide is built):** testbed CPU robustness check (~18 runs + own calibration; otherwise a stated threat to validity), testbed guide check (~20 runs), optional 4th testbed scenario.

**Cut order:** "only if time" items → phase 2 testbed → phase 2 entirely → testbed reps 5 → 3 → number of scenarios. Never cut: controls, mechanism verification, simulator vs. testbed check. Do not add more dimensions (timeouts, R, trigger strength) → future work.

Role split: **simulator draws the map**, **testbed checks it** at selected points, especially near boundaries.

## Testbed scenarios ✅
The 3 testbed scenarios are taken from the **simulator's map of the unprotected baseline** (calibrated values), by a rule fixed in advance, then frozen before the main testbed runs:
| Scenario | Rule | Example (k = 2) | Needed for |
|---|---|---|---|
| A: mild | All baseline seeds recover, middle load | 60% load, 2 s | H5 (single mechanism enough), no false alarms |
| B: boundary | ~30–70% of baseline seeds stuck | 70% load, 5 s | Where the guide's recommendations change |
| C: severe | All baseline seeds stuck, N ≥ 3 × μT at end of slowdown | 80% load, 20 s | H2, H3, H5 |
All 6 core configurations run in each scenario (phase 2 configurations only if time). Optional 4th scenario near a single mechanism's boundary: candidate for the guide check.

## Positive controls ✅
One scenario per mechanism where it should clearly work; part of mechanism verification, not of the main runs (weeks 3–4, double as pilot runs):
| Mechanism | Scenario | Must happen |
|---|---|---|
| Retry budget | Moderate load, short slowdown | Amplification near 1 + ratio, recovers |
| Deadline drop | Large stale backlog | Expired/hopeless requests dropped, queue empties within seconds |
| Load shedding (phase 2) | No retries, short burst above 100% load | Queue at limit, accepted requests within timeout |
| Circuit breaker (phase 2) | Backend fails hard (errors) | Opens, fails fast, probe closes it later |

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
| The single mitigations (2 core, +2 in phase 2) | Outcome, time to recovery, retry amplification, wasted work (RQ2, H2, H3) |
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
