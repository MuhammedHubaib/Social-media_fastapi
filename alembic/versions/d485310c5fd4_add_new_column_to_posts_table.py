"""add new column to posts table

Revision ID: d485310c5fd4
Revises: 4d884c5fb06d
Create Date: 2023-11-16 13:24:03.438555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd485310c5fd4'
down_revision: Union[str, None] = '4d884c5fb06d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content',sa.String(),nullable=False)
    )
    pass


def downgrade():
    
    op.drop_column('posts','content')
    pass
