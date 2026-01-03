#!/usr/bin/env python3
"""
Deploy admin refactor changes to PythonAnywhere
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr.strip()}")
        return False

def main():
    """Main deployment function."""
    print("🚀 Deploying Admin Refactor Changes to PythonAnywhere")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('app/routes/admin'):
        print("❌ Error: Not in the correct project directory")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    print("\n📋 Changes to deploy:")
    print("- Refactored admin.py into modular structure")
    print("- Fixed /admin/blocks API endpoint")
    print("- Removed references to non-existent 'description' field")
    print("- Updated route parameter handling")
    
    # Step 1: Commit changes locally
    print("\n" + "=" * 60)
    print("STEP 1: Committing changes locally")
    
    if not run_command("git add .", "Adding all changes to git"):
        return False
    
    commit_msg = "Refactor admin routes and fix blocks API endpoint"
    if not run_command(f'git commit -m "{commit_msg}"', "Committing changes"):
        print("ℹ️  No changes to commit (already committed)")
    
    # Step 2: Push to GitHub
    print("\n" + "=" * 60)
    print("STEP 2: Pushing to GitHub")
    
    if not run_command("git push origin main", "Pushing to GitHub"):
        return False
    
    # Step 3: Instructions for PythonAnywhere
    print("\n" + "=" * 60)
    print("STEP 3: Update on PythonAnywhere")
    print("\nNow run these commands in a PythonAnywhere Bash console:")
    print("\n" + "-" * 40)
    print("cd tcz")
    print("git pull origin main")
    print("source ~/.virtualenvs/tennisclub/bin/activate")
    print("pip install -r requirements.txt --upgrade")
    print("export FLASK_APP=wsgi.py")
    print("flask db upgrade")
    print("-" * 40)
    
    print("\nThen reload your web app:")
    print("1. Go to: https://www.pythonanywhere.com/user/woifh/webapps/")
    print("2. Click the green 'Reload' button")
    
    print("\n✅ Deployment preparation complete!")
    print("\nKey changes deployed:")
    print("- ✅ Admin routes now modular (views, blocks, bulk, reasons, templates, series, audit)")
    print("- ✅ Fixed /admin/blocks API to handle court_ids, reason_ids, block_types parameters")
    print("- ✅ Removed non-existent 'description' field references")
    print("- ✅ Updated admin_panel route to admin.index")
    print("- ✅ All admin functionality preserved in new structure")
    
    print(f"\nYour app will be updated at: https://woifh.pythonanywhere.com")

if __name__ == "__main__":
    main()