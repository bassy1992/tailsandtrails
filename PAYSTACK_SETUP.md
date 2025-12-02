# Paystack Payment Setup Guide

## Quick Start

The payment system now uses **Paystack only** - no more Mobile Money integration needed. Paystack handles all payment methods including cards, mobile money, bank transfers, and USSD.

## What Changed

### Removed
- ❌ Mobile Money payment method selection
- ❌ MTN MoMo direct integration
- ❌ Payment method radio buttons
- ❌ Multiple payment provider logic

### Added
- ✅ Single Paystack integration for all payments
- ✅ Redirect to Paystack's hosted payment page
- ✅ Payment callback handler
- ✅ Automatic payment verification

## Setup Steps

### 1. Get Paystack API Keys

1. Sign up at [paystack.com](https://paystack.com)
2. Go to Settings → API Keys & Webhooks
3. Copy your keys:
   - Secret Key (starts with `sk_test_` or `sk_live_`)
   - Public Key (starts with `pk_test_` or `pk_live_`)

### 2. Configure Backend

Add to `Tback/.env`:
```bash
PAYSTACK_SECRET_KEY=sk_test_your_secret_key_here
PAYSTACK_PUBLIC_KEY=pk_test_your_public_key_here
PAYSTACK_WEBHOOK_SECRET=your_webhook_secret_here
```

### 3. Set Up Webhook (Production Only)

1. In Paystack Dashboard → Settings → Webhooks
2. Add webhook URL: `https://yourdomain.com/api/payments/paystack/webhook/`
3. Enable events:
   - `charge.success`
   - `charge.failed`

### 4. Test the Integration

#### Using Test Cards
```
Card Number: 4084 0840 8408 4081
CVV: 408
Expiry: Any future date
PIN: 0000
OTP: 123456
```

#### Test Flow
1. Go to booking page: `http://localhost:5000/booking/1`
2. Select travelers and options
3. Click "Proceed to Payment"
4. You'll be redirected to Paystack
5. Enter test card details
6. Complete payment
7. You'll be redirected back with confirmation

## Payment Flow

```
User clicks "Proceed to Payment"
         ↓
Backend creates payment record
         ↓
Backend calls Paystack API to initialize
         ↓
User redirected to Paystack's page
         ↓
User completes payment on Paystack
         ↓
Paystack redirects to /payment-callback
         ↓
Backend verifies payment with Paystack
         ↓
User sees success page
```

## Supported Payment Methods

Paystack automatically provides:
- 💳 **Cards**: Visa, Mastercard, Verve
- 📱 **Mobile Money**: MTN, Vodafone, AirtelTigo
- 🏦 **Bank Transfer**: Direct transfers
- 📞 **USSD**: Bank USSD codes
- 📷 **QR Code**: Scan to pay

Users choose their method on Paystack's page.

## API Endpoints

### Frontend Calls
- `POST /api/payments/checkout/create/` - Create payment
- `POST /api/payments/paystack/initialize/` - Get Paystack URL
- `GET /api/payments/paystack/verify/{ref}/` - Verify payment

### Paystack Calls (Webhook)
- `POST /api/payments/paystack/webhook/` - Payment updates

## Troubleshooting

### "Payment provider not available"
- Check that Paystack provider exists in database
- Run: `python manage.py shell` then check `PaymentProvider.objects.filter(code='paystack')`

### "Failed to initialize Paystack payment"
- Verify `PAYSTACK_SECRET_KEY` is set in `.env`
- Check backend logs for Paystack API errors
- Ensure amount is valid (minimum 100 kobo = 1 GHS)

### Payment stuck on "Verifying"
- Check if webhook is configured (production)
- Manually verify: `GET /api/payments/paystack/verify/{reference}/`
- Check backend logs for verification errors

### User not redirected back
- Verify callback URL is correct: `http://localhost:5000/payment-callback`
- Check browser console for errors
- Ensure reference is in URL: `?reference=PAY_xxxxx`

## Testing Checklist

- [ ] Payment creation works
- [ ] Redirect to Paystack works
- [ ] Can complete payment with test card
- [ ] Redirect back to callback works
- [ ] Payment verification works
- [ ] Success page shows correct details
- [ ] Failed payment shows error message
- [ ] Booking details stored correctly

## Production Checklist

- [ ] Switch to live API keys (`sk_live_` and `pk_live_`)
- [ ] Configure webhook URL in Paystack dashboard
- [ ] Test with real card (small amount)
- [ ] Verify webhook receives events
- [ ] Set up SSL certificate (required by Paystack)
- [ ] Update callback URL to production domain
- [ ] Test refund functionality
- [ ] Monitor Paystack dashboard for transactions

## Support

- Paystack Docs: https://paystack.com/docs
- Paystack Support: support@paystack.com
- Test Cards: https://paystack.com/docs/payments/test-payments
