"""add_membership_type_and_payment_tracking

Revision ID: 76ceffea5475
Revises: 7347717de84b
Create Date: 2026-01-07 17:39:06.850779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76ceffea5475'
down_revision = '7347717de84b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('member', schema=None) as batch_op:
        # Add membership_type field: 'full' (can reserve) or 'sustaining' (no access)
        batch_op.add_column(sa.Column('membership_type', sa.String(length=20), nullable=False, server_default='full'))
        # Add fee_paid field to track annual membership payment
        batch_op.add_column(sa.Column('fee_paid', sa.Boolean(), nullable=False, server_default='0'))
        # Track when fee was marked as paid
        batch_op.add_column(sa.Column('fee_paid_date', sa.Date(), nullable=True))
        # Track who marked the fee as paid
        batch_op.add_column(sa.Column('fee_paid_by_id', sa.Integer(), nullable=True))
        # Add foreign key for fee_paid_by
        batch_op.create_foreign_key('fk_member_fee_paid_by', 'member', ['fee_paid_by_id'], ['id'])
        # Add indexes for efficient queries
        batch_op.create_index('idx_member_membership_type', ['membership_type'], unique=False)
        batch_op.create_index('idx_member_fee_paid', ['fee_paid'], unique=False)


def downgrade():
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.drop_index('idx_member_fee_paid')
        batch_op.drop_index('idx_member_membership_type')
        batch_op.drop_constraint('fk_member_fee_paid_by', type_='foreignkey')
        batch_op.drop_column('fee_paid_by_id')
        batch_op.drop_column('fee_paid_date')
        batch_op.drop_column('fee_paid')
        batch_op.drop_column('membership_type')
