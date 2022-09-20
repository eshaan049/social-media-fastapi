"""add foreign-key to posts table

Revision ID: 817f218b711e
Revises: 5549d40b4155
Create Date: 2022-09-19 01:06:31.672546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '817f218b711e'
down_revision = '5549d40b4155'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users.fk", table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
