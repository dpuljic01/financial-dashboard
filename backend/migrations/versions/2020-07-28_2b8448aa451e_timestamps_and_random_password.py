"""timestamps and random password

Revision ID: 2b8448aa451e
Revises: 93e48ab4b966
Create Date: 2020-07-28 23:25:26.245872

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2b8448aa451e'
down_revision = '93e48ab4b966'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('portfolio', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('portfolio', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.add_column('stocks', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('stocks', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.alter_column('users', 'password',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.add_column('users', sa.Column('last_logged_in', sa.DateTime(), nullable=True))
    op.add_column('portfolio', sa.Column('info', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('portfolio', 'info')
    op.drop_column('users', 'last_logged_in')
    op.alter_column('users', 'password',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    op.drop_column('stocks', 'updated_at')
    op.drop_column('stocks', 'created_at')
    op.drop_column('portfolio', 'updated_at')
    op.drop_column('portfolio', 'created_at')
    # ### end Alembic commands ###
