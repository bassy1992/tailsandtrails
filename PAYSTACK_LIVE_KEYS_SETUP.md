# Switching from Paystack Test Keys to Live Keys

## Current Status
You're currently using **TEST KEYS**:
- Public Key: `pk_test_ad2c643f10aafac35eda3a819810934b137892f1`
- Secret Key: `sk_test_26d017072e1c9bc8709b3324665ee8f490bde3dd`

## Steps to Switch to Live Keys

### Step 1: Get Your Live Keys from Paystack

1. **Log in to Paystack Dashboard**
   - Go to: https://dashboard.paystack.com/
   - Use your Paystack account credentials

2. **Navigate to Settings**
   - Click on **Settings** in the left sidebar
   - Click on **API Keys & Webhooks**

3. **Switch to Live Mode**
   - At the top of the page, you'll see a toggle between **Test** and **Live**
   - Click on **Live** mode

4. **Copy Your Live Keys**
   - **Public Key**: Starts with `pk_live_...`
   - **Secret Key**: Starts with `sk_live_...` (click "Show" to reveal it)
   
   ⚠️ **IMPORTANT**: Keep your secret key secure! Never share it publicly or commit it to GitHub.

### Step 2: Update Backend Environment Variables

#### Option A: Update Railway Environment Variables (Recommended for Production)

1. Go to your Railway dashboard: https://railway.app/
2. Select your backend project
3. Go to **Variables** tab
4. Update these variables:
   ```
   PAYSTACK_PUBLIC_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLIC_KEY
   PAYSTACK_SECRET_KEY=sk_live_YOUR_ACTUAL_LIVE_SECRET_KEY
   ```
5. Click **Save** - Railway will automatically redeploy

#### Option B: Update Local .env File (For Local Testing)

Edit `Tback/.env`:
```env
# Paystack Configuration (Ghana) - LIVE KEYS
PAYSTACK_PUBLIC_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLIC_KEY
PAYSTACK_SECRET_KEY=sk_live_YOUR_ACTUAL_LIVE_SECRET_KEY
PAYSTACK_WEBHOOK_URL=https://tailsandtrails-production.up.railway.app/api/payments/paystack/webhook/
```

### Step 3: Update Frontend Environment Variables

#### Update Vercel Environment Variables

1. Go to your Vercel dashboard: https://vercel.com/
2. Select your frontend project (tfront)
3. Go to **Settings** → **Environment Variables**
4. Update or add:
   ```
   VITE_PAYSTACK_PUBLIC_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLIC_KEY
   ```
5. Click **Save**
6. Redeploy your frontend:
   ```bash
   cd Tfront
   vercel --prod
   ```

### Step 4: Configure Paystack Webhook (IMPORTANT!)

1. In Paystack Dashboard (Live Mode)
2. Go to **Settings** → **API Keys & Webhooks**
3. Scroll down to **Webhook URL**
4. Enter your webhook URL:
   ```
   https://tailsandtrails-production.up.railway.app/api/payments/paystack/webhook/
   ```
5. Click **Save**
6. Copy the **Webhook Secret** (if provided)

### Step 5: Verify Business Information

Before going live, ensure your Paystack account is fully verified:

1. **Business Information**
   - Go to **Settings** → **Business Information**
   - Ensure all details are complete and verified

2. **Bank Account**
   - Go to **Settings** → **Settlement Account**
   - Add your bank account for receiving payments
   - Verify the account

3. **KYC Documents**
   - Upload required documents (Business registration, ID, etc.)
   - Wait for Paystack approval (usually 1-3 business days)

### Step 6: Test Live Payments

⚠️ **IMPORTANT**: Test with small amounts first!

1. **Test Card Payment**
   - Use a real card with a small amount (e.g., GH₵1)
   - Complete the payment flow
   - Verify booking is created
   - Check if confirmation email is sent

2. **Test Mobile Money Payment**
   - Use a real mobile money number
   - Test with a small amount (e.g., GH₵1)
   - Approve the payment on your phone
   - Verify booking is created

