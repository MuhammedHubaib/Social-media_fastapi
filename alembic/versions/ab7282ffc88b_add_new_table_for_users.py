"""add new table for users

Revision ID: ab7282ffc88b
Revises: d485310c5fd4
Create Date: 2023-11-16 13:30:30.056141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab7282ffc88b'
down_revision: Union[str, None] = 'd485310c5fd4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'users',
            sa.Column('id',sa.Integer,primary_key= True,nullable= False),
            sa.Column('email',sa.String,unique=True,nullable=False),
            sa.Column('password',sa.String,nullable= False),
            sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
    )
    pass


def downgrade():
    op.drop_table('users')
    pass
