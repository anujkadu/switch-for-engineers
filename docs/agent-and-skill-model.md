# Agent and skill model

| Layer | Purpose | Location |
|---|---|---|
| Switch role instructions | Persistent role, boundaries and collaboration policy | `agents/*/AGENT.md` |
| Codex skills | Repeatable development/review workflows | `.agents/skills/*/SKILL.md` |
| MCP tools | Typed operations over authoritative state | Backend MCP adapter |
| Switch/Discord | Runtime connectivity and learner communication | Local runtime configuration |

## Agent IDs
- `efs-orchestrator` → `agents/orchestrator/AGENT.md`
- `senior-architect-test` → `agents/senior-architect/AGENT.md`
- `critical-reviewer` → `agents/critical-reviewer/AGENT.md`
- `engineering-mentor` → `agents/engineering-mentor/AGENT.md`

Role files are canonical prompt sources, not automatic Switch registration.

## Seven Codex skills
1. `architecture-tradeoff-analysis`
2. `concurrency-failure-review`
3. `reliability-failure-mode-review`
4. `implementation-code-review`
5. `socratic-engineering-coaching`
6. `progressive-hinting`
7. `engineering-concept-explanation`

Open this repository as the Codex working directory and verify skill discovery. A separately launched Switch agent may have a different skill discovery scope; do not assume Codex skills are automatically available there.
