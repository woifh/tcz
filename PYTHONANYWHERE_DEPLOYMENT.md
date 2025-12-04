# PythonAnywhere Deployment Guide

## Prerequisites

1. A PythonAnywhere account (free or paid)
2. Your GitHub repository URL: https://github.com/woifh/tcz.git

## Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com/
2. Sign up for a free account (or use existing account)
3. Verify your email address

## Step 2: Set Up MySQL Database

1. Go to the **Databases** tab in PythonAnywhere
2. Create a new MySQL database:
   - Database name: `yourusername$tennisclub` (replace `yourusername` with your PythonAnywhere username)
   - Set a password and save it
3. Note down:
   - Database name: `yourusername$tennisclub`
   - Database host: `yourusername.mysql.pythonanywhere-services.com`
   - Username: `yourusername`
   - Password: (the one you just set)

## Step 3: Clone Repository

1. Go to the **Consoles** tab
2. Start a new **Bash console**
3. Clone your repository:
   ```bash
   git clone https://github.com/woifh/tcz.git
   cd tcz
   ```

## Step 4: Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 tennisclub
```

## Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 6: Configure Environment Variables

Create a `.env` file in the project root:

```bash
nano .env
```

Add the following (replace with your actual values):

```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://yourusername:yourpassword@yourusername.mysql.pythonanywhere-services.com/yourusername$tennisclub

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=production

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=noreply@tennisclub.de

# Application Settings
COURTS_COUNT=6
BOOKING_START_HOUR=6
BOOKING_END_HOUR=22
MAX_ACTIVE_RESERVATIONS=2
```

**Important Notes:**
- Generate a strong SECRET_KEY: `python3 -c "import secrets; print(secrets.token_hex(32))"`
- For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your regular password
- Save the file: Ctrl+O, Enter, Ctrl+X

## Step 7: Initialize Database

```bash
# Set Flask app
export FLASK_APP=wsgi.py

# Run migrations
flask db upgrade

# Create admin user
flask create-admin --name "Admin" --email "admin@tennisclub.de" --password "your-admin-password"

# Initialize courts
python3 init_db.py
```

## Step 8: Configure Web App

1. Go to the **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**
5. Click through the wizard

### Configure WSGI File

1. Click on the WSGI configuration file link
2. Delete all content and replace with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/tcz'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from wsgi import application
```

Replace `yourusername` with your actual PythonAnywhere username.

### Configure Virtual Environment

1. In the **Web** tab, find the **Virtualenv** section
2. Enter: `/home/yourusername/.virtualenvs/tennisclub`

### Configure Static Files

In the **Static files** section, add:

| URL | Directory |
|-----|-----------|
| /static/ | /home/yourusername/tcz/app/static/ |

## Step 9: Install Additional Dependencies

If you get import errors, install these in your virtualenv:

```bash
workon tennisclub
pip install python-dotenv
pip install Flask-Limiter
pip install email-validator
```

## Step 10: Reload Web App

1. Go back to the **Web** tab
2. Click the big green **Reload** button
3. Your app should now be live at: `yourusername.pythonanywhere.com`

## Step 11: Test the Application

1. Visit `https://yourusername.pythonanywhere.com`
2. Log in with your admin credentials
3. Test creating reservations
4. Check that emails are being sent (if configured)

## Troubleshooting

### Check Error Logs

1. Go to the **Web** tab
2. Click on **Error log** link
3. Look for any Python errors

### Common Issues

**Database Connection Errors:**
- Verify DATABASE_URL in .env file
- Check MySQL database is created
- Verify username and password

**Import Errors:**
- Make sure all dependencies are installed in the virtualenv
- Check that the virtualenv path is correct in Web tab

**Static Files Not Loading:**
- Verify static files path in Web tab
- Check file permissions: `chmod -R 755 ~/tcz/app/static`

**Email Not Sending:**
- Verify MAIL_* settings in .env
- For Gmail, ensure you're using an App Password
- Check that MAIL_USE_TLS is set to True

### View Application Logs

```bash
tail -f /var/log/yourusername.pythonanywhere.com.error.log
```

## Updating the Application

When you make changes to your code:

```bash
cd ~/tcz
git pull origin main
workon tennisclub
pip install -r requirements.txt  # If dependencies changed
flask db upgrade  # If database schema changed
```

Then reload the web app from the Web tab.

## Security Checklist

- [ ] Changed SECRET_KEY to a strong random value
- [ ] Using HTTPS (PythonAnywhere provides this automatically)
- [ ] Email credentials are secure (using App Password)
- [ ] Admin password is strong
- [ ] .env file is not committed to git (it's in .gitignore)
- [ ] Database password is strong

## Performance Optimization

For better performance on PythonAnywhere:

1. **Enable MySQL Connection Pooling** - Already configured in the app
2. **Use Redis for Rate Limiting** (paid accounts only):
   ```python
   # In app/__init__.py, change:
   storage_uri="redis://localhost:6379"
   ```

## Monitoring

1. **Check Error Logs Regularly**: Web tab → Error log
2. **Monitor Database Size**: Databases tab
3. **Check CPU Usage**: Account tab (free accounts have daily limits)

## Backup

Regular backups are important:

```bash
# Backup database
mysqldump -u yourusername -h yourusername.mysql.pythonanywhere-services.com -p yourusername$tennisclub > backup.sql

# Backup uploaded files (if any)
tar -czf backup.tar.gz ~/tcz/instance/
```

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- PythonAnywhere Forums: https://www.pythonanywhere.com/forums/
- Your GitHub Issues: https://github.com/woifh/tcz/issues

## Next Steps

After deployment:

1. Test all functionality thoroughly
2. Create additional member accounts
3. Set up email notifications properly
4. Consider upgrading to a paid account for:
   - Custom domain
   - More CPU time
   - SSH access
   - Always-on tasks
