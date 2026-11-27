# Analytical model ✅ (own chapter, ~3–4 pages)

## Scope ✅ (2026-11-27)
One backend behind the gateway; it gets the slowdown. An open circuit breaker rejects requests (no failover). All rates are per backend. Extension to several backends: see the last section. Core mechanisms: retry budget, deadline drop; circuit breaker and load shedding are phase 2.

## Assumptions ✅ (all predictions are approximations under these)
| # | Assumption | Used by |
|---|---|---|
| A1 | Fluid model: average rates, no randomness (Poisson arrivals and jitter averaged out) | all |
| A2 | FIFO queue, fixed service time S (kS during the slowdown), c identical workers | N*, t_resp, drop rule |
| A3 | No retries during the slowdown (backlog built by fresh arrivals only) | B, D*, drain times |
| A4 | Backoff ignored (shifts timing, not the steady-state attempt rate) | A_stuck, stuck condition |
| A5 | Retry budget at steady state (initial tokens and bucket capacity ignored) | budget bound, t_budget |
| A6 | Healthy-state errors (1%) ignored | all |

The comparison with the simulator measures how much these assumptions matter. Known direction: A3 makes D* optimistic (t_r < D* at every load).

## Variables and formulas ✅

| Symbol | Meaning | Unit |
|---|---|---|
| c | Workers (4) | – |
| S | Service time of one request (nominal 40 ms) | s |
| μ | Capacity, μ = c/S (4 / 40 ms = 100) | req/s |
| ρ | Load as a fraction of μ | – |
| λ | Fresh (original) arrival rate | req/s |
| T | Client timeout per attempt | s |
| R | Max retries per request | – |
| k | Slowdown factor (service time becomes kS, capacity μ/k) | – |
| D | Slowdown duration | s |
| N | Requests in system at the backend (waiting + in service) | req |
| B | N at the end of the slowdown (backlog) | req |
| b | Retry budget ratio | – |
| C | Retry budget bucket capacity | tokens |
| L | Load shedding limit (backend admission on N; phase 2) | req |

Fresh arrival rate:
$$\lambda = \rho\,\mu$$

Response time of an arriving request (since c/μ = S):
$$t_{\text{resp}} \approx \frac{N - c}{\mu} + S = \frac{N}{\mu}$$

Threshold (requests in system), always with the capacity of the current phase:
$$N^{*} = \mu T \;(\text{normal: } 100), \qquad N^{*}_{\text{slow}} = \frac{\mu}{k}\,T \;(\text{slowdown: } 50)$$
Counting only waiting requests (Q = N − c) gives μT − c = 96 and μT/k − c = 46. The model uses N.

Backlog at the end of the slowdown:
$$B = \left(\lambda - \frac{\mu}{k}\right) D$$

Critical slowdown duration (≈ under A1–A3; an upper bound because of A3):
$$D^{*} = \frac{\mu T}{\lambda - \mu/k} = \frac{T}{\rho - 1/k}$$

From when retries during the slowdown add load (first timeouts at t_s, their retries arrive about T later):
$$t_r \approx t_s + T, \qquad t_s = \frac{\mu T/k}{\lambda - \mu/k} = \frac{T}{k\rho - 1}$$

Attempt rate when stuck (client attempts):
$$A_{\text{stuck}} = \lambda\,(1 + R)$$
Offered work to the backend = attempts **forwarded** by the gateway. Without breaker or shedding this equals A_stuck; with them it is lower.

Vulnerable zone:
$$\lambda < \mu < \lambda\,(1 + R)$$

Stuck condition (with the forwarded attempt rate):
$$B > \mu T \quad \text{and} \quad \lambda\,(1+R) > \mu$$

Drain time without retries:
$$t_{\text{no-retry}} = \frac{B - \mu T}{\mu - \lambda}$$

Retry budget (one token bucket in the generator; ≈ under A1, A5):
$$\lambda\,(1+b) < \mu \iff b < \frac{1}{\rho} - 1$$
Not a strict bound for every run. Initial tokens and bucket capacity only change the transient: a full bucket at the trigger allows a burst of up to C extra retries. Keep C small (C = 10 tokens ✅) so the burst stays below ~10% of μT.

Drain time with retry budget:
$$t_{\text{budget}} = \frac{B - \mu T}{\mu - \lambda\,(1 + b)}$$

