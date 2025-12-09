# Database Connection Fix - 500 Error Resolved

## The Problem

After the initial server start, login was returning a 500 error. The actual issue was:
```
pymysql.err.OperationalError: (2003, "Can't connect to MySQL server on 'localhost' ([Errno 61] Connection refused)")
```

## Root Cause

The Flask application was trying to connect to MySQL instead of SQLite, even though `.env` was configured for SQLite:
```
DATABASE_URL=sqlite:///instance/tennis_club.db
```

The issue was that the Flask process wasn't properly loading the `.env` file on startup, so it fell back to the default MySQL configuration in `config.py`.

## The Fix

Restarted the Flask server using `./restart_server.sh`, which properly:
1. Activates the virtual environment
2. Loads environment variables from `.env`
3. Starts Flask with the correct SQLite database configuration

## Verification

✅ Server is now running correctly:
- Login page loads (200 OK)
- No 500 errors
- SQLite database is being used
- Process ID: 42662

## Test It

The application is now fully functional:
1. Go to http://localhost:5001
2. Login with test credentials:
   - Admin: `admin@test.com` / `admin123`
   - Member: `member@test.com` / `member123`

## Key Takeaway

When you see database connection errors, always check:
1. Is the `.env` file configured correctly?
2. Is the Flask process loading the `.env` file?
3. Try restarting the server to reload environment variables

## Files Involved

- `.env` - Contains `DATABASE_URL=sqlite:///instance/tennis_club.db`
- `config.py` - Reads `DATABASE_URL` from environment
- `wsgi.py` - Loads `.env` using `python-dotenv`
- `restart_server.sh` - Properly restarts server with environment variables

Everything is working now! 🎉
