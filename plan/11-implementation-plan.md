# Implementation plan (core only) 🟡

Step-by-step order for implementing the core (retry budget, deadline drop, their pair, baseline, no-retry control). Phase 2 and "only if time" items are not in here. Proposed 2026-11-27, not yet confirmed.

## Principles
- **Riskiest first.** The testbed baseline is the one thing the prototype has not shown. It comes before the simulator and before any mechanism.
- **One contract, two implementations.** Protocol, scenario schema and CSV formats are shared code (`common/`). Client, gateway, backend and mechanisms are written separately in simulator and testbed (mechanism verification, `01`).
- **Every step ends with a check** you can run, not just code that exists.
- **No mechanism before the baseline is stuck** in both environments (week-2 checkpoint, `06`).

## Code layout
```
experiment/
├── pyproject.toml, uv.lock
├── common/       # protocol, scenario schema, log schemas, CSV writers, seeding
├── scenarios/    # YAML files + grid generator
├── testbed/      # generator, gateway, backend, docker-compose.yml, Dockerfile
├── simulator/    # heapq engine + client/gateway/backend modules
├── runner/       # run_one, run_batch, calibrate.py, setup.sh
├── analysis/     # per-second → per-run → per-cell → guide; model.py; plots
├── tests/
└── data/         # gitignored
```

## Step 0: Repo setup (½ day) ✅ 2026-11-27
- [x] uv project in `experiment/`, Python 3.12, deps: pydantic, pyyaml, pandas, numpy, scipy, matplotlib, pytest (dev group).
- [x] Folder layout above, `.gitignore` for `data/`.
- [x] One dummy test passes with `uv run pytest`.

**Done when:** a fresh clone runs `uv sync && uv run pytest` without errors.

## Step 1: Shared contract (1 day)
- [ ] `common/scenario.py`: pydantic model. Fields: `run_id`, `seed`, `config` (baseline / budget / deadline_drop / budget+dd / no_retry), `rho`, `slowdown_s` (D), `k`, `T`, `R`, `backoff_ms` [100, 200, 400], `jitter` (full), `budget_b`, `budget_C`, `S_nominal_ms`, `workers`, `service_ms`, `error_rate` (0 or 0.01), `warmup_s`, `trigger_at_s`, `observe_s` (120), `grace_s` (5). Validates ranges (e.g. 1/k < ρ < 1 warning).
- [ ] `common/protocol.py`: request message (request_id, attempt, send_ts, deadline_ts) and response (status `ok` / `error` / `dropped` / `rejected_shed` / `rejected_breaker`). JSON lines over TCP.
- [ ] `common/logs.py`: column lists for client per-attempt, client per-second, gateway per-second, backend per-second, run metadata (fields exactly as in `02` Logging). One writer function per table.
- [ ] Load one hand-written YAML scenario from `scenarios/`.

**Done when:** a unit test round-trips a scenario YAML and writes/reads an empty CSV of each table.

## Step 2: Testbed generator alone (1–2 days) ⚠️ biggest risk
- [ ] Open-loop Poisson sender with asyncio: schedule from precomputed exponential gaps on `loop.time()`, never wait for responses.
- [ ] Dummy echo server that answers immediately.
- [ ] Per-second log: intended vs. actual send rate, generator lag (actual minus scheduled send time).
- [ ] A few persistent multiplexed connections (🟡, `02`): many requests in flight per connection, responses matched by request_id. `ulimit -n` and listen backlog generous anyway.

**Done when:** at 400 attempts/s for 60 s, actual rate is within ±2% of intended and p99 lag < 5 ms, on Mac and on the Fedora machine.

