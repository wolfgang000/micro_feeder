"""initial migration

Revision ID: cd278dcdbb2c
Revises: 
Create Date: 2023-07-07 17:54:49.265770

"""
from alembic import op
import sqlalchemy as sa
import migrations.helper as helper


# revision identifiers, used by Alembic.
revision = "cd278dcdbb2c"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/up/U_cd278dcdbb2c_initial_migration.sql",
    )


def downgrade() -> None:
    helper.exec_sql(
        op.get_bind(),
        "migrations/sql/down/D_cd278dcdbb2c_initial_migration.sql",
    )
