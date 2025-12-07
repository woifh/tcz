"""add_index_on_member_name

Revision ID: ccc33b628ab6
Revises: a38dd0c89b2f
Create Date: 2025-12-06 18:56:15.069057

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ccc33b628ab6'
down_revision = 'a38dd0c89b2f'
branch_labels = None
depends_on = None


def upgrade():
    # Add index on member.name for search performance
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.create_index('idx_member_name', ['name'], unique=False)


def downgrade():
    # Remove index on member.name
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.drop_index('idx_member_name')
