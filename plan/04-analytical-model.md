# Analytical model ✅ (own chapter, ~3–4 pages)

Notation: μ capacity (req/s), λ = ρμ (original req/s), R max retries, T client timeout, k slowdown factor, Q queue length.

μT: req can be finished within one timeout window

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
| Load shedding | Keeps Q below limit (helps only if rejections are not retried away) |
| Circuit breaker | Rejects calls, but rejected calls are retried → loop intact (H4) |

## Simple quantitative predictions
- Threshold: Q* = μT (prototype: 100).
- Critical slowdown duration (How long until it passes threshold) (μ cancels, hardware-independent):
  `D* = T / (ρ − 1/k)` → ρ = 0.8, k = 5, T = 1 s gives ≈ 1.7 s.
- Drain time without retries: backlog B = (λ − μ/k)·D; time until Q < μT is (B − μT) / (μ − λ).
  Prototype check: B = 600, (600 − 100)/20 = **25 s** predicted vs. **24–33 s** simulated.
- No full stochastic queueing theory (out of scope).
