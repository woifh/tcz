#!/usr/bin/env python3
"""Quick script to add an admin user"""
import sys
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models import Member

if len(sys.argv) != 5:
    print("Usage: python add_admin.py <firstname> <lastname> <email> <password>")
    print("Example: python add_admin.py John Doe john@example.com mypassword")
    sys.exit(1)

firstname, lastname, email, password = sys.argv[1:5]

app = create_app('development')

with app.app_context():
    # Check if user exists
    if Member.query.filter_by(email=email).first():
        print(f"❌ User with email {email} already exists")
        sys.exit(1)
    
    # Create admin
    admin = Member(
        firstname=firstname,
        lastname=lastname,
        email=email,
        role='administrator'
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print("✅ Admin user created successfully!")
    print(f"   Name: {firstname} {lastname}")
    print(f"   Email: {email}")
    print(f"   Role: Administrator")
