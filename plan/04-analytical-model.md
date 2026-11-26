# Analytical model ✅ (own chapter, ~3–4 pages)

Notation: μ capacity (req/s), λ = ρμ (original req/s), R max retries, T client timeout, k slowdown factor, Q queue length.

μT: req can be finished within one timeout window

## Variables and formulas ✅

| Symbol | Meaning | Unit |
|---|---|---|
| μ | Capacity of the backend | req/s |
| ρ | Load as a fraction of capacity | – |
| λ | Fresh (original) arrival rate | req/s |
| T | Client timeout | s |
| R | Max retries per request | – |
| k | Slowdown factor (capacity becomes μ/k) | – |
| D | Slowdown duration | s |
| Q | Queue length | req |
| B | Backlog (queue length) at the end of the slowdown | req |
| b | Retry budget ratio | – |
| L | Load shedding queue limit | req |

Fresh arrival rate:
$$\lambda = \rho\,\mu$$

Threshold (queue length):
$$Q^{*} = \mu T$$

Backlog at the end of the slowdown:
$$B = \left(\lambda - \frac{\mu}{k}\right) D$$

Critical slowdown duration:
$$D^{*} = \frac{\mu T}{\lambda - \mu/k} = \frac{T}{\rho - 1/k}$$

Attempt rate when stuck:
$$A_{\text{stuck}} = \lambda\,(1 + R)$$

Vulnerable zone:
$$\lambda < \mu < \lambda\,(1 + R)$$

Stuck condition:
$$B > \mu T \quad \text{and} \quad \lambda\,(1+R) > \mu$$

Drain time without retries:
$$t_{\text{no-retry}} = \frac{B - \mu T}{\mu - \lambda}$$

Retry budget recovers if:
$$\lambda\,(1+b) < \mu \iff b < \frac{1}{\rho} - 1$$

Drain time with retry budget:
$$t_{\text{budget}} = \frac{B - \mu T}{\mu - \lambda\,(1+b)}$$

Load shedding recovers if:
$$L \lesssim \mu T$$

Drain time while the circuit breaker is open (no new arrivals):
$$t_{\text{breaker}} = \frac{B - \mu T}{\mu}$$

Deadline drop rule ("can't finish in time"):
$$\text{drop if} \quad t_{\text{now}} + \frac{1}{\mu} \ge \text{deadline}$$

## Retry loop
1. Q > μT → every request waits longer than T → all time out.
2. All timed-out requests are retried → attempts ≈ λ(1 + R).
3. Server still processes stale work → served ≤ μ.
4. If λ(1 + R) > μ, Q does not shrink → step 1 holds again.

Vulnerable zone: λ < μ < λ(1 + R). Induction on P(t): Q(t) > μT shows the state sustains itself (for the model: average rates, FIFO, no external change). Bounded queues: invariant becomes "queue stays at limit, limit > μT".

## Which step each mechanism breaks
| Mechanism | Breaks |
|---|---|
| Retry budget | Step 2 (caps attempts at λ(1 + b)) |
| Deadline drop | Step 3 (stale work costs ~nothing) |
| Load shedding | Step 1: keeps Q ≤ limit L. Recovers only if L ≲ μT (accepted requests then finish in time); with L > μT the queue sits full at L and stays stuck ✅ |
| Circuit breaker | Step 1: while open, no new requests reach the backend, so the stale backlog drains and rejected requests use up their retries quickly. Recovers, but all requests to that backend fail while open; long open time delays recovery ✅ (corrected 2026-11-23; earlier claim "loop intact" was wrong, see `10-prototype-findings.md`) |

## Simple quantitative predictions
- Threshold: Q* = μT (prototype: 100).
- Critical slowdown duration (How long until it passes threshold) (μ cancels, hardware-independent):
  `D* = T / (ρ − 1/k)` → with k = 2 ✅, T = 1 s: ρ = 0.6 → 10 s, 0.7 → 5 s, 0.8 → 3.3 s, 0.9 → 2.5 s; ρ ≤ 0.5 → never (trigger alone does not overload).
- Drain time without retries: backlog B = (λ − μ/k)·D; time until Q < μT is (B − μT) / (μ − λ).
  Prototype check: B = 600, (600 − 100)/20 = **25 s** predicted vs. **24–33 s** simulated.
- Retry budget rule ✅: recovers only if λ(1 + b) < μ, i.e. budget ratio b < 1/ρ − 1 (80% load → b < 25%; 90% → b < ~11%). Drain time (B − μT) / (μ − λ(1 + b)).
- Outputs of the model: stuck/recovers (binary) plus quantities: threshold, D*, backlog, attempt rate when stuck, drain/recovery time, parameter limits.
- Prototype comparison ✅: direction right everywhere checked; model is consistently slightly optimistic (tips a bit earlier, recovers a bit slower than predicted), likely because retries during the slowdown and randomness are ignored. Backoff is ignored on purpose (changes timing, not the steady-state attempt rate).
- Predictions are computed for every grid cell by a script and fixed before the main runs. Shown as: boundary heatmap with D* line, agreement table (model vs. observed outcome), predicted vs. observed time-to-recovery scatter.
- No full stochastic queueing theory (out of scope).
