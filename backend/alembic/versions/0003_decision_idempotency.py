"""Add idempotency keys to mission decisions."""

import sqlalchemy as sa
from alembic import op

revision = "0003_decision_idempotency"
down_revision = "0002_mission_engine"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("mission_decisions", sa.Column("idempotency_key", sa.String(255)), schema="efs")
    op.add_column("mission_decisions", sa.Column("request_hash", sa.String(64)), schema="efs")
    op.execute("UPDATE efs.mission_decisions SET idempotency_key = id::text, request_hash = ''")
    op.alter_column("mission_decisions", "idempotency_key", nullable=False, schema="efs")
    op.alter_column("mission_decisions", "request_hash", nullable=False, schema="efs")
    op.create_unique_constraint(
        "uq_efs_decision_idempotency", "mission_decisions",
        ["session_id", "learner_id", "idempotency_key"], schema="efs",
    )


def downgrade() -> None:
    op.drop_constraint("uq_efs_decision_idempotency", "mission_decisions", schema="efs")
    op.drop_column("mission_decisions", "request_hash", schema="efs")
    op.drop_column("mission_decisions", "idempotency_key", schema="efs")
