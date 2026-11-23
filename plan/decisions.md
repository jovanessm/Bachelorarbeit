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
