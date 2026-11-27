# System design

## Architecture ✅
```
load generator (client) ──► gateway ──► backend  (gets the slowdown trigger)
```
- **One backend ✅ (2026-11-27)**, one container configured by env vars. Simplified from two backends (A healthy, B slowed): with key routing and no failover, A never interacted with B, so it added complexity and testbed load without new results. Multi-backend effects (breaker cost for partial traffic, shared-budget dilution) are derived analytically in `04`. **No failover**: an open breaker rejects requests.
- Simulator models the same parts as modules. Both read the **same scenario files** and write the **same CSV format**.

## Components (11)
| # | Component | Role |
|---|---|---|
| 1 | Load generator | Open-loop Poisson arrivals, timeouts, retries, **retry budget**, per-attempt log |
| 2 | Gateway | Forwarding, **circuit breaker**, **load shedding**, deadline check (expired only) |
| 3 | Backend | FIFO queue (`asyncio.Queue`), N workers, **deadline drop**, trigger endpoint |
| 4 | Simulator | Own `heapq` event loop + client/gateway/backend modules ✅ |
| 5 | Scenario schema + generator | YAML + pydantic, generates grid |
| 6 | Runner | Runs scenarios in random order, triggers, collects, flags bad runs, progress file |
| 7 | calibrate.py | Measures capacity etc., writes `calibration.json` |
| 8 | Analysis | Summary → outcome classes → aggregation → plots → decision guide |
| 9 | Tests | pytest per mechanism + small end-to-end |
| 10 | Setup script | ulimit, backlog, CPU pinning, Docker |
| 11 | Shared protocol | Request id, attempt number, attempt deadline (attempt send time + T; no end-to-end deadline) |

Share protocol and data formats between simulator and testbed, but implement mechanisms separately in each (keeps them independent for verification) ✅.

## Key design choices
- **Service time ✅:** `asyncio.sleep` inside a fixed number of workers (capacity = workers ÷ service time, e.g. 4 ÷ 40 ms = 100 req/s). Plus 2 to 3 CPU-work runs as robustness check. (Unlike ResilienceBench, where injected delays use no server capacity.)
- **Load ✅:** Poisson arrivals, open-loop (generator never waits for responses). Log intended vs. actual send rate.
- **Retries ✅:** only the client retries. R = 3 (4 attempts total); retry on timeouts and on error/rejection responses; exponential backoff 100 / 200 / 400 ms with full jitter (random wait in [0, backoff]); T = 1 s per attempt, fresh deadline per retry (no end-to-end deadline; total request latency is reported as a secondary metric). Backoff is part of the realistic client baseline, not a fifth mitigation: it delays retries but does not reduce them, so the stuck state is still possible. Use this client from the spike and week-2 checkpoint on. Runner waits a ~5 s grace period at the end of each run.
- **Retry budget ✅:** one shared token bucket for the whole generator.
- **Stale work:** the baseline backend keeps processing requests whose client already gave up.
- **Trigger ✅:** slowdown factor k = 2: the backend's service time doubles (40 → 80 ms), so its capacity halves (100 → 50 req/s) for the slowdown duration.
- **Deadline drop ✅:** "drop if it can't finish in time": the backend drops a request when a worker takes it if `now + S ≥ attempt deadline`, with nominal S = 40 ms (service time of one request, not 1/μ; underestimates the 80 ms during the slowdown, stated as a limitation). The gateway only drops already-expired requests. Not only "drop if already expired". The expired-only variant stayed stuck in the prototype with the realistic client (see `10-prototype-findings.md`); optionally report it as a comparison.
- **Queues:** explicit app-level queues; all hidden limits (listen backlog, connections) must be above μT.
- **Bounded queue note:** a limit above μT stays stuck; a limit below μT acts as load shedding.

## Mechanisms ✅
| Mechanism | Side | Where |
|---|---|---|
| Retry budget | Client | Load generator |
| Circuit breaker | Client (caller of backend) | Gateway; rejects when open, no failover |
| Deadline drop | Server | Gateway and backend |
| Load shedding | Server | Gateway |

## Logging
General ✅: per-attempt rows only at the client, kept in memory and written after the run; servers only counters + queue length sampled once per second; no per-request print/logging/file writes; overhead measured once (target < 1 to 2%). Simulator writes the same files and fields.

Fields ✅:
- **Client, per attempt:** run_id, request_id, attempt (0 = first), send_ts, deadline_ts, end_ts, outcome (`ok` / `timeout` / `rejected_shed` / `rejected_breaker` / `error`), latency_ms.
- **Client, per second:** intended vs. actual send rate, attempts (original / retry), retries scheduled, retries denied by budget, budget tokens, requests in flight.
- **Gateway, per second:** received, forwarded, shed, breaker rejections, dropped as expired (each split original / retry by attempt number), breaker state (+ each state change with timestamp), in flight.
- **Backend, per second:** queue length, arrivals, completed, completed after deadline, dropped by deadline drop, busy workers, time spent on expired work, trigger on/off.
- **Run metadata:** scenario, configuration, seed, machine, calibration version, Git commit. **Host, per second:** CPU, memory, open file descriptors.

Metric sources: goodput and amplification and healthy-state cost from client rows; request latency from client rows (first send_ts per request_id); offered work from gateway forwarded counts (this, not client attempts, is the work offered to the backend); attempts/s from client per-second log; queue and trend from the backend (gateway in-flight separately); wasted work from the backend; mechanism telemetry from client (budget), gateway (breaker, shedding), backend (deadline drop); run flagging from generator lag and host metrics.

## Calibration ✅
Separate script on the same testbed, no trigger, no retries, load ramp. Measures capacity μ, service-time spread, logging overhead, generator check, queue/OS limits → `calibration.json`, used by scenario generator (`rate = ρ × μ`) and simulator. Rerun per machine and after changes affecting capacity.
