---
name: concurrency-failure-review
description: Review concurrent workflows for race conditions, violated invariants, unsafe transaction boundaries, retries and duplicate effects.
---

# Concurrency Failure Review

1. State the invariant that must never be violated.
2. Enumerate operation ordering for at least two concurrent actors.
3. Identify read/write and transaction boundaries.
4. Construct an interleaving that violates the invariant.
5. Inspect database constraints, isolation, locks and atomic operations; do not assume behaviour.
6. Analyse retries, duplicate requests, timeouts, crashes and partial completion.
7. Separate prevention, detection and recovery.
8. Specify a test under the real persistence model.

EFS invariant: a seat cannot have more than one active confirmed reservation for the same event. Verify where it is enforced. Check-then-insert without atomic enforcement is suspect. In-memory or single-threaded tests do not prove database concurrency correctness.

Output: invariant; interleaving; root cause; control; remaining failure modes; verification.
