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

Phase 1 provides PostgreSQL settings, SQLAlchemy sessions, and an Alembic migration that creates only the isolated `efs` schema. Domain workflows, MCP tools and the challenge runner are not implemented yet.

## Database configuration

Set `EFS_DATABASE_URL`, optional `EFS_TEST_DATABASE_URL`, and `EFS_LOG_LEVEL` in a local `.env` file. URLs must use PostgreSQL with psycopg 3; SQLite URLs are rejected. Never commit `.env` or credentials.

From the repository root, review migration SQL with:

```bash
EFS_DATABASE_URL='postgresql+psycopg://...' alembic -c backend/alembic.ini upgrade head --sql
```

The initial migration creates `efs` and `efs.alembic_version` only. It must be explicitly reviewed before applying to Neon production. Do not use `Base.metadata.create_all()` for production schema management.

Run tests and lint from the repository root with `pytest` and `ruff check .`. Integration tests must use a separate PostgreSQL test database and must never target production.

## Safety
Never expose arbitrary shell execution through MCP. Before accepting untrusted submissions, the challenge runner needs a fixed test contract and explicit resource/time limits.
