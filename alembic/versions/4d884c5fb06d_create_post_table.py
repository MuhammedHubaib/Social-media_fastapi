"""create post table

Revision ID: 4d884c5fb06d
Revises: 
Create Date: 2023-11-16 12:57:21.384847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4d884c5fb06d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False),
                    )
    pass
    


def downgrade():
    
    op.drop_table('posts')
    
    pass
