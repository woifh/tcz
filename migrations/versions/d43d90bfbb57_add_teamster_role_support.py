"""add_teamster_role_support

This migration adds support for the 'teamster' role to the Tennis Club system.

The teamster role is an intermediate permission level between 'member' and 'administrator',
specifically focused on court blocking capabilities for team management.

No schema changes are required - the existing VARCHAR(20) role column already
supports the 'teamster' value. This migration adds a constraint to validate
the role values.

Revision ID: d43d90bfbb57
Revises: f1g2h3i4j5k6
Create Date: 2026-01-06 20:22:26.626684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd43d90bfbb57'
down_revision = 'f1g2h3i4j5k6'
branch_labels = None
depends_on = None


def upgrade():
    """
    Add teamster role support.

    Creates a check constraint to validate role values are one of:
    'member', 'teamster', or 'administrator'.
    """
    # Add check constraint for valid role values
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.create_check_constraint(
            'member_role_check',
            "role IN ('member', 'teamster', 'administrator')"
        )


def downgrade():
    """
    Remove teamster role support.

    Drops the role check constraint.
    Note: Any members with 'teamster' role should be updated to 'member'
    before running this downgrade.
    """
    # Remove check constraint
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.drop_constraint('member_role_check', type_='check')
