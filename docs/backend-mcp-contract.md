# Backend and MCP contract

**Status: proposal only.** Tool schemas must be agreed jointly by Developer 1 and Developer 2 before runtime configuration depends on them. Names below are candidates, not implemented tools.

Developer 2 owns the backend MCP server/tool implementations. Developer 1 owns agent-side MCP client configuration and end-to-end verification.

## Principles
- Tool handlers call application services; no domain rules in handlers.
- State-changing calls validate session, stage and input.
- Return structured success/error results.
- Make writes safe against duplicate delivery where appropriate.
- Agents trust returned state, not assumptions.
- Never expose arbitrary SQL, shell or filesystem access.

## Candidate tool set

| Capability | Candidate tool | Purpose |
|---|---|---|
| Mission | `get_mission` | Read mission definition |
| Session | `create_session` | Start learner session |
| Session | `get_session` | Read authoritative state |
| Decisions | `save_decision` | Persist explicit decision and rationale |
| Decisions | `list_decisions` | Read recorded decisions |
| Progression | `validate_stage` | Evaluate stage requirements |
| Progression | `advance_stage` | Perform permitted transition |
| Challenge | `get_challenge` | Read challenge instructions |
| Challenge | `submit_challenge` | Submit to controlled runner |
| Challenge | `get_test_results` | Read actual test result |
| Evaluation | `get_evaluation` | Read backend-computed assessment |

Finalise argument/return schemas, error codes, session scoping and idempotency semantics jointly.

## First integration proof
Start with a harmless read-only tool such as `get_mission`. Verify that the actual Switch-connected agent can discover it, invoke it, receive its result and report that exact result in Discord. Repeat after runtime restart.

Backend computes stage progression, test results and scores. LLMs may explain evidence but must not invent or recalculate authoritative results.
