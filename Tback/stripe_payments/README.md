# Stripe Payments App

A comprehensive Django app for handling Stripe payments with Payment Intents, webhooks, refunds, and payment method management.

## Features

- **Payment Intents**: Create, confirm, and cancel Stripe Payment Intents
- **Payment Methods**: Save and manage customer payment methods
- **Webhooks**: Secure webhook handling for real-time payment updates
- **Refunds**: Create and manage refunds for successful payments
- **Customer Management**: Automatic Stripe customer creation and management
- **Admin Interface**: Full Django admin integration
- **API Endpoints**: Complete RESTful API for frontend integration

## Models

### StripeCustomer
- Links Django users to Stripe customers
- Automatic customer creation on first payment

### StripePaymentIntent
- Stores Payment Intent information
- Tracks payment status and metadata
- Links to bookings for travel payments

### StripePaymentMethod
- Stores saved payment methods
- Card details and expiration information
- Default payment method management

### StripeWebhookEvent
- Stores and processes Stripe webhooks
- Prevents duplicate processing
- Error tracking and retry logic

### StripeRefund
- Manages refund requests and status
- Links to original Payment Intent
- Reason and description tracking

## API Endpoints

### Payment Intents
- `POST /api/stripe/payment-intents/create/` - Create Payment Intent
- `GET /api/stripe/payment-intents/` - List user's Payment Intents
- `GET /api/stripe/payment-intents/<id>/` - Get Payment Intent details
- `POST /api/stripe/payment-intents/<id>/confirm/` - Confirm Payment Intent
- `POST /api/stripe/payment-intents/<id>/cancel/` - Cancel Payment Intent
- `GET /api/stripe/payment-intents/<id>/client-secret/` - Get client secret

### Payment Methods
- `GET /api/stripe/payment-methods/` - List saved payment methods

### Refunds
- `POST /api/stripe/payment-intents/<id>/refunds/` - Create refund

### Webhooks
- `POST /api/stripe/webhooks/stripe/` - Stripe webhook endpoint

## Setup

1. **Install Stripe library**:
```bash
pip install stripe
```

2. **Add to INSTALLED_APPS**:
```python
INSTALLED_APPS = [
    # ... other apps
    'stripe_payments',
]
```

3. **Configure Stripe settings**:
```python
# Stripe settings
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'  # Your publishable key
STRIPE_SECRET_KEY = 'sk_test_...'       # Your secret key
STRIPE_WEBHOOK_SECRET = 'whsec_...'     # Your webhook secret
```

4. **Run migrations**:
```bash
python manage.py makemigrations stripe_payments
python manage.py migrate
```

5. **Add URLs**:
```python
# urls.py
urlpatterns = [
    # ... other patterns
    path('api/stripe/', include('stripe_payments.urls')),
]
```

## Usage Examples

### Creating a Payment Intent

**API Request:**
```json
POST /api/stripe/payment-intents/create/
{
    "amount": 99.99,
    "currency": "USD",
    "description": "Travel booking payment",
    "booking_id": 123,
    "save_payment_method": true
}
```

**Response:**
```json
{
    "id": 1,
    "stripe_payment_intent_id": "pi_1234567890",
    "amount": "99.99",
    "currency": "USD",
    "status": "requires_payment_method",
    "client_secret": "pi_1234567890_secret_...",
    "created_at": "2024-01-01T12:00:00Z"
}
```

### Frontend Integration

```javascript
// Initialize Stripe
const stripe = Stripe('pk_test_...');

// Create Payment Intent
const response = await fetch('/api/stripe/payment-intents/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token your-auth-token'
    },
    body: JSON.stringify({
        amount: 99.99,
        currency: 'USD',
        description: 'Travel booking payment'
    })
});

const paymentIntent = await response.json();

// Confirm payment with Stripe Elements
const {error} = await stripe.confirmPayment({
    elements,
    clientSecret: paymentIntent.client_secret,
    confirmParams: {
        return_url: 'https://yoursite.com/payment-success'
    }
});
```

### Programmatic Usage

```python
from stripe_payments.services import StripeService

# Create Payment Intent
stripe_service = StripeService()
result = stripe_service.create_payment_intent(
    user=user,
    amount=99.99,
    currency='USD',
    description='Travel booking payment',
    booking=booking
)

if result['success']:
    payment_intent = result['payment_intent']
    client_secret = result['client_secret']
    print(f"Payment Intent created: {payment_intent.stripe_payment_intent_id}")
else:
    print(f"Error: {result['error']}")
```

## Webhook Configuration

1. **Set up webhook endpoint in Stripe Dashboard**:
   - URL: `https://yourdomain.com/api/stripe/webhooks/stripe/`
   - Events: `payment_intent.succeeded`, `payment_intent.payment_failed`, `payment_intent.canceled`

2. **Configure webhook secret** in settings:
```python
STRIPE_WEBHOOK_SECRET = 'whsec_your_webhook_secret'
```

## Supported Webhook Events

- `payment_intent.succeeded` - Payment completed successfully
- `payment_intent.payment_failed` - Payment failed
- `payment_intent.canceled` - Payment was canceled
- `charge.dispute.created` - Chargeback/dispute created

## Error Handling

The app includes comprehensive error handling:

- **Stripe API errors** are caught and returned as user-friendly messages
- **Database errors** are logged and handled gracefully
- **Webhook processing errors** are stored for debugging
- **Duplicate webhook events** are automatically detected and ignored

## Security Features

- **Webhook signature verification** prevents unauthorized requests
- **User authentication** required for all payment operations
- **Payment Intent ownership** verification prevents unauthorized access
- **Sensitive data masking** in logs and admin interface

## Testing

```python
# Test Payment Intent creation
from django.test import TestCase
from django.contrib.auth import get_user_model
from stripe_payments.services import StripeService

User = get_user_model()

class StripePaymentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.stripe_service = StripeService()
    
    def test_create_payment_intent(self):
        result = self.stripe_service.create_payment_intent(
            user=self.user,
            amount=10.00,
            currency='USD',
            description='Test payment'
        )
        
        self.assertTrue(result['success'])
        self.assertIn('payment_intent', result)
        self.assertIn('client_secret', result)
```

## Admin Interface

The app provides a comprehensive Django admin interface:

- **Payment Intent management** with status filtering and search
- **Customer management** with payment history
- **Webhook event monitoring** with processing status
- **Refund management** with status tracking
- **Payment method overview** with card details

## Monitoring and Logging

- All Stripe API calls are logged with request/response details
- Webhook processing is logged with success/failure status
- Payment status changes are tracked with timestamps
- Error conditions are logged with full context

## Production Considerations

1. **Use production Stripe keys** in production environment
2. **Configure proper webhook endpoints** with HTTPS
3. **Set up monitoring** for failed webhook processing
4. **Implement proper error handling** in frontend
5. **Test webhook endpoints** thoroughly before going live
6. **Monitor payment failures** and implement retry logic
7. **Set up alerts** for unusual payment patterns

## Troubleshooting

### Common Issues

1. **Webhook not receiving events**:
   - Check webhook URL is publicly accessible
   - Verify webhook secret is correct
   - Check Stripe Dashboard for webhook delivery attempts

2. **Payment Intent creation fails**:
   - Verify Stripe API keys are correct
   - Check amount is above minimum (usually $0.50)
   - Ensure currency is supported

3. **Frontend integration issues**:
   - Verify publishable key matches secret key environment
   - Check CORS settings for API endpoints
   - Ensure proper authentication headers

### Debug Mode

Enable debug logging for detailed information:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'stripe_payments.log',
        },
    },
    'loggers': {
        'stripe_payments': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```