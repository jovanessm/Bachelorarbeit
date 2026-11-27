# Research design

## Research questions ✅
1. **RQ1, Vulnerability:** Under which baseline loads and slowdown durations does an unprotected service chain with client retries fail to recover after the slowdown ends?
2. **RQ2, Strategy selection:** Which single mitigation (core: retry budget, deadline drop; phase 2 if time: circuit breaker, load shedding) prevents or ends the failure under which conditions, and at what cost in normal operation?
3. **RQ3, Combination:** Under which conditions does combining a client-side and a server-side mitigation improve on either mitigation alone (whether it recovers, time to recovery, wasted work), and when is a single mitigation sufficient?

## Hypotheses ✅
| # | Hypothesis | RQ |
|---|---|---|
| H1 | Above a load-dependent slowdown duration, the unprotected chain ends in metastability-consistent non-recovery, while the no-retry control under the same trigger recovers. | RQ1 |
| H2 | After a large stale backlog has formed (N ≥ 3 × μT at the end of the slowdown 🟡), retry budget alone recovers more slowly than deadline drop alone: median time to recovery of the budget ≥ 2 × that of deadline drop 🟡 (non-recovery counts as slower), in every such simulator cell and in testbed scenario C. | RQ2 |
| H3 (phase 2 only) | Load shedding restores recovery only if its queue limit is at most about μT; with a higher limit the system stays stuck. The circuit breaker restores recovery, but fails all requests to the slowed backend while open, so its time to recovery grows with the open time. (Rewritten 2026-11-23 after prototype, see `10-prototype-findings.md`.) | RQ2 |
| H4 | In normal operation (healthy-state runs, 1% random errors), retry budget and deadline drop cost almost nothing at every tested load: goodput ≥ 98% of the baseline's, p99 request latency ≤ 1.1 × the baseline's, request failure rate at most +0.5 percentage points 🟡. Phase 2 adds: load shedding rejects ≥ 1% 🟡 of requests at 90% load; circuit breaker false trips. | RQ2 |
| H5 | In high-load, long-slowdown cells (ρ ≥ 0.8 and D ≥ 10 s 🟡; testbed scenario C), retry budget + deadline drop recovers in all seeds with less wasted work and fewer attempts than either mechanism alone; its median time to recovery is never longer than that of the better single mechanism, and ≤ 0.5 × that of deadline drop alone in cells where deadline drop alone takes > 5 s 🟡 (avoids comparing near-instant recoveries). The retry budget alone is predicted to fail at 90% load (b = 20% > 1/ρ − 1, fluid model; near the boundary, so tested, not assumed); deadline drop alone recovers but more slowly. In low-load, short-slowdown cells (ρ ≤ 0.6 and D ≤ 2 s 🟡; scenario A), both single mechanisms recover in all seeds and the pair's median time to recovery is within 1 s 🟡 of the better one. (Rewritten 2026-11-27: in the prototype deadline drop alone already recovered, so "neither recovers alone" would fail in every cell.) | RQ3 |
| Criterion | Simulator and testbed agree on the outcome class in ≥ 80% of validation cells 🟡. Cell = testbed scenario × configuration with a trigger (core: 3 scenarios × 5 = 15 cells). Scenarios A and C: class per cell = majority over the testbed reps, and over the simulator seeds at the same calibrated parameters, using 3 classes: recovered, slow recovery, non-recovery (metastability-consistent and not-extended merged); ties count as disagreement. Scenario B (boundary, chosen at 30–70% stuck, so its majority is close to a coin flip): compare the share of non-recovering runs instead; a cell agrees if simulator and testbed shares differ by ≤ 30 percentage points 🟡. Cells with unexplained non-recovery are excluded and reported. Agreement = matching cells ÷ cells (core: ≥ 12 of 15). | Methods |

## Definitions ✅
| Term | Definition |
|---|---|
| Capacity μ | Max requests/s the backend can finish (c workers ÷ service time S, 4 ÷ 40 ms = 100), measured in calibration |
| Load ρ | Fresh arrival rate as a fraction of μ (λ = ρμ) |
| Goodput | Unique original requests that succeed: at least one attempt returned ok before that attempt's deadline (attempt send time + T). Counted in the 1 s interval of success. |
| Recovered | Goodput ≥ 90% of pre-trigger level for 5 consecutive 1 s intervals |
| Observation window | 120 s after the slowdown ends |
| Time to recovery | End of slowdown to start of the 5 s recovered period. Runs that do not recover count as censored (> 120 s) in medians and comparisons |
| Retry amplification | Total attempts ÷ original requests |
| Request latency | First send of the original request to its successful response, across retries (max ≈ 4.7 s). Secondary metric, p50/p99. Not end-to-end deadline compliance |
| Request failure rate | Share of original requests that fail after all retries |
| Offered work | Attempts forwarded to the backend by the gateway per second (client attempts minus breaker rejections and gateway drops; requests shed at the backend count as offered but cost almost nothing) |
| Wasted work | Share of server processing spent on already-expired requests |
| Recovery boundary | Longest slowdown in the grid after which the chain still recovers |
| Healthy-state cost | Goodput, p99 request latency, rejection rate without trigger |
| Queue N | Requests in system at the backend (waiting + in service); waiting queue = N − busy workers; gateway in-flight logged separately; trend = slope of linear fit of N over last 30 s |

Report results in **relative units** (ρ, slowdown duration as multiple of timeout D/T), so the guide transfers to other systems.

## Outcome classes ✅
| Outcome | Criterion |
|---|---|
| Recovered | Recovered within the 120 s window |
| Slow recovery | Not recovered in window, but queue trend negative, or recovers in extended run |
| Metastability-consistent non-recovery | Not recovered; attempts forwarded to the backend ≥ μ; N trend ≥ 0 and N stays above μT; still not recovered in extended 10 min run |
| Non-recovery, not extended | Testbed only: not recovered, not selected for extension |
| Unexplained non-recovery | Not recovered, attempts forwarded to the backend below capacity: other cause, reported separately |

Metastability is defined by the sustaining loop, not by a time limit. Finite runs show consistency with metastability, not proof.

## Controls ✅
- **Healthy-state runs (no trigger):** baseline and every mitigation configuration separately, with 1% random errors; measure healthy-state cost (H4).
- **No-retry control:** same system and trigger, retries off. Must recover; proves retries sustain the failure. Not a proposed fix.

## Mechanism verification ✅
unit tests per mechanism, per-second mechanism telemetry, analytical prediction made beforehand, positive control per mechanism, agreement of two independent implementations (simulator, testbed).
