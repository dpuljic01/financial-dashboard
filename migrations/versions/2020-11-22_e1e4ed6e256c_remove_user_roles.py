"""remove user roles

Revision ID: e1e4ed6e256c
Revises: 7f12bc9c084b
Create Date: 2020-11-22 14:52:10.614611

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e1e4ed6e256c'
down_revision = '7f12bc9c084b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_roles')
    op.drop_table('roles')
    op.add_column('users', sa.Column('role', sa.String(length=100), server_default='user', nullable=True))
    op.alter_column('users', 'password',
               existing_type=postgresql.BYTEA(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'password',
               existing_type=postgresql.BYTEA(),
               nullable=True)
    op.drop_column('users', 'role')
    op.create_table('user_roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='user_roles_role_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_roles_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='user_roles_pkey')
    )
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='roles_pkey'),
    sa.UniqueConstraint('name', name='uq_roles_name')
    )
    # ### end Alembic commands ###
