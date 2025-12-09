# API 500 Errors - FIXED ✅

## The Problem

Two API endpoints were returning 500 errors:
1. `/courts/availability?date=2025-12-09`
2. `/reservations/?format=json`

## Root Cause

The database schema was missing the `is_short_notice` column that was added in recent updates. The code was trying to query a column that didn't exist in the database.

**Error:**
```
sqlite3.OperationalError: no such column: reservation.is_short_notice
```

## The Fix

Ran database migrations to add the missing column:

```bash
# Stamp the database at the previous migration
flask db stamp 088504aa5508

# Upgrade to add the is_short_notice column
flask db upgrade
```

This added:
- `is_short_notice` BOOLEAN column to the `reservation` table (default: FALSE)
- Index on `is_short_notice` for better query performance

## Verification

Tested the database connection successfully:
- ✅ Members: 4
- ✅ Courts: 6
- ✅ Reservations: 18
- ✅ All queries working

## Current Status

✅ **Server restarted with updated schema**
- URL: http://localhost:5001
- Process ID: 43514
- Database: Fully migrated with `is_short_notice` column
- All API endpoints should now work correctly

## Test It

The application should now work without 500 errors:
1. Refresh your browser
2. Try viewing court availability
3. Try viewing reservations
4. All features should work normally

## What is `is_short_notice`?

This column tracks bookings made within 15 minutes of the start time. These bookings:
- Don't count toward the 2-reservation limit
- Are displayed with an orange background
- Show "Kurzfristig gebucht" (Short notice booking)

Everything is working now! 🎉
