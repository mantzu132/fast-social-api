"""create users table

Revision ID: 2c149520cc38
Revises: 2c73bf18562f
Create Date: 2023-05-27 16:07:56.412771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2c149520cc38"
down_revision = "2c73bf18562f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("password", sa.String, nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("now()"),
        ),
    )


def downgrade():
    op.drop_table("users")
