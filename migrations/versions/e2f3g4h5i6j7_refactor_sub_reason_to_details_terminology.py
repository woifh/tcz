"""Refactor sub_reason to details terminology

Revision ID: e2f3g4h5i6j7
Revises: 4acdcc39bec3
Create Date: 2025-01-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e2f3g4h5i6j7'
down_revision = '4acdcc39bec3'
branch_labels = None
depends_on = None


def upgrade():
    """
    Create database tables from scratch with details terminology.
    
    This migration:
    1. Drops existing tables with sub_reason terminology
    2. Creates new tables with details terminology
    3. Preserves existing data by backing up and restoring
    4. Updates all foreign key constraints and indexes
    """
    
    # Step 1: Backup existing data
    print("Backing up existing data...")
    
    # Backup block data
    op.execute("""
        CREATE TEMPORARY TABLE block_backup AS 
        SELECT id, court_id, date, start_time, end_time, reason_id, 
               sub_reason as details, series_id, batch_id, is_modified, 
               created_by_id, created_at 
        FROM block
    """)
    
    # Backup block_series data
    op.execute("""
        CREATE TEMPORARY TABLE block_series_backup AS 
        SELECT id, name, start_date, end_date, start_time, end_time, 
               recurrence_pattern, recurrence_days, reason_id, 
               sub_reason as details, created_by_id, created_at 
        FROM block_series
    """)
    
    # Backup block_template data
    op.execute("""
        CREATE TEMPORARY TABLE block_template_backup AS 
        SELECT id, name, court_selection, start_time, end_time, reason_id, 
               sub_reason as details, recurrence_pattern, recurrence_days, 
               created_by_id, created_at 
        FROM block_template
    """)
    
    # Backup sub_reason_template data
    op.execute("""
        CREATE TEMPORARY TABLE details_template_backup AS 
        SELECT id, reason_id, template_name, created_by_id, created_at 
        FROM sub_reason_template
    """)
    
    # Step 2: Drop existing tables
    print("Dropping existing tables...")
    op.drop_table('block')
    op.drop_table('block_series')
    op.drop_table('block_template')
    op.drop_table('sub_reason_template')
    
    # Step 3: Create new tables with details terminology
    print("Creating new tables with details terminology...")
    
    # Create block table with details column
    op.create_table('block',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('court_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('details', sa.String(length=255), nullable=True),
        sa.Column('series_id', sa.Integer(), nullable=True),
        sa.Column('batch_id', sa.String(length=36), nullable=True),
        sa.Column('is_modified', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['court_id'], ['court.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id']),
        sa.ForeignKeyConstraint(['series_id'], ['block_series.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create block_series table with details column
    op.create_table('block_series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('recurrence_pattern', sa.String(length=20), nullable=False),
        sa.Column('recurrence_days', sa.JSON(), nullable=True),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('details', sa.String(length=255), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create block_template table with details column
    op.create_table('block_template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('court_selection', sa.JSON(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('details', sa.String(length=255), nullable=True),
        sa.Column('recurrence_pattern', sa.String(length=20), nullable=True),
        sa.Column('recurrence_days', sa.JSON(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create details_template table (renamed from sub_reason_template)
    op.create_table('details_template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('template_name', sa.String(length=100), nullable=False),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Step 4: Create indexes
    print("Creating indexes...")
    
    # Block table indexes
    with op.batch_alter_table('block', schema=None) as batch_op:
        batch_op.create_index('idx_block_date', ['date'], unique=False)
        batch_op.create_index('idx_block_court_date', ['court_id', 'date'], unique=False)
        batch_op.create_index('idx_block_series', ['series_id'], unique=False)
        batch_op.create_index('idx_block_reason', ['reason_id'], unique=False)
        batch_op.create_index('idx_block_batch', ['batch_id'], unique=False)
        batch_op.create_index('ix_block_batch_id', ['batch_id'], unique=False)
    
    # Block_series table indexes
    with op.batch_alter_table('block_series', schema=None) as batch_op:
        batch_op.create_index('idx_block_series_dates', ['start_date', 'end_date'], unique=False)
        batch_op.create_index('idx_block_series_reason', ['reason_id'], unique=False)
    
    # Block_template table indexes
    with op.batch_alter_table('block_template', schema=None) as batch_op:
        batch_op.create_index('idx_block_template_name', ['name'], unique=False)
        batch_op.create_index('idx_block_template_reason', ['reason_id'], unique=False)
    
    # Details_template table indexes
    with op.batch_alter_table('details_template', schema=None) as batch_op:
        batch_op.create_index('idx_details_template_reason', ['reason_id'], unique=False)
    
    # Step 5: Restore data from backups
    print("Restoring data from backups...")
    
    # Restore block data
    op.execute("""
        INSERT INTO block (id, court_id, date, start_time, end_time, reason_id, 
                          details, series_id, batch_id, is_modified, created_by_id, created_at)
        SELECT id, court_id, date, start_time, end_time, reason_id, 
               details, series_id, batch_id, is_modified, created_by_id, created_at
        FROM block_backup
    """)
    
    # Restore block_series data
    op.execute("""
        INSERT INTO block_series (id, name, start_date, end_date, start_time, end_time, 
                                 recurrence_pattern, recurrence_days, reason_id, details, 
                                 created_by_id, created_at)
        SELECT id, name, start_date, end_date, start_time, end_time, 
               recurrence_pattern, recurrence_days, reason_id, details, 
               created_by_id, created_at
        FROM block_series_backup
    """)
    
    # Restore block_template data
    op.execute("""
        INSERT INTO block_template (id, name, court_selection, start_time, end_time, reason_id, 
                                   details, recurrence_pattern, recurrence_days, created_by_id, created_at)
        SELECT id, name, court_selection, start_time, end_time, reason_id, 
               details, recurrence_pattern, recurrence_days, created_by_id, created_at
        FROM block_template_backup
    """)
    
    # Restore details_template data
    op.execute("""
        INSERT INTO details_template (id, reason_id, template_name, created_by_id, created_at)
        SELECT id, reason_id, template_name, created_by_id, created_at
        FROM details_template_backup
    """)
    
    # Step 6: Clean up temporary tables
    print("Cleaning up temporary tables...")
    op.execute("DROP TABLE block_backup")
    op.execute("DROP TABLE block_series_backup")
    op.execute("DROP TABLE block_template_backup")
    op.execute("DROP TABLE details_template_backup")
    
    print("Migration completed successfully:")
    print("- Created new tables with details terminology")
    print("- Preserved all existing data")
    print("- Updated all indexes and foreign key relationships")
    print("- Removed old tables with sub_reason terminology")


def downgrade():
    """
    Rollback the details terminology to sub_reason by recreating tables.
    
    This rollback:
    1. Backs up existing data from details tables
    2. Drops details tables and recreates sub_reason tables
    3. Restores all existing data during the rollback
    4. Restores original foreign key constraints and indexes
    """
    
    # Step 1: Backup existing data
    print("Backing up existing data...")
    
    # Backup block data
    op.execute("""
        CREATE TEMPORARY TABLE block_backup AS 
        SELECT id, court_id, date, start_time, end_time, reason_id, 
               details as sub_reason, series_id, batch_id, is_modified, 
               created_by_id, created_at 
        FROM block
    """)
    
    # Backup block_series data
    op.execute("""
        CREATE TEMPORARY TABLE block_series_backup AS 
        SELECT id, name, start_date, end_date, start_time, end_time, 
               recurrence_pattern, recurrence_days, reason_id, 
               details as sub_reason, created_by_id, created_at 
        FROM block_series
    """)
    
    # Backup block_template data
    op.execute("""
        CREATE TEMPORARY TABLE block_template_backup AS 
        SELECT id, name, court_selection, start_time, end_time, reason_id, 
               details as sub_reason, recurrence_pattern, recurrence_days, 
               created_by_id, created_at 
        FROM block_template
    """)
    
    # Backup details_template data
    op.execute("""
        CREATE TEMPORARY TABLE sub_reason_template_backup AS 
        SELECT id, reason_id, template_name, created_by_id, created_at 
        FROM details_template
    """)
    
    # Step 2: Drop existing tables
    print("Dropping existing tables...")
    op.drop_table('block')
    op.drop_table('block_series')
    op.drop_table('block_template')
    op.drop_table('details_template')
    
    # Step 3: Create original tables with sub_reason terminology
    print("Creating original tables with sub_reason terminology...")
    
    # Create block table with sub_reason column
    op.create_table('block',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('court_id', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('sub_reason', sa.String(length=255), nullable=True),
        sa.Column('series_id', sa.Integer(), nullable=True),
        sa.Column('batch_id', sa.String(length=36), nullable=True),
        sa.Column('is_modified', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['court_id'], ['court.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id']),
        sa.ForeignKeyConstraint(['series_id'], ['block_series.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create block_series table with sub_reason column
    op.create_table('block_series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('recurrence_pattern', sa.String(length=20), nullable=False),
        sa.Column('recurrence_days', sa.JSON(), nullable=True),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('sub_reason', sa.String(length=255), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create block_template table with sub_reason column
    op.create_table('block_template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('court_selection', sa.JSON(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('sub_reason', sa.String(length=255), nullable=True),
        sa.Column('recurrence_pattern', sa.String(length=20), nullable=True),
        sa.Column('recurrence_days', sa.JSON(), nullable=True),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    
    # Create sub_reason_template table
    op.create_table('sub_reason_template',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reason_id', sa.Integer(), nullable=False),
        sa.Column('template_name', sa.String(length=100), nullable=False),
        sa.Column('created_by_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['created_by_id'], ['member.id']),
        sa.ForeignKeyConstraint(['reason_id'], ['block_reason.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Step 4: Create original indexes
    print("Creating original indexes...")
    
    # Block table indexes
    with op.batch_alter_table('block', schema=None) as batch_op:
        batch_op.create_index('idx_block_date', ['date'], unique=False)
        batch_op.create_index('idx_block_court_date', ['court_id', 'date'], unique=False)
        batch_op.create_index('idx_block_series', ['series_id'], unique=False)
        batch_op.create_index('idx_block_reason', ['reason_id'], unique=False)
        batch_op.create_index('idx_block_batch', ['batch_id'], unique=False)
        batch_op.create_index('ix_block_batch_id', ['batch_id'], unique=False)
    
    # Block_series table indexes
    with op.batch_alter_table('block_series', schema=None) as batch_op:
        batch_op.create_index('idx_block_series_dates', ['start_date', 'end_date'], unique=False)
        batch_op.create_index('idx_block_series_reason', ['reason_id'], unique=False)
    
    # Block_template table indexes
    with op.batch_alter_table('block_template', schema=None) as batch_op:
        batch_op.create_index('idx_block_template_name', ['name'], unique=False)
        batch_op.create_index('idx_block_template_reason', ['reason_id'], unique=False)
    
    # Sub_reason_template table indexes
    with op.batch_alter_table('sub_reason_template', schema=None) as batch_op:
        batch_op.create_index('idx_sub_reason_template_reason', ['reason_id'], unique=False)
    
    # Step 5: Restore data from backups
    print("Restoring data from backups...")
    
    # Restore block data
    op.execute("""
        INSERT INTO block (id, court_id, date, start_time, end_time, reason_id, 
                          sub_reason, series_id, batch_id, is_modified, created_by_id, created_at)
        SELECT id, court_id, date, start_time, end_time, reason_id, 
               sub_reason, series_id, batch_id, is_modified, created_by_id, created_at
        FROM block_backup
    """)
    
    # Restore block_series data
    op.execute("""
        INSERT INTO block_series (id, name, start_date, end_date, start_time, end_time, 
                                 recurrence_pattern, recurrence_days, reason_id, sub_reason, 
                                 created_by_id, created_at)
        SELECT id, name, start_date, end_date, start_time, end_time, 
               recurrence_pattern, recurrence_days, reason_id, sub_reason, 
               created_by_id, created_at
        FROM block_series_backup
    """)
    
    # Restore block_template data
    op.execute("""
        INSERT INTO block_template (id, name, court_selection, start_time, end_time, reason_id, 
                                   sub_reason, recurrence_pattern, recurrence_days, created_by_id, created_at)
        SELECT id, name, court_selection, start_time, end_time, reason_id, 
               sub_reason, recurrence_pattern, recurrence_days, created_by_id, created_at
        FROM block_template_backup
    """)
    
    # Restore sub_reason_template data
    op.execute("""
        INSERT INTO sub_reason_template (id, reason_id, template_name, created_by_id, created_at)
        SELECT id, reason_id, template_name, created_by_id, created_at
        FROM sub_reason_template_backup
    """)
    
    # Step 6: Clean up temporary tables
    print("Cleaning up temporary tables...")
    op.execute("DROP TABLE block_backup")
    op.execute("DROP TABLE block_series_backup")
    op.execute("DROP TABLE block_template_backup")
    op.execute("DROP TABLE sub_reason_template_backup")
    
    print("Rollback completed successfully:")
    print("- Recreated original tables with sub_reason terminology")
    print("- Preserved all existing data")
    print("- Restored original indexes and foreign key relationships")
    print("- Removed tables with details terminology")