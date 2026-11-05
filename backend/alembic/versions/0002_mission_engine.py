"""Create mission engine persistence tables."""

from alembic import op

revision = "0002_mission_engine"
down_revision = "0001_create_efs_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE efs.session_status AS ENUM ('active', 'completed', 'abandoned')")
    op.execute(
        "CREATE TYPE efs.event_type AS ENUM ("
        "'mission_started', 'decision_submitted', 'stage_advanced', "
        "'mission_completed', 'mission_abandoned')"
    )
    op.execute("""
        CREATE TABLE efs.mission_sessions (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            learner_id varchar(255) NOT NULL,
            mission_id varchar(255) NOT NULL,
            mission_version varchar(64) NOT NULL,
            current_stage_id varchar(255) NOT NULL,
            status efs.session_status NOT NULL,
            started_at timestamptz NOT NULL DEFAULT now(),
            completed_at timestamptz,
            abandoned_at timestamptz,
            created_at timestamptz NOT NULL DEFAULT now(),
            updated_at timestamptz NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE UNIQUE INDEX uq_efs_active_mission_session
        ON efs.mission_sessions (learner_id, mission_id, mission_version)
        WHERE status = 'active'
    """)
    op.execute("""
        CREATE TABLE efs.mission_decisions (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id uuid NOT NULL REFERENCES efs.mission_sessions(id) ON DELETE CASCADE,
            learner_id varchar(255) NOT NULL,
            stage_id varchar(255) NOT NULL,
            content jsonb NOT NULL,
            submitted_at timestamptz NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE TABLE efs.mission_events (
            id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
            session_id uuid NOT NULL REFERENCES efs.mission_sessions(id) ON DELETE CASCADE,
            learner_id varchar(255) NOT NULL,
            event_type efs.event_type NOT NULL,
            stage_id varchar(255),
            payload jsonb NOT NULL DEFAULT '{}'::jsonb,
            created_at timestamptz NOT NULL DEFAULT now()
        )
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS efs.mission_events")
    op.execute("DROP TABLE IF EXISTS efs.mission_decisions")
    op.execute("DROP INDEX IF EXISTS efs.uq_efs_active_mission_session")
    op.execute("DROP TABLE IF EXISTS efs.mission_sessions")
    op.execute("DROP TYPE IF EXISTS efs.event_type")
    op.execute("DROP TYPE IF EXISTS efs.session_status")
