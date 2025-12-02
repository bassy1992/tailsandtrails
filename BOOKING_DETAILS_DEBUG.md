# Booking Details Not Showing - Debug Guide

## Current Issue

After payment, the booking details in Django admin show:
- ❌ Adults: 0 (should be 1)
- ❌ Date: Not showing
- ❌ Base price: Not showing

## Root Cause

The booking details ARE being sent from the frontend, but something is wrong with either:
1. The data format being sent
2. The conversion on the backend
3. The storage in the database

## What I've Added

### 1. Enhanced Logging
Added detailed logging in `Tback/payments/views.py` to track:
- What booking_details are received from frontend
- The conversion process
- The final metadata stored

### 2. Debug Scripts
Created scripts to inspect the actual data:
- `Tback/check_latest_payment.py` - Check the most recent payment
- `Tback/inspect_railway_payments.py` - Inspect all payments in Railway

## How to Debug

### Step 1: Deploy Backend Changes
```bash
# Commit and push the backend changes
git add Tback/payments/views.py
git commit -m "Add detailed logging for booking details"
git push origin main

# Wait for Railway to deploy
```

### Step 2: Make a Test Payment
1. Go to https://www.talesandtrailsghana.com
2. Select "Tent Xcape"
3. Set travelers: 1 adult, 0 children
4. Select a date
5. Proceed to payment
6. Complete payment

### Step 3: Check Railway Logs
```bash
# View Railway logs
railway logs

# Look for these log messages:
# - "Received booking_details from frontend: {...}"
# - "Converting frontend booking data for payment..."
# - "Converted data: {...}"
# - "Stored real-time booking details for payment..."
# - "Final metadata: {...}"
```

### Step 4: Inspect the Payment
```bash
# SSH into Railway and run the check script
railway run python check_latest_payment.py
```

This will show:
- The full payment metadata
- What booking_details are stored
- Which fields are missing

## Expected Data Structure

### What Frontend Sends:
```json
{
  "type": "destination",
  "destination": {
    "name": "Tent Xcape",
    "location": "Ghana",
    "duration": "3 Days / 2 Nights",
    "image_url": "..."
  },
  "travelers": {
    "adults": 1,
    "children": 0
  },
  "selected_date": "2025-12-15",
  "selected_options": {
    "accommodation": {
      "id": "standard",
      "name": "Standard Hotel (included)",
      "price": 0
    },
    "transport": {...},
    "meals": {...}
  },
  "pricing": {
    "base_total": 1500.00,
    "options_total": 0.00,
    "final_total": 1500.00
  },
  "user_info": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+233240381084"
  }
}
```

### What Should Be Stored in Database:
```json
{
  "booking_details": {
    "user_info": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+233240381084"
    },
    "destination": {
      "name": "Tent Xcape",
      "location": "Ghana",
      "duration": "3 Days / 2 Nights",
      "base_price": 0
    },
    "travelers": {
      "adults": 1,
      "children": 0
    },
    "selected_date": "2025-12-15",
    "selected_options": {
      "accommodation": {
        "name": "Standard Hotel (included)",
        "price": 0,
        "is_default": true
      },
      ...
    },
    "pricing": {
      "base_total": 1500.00,
      "options_total": 0.00,
      "final_total": 1500.00
    }
  }
}
```

## Possible Issues

### Issue 1: Frontend Not Sending Data
**Check**: Look at browser console when making payment
**Fix**: Verify `bookingDetails` object in `Booking.tsx`

### Issue 2: Backend Not Receiving Data
**Check**: Railway logs should show "Received booking_details from frontend"
**Fix**: Check API serializer accepts `booking_details` field

### Issue 3: Conversion Error
**Check**: Railway logs should show "Converted data"
**Fix**: Update `convert_frontend_booking_data()` function

### Issue 4: Storage Error
**Check**: Railway logs should show "Stored real-time booking details"
**Fix**: Update `store_booking_details_in_payment()` function

## Quick Fix Commands

### Check Latest Payment Locally
```bash
cd Tback
python check_latest_payment.py
```

### Check on Railway
```bash
railway run python check_latest_payment.py
```

### View Railway Logs
```bash
railway logs --tail
```

### Force Refresh Payment Data
```bash
# If you know the payment reference
railway run python manage.py shell
>>> from payments.models import Payment
>>> p = Payment.objects.get(reference='PAY12345')
>>> print(p.metadata)
```

## Next Steps

1. ✅ Deploy backend changes with logging
2. ⏳ Make a test payment
3. ⏳ Check Railway logs
4. ⏳ Run check_latest_payment.py
5. ⏳ Identify where the data is lost
6. ⏳ Fix the issue
7. ⏳ Test again

## Contact for Help

If you're stuck, share:
1. Railway logs (the booking_details lines)
2. Output from `check_latest_payment.py`
3. Browser console logs during payment
4. The payment reference number

This will help identify exactly where the data is being lost.
