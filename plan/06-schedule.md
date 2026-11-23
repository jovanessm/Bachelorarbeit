# Schedule

## Official dates (from `thesis/org/schedule.md`)
| Date | Event |
|---|---|
| 03.11.2026 | Exposé v1 (done) |
| 24.11.2026 | Exposé v2 |
| 29.11.2026 | Exposé v3 |
| 02.12.2026 | Einzelgespräch |
| 16.12.2026 | 1st meeting Bachelormodul |
| 12.01.2027 | 2nd meeting Bachelormodul |
| 31.01.2027 | Submit Leseprobe |
| 02.02.2027 | Leseprobe discussion |
| 04.03.2027 | **Thesis submission** |
| 19.03.2027 | Kolloquium |

❓ Official start / registration date and how the 8 weeks map onto these dates are not decided yet.

## 8-week plan 🟡 (+ weeks 9–10 buffer; writing runs alongside from week 1)
| Week | Focus | Exit deliverable |
|---|---|---|
| 0 (before start) | 1–2 day spike on the Mac: minimal testbed shows stuck baseline + recovering no-retry control 🟡 | Go for topic |
| 1 | Literature check, frozen definitions/parameters, simulator baseline + controls, minimal testbed | Research protocol, outline |
| 2 | Open-loop generator, testbed baseline, day-1 checks (pool limits, ulimit, stale work, hidden queue limits) | **Checkpoint:** both environments show stuck baseline + recovering no-retry control |
| 3 | All 4 mechanisms in simulator, unit tests, pilot runs; analytical model | Simulator ready |
| 4 | All 4 mechanisms in testbed, telemetry, calibration | Testbed ready |
| 5 | Main simulator grid + testbed runs (nights) | Raw dataset |
| 6 | Analysis, decision guide, guide check | Figures, tables, guide |
| 7 | Full draft | Draft |
| 8 | Review, essential reruns, references, reproduction package | Submission-ready |

**Cut order if late:** testbed pairs other than budget + deadline drop → testbed reps (5 → 3) → number of scenarios. Never cut: controls, mechanism verification, simulator vs. testbed check.

## Fallback (if week-2 checkpoint fails) ✅ drafted
Narrower study of post-overload recovery speed, stating clearly that metastability was not demonstrated.
- Title: *Evaluating Client-Side and Server-Side Mitigations for Retry-Amplified Overload Recovery: A Simulation and Testbed Study*
- RQs: (1) how load and slowdown duration affect time to recovery; (2) how mechanisms alone and in pairs affect recovery time, wasted work, goodput; (3) how well the simulator reproduces the testbed and which testbed properties explain differences.
- H6 becomes rank agreement (Spearman ρ ≥ 0.8), fixed before the runs.
