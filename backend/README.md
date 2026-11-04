# EFS Python backend

Standalone Python application owning deterministic mission logic, persistence and the MCP interface.

## Responsibilities
- Mission definitions and requirements
- Session state and current stage
- Learner decisions and reasoning records
- Stage validation/progression
- Coding challenge submissions and controlled test results
- Evidence-based evaluation/scores
- SQLite persistence
- MCP tools that call the same application services used by tests

## Package boundaries
- `domain/`: domain models, enums and invariants
- `missions/`: structured mission definitions/loaders
- `services/`: application use-cases
- `persistence/`: SQLite schema, repositories and transactions
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

This is currently a package scaffold. Domain workflows, database schema, MCP tools and challenge runner are not implemented yet.

## Safety
Never expose arbitrary shell execution through MCP. Before accepting untrusted submissions, the challenge runner needs a fixed test contract and explicit resource/time limits.
