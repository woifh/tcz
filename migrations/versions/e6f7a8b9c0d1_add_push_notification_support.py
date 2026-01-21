"""Add push notification support

Revision ID: e6f7a8b9c0d1
Revises: d5e6f7a8b9c0
Create Date: 2026-01-21

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6f7a8b9c0d1'
down_revision = 'd5e6f7a8b9c0'
branch_labels = None
depends_on = None


def upgrade():
    # Add push notification preference columns to member table
    op.add_column('member', sa.Column('push_notifications_enabled', sa.Boolean(), nullable=False, server_default='1'))
    op.add_column('member', sa.Column('push_notify_own_bookings', sa.Boolean(), nullable=False, server_default='1'))
    op.add_column('member', sa.Column('push_notify_other_bookings', sa.Boolean(), nullable=False, server_default='1'))
    op.add_column('member', sa.Column('push_notify_court_blocked', sa.Boolean(), nullable=False, server_default='1'))
    op.add_column('member', sa.Column('push_notify_booking_overridden', sa.Boolean(), nullable=False, server_default='1'))

    # Create device_token table
    op.create_table('device_token',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.String(length=36), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('platform', sa.String(length=20), nullable=False, server_default='ios'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['member.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index('idx_device_token_member', 'device_token', ['member_id'], unique=False)


def downgrade():
    op.drop_index('idx_device_token_member', table_name='device_token')
    op.drop_table('device_token')
    op.drop_column('member', 'push_notify_booking_overridden')
    op.drop_column('member', 'push_notify_court_blocked')
    op.drop_column('member', 'push_notify_other_bookings')
    op.drop_column('member', 'push_notify_own_bookings')
    op.drop_column('member', 'push_notifications_enabled')
