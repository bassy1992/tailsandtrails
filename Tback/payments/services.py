import logging
import requests
from typing import Dict, Any, Optional
from django.conf import settings
from django.utils import timezone
from .models import Payment, PaymentProvider, PaymentCallback
from .mtn_momo_service import MTNMoMoService

logger = logging.getLogger(__name__)

class PaymentService:
    """Service class for handling payment operations"""
    
    def __init__(self):
        self.timeout = getattr(settings, 'PAYMENT_TIMEOUT', 30)
    
    def initiate_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate payment with the provider"""
        try:
            provider = payment.provider
            
            if provider.code == 'mtn_momo':
                return self._initiate_mtn_momo_payment(payment)
            elif provider.code == 'vodafone_cash':
                return self._initiate_vodafone_payment(payment)
            elif provider.code == 'airteltigo_money':
                return self._initiate_airteltigo_payment(payment)
            elif provider.code == 'mpesa_kenya':
                return self._initiate_mpesa_payment(payment)
            elif provider.code == 'stripe':
                return self._initiate_stripe_payment(payment)
            else:
                return {
                    'success': False,
                    'message': f'Unsupported payment provider: {provider.code}'
                }
                
        except Exception as e:
            logger.error(f"Payment initiation error: {str(e)}")
            return {
                'success': False,
                'message': 'Payment initiation failed',
                'error': str(e)
            }
    
    def _initiate_mtn_momo_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate MTN Mobile Money payment using the dedicated service"""
        mtn_service = MTNMoMoService()
        
        # Check if MTN MoMo is configured
        if not mtn_service.is_configured():
            logger.warning("MTN MoMo not configured, using demo mode")
            # Return demo success for development
            import uuid
            return {
                'success': True,
                'external_reference': f"DEMO_MTN_{str(uuid.uuid4())[:8]}",
                'message': 'Demo: Payment request sent to customer phone'
            }
        
        # Use the real MTN MoMo service
        return mtn_service.initiate_payment(payment)
    
    def _check_mtn_momo_status(self, payment: Payment) -> Dict[str, Any]:
        """Check MTN Mobile Money payment status"""
        mtn_service = MTNMoMoService()
        
        if not mtn_service.is_configured():
            # For demo mode, return current status
            return {
                'success': True,
                'status': payment.status,
                'message': 'Demo mode: Status check completed'
            }
        
        # Use the real MTN MoMo service
        return mtn_service.check_payment_status(payment.external_reference)

    def _initiate_vodafone_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate Vodafone Cash payment"""
        # Placeholder for Vodafone Cash integration
        return {
            'success': False,
            'message': 'Vodafone Cash integration not implemented yet'
        }
    
    def _initiate_airteltigo_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate AirtelTigo Money payment"""
        # Placeholder for AirtelTigo Money integration
        return {
            'success': False,
            'message': 'AirtelTigo Money integration not implemented yet'
        }

    def _initiate_mpesa_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate M-Pesa STK Push payment"""
        config = payment.provider.configuration
        
        # Get access token
        token_result = self._get_mpesa_token(config)
        if not token_result.get('success'):
            return token_result
        
        access_token = token_result['access_token']
        
        # Prepare STK Push request
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        business_short_code = config.get('business_short_code')
        passkey = config.get('passkey')
        
        # Generate password
        import base64
        password_string = f"{business_short_code}{passkey}{timestamp}"
        password = base64.b64encode(password_string.encode()).decode('utf-8')
        
        payload = {
            'BusinessShortCode': business_short_code,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(payment.amount),
            'PartyA': payment.phone_number.replace('+', ''),
            'PartyB': business_short_code,
            'PhoneNumber': payment.phone_number.replace('+', ''),
            'CallBackURL': f"{settings.BASE_URL}/api/payments/callback/mpesa/",
            'AccountReference': payment.reference,
            'TransactionDesc': payment.description or f'Payment for booking {payment.booking_id}'
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                config.get('stk_push_url'),
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('ResponseCode') == '0':
                    return {
                        'success': True,
                        'external_reference': result.get('CheckoutRequestID'),
                        'message': 'STK Push sent successfully'
                    }
                else:
                    return {
                        'success': False,
                        'message': result.get('ResponseDescription', 'STK Push failed')
                    }
            else:
                return {
                    'success': False,
                    'message': f'HTTP {response.status_code}: {response.text}'
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': 'Network error during payment initiation',
                'error': str(e)
            }
    
    def _get_mpesa_token(self, config: Dict) -> Dict[str, Any]:
        """Get M-Pesa access token"""
        import base64
        
        consumer_key = config.get('consumer_key')
        consumer_secret = config.get('consumer_secret')
        
        if not consumer_key or not consumer_secret:
            return {
                'success': False,
                'message': 'M-Pesa credentials not configured'
            }
        
        # Encode credentials
        credentials = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode('utf-8')
        
        headers = {
            'Authorization': f'Basic {credentials}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                config.get('token_url'),
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'access_token': result.get('access_token')
                }
            else:
                return {
                    'success': False,
                    'message': f'Token request failed: {response.status_code}'
                }
                
        except requests.RequestException as e:
            return {
                'success': False,
                'message': 'Failed to get access token',
                'error': str(e)
            }
    
    def _initiate_airtel_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate Airtel Money payment"""
        # Placeholder for Airtel Money integration
        return {
            'success': False,
            'message': 'Airtel Money integration not implemented yet'
        }
    
    def _initiate_stripe_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate Stripe payment"""
        # Placeholder for Stripe integration
        return {
            'success': False,
            'message': 'Stripe integration not implemented yet'
        }
    
    def cancel_payment(self, payment: Payment) -> Dict[str, Any]:
        """Cancel a payment"""
        try:
            provider = payment.provider
            
            if provider.code == 'mpesa':
                # M-Pesa doesn't support cancellation after STK push
                return {
                    'success': True,
                    'message': 'Payment marked as cancelled'
                }
            else:
                return {
                    'success': True,
                    'message': 'Payment cancelled'
                }
                
        except Exception as e:
            logger.error(f"Payment cancellation error: {str(e)}")
            return {
                'success': False,
                'message': 'Cancellation failed',
                'error': str(e)
            }
    
    def process_callback(self, payment: Payment, callback: PaymentCallback) -> Dict[str, Any]:
        """Process payment callback"""
        try:
            provider = payment.provider
            
            if provider.code == 'mtn_momo':
                return self._process_mtn_momo_callback(payment, callback)
            elif provider.code == 'vodafone_cash':
                return self._process_vodafone_callback(payment, callback)
            elif provider.code == 'airteltigo_money':
                return self._process_airteltigo_callback(payment, callback)
            elif provider.code == 'mpesa_kenya':
                return self._process_mpesa_callback(payment, callback)
            elif provider.code == 'stripe':
                return self._process_stripe_callback(payment, callback)
            else:
                return {
                    'success': False,
                    'message': f'Unsupported provider for callback: {provider.code}'
                }
                
        except Exception as e:
            logger.error(f"Callback processing error: {str(e)}")
            return {
                'success': False,
                'message': 'Callback processing failed',
                'error': str(e)
            }
    
    def _process_mtn_momo_callback(self, payment: Payment, callback: PaymentCallback) -> Dict[str, Any]:
        """Process MTN Mobile Money callback"""
        callback_data = callback.callback_data
        
        # MTN MoMo callback structure
        status = callback_data.get('status')
        transaction_id = callback_data.get('financialTransactionId')
        external_id = callback_data.get('externalId')
        
        if status == 'SUCCESSFUL':
            return {
                'success': True,
                'status': 'successful',
                'transaction_id': transaction_id,
                'external_id': external_id,
                'message': 'Payment completed successfully'
            }
        elif status == 'FAILED':
            reason = callback_data.get('reason', 'Payment failed')
            return {
                'success': True,
                'status': 'failed',
                'message': reason
            }
        elif status == 'PENDING':
            return {
                'success': True,
                'status': 'processing',
                'message': 'Payment is being processed'
            }
        else:
            return {
                'success': True,
                'status': 'failed',
                'message': f'Unknown status: {status}'
            }
    
    def _process_vodafone_callback(self, payment: Payment, callback: PaymentCallback) -> Dict[str, Any]:
        """Process Vodafone Cash callback"""
        # Placeholder for Vodafone Cash callback processing
        return {
            'success': False,
            'message': 'Vodafone Cash callback processing not implemented'
        }
    
    def _process_airteltigo_callback(self, payment: Payment, callback: PaymentCallback) -> Dict[str, Any]:
        """Process AirtelTigo Money callback"""
        # Placeholder for AirtelTigo Money callback processing
        return {
            'success': False,
            'message': 'AirtelTigo Money callback processing not implemented'
        }

    def _process_mpesa_callback(self, payment: Payment, callback: PaymentCallback) -> Dict[str, Any]:
        """Process M-Pesa callback"""
        callback_data = callback.callback_data
        
        # Extract result from callback
        body = callback_data.get('Body', {})
        stk_callback = body.get('stkCallback', {})
        
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc', '')
        
        if result_code == 0:
            # Payment successful
            callback_metadata = stk_callback.get('CallbackMetadata', {})
            items = callback_metadata.get('Item', [])
            
            # Extract transaction details
            transaction_id = None
            phone_number = None
            amount = None
            
            for item in items:
                name = item.get('Name')
                value = item.get('Value')
                
                if name == 'MpesaReceiptNumber':
                    transaction_id = value
                elif name == 'PhoneNumber':
                    phone_number = value
                elif name == 'Amount':
                    amount = value
            
            return {
                'success': True,
                'status': 'successful',
                'transaction_id': transaction_id,
                'phone_number': phone_number,
                'amount': amount,
                'message': result_desc
            }
        else:
            # Payment failed
            return {
                'success': True,
                'status': 'failed',
                'message': result_desc
            }
    
    def _process_airtel_callback(self, payment: Payment, callback: PaymentCallback) -> Dict[str, Any]:
        """Process Airtel Money callback"""
        # Placeholder for Airtel Money callback processing
        return {
            'success': False,
            'message': 'Airtel Money callback processing not implemented'
        }
    
    def _process_stripe_callback(self, payment: Payment, callback: PaymentCallback) -> Dict[str, Any]:
        """Process Stripe webhook"""
        # Placeholder for Stripe webhook processing
        return {
            'success': False,
            'message': 'Stripe webhook processing not implemented'
        }
    
    def check_payment_status(self, payment: Payment) -> Dict[str, Any]:
        """Check payment status with provider"""
        try:
            provider = payment.provider
            
            if provider.code == 'mpesa':
                return self._check_mpesa_status(payment)
            else:
                return {
                    'success': False,
                    'message': f'Status check not supported for {provider.code}'
                }
                
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return {
                'success': False,
                'message': 'Status check failed',
                'error': str(e)
            }
    
    def _check_mpesa_status(self, payment: Payment) -> Dict[str, Any]:
        """Check M-Pesa payment status"""
        # This would typically involve querying M-Pesa's transaction status API
        # For now, return the current status
        return {
            'success': True,
            'status': payment.status,
            'message': 'Status check completed'
        }
    
    def check_payment_status(self, payment: Payment) -> Dict[str, Any]:
        """Check payment status with provider"""
        try:
            provider = payment.provider
            
            if provider.code == 'mtn_momo':
                return self._check_mtn_momo_status(payment)
            elif provider.code == 'mpesa_kenya':
                return self._check_mpesa_status(payment)
            else:
                return {
                    'success': False,
                    'message': f'Status check not supported for {provider.code}'
                }
                
        except Exception as e:
            logger.error(f"Status check error: {str(e)}")
            return {
                'success': False,
                'message': 'Status check failed',
                'error': str(e)
            }
    
    def extract_payment_reference(self, provider: PaymentProvider, callback_data: Dict) -> Optional[str]:
        """Extract payment reference from callback data"""
        if provider.code == 'mtn_momo':
            return callback_data.get('externalId')
        elif provider.code == 'vodafone_cash':
            return callback_data.get('reference') or callback_data.get('externalId')
        elif provider.code == 'airteltigo_money':
            return callback_data.get('reference') or callback_data.get('externalId')
        elif provider.code == 'mpesa_kenya':
            body = callback_data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            return stk_callback.get('CheckoutRequestID')
        
        # For other providers, look for common reference fields
        return callback_data.get('reference') or callback_data.get('transaction_id') or callback_data.get('externalId')