#!/usr/bin/env python3
"""
Create a new admin user for the Tennis Club Reservation System
Usage: python create_admin_user.py
"""
import os
import sys
from getpass import getpass

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Member

def create_admin():
    """Interactive script to create a new admin user"""
    print("=" * 60)
    print("Create New Admin User")
    print("=" * 60)
    print()
    
    # Get user input
    print("Enter admin details:")
    firstname = input("First name: ").strip()
    lastname = input("Last name: ").strip()
    email = input("Email: ").strip()
    
    # Validate email
    if not email or '@' not in email:
        print("❌ Invalid email address")
        sys.exit(1)
    
    # Get password (hidden input)
    password = getpass("Password: ")
    password_confirm = getpass("Confirm password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match")
        sys.exit(1)
    
    if len(password) < 6:
        print("❌ Password must be at least 6 characters")
        sys.exit(1)
    
    # Create the app context
    app = create_app('development')
    
    with app.app_context():
        # Check if user already exists
        existing_user = Member.query.filter_by(email=email).first()
        if existing_user:
            print(f"❌ User with email {email} already exists")
            sys.exit(1)
        
        # Create new admin user
        admin = Member(
            firstname=firstname,
            lastname=lastname,
            email=email,
            role='administrator'
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        print()
        print("=" * 60)
        print("✅ Admin user created successfully!")
        print("=" * 60)
        print()
        print("Admin Details:")
        print(f"  Name: {firstname} {lastname}")
        print(f"  Email: {email}")
        print(f"  Role: Administrator")
        print()
        print("You can now login with these credentials.")
        print()

if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\n❌ Operation cancelled")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
