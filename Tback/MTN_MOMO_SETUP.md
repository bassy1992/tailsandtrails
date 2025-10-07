# MTN Mobile Money Integration Setup for Trails & Trails

This document explains how to set up and use the MTN Mobile Money API integration for Trails & Trails payments.

## Prerequisites

1. **MTN MOMO Developer Account**: Sign up at [MTN MOMO Developer Portal](https://momodeveloper.mtn.com/)
2. **API Credentials**: Obtain your Collection API credentials
3. **Webhook URL**: Set up a publicly accessible webhook URL for production

## Configuration

### 1. Environment Variables

The system uses environment variables from the `.env` file. Update these values:

```env
# MTN Mobile Money Configuration
MTN_MOMO_ENVIRONMENT=sandbox  # or 'production'
MTN_MOMO_BASE_URL=https://sandbox.momodeveloper.mtn.com
MTN_MOMO_COLLECTION_USER_ID=your-actual-collection-user-id
MTN_MOMO_COLLECTION_API_KEY=your-actual-collection-api-key
MTN_MOMO_COLLECTION_SUBSCRIPTION_KEY=your-actual-subscription-key
MTN_MOMO_CALLBACK_URL=http://localhost:8000/api/payments/mtn-momo/webhook/
```

### 2. Production Configuration

For production, update:
- `MTN_MOMO_ENVIRONMENT=production`
- `MTN_MOMO_BASE_URL=https://momodeveloper.mtn.com`
- `MTN_MOMO_CALLBACK_URL=https://yourdomain.com/api/payments/mtn-momo/webhook/`

## API Endpoints

### Payment Flow

1. **Get Payment Methods**
   ```
   GET /api/payments/checkout/methods/
   ```

2. **Create Payment**
   ```
   POST /api/payments/checkout/create/
   ```

3. **Check Payment Status**
   ```
   GET /api/payments/{reference}/status/
   ```

4. **Complete Payment (Demo)**
   ```
   POST /api/payments/{reference}/complete/
   ```

5. **MTN MoMo Webhook**
   ```
   POST /api/payments/mtn-momo/webhook/
   ```

## Testing

### 1. Check Configuration
```bash
python manage.py test_mtn_momo --check-config
```

### 2. Test API Connection (requires real credentials)
```bash
python manage.py test_mtn_momo
```

### 3. Test Payment Flow
```bash
python manage.py test_mtn_momo --phone 233244123456 --amount 1.0
```

### 4. Test Complete Flow
```bash
python test_momo_flow.py
```

### 5. Frontend Testing
1. Start the backend: `python manage.py runserver 8000`
2. Start the frontend: `npm run dev` (or your frontend server)
3. Navigate to a booking page
4. Select "Mobile Money" as payment method
5. Complete the payment flow

## Payment Statuses

- **pending**: Payment created but not yet initiated
- **processing**: Payment request sent to MTN MOMO
- **successful**: Payment completed successfully
- **failed**: Payment failed
- **cancelled**: Payment cancelled by user

## Demo Mode vs Production Mode

### Demo Mode (Default)
- Used when MTN MoMo credentials are not configured
- Simulates successful payment initiation
- Allows manual payment completion via API
- Perfect for development and testing

### Production Mode
- Used when real MTN MoMo credentials are configured
- Makes actual API calls to MTN MoMo
- Handles real payment processing
- Requires valid MTN MoMo developer account

## Error Handling

The system handles various error scenarios:

1. **Network Errors**: Retry mechanism and graceful fallbacks
2. **API Errors**: Detailed error messages from MTN MOMO
3. **Invalid Phone Numbers**: Validation for Ghana mobile numbers
4. **Missing Credentials**: Automatic fallback to demo mode

## Security Features

1. **Transaction References**: Unique identifiers for each payment
2. **Webhook Verification**: Secure webhook processing
3. **Data Encryption**: Sensitive data is encrypted in transit
4. **No PIN Storage**: MTN MOMO PINs are never stored
5. **Environment Variables**: Credentials stored securely

## Phone Number Validation

The system validates Ghana phone numbers and supports these formats:
- `+233244123456`
- `233244123456`
- `0244123456`
- `244123456`

Valid prefixes: 20, 23, 24, 25, 26, 27, 28, 29, 50, 54, 55, 59

## Monitoring

### Admin Interface
Access the Django admin to monitor payments:
- `/admin/payments/payment/` - View all payments
- `/admin/payments/paymentlog/` - View payment logs
- `/admin/payments/paymentcallback/` - View webhook logs

### Logging
Payment activities are logged for debugging:
```python
import logging
logger = logging.getLogger('payments')
```

## Troubleshooting

### Common Issues

1. **Configuration Errors**
   - Check your `.env` file has correct MTN MoMo credentials
   - Verify subscription key is correct
   - Ensure environment is set to 'sandbox' for testing

2. **Payment Failures**
   - Ensure phone number format is correct (233XXXXXXXXX)
   - Check account balance in sandbox
   - Verify API credentials are active

3. **Webhook Issues**
   - Verify webhook URL is publicly accessible
   - Check webhook logs in admin
   - Ensure HTTPS for production webhooks

4. **Demo Mode Issues**
   - Demo mode works without real credentials
   - Use manual completion endpoint for testing
   - Check payment logs for demo transactions

### Getting Real MTN MoMo Credentials

1. Visit [MTN MOMO Developer Portal](https://momodeveloper.mtn.com/)
2. Create an account and verify your identity
3. Create a new application
4. Subscribe to the Collections API
5. Generate API User and API Key
6. Get your Subscription Key from the portal
7. Update your `.env` file with real credentials

### Support

For technical issues:
1. Check the Django logs
2. Review MTN MOMO developer documentation
3. Contact MTN MOMO support for API-specific issues
4. Check the payment logs in Django admin

## Production Checklist

- [ ] Update environment variables for production
- [ ] Set up proper webhook URL with HTTPS
- [ ] Configure proper logging and monitoring
- [ ] Test with real MTN MOMO accounts
- [ ] Implement proper error handling
- [ ] Set up backup payment methods (Stripe)
- [ ] Configure email notifications
- [ ] Set up database backups
- [ ] Test webhook endpoint accessibility
- [ ] Verify SSL certificates

## Integration Status

✅ **Completed Features:**
- MTN MoMo service integration
- Payment creation and tracking
- Webhook handling
- Phone number validation
- Demo mode for development
- Admin interface
- Comprehensive logging
- Error handling
- Frontend integration
- Management commands for testing

🔄 **Demo Mode Active:**
- System works without real MTN MoMo credentials
- Perfect for development and testing
- Manual payment completion available
- All payment flows functional

🚀 **Ready for Production:**
- Add real MTN MoMo credentials to `.env`
- Update webhook URL for production
- System will automatically switch to production mode