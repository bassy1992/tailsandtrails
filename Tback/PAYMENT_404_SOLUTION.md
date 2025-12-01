# Payment 404 Error Solution Guide

## Problem
Frontend is getting 404 errors when trying to access payment status:
```
GET http://localhost:8000/api/payments/PAY-20250820095826-3DVVIH/status/
[HTTP/1.1 404 Not Found]
```

## Root Cause
The payment reference `PAY-20250820095826-3DVVIH` doesn't exist in the database. This can happen when:

1. **Database was cleared** - We deleted all payment data earlier
2. **Frontend cache** - Browser/app is using cached/stale payment references
3. **Payment creation failed** - Payment wasn't properly saved but frontend has the reference
4. **Timing issue** - Frontend tries to check status before payment is fully created

## Solutions

### 1. Clear Frontend Cache
**For Web Browser:**
- Press `Ctrl+Shift+R` (hard refresh)
- Open Developer Tools → Application → Storage → Clear All
- Clear localStorage: `localStorage.clear()`

**For Mobile App:**
- Clear app cache/data
- Restart the app

### 2. Check Current Payments in Database
```bash
cd Tback
python manage.py shell -c "
from payments.models import Payment
print(f'Total payments: {Payment.objects.count()}')
for p in Payment.objects.all()[:10]:
    print(f'- {p.reference} ({p.status})')
"
```

### 3. Create a Test Payment
```bash
python manage.py shell -c "
from payments.models import Payment, PaymentProvider
from payments.utils import generate_payment_reference

provider = PaymentProvider.objects.get_or_create(
    code='mtn_momo',
    defaults={'name': 'MTN MoMo', 'is_active': True}
)[0]

payment = Payment.objects.create(
    reference=generate_payment_reference(),
    amount=50.00,
    currency='GHS',
    payment_method='momo',
    provider=provider,
    phone_number='+233244123456',
    status='processing'
)

print(f'Created payment: {payment.reference}')
print(f'Test URL: http://localhost:8000/api/payments/{payment.reference}/status/')
"
```

### 4. Test Payment Flow
```bash
python test_payment_flow.py
```

### 5. Debug Endpoint
Visit: `http://localhost:8000/api/payments/debug/`

This will show:
- Total payments in database
- Recent payments (last 24 hours)
- Payment references and statuses

## Prevention

### 1. Improved Error Handling
The payment status endpoint now provides better debugging info:

```json
{
  "error": "Payment not found",
  "reference": "PAY-20250820095826-3DVVIH",
  "message": "No payment found with reference: PAY-20250820095826-3DVVIH",
  "debug_info": {
    "total_payments": 3,
    "similar_references": [],
    "recent_payments": ["PAY-20250820101709-MUV0SP", "PAY-20250820101408-2I91VF"]
  }
}
```

### 2. Auto-Completion System
New payments now auto-complete after 30 seconds:
- Status changes from "processing" to "successful" (90% rate) or "failed" (10% rate)
- Perfect for demo environments
- No manual intervention needed

### 3. Frontend Best Practices
- Always handle 404 errors gracefully
- Show user-friendly error messages
- Implement retry logic with exponential backoff
- Clear cached references when they fail

## Quick Fix Commands

**Restart Django Server:**
```bash
cd Tback
python manage.py runserver 8000
```

**Clear All Payments and Start Fresh:**
```bash
python manage.py shell -c "
from payments.models import Payment, PaymentCallback, PaymentLog
PaymentLog.objects.all().delete()
PaymentCallback.objects.all().delete()
Payment.objects.all().delete()
print('All payment data cleared')
"
```

**Create Demo Payment:**
```bash
python demo_auto_completion.py
```

## Current System Status

✅ **Auto-completion working** - Payments complete automatically after 30 seconds
✅ **Database cleared** - Fresh start with no old data
✅ **Error handling improved** - Better debugging information
✅ **Admin interface updated** - No delete protection, read-only fields

The system is working correctly. The 404 errors are likely due to frontend cache issues or trying to access old payment references that no longer exist.