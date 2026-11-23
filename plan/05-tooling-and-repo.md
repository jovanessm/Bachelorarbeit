# Tooling and repository

## Toolstack ✅
| Area | Tool |
|---|---|
| Language | Python 3.12 (simulator, testbed, analysis) ✅ |
| Simulator | own `heapq` event loop ✅ |
| Testbed | `asyncio` (plain TCP + small JSON protocol) |
| Containers | Docker + Docker Compose (`cpus`, `cpuset`) |
| Scenarios | YAML + PyYAML + pydantic |
| Data / analysis | CSV or Parquet, pandas, numpy, scipy |
| Plots | matplotlib (+ seaborn), PDF export for LaTeX |
| Tests | pytest |
| Environment | uv (lock file) |
| Writing | LaTeX with the H-Da template in `thesis/`, IEEEtran BibTeX, Zotero |

Not used: Kubernetes, Prometheus/Grafana, databases, Locust/k6.

## Repository layout (monorepo)
```
Bachelorarbeit/
├── plan/          # this planning folder
├── expose/        # v1, v2, ...
├── experiment/
│   ├── simulator/
│   ├── testbed/   # generator, gateway, backend, docker-compose
│   ├── scenarios/
│   ├── runner/    # runner, calibrate.py, setup script
│   ├── analysis/
│   └── tests/
│   └── data/      # raw CSVs, gitignored; archive at the end
└── thesis/        # H-Da LaTeX template; figures from analysis
```