import os
import requests
import hashlib
import hmac
import json
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from .models import Payment, PaymentLog
import logging

logger = logging.getLogger(__name__)

class PaystackService:
    """Service for handling Paystack payments"""
    
    def __init__(self):
        self.secret_key = os.getenv('PAYSTACK_SECRET_KEY')
        self.public_key = os.getenv('PAYSTACK_PUBLIC_KEY')
        self.webhook_secret = os.getenv('PAYSTACK_WEBHOOK_SECRET')
        self.base_url = 'https://api.paystack.co'
        
        if not self.secret_key:
            raise ValueError("PAYSTACK_SECRET_KEY not found in environment variables")
    
    def _get_headers(self):
        """Get headers for Paystack API requests"""
        return {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json',
        }
    
    def initialize_payment(self, payment: Payment, callback_url: str = None):
        """Initialize a payment with Paystack"""
        try:
            # Convert amount to kobo (Paystack uses kobo for NGN)
            amount_in_kobo = int(payment.amount * 100)
            
            payload = {
                'email': payment.user.email if payment.user else 'guest@example.com',
                'amount': amount_in_kobo,
                'currency': payment.currency,
                'reference': payment.reference,
                'callback_url': callback_url or f"{settings.BASE_URL}/api/payments/paystack/callback/",
                'metadata': {
                    'payment_id': str(payment.payment_id),
                    'booking_id': payment.booking.id if payment.booking else None,
                    'user_id': payment.user.id if payment.user else None,
                    **payment.metadata
                }
            }
            
            # Add customer info if available
            if payment.user:
                payload['customer'] = {
                    'email': payment.user.email,
                    'first_name': payment.user.first_name,
                    'last_name': payment.user.last_name,
                    'phone': payment.phone_number or payment.user.phone_number
                }
            
            response = requests.post(
                f'{self.base_url}/transaction/initialize',
                headers=self._get_headers(),
                json=payload
            )
            
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get('status'):
                # Update payment with Paystack reference
                payment.external_reference = response_data['data']['reference']
                payment.status = 'processing'
                payment.metadata.update({
                    'paystack_access_code': response_data['data']['access_code'],
                    'paystack_authorization_url': response_data['data']['authorization_url']
                })
                payment.save()
                
                payment.log('info', 'Payment initialized with Paystack', response_data)
                
                return {
                    'success': True,
                    'data': response_data['data'],
                    'authorization_url': response_data['data']['authorization_url'],
                    'access_code': response_data['data']['access_code'],
                    'reference': response_data['data']['reference']
                }
            else:
                payment.log('error', 'Failed to initialize payment with Paystack', response_data)
                return {
                    'success': False,
                    'error': response_data.get('message', 'Unknown error occurred')
                }
                
        except Exception as e:
            logger.error(f"Error initializing Paystack payment: {str(e)}")
            payment.log('error', f'Exception during payment initialization: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }
    
    def verify_payment(self, reference: str):
        """Verify a payment with Paystack"""
        try:
            response = requests.get(
                f'{self.base_url}/transaction/verify/{reference}',
                headers=self._get_headers()
            )
            
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get('status'):
                return {
                    'success': True,
                    'data': response_data['data']
                }
            else:
                return {
                    'success': False,
                    'error': response_data.get('message', 'Verification failed')
                }
                
        except Exception as e:
            logger.error(f"Error verifying Paystack payment: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def handle_webhook(self, payload: dict, signature: str):
        """Handle Paystack webhook"""
        try:
            # Verify webhook signature
            if not self.verify_webhook_signature(payload, signature):
                logger.warning("Invalid webhook signature")
                return {'success': False, 'error': 'Invalid signature'}
            
            event = payload.get('event')
            data = payload.get('data', {})
            
            if event == 'charge.success':
                return self._handle_successful_payment(data)
            elif event == 'charge.failed':
                return self._handle_failed_payment(data)
            else:
                logger.info(f"Unhandled webhook event: {event}")
                return {'success': True, 'message': f'Event {event} received but not processed'}
                
        except Exception as e:
            logger.error(f"Error handling Paystack webhook: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def verify_webhook_signature(self, payload: dict, signature: str):
        """Verify Paystack webhook signature"""
        if not self.webhook_secret:
            logger.warning("Webhook secret not configured")
            return False
        
        # Convert payload to JSON string
        payload_str = json.dumps(payload, separators=(',', ':'))
        
        # Create expected signature
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload_str.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    
    def _handle_successful_payment(self, data: dict):
        """Handle successful payment webhook"""
        try:
            reference = data.get('reference')
            if not reference:
                return {'success': False, 'error': 'No reference in webhook data'}
            
            # Find payment by reference
            try:
                payment = Payment.objects.get(reference=reference)
            except Payment.DoesNotExist:
                logger.warning(f"Payment not found for reference: {reference}")
                return {'success': False, 'error': 'Payment not found'}
            
            # Update payment status
            payment.status = 'successful'
            payment.processed_at = timezone.now()
            payment.external_reference = data.get('id', payment.external_reference)
            payment.metadata.update({
                'paystack_transaction_id': data.get('id'),
                'paystack_gateway_response': data.get('gateway_response'),
                'paystack_channel': data.get('channel'),
                'paystack_fees': data.get('fees'),
                'paystack_authorization': data.get('authorization', {})
            })
            payment.save()
            
            payment.log('info', 'Payment completed successfully via webhook', data)
            
            # Update booking status if applicable
            if payment.booking:
                payment.booking.payment_status = 'paid'
                payment.booking.save()
            
            return {'success': True, 'message': 'Payment processed successfully'}
            
        except Exception as e:
            logger.error(f"Error handling successful payment: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _handle_failed_payment(self, data: dict):
        """Handle failed payment webhook"""
        try:
            reference = data.get('reference')
            if not reference:
                return {'success': False, 'error': 'No reference in webhook data'}
            
            # Find payment by reference
            try:
                payment = Payment.objects.get(reference=reference)
            except Payment.DoesNotExist:
                logger.warning(f"Payment not found for reference: {reference}")
                return {'success': False, 'error': 'Payment not found'}
            
            # Update payment status
            payment.status = 'failed'
            payment.processed_at = timezone.now()
            payment.metadata.update({
                'paystack_transaction_id': data.get('id'),
                'paystack_gateway_response': data.get('gateway_response'),
                'paystack_failure_reason': data.get('gateway_response')
            })
            payment.save()
            
            payment.log('error', 'Payment failed via webhook', data)
            
            return {'success': True, 'message': 'Failed payment processed'}
            
        except Exception as e:
            logger.error(f"Error handling failed payment: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def refund_payment(self, payment: Payment, amount: Decimal = None, reason: str = None):
        """Refund a payment"""
        try:
            refund_amount = amount or payment.amount
            amount_in_kobo = int(refund_amount * 100)
            
            payload = {
                'transaction': payment.external_reference,
                'amount': amount_in_kobo,
            }
            
            if reason:
                payload['customer_note'] = reason
                payload['merchant_note'] = reason
            
            response = requests.post(
                f'{self.base_url}/refund',
                headers=self._get_headers(),
                json=payload
            )
            
            response_data = response.json()
            
            if response.status_code == 200 and response_data.get('status'):
                payment.status = 'refunded'
                payment.metadata.update({
                    'refund_data': response_data['data'],
                    'refund_reason': reason
                })
                payment.save()
                
                payment.log('info', f'Payment refunded: {refund_amount}', response_data)
                
                return {
                    'success': True,
                    'data': response_data['data']
                }
            else:
                payment.log('error', 'Failed to refund payment', response_data)
                return {
                    'success': False,
                    'error': response_data.get('message', 'Refund failed')
                }
                
        except Exception as e:
            logger.error(f"Error refunding Paystack payment: {str(e)}")
            payment.log('error', f'Exception during refund: {str(e)}')
            return {
                'success': False,
                'error': str(e)
            }