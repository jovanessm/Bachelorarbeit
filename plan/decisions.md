# Decisions log

| Date | Decision |
|---|---|
| ≤ 2026-11-09 | Topic: retry-driven metastable failures, simulator + Docker testbed |
| ≤ 2026-11-09 | 4 mechanisms (2 client, 2 server), all in simulator and testbed |
| ≤ 2026-11-09 | 8 weeks planned + 2 weeks buffer |
| 2026-11-09 | Five-outcome definition with extended runs; H1 uses "metastability-consistent non-recovery" |
| 2026-11-23 | Reframe as decision guide; title "When to Use Which Mitigation? ..." |
| 2026-11-23 | Simulator validity as validation step in methods (3 RQs) |
| 2026-11-23 | Testbed in Python asyncio |
| 2026-11-23 | Service time: sleep inside workers + small CPU-work robustness check |
| 2026-11-23 | Assumed (not objected): analytical model chapter, finer simulator grid, guide check, definition tweak, shared retry budget, own heapq engine |
| 2026-11-23 | 9 configurations (4 client × server pairs only) |
| 2026-11-23 | Main testbed runs on a dedicated Linux machine |
| 2026-11-23 | Monorepo with `plan/`, `experiment/`, `thesis/` |
| 2026-11-23 | Hypotheses trimmed to H1–H5 + simulator/testbed agreement criterion |
| 2026-11-23 | Client retries: R = 3, retry on timeouts and errors, exponential backoff 100/200/400 ms with full jitter, T = 1 s per attempt |
| 2026-11-23 | Simulator grid: 5 loads (50–90%) × 6 slowdown durations (1–40 s), slowdown factor k = 2, 10 seeds (3,300 runs) |
| 2026-11-27 | Load and model defined per backend B: μ = one backend's capacity, ρ = load on B, generator total rate = ρμ ÷ s_B |
| 2026-11-27 | Retries keep their key (same backend); no failover, an open breaker rejects |
| 2026-11-27 | Thresholds use requests in system N (waiting + in service): N* = μT with the current phase's capacity (100 normal, 50 during slowdown) |
| 2026-11-27 | Shared retry budget: B's effective ratio b/s_B, recovery if b < s_B(1/ρ − 1), stated as steady-state approximation |
| 2026-11-27 | Deadline drop: drop if now + S ≥ attempt deadline, nominal S = 40 ms; gateway drops expired only |
| 2026-11-27 | Deadlines per attempt; goodput by per-attempt deadline (primary), request latency first send → success (secondary); recovery judged on B's goodput |
| 2026-11-27 | Log client attempts per backend and gateway forwarded per backend separately; offered work = forwarded to B |
| 2026-11-27 | Simplified to **one backend** (was A healthy + B slowed). With key routing and no failover A never interacts with B; breaker cost for partial traffic and shared-budget dilution (b/s) derived analytically. Supersedes the per-backend / s_B entries above; retry budget rule back to b < 1/ρ − 1 |
