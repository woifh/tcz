#!/usr/bin/env python3
"""
Debug script to test just the data attribute rendering
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Block
from flask import render_template_string

def test_data_attribute_only():
    """Test just the data attribute rendering"""
    app = create_app()
    
    with app.app_context():
        # Get a block with a valid batch_id
        block = Block.query.filter(Block.batch_id.isnot(None)).first()
        
        if not block:
            print("❌ No blocks with batch_id found")
            return
        
        print(f"✅ Found block with batch_id: {block.batch_id}")
        
        # Create edit_block_data exactly as the route does
        edit_block_data = {
            'id': block.id,
            'batch_id': block.batch_id,  # This is the key field
            'court_ids': [block.court_id],
            'date': block.date,
            'start_time': block.start_time,
            'end_time': block.end_time,
            'reason_id': block.reason_id,
            'sub_reason': block.sub_reason,
            'created_by': block.created_by_id,
            'created_at': block.created_at,
            'related_block_ids': [block.id]
        }
        
        print(f"\n📊 edit_block_data:")
        print(f"   batch_id: '{edit_block_data['batch_id']}' (type: {type(edit_block_data['batch_id'])})")
        
        # Test the exact template condition from the HTML file
        template_condition = """
        {%- if edit_block_data and edit_block_data.batch_id and edit_block_data.batch_id != 'None' and edit_block_data.batch_id != 'null' -%}
        {{ edit_block_data.batch_id }}
        {%- else -%}
        EMPTY
        {%- endif -%}
        """
        
        try:
            result = render_template_string(template_condition, edit_block_data=edit_block_data)
            print(f"\n🔍 Template condition result: '{result.strip()}'")
            
            # Test each part of the condition
            print(f"\n🧪 Condition breakdown:")
            print(f"   edit_block_data exists: {edit_block_data is not None}")
            print(f"   edit_block_data.batch_id exists: {'batch_id' in edit_block_data and edit_block_data['batch_id'] is not None}")
            print(f"   batch_id value: '{edit_block_data.get('batch_id')}'")
            print(f"   batch_id != 'None': {edit_block_data.get('batch_id') != 'None'}")
            print(f"   batch_id != 'null': {edit_block_data.get('batch_id') != 'null'}")
            
            # Test the full data attribute as it appears in the template
            full_template = """
            data-batch-id="{{ edit_block_data.batch_id if (edit_block_data and edit_block_data.batch_id and edit_block_data.batch_id != 'None' and edit_block_data.batch_id != 'null') else '' }}"
            """
            
            full_result = render_template_string(full_template, edit_block_data=edit_block_data)
            print(f"\n🎯 Full data attribute: {full_result.strip()}")
            
        except Exception as e:
            print(f"❌ Template rendering error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_data_attribute_only()