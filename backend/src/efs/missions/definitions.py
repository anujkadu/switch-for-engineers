from dataclasses import dataclass
from typing import Any, Protocol


class ProgressionRule(Protocol):
    def __call__(self, decisions: list[dict[str, Any]]) -> bool: ...


@dataclass(frozen=True)
class StageDefinition:
    stage_id: str
    order: int
    instructions: str
    learning_objectives: tuple[str, ...]
    progression_rule: ProgressionRule

    def __post_init__(self) -> None:
        if not self.stage_id or self.order < 1 or not self.instructions:
            raise ValueError("stage_id, positive order, and instructions are required")
        if not self.learning_objectives:
            raise ValueError("at least one learning objective is required")


@dataclass(frozen=True)
class MissionDefinition:
    mission_id: str
    version: str
    title: str
    description: str
    stages: tuple[StageDefinition, ...]

    def __post_init__(self) -> None:
        if not self.mission_id or not self.version or not self.title or not self.description:
            raise ValueError("mission identity and descriptive fields are required")
        if not self.stages:
            raise ValueError("a mission requires at least one stage")
        orders = [stage.order for stage in self.stages]
        if orders != list(range(1, len(orders) + 1)):
            raise ValueError("stages must have contiguous order values starting at one")
        if len({stage.stage_id for stage in self.stages}) != len(self.stages):
            raise ValueError("stage IDs must be unique")

    @property
    def first_stage(self) -> StageDefinition:
        return self.stages[0]

    def stage(self, stage_id: str) -> StageDefinition:
        for stage in self.stages:
            if stage.stage_id == stage_id:
                return stage
        raise KeyError(stage_id)

    def next_stage(self, stage_id: str) -> StageDefinition | None:
        current = self.stage(stage_id)
        return self.stages[current.order] if current.order < len(self.stages) else None
