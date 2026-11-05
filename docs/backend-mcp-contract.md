# Backend and MCP contract

**Status: Phase 3A implemented locally.** The stdio server exposes the contracts below through separate capability profiles.

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

All responses use `{ok: true, ...}` or `{ok: false, error: {code, message}}`. UUIDs are strings and timestamps are RFC 3339. Decision submissions require an `idempotency_key`; reusing a key with different content returns `idempotency_conflict`.

Start the server with `efs-mcp` and `EFS_MCP_PROFILE=orchestrator|specialist`. The specialist profile cannot discover mutation tools because they are not registered in that server instance.

## First integration proof
Start with a harmless read-only tool such as `get_mission`. Verify that the actual Switch-connected agent can discover it, invoke it, receive its result and report that exact result in Discord. Repeat after runtime restart.

Backend computes stage progression, test results and scores. LLMs may explain evidence but must not invent or recalculate authoritative results.
