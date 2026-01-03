#!/usr/bin/env python3
"""
Debug script to directly test the route function
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Block, Member
from app.routes.admin import court_blocking_edit_batch
from flask import render_template

def test_route_direct():
    """Test the route function directly"""
    app = create_app()
    
    with app.app_context():
        # Get a block with a valid batch_id
        block = Block.query.filter(Block.batch_id.isnot(None)).first()
        
        if not block:
            print("❌ No blocks with batch_id found")
            return
        
        print(f"✅ Found block with batch_id: {block.batch_id}")
        print(f"   Block ID: {block.id}")
        
        # Simulate the route logic
        batch_id = block.batch_id
        actual_batch_id = batch_id.replace('batch_', '') if batch_id.startswith('batch_') else batch_id
        
        # Get all blocks with this batch_id
        blocks = Block.query.filter_by(batch_id=actual_batch_id).all()
        
        if not blocks:
            print("❌ No blocks found with this batch_id")
            return
        
        # Use the first block as the primary block for data
        primary_block = blocks[0]
        
        # Extract court IDs from all blocks in the batch
        court_ids = [block.court_id for block in blocks]
        
        # Create a combined block data structure
        edit_block_data = {
            'id': primary_block.id,
            'batch_id': actual_batch_id,  # Use the batch_id from the URL, not from the database
            'court_ids': court_ids,
            'date': primary_block.date,
            'start_time': primary_block.start_time,
            'end_time': primary_block.end_time,
            'reason_id': primary_block.reason_id,
            'sub_reason': primary_block.sub_reason,
            'created_by': primary_block.created_by_id,
            'created_at': primary_block.created_at,
            'related_block_ids': [block.id for block in blocks]
        }
        
        print(f"\n📊 edit_block_data created by route:")
        for key, value in edit_block_data.items():
            print(f"   {key}: {value} (type: {type(value)})")
        
        # Test the template rendering with this data
        try:
            html = render_template('admin/court_blocking.html', edit_block_data=edit_block_data)
            
            # Look for the data-batch-id attribute in the HTML
            import re
            batch_id_match = re.search(r'data-batch-id="([^"]*)"', html)
            
            if batch_id_match:
                found_batch_id = batch_id_match.group(1)
                print(f"\n✅ Found data-batch-id in rendered HTML: '{found_batch_id}'")
                
                if found_batch_id == actual_batch_id:
                    print(f"   ✅ Batch ID matches expected value")
                else:
                    print(f"   ❌ Batch ID mismatch. Expected: '{actual_batch_id}', Found: '{found_batch_id}'")
            else:
                print(f"\n❌ data-batch-id attribute not found in rendered HTML")
                
                # Look for the form element
                form_match = re.search(r'<form[^>]*id="multi-court-form"[^>]*>', html)
                if form_match:
                    print(f"   Form element found: {form_match.group(0)}")
                else:
                    print(f"   ❌ Form element not found")
            
            # Also check for edit mode
            edit_mode_match = re.search(r'data-edit-mode="([^"]*)"', html)
            if edit_mode_match:
                print(f"   Edit mode: {edit_mode_match.group(1)}")
                
        except Exception as e:
            print(f"❌ Template rendering error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    test_route_direct()