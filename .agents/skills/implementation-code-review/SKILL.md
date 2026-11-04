---
name: implementation-code-review
description: Review code for correctness, security, maintainability, test coverage and consistency with architecture and backend contracts.
---

# Implementation Code Review

1. Read requirements, architecture notes and contracts first.
2. Trace changed code paths and callers.
3. Prioritise correctness, data integrity, security and failure handling.
4. Check validation, errors, resource lifecycle and concurrency assumptions.
5. Check normal and adversarial test cases.
6. Verify tests exercise the claimed behaviour.
7. Report findings by severity with file/line references where possible.
8. Separate blockers from improvements/questions.
9. Never claim tests ran without execution evidence.

Output: verdict; severity-ordered findings; missing tests; limitations/non-findings.
