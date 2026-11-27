# Open items

## Decisions ❓
- Map the 8-week plan onto official dates (start/registration date).
- Workers and service time of the backend (proposal 4 × 40 ms, already used throughout the plan).
- Testbed transport: plain asyncio TCP (toolstack) vs. aiohttp. Proposal 🟡: plain TCP, JSON lines, a few persistent multiplexed connections per hop (see `02`).
- Thresholds in H2, H4, H5 and the agreement criterion (🟡 proposals in `01`), including "large backlog" N ≥ 3 × μT. Fix before the main runs.
- Loads for testbed healthy-state runs (proposal 60% and 90%).
- Phase 2 only (fix at the go decision, end of week 4): breaker threshold and open time; shedding limit L (+ sweep for H3).

## Decided ✅ (details in `decisions.md` and the linked files)
- Testbed machine: old laptop with Fedora (`03`).
- Timeouts are decided by the client only; the gateway stops waiting at the attempt deadline and sends no timeout response (`02`).
- Core: retry budget + deadline drop; circuit breaker and load shedding = phase 2 (`03`, `06`).
- Retry budget: b = 20%, C = 10 tokens, starts full (`02`).
- Healthy-state runs per configuration, no trigger, 1% random errors, so the cost of the retry budget (and in phase 2 of the breaker) becomes visible (`03`).
- Simulator grid: 5 loads (50–90%) × 6 slowdown durations (1–40 s), k = 2, 10 seeds (`03`).
- Extended testbed runs: at most one repetition per cell (configuration × scenario), the first non-recovering one or one picked at random; priority if time is short: baseline → cells near the recovery boundary → cells where the simulator disagrees. Others labelled "non-recovery, not extended". Core estimate ~6 runs, ~1 h (`03`).
- Timeouts: one client timeout T; fresh deadline per retry (attempt send time + T); the gateway's wait limit is the remaining attempt deadline (in phase 2 the breaker counts slow calls as failures).
- Phase 2 hypotheses: H4 adds breaker false trips; H5 adds "pairs with the breaker recover no better than their server-side mechanism alone".

## To-dos
- [x] Exposé v2 due **24.11.2026**: update to new framing, answer Prof. Hahn's 3 questions (mechanism verification, data reduction, ResilienceBench), corrected references.
- [ ] Exposé v3 due **29.11.2026**: one sentence on the simplification to one backend (reason: no interaction without failover; multi-backend effects → discussion / future work).
- [ ] Read `thesis/org/empfehlungen_zu_abschlussarbeiten.pdf` and `anleitung_expose.pdf` (page count, required structure).
- [ ] Confirm with Alte Leipziger that a company-independent topic is fine.
- [ ] 1–2 day spike on the Mac before registering (also the first check of the single-backend design outside the prototype).
- [ ] Check old laptop (CPU, cores, RAM, disk, timer test). Fedora installed ✅.
- [ ] Verify remaining references (`08-literature.md`).
- [ ] Optional: check ResilienceBench-Operator.

## Prof. Hahn's feedback (2026-11-22) and planned answers
| Point | Answer | Where |
|---|---|---|
| Correct implementation vs. mechanism really ineffective? | Mechanism verification (tests, telemetry, prediction, positive control, two implementations) | `01-research-design.md` |
| Reduce the mass of data | Aggregation levels up to a decision table | `03-experiments.md` |
| Source 3 already has a testbed | Checked: different question; reuse declarative idea | `05-tooling-and-repo.md` |
| Turn the argument around | Decision guide framing, new title and RQs | `00-overview.md` |
