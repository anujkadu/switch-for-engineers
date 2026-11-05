# EFS Python backend

Standalone Python application owning deterministic mission logic, persistence and the MCP interface.

## Responsibilities
- Mission definitions and requirements
- Session state and current stage
- Learner decisions and reasoning records
- Stage validation/progression
- Coding challenge submissions and controlled test results
- Evidence-based evaluation/scores
- PostgreSQL persistence through SQLAlchemy 2.x and psycopg 3
- MCP tools that call the same application services used by tests

## Package boundaries
- `domain/`: domain models, enums and invariants
- `missions/`: structured mission definitions/loaders
- `services/`: application use-cases
- `persistence/`: database schema, repositories and transactions
- `mcp/`: thin MCP handlers only; no business rules
- `challenge/`: bounded challenge interface and safe runner

## Setup
From repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest
python -m efs --check
```

Phase 3A provides a stdio MCP adapter over the mission service. It exposes separate orchestrator and specialist profiles; specialists receive read-only tools.

## MCP server

After installing the package into the active virtual environment:

```bash
EFS_DATABASE_URL='postgresql+psycopg://...' EFS_MCP_PROFILE=orchestrator efs-mcp
EFS_DATABASE_URL='postgresql+psycopg://...' EFS_MCP_PROFILE=specialist efs-mcp
```

Keep credentials in `.env` or the process environment. MCP protocol output is written to stdout; application logging is written to stderr. The orchestrator profile exposes all eight mission tools. The specialist profile exposes only `get_mission`, `get_mission_progress`, and `get_decision_history`.

Use the isolated `EFS_TEST_DATABASE_URL` for integration tests. Never configure automated tests with the production URL.

## Database configuration

Set `EFS_DATABASE_URL`, optional `EFS_TEST_DATABASE_URL`, and `EFS_LOG_LEVEL` in a local `.env` file. URLs must use PostgreSQL with psycopg 3; SQLite URLs are rejected. Never commit `.env` or credentials.

From the repository root, review migration SQL with:

```bash
EFS_DATABASE_URL='postgresql+psycopg://...' alembic -c backend/alembic.ini upgrade head --sql
```

The initial migration creates `efs` and `efs.alembic_version` only. It must be explicitly reviewed before applying to Neon production. Do not use `Base.metadata.create_all()` for production schema management.

Run tests and lint from the repository root with `pytest` and `ruff check .`. Integration tests must use a separate PostgreSQL test database and must never target production.

The mission engine uses exact mission ID/version lookup, append-only decisions, explicit stage progression rules, row locking for progression, and one active session per learner/mission/version. Set `EFS_TEST_DATABASE_URL` before running PostgreSQL integration tests; tests skip clearly when it is absent.

## Safety
Never expose arbitrary shell execution through MCP. Before accepting untrusted submissions, the challenge runner needs a fixed test contract and explicit resource/time limits.
