"""add user avatar

Revision ID: a4f2c9d81b3e
Revises: e1e4ed6e256c
Create Date: 2026-08-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a4f2c9d81b3e'
down_revision = 'e1e4ed6e256c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('avatar', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('users', 'avatar')