3. **Check Paystack Dashboard**
   - Go to **Transactions** in Paystack dashboard
   - Verify the test transaction appears
   - Check transaction status

### Step 7: Monitor First Real Transactions

1. **Watch Backend Logs**
   ```bash
   # In Railway dashboard
   # Go to your backend project → Deployments → View Logs
   ```

2. **Check for These Log Messages**
   - "Payment initialized successfully"
   - "Payment status updated via verification"
   - "Auto-created booking for successful payment"
   - "Booking confirmation email sent"

3. **Verify in Database**
   - Check admin panel: `/admin/payments/payment/`
   - Verify bookings are created
   - Check email logs

## Important Differences: Test vs Live

| Feature | Test Mode | Live Mode |
|---------|-----------|-----------|
| **Keys** | `pk_test_...` / `sk_test_...` | `pk_live_...` / `sk_live_...` |
| **Payments** | Simulated (no real money) | Real money transactions |
| **Cards** | Test cards only | Real cards only |
| **Mobile Money** | Simulated approval | Real phone approval required |
| **Settlement** | No actual payout | Money settled to your bank |
| **Fees** | No fees charged | Paystack fees apply |

## Paystack Fees (Ghana)

When using live keys, Paystack charges:
- **Local Cards**: 1.95% capped at GH₵10
- **International Cards**: 3.9% + GH₵1
- **Mobile Money**: 1.5% (no cap)

## Rollback Plan

If you need to switch back to test mode:

1. **Update Environment Variables**
   ```
   PAYSTACK_PUBLIC_KEY=pk_test_ad2c643f10aafac35eda3a819810934b137892f1
   PAYSTACK_SECRET_KEY=sk_test_26d017072e1c9bc8709b3324665ee8f490bde3dd
   ```

2. **Redeploy**
   - Railway will auto-redeploy backend
   - Redeploy frontend: `vercel --prod`

## Security Checklist

Before going live, ensure:

- [ ] Live secret key is stored in Railway environment variables (not in code)
- [ ] Live secret key is NOT committed to GitHub
- [ ] `.env` file is in `.gitignore`
- [ ] Webhook URL is configured in Paystack dashboard
- [ ] SSL/HTTPS is enabled on your domain
- [ ] Business information is verified in Paystack
- [ ] Bank account is added for settlements
- [ ] Test transactions completed successfully

## Troubleshooting

### Issue: "Invalid API Key"
**Solution**: Double-check you copied the correct live keys from Paystack dashboard

### Issue: "Payment fails immediately"
**Solution**: 
- Verify your Paystack account is fully verified
- Check if business information is complete
- Ensure you're not using test cards in live mode

### Issue: "Webhook not receiving events"
**Solution**:
- Verify webhook URL in Paystack dashboard
- Check Railway logs for incoming webhook requests
- Ensure webhook URL is accessible (test with curl)

### Issue: "Mobile Money not working"
**Solution**:
- Ensure you're using a real Ghana mobile money number
- Check if the number is registered for mobile money
- Verify the provider (MTN, Vodafone, AirtelTigo) is correct

## Support

If you encounter issues:
1. Check Paystack documentation: https://paystack.com/docs/
2. Contact Paystack support: support@paystack.com
3. Check Railway logs for backend errors
4. Review `PAYMENT_CONFIRMATION_FIX.md` for payment flow details

## Quick Reference

**Current Setup (Test)**:
```env
PAYSTACK_PUBLIC_KEY=pk_test_ad2c643f10aafac35eda3a819810934b137892f1
PAYSTACK_SECRET_KEY=sk_test_26d017072e1c9bc8709b3324665ee8f490bde3dd
```

**Live Setup (Replace with your actual keys)**:
```env
PAYSTACK_PUBLIC_KEY=pk_live_YOUR_ACTUAL_LIVE_PUBLIC_KEY
PAYSTACK_SECRET_KEY=sk_live_YOUR_ACTUAL_LIVE_SECRET_KEY
```

---

**Ready to go live?** Follow the steps above carefully and test thoroughly before announcing to customers!
