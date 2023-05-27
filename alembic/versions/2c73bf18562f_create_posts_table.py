"""create posts table

Revision ID: 2c73bf18562f
Revises: 
Create Date: 2023-05-27 15:28:14.071351

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = "2c73bf18562f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("title", sa.String, nullable=False),
        sa.Column("content", sa.String, nullable=False),
        sa.Column("published", sa.Boolean, server_default="TRUE", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("now()"),
        ),
    )


def downgrade():
    op.drop_table("posts")
