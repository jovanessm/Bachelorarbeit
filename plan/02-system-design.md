# System design

## Architecture ✅
```
load generator (client) ──► gateway ──► backend A  (healthy)
                                   └──► backend B  (gets the slowdown trigger)
```
- Backends A and B: **same code and image, two containers**, configured by env vars. Gateway splits load by key (e.g. 50/50).
- Simulator models the same parts as modules. Both read the **same scenario files** and write the **same CSV format**.

## Components (11)
| # | Component | Role |
|---|---|---|
| 1 | Load generator | Open-loop Poisson arrivals, timeouts, retries, **retry budget**, per-attempt log |
| 2 | Gateway | Routing, **circuit breaker** (per backend), **load shedding**, deadline check |
| 3 | Backend (×2) | FIFO queue (`asyncio.Queue`), N workers, **deadline drop**; B has trigger endpoint |
| 4 | Simulator | Own `heapq` event loop + client/gateway/backend modules ✅ |
| 5 | Scenario schema + generator | YAML + pydantic, generates grid |
| 6 | Runner | Runs scenarios in random order, triggers, collects, flags bad runs, progress file |
| 7 | calibrate.py | Measures capacity etc., writes `calibration.json` |
| 8 | Analysis | Summary → outcome classes → aggregation → plots → decision guide |
| 9 | Tests | pytest per mechanism + small end-to-end |
| 10 | Setup script | ulimit, backlog, CPU pinning, Docker |
| 11 | Shared protocol | Request id, attempt number, end-to-end deadline |

Share protocol and data formats between simulator and testbed, but implement mechanisms separately in each (keeps them independent for verification) 🟡.

## Key design choices
- **Service time ✅:** `asyncio.sleep` inside a fixed number of workers (capacity = workers ÷ service time, e.g. 4 ÷ 40 ms = 100 req/s). Plus 2 to 3 CPU-work runs as robustness check. (Unlike ResilienceBench, where injected delays use no server capacity.)
- **Load ✅:** Poisson arrivals, open-loop (generator never waits for responses). Log intended vs. actual send rate.
- **Retries ✅:** only the client retries. R = 3 (4 attempts total); retry on timeouts and on error/rejection responses; exponential backoff 100 / 200 / 400 ms with full jitter (random wait in [0, backoff]); T = 1 s per attempt, fresh deadline per retry. Backoff is part of the realistic client baseline, not a fifth mitigation: it delays retries but does not reduce them, so the stuck state is still possible. Use this client from the spike and week-2 checkpoint on. Runner waits a ~5 s grace period at the end of each run.
- **Retry budget ✅:** one shared token bucket for the whole generator.
- **Stale work:** baseline backends keep processing requests whose client already gave up.
- **Queues:** explicit app-level queues; all hidden limits (listen backlog, connections) must be above μT.
- **Bounded queue note:** a limit above μT stays stuck; a limit below μT acts as load shedding.

## Mechanisms ✅
| Mechanism | Side | Where |
|---|---|---|
| Retry budget | Client | Load generator |
| Circuit breaker | Client (caller of backend) | Gateway, per backend |
| Deadline drop | Server | Gateway and backend |
| Load shedding | Server | Gateway |

## Logging ✅
- Client: one row per attempt, kept in memory, written after the run.
- Servers: only counters + queue length, sampled once per second.
- Mechanism telemetry per second: tokens, retries denied, breaker state changes, dropped, shed.
- No per-request print/logging/file writes. Measure overhead once (target < 1 to 2%).

## Calibration ✅
Separate script on the same testbed, no trigger, no retries, load ramp. Measures capacity μ, service-time spread, logging overhead, generator check, queue/OS limits → `calibration.json`, used by scenario generator (`rate = ρ × μ`) and simulator. Rerun per machine and after changes affecting capacity.
