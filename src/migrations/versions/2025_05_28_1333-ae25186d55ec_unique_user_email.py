"""unique user email

Revision ID: ae25186d55ec
Revises: c80dcb224e3e
Create Date: 2025-05-28 13:33:44.130421

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ae25186d55ec"
down_revision: Union[str, None] = "c80dcb224e3e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
