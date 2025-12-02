# Paystack Payment Integration

## Overview
The booking system now uses Paystack as the exclusive payment gateway. Users are redirected to Paystack's secure hosted payment page where they can pay using:
- Credit/Debit Cards (Visa, Mastercard, Verve)
- Mobile Money (MTN, Vodafone, AirtelTigo)
- Bank Transfer
- USSD

## Payment Flow

### 1. User Journey
1. User selects tour and customizes booking options
2. Clicks "Proceed to Payment"
3. Backend creates a payment record
4. Backend initializes Paystack payment
5. User is redirected to Paystack's hosted payment page
6. User completes payment on Paystack's website
7. Paystack redirects back to our callback URL
8. We verify the payment with Paystack
9. User sees success confirmation

### 2. Technical Implementation

#### Frontend Components

**Booking Page** (`Tfront/client/pages/Booking.tsx`)
- Removed payment method selection (Paystack handles all methods)
- Shows single "Secure Payment" section with Paystack branding
- `handleProceedToPayment()` function:
  1. Creates payment via `/api/payments/checkout/create/`
  2. Initializes Paystack via `/api/payments/paystack/initialize/`
  3. Redirects to Paystack's `authorization_url`

**Payment Callback Page** (`Tfront/client/pages/PaymentCallback.tsx`)
- Handles redirect from Paystack after payment
- Verifies payment status with backend
- Shows loading state while verifying
- Redirects to success page on confirmation

**API Client** (`Tfront/client/lib/api.ts`)
- `createCheckoutPayment()` - Creates payment record
- `initializePaystack()` - Gets Paystack authorization URL
- `verifyPaystack()` - Verifies payment after redirect

#### Backend Endpoints

**Payment Creation**
- `POST /api/payments/checkout/create/`
- Creates Payment record with booking details
- Returns payment reference

**Paystack Initialization**
- `POST /api/payments/paystack/initialize/`
- Calls Paystack API to initialize transaction
- Returns authorization URL for redirect

**Paystack Verification**
- `GET /api/payments/paystack/verify/{reference}/`
- Verifies payment status with Paystack
- Updates local payment record

**Paystack Webhook**
- `POST /api/payments/paystack/webhook/`
- Receives real-time payment updates from Paystack
- Updates payment status automatically

### 3. Configuration Required

#### Environment Variables
```bash
# Backend (.env)
PAYSTACK_SECRET_KEY=sk_test_xxxxxxxxxxxxx
PAYSTACK_PUBLIC_KEY=pk_test_xxxxxxxxxxxxx
PAYSTACK_WEBHOOK_SECRET=xxxxxxxxxxxxx
```

#### Paystack Dashboard Setup
1. Go to Settings > API Keys & Webhooks
2. Copy your test/live keys
3. Set webhook URL: `https://yourdomain.com/api/payments/paystack/webhook/`
4. Enable these events:
   - charge.success
   - charge.failed

### 4. Payment Methods Supported

Paystack automatically handles:
- **Cards**: Visa, Mastercard, Verve
- **Mobile Money**: MTN Mobile Money, Vodafone Cash, AirtelTigo Money
- **Bank Transfer**: Direct bank transfers
- **USSD**: USSD codes for bank payments
- **QR Code**: Scan to pay

Users select their preferred method on Paystack's page.

### 5. Security Features

- SSL/TLS encryption for all transactions
- PCI DSS compliant payment processing
- 3D Secure authentication for cards
- Webhook signature verification
- No card details stored on our servers

### 6. Testing

#### Test Cards (Paystack Test Mode)
```
Success: 4084 0840 8408 4081
Insufficient Funds: 4084 0840 8408 4082
Declined: 5060 6666 6666 6666 6666
```

#### Test Flow
1. Navigate to any tour booking page
2. Select travelers and add-ons
3. Click "Proceed to Payment"
4. You'll be redirected to Paystack's test page
5. Use test card details above
6. Complete payment
7. You'll be redirected back with confirmation

### 7. Error Handling

- **Payment Creation Fails**: User sees error, can retry
- **Paystack Initialization Fails**: User sees error, can retry
- **Payment Declined**: Paystack shows error, user can try different method
- **Verification Fails**: Callback page shows error, user can contact support
- **Network Issues**: Webhook ensures payment status is eventually updated

### 8. Routes

- `/booking/:id` - Booking page
- `/payment-callback` - Handles Paystack redirect
- `/payment-success` - Success confirmation page

### 9. Advantages of Paystack

✅ Handles multiple payment methods in one integration
✅ Hosted payment page (PCI compliance handled by Paystack)
✅ Mobile-optimized payment experience
✅ Automatic retry for failed payments
✅ Real-time payment notifications via webhooks
✅ Detailed transaction analytics
✅ Automatic currency conversion
✅ Fraud detection and prevention
