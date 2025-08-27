"""add content column to posts table

Revision ID: 46627fceb9d2
Revises: c6fc8c60419f
Create Date: 2025-08-24 12:25:09.748277

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '46627fceb9d2'
down_revision: Union[str, Sequence[str], None] = 'c6fc8c60419f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