Load shedding recovers if (phase 2; admission at the backend on N, so L bounds the actual outstanding work):
$$L \lesssim \mu T$$

Drain time while the circuit breaker is open (phase 2) (no requests reach the backend; they are rejected, no failover):
$$t_{\text{breaker}} = \frac{B - \mu T}{\mu}$$

Deadline drop rule ("can't finish in time"), checked by the backend when a worker takes the request:
$$\text{drop if} \quad t_{\text{now}} + S \ge \text{attempt deadline}, \qquad S = 40\text{ ms (nominal)}$$
Uses the service time of one request, not 1/μ (10 ms is only the time between completions across 4 workers). During the slowdown the true service time is 80 ms, so requests with 40–80 ms left are still processed and miss their deadline: a small extra amount of wasted work, stated as a limitation. Optional sanity check in the week-3 positive controls: nominal S vs. true current S, ~10 seeds each. The gateway only drops already-expired requests (it does not know the backend's queue).

## Retry loop
1. N > μT → every arriving request waits longer than T → all time out.
2. All timed-out requests are retried → attempts ≈ λ(1 + R).
3. The backend still processes stale work → served ≤ μ.
4. If the forwarded attempt rate λ(1 + R) > μ, N does not shrink → step 1 holds again.

Vulnerable zone: λ < μ < λ(1 + R). Induction on P(t): N(t) > μT shows the state sustains itself (for the model: average rates, FIFO, no external change). Bounded queues: invariant becomes "queue stays at limit, limit > μT".

## Which step each mechanism breaks
| Mechanism | Breaks |
|---|---|
| Retry budget | Step 2 (caps attempts at λ(1 + b)) |
| Deadline drop | Step 3 (stale work costs ~nothing) |
| Load shedding (phase 2) | Step 1: keeps in-flight requests ≤ L. Recovers only if L ≲ μT (accepted requests then finish in time); with L > μT the queue sits full at L and stays stuck ✅ |
| Circuit breaker (phase 2) | Step 1: while open, the gateway rejects all requests (no failover), so the stale backlog drains and rejected requests use up their retries quickly. Recovers, but all requests fail while open; long open time delays recovery ✅ (corrected 2026-11-23; earlier claim "loop intact" was wrong, see `10-prototype-findings.md`) |

## Simple quantitative predictions
- Threshold: N* = μT = 100 (prototype: 100; waiting-only 96).
- Critical slowdown duration (how long until the backlog passes the threshold; μ cancels, hardware-independent), upper bound, plus when retries during the slowdown start to matter, with k = 2 ✅, T = 1 s:

  | ρ | Retries start t_r | D* |
  |---|---|---|
  | 0.6 | 6 s | 10 s |
  | 0.7 | 3.5 s | 5 s |
  | 0.8 | 2.7 s | 3.3 s |
  | 0.9 | 2.25 s | 2.5 s |

  ρ ≤ 0.5 → never (trigger alone does not overload). t_r < D* at every load, so the real boundary lies somewhat below D*.
- Drain time without retries: backlog B = (λ − μ/k)·D; time until N < μT is (B − μT) / (μ − λ).
  Prototype check: B = 600, (600 − 100)/20 = **25 s** predicted vs. **24–33 s** simulated.
- Retry budget rule ✅: recovers only if b < 1/ρ − 1 (80% load → b < 25%; 90% → b < ~11%). Chosen b = 20% ✅ → recovers below ρ ≈ 0.83, fails at 90% (gives H5 its test cell); b = 10% would recover in the whole grid. Drain time (B − μT) / (μ − λ(1 + b)).
- Outputs of the model: stuck/recovers (binary) plus quantities: threshold, D*, backlog, attempt rate when stuck, drain/recovery time, parameter limits.
- Prototype comparison ✅: direction right everywhere checked; model is consistently slightly optimistic (tips a bit earlier, recovers a bit slower than predicted), likely because retries during the slowdown (from t_r on, before D* at every load) and randomness are ignored. Backoff is ignored on purpose (changes timing, not the steady-state attempt rate).
- Predictions are approximations under A1–A6, computed for every grid cell by a script and fixed before the main runs. Shown as: boundary heatmap with D* line, agreement table (model vs. observed outcome), predicted vs. observed time-to-recovery scatter.
- No full stochastic queueing theory (out of scope).