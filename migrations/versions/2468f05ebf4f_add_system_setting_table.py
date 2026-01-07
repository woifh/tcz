"""add system setting table

Revision ID: 2468f05ebf4f
Revises: 76ceffea5475
Create Date: 2026-01-07 17:50:22.568721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2468f05ebf4f'
down_revision = '76ceffea5475'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('system_setting',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('key', sa.String(length=100), nullable=False),
        sa.Column('value', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_system_setting_key', 'system_setting', ['key'], unique=True)


def downgrade():
    op.drop_index('ix_system_setting_key', table_name='system_setting')
    op.drop_table('system_setting')
