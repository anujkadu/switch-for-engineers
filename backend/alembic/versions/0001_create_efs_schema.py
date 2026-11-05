"""Create the isolated EFS schema."""
from alembic import op

revision = "0001_create_efs_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA IF NOT EXISTS efs")


def downgrade() -> None:
    # The schema may predate this migration or contain objects from later
    # migrations. Never drop the shared EFS schema during a single revision's
    # downgrade; schema lifecycle is managed separately from revision rollback.
    pass
