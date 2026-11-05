from typing import Any

from efs.missions.definitions import MissionDefinition, StageDefinition


def _one_decision(decisions: list[dict[str, Any]]) -> bool:
    return bool(decisions)


SAMPLE_MISSION = MissionDefinition(
    mission_id="phase2-sample",
    version="1.0",
    title="Sample Mission",
    description="A deterministic mission used to exercise the mission engine.",
    stages=(
        StageDefinition(
            stage_id="observe",
            order=1,
            instructions="Record an observation.",
            learning_objectives=("Submit structured evidence",),
            progression_rule=_one_decision,
        ),
        StageDefinition(
            stage_id="act",
            order=2,
            instructions="Record an action.",
            learning_objectives=("Complete a mission",),
            progression_rule=_one_decision,
        ),
    ),
)
