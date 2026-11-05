import hashlib
import json
import uuid
from collections.abc import Mapping
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker

from efs.domain.errors import (
    InvalidDecisionError,
    InvalidTransitionError,
    LearnerMismatchError,
    SessionNotFoundError,
    StageProgressionError,
)
from efs.missions.registry import MissionRegistry
from efs.persistence.models import (
    EventType,
    MissionDecision,
    MissionEvent,
    MissionSession,
    SessionStatus,
)


class MissionService:
    def __init__(self, sessions: sessionmaker[Session], registry: MissionRegistry) -> None:
        self.sessions = sessions
        self.registry = registry

    def start_mission(self, learner_id: str, mission_id: str, version: str) -> MissionSession:
        self._require_learner(learner_id)
        mission = self.registry.get(mission_id, version)
        try:
            with self.sessions.begin() as session:
                existing = self._active_session(session, learner_id, mission_id, version)
                if existing:
                    return existing
                item = MissionSession(
                    learner_id=learner_id,
                    mission_id=mission.mission_id,
                    mission_version=mission.version,
                    current_stage_id=mission.first_stage.stage_id,
                    status=SessionStatus.ACTIVE,
                )
                session.add(item)
                session.flush()
                self._event(session, item, EventType.MISSION_STARTED, item.current_stage_id)
                return item
        except IntegrityError as exc:
            if "uq_efs_active_mission_session" not in str(exc.orig):
                raise
            with self.sessions() as session:
                existing = self._active_session(session, learner_id, mission_id, version)
                if existing:
                    return existing
            raise

    def submit_decision(
        self, session_id: uuid.UUID, learner_id: str, content: Mapping[str, object],
        idempotency_key: str | None = None,
    ) -> MissionDecision:
        self._require_learner(learner_id)
        if not isinstance(content, Mapping) or not content:
            raise InvalidDecisionError("decision content must be a non-empty object")
        idempotency_key = idempotency_key or str(uuid.uuid4())
        if not idempotency_key.strip():
            raise InvalidDecisionError("idempotency_key must be non-empty")
        request_hash = hashlib.sha256(
            json.dumps(content, sort_keys=True, separators=(",", ":"), default=str).encode()
        ).hexdigest()
        with self.sessions.begin() as session:
            item = self._locked_session(session, session_id)
            if item.learner_id != learner_id:
                raise LearnerMismatchError("decision learner does not own the session")
            if item.status is not SessionStatus.ACTIVE:
                raise InvalidTransitionError("decisions can only be submitted to active sessions")
            existing = session.scalar(
                select(MissionDecision).where(
                    MissionDecision.session_id == item.id,
                    MissionDecision.learner_id == learner_id,
                    MissionDecision.idempotency_key == idempotency_key,
                )
            )
            if existing:
                if existing.request_hash != request_hash:
                    raise InvalidDecisionError("idempotency key was reused with different content")
                return existing
            decision = MissionDecision(
                session_id=item.id,
                learner_id=learner_id,
                stage_id=item.current_stage_id,
                content=dict(content),
                idempotency_key=idempotency_key,
                request_hash=request_hash,
            )
            session.add(decision)
            session.flush()
            self._event(
                session,
                item,
                EventType.DECISION_SUBMITTED,
                item.current_stage_id,
                {"decision_id": str(decision.id)},
            )
            return decision

    def advance_stage(self, session_id: uuid.UUID, learner_id: str) -> MissionSession:
        with self.sessions.begin() as session:
            item = self._locked_session(session, session_id)
            self._check_owner(item, learner_id)
            if item.status is not SessionStatus.ACTIVE:
                raise InvalidTransitionError("only active sessions can advance")
            mission = self.registry.get(item.mission_id, item.mission_version)
            stage = mission.stage(item.current_stage_id)
            decisions = session.scalars(
                select(MissionDecision).where(
                    MissionDecision.session_id == item.id,
                    MissionDecision.stage_id == item.current_stage_id,
                )
            ).all()
            decision_data = [decision.content for decision in decisions]
            if not stage.progression_rule(decision_data):
                raise StageProgressionError("stage progression requirements are not satisfied")
            next_stage = mission.next_stage(item.current_stage_id)
            if next_stage is None:
                item.status = SessionStatus.COMPLETED
                item.completed_at = datetime.now(UTC)
                self._event(session, item, EventType.MISSION_COMPLETED, item.current_stage_id)
            else:
                item.current_stage_id = next_stage.stage_id
                self._event(session, item, EventType.STAGE_ADVANCED, next_stage.stage_id)
            session.flush()
            return item

    def abandon_mission(self, session_id: uuid.UUID, learner_id: str) -> MissionSession:
        with self.sessions.begin() as session:
            item = self._locked_session(session, session_id)
            self._check_owner(item, learner_id)
            if item.status is not SessionStatus.ACTIVE:
                raise InvalidTransitionError("only active sessions can be abandoned")
            item.status = SessionStatus.ABANDONED
            item.abandoned_at = datetime.now(UTC)
            self._event(session, item, EventType.MISSION_ABANDONED, item.current_stage_id)
            session.flush()
            return item

    def complete_mission(self, session_id: uuid.UUID, learner_id: str) -> MissionSession:
        """Complete only when the current stage is final and satisfied."""
        with self.sessions.begin() as session:
            item = self._locked_session(session, session_id)
            self._check_owner(item, learner_id)
            if item.status is not SessionStatus.ACTIVE:
                raise InvalidTransitionError("only active sessions can be completed")
            mission = self.registry.get(item.mission_id, item.mission_version)
            if mission.next_stage(item.current_stage_id) is not None:
                raise InvalidTransitionError("the current stage is not final")
            decisions = session.scalars(
                select(MissionDecision).where(
                    MissionDecision.session_id == item.id,
                    MissionDecision.stage_id == item.current_stage_id,
                )
            ).all()
            if not mission.stage(item.current_stage_id).progression_rule(
                [decision.content for decision in decisions]
            ):
                raise StageProgressionError("stage progression requirements are not satisfied")
            item.status = SessionStatus.COMPLETED
            item.completed_at = datetime.now(UTC)
            self._event(session, item, EventType.MISSION_COMPLETED, item.current_stage_id)
            session.flush()
            return item

    def get_progress(self, session_id: uuid.UUID, learner_id: str) -> MissionSession:
        with self.sessions() as session:
            item = session.get(MissionSession, session_id)
            if not item:
                raise SessionNotFoundError(str(session_id))
            self._check_owner(item, learner_id)
            return item

    def get_decision_history(self, session_id: uuid.UUID, learner_id: str) -> list[MissionDecision]:
        with self.sessions() as session:
            item = self._locked_session(session, session_id)
            self._check_owner(item, learner_id)
            return list(
                session.scalars(
                    select(MissionDecision)
                    .where(MissionDecision.session_id == session_id)
                    .order_by(MissionDecision.submitted_at, MissionDecision.id)
                )
            )

    @staticmethod
    def _require_learner(learner_id: str) -> None:
        if not learner_id or not learner_id.strip():
            raise ValueError("learner_id must be non-empty")

    @staticmethod
    def _check_owner(item: MissionSession, learner_id: str) -> None:
        MissionService._require_learner(learner_id)
        if item.learner_id != learner_id:
            raise LearnerMismatchError("learner does not own the session")

    @staticmethod
    def _locked_session(session: Session, session_id: uuid.UUID) -> MissionSession:
        item = session.scalar(
            select(MissionSession).where(MissionSession.id == session_id).with_for_update()
        )
        if not item:
            raise SessionNotFoundError(str(session_id))
        return item

    @staticmethod
    def _active_session(
        session: Session, learner_id: str, mission_id: str, version: str
    ) -> MissionSession | None:
        return session.scalar(
            select(MissionSession)
            .where(
                MissionSession.learner_id == learner_id,
                MissionSession.mission_id == mission_id,
                MissionSession.mission_version == version,
                MissionSession.status == SessionStatus.ACTIVE,
            )
            .with_for_update()
        )

    @staticmethod
    def _event(
        session: Session,
        item: MissionSession,
        event_type: EventType,
        stage_id: str | None,
        payload=None,
    ) -> None:
        session.add(
            MissionEvent(
                session_id=item.id,
                learner_id=item.learner_id,
                event_type=event_type,
                stage_id=stage_id,
                payload=payload or {},
            )
        )
