# Open items

## Decisions ❓
- Map the 8-week plan onto official dates (start/registration date).
- ✅ Retry budget: b = 20%, C = 10 tokens (starts full).
- Phase 2 only (fix at the go decision, end of week 4): breaker threshold and open time; shedding limit L (+ sweep for H3).
- Workers and service time of the backend (e.g. 4 × 40 ms).
- Testbed transport: plain asyncio TCP vs. aiohttp.
- Threshold for "large backlog" in H2 (proposal: queue ≥ 3 × μT at end of slowdown).
- ✅ Add 1% random errors to the healthy (no-trigger) scenario, so the costs of retry budget and circuit breaker become visible.
- ✅ Extend H4 with circuit breaker false trips, and H5 with "pairs with the circuit breaker recover no better than their server-side mechanism alone".
- Exact simulator grid values (loads, durations).
- ✅ Selection rule for extended testbed runs, fixed before the main runs: at most one repetition per cell (configuration × scenario), e.g. the first non-recovering one or one picked at random; priority if time is short: baseline → cells near the recovery boundary → cells where the simulator disagrees. Other non-recovering repetitions are labelled "non-recovery, not extended". Estimate ~10–15 runs, 2–2.5 h (update `03-experiments.md` once decided).
- ✅ Timeouts: one client timeout T for all runs; each retry gets a fresh deadline (attempt time + T); the gateway uses the remaining deadline as its wait limit for the backend, so the circuit breaker counts slow calls as failures.

## To-dos
- [ ] Exposé v2 due **24.11.2026**: update to new framing, answer Prof. Hahn's 3 questions (mechanism verification, data reduction, ResilienceBench), corrected references.
- [ ] Exposé v3 due **29.11.2026**: one sentence on the simplification to one backend (reason: no interaction without failover; multi-backend effects derived analytically).
- [ ] Read `thesis/org/empfehlungen_zu_abschlussarbeiten.pdf` and `anleitung_expose.pdf` (page count, required structure).
- [ ] Confirm with Alte Leipziger that a company-independent topic is fine.
- [ ] 1–2 day spike on the Mac before registering.
- [ ] Check old laptop (CPU, cores, RAM, disk; Ubuntu live USB; timer test).
- [ ] Verify remaining references (`08-literature.md`).
- [ ] Optional: check ResilienceBench-Operator.

## Prof. Hahn's feedback (2026-11-22) and planned answers
| Point | Answer | Where |
|---|---|---|
| Correct implementation vs. mechanism really ineffective? | Mechanism verification (tests, telemetry, prediction, positive control, two implementations) | `01-research-design.md` |
| Reduce the mass of data | Aggregation levels up to a decision table | `03-experiments.md` |
| Source 3 already has a testbed | Checked: different question; reuse declarative idea | `05-tooling-and-repo.md` |
| Turn the argument around | Decision guide framing, new title and RQs | `00-overview.md` |
