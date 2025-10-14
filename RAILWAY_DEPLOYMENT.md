# Railway Backend Deployment Guide

## Files Created for Railway Deployment

1. **railway.json** - Railway-specific configuration
2. **Procfile** - Process definitions for Railway
3. **nixpacks.toml** - Build configuration

## Deployment Steps

### 1. Connect to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select this repository

### 2. Configure Environment Variables
In Railway dashboard, add these environment variables:

**Required:**
```
SECRET_KEY=your-production-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://... (Railway will provide this)
```

**Payment Configuration:**
```
PAYSTACK_PUBLIC_KEY=pk_live_your_live_key
PAYSTACK_SECRET_KEY=sk_live_your_live_key
PAYSTACK_WEBHOOK_URL=https://your-app.railway.app/api/payments/paystack/webhook/

MTN_MOMO_ENVIRONMENT=production
MTN_MOMO_BASE_URL=https://momodeveloper.mtn.com
MTN_MOMO_COLLECTION_USER_ID=your-production-user-id
MTN_MOMO_COLLECTION_API_KEY=your-production-api-key
MTN_MOMO_COLLECTION_SUBSCRIPTION_KEY=your-production-subscription-key
MTN_MOMO_CALLBACK_URL=https://your-app.railway.app/api/payments/mtn-momo/webhook/
```

**Site Configuration:**
```
BASE_URL=https://your-app.railway.app
SITE_NAME=Trails & Trails
```

### 3. Add PostgreSQL Database
1. In Railway dashboard, click "New" → "Database" → "PostgreSQL"
2. Railway will automatically set the DATABASE_URL environment variable

### 4. Deploy
1. Railway will automatically deploy when you push to your main branch
2. The build process will:
   - Install Python dependencies from Tback/requirements.txt
   - Run collectstatic for static files
   - Start the Django app with Gunicorn

### 5. Run Migrations
After first deployment, you may need to run migrations:
1. Go to Railway dashboard → Your service → "Deploy" tab
2. Click "View Logs" to see if migrations ran automatically
3. If needed, you can run migrations manually via Railway CLI

## Important Notes

- The app is configured to serve only the backend (Tback folder)
- Static files are handled by WhiteNoise
- CORS is configured to allow your frontend domain
- Database will use PostgreSQL in production, SQLite locally
- All webhook URLs should point to your Railway domain

## Health Check
Your app will be available at: `https://your-app.railway.app/api/health/`

## Frontend Integration
Update your frontend to point to: `https://your-app.railway.app/api/`