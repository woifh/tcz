#!/usr/bin/env python3

import sqlite3

def debug_form_state():
    """Debug the current form state by checking what's in the database."""
    
    # Connect to the database
    conn = sqlite3.connect('instance/tennis_club_dev.db')
    cursor = conn.cursor()
    
    try:
        # Get all blocks with batch_id
        cursor.execute("""
            SELECT id, court_id, batch_id, date, start_time, end_time, sub_reason 
            FROM block 
            WHERE batch_id IS NOT NULL 
            ORDER BY created_at DESC 
            LIMIT 10
        """)
        
        blocks = cursor.fetchall()
        
        if not blocks:
            print("❌ No blocks with batch_id found in database")
            return
        
        print("📋 Found blocks with batch_id:")
        for block in blocks:
            block_id, court_id, batch_id, date, start_time, end_time, sub_reason = block
            print(f"   Block {block_id}: Court {court_id}, Batch {batch_id}, {date} {start_time}-{end_time}")
            if sub_reason:
                print(f"      Sub-reason: {sub_reason}")
        
        # Use the first batch for testing
        test_batch_id = blocks[0][2]  # batch_id
        print(f"\n🔗 Test edit URL: http://127.0.0.1:5001/admin/court-blocking/{test_batch_id}")
        
        # Show what the backend should be setting
        print(f"\n📝 Expected template data:")
        print(f"   data-edit-mode=\"true\"")
        print(f"   data-batch-id=\"{test_batch_id}\"")
        print(f"   data-block-id=\"{blocks[0][0]}\"")
        
        print(f"\n📝 Expected JavaScript data:")
        print(f"   batch_id: '{test_batch_id}'")
        
        return test_batch_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        conn.close()

if __name__ == '__main__':
    debug_form_state()