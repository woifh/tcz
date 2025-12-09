# Server Restart Guide

## The Issue You Encountered

When you ran `python3 restart_server.py`, you got this error:
```
ModuleNotFoundError: No module named 'dotenv'
```

## Why This Happened

The `restart_server.py` script imports `python-dotenv` at line 12:
```python
from dotenv import load_dotenv
```

However, `python-dotenv` is only installed in your **virtual environment** (`venv/`), not in your system Python. When you ran `python3 restart_server.py`, you were using the system Python which doesn't have access to the packages in your venv.

## The Solution

You have **two easy options**:

### Option 1: Use the Bash Script (Easiest)
```bash
./restart_server.sh
```

This script automatically activates the virtual environment for you, so you don't need to worry about it.

### Option 2: Activate venv First, Then Use Python Script
```bash
source venv/bin/activate
python restart_server.py
```

Notice:
- Use `source venv/bin/activate` first
- Then use `python` (not `python3`) - this uses the venv's Python
- The script provides more control with flags: `--start`, `--stop`, `--restart`

## What I Did to Fix It

1. **Fixed the bash script** - Added `source venv/bin/activate` to ensure it uses the venv's Python
2. **Started the server** - The Flask server is now running at http://localhost:5001
3. **Updated documentation** - Added clear instructions in `LOCAL_TESTING_INFO.md`

## Current Server Status

✅ **Flask server is running!**
- **URL**: http://localhost:5001
- **Process ID**: 42461
- **Port**: 5001
- **Rate Limiting**: Disabled for local development

To stop it:
```bash
pkill -f "flask run"
```

## Key Takeaway

**Always activate the virtual environment before running Python scripts:**
```bash
source venv/bin/activate
```

This ensures you're using the correct Python interpreter with all the required packages installed.

## Test It Out

The server is ready! You can now:
1. Open http://localhost:5001 in your browser
2. Login with test credentials:
   - Admin: `admin@test.com` / `admin123`
   - Member: `member@test.com` / `member123`
3. Test the booking functionality

Everything is working perfectly now! 🎉
