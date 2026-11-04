# Development workflow

## Setup
```bash
git clone https://github.com/anujkadu/switch-for-engineers.git
cd switch-for-engineers
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Checks
```bash
pytest
ruff check .
python -m efs --check
```

## Suggested sequence
1. Agree mission/session/stage identifiers and MCP schemas.
2. Define domain models and stage enums.
3. Add Mission 001 structured definition and validation.
4. Add SQLite schema, transactions and repositories.
5. Implement session/decision services with tests.
6. Implement deterministic stage validation/progression.
7. Define challenge interface and safe runner boundary.
8. Implement evidence-based evaluation.
9. Add MCP handlers calling services.
10. Prove real Switch-agent-to-MCP invocation with one read-only tool.
11. Add remaining tools and end-to-end tests.

Use focused branches, update docs when contracts change, run relevant tests, and never commit credentials, database files or private runtime identifiers. This scaffold is not a completed simulator.
