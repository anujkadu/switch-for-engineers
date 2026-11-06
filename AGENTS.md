# AGENTS.md

## Project Overview

EFS stands for **Engineering Foundational Suite**.

EFS is a coordinated multi-agent engineering assistance system built on top of Switch. It helps developers learn, build, review software, explore open-source contributions, and discover career opportunities.

The system consists of a central Orchestrator and specialised agents that collaborate through Switch rooms.

## Core Principles

All agents and contributors working on EFS should follow these principles.

### 1. Understand Before Changing

- Inspect the existing project structure before proposing changes.
- Read the relevant agent instructions and configuration files before modifying them.
- Understand how Switch, the agents, rooms, and MCP integrations interact.
- Do not assume an implementation exists merely because it is described in documentation.

### 2. Preserve the Multi-Agent Architecture

EFS is designed around specialised responsibilities.

- The Orchestrator is the primary developer-facing coordinator.
- Specialist agents should focus on their assigned domains.
- Delegate work when a request genuinely benefits from specialist expertise.
- Collect actual specialist responses before presenting a consolidated result.
- Do not fabricate delegation, tool execution, or specialist feedback.

### 3. Keep Responsibilities Separate

Avoid unnecessarily duplicating responsibilities across agents.

- Engineering Mentor: technical understanding and implementation guidance.
- Senior Architect: architecture, design decisions, and trade-offs.
- Critical Reviewer: independent challenge, risks, and correctness.
- Job Search: career discovery and opportunity research.
- Orchestrator: coordination, delegation, and synthesis.

Refer to `docs/agent-and-skill-model.md` for the responsibility model.

### 4. Prefer Evidence Over Assumptions

- Use connected tools when the task requires external information.
- Ground GitHub claims in actual repository, issue, or pull request data.
- Ground job recommendations in actual Openings MCP results.
- Use Context7 when current library or framework documentation is needed.
- Clearly distinguish retrieved facts from assumptions and recommendations.
- State when a tool or integration is unavailable.

### 5. Protect Credentials and Permissions

- Never commit API keys, access tokens, passwords, or private credentials.
- Do not print secrets in logs, examples, or documentation.
- Use the configured agent-session environment for credentials where required.
- Respect the permissions granted to external integrations.
- Never perform destructive or externally visible operations without appropriate user authorisation.

### 6. Avoid Unverified Capabilities

Do not claim that EFS currently provides:

- Persistent learner progression or scoring.
- Mission-state tracking through a custom backend.
- Database-backed evaluation history.
- Guaranteed job availability or application success.
- Automatic repository modifications without explicit permission.

Document only functionality that is implemented and verified.

## Agent Responsibilities

| Agent | Primary responsibility |
|---|---|
| `efs-orchestrator` | Developer-facing coordination and synthesis |
| `engineering-mentor` | Technical learning and implementation mentorship |
| `senior-architect-test` | System architecture and design analysis |
| `critical-reviewer` | Independent technical challenge and risk analysis |
| `job-search` | Job discovery and career guidance |

The agent names above should remain consistent with the configured Switch agents.

## Collaboration Guidelines

The internal collaboration room is:

`efs-agent-convo`

When coordinating specialist work:

1. Identify the specialist or specialists relevant to the request.
2. Provide each specialist with sufficient task context.
3. Use the internal collaboration room for the handoff.
4. Wait for actual responses.
5. Evaluate conflicting recommendations rather than blindly merging them.
6. Present a clear synthesis to the developer.

Not every request requires every specialist. Delegation should be relevant to the task.

## MCP Integration Guidelines

EFS uses the following integrations:

| MCP | Intended agent | Responsibility |
|---|---|---|
| GitHub MCP | `efs-orchestrator` | GitHub operations and repository information |
| Context7 MCP | `efs-orchestrator` | Technical documentation |
| Openings MCP | `job-search` | Job discovery |

MCP configuration is maintained in the relevant agent `.toml` files.

Credentials, where required, are provided through the configured agent session. Openings MCP does not require credentials in the current EFS setup.

Do not assume an MCP server is available simply because a configuration entry exists. Verify connectivity and tool availability.

## Development Guidelines

When changing EFS:

1. Inspect the relevant files and existing behaviour.
2. Identify which agent, instruction, configuration, or integration is affected.
3. Make the smallest change that addresses the requirement.
4. Preserve existing working behaviour.
5. Validate the change using an appropriate test or runtime check.
6. Update documentation when behaviour or configuration changes.
7. Report what was changed and what remains unverified.

### Configuration changes

- Preserve valid TOML syntax.
- Do not replace existing configuration wholesale without understanding its contents.
- Avoid duplicating MCP definitions unnecessarily.
- Keep environment-specific values out of committed configuration.
- Verify that configuration is loaded by the intended agent runtime.

### Documentation changes

- Use consistent agent names and room names.
- Link to official documentation where platform-specific instructions are maintained externally.
- Distinguish current capabilities from future ideas.
- Avoid documenting speculative implementation details as completed features.

## Git and Contribution Safety

- Do not overwrite unrelated user changes.
- Do not force-push, delete branches, or rewrite history without explicit permission.
- Do not create commits, push changes, or open pull requests unless requested.
- Review the diff before declaring a change complete.
- Keep changes focused and explain their purpose.

## Definition of Done

A change is considered complete when:

- Its intended behaviour is implemented.
- Relevant configuration remains valid.
- Appropriate checks have been performed.
- Existing behaviour has not been unintentionally broken.
- Documentation reflects the change.
- Known limitations and unverified areas are clearly reported.

## Source of Truth

Use the following documents for project understanding:

- `README.md`: project introduction and setup.
- `docs/architecture.md`: system architecture and integrations.
- `docs/agent-and-skill-model.md`: agent responsibilities and skill model.
- `docs/development-workflow.md`: development and contribution practices.

Individual Switch agent instructions remain the source of truth for each agent's runtime behaviour.
