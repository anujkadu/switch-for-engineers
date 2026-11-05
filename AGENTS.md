# Repository instructions

- Product: Engineering Flight Simulator (EFS), a Discord-first engineering simulation. V1 is Mission 001 — The Double Booking Crisis.
- Discord is the learner interface; Switch is the agent collaboration layer; MCP exposes backend operations.
- The standalone Python backend is authoritative for mission facts, session state, decisions, stage progression, challenge results and evaluation.
- PostgreSQL is the V1 persistence layer, using SQLAlchemy 2.x, psycopg 3 and Alembic. Do not add microservices, a frontend or another orchestrator without an explicit scope decision.
- Developer 1 owns Switch/Discord/agent configuration and agent-side MCP integration.
- Developer 2 owns Python domain logic, persistence, progression, challenge runner, evaluation and backend MCP server.
- MCP names and schemas are joint contracts; do not change unilaterally.
- Keep domain services independent of MCP transport. Validate inputs at service boundaries.
- Never invent state, test results or scores. Never claim in-memory tests prove database-level concurrency correctness.
- Never execute arbitrary learner code with unrestricted shell access.
- Keep secrets and machine-specific identifiers out of source control.
- Inspect existing code/docs, make focused changes, add tests, run relevant checks and report exactly what ran.
