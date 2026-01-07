"""Add reason_audit_log table

Revision ID: e9f967e22487
Revises: 90886bac5240
Create Date: 2026-01-07 21:52:43.892002

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9f967e22487'
down_revision = '90886bac5240'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('reason_audit_log',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('operation', sa.String(length=20), nullable=False),
        sa.Column('operation_data', sa.JSON(), nullable=True),
        sa.Column('performed_by_id', sa.Integer(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['performed_by_id'], ['member.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_reason_audit_timestamp', 'reason_audit_log', ['timestamp'], unique=False)
    op.create_index('idx_reason_audit_admin', 'reason_audit_log', ['performed_by_id'], unique=False)
    op.create_index('idx_reason_audit_operation', 'reason_audit_log', ['operation'], unique=False)
    op.create_index('idx_reason_audit_reason', 'reason_audit_log', ['reason_id'], unique=False)


def downgrade():
    op.drop_index('idx_reason_audit_reason', table_name='reason_audit_log')
    op.drop_index('idx_reason_audit_operation', table_name='reason_audit_log')
    op.drop_index('idx_reason_audit_admin', table_name='reason_audit_log')
    op.drop_index('idx_reason_audit_timestamp', table_name='reason_audit_log')
    op.drop_table('reason_audit_log')
