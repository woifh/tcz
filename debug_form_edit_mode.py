#!/usr/bin/env python3
"""
Debug script to test form edit mode detection.
This script will create a test blocking and then access the edit page to see what's happening.
"""

import requests
import json
from datetime import datetime, date, time

BASE_URL = "http://127.0.0.1:5001"

def login_admin():
    """Login as admin user"""
    session = requests.Session()
    
    # Get login page
    login_page = session.get(f"{BASE_URL}/auth/login")
    
    # Login with admin credentials
    login_data = {
        'email': 'admin@tennisclub.de',
        'password': 'admin123'
    }
    
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=True)
    
    # Check if we're logged in by trying to access admin page
    admin_check = session.get(f"{BASE_URL}/admin/overview")
    if admin_check.status_code == 200:
        print("✅ Admin login successful")
        return session
    else:
        print(f"❌ Admin login failed - cannot access admin page: {admin_check.status_code}")
        return None

def create_test_blocking(session):
    """Create a test blocking entry via API"""
    blocking_data = {
        'court_ids': [1, 2],
        'date': '2026-01-10',
        'start_time': '10:00',
        'end_time': '12:00',
        'reason_id': 1,  # Assuming reason ID 1 exists
        'sub_reason': 'Debug test blocking'
    }
    
    response = session.post(
        f"{BASE_URL}/admin/blocks/multi-court",
        json=blocking_data,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Test blocking created: {result.get('message')}")
        return True
    else:
        print(f"❌ Failed to create test blocking: {response.status_code}")
        print(f"Response: {response.text}")
        return False

def get_test_batch_id(session):
    """Get the batch_id of our test blocking"""
    response = session.get(f"{BASE_URL}/admin/blocks?date=2026-01-10")
    
    if response.status_code == 200:
        result = response.json()
        blocks = result.get('blocks', [])
        
        # Find blocks with our test data
        test_blocks = [b for b in blocks if b.get('sub_reason') == 'Debug test blocking']
        if test_blocks:
            batch_id = test_blocks[0].get('batch_id')
            print(f"✅ Found test blocks with batch_id: {batch_id}")
            return batch_id
        else:
            print("❌ Test blocks not found")
            return None
    else:
        print(f"❌ Failed to get blocks: {response.status_code}")
        return None

def check_edit_page_html(session, batch_id):
    """Check the HTML of the edit page to see if data attributes are set correctly"""
    edit_url = f"{BASE_URL}/admin/court-blocking/{batch_id}"
    response = session.get(edit_url)
    
    if response.status_code == 200:
        html_content = response.text
        
        print(f"✅ Edit page loaded successfully: {edit_url}")
        
        # Check for data attributes in the HTML
        if 'data-edit-mode="true"' in html_content:
            print("✅ Found data-edit-mode='true' in HTML")
        else:
            print("❌ data-edit-mode='true' NOT found in HTML")
            
        if f'data-batch-id="{batch_id}"' in html_content:
            print(f"✅ Found data-batch-id='{batch_id}' in HTML")
        else:
            print(f"❌ data-batch-id='{batch_id}' NOT found in HTML")
            
        # Check for window.editBlockData
        if 'window.editBlockData' in html_content:
            print("✅ Found window.editBlockData in HTML")
        else:
            print("❌ window.editBlockData NOT found in HTML")
            
        # Extract the form element to see the actual data attributes
        import re
        form_match = re.search(r'<form[^>]*id="multi-court-form"[^>]*>', html_content)
        if form_match:
            form_tag = form_match.group(0)
            print(f"\n📋 Form tag: {form_tag}")
        else:
            print("❌ Could not find form tag")
            
        return True
    else:
        print(f"❌ Failed to load edit page: {response.status_code}")
        return False

def cleanup_test_data(session):
    """Clean up test data"""
    response = session.get(f"{BASE_URL}/admin/blocks?date=2026-01-10")
    
    if response.status_code == 200:
        result = response.json()
        blocks = result.get('blocks', [])
        
        # Find test blocks
        test_blocks = [b for b in blocks if 'debug test blocking' in (b.get('sub_reason') or '').lower()]
        
        for block in test_blocks:
            batch_id = block.get('batch_id')
            if batch_id:
                delete_response = session.delete(f"{BASE_URL}/admin/blocks/batch/{batch_id}")
                if delete_response.status_code == 200:
                    print(f"✅ Cleaned up test batch: {batch_id}")
                else:
                    print(f"❌ Failed to clean up batch {batch_id}: {delete_response.status_code}")

def main():
    print("🔍 Debugging Form Edit Mode Detection")
    print("=" * 50)
    
    # Login
    session = login_admin()
    if not session:
        return
    
    try:
        # Create test blocking
        if not create_test_blocking(session):
            return
        
        # Get the batch_id
        batch_id = get_test_batch_id(session)
        if not batch_id:
            return
        
        # Check the edit page HTML
        if not check_edit_page_html(session, batch_id):
            return
            
        print(f"\n🔗 Edit URL: {BASE_URL}/admin/court-blocking/{batch_id}")
        print("📝 Manual test: Open this URL in browser and check console for:")
        print("   - 'Initializing form in edit mode from data attributes'")
        print("   - 'Form submitted - Edit mode: true, Batch ID: <uuid>'")
        
    finally:
        # Clean up
        print("\n🧹 Cleaning up test data...")
        cleanup_test_data(session)
    
    print("\n✅ Debug completed")

if __name__ == "__main__":
    main()