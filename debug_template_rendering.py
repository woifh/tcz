#!/usr/bin/env python3
"""Debug script to test template rendering with batch_id."""

import sys
sys.path.append('.')
from app import create_app, db
from app.models import Block
from flask import render_template_string

app = create_app()

with app.app_context():
    # Get the first block with batch_id
    block = Block.query.filter(Block.batch_id.isnot(None)).first()
    
    if not block:
        print("No blocks with batch_id found")
        sys.exit(1)
    
    print(f"Found block: ID={block.id}, batch_id={block.batch_id}")
    
    # Simulate the backend route logic
    actual_batch_id = block.batch_id
    blocks = Block.query.filter_by(batch_id=actual_batch_id).all()
    primary_block = blocks[0]
    court_ids = [block.court_id for block in blocks]
    
    edit_block_data = {
        'id': primary_block.id,
        'batch_id': actual_batch_id,  # This should be the actual batch_id
        'court_ids': court_ids,
        'date': primary_block.date,
        'start_time': primary_block.start_time,
        'end_time': primary_block.end_time,
        'reason_id': primary_block.reason_id,
        'sub_reason': primary_block.sub_reason,
        'created_by': primary_block.created_by,
        'created_at': primary_block.created_at,
        'related_block_ids': [block.id for block in blocks]
    }
    
    print(f"edit_block_data = {edit_block_data}")
    
    # Test template rendering
    template_snippet = '''
    <form data-batch-id="{{ edit_block_data.batch_id if edit_block_data else '' }}">
        Batch ID: {{ edit_block_data.batch_id if edit_block_data else 'None' }}
    </form>
    '''
    
    rendered = render_template_string(template_snippet, edit_block_data=edit_block_data)
    print(f"Rendered template:\n{rendered}")