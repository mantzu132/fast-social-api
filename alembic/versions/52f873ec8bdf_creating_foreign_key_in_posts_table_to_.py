"""creating foreign key in posts table to id in users

Revision ID: 52f873ec8bdf
Revises: 2c149520cc38
Create Date: 2023-05-27 16:38:31.404693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52f873ec8bdf"
down_revision = "2c149520cc38"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("user_id", sa.Integer, nullable=False))

    op.create_foreign_key(None, "posts", "users", ["user_id"], ["id"])


def downgrade():
    op.drop_constraint(None, "posts", type_="foreignkey")

    op.drop_column("posts", "user_id")
