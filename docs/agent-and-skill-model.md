# EFS Agent and Skill Model

## 1. Introduction

EFS uses a specialised multi-agent architecture.

Instead of expecting one AI agent to handle every engineering task, EFS distributes responsibilities across agents with different areas of expertise.

Each agent has a defined role, instructions, and access to relevant tools.

The system also supports the use of reusable skills to organise repeatable workflows and domain-specific procedures.

This document explains how agents and skills fit together.

## 2. What Is an Agent?

An agent is an AI-powered worker configured to perform a particular responsibility.

An agent generally has:

- A name and description.
- A system or role instruction.
- A configured model provider.
- An execution environment.
- Access to selected tools and MCP integrations.
- Room membership and communication capabilities.

An agent's instructions define how it should interpret requests, approach tasks, and communicate results.

## 3. EFS Agent Structure

EFS currently defines five primary agents.

### 3.1 EFS Orchestrator

**Agent ID:** `efs-orchestrator`

**Role:** Central coordinator and developer-facing interface.

The Orchestrator is responsible for understanding developer requests and coordinating specialist agents.

Responsibilities:

- Act as the primary point of contact.
- Understand the developer's intent.
- Determine whether specialist delegation is necessary.
- Identify the appropriate specialist agents.
- Coordinate handoffs through `efs-agent-convo`.
- Collect actual specialist responses.
- Resolve conflicting recommendations where possible.
- Produce a consolidated response.

The Orchestrator should not pretend to have received specialist feedback when no specialist response exists.

**Primary integrations:**

- GitHub MCP
- Context7 MCP

### 3.2 Engineering Mentor

**Agent ID:** `engineering-mentor`

**Role:** Technical mentor and implementation guide.

Responsibilities:

- Explain programming and engineering concepts.
- Help developers understand unfamiliar technologies.
- Break complex implementation tasks into manageable steps.
- Explain the reasoning behind implementation decisions.
- Encourage understanding rather than blind code copying.
- Provide practical examples where appropriate.

The Engineering Mentor should adapt its explanation to the developer's stated experience and task.

### 3.3 Senior Architect

**Agent ID:** `senior-architect-test`

**Role:** Architecture and system design specialist.

Responsibilities:

- Evaluate proposed system architectures.
- Identify component boundaries and dependencies.
- Analyse scalability and maintainability concerns.
- Discuss architectural trade-offs.
- Identify risks in technology and design choices.
- Recommend appropriate patterns where justified.

Recommendations should explain their reasoning and relevant trade-offs rather than presenting one design as universally correct.

### 3.4 Critical Reviewer

**Agent ID:** `critical-reviewer`

**Role:** Independent technical reviewer.

Responsibilities:

- Challenge assumptions.
- Identify logical weaknesses.
- Evaluate correctness and edge cases.
- Highlight security and reliability concerns.
- Identify missing requirements.
- Question recommendations that lack sufficient evidence.

The Critical Reviewer should provide independent analysis rather than merely agreeing with another agent's conclusions.

### 3.5 Job Search Agent

**Agent ID:** `job-search`

**Role:** Career discovery and opportunity research specialist.

Responsibilities:

- Discover relevant job opportunities.
- Search supported job sources using Openings MCP.
- Evaluate opportunities against stated skills and interests.
- Identify recurring technology and experience requirements.
- Highlight possible skill gaps.
- Provide grounded career recommendations.

**Primary integration:**

- Openings MCP

Job listings and availability must be based on actual tool results. The agent must not invent employers, job descriptions, or vacancies.

## 4. Agent Responsibility Matrix

| Capability | Orchestrator | Mentor | Architect | Reviewer | Job Search |
|---|---|---|---|---|---|
| Request classification | Primary | — | — | — | — |
| Technical mentorship | Coordinates | Primary | Supporting | Supporting | — |
| Architecture analysis | Coordinates | Supporting | Primary | Challenges | — |
| Independent review | Coordinates | Supporting | Supporting | Primary | — |
| GitHub workflows | Primary tool access | Supporting | Supporting | Supporting | — |
| Documentation retrieval | Primary tool access | Supporting | Supporting | Supporting | — |
| Job discovery | Coordinates | — | — | — | Primary |

