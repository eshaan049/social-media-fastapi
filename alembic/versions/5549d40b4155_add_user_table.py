"""add user table

Revision ID: 5549d40b4155
Revises: 9968bb780caf
Create Date: 2022-09-19 00:53:22.719827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5549d40b4155'
down_revision = '9968bb780caf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass

def downgrade() -> None:
    op.drop_table('users')
    pass
