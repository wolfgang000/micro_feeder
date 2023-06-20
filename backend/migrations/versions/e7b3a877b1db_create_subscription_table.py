"""create subscription table

Revision ID: e7b3a877b1db
Revises: 
Create Date: 2023-06-19 19:57:37.185699

"""
from alembic import op
import sqlalchemy as sa
import migrations.helper as helper


# revision identifiers, used by Alembic.
revision = "e7b3a877b1db"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/up/U_e7b3a877b1db_create_subscription_table.sql",
    )


def downgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/down/D_e7b3a877b1db_create_subscription_table.sql",
    )
