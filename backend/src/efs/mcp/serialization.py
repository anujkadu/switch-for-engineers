# ruff: noqa: E501
from datetime import datetime
from typing import Any


def timestamp(value: datetime | None) -> str | None:
    return value.isoformat() if value else None


def session(value: Any) -> dict[str, Any]:
    return {"id": str(value.id), "learner_id": value.learner_id,
            "mission_id": value.mission_id, "mission_version": value.mission_version,
            "current_stage_id": value.current_stage_id, "status": value.status.value,
            "started_at": timestamp(value.started_at), "completed_at": timestamp(value.completed_at),
            "abandoned_at": timestamp(value.abandoned_at)}


def decision(value: Any) -> dict[str, Any]:
    return {"id": str(value.id), "session_id": str(value.session_id),
            "learner_id": value.learner_id, "stage_id": value.stage_id,
            "content": value.content, "submitted_at": timestamp(value.submitted_at)}


def definition(value: Any) -> dict[str, Any]:
    return {"mission_id": value.mission_id, "version": value.version,
            "title": value.title, "description": value.description,
            "stages": [{"stage_id": s.stage_id, "order": s.order,
                         "instructions": s.instructions,
                         "learning_objectives": list(s.learning_objectives)} for s in value.stages]}
