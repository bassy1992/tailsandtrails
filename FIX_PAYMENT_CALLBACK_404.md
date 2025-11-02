# Fix Payment Callback 404 Error

## Problem
Paystack is redirecting to `https://tfront-two.vercel.app/payment-callback` which returns a 404 error because that deployment no longer exists.

## Root Cause
The `FRONTEND_URL` in your backend settings was set to `tfront-two.vercel.app` which is an old/deleted Vercel deployment.

## Solution

### Step 1: Update Backend Settings (DONE)
I've updated `Tback/tback_api/settings.py` to use `https://tfront.vercel.app` as the default.

### Step 2: Update Railway Environment Variable

1. Go to Railway dashboard: https://railway.app/
2. Select your backend project
3. Go to **Variables** tab
4. Add or update this variable:
   ```
   FRONTEND_URL=https://www.talesandtrailsghana.com
   ```
5. Click **Save** - Railway will automatically redeploy

### Step 3: Set Up Vercel Production Domain (Recommended)

To avoid this issue in the future, set up a stable production domain in Vercel:

#### Option A: Use Vercel's Default Production URL
1. Go to Vercel dashboard
2. Select your `tfront` project
3. Go to **Settings** → **Domains**
4. Your production URL should be: `tfront.vercel.app`
5. This URL is stable and won't change with deployments

#### Option B: Add a Custom Domain (Best for Production)
1. Buy a domain (e.g., `tailsandtrails.com`)
2. In Vercel dashboard → Settings → Domains
3. Click **Add Domain**
4. Enter your domain (e.g., `tailsandtrails.com`)
5. Follow DNS configuration instructions
6. Update Railway `FRONTEND_URL` to your custom domain

### Step 4: Test the Fix

1. **Make a test payment**:
   - Go to your site
   - Start a booking or ticket purchase
   - Complete payment on Paystack

2. **Verify redirect**:
   - After payment, you should be redirected to:
     `https://tfront.vercel.app/payment-callback?reference=PAY-...`
   - NOT to `tfront-two.vercel.app`

3. **Check confirmation page**:
   - Should see payment verification screen
   - Then redirect to success page
   - Booking should be created
   - Email should be sent

## Current URLs

### Frontend
- **Production Custom Domain**: `https://www.talesandtrailsghana.com` ✅ (PRIMARY - Use this)
- **Vercel URL**: `https://tfront.vercel.app` ✅ (Backup)
- **Project URL**: `https://tfront-bassys-projects-fca17413.vercel.app` ✅ (Also works)
- **Old URL**: `https://tfront-two.vercel.app` ❌ (Don't use - deleted)

### Backend (Railway)
- **Production URL**: `https://tailsandtrails-production.up.railway.app` ✅

## Verification Commands

### Check Current FRONTEND_URL in Railway
```bash
# In Railway dashboard, go to Variables tab
# Look for FRONTEND_URL value
```

### Test Payment Callback URL
```bash
# The callback URL should be:
https://www.talesandtrailsghana.com/payment-callback

# NOT:
https://tfront-two.vercel.app/payment-callback
```

## Quick Fix Checklist

- [x] Updated `settings.py` default FRONTEND_URL
- [ ] Update Railway `FRONTEND_URL` environment variable
- [ ] Commit and push changes
- [ ] Wait for Railway to redeploy
- [ ] Test a payment to verify redirect works

## After Fix

Once fixed, the payment flow will be:
1. User completes payment on Paystack
2. Paystack redirects to: `https://www.talesandtrailsghana.com/payment-callback?reference=PAY-...`
3. PaymentCallback page verifies payment
4. Creates booking/ticket purchase
5. Sends confirmation email
6. Redirects to success page

## Troubleshooting

### Still getting 404?
- Clear browser cache
- Check Railway logs to see what FRONTEND_URL is being used
- Verify Railway environment variable is set correctly
- Wait 2-3 minutes for Railway to fully redeploy

### Redirect goes to wrong URL?
- Check Paystack dashboard for any hardcoded callback URLs
- Verify no old callback URLs are cached
- Test with a new payment (new reference)

### Payment succeeds but no booking created?
- Check Railway logs for errors
- Verify payment signal is running
- Check `PAYMENT_CONFIRMATION_FIX.md` for booking creation issues

## Prevention

To prevent this in the future:

1. **Use custom domain**: Always use `www.talesandtrailsghana.com` for production
2. **Set environment variables**: Don't rely on defaults in code
3. **Monitor deployments**: Check that new deployments don't break URLs
4. **Keep domain stable**: Custom domains don't change with deployments

## Support

If issues persist:
- Check Railway logs: `railway logs`
- Check Vercel logs in dashboard
- Review payment in admin: `/admin/payments/payment/`
- Contact: Talesandtrailsghana@gmail.com
