"""add feed_last_etag to subscription

Revision ID: 581fb18ec960
Revises: cd278dcdbb2c
Create Date: 2023-07-14 18:33:02.638556

"""
from alembic import op
import sqlalchemy as sa
import migrations.helper as helper


# revision identifiers, used by Alembic.
revision = "581fb18ec960"
down_revision = "cd278dcdbb2c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/up/U_581fb18ec960_add_feed_last_etag_to_subscription.sql",
    )


def downgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/up/D_581fb18ec960_add_feed_last_etag_to_subscription.sql",
    )
