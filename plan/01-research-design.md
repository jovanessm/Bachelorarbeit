# Research design

## Research questions ✅
1. **RQ1, Vulnerability:** Under which baseline loads and slowdown durations does an unprotected service chain with client retries fail to recover after the slowdown ends?
2. **RQ2, Strategy selection:** Which single mitigation (retry budget, circuit breaker, deadline drop, load shedding) prevents or ends the failure under which conditions, and at what cost in normal operation?
3. **RQ3, Combination:** Under which conditions does combining a client-side and a server-side mitigation recover where neither does alone, and when is a single mitigation sufficient?

## Hypotheses ✅
| # | Hypothesis | RQ |
|---|---|---|
| H1 | Above a load-dependent slowdown duration, the unprotected chain ends in metastability-consistent non-recovery, while the no-retry control under the same trigger recovers. | RQ1 |
| H2 | After a large stale backlog has formed (TODO: define large stale backlog: e.g. queue ≥ 3 × μT at the end of the slowdown ❓), retry budget alone recovers more slowly than deadline drop alone. | RQ2 |
| H3 | Without a retry budget, load shedding and the circuit breaker do not restore recovery, because rejected requests are retried. | RQ2 |
| H4 | In normal operation, retry budget and deadline drop cost almost nothing, while load shedding rejects a measurable share of requests at the higher load level. | RQ2 |
| H5 | Retry budget + deadline drop recovers at high load with long slowdowns, where neither mechanism recovers alone, while at low load with short slowdowns a single mechanism is enough. | RQ3 |
| Criterion | Simulator and testbed agree on the outcome class in ≥ 80% of validation scenarios. | Methods |

## Definitions ✅
| Term | Definition |
|---|---|
| Capacity μ | Max requests/s the backend can finish (workers ÷ service time), measured in calibration |
| Load ρ | Fresh arrival rate as a fraction of μ |
| Goodput | Unique original requests answered successfully before their deadline, per 1 s interval |
| Recovered | Goodput ≥ 90% of pre-trigger level for 5 consecutive 1 s intervals |
| Observation window | 120 s after the slowdown ends |
| Time to recovery | End of slowdown to start of the 5 s recovered period |
| Retry amplification | Total attempts ÷ original requests |
| Wasted work | Share of server processing spent on already-expired requests |
| Recovery boundary | Longest slowdown in the grid after which the chain still recovers |
| Healthy-state cost | Goodput, p99 latency, rejection rate without trigger |
| Queue | Pending requests at gateway + both backends; trend = slope of linear fit over last 30 s |

Report results in **relative units** (ρ, slowdown duration as multiple of timeout D/T), so the guide transfers to other systems.

## Outcome classes ✅
| Outcome | Criterion |
|---|---|
| Recovered | Recovered within the 120 s window |
| Slow recovery | Not recovered in window, but queue trend negative, or recovers in extended run |
| Metastability-consistent non-recovery | Not recovered; attempts ≥ capacity; queue trend ≥ 0 and queue stays above μT; still not recovered in extended 10 min run |
| Non-recovery, not extended | Testbed only: not recovered, not selected for extension |
| Unexplained non-recovery | Not recovered, attempts below capacity: other cause, reported separately |

Metastability is defined by the sustaining loop, not by a time limit. Finite runs show consistency with metastability, not proof.

## Controls ✅
- **No-trigger control:** healthy-state cost.
- **No-retry control:** same system and trigger, retries off. Must recover; proves retries sustain the failure. Not a proposed fix.

## Mechanism verification ✅
unit tests per mechanism, per-second mechanism telemetry, analytical prediction made beforehand, positive control per mechanism, agreement of two independent implementations (simulator, testbed).
