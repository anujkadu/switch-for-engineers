---
name: architecture-tradeoff-analysis
description: Analyse architecture proposals, compare viable alternatives, expose trade-offs and recommend the simplest design satisfying explicit requirements.
---

# Architecture Tradeoff Analysis

1. Restate requirements/constraints; separate facts from assumptions.
2. Identify relevant quality attributes and invariants.
3. Describe the proposal as components and data/request flows.
4. Compare at least one credible alternative.
5. Evaluate correctness, consistency, availability, latency, throughput, complexity, operability and cost as relevant.
6. Explain strongest arguments for and against each option.
7. Recommend the simplest sufficient option.
8. State uncertainties and evidence that could change the recommendation.

For EFS Mission 001 consider seat uniqueness, reservation lifecycle, transaction boundaries, idempotency and contention. Do not recommend distributed infrastructure without evidence.

Output: requirements/assumptions; options; trade-offs; recommendation; risks/validation; one decision question.
