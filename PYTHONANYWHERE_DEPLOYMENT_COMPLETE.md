# PythonAnywhere Deployment Guide

## What Was Deployed

### Code Changes
1. **Email Validator Fix** - Disabled deliverability check to allow test domains
   - File: `app/utils/validators.py`
   - Change: Added `check_deliverability=False` parameter

2. **Restart Script Update** - Fixed environment variable loading
   - File: `restart_server.sh`
   - Change: Added `.env` file loading

3. **Documentation** - Added comprehensive troubleshooting guides
   - `API_500_ERRORS_FIXED.md`
   - `DATABASE_CONNECTION_FIX.md`
   - `LOGIN_FIXED_FINAL.md`
   - `SERVER_RESTART_GUIDE.md`

### Database Changes
- **Migration**: `c97a5390ecac` - Add `is_short_notice` field to reservation table
- **Column Added**: `is_short_notice` BOOLEAN (default: FALSE)
- **Index Added**: `idx_reservation_short_notice` for better query performance

## Deployment Steps

### Automated Deployment
Run the deployment script on PythonAnywhere:

```bash
cd ~/tcz && bash deploy_now.sh
```

This will:
1. Pull latest code from GitHub
2. Activate virtual environment
3. Run database migrations
4. Reload the webapp

### Manual Deployment (if needed)

```bash
# 1. Navigate to project
cd ~/tcz

# 2. Pull latest changes
git pull origin main

# 3. Activate virtual environment
source ~/.virtualenvs/tennisclub/bin/activate

# 4. Run migrations
export FLASK_APP=wsgi.py
flask db upgrade

# 5. Reload webapp
touch /var/www/woifh_pythonanywhere_com_wsgi.py
```

## Verification

After deployment, verify:

1. **Website loads**: https://woifh.pythonanywhere.com
2. **Login works**: Use test credentials
3. **Court availability loads**: No 500 errors
4. **Reservations load**: No 500 errors
5. **Short notice bookings**: Orange background for bookings within 15 minutes

## Important Notes

### Production vs Development

**Local Development** (`.env`):
```bash
RATELIMIT_ENABLED=false
DATABASE_URL=sqlite:////Users/woifh/tcz/tcz/instance/tennis_club.db
```

**Production** (PythonAnywhere `.env`):
```bash
# Rate limiting should be ENABLED (or not set)
# DATABASE_URL should use MySQL
DATABASE_URL=mysql+pymysql://username:password@host/database
```

### Database Differences

- **Local**: SQLite with absolute path
- **Production**: MySQL on PythonAnywhere

### Email Validation

The `check_deliverability=False` change applies to both environments, allowing test domains like `@test.com` to work.

## Troubleshooting

### If migrations fail:
```bash
# Check current migration status
flask db current

# If needed, stamp to specific revision
flask db stamp 088504aa5508

# Then upgrade
flask db upgrade
```

### If webapp doesn't reload:
1. Go to https://www.pythonanywhere.com/user/woifh/webapps/
2. Click "Reload" button manually

### If database errors occur:
- Check that migrations ran successfully
- Verify `is_short_notice` column exists:
  ```sql
  DESCRIBE reservation;
  ```

## Deployment Scripts

Three deployment scripts are available:

1. **deploy_now.sh** - Quick deployment (recommended)
2. **deploy_update.sh** - Full deployment with dependency updates
3. **deploy_with_migrations.sh** - Deployment focused on migrations

## Next Steps

After successful deployment:
1. Test all features on production
2. Monitor for any errors
3. Check that short notice bookings work correctly
4. Verify email validation accepts test domains

## Rollback (if needed)

If something goes wrong:

```bash
cd ~/tcz
git log --oneline -5  # Find previous commit
git reset --hard <commit-hash>
flask db downgrade  # Rollback migration
touch /var/www/woifh_pythonanywhere_com_wsgi.py
```

## Support

If issues persist:
- Check PythonAnywhere error logs
- Review Flask application logs
- Verify database connection settings
- Ensure all environment variables are set correctly

---

**Deployment Date**: December 9, 2025
**Deployed By**: Kiro AI Assistant
**Status**: Ready to deploy
