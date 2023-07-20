"""add feed_last_fetched_at

Revision ID: 0c9bb5aa4e4f
Revises: d517c4fcd82b
Create Date: 2023-07-20 14:03:07.250312

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "0c9bb5aa4e4f"
down_revision = "d517c4fcd82b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE subscription ADD COLUMN feed_last_fetched_at timestamp(0) NOT NULL DEFAULT NOW();
            """
        )
    )


def downgrade() -> None:
    pass
