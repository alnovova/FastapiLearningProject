"""initial migration

Revision ID: 4aa980f58f7f
Revises: 
Create Date: 2025-05-24 19:42:02.341292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '4aa980f58f7f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('hotels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=100), nullable=False),
        sa.Column('location', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('hotels')
