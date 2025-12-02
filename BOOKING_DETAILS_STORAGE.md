# Booking Details Storage in Payment Metadata

## Overview
When a user makes a payment for a tour booking, all the booking details (customer info, destination, travelers, selected options, pricing) are now stored in the payment's `metadata` field under `booking_details`.

## What Gets Stored

The payment metadata contains a `booking_details` object with the following structure:

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
      "base_price": 1500.00
    },
    "travelers": {
      "adults": 2,
      "children": 1
    },
    "selected_date": "2025-09-20",
    "selected_options": {
      "accommodation": {
        "name": "Premium Hotel",
        "price": 500.00,
        "is_default": false
      },
      "transport": {
        "name": "Private Van",
        "price": 800.00,
        "is_default": false
      },
      "meals": {
        "name": "Standard Meals",
        "price": 0.00,
        "is_default": true
      },
      "medical": {
        "name": "Travel Insurance",
        "price": 200.00,
        "is_default": false
      },
      "experiences": [
        {
          "name": "Cultural Experience",
          "price": 250.00
        }
      ]
    },
    "pricing": {
      "base_total": 4500.00,
      "options_total": 2150.00,
      "final_total": 6650.00
    }
  }
}
```

## How It Works

### Frontend (Booking.tsx)
When the user clicks "Proceed to Payment", the booking page sends:

```typescript
const bookingDetails = {
  type: 'destination',
  destination: {
    name: bookingData.tourName,
    location: tourData?.location || 'Ghana',
    duration: bookingData.duration,
    image_url: tourData?.image || ''
  },
  travelers: {
    adults: bookingData.travelers.adults,
    children: bookingData.travelers.children
  },
  selected_date: bookingData.selectedDate,
  selected_options: {
    accommodation: {...},
    transport: {...},
    meals: {...}
  },
  pricing: {
    base_total: totals.baseTotal,
    options_total: totals.addOnTotal,
    final_total: totals.total
  },
  user_info: {
    name: `${user?.first_name} ${user?.last_name}`,
    email: user?.email,
    phone: user?.phone || ''
  }
};
```

### Backend (payments/views.py)
The `checkout_payment` endpoint:

1. Receives the `booking_details` from the request
2. Calls `convert_frontend_booking_data()` to convert the frontend structure to backend format
3. Calls `store_booking_details_in_payment()` to save it in the payment's metadata
4. The data is now accessible in the Django admin and via API

## Files Modified

1. **Tback/payments/views.py**
   - Updated `convert_frontend_booking_data()` to handle the actual structure sent from frontend
   - Added better logging for debugging
   - Properly extracts all booking information

2. **Tback/payments/booking_utils.py**
   - Contains `store_booking_details_in_payment()` function
   - Structures the data for easy display in admin

## Testing

### Local Testing
Run the test script to verify booking details are being stored:

```bash
cd Tback
python test_booking_details_storage.py
```

### Railway Production Testing
To inspect payments in the Railway database:

```bash
# SSH into Railway
railway run python inspect_railway_payments.py
```

This will show:
- All recent payments
- Their booking details (if stored)
- Customer information
- Destination details
- Selected options
- Pricing breakdown

### Backfilling Existing Payments
If you want to add booking details to existing payments that don't have them:

```bash
# Dry run (see what would be updated)
railway run python backfill_booking_details.py

# Actually update the payments
railway run python backfill_booking_details.py --live
```

**Note**: New payments created after deploying these changes will automatically have booking details stored.

## Viewing in Django Admin

In the Django admin panel:
1. Go to Payments
2. Click on any payment
3. Scroll to the "Metadata" field
4. You'll see the full `booking_details` object with all customer and booking information

## Benefits

1. **Complete Audit Trail**: Every payment has full booking context
2. **Customer Support**: Easy to see what the customer booked
3. **Reporting**: Can analyze popular destinations, options, etc.
4. **Recovery**: If booking record is lost, payment metadata has all details
5. **Admin Display**: Django admin can show formatted booking details

## Next Steps

If you want to enhance this further:
1. Add a custom admin display for booking_details
2. Create reports based on booking metadata
3. Add email templates that use booking_details
4. Create booking confirmation PDFs from payment metadata
