"""add content column to posts table

Revision ID: 9968bb780caf
Revises: bcc6ec3cacca
Create Date: 2022-09-19 00:41:49.768043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9968bb780caf'
down_revision = 'bcc6ec3cacca'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass



def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