## Step 3: Testbed backend + gateway (2 days)
- [ ] Backend: `asyncio.Queue` (unbounded), `workers` tasks, each does `await asyncio.sleep(service_ms × factor)`. Stale work kept (no drop yet).
- [ ] Trigger endpoint (control port): set factor = k at a time, reset after D.
- [ ] Backend per-second sampler: queue length, N = queue + busy, arrivals, completed, completed after deadline, busy workers, time spent on expired work, trigger on/off.
- [ ] 1% random error responses when `error_rate` > 0.
- [ ] Gateway: forward, stop waiting at the attempt deadline (no timeout response; the client decides timeouts), discard and count late backend responses. Drop already-expired requests on arrival. Per-second counters (received, forwarded, dropped expired; split original / retry).
- [ ] `docker-compose.yml`: 3 services, `cpus`/`cpuset` per container, raised listen backlog and ulimits (`setup.sh`).

**Done when:** a 100 req/s ramp shows capacity ≈ 100 req/s, and N during the slowdown grows at about λ − μ/k.

## Step 4: Testbed client with retries (1–2 days)
- [ ] Per attempt: timeout T, retry on timeout / error / rejection, R = 3, backoff 100/200/400 ms with full jitter, fresh deadline per retry.
- [ ] Per-attempt rows in memory, written after the run (+ grace period).
- [ ] Client per-second log: attempts original / retry, retries scheduled, in flight.
- [ ] `config = no_retry` switches retries off.

**Done when:** a healthy run at 60% load has amplification ≈ 1.01 (1% errors) and no timeouts.

## Step 5: Minimal analysis (1 day)
- [ ] `analysis/per_second.py`: goodput per 1 s (unique originals with an `ok` before their attempt deadline, counted in the second of success).
- [ ] `analysis/per_run.py`: pre-trigger goodput, recovered rule (≥ 90% for 5 consecutive seconds within 120 s), time to recovery, amplification, N trend over last 30 s, forwarded attempts vs. μ → outcome class (`01`).
- [ ] One plot per run: goodput, attempts/s, N over time, trigger shaded.

**Done when:** classification gives the expected class on 3 hand-made synthetic runs (unit tests).

## Step 6: Testbed spike result = first half of the week-2 checkpoint
- [ ] Baseline at 80% load, D = 20 s, k = 2: stuck (metastability-consistent), 3 reps.
- [ ] No-retry control, same scenario: recovers, 3 reps. Compare drain time with the model (≈ 25 s).
- [ ] Run "day-1 checks": no hidden queue limits (listen backlog, connection pool, ulimit), stale work really processed, host CPU not saturated, generator lag fine.

**Done when:** both results hold. If not: debug for at most ~3 days, then decide on the fallback (`06`).

## Step 7: Simulator baseline (2–3 days)
- [ ] `simulator/engine.py`: `heapq` event loop, simulated clock, seeded RNG streams (arrivals, service, jitter, errors separate).
- [ ] Modules: client (same retry logic, written again), gateway (forward, expired drop, deadline timeout), backend (FIFO, c workers, fixed service time ×k during slowdown, stale work).
- [ ] Reads the same scenario YAML, writes the same CSV tables and metadata.
- [ ] Unit tests: M/D/c-style sanity (N small at 50% load), backlog growth during slowdown ≈ (λ − μ/k)·D.

**Done when:** the step-6 scenarios give the same outcome classes as the testbed, and the analysis code from step 5 runs unchanged on simulator output. → **Week-2 checkpoint passed.**

## Step 8: Analytical model script (½–1 day)
- [ ] `analysis/model.py`: for each cell compute B, D*, t_s, t_r, A_stuck, stuck/recovers, drain times (no retry, budget) from `04`.
- [ ] Writes `model_predictions.csv`. Commit it before main runs (prediction fixed beforehand).

**Done when:** values match the tables in `04` (unit test on ρ = 0.6–0.9).

## Step 9: Retry budget (1–2 days, simulator then testbed)
- [ ] Token bucket in the client: +b per original, −1 per retry, cap C = 10, starts full. Denied retry = request fails.
- [ ] Telemetry: retries denied, tokens per second.
- [ ] Unit tests: refill, cap, denial, long-run retry ratio ≤ b.
- [ ] Positive control: moderate load, short slowdown → amplification ≈ 1 + b, recovers (3 reps each environment).

