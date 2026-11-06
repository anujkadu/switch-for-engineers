---
name: reliability-failure-mode-review
description: MUST USE when reviewing or discussing production reliability, application crashes, service failures, database-to-message-queue dual writes, lost events, retries, timeouts, partial commits, payment failures, asynchronous processing, message delivery guarantees, recovery, or failover. Automatically activate whenever a system's operation can succeed partially or fail between multiple components. 
---

# Reliability Failure Mode Review

## Objective

Identify how a system behaves when components fail, operations are interrupted, or dependencies become unavailable.

## Workflow

1. Understand the expected system behaviour and reliability requirements.
2. Identify critical components and external dependencies.
3. Examine timeout, retry, and failure-handling behaviour.
4. Identify partial-success and partial-failure scenarios.
5. Examine process crashes, network interruptions, service outages, and failover.
6. Check idempotency, duplicate execution, and recovery mechanisms.
7. Examine data consistency during failure and recovery.
8. Rank findings by severity and practical likelihood.
9. Recommend mitigations and explain their trade-offs.

## Rules

- Distinguish availability problems from correctness problems.
- Never assume retries are automatically safe.
- Consider retry storms, duplicate operations, and cascading failures.
- Do not assume external services participate in database transactions.
- Identify what happens to in-flight operations when a dependency fails.
- Acknowledge adequate failure handling rather than manufacturing criticism.
- Never claim a failure has been tested unless evidence exists.
- Retrieve authoritative mission context through available MCP tools when needed.
