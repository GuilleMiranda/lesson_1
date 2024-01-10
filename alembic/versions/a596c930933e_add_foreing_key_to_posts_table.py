"""add foreing key to posts table

Revision ID: a596c930933e
Revises: 0d50712f2182
Create Date: 2024-01-08 20:59:58.532733

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a596c930933e"
down_revision: Union[str, None] = "0d50712f2182"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_user_id_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["user_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("posts_user_id_fk", table_name="posts")
    op.drop_column("posts", "user_id")
