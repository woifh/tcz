#!/usr/bin/env python3
"""
Debug script to test template data attribute rendering
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Block
from flask import render_template_string

def test_template_data_attribute():
    """Test the template data attribute rendering"""
    app = create_app()
    
    with app.app_context():
        # Get a block with a valid batch_id
        block = Block.query.filter(Block.batch_id.isnot(None)).first()
        
        if not block:
            print("❌ No blocks with batch_id found")
            return
        
        print(f"✅ Found block with batch_id: {block.batch_id}")
        print(f"   Block ID: {block.id}")
        print(f"   Batch ID type: {type(block.batch_id)}")
        print(f"   Batch ID value: '{block.batch_id}'")
        
        # Create test edit_block_data similar to what the route creates
        edit_block_data = {
            'id': block.id,
            'batch_id': block.batch_id,
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
        for key, value in edit_block_data.items():
            print(f"   {key}: {value} (type: {type(value)})")
        
        # Test the template condition
        template_test = """
        data-batch-id="{{ edit_block_data.batch_id if (edit_block_data and edit_block_data.batch_id and edit_block_data.batch_id != 'None' and edit_block_data.batch_id != 'null') else '' }}"
        """
        
        try:
            result = render_template_string(template_test, edit_block_data=edit_block_data)
            print(f"\n🔍 Template result: {result.strip()}")
            
            # Test individual conditions
            print(f"\n🧪 Condition tests:")
            print(f"   edit_block_data exists: {edit_block_data is not None}")
            print(f"   edit_block_data.batch_id exists: {edit_block_data.get('batch_id') is not None}")
            print(f"   batch_id != 'None': {edit_block_data.get('batch_id') != 'None'}")
            print(f"   batch_id != 'null': {edit_block_data.get('batch_id') != 'null'}")
            
            # Test the actual value that would be rendered
            batch_id_value = edit_block_data.get('batch_id')
            if batch_id_value and batch_id_value != 'None' and batch_id_value != 'null':
                print(f"   ✅ Should render: data-batch-id=\"{batch_id_value}\"")
            else:
                print(f"   ❌ Should render empty: data-batch-id=\"\"")
                
        except Exception as e:
            print(f"❌ Template rendering error: {e}")

if __name__ == '__main__':
    test_template_data_attribute()