import pytest
from efs.missions import (
    SAMPLE_MISSION,
    MissionDefinition,
    MissionNotFoundError,
    MissionRegistry,
    StageDefinition,
)


def test_sample_mission_is_ordered_and_exactly_resolvable():
    registry = MissionRegistry((SAMPLE_MISSION,))
    assert registry.get("phase2-sample", "1.0").first_stage.stage_id == "observe"
    with pytest.raises(MissionNotFoundError):
        registry.get("phase2-sample", "latest")


def test_invalid_stage_order_is_rejected():
    with pytest.raises(ValueError):
        MissionDefinition(
            "m", "1", "M", "D", (StageDefinition("s", 2, "I", ("O",), lambda _: True),)
        )
