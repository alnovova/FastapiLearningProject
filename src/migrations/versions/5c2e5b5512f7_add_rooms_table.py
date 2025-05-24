"""add rooms table

Revision ID: 5c2e5b5512f7
Revises: 4aa980f58f7f
Create Date: 2025-05-24 20:04:20.424164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '5c2e5b5512f7'
down_revision: Union[str, None] = '4aa980f58f7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hotel_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['hotel_id'], ['hotels.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('rooms')
