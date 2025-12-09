# Deploy to PythonAnywhere - Instructions

## ✅ Git Changes Pushed

All changes have been committed and pushed to GitHub:
- Commit: "Fix login and API 500 errors - disable email deliverability check, fix database migrations, update restart script"
- Branch: main
- Status: Pushed successfully

## 🚀 Deploy to PythonAnywhere

### Option 1: Run Deployment Script (Recommended)

Open a Bash console on PythonAnywhere and run:

```bash
cd ~/tcz && python3 deploy.py
```

This will automatically:
1. Pull latest code from GitHub
2. Run database migrations
3. Reload the webapp

### Option 2: Manual Deployment

If the script doesn't work, run these commands manually:

```bash
# 1. Navigate to project
cd ~/tcz

# 2. Pull latest changes
git pull origin main

# 3. Activate virtual environment
source ~/.virtualenvs/tennisclub/bin/activate

# 4. Run database migrations
export FLASK_APP=wsgi.py
flask db upgrade

# 5. Reload webapp
touch /var/www/woifh_pythonanywhere_com_wsgi.py
```

### Option 3: Use Existing Script

```bash
cd ~/tcz && bash deploy_now.sh
```

## 📋 What Will Be Deployed

### Code Changes
- ✅ Email validator fix (allows test domains)
- ✅ Restart script improvements
- ✅ New documentation files

### Database Changes
- ✅ Migration `c97a5390ecac` - Adds `is_short_notice` column
- ✅ Index on `is_short_notice` for performance

## 🔍 Verification Steps

After deployment, verify:

1. **Website loads**: https://woifh.pythonanywhere.com
2. **Login works**: Try logging in with test credentials
3. **No 500 errors**: Check court availability and reservations
4. **Short notice bookings**: Should show with orange background

## ⚠️ Important Notes

### Database Migration
The migration adds the `is_short_notice` column to the `reservation` table. This is required for the application to work correctly.

### Email Validation
The email validator now accepts test domains (like `@test.com`) in both development and production.

### Rate Limiting
Make sure rate limiting is ENABLED in production (it should be by default).

## 🆘 Troubleshooting

### If git pull fails:
```bash
cd ~/tcz
git status
git stash  # If there are local changes
git pull origin main
```

### If migrations fail:
```bash
flask db current  # Check current version
flask db stamp 088504aa5508  # Stamp to previous version
flask db upgrade  # Try again
```

### If webapp doesn't reload:
1. Go to https://www.pythonanywhere.com/user/woifh/webapps/
2. Click the "Reload" button manually

## 📞 Need Help?

If you encounter any issues:
1. Check the error logs on PythonAnywhere
2. Verify the virtual environment is activated
3. Ensure all environment variables are set
4. Check that the database connection works

---

**Ready to deploy!** Just run one of the commands above in a PythonAnywhere Bash console.
