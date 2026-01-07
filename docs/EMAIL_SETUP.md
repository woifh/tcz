# Email Setup Guide for Tennis Club Reservation System

This guide explains how to configure email notifications for both local development and production deployment on PythonAnywhere.

## Table of Contents

- [Overview](#overview)
- [Gmail App Password Setup](#gmail-app-password-setup)
- [Local Development Setup](#local-development-setup)
- [Production Setup (PythonAnywhere)](#production-setup-pythonanywhere)
- [Testing Email Configuration](#testing-email-configuration)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)

---

## Overview

The Tennis Club Reservation System sends email notifications for:

- **Booking Created** - Confirmation when a reservation is made
- **Booking Modified** - Notification when a reservation is updated
- **Booking Cancelled** - Notice when a reservation is cancelled by the user
- **Admin Override** - Special notification when an admin cancels a reservation

All emails are sent using **Gmail SMTP** with **App Password** authentication.

### Why App Passwords?

Google requires App Passwords for applications that access Gmail via SMTP. This is more secure than using your regular Gmail password and allows you to revoke access to specific apps without changing your main password.

---

## Gmail App Password Setup

Follow these steps to generate a Gmail App Password:

### Prerequisites

- A Gmail account
- 2-Step Verification enabled on your Google account

### Step-by-Step Instructions

#### 1. Enable 2-Step Verification (if not already enabled)

1. Go to [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Scroll to "How you sign in to Google"
3. Click "2-Step Verification"
4. Follow the prompts to enable it (you'll need your phone)

#### 2. Generate an App Password

1. Go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - You may need to sign in again

2. Under "Select app", choose **"Mail"**

3. Under "Select device", choose **"Other (Custom name)"**

4. Enter a name to identify this app:
   - For development: `Tennis Club Dev`
   - For production: `Tennis Club Production`

5. Click **"Generate"**

6. Google will show you a 16-character password like: `abcd efgh ijkl mnop`

7. **Copy this password** (you won't be able to see it again)
   - Remove the spaces when you paste it: `abcdefghijklmnop`

8. Click **"Done"**

### Important Notes

- Each App Password is unique and tied to a specific device/app
- You can create separate App Passwords for development and production
- You can revoke an App Password anytime from the same page
- If you lose an App Password, just generate a new one

---

## Local Development Setup

### Step 1: Configure Your .env File

1. Open your `.env` file in the project root

2. Find the email configuration section:

```bash
# Email Configuration (SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@tennisclub.de
```

3. Fill in your Gmail credentials:

```bash
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcdefghijklmnop  # Your 16-character app password (no spaces)
```

### Step 2: Test Your Configuration

Run the test email command:

```bash
flask test-email your-email@gmail.com
```

You should see:

```
✓ Email configuration test successful!
  Test email sent to: your-email@gmail.com
  Check your inbox to confirm receipt.
```

### Step 3: Verify Email Receipt

1. Check your inbox for the test email
2. The email should come from `noreply@tennisclub.de`
3. Subject: "Tennis Club - Email Configuration Test"

### Optional: Disable Email for Local Development

If you don't want to set up email for local testing:

1. Leave `MAIL_USERNAME` and `MAIL_PASSWORD` empty:

```bash
MAIL_USERNAME=
MAIL_PASSWORD=
```

2. The application will continue to work, but emails won't be sent
3. Email failures will be logged but won't crash the app

---

## Production Setup (PythonAnywhere)

### Step 1: Create .env.production File

1. Copy the `.env.production.example` template:

```bash
cp .env.production.example .env.production
```

2. Edit `.env.production` with your production settings

### Step 2: Configure Production Email

Open `.env.production` and configure:

```bash
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USE_SSL=false
MAIL_USERNAME=your-production-email@gmail.com
MAIL_PASSWORD=your-production-app-password
MAIL_DEFAULT_SENDER=noreply@tennisclub.de
```

**Important Security Notes:**

- Use a **different** Gmail account or App Password for production
- **Never** commit `.env.production` to version control (it's in .gitignore)
- Store the production App Password securely (password manager)

### Step 3: Upload to PythonAnywhere

1. Upload `.env.production` to your PythonAnywhere project directory:
   - Use the Files tab in PythonAnywhere web interface
   - Or use `scp` to upload the file
   - Place it in: `/home/YOUR_USERNAME/tcz/.env.production`

2. Verify the file is in the correct location:

```bash
# In PythonAnywhere Bash console
cd ~/tcz
ls -la .env.production
```

### Step 4: Verify WSGI Configuration

The `wsgi.py` file should already be configured to load `.env` files:

```python
# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()  # Loads .env in development
except ImportError:
    pass
```

For production, ensure your PythonAnywhere WSGI file points to the correct environment.

### Step 5: Reload Your Web App

1. Go to your PythonAnywhere Web tab
2. Click the green **"Reload"** button
3. Wait for the reload to complete

### Step 6: Test Production Email

In a PythonAnywhere Bash console:

```bash
cd ~/tcz
source ~/.virtualenvs/tennisclub/bin/activate
export FLASK_APP=wsgi.py
flask test-email your-email@gmail.com
```

### Step 7: Test with Real Reservation

1. Create a test reservation on your production site
2. Check that confirmation emails are received
3. Verify both `booked_for` and `booked_by` members receive emails

---

## Testing Email Configuration

### CLI Test Command

The `flask test-email` command sends a test email and displays configuration info:

```bash
flask test-email recipient@example.com
```

**Output (Success):**

```
Email Configuration:
  Server: smtp.gmail.com:587
  TLS: Enabled
  Username: your-email@gmail.com
  Default Sender: noreply@tennisclub.de

✓ Email configuration test successful!
  Test email sent to: recipient@example.com
  Check your inbox to confirm receipt.
```

**Output (Not Configured):**

```
Email Configuration:
  Server: smtp.gmail.com:587
  TLS: Enabled
  Username: Not configured
  Default Sender: noreply@tennisclub.de

⚠ Email is not configured
  Set MAIL_USERNAME and MAIL_PASSWORD to enable email notifications.
```

### Testing Through the Application

1. **Create a Reservation:**
   - Log in to the application
   - Create a new court reservation
   - Both members should receive "Booking Created" email

2. **Modify a Reservation:**
   - Edit an existing reservation
   - Both members should receive "Booking Modified" email

3. **Cancel a Reservation:**
   - Cancel a reservation
   - Both members should receive "Booking Cancelled" email

---

## Troubleshooting

### "Authentication failed" Error

**Symptom:** Email sending fails with authentication error

**Solutions:**

1. Verify you're using an App Password, not your regular Gmail password
2. Check that 2-Step Verification is enabled
3. Ensure no spaces in the App Password
4. Generate a new App Password and try again

### "Connection refused" Error

**Symptom:** Cannot connect to SMTP server

**Solutions:**

1. Check your internet connection
2. Verify SMTP settings:
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   ```
3. Try with a different network (corporate firewalls may block SMTP)

### Emails Not Being Received

**Symptom:** No error shown but emails don't arrive

**Solutions:**

1. Check your spam/junk folder
2. Verify the recipient email address is correct
3. Check if Gmail is marking the emails as spam
4. Try sending to a different email address

### "MAIL_USERNAME not configured" Warning

**Symptom:** Warning message when testing email

**Solution:**

This is normal if you haven't configured email yet. Either:
- Set up Gmail App Password (see above)
- Or leave it empty to disable email (app still works)

### PythonAnywhere Specific Issues

**Symptom:** Emails work locally but not on PythonAnywhere

**Solutions:**

1. Verify `.env.production` file exists in the project directory
2. Check that `dotenv` is installed: `pip show python-dotenv`
3. Ensure web app has been reloaded after changing .env files
4. Check error logs: `/var/log/YOUR_USERNAME.pythonanywhere.com.error.log`
5. Run `flask test-email` from PythonAnywhere Bash console to see errors

---

## Security Best Practices

### Do's ✓

- **DO** use Gmail App Passwords, never your account password
- **DO** enable 2-Step Verification on your Gmail account
- **DO** use separate App Passwords for development and production
- **DO** keep `.env.production` out of version control (it's in .gitignore)
- **DO** store production credentials securely (password manager)
- **DO** revoke old App Passwords when no longer needed
- **DO** use a dedicated Gmail account for production emails (optional but recommended)

### Don'ts ✗

- **DON'T** commit `.env` or `.env.production` files to Git
- **DON'T** use your main Gmail password
- **DON'T** share App Passwords with others
- **DON'T** reuse the same App Password across multiple applications
- **DON'T** hardcode credentials in source code
- **DON'T** disable 2-Step Verification after setting up App Passwords

### Credential Management

**Local Development:**
- Store in `.env` file (gitignored)
- Can use a test Gmail account
- OK to use the same account for multiple developers' local testing

**Production:**
- Store in `.env.production` file (gitignored)
- Use a dedicated Gmail account for the production application
- Consider using: `tennisclub@yourdomain.com` or similar
- Store credentials in a password manager
- Document where production credentials are stored (for team handoff)

### Revoking Access

If an App Password is compromised:

1. Go to [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Click the trash icon next to the compromised App Password
3. Generate a new App Password
4. Update your `.env` or `.env.production` file
5. Reload the application (or restart Flask locally)

---

## Email Templates

The application sends German language emails with the following structure:

### Booking Created Email

```
Subject: Buchungsbestätigung - Tennisplatz {court_number}

Hallo {member_name},

Ihre Buchung wurde erfolgreich erstellt:

Platz: {court_number}
Datum: {date}
Uhrzeit: {start_time} - {end_time}
Gebucht für: {booked_for_name}
Gebucht von: {booked_by_name}

Mit freundlichen Grüßen
Ihr Tennisclub-Team
```

### Booking Modified Email

```
Subject: Buchungsänderung - Tennisplatz {court_number}

Hallo {member_name},

Ihre Buchung wurde geändert:
[Details...]
```

### Booking Cancelled Email

```
Subject: Buchungsstornierung - Tennisplatz {court_number}

Hallo {member_name},

Ihre Buchung wurde storniert:
[Details...]
```

---

## Support

If you continue to have issues with email setup:

1. Check the application logs for detailed error messages
2. Verify all configuration settings match this guide
3. Try the troubleshooting steps above
4. Contact your system administrator

---

## Additional Resources

- [Gmail App Passwords Documentation](https://support.google.com/accounts/answer/185833)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)
- [PythonAnywhere Help](https://help.pythonanywhere.com/)

---

**Last Updated:** 2026-01-07
