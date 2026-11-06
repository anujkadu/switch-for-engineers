---
name: implementation-code-review
description: Perform rigorous software implementation reviews for correctness, security, concurrency, error handling, maintainability, and adherence to requirements. Use when reviewing submitted code or implementation changes.
---

# Implementation Code Review

## Objective

Identify concrete defects and improvement opportunities in software implementations.

## Workflow

1. Understand the intended behaviour and implementation requirements.
2. Inspect the relevant code and its dependencies.
3. Identify correctness defects and violated assumptions.
4. Examine input validation, error handling, and edge cases.
5. Review concurrency safety, state management, and transaction boundaries.
6. Check security weaknesses and unsafe operations.
7. Evaluate maintainability, readability, and unnecessary complexity.
8. Rank findings by severity.
9. Explain the impact of each finding and recommend practical fixes.
10. Identify areas that require tests or additional evidence.

## Rules

- Prioritise actual defects over stylistic preferences.
- Reference specific code locations when available.
- Do not invent code behaviour or execution results.
- Distinguish confirmed bugs from potential risks.
- Never claim tests passed unless actual test results are available.
- Do not rewrite the entire implementation when targeted fixes are sufficient.
- Acknowledge good implementation decisions.
- Retrieve authoritative requirements through available MCP tools when needed.
