"""create user table

Revision ID: 5a6b4b830fac
Revises: e7b3a877b1db
Create Date: 2023-06-26 15:09:19.115341

"""
from alembic import op
import sqlalchemy as sa
import migrations.helper as helper


# revision identifiers, used by Alembic.
revision = "5a6b4b830fac"
down_revision = "e7b3a877b1db"
branch_labels = None
depends_on = None


def upgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/up/U_5a6b4b830fac_create_user_table.sql",
    )


def downgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/up/U_5a6b4b830fac_create_user_table.sql",
    )
