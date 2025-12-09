# Login Issue - FIXED ✅

## Summary of Issues and Fixes

### Issue 1: Rate Limiting (429 Error)
**Problem:** Login was blocked by rate limiter (5 attempts per minute)
**Fix:** Added `RATELIMIT_ENABLED=false` to `.env`

### Issue 2: MySQL Connection Error
**Problem:** Flask was trying to connect to MySQL instead of SQLite
**Fix:** Updated restart script to load `.env` variables properly

### Issue 3: Email Validation Rejecting @test.com
**Problem:** `email-validator` library was rejecting `@test.com` domain as invalid
**Fix:** Modified `app/utils/validators.py` to disable deliverability check:
```python
valid = validate_email(email, check_deliverability=False)
```

### Issue 4: SQLite Database Path
**Problem:** Relative path `sqlite:///instance/tennis_club.db` wasn't working
**Fix:** Changed to absolute path in `.env`:
```
DATABASE_URL=sqlite:////Users/woifh/tcz/tcz/instance/tennis_club.db
```

## Current Status

✅ **Server is running correctly**
- URL: http://localhost:5001
- Process ID: 43189
- Database: SQLite at `/Users/woifh/tcz/tcz/instance/tennis_club.db`
- Rate limiting: Disabled for local development
- Email validation: Allows test domains

## Test Users in Database

The database contains these users:
- `admin@test.com` / `admin123` (administrator)
- `member@test.com` / `member123` (member)
- `wolfgang.hacker@gmail.com` (member)
- `test@test.com` (member)

## How to Login

1. Go to http://localhost:5001
2. Use credentials:
   - **Admin**: `admin@test.com` / `admin123`
   - **Member**: `member@test.com` / `member123`

## Files Modified

1. `.env` - Added `RATELIMIT_ENABLED=false` and fixed `DATABASE_URL`
2. `app/utils/validators.py` - Disabled email deliverability check
3. `restart_server.sh` - Added `.env` loading

## Important Notes

- **For Production**: Re-enable rate limiting and email deliverability checks
- **Database Path**: Use relative paths in production (works fine on PythonAnywhere)
- **Test Domains**: The `check_deliverability=False` allows @test.com emails for local testing

## Next Steps

The application is now fully functional! You can:
1. Login with test credentials
2. View court availability
3. Make reservations
4. Manage favourites
5. View your bookings

Everything is working! 🎉
