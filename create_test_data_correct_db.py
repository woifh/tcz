#!/usr/bin/env python3
"""
Create test data in the CORRECT database that the Flask app is using
"""

import sqlite3
import os
from datetime import date, time

def create_test_data():
    # The actual database from .env file
    db_path = "instance/tennis_club.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return False
    
    print(f"🔧 Creating test data in ACTUAL database: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        batch_id = "1d40fb5c-500c-4127-9c4a-05d9f53fe47f"
        
        # First, check if we have the required tables and data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='block';")
        if not cursor.fetchone():
            print("❌ Block table doesn't exist. Need to initialize database first.")
            return False
        
        # Check if we have a member (for created_by_id)
        cursor.execute("SELECT id FROM member WHERE role = 'admin' LIMIT 1;")
        admin = cursor.fetchone()
        if not admin:
            print("❌ No admin member found. Need to create one first.")
            return False
        
        admin_id = admin[0]
        print(f"✅ Using admin member ID: {admin_id}")
        
        # Check if we have a block reason
        cursor.execute("SELECT id FROM block_reason LIMIT 1;")
        reason = cursor.fetchone()
        if not reason:
            print("❌ No block reason found. Need to create one first.")
            return False
        
        reason_id = reason[0]
        print(f"✅ Using block reason ID: {reason_id}")
        
        # Create test blocks for multiple courts (like in the screenshot)
        courts = [1, 2, 3, 4, 5, 6]  # 6 courts as shown in screenshot
        
        for court_id in courts:
            # Check if block already exists
            cursor.execute("SELECT id FROM block WHERE batch_id = ? AND court_id = ?", (batch_id, court_id))
            existing = cursor.fetchone()
            
            if existing:
                print(f"⚠️ Block already exists for court {court_id}")
                continue
            
            # Insert the block
            cursor.execute("""
                INSERT INTO block (court_id, date, start_time, end_time, reason_id, sub_reason, batch_id, is_modified, created_by_id, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                court_id,
                '2026-01-04',  # Tomorrow
                '08:00:00',    # 08:00
                '22:00:00',    # 22:00
                reason_id,
                'Geplant',
                batch_id,
                0,  # is_modified = False
                admin_id
            ))
            
            print(f"✅ Created block for court {court_id}")
        
        conn.commit()
        
        # Verify the blocks were created
        cursor.execute("SELECT id, court_id, date FROM block WHERE batch_id = ?", (batch_id,))
        blocks = cursor.fetchall()
        print(f"\n📊 Verification: Found {len(blocks)} blocks with batch_id {batch_id}")
        
        for block in blocks:
            print(f"  Block {block[0]}: Court {block[1]}, Date {block[2]}")
        
        print(f"\n✅ Test data created successfully in ACTUAL database!")
        print(f"🔗 You can now test the edit URL: http://127.0.0.1:5001/admin/court-blocking/{batch_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = create_test_data()
    exit(0 if success else 1)