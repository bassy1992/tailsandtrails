# Payments App

A comprehensive Django payment processing app that supports multiple payment providers including M-Pesa, Airtel Money, and Stripe.

## Features

- **Multiple Payment Providers**: Support for M-Pesa, Airtel Money, and Stripe
- **Payment Tracking**: Complete payment lifecycle tracking with status updates
- **Callback Handling**: Secure webhook/callback processing from payment providers
- **Logging**: Comprehensive logging of all payment activities
- **Admin Interface**: Full admin interface for payment management
- **API Endpoints**: RESTful API for payment operations
- **Email Notifications**: Automated email notifications for payment status changes

## Models

### PaymentProvider
- Stores payment provider configurations (M-Pesa, Airtel Money, Stripe)
- JSON configuration field for provider-specific settings
- Active/inactive status management

### Payment
- Main payment record with user, amount, currency, and status
- Supports multiple payment methods (mobile money, bank transfer, card)
- Automatic reference generation
- Booking association for travel bookings

### PaymentCallback
- Stores callbacks/webhooks from payment providers
- Full callback payload storage
- Processing status tracking

### PaymentLog
- Comprehensive logging of all payment activities
- Multiple log levels (info, warning, error, debug)
- JSON data storage for additional context

## API Endpoints

### Payment Operations
- `GET /api/payments/providers/` - List active payment providers
- `POST /api/payments/create/` - Create a new payment
- `GET /api/payments/list/` - List user's payments
- `GET /api/payments/<reference>/` - Get payment details
- `GET /api/payments/<reference>/status/` - Check payment status
- `POST /api/payments/<reference>/cancel/` - Cancel a payment

### Callbacks
- `POST /api/payments/callback/<provider_code>/` - Handle provider callbacks

## Setup

1. **Add to INSTALLED_APPS**:
```python
INSTALLED_APPS = [
    # ... other apps
    'payments',
]
```

2. **Run migrations**:
```bash
python manage.py makemigrations payments
python manage.py migrate
```

3. **Setup payment providers**:
```bash
python manage.py setup_payment_providers
```

4. **Configure payment providers** in Django admin or programmatically:
   - M-Pesa: Add consumer key, secret, business short code, and passkey
   - Airtel Money: Add client ID and secret
   - Stripe: Add publishable key, secret key, and webhook secret

## Configuration

Add these settings to your Django settings:

```python
# Payment settings
PAYMENT_TIMEOUT = 30  # seconds
BASE_URL = 'https://yourdomain.com'  # For callbacks
SITE_NAME = 'Your Site Name'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

## Usage Examples

### Creating a Payment
```python
from payments.models import Payment, PaymentProvider

provider = PaymentProvider.objects.get(code='mpesa')
payment = Payment.objects.create(
    user=user,
    amount=100.00,
    currency='KES',
    payment_method='mobile_money',
    provider=provider,
    phone_number='+254700000000',
    description='Travel booking payment'
)
```

### Processing Payments
```python
from payments.services import PaymentService

service = PaymentService()
result = service.initiate_payment(payment)

if result['success']:
    print(f"Payment initiated: {result['external_reference']}")
else:
    print(f"Payment failed: {result['message']}")
```

## Management Commands

### Setup Payment Providers
```bash
python manage.py setup_payment_providers
```

### Check Pending Payments
```bash
# Check payments pending for more than 24 hours
python manage.py check_pending_payments

# Check and update status from providers
python manage.py check_pending_payments --update

# Check payments pending for more than 6 hours
python manage.py check_pending_payments --hours 6
```

## Testing

Run the payment tests:
```bash
python manage.py test payments
```

## Security Considerations

1. **Callback Verification**: Always verify callbacks from payment providers
2. **HTTPS**: Use HTTPS for all payment-related endpoints
3. **API Keys**: Store API keys securely (environment variables)
4. **Logging**: Sensitive data is automatically masked in logs
5. **Permissions**: API endpoints require authentication

## Provider-Specific Notes

### M-Pesa
- Uses STK Push for payment initiation
- Requires sandbox/production configuration
- Callback URL must be publicly accessible

### Airtel Money
- Implementation placeholder - needs completion
- Requires client credentials

### Stripe
- Implementation placeholder - needs completion
- Requires webhook endpoint setup

## Troubleshooting

1. **Payment stuck in processing**: Use the `check_pending_payments` command
2. **Callback not received**: Check callback URL accessibility
3. **Provider configuration**: Verify API keys and endpoints in admin
4. **Email notifications**: Check email backend configuration

## Contributing

When adding new payment providers:
1. Add provider configuration to `setup_payment_providers` command
2. Implement provider-specific methods in `PaymentService`
3. Add callback processing logic
4. Update tests and documentation