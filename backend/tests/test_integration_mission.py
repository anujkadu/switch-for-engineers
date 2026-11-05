import os
import threading
import uuid

import pytest
from efs.config import Settings
from efs.db import create_engine_for, create_session_factory
from efs.domain.errors import InvalidTransitionError, LearnerMismatchError, StageProgressionError
from efs.missions import SAMPLE_MISSION, MissionRegistry
from efs.persistence import EventType, MissionEvent, SessionStatus
from efs.services import MissionService
from sqlalchemy import select

pytestmark = pytest.mark.skipif(
    not os.getenv("EFS_TEST_DATABASE_URL"), reason="EFS_TEST_DATABASE_URL is not configured"
)


@pytest.fixture(scope="module")
def service():
    settings = Settings(
        database_url="postgresql+psycopg://integration-placeholder",
        test_database_url=os.environ["EFS_TEST_DATABASE_URL"],
    )
    engine = create_engine_for(settings, test=True)
    factory = create_session_factory(engine)
    yield MissionService(factory, MissionRegistry((SAMPLE_MISSION,)))
    engine.dispose()


def test_start_resume_and_concurrent_start(service):
    learner = f"learner-{uuid.uuid4()}"
    results = []

    def start():
        results.append(service.start_mission(learner, "phase2-sample", "1.0").id)

    threads = [threading.Thread(target=start) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len(results) == 2
    assert results[0] == results[1]


def test_decisions_progress_events_and_completion(service):
    learner = f"learner-{uuid.uuid4()}"
    item = service.start_mission(learner, "phase2-sample", "1.0")
    with pytest.raises(StageProgressionError):
        service.advance_stage(item.id, learner)
    service.submit_decision(item.id, learner, {"observation": "ok"})
    item = service.advance_stage(item.id, learner)
    service.submit_decision(item.id, learner, {"action": "done"})
    item = service.complete_mission(item.id, learner)
    assert item.status is SessionStatus.COMPLETED
    with service.sessions() as session:
        event_types = session.scalars(
            select(MissionEvent.event_type).where(MissionEvent.session_id == item.id)
        ).all()
    assert event_types == [
        EventType.MISSION_STARTED,
        EventType.DECISION_SUBMITTED,
        EventType.STAGE_ADVANCED,
        EventType.DECISION_SUBMITTED,
        EventType.MISSION_COMPLETED,
    ]


def test_ownership_and_failed_operations_leave_state_unchanged(service):
    learner = f"learner-{uuid.uuid4()}"
    item = service.start_mission(learner, "phase2-sample", "1.0")
    with pytest.raises(LearnerMismatchError):
        service.submit_decision(item.id, "other", {"bad": True})
    with service.sessions() as session:
        event = session.scalar(select(MissionEvent).where(MissionEvent.session_id == item.id))
        assert event.event_type is EventType.MISSION_STARTED
    service.abandon_mission(item.id, learner)
    with pytest.raises(InvalidTransitionError):
        service.submit_decision(item.id, learner, {"late": True})
