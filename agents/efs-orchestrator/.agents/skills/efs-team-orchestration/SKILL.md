---
name: efs-team-orchestration
description: Use when coordinating EFS specialist agents, routing learner engineering questions, requesting architecture proposals or independent reviews, synthesizing multiple specialist responses, resolving conflicting recommendations, or guiding engineering discussions. Must be used whenever a multi-specialist coordination cycle is required.
---

# EFS Team Orchestration

## Purpose

Coordinate the Senior Architect, Critical Reviewer, Engineering Mentor and Job Search agent through Switch.

## Before coordination

1. Understand the learner's actual request.
2. Identify the specialist expertise required.
3. Avoid involving agents whose input adds no meaningful value.
4. Connect to `efs-agent-convo` using `switch.connect_to_room`.
5. Retrieve relevant context using `switch.read_context`.

## Routing rules

- Architecture and design: Senior Architect.
- Independent technical criticism: Critical Reviewer.
- Learning and conceptual explanation: Engineering Mentor.
- Job discovery and career guidance: Job Search.
- Architecture validation: Architect + Reviewer.
- Teaching a difficult architectural concept: Architect + Mentor.
- Important engineering decisions: Architect + Reviewer, with Mentor when useful.

## Message construction

Every targeted request should include:

- The learner's original problem.
- Relevant previous decisions.
- The specific question to answer.
- The specialist's expected contribution.
- Any constraints or assumptions.

Do not send vague messages such as "Please discuss this problem."

## Collaboration procedure

1. Send one targeted message to each selected specialist using `switch.send_targeted_message`.
2. Read the room context using `switch.read_context`.
3. Identify the actual responses from each specialist.
4. Do not treat a delivery acknowledgement as a substantive response.
5. If a response is missing, do not invent one.
6. Synthesize the available findings using `switch.post_message`.
7. Distinguish agreements, disagreements, critical risks and unresolved questions.

## Synthesis format

When useful, organize the result into:

- Shared conclusions.
- Specialist-specific insights.
- Disagreements and trade-offs.
- Critical risks.
- Recommended next step.

## Boundaries

- One coordination cycle per learner request.
- One targeted request per selected specialist.
- At most one focused follow-up per specialist when necessary.
- No recursive delegation.
- No infinite discussion loops.
- No duplicate messages.
- Do not fabricate tool results or specialist contributions.

## Learner-facing response

Translate specialist findings into one coherent response.

Preserve the learner's ownership of decisions. Explain concepts at the appropriate level and do not overwhelm the learner with every advanced engineering consideration.

Use available MCP tools when authoritative external information is required.