The table describes intended responsibilities, not a requirement that every request involve all agents.

## 5. What Is a Skill?

A skill is a reusable set of instructions or workflow knowledge that helps an agent perform a particular kind of task consistently.

A skill may describe:

- A repeatable procedure.
- Domain-specific guidance.
- Expected inputs and outputs.
- Validation steps.
- Tool usage conventions.
- Decision-making criteria.

A skill is not necessarily a separate agent.

For example, an agent may use a reusable architecture-review skill while remaining the same Senior Architect agent.

## 6. Agent vs. Skill

| Aspect | Agent | Skill |
|---|---|---|
| Purpose | Performs a defined role | Provides reusable task knowledge |
| Identity | Has an agent identity | Does not need a separate identity |
| Instructions | Defines overall behaviour | Defines a focused workflow |
| Execution | Runs as an agent | Used by an agent when relevant |
| Collaboration | Can communicate with other agents | Does not independently coordinate agents |
| Example | `engineering-mentor` | A reusable code-explanation workflow |

A useful way to think about the relationship:

**Agent = Who performs the work**

**Skill = How a particular task should be performed**

## 7. How Skills Fit into EFS

Skills can help standardise repeated workflows across the system.

Examples of potential skill areas include:

| Skill area | Example use |
|---|---|
| Architecture evaluation | Review component boundaries and trade-offs |
| Code review | Identify correctness, maintainability, and security issues |
| Repository exploration | Understand project structure and contribution conventions |
| Documentation research | Retrieve and interpret relevant technical documentation |
| Job matching | Compare actual job requirements with developer-provided skills |

These examples describe possible reusable skill capabilities. They should only be documented as implemented skills once the corresponding skill files and configuration exist.

## 8. Collaboration Model

The Orchestrator coordinates specialist agents through the internal Switch room:

`efs-agent-convo`

A typical collaboration process:

1. The Orchestrator receives a request.
2. It identifies the required expertise.
3. It delegates relevant work to one or more specialists.
4. Specialists perform their assigned analysis.
5. Specialists return their findings.
6. The Orchestrator evaluates and combines the results.
7. The developer receives a consolidated response.

### Example: Architecture review

A developer asks:

> Evaluate this application architecture for scalability and maintainability.

The Orchestrator may:

1. Delegate design analysis to the Senior Architect.
2. Ask the Critical Reviewer to independently challenge the proposal.
3. Collect the responses.
4. Highlight agreements and disagreements.
5. Present the final assessment and recommendations.

The same process should not be forced onto simple requests that do not need multiple specialists.

## 9. Designing New Agents

When introducing a new EFS agent, define the following before adding it to Switch:

1. **Purpose:** What problem does the agent solve?
2. **Responsibility:** What work does it own?
3. **Boundaries:** What should it not attempt?
4. **Inputs:** What information does it need?
5. **Outputs:** What should it return?
6. **Tools:** Which MCP integrations or other tools does it require?
7. **Collaboration:** When should the Orchestrator involve it?
8. **Validation:** How can its responses be evaluated?

Avoid creating agents that duplicate existing responsibilities without a clear reason.

## 10. Designing New Skills

Before adding a skill:

1. Identify a repeated workflow.
2. Determine which agent should use it.
3. Define the expected input and output.
4. Write clear, reusable instructions.
5. Include validation and failure-handling guidance.
6. Test it against representative tasks.
7. Update documentation to reflect its actual availability.

Prefer reusable skills over creating a new agent for every small capability.

## 11. Guiding Principle

EFS should remain modular and specialised.

Agents should have clear ownership. Skills should capture reusable knowledge. The Orchestrator should coordinate work without unnecessarily duplicating specialist responsibilities.

The goal is not to maximise the number of agents. The goal is to provide the right expertise at the right time.
