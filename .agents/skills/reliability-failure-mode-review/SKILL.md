---
name: reliability-failure-mode-review
description: Identify service failure modes, partial failures, recovery gaps, operational risks and resilience trade-offs.
---

# Reliability Failure Mode Review

1. Map the critical user journey and dependencies.
2. Identify component, network, database and external-service failures.
3. For each, describe trigger, symptom and user impact.
4. Analyse timeouts, retries, idempotency, backpressure and degraded operation.
5. Identify consistency and recovery implications.
6. Rank risks only where evidence supports it; do not invent probabilities.
7. Recommend proportionate mitigations and operational signals.
8. State unknowns and propose failure-injection/integration tests.

Prefer practical controls over generic "add retries" or "use a queue" advice.
