# EFS architecture

Discord is the learner interface. Switch routes and connects the learner-facing Orchestrator and specialists. Agents use MCP to access a standalone Python backend. The backend persists authoritative state in PostgreSQL through SQLAlchemy 2.x, psycopg 3 and Alembic.

- **Discord:** conversation surface, not mission state.
- **Switch:** agent connectivity, shared room context and targeted collaboration.
- **Agents:** Orchestrator routes/synthesizes; Architect analyses design; Reviewer analyses correctness/failure; Mentor teaches progressively.
- **MCP adapter:** thin typed boundary calling application services.
- **Python backend:** sole authority for mission definitions, sessions, decisions, progression, challenge results and evaluation.
- **PostgreSQL:** V1 persistence. EFS application objects live in the dedicated `efs` schema; Neon-managed `neon_auth` is never modified.

## Request flow
1. Learner messages Discord.
2. Switch routes to Orchestrator.
3. Orchestrator retrieves authoritative context through MCP when needed.
4. Orchestrator consults relevant specialists through targeted Switch messages.
5. Orchestrator synthesizes the answer.
6. Learner decisions are submitted to backend services.
7. Backend validates and persists; its response confirms the write.
8. Backend services validate stage progression and compute evaluation.

## Constraints
One backend, not microservices. Domain services are transport-independent. No arbitrary learner shell execution. No agent-authored mission state or scores. Mem0, if considered later, is optional agent knowledge only—not mission/session authority.
