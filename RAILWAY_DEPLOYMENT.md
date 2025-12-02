# Railway Deployment Checklist

## Environment Variables on Railway

Make sure these are set in your Railway project settings:

### Required Paystack Variables
```
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxxx (or sk_live_ for production)
PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxxx (or pk_live_ for production)
PAYSTACK_WEBHOOK_SECRET=xxxxxxxxxxxxx (optional, for webhook verification)
```

### Other Required Variables
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-railway-domain.up.railway.app,yourdomain.com
DATABASE_URL=postgresql://... (Railway provides this automatically)
```

## Deployment Steps

### 1. Push Code to GitHub
```bash
git add -A
git commit -m "Your commit message"
git push origin main
```
✅ Already done!

### 2. Railway Auto-Deploy
Railway will automatically detect the push and start deploying.

### 3. Run Database Setup (After Deploy)

SSH into Railway or use Railway CLI:

```bash
# Install Railway CLI if needed
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run migrations
railway run python Tback/manage.py migrate

# Create Paystack provider
railway run python Tback/setup_paystack_provider.py

# Create superuser (if needed)
railway run python Tback/manage.py createsuperuser
```

### 4. Verify Deployment

#### Check Backend
- Visit: `https://your-backend.up.railway.app/api/`
- Should see API endpoints list

#### Check Paystack Provider
- Visit: `https://your-backend.up.railway.app/api/payments/providers/`
- Should see Paystack in the list

#### Check Payment Methods
- Visit: `https://your-backend.up.railway.app/api/payments/checkout/methods/`
- Should see Paystack payment method

### 5. Test Payment Flow

1. Go to your frontend: `https://your-frontend.vercel.app`
2. Navigate to a tour booking page
3. Click "Proceed to Payment"
4. Should redirect to Paystack's payment page
5. Use test card: `4084 0840 8408 4081`
6. Complete payment
7. Should redirect back with success

## Troubleshooting

### "Payment provider not available"
```bash
# Run the setup script
railway run python Tback/setup_paystack_provider.py
```

### "Failed to initialize Paystack payment"
- Check that `PAYSTACK_SECRET_KEY` is set on Railway
- Check Railway logs: `railway logs`
- Verify the key starts with `sk_test_` or `sk_live_`

### CORS Errors
Make sure `ALLOWED_HOSTS` and CORS settings include your frontend domain:
```python
# In settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend.vercel.app",
    "http://localhost:5000",
]
```

### Database Connection Issues
Railway provides `DATABASE_URL` automatically. Make sure it's being used in settings.py:
```python
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}
```

## Frontend Environment Variables (Vercel)

Make sure your frontend has:
```
VITE_API_URL=https://your-backend.up.railway.app/api
```

## Production Checklist

When going live:

- [ ] Switch to live Paystack keys (`sk_live_` and `pk_live_`)
- [ ] Set `DEBUG=False` on Railway
- [ ] Configure custom domain
- [ ] Set up Paystack webhook: `https://yourdomain.com/api/payments/paystack/webhook/`
- [ ] Enable webhook events in Paystack dashboard:
  - `charge.success`
  - `charge.failed`
- [ ] Test with real card (small amount)
- [ ] Set up SSL certificate (Railway provides this automatically)
- [ ] Update `ALLOWED_HOSTS` with production domain
- [ ] Update CORS settings with production frontend URL
- [ ] Monitor Railway logs for errors
- [ ] Set up error tracking (Sentry, etc.)

## Useful Railway Commands

```bash
# View logs
railway logs

# Run Django shell
railway run python Tback/manage.py shell

# Run migrations
railway run python Tback/manage.py migrate

# Create superuser
railway run python Tback/manage.py createsuperuser

# Check environment variables
railway variables

# Restart service
railway restart
```

## Support

- Railway Docs: https://docs.railway.app
- Paystack Docs: https://paystack.com/docs
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

## Quick Test Script

Run this to verify everything is working:

```bash
# Test API is accessible
curl https://your-backend.up.railway.app/api/

# Test Paystack provider exists
curl https://your-backend.up.railway.app/api/payments/providers/

# Test payment methods endpoint
curl https://your-backend.up.railway.app/api/payments/checkout/methods/
```

All endpoints should return JSON responses without errors.
