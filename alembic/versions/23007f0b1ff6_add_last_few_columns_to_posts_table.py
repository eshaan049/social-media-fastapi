"""add last few columns to posts table

Revision ID: 23007f0b1ff6
Revises: 817f218b711e
Create Date: 2022-09-19 01:19:39.367137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23007f0b1ff6'
down_revision = '817f218b711e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
