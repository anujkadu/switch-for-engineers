# Engineering Flight Simulator (EFS)

**A Discord-first, AI-assisted engineering simulation where the learner acts as Engineering Lead.**

EFS turns realistic software-engineering incidents into guided missions. The learner investigates a problem, proposes an architecture, defends decisions, implements a focused solution, and reviews evidence with an AI engineering team.

## Mission 001 — The Double Booking Crisis

A high-demand ticket-booking platform occasionally confirms the same seat to multiple customers. The learner investigates the incident, reasons about concurrency and correctness, designs a safe reservation workflow, completes a bounded coding challenge, and reviews evidence.

Stages: **Understand → Architecture → Implementation → Review**.

## Architecture

```text
Learner → Discord → Switch → EFS Orchestrator
                              ├─ Senior Architect
                              ├─ Critical Reviewer
                              └─ Engineering Mentor
                                      |
                                     MCP
                                      |
                         Standalone Python backend
                         ├─ Mission definitions
                         ├─ Session / decision state
                         ├─ Stage validation / progression
                         ├─ Controlled challenge runner
                         └─ Evidence-based evaluation
                                      |
                                    PostgreSQL
```

**Authority boundaries:** Discord is the learner interface; Switch handles agent collaboration; agents provide specialist reasoning; MCP is the typed backend interface; the Python backend is authoritative for mission/session state, decisions, progression, test results and scores. Agents must never invent completion, test results or scores. In-memory tests do not prove database concurrency correctness.

## Agent team

| Agent ID | Responsibility |
|---|---|
| `efs-orchestrator` | Learner-facing coordinator; routes and synthesizes specialist input |
| `senior-architect-test` | Architecture, design alternatives and trade-offs |
| `critical-reviewer` | Independent review, concurrency, correctness, reliability, security and failure modes |
| `engineering-mentor` | Concept explanations, learning-gap diagnosis and progressive hints |

## Repository structure

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── agents/                    # Canonical Switch role instructions
├── .agents/skills/            # Seven Codex project skills
├── backend/
│   ├── src/efs/
│   │   ├── domain/
│   │   ├── missions/
│   │   ├── services/
│   │   ├── persistence/
│   │   ├── mcp/
│   │   └── challenge/
│   └── tests/
├── docs/
└── tests/agent-evaluations/
```

## Quick start

Requires Python 3.11+.

```bash
git clone https://github.com/anujkadu/switch-for-engineers.git
cd switch-for-engineers
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
pytest
ruff check .
python -m efs --check
```

The backend currently provides the Phase 1/2 PostgreSQL persistence and mission engine plus the Phase 3A stdio MCP adapter. The challenge runner, scoring/evaluation and Discord/Switch end-to-end integration remain future work. See [backend/README.md](backend/README.md) and [docs/backend-mcp-contract.md](docs/backend-mcp-contract.md).

## Agents and skills

Agent role prompts are versioned under `agents/`. Apply them to the corresponding local Switch agent using your installed Switch configuration mechanism; these files are canonical prompt sources, not auto-registration. Codex skills are under `.agents/skills/`; open this repository as the Codex working directory and verify discovery. Codex project skills do not automatically become skills in a separate Switch runtime.

## Ownership

- **Developer 1:** Switch, Discord, agent roles/prompts, collaboration and agent-side MCP connection.
- **Developer 2:** Python backend, mission logic, persistence, progression, coding challenge, evaluation and backend MCP server.
- **Joint:** MCP tool names and schemas.

## Principles

1. One standalone backend; no microservices without evidence.
2. Switch remains the collaboration layer; do not duplicate it with another orchestrator.
3. Domain logic stays independent of MCP transport.
4. Backend state and deterministic evaluation are authoritative.
5. Never expose unrestricted shell execution to learner code.
6. Keep secrets, Discord tokens, private room IDs and machine-specific paths out of Git.
7. Focus on delivering one complete mission.

## Current milestone

Repository bootstrap: agent role sources, seven skills, architecture docs and Python package scaffold. Not yet a completed simulator.
