import enum
import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, UniqueConstraint, func, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from efs.db import Base


class SessionStatus(enum.StrEnum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class EventType(enum.StrEnum):
    MISSION_STARTED = "mission_started"
    DECISION_SUBMITTED = "decision_submitted"
    STAGE_ADVANCED = "stage_advanced"
    MISSION_COMPLETED = "mission_completed"
    MISSION_ABANDONED = "mission_abandoned"


def enum_values(enum_type: type[enum.StrEnum]) -> list[str]:
    return [item.value for item in enum_type]


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class MissionSession(TimestampMixin, Base):
    __tablename__ = "mission_sessions"
    __table_args__ = (
        Index(
            "uq_efs_active_mission_session",
            "learner_id",
            "mission_id",
            "mission_version",
            unique=True,
            postgresql_where=text("status = 'active'"),
        ),
        {"schema": "efs"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_id: Mapped[str] = mapped_column(String(255), nullable=False)
    mission_version: Mapped[str] = mapped_column(String(64), nullable=False)
    current_stage_id: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[SessionStatus] = mapped_column(
        Enum(
            SessionStatus,
            name="session_status",
            schema="efs",
            values_callable=enum_values,
        ),
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    abandoned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    decisions: Mapped[list["MissionDecision"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )
    events: Mapped[list["MissionEvent"]] = relationship(
        back_populates="session", cascade="all, delete-orphan"
    )


class MissionDecision(Base):
    __tablename__ = "mission_decisions"
    __table_args__ = (
        UniqueConstraint(
            "session_id", "learner_id", "idempotency_key",
            name="uq_efs_decision_idempotency",
        ),
        {"schema": "efs"},
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("efs.mission_sessions.id", ondelete="CASCADE"), nullable=False
    )
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    stage_id: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    request_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    session: Mapped[MissionSession] = relationship(back_populates="decisions")


class MissionEvent(Base):
    __tablename__ = "mission_events"
    __table_args__ = ({"schema": "efs"},)

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("efs.mission_sessions.id", ondelete="CASCADE"), nullable=False
    )
    learner_id: Mapped[str] = mapped_column(String(255), nullable=False)
    event_type: Mapped[EventType] = mapped_column(
        Enum(EventType, name="event_type", schema="efs", values_callable=enum_values),
        nullable=False,
    )
    stage_id: Mapped[str | None] = mapped_column(String(255))
    payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    session: Mapped[MissionSession] = relationship(back_populates="events")
