#!/usr/bin/env python3
"""Debug the template condition issue."""

import sys
sys.path.append('.')
from app import create_app, db
from app.models import Block
from flask import render_template_string

app = create_app()

with app.app_context():
    block = Block.query.filter(Block.batch_id.isnot(None)).first()
    
    # Create the exact same edit_block_data as the backend
    edit_block_data = {
        'id': block.id,
        'batch_id': block.batch_id,
        'court_ids': [block.court_id],
        'date': block.date,
        'start_time': block.start_time,
        'end_time': block.end_time,
        'reason_id': block.reason_id,
        'sub_reason': block.sub_reason,
        'created_by': block.created_by,
        'created_at': block.created_at,
        'related_block_ids': [block.id]
    }
    
    print(f"edit_block_data: {edit_block_data}")
    print(f"edit_block_data['batch_id']: {edit_block_data['batch_id']}")
    print(f"type: {type(edit_block_data['batch_id'])}")
    
    # Test each part of the condition
    template_tests = [
        ('edit_block_data exists', '{{ edit_block_data is not none }}'),
        ('edit_block_data truthy', '{{ edit_block_data | bool }}'),
        ('batch_id exists', '{{ edit_block_data.batch_id is not none if edit_block_data else "NO_DATA" }}'),
        ('batch_id truthy', '{{ edit_block_data.batch_id | bool if edit_block_data else "NO_DATA" }}'),
        ('combined condition', '{{ (edit_block_data and edit_block_data.batch_id) | bool }}'),
        ('final result', '{{ edit_block_data.batch_id if edit_block_data and edit_block_data.batch_id else "EMPTY" }}'),
    ]
    
    for test_name, template in template_tests:
        try:
            result = render_template_string(template, edit_block_data=edit_block_data)
            print(f"{test_name}: {result}")
        except Exception as e:
            print(f"{test_name}: ERROR - {e}")
    
    # Test the exact form tag
    form_template = '''<form data-batch-id="{{ edit_block_data.batch_id if edit_block_data and edit_block_data.batch_id else '' }}">'''
    
    try:
        form_result = render_template_string(form_template, edit_block_data=edit_block_data)
        print(f"Form tag result: {form_result}")
        
        # Extract the data-batch-id value
        import re
        match = re.search(r'data-batch-id="([^"]*)"', form_result)
        if match:
            print(f"Extracted batch_id: '{match.group(1)}'")
        else:
            print("No batch_id found in form tag")
            
    except Exception as e:
        print(f"Form template error: {e}")