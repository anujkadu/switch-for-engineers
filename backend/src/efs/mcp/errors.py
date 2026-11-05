from efs.domain.errors import (
    InvalidDecisionError,
    InvalidTransitionError,
    LearnerMismatchError,
    SessionNotFoundError,
    StageProgressionError,
)
from efs.missions.registry import MissionNotFoundError


def error_response(exc: Exception) -> dict[str, object]:
    mapping = {
        MissionNotFoundError: ("mission_not_found", "mission or version was not found"),
        SessionNotFoundError: ("session_not_found", "session was not found"),
        LearnerMismatchError: ("learner_mismatch", "learner does not own this session"),
        InvalidTransitionError: ("invalid_transition", str(exc)),
        StageProgressionError: ("progression_not_satisfied", str(exc)),
        InvalidDecisionError: (
            "idempotency_conflict" if "idempotency key" in str(exc) else "invalid_decision",
            str(exc),
        ),
        ValueError: ("invalid_input", str(exc)),
    }
    code, message = mapping.get(type(exc), ("internal_error", "backend operation failed"))
    return {"ok": False, "error": {"code": code, "message": message}}
