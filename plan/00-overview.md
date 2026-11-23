# Overview

## Topic ✅
Retry-driven metastable failures: a short trigger (a slow backend) pushes a service chain into overload, and client retries plus stale queued work keep it overloaded after the trigger has ended.

## Framing ✅
Practitioners know several countermeasures, but nobody says **which one to use when, or whether combining them pays off**. The thesis answers this with an **experimentally derived decision guide**. The evaluation is the method, the guide is the result.

## Title ✅
**Choosing the Right Mitigation: Experimentally Derived Guidance for Client-Side and Server-Side Strategies Against Retry-Driven Metastable Failures**

## Constraints ✅
- English, IEEE citations, H-Da LaTeX template (`thesis/`).
- 8 weeks of planned work + 2 weeks buffer.
- Own implementation, measurable results, not a pure literature review, durable topic (no dependency on languages, frameworks or AI models).
- Hardware: MacBook (development), dedicated Linux machine for main testbed runs (old laptop, to be checked).

## Status (2026-11-23)
- Exposé v1 sent, feedback received (see `09-open-items.md` for how each point is answered).
- Simulator feasibility prototype exists (not thesis code): baseline gets stuck, no-retry control recovers.
- Exposés in Claude Docs are not yet updated to the new framing.
