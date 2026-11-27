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

## Status (2026-11-27)
- Exposé v2 sent; second feedback round answered (see `00-feedback.md`).
- Design simplified to one backend; core cut to 2 mechanisms (retry budget, deadline drop), circuit breaker and load shedding as phase 2.
- Simulator feasibility prototype exists (not thesis code): baseline gets stuck, no-retry control recovers.
- Exposé v3 due 29.11.2026.
