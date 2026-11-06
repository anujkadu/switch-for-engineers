---
name: concurrency-failure-review
description: Independently review software designs and implementations for race conditions, concurrency defects, unsafe state transitions, and data consistency failures. Use when evaluating concurrent operations or systems with shared mutable state.
---

# Concurrency Failure Review

## Objective

Identify how concurrent operations can violate system invariants and produce incorrect outcomes.

## Workflow

1. Understand the intended system behaviour and correctness invariants.
2. Identify shared resources and concurrent operations.
3. Examine critical execution paths for race conditions.
4. Construct concrete execution interleavings that could produce invalid states.
5. Investigate transaction boundaries, isolation levels, locking, atomic operations, and retry behaviour.
6. Examine timeouts, process crashes, stale operations, and failover scenarios.
7. Assess whether database constraints and other durable safeguards enforce correctness.
8. Rank findings by severity and likelihood.
9. Explain the consequences and recommend practical mitigations.

## Rules

- Do not invent system behaviour or requirements.
- Distinguish confirmed defects from hypothetical risks.
- Never assume that distributed locks alone guarantee data consistency.
- Consider the authoritative data store and its actual consistency guarantees.
- Avoid reporting theoretical edge cases without explaining their practical impact.
- Acknowledge sound engineering decisions.
- Do not automatically agree with the Senior Architect.
- Retrieve authoritative mission context through available MCP tools when needed.
- Never fabricate test results or claim that a defect has been reproduced without evidence.
