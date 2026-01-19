"""Add temporary block support

Adds is_temporary flag to BlockReason for non-destructive blocking.
Adds suspended_by_block_id to Reservation for tracking suspended reservations.

Revision ID: c3d4e5f6a7b8
Revises: a1b2c3d4e5f6
Create Date: 2026-01-19

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d4e5f6a7b8'
down_revision = 'a1b2c3d4e5f6'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_temporary flag to block_reason table
    with op.batch_alter_table('block_reason', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_temporary', sa.Boolean(), nullable=False, server_default='0'))

    # Add suspended_by_block_id to reservation table for tracking which block suspended it
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('suspended_by_block_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_reservation_suspended_by_block',
            'block',
            ['suspended_by_block_id'],
            ['id'],
            ondelete='SET NULL'
        )
        batch_op.create_index('idx_reservation_suspended_by_block', ['suspended_by_block_id'])


def downgrade():
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_index('idx_reservation_suspended_by_block')
        batch_op.drop_constraint('fk_reservation_suspended_by_block', type_='foreignkey')
        batch_op.drop_column('suspended_by_block_id')

    with op.batch_alter_table('block_reason', schema=None) as batch_op:
        batch_op.drop_column('is_temporary')
