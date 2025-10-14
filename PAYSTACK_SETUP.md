# Paystack Ghana Integration Setup Guide

This guide will help you set up Paystack Ghana for both mobile money and card payments on your Tails & Trails platform.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
cd Tback
pip install paystackapi==2.1.0
```

### 2. Get Paystack API Keys

1. Sign up at [Paystack Ghana](https://paystack.com/gh)
2. Complete your business verification
3. Go to Settings > API Keys & Webhooks
4. Copy your **Test** keys for development:
   - Public Key (starts with `pk_test_`)
   - Secret Key (starts with `sk_test_`)

### 3. Configure Environment Variables

Update your `Tback/.env` file:

```env
# Paystack Configuration (Ghana)
PAYSTACK_PUBLIC_KEY=pk_test_your_actual_paystack_public_key_here
PAYSTACK_SECRET_KEY=sk_test_your_actual_paystack_secret_key_here
PAYSTACK_WEBHOOK_URL=http://localhost:8000/api/payments/paystack/webhook/
```

### 4. Run Database Migrations

```bash
cd Tback
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the Servers

**Backend:**
```bash
cd Tback
python manage.py runserver
```

**Frontend:**
```bash
cd Tfront
npm run dev
```

## 💳 Payment Methods Supported

### Mobile Money
- **MTN Mobile Money** - Most popular in Ghana
- **Vodafone Cash** - Wide coverage
- **AirtelTigo Money** - Good alternative

### Card Payments
- **Visa** - Local and international
- **Mastercard** - Local and international  
- **Verve** - Nigerian cards accepted

## 🔧 API Endpoints

### Create Payment
```
POST /api/payments/paystack/create/
```

**Request Body:**
```json
{
  "amount": 100.00,
  "email": "customer@example.com",
  "payment_method": "card", // or "mobile_money"
  "provider": "mtn", // for mobile money only
  "phone_number": "+233241234567", // for mobile money only
  "description": "Tour booking payment"
}
```

### Verify Payment
```
GET /api/payments/paystack/verify/{reference}/
```

### Webhook Endpoint
```
POST /api/payments/paystack/webhook/
```

## 🎯 Frontend Integration

### Card Payments
Users are redirected to Paystack's secure payment page:
1. Navigate to `/paystack-checkout`
2. Fill in customer details
3. Redirect to Paystack
4. Return to `/payment-callback` for verification

### Mobile Money Payments
Direct mobile money integration:
1. Navigate to `/momo-checkout` 
2. Select provider (MTN, Vodafone, AirtelTigo)
3. Enter phone number
4. Receive prompt on phone
5. Authorize payment

## 🔒 Security Features

- **PCI DSS Compliant** - Paystack handles card data securely
- **3D Secure** - Additional authentication for cards
- **Webhook Verification** - Secure payment notifications
- **Encrypted Communication** - All API calls use HTTPS

## 📱 Mobile Money Flow

1. **Customer selects Mobile Money**
2. **Enters phone number and provider**
3. **Backend calls Paystack API**
4. **Customer receives USSD prompt**
5. **Customer enters PIN to authorize**
6. **Webhook confirms payment**
7. **Customer redirected to success page**

## 💡 Testing

### Test Card Numbers (Paystack Ghana)
```
Success: 4084084084084081
Decline: 4084084084084099
Insufficient Funds: 4084084084084107
```

### Test Mobile Money
Use any valid Ghana mobile number in test mode. Paystack will simulate the payment flow.

## 🚨 Production Setup

### 1. Switch to Live Keys
Replace test keys with live keys in `.env`:
```env
PAYSTACK_PUBLIC_KEY=pk_live_your_live_public_key
PAYSTACK_SECRET_KEY=sk_live_your_live_secret_key
```

### 2. Configure Webhooks
In Paystack Dashboard:
1. Go to Settings > API Keys & Webhooks
2. Add webhook URL: `https://yourdomain.com/api/payments/paystack/webhook/`
3. Select events: `charge.success`, `charge.failed`

### 3. Update CORS Settings
Update `settings.py` for production:
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
]
CORS_ALLOW_ALL_ORIGINS = False  # Set to False in production
```

## 📊 Payment Flow Diagram

```
Customer → Select Payment Method → Paystack → Authorization → Webhook → Success Page
    ↓              ↓                  ↓           ↓            ↓          ↓
  Browse         Card/MoMo         Secure       Phone/PIN    Backend    Confirmation
   Tours         Details           Payment       Prompt      Update     & Receipt
```

## 🛠 Troubleshooting

### Common Issues

1. **"Invalid API Key"**
   - Check your `.env` file has correct keys
   - Ensure no extra spaces in the keys

2. **"Payment not found"**
   - Verify payment reference is correct
   - Check database for payment record

3. **Mobile Money not working**
   - Ensure phone number format: `+233XXXXXXXXX`
   - Check provider code: `mtn`, `vodafone`, `airteltigo`

4. **Webhook not received**
   - Verify webhook URL is accessible
   - Check Paystack dashboard for webhook logs

### Debug Mode
Enable debug logging in `settings.py`:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'payments': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📞 Support

- **Paystack Support:** [support@paystack.com](mailto:support@paystack.com)
- **Documentation:** [https://paystack.com/docs](https://paystack.com/docs)
- **Ghana Specific:** [https://paystack.com/gh/developers](https://paystack.com/gh/developers)

## ✅ Checklist

- [ ] Paystack account created and verified
- [ ] API keys configured in `.env`
- [ ] Dependencies installed
- [ ] Database migrated
- [ ] Test payments working
- [ ] Webhooks configured
- [ ] Mobile money tested
- [ ] Card payments tested
- [ ] Production keys ready (for live deployment)

Your Paystack Ghana integration is now ready! 🎉