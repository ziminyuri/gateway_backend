"""empty message

Revision ID: d7e3902ce748
Revises: 
Create Date: 2022-05-11 10:06:21.806222

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd7e3902ce748'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('auth_history',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('login_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_agent', sa.String(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('device_type', sa.String(length=10), nullable=False),
    sa.Column('ip_address', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id', 'device_type')
    )
    op.create_table('permission_role',
    sa.Column('permission_id', sa.Integer(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('permission_id', 'role_id')
    )
    op.create_table('profile',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=False),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('phone'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('social_account',
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('social_name', sa.String(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('totp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('secret', sa.String(), nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('secret'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('user_role',
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('totp')
    op.drop_table('social_account')
    op.drop_table('profile')
    op.drop_table('permission_role')
    op.drop_table('auth_history')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('permission')
    # ### end Alembic commands ###
