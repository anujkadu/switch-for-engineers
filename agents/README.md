# Agent configuration

One directory per Switch agent. Each directory may contain:

| File | Purpose |
|---|---|
| `AGENT.md` | Canonical role prompt: scope, boundaries, collaboration policy |
| `.codex/config.toml` | MCP client configuration for that agent |
| `.agents/skills/*/SKILL.md` | Skills discoverable by that agent |

Applying these files through the supported local Switch configuration process is a separate step; copying files here does not register agents.

| Switch agent ID | Directory | Role prompt | MCP config | Skills |
|---|---|---|---|---|
| `efs-orchestrator` | `efs-orchestrator/` | `AGENT.md` | GitHub, Context7 | `efs-team-orchestration` |
| `senior-architect-test` | `senior-architect-test/` | `AGENT.md` | — | `architecture-tradeoff-analysis` |
| `critical-reviewer` | `critical-reviewer/` | `AGENT.md` | — | `concurrency-failure-review`, `implementation-code-review`, `reliability-failure-mode-review` |
| `engineering-mentor` | `engineering-mentor/` | `AGENT.md` | — | `engineering-concept-explanation`, `progressive-hinting`, `socratic-engineering-coaching` |
| `job-search` | `job-search/` | `AGENT.md` | Openings | — |

The internal collaboration room is `efs-agent-convo`. Its UUID and Discord channel identifiers are intentionally not committed.

Skills live only under each agent directory. There is no repository-level skill copy, so a skill is available to an agent only if it exists in that agent's `.agents/skills/`.

MCP servers are assigned per agent rather than shared globally. GitHub and Context7 are configured for the Orchestrator; Openings is configured for the Job Search agent. See the repository `README.md` for setup and authentication details.
