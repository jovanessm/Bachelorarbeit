# Prototype findings (feasibility simulator, not thesis code)

Simplified simulator in Claude's workspace: one backend (FIFO, exponential service times, capacity 100 req/s), open-loop Poisson client, T = 1 s, R = 3, no gateway, 3–5 seeds. Results are **pointers, not evidence for the thesis**. Last run 2026-11-23. Its single backend matches the thesis design (μ = 100); the thesis adds a gateway in front. The single-backend design is so far only supported by this simulation; the testbed check comes at the week-2 checkpoint.

## 1. Baseline and controls (80% load)
| Configuration | Result |
|---|---|
| Baseline, fixed 50 ms backoff | Stuck in 5/5; queue ~24,600; ~320 attempts/s |
| Baseline, exponential backoff + full jitter | Stuck in 5/5; queue ~24,300; ~317 attempts/s |
| No-retry control | Recovers in 21–36 s (k = 5, 10 s) / 10–32 s (k = 2, 10–20 s) |
| Retry budget (k = 5, 10 s) | Recovers in 34–71 s |
| Budget + deadline drop | Recovers in ~1 s |

Backoff does not prevent the stuck state (attempt rate unchanged), as the model predicts.

## 2. Deadline drop variant matters
| Variant (k = 5, 10 s, exp backoff + jitter) | Result |
|---|---|
| Drop only already-expired requests | Stuck in 5/5 (with old fixed backoff it had recovered in 14–54 s) |
| Drop if it can't finish in time | Recovers in 1–11 s |
→ Use the "can't finish in time" variant; good example for "correct implementation vs. effective".

## 3. Slowdown factor
- k = 5: baseline stuck after only 2 s at 60–80% load → map almost all "stuck", not useful.
- k = 2 (stuck seeds of 3): boundary at ~5–20 s (60%), ~2–5 s (70–90%); 50% occasionally stuck for long slowdowns. Model D* (10 / 5 / 3.3 / 2.5 s) is close but slightly optimistic. → k = 2 chosen.

## 4. Load shedding (80% load, k = 2, μT = 100)
| Limit L | 10 s slowdown | 20 s slowdown |
|---|---|---|
| 25 / 50 / 100 | Recovers in 1–9 s | Recovers in 1–17 s |
| 200 / 500 | Stuck (queue sits at L) | Stuck |
→ Recovers only if L ≲ μT (tipping point between μT and 2μT).

## 5. Circuit breaker (5 consecutive timeouts, 80% load, k = 2)
| Open time | 10 s slowdown | 20 s slowdown |
|---|---|---|
| 1 s | 1–22 s | 1–6 s |
| 5 s | 4–15 s | 1–16 s |
| 10 s | 2–12 s | 4–12 s |
| 30 s | 22–27 s | 12–17 s |
→ Recovers with all tested open times (backlog drains while open); long open time delays recovery. Old prediction "breaker alone does not help" was wrong → H3 rewritten.
The thesis design also has one backend, so an open breaker blocks all traffic (worst-case cost; with several backends the cost scales with the slowed backend's traffic share).
