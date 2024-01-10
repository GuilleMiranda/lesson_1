"""create post table

Revision ID: d416a5718470
Revises: 
Create Date: 2024-01-08 20:35:21.263924

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd416a5718470'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts",
                    sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False),
                   )


def downgrade() -> None:
    op.drop_table(table_name="posts")
