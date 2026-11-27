# experiment/

Simulator, testbed and analysis for the thesis. Plan: `../plan/11-implementation-plan.md`.

## Setup

```sh
cd experiment
uv sync          # installs Python 3.12 + dependencies from uv.lock
uv run pytest    # runs the tests
```

## Layout

| Folder | Content |
|---|---|
| `common/` | Shared contract: protocol, scenario schema, log schemas, CSV writers |
| `scenarios/` | Scenario YAML files + grid generator |
| `testbed/` | Load generator, gateway, backend (asyncio), Docker Compose |
| `simulator/` | Own `heapq` event loop + client/gateway/backend modules |
| `runner/` | Single runs, batches, `calibrate.py`, setup script |
| `analysis/` | Per second → per run → per cell → decision guide, model predictions, plots |
| `tests/` | pytest |
| `data/` | Raw run data (gitignored) |
