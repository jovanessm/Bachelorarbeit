1. Fix the load definition (critical). Your gateway distributes requests 50/50 between two backends, but the analytical model uses one backend's capacity. Define whether \(\mu\) and \(\rho\) refer to the affected backend or the entire system. Otherwise, your experiments may not create the intended overload.

2. Correct the deadline model. Your formula uses \(1/\mu\) as expected service time. With four workers and 40 ms per request, \(\mu=100\) requests/s, but individual service time is 40 ms, not 10 ms. Also clarify whether deadlines apply per attempt or across the entire original request.

3. Reduce optional experimental work. You now have 3,300 main simulation runs, extended runs, 165 main testbed runs, CPU robustness checks, an analytical model, and a decision guide. This is ambitious for eight weeks. Prioritize the core experiments and remove optional validation breadth before reducing repetitions.

4. Protect your writing schedule. Aim to have the background, related work, analytical model, and methodology substantially drafted before week 5. Writing an entire 42–52-page thesis during weeks 7–8 would be risky.

5. Resolve remaining decisions early. Finalize the official thesis start date, retry-budget ratio, circuit-breaker parameters, and testbed hardware before the main implementation begins.

## Status
| # | Status | Where |
|---|---|---|
| 1 | ✅ 2026-11-27 | Resolved by simplifying to one backend: μ = its capacity, ρ = λ/μ. `04` scope + multi-backend extension (analytical); `01` definitions (N, offered work); `02` architecture, no failover, logging |
| 2 | ✅ 2026-11-27 | `04` phase-dependent threshold N* = μT, D* as upper bound + t_r, drop rule with S; `01` goodput + request latency; `02` deadline drop, protocol |
| 3 | ✅ 2026-11-27 | Core cut to 2 mechanisms (Prof.); optional items demoted to "only if time"; new cut order in `03`, `06` |
| 4 | open | |
| 5 | 🟡 partly | Done: b = 20%, C = 10; breaker/shedding parameters fixed at phase 2 go. Open: start date, testbed hardware |

## Prof. feedback (2026-11-27)
| Point | Answer | Where |
|---|---|---|
| Load shedding must control actual outstanding work, not the gateway's local queue | Backend admission on N (waiting + in service); phase 2 | `02`, `04` |
| Model predictions as approximations under explicit assumptions | Assumptions A1–A6, each formula tied to them; D* an upper bound | `04` |
| Reduce to 2 mechanisms, 4 if time | Core: retry budget + deadline drop (6 configs); breaker + shedding = phase 2 with go/no-go at end of week 4 | `01`, `03`, `06` |
| Fix mechanism parameters before main experiments | Core frozen by end of week 1; phase 2 at the go decision | `06`, `09` |

## Review (2026-11-27)
| Point | Answer |
|---|---|
| `03` called D* exact | Now "approximate (A1–A6, upper bound)" |
| `04` referenced a missing multi-backend extension | Section dropped on purpose; dangling references removed (`02`, `04`, `10`) |
| `09` outdated | Split into open decisions and decided items; estimates updated |
| Healthy-state runs per mitigation configuration | Added: separate no-trigger runs for each configuration (sim 4 × 5 loads × 10 seeds; testbed 4 × 2 loads × 5 reps) |
| Single-backend design unverified, prototype is simulation only | Stated in `02`, `06`, `10`; week-2 checkpoint is the first real check |
| H5 contradicted the prototype (deadline drop alone recovers) | Rewritten: pair faster + less wasted work; budget alone fails at 90% || Budget inequality is sufficient, not necessary; 90% failure not guaranteed | `04` and H5: "predicted to fail, tested not assumed" |
| RQ3 still reflected old H5 | RQ3 now covers recovery, time to recovery, wasted work |
| Response time needs minimum S; D* applicable region | `04`: t_resp ≈ max(S, N/μ); D* only for 1/k < ρ < 1 |
| Quantify H2, H4, H5; define 80% criterion | `01`: thresholds 🟡, criterion on 15 cells, majority class, ties = disagreement |

