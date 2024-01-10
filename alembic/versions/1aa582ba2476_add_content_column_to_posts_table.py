"""add content column to posts table

Revision ID: 1aa582ba2476
Revises: d416a5718470
Create Date: 2024-01-08 20:47:53.356662

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1aa582ba2476'
down_revision: Union[str, None] = 'd416a5718470'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
