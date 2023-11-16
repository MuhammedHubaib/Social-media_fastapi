"""add some more tables to posts inclueds fkey

Revision ID: 14c9f242a992
Revises: ab7282ffc88b
Create Date: 2023-11-16 13:47:15.087196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14c9f242a992'
down_revision: Union[str, None] = 'ab7282ffc88b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fkey',source_table='posts',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
