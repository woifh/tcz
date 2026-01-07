"""Remove orphaned tables from old implementation

Revision ID: 200629f86aa0
Revises: 7347717de84b
Create Date: 2026-01-07 12:29:46.559264

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '200629f86aa0'
down_revision = '7347717de84b'
branch_labels = None
depends_on = None


def upgrade():
    # Drop orphaned tables from old block template/series implementation
    # These tables are no longer referenced in the current models
    op.drop_table('block_series')
    op.drop_table('block_template')
    op.drop_table('details_template')


def downgrade():
    # Recreate tables if we need to roll back
    # Note: We don't recreate data, just the structure
    op.create_table('details_template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('block_template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('block_series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
