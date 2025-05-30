"""add users

Revision ID: c80dcb224e3e
Revises: 2b371765b7e0
Create Date: 2025-05-28 09:03:58.459169

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c80dcb224e3e"
down_revision: Union[str, None] = "2b371765b7e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