## Step 10: Deadline drop (1–2 days, simulator then testbed)
- [ ] Backend checks when a worker takes a request: drop if `now + S_nominal ≥ deadline_ts`, respond `dropped`, cost ~0.
- [ ] Gateway keeps dropping already-expired only.
- [ ] Telemetry: dropped by deadline drop per second, wasted-work time.
- [ ] Unit tests: boundary cases (exactly at deadline, 1 ms either side), not applied in baseline.
- [ ] Positive control: large stale backlog → queue empties within seconds.
- [ ] Optional: nominal S vs. true current S, ~10 simulator seeds.
- [ ] Pair config (budget + dd) is just both flags on; one smoke run.

**Done when (steps 9–10):** all positive controls pass in both environments.

## Step 11: Calibration (1 day)
- [ ] `runner/calibrate.py`: no trigger, no retries, load ramp → μ, service-time spread, logging overhead (logging on vs. off), generator check, OS/queue limits → `calibration.json` (with machine + git commit).
- [ ] Scenario generator uses `rate = ρ × μ_measured`; simulator uses the same μ and S.

## Step 12: Runner + grid (2–3 days)
- [ ] `scenarios/generate.py`: simulator grid (5 configs × 5 loads × 6 durations × 10 seeds = 1,500), healthy-state (200), testbed scenarios A/B/C (picked later by rule).
- [ ] `runner/run_one.py`: start containers, warm-up, trigger, observe, collect CSVs, write metadata, tear down.
- [ ] `runner/run_batch.py`: random order, strictly sequential (testbed) / parallel (simulator), progress file to resume after a crash, auto-flagging (host CPU, generator lag, idle latency) and requeue of flagged runs.
- [ ] Extended runs: rerun non-recovering runs for 10 min (simulator all, testbed by priority rule in `09`).

**Done when:** a mini batch of 10 mixed testbed runs survives a deliberate kill + resume.

## Step 13: Full analysis pipeline (3–5 days, can start on pilot data)
- [ ] Per run → per cell (share recovered, median TTR with censoring, spread, wasted work, amplification).
- [ ] Healthy-state cost table (H4 thresholds).
- [ ] Hypothesis checks H1, H2, H4, H5 as scripts with pass/fail output.
- [ ] Model vs. simulator: boundary heatmap with D* line, agreement table, predicted vs. observed TTR scatter.
- [ ] Testbed scenario picker (rule from `03`), then freeze A/B/C.
- [ ] Simulator vs. testbed agreement (15 cells, A/C majority class, B share ±30 pp).
- [ ] Decision table → decision guide; guide check on 2–3 new simulator scenarios.
- [ ] Plots exported as PDF into `thesis/gfx/`.

## Step 14: Main runs (2 nights + 1 rerun)
- [ ] Simulator grid + healthy-state + extended (< 1 h).
- [ ] Pick and freeze testbed scenarios A/B/C from the simulator map.
- [ ] Testbed: 75 trigger + 40 healthy-state + ~6 extended runs on the Fedora machine.
- [ ] Archive raw data, keep summaries in Git.

## Step 15: Reproduction package (1 day)
- [ ] README with one-command setup, calibration, runs, analysis.
- [ ] Tag the commit used for the thesis results.

## Mapping to the schedule (`06`)
| Week | Steps |
|---|---|
| 1 | 0, 1, 2, 3 |
| 2 | 4, 5, 6, 7 → checkpoint |
| 3 | 8, 9, 10 in simulator, unit tests, positive controls |
| 4 | 9, 10 in testbed, 11, 12 → phase 2 go/no-go |
| 5 | 13 on pilot data, 14 |
| 6 | 13 finished, guide check |

Differs from `06` on purpose: testbed baseline before simulator baseline (risk first), so the simulator moves from week 1 to week 2.

## Open points for this plan ❓
- Confirm multiplexed persistent connections (🟡 in `02`).
