"""add few more column tables

Revision ID: f18d37d858d2
Revises: 14c9f242a992
Create Date: 2023-11-16 14:11:55.456577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f18d37d858d2'
down_revision: Union[str, None] = '14c9f242a992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('published',sa.Boolean,server_default=sa.text('True'),nullable=False))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','creatde_at')
    pass
