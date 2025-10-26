# Render Deployment Guide - Quick Reference

## Your Supabase Database Details

**Connection String:**
```
postgresql://postgres:[YOUR_PASSWORD]@db.lkoiyvnkuaaxpcuimvbw.supabase.co:5432/postgres
```

**Breakdown:**
- Host: `db.lkoiyvnkuaaxpcuimvbw.supabase.co`
- Port: `5432`
- Database: `postgres`
- User: `postgres`
- Password: (You have this from Supabase dashboard)

## Render Deployment Checklist

### Before You Start
- [ ] Code committed to GitHub
- [ ] Supabase database created and connection string saved
- [ ] GitHub repository is public (or Render connected to your GitHub account)

### Step-by-Step Deployment

**1. Push to GitHub (if not already done)**
```bash
git status
git add .
git commit -m "Configure for Render deployment with Supabase"
git push origin main
```

**2. Go to Render Dashboard**
- Visit: https://render.com
- Sign up or log in
- Click **"New +"** → **"Web Service"**

**3. Connect Repository**
- Click **"Connect GitHub"**
- Select your repository: `Hackathon` (or your repo name)
- Render will detect `render.yaml` automatically

**4. Configure Settings**

Render will pre-fill most settings from `render.yaml`. Verify:
- **Name**: `banking-api` (or your preferred name)
- **Region**: Oregon (Free)
- **Branch**: `main`
- **Build Command**: `pip install -r requirements.txt && cd backend && python manage.py collectstatic --no-input && python manage.py migrate`
- **Start Command**: `cd backend && gunicorn backend.wsgi:application --bind 0.0.0.0:$PORT`

**5. Set Environment Variables**

Click **"Environment"** tab and add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://postgres:[YOUR_PASSWORD]@db.lkoiyvnkuaaxpcuimvbw.supabase.co:5432/postgres` |
| `SECRET_KEY` | (Auto-generated - leave as is) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app-name.onrender.com` |

**IMPORTANT**: Replace `[YOUR_PASSWORD]` with your actual Supabase password!

**6. Deploy**
- Click **"Create Web Service"**
- Wait 5-10 minutes for deployment
- Watch build logs for any errors

**7. Verify Deployment**
Once deployed:
- Note your app URL: `https://your-app-name.onrender.com`
- Check build logs show: ✅ Migrations completed
- Check deploy logs show: ✅ Server started

**8. Create Superuser**
- Go to Render dashboard → Your service → **"Shell"** tab
- Run:
```bash
cd backend
python manage.py createsuperuser
```
- Enter email, username, password

**9. Test Your API**

Visit: `https://your-app-name.onrender.com/api/docs/`

You should see the Swagger API documentation!

Test login:
```bash
curl -X POST https://your-app-name.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"your-admin@example.com","password":"YourPassword"}'
```

## Post-Deployment Tasks

### Update README with Live URL
Replace in README.md:
```
- API Base URL: `https://your-banking-api.onrender.com` (will be updated after deployment)
```

With your actual Render URL:
```
- API Base URL: `https://your-actual-app.onrender.com`
```

### Test with Postman
1. Open your Postman collection
2. Update `base_url` environment variable to your Render URL
3. Run all tests to verify production deployment

### Create Test Users on Production
Use the Render shell to create test accounts:
```bash
cd backend
python manage.py shell

# In Python shell:
from accounts.models import User
from banking.models import BankAccount

# Create test customer
user = User.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='Test@123',
    role='customer'
)

# Create bank account
account = BankAccount.objects.create(
    user=user,
    account_number='ACC1234567890',
    balance=10000.00
)
```

## Troubleshooting

### Build Failed
**Error**: "Could not find a version that satisfies..."
- Check `requirements.txt` has correct versions
- Render uses Python 3.9.18 (specified in render.yaml)

### Database Connection Failed
**Error**: "could not connect to server"
- Verify DATABASE_URL is correct
- Check Supabase database is running
- Ensure password has no special characters that need escaping

### Static Files Not Loading
**Error**: 404 on /static/
- Check `ALLOWED_HOSTS` includes your Render domain
- Verify `collectstatic` ran successfully in build logs

### Migrations Failed
**Error**: "No migrations to apply" or migration errors
- Check all migration files are committed to Git
- Run migrations manually via Render shell:
```bash
cd backend
python manage.py migrate --run-syncdb
```

## Performance Notes

**Free Tier Limitations:**
- Render free tier spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds to wake up
- Supabase free tier has connection limits (suitable for demos)

**For Production:**
- Upgrade to Render paid tier ($7/month) for always-on
- Consider connection pooling for Supabase (PgBouncer)

## Next Steps After Deployment

1. ✅ Note your live URL
2. ✅ Update README.md with live URL
3. ✅ Test all API endpoints with Postman
4. ✅ Create demo accounts for hackathon judges
5. ✅ Prepare demo script with live API

## Support

If you encounter issues:
- Render Dashboard → Your Service → "Logs" tab
- Supabase Dashboard → Project → "Database" → "Logs"
- Check this deployment guide for common issues
