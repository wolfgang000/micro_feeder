"""add feed_last_modified to subscription

Revision ID: d517c4fcd82b
Revises: 581fb18ec960
Create Date: 2023-07-15 10:29:56.252286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = "d517c4fcd82b"
down_revision = "581fb18ec960"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()
    conn.execute(
        text(
            """
                ALTER TABLE subscription ADD COLUMN feed_last_modified text NULL;
            """
        )
    )


def downgrade() -> None:
    pass
