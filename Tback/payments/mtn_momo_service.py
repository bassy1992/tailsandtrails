import requests
import uuid
import base64
import logging
from typing import Dict, Any, Optional
from django.conf import settings
from django.utils import timezone
from .models import Payment

logger = logging.getLogger(__name__)

class MTNMoMoService:
    """Service class for MTN Mobile Money API integration"""
    
    def __init__(self):
        self.environment = settings.MTN_MOMO_ENVIRONMENT
        self.base_url = settings.MTN_MOMO_BASE_URL
        self.collection_user_id = settings.MTN_MOMO_COLLECTION_USER_ID
        self.collection_api_key = settings.MTN_MOMO_COLLECTION_API_KEY
        self.subscription_key = settings.MTN_MOMO_COLLECTION_SUBSCRIPTION_KEY
        self.callback_url = settings.MTN_MOMO_CALLBACK_URL
        self.timeout = 30
        
    def _get_access_token(self) -> Dict[str, Any]:
        """Get access token for MTN MoMo API"""
        try:
            # Encode credentials
            credentials = base64.b64encode(
                f"{self.collection_user_id}:{self.collection_api_key}".encode()
            ).decode('utf-8')
            
            headers = {
                'Authorization': f'Basic {credentials}',
                'Ocp-Apim-Subscription-Key': self.subscription_key,
                'Content-Type': 'application/json'
            }
            
            response = requests.post(
                f"{self.base_url}/collection/token/",
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'access_token': result.get('access_token'),
                    'expires_in': result.get('expires_in')
                }
            else:
                logger.error(f"MTN MoMo token request failed: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f'Token request failed: {response.status_code}'
                }
                
        except requests.RequestException as e:
            logger.error(f"MTN MoMo token request error: {str(e)}")
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
    
    def initiate_payment(self, payment: Payment) -> Dict[str, Any]:
        """Initiate payment with MTN Mobile Money"""
        try:
            # Get access token
            token_result = self._get_access_token()
            if not token_result['success']:
                return token_result
            
            access_token = token_result['access_token']
            
            # Generate unique transaction reference
            transaction_ref = str(uuid.uuid4())
            
            # Format phone number (remove + and spaces)
            phone_number = payment.phone_number.replace('+', '').replace(' ', '')
            
            # Prepare payment request
            payload = {
                'amount': str(int(float(payment.amount))),  # MTN expects string amount without decimals
                'currency': payment.currency,
                'externalId': payment.reference,
                'payer': {
                    'partyIdType': 'MSISDN',
                    'partyId': phone_number
                },
                'payerMessage': payment.description or f'Payment for {settings.SITE_NAME}',
                'payeeNote': f'Payment from {payment.user.email if payment.user else "customer"}'
            }
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'X-Reference-Id': transaction_ref,
                'X-Target-Environment': self.environment,
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': self.subscription_key
            }
            
            response = requests.post(
                f"{self.base_url}/collection/v1_0/requesttopay",
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 202:  # MTN returns 202 for accepted requests
                logger.info(f"MTN MoMo payment initiated: {transaction_ref}")
                return {
                    'success': True,
                    'external_reference': transaction_ref,
                    'message': 'Payment request sent to customer phone',
                    'transaction_id': transaction_ref
                }
            else:
                logger.error(f"MTN MoMo payment failed: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f'MTN MoMo API error: {response.status_code}',
                    'message': 'Failed to initiate payment'
                }
                
        except requests.RequestException as e:
            logger.error(f"MTN MoMo payment error: {str(e)}")
            return {
                'success': False,
                'error': f'Network error: {str(e)}',
                'message': 'Network error during payment initiation'
            }
        except Exception as e:
            logger.error(f"MTN MoMo payment exception: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error during payment initiation'
            }
    
    def check_payment_status(self, external_reference: str) -> Dict[str, Any]:
        """Check payment status with MTN MoMo"""
        try:
            # Get access token
            token_result = self._get_access_token()
            if not token_result['success']:
                return token_result
            
            access_token = token_result['access_token']
            
            headers = {
                'Authorization': f'Bearer {access_token}',
                'X-Target-Environment': self.environment,
                'Ocp-Apim-Subscription-Key': self.subscription_key
            }
            
            response = requests.get(
                f"{self.base_url}/collection/v1_0/requesttopay/{external_reference}",
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                status = result.get('status', '').upper()
                
                # Map MTN status to our status
                status_mapping = {
                    'PENDING': 'processing',
                    'SUCCESSFUL': 'successful',
                    'FAILED': 'failed',
                    'TIMEOUT': 'failed',
                    'CANCELLED': 'cancelled'
                }
                
                mapped_status = status_mapping.get(status, 'processing')
                
                return {
                    'success': True,
                    'status': mapped_status,
                    'mtn_status': status,
                    'transaction_id': result.get('financialTransactionId'),
                    'reason': result.get('reason', ''),
                    'message': f'Payment status: {status}'
                }
            else:
                logger.error(f"MTN MoMo status check failed: {response.status_code} - {response.text}")
                return {
                    'success': False,
                    'error': f'Status check failed: {response.status_code}',
                    'message': 'Failed to check payment status'
                }
                
        except requests.RequestException as e:
            logger.error(f"MTN MoMo status check error: {str(e)}")
            return {
                'success': False,
                'error': f'Network error: {str(e)}',
                'message': 'Network error during status check'
            }
        except Exception as e:
            logger.error(f"MTN MoMo status check exception: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Unexpected error during status check'
            }
    
    def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process MTN MoMo webhook notification"""
        try:
            # Extract relevant data from webhook
            external_id = webhook_data.get('externalId')
            status = webhook_data.get('status', '').upper()
            transaction_id = webhook_data.get('financialTransactionId')
            reason = webhook_data.get('reason', '')
            
            if not external_id:
                return {
                    'success': False,
                    'error': 'Missing external ID in webhook data'
                }
            
            # Map MTN status to our status
            status_mapping = {
                'PENDING': 'processing',
                'SUCCESSFUL': 'successful',
                'FAILED': 'failed',
                'TIMEOUT': 'failed',
                'CANCELLED': 'cancelled'
            }
            
            mapped_status = status_mapping.get(status, 'processing')
            
            logger.info(f"MTN MoMo webhook processed: {external_id} -> {mapped_status}")
            
            return {
                'success': True,
                'external_id': external_id,
                'status': mapped_status,
                'mtn_status': status,
                'transaction_id': transaction_id,
                'reason': reason,
                'message': f'Webhook processed: {status}'
            }
            
        except Exception as e:
            logger.error(f"MTN MoMo webhook processing error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Error processing webhook'
            }
    
    def validate_phone_number(self, phone_number: str) -> Dict[str, Any]:
        """Validate Ghana phone number format for MTN MoMo"""
        try:
            # Remove spaces and special characters
            clean_number = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            
            # Handle different formats
            if clean_number.startswith('+233'):
                clean_number = clean_number[4:]
            elif clean_number.startswith('233'):
                clean_number = clean_number[3:]
            elif clean_number.startswith('0'):
                clean_number = clean_number[1:]
            
            # Check if it's a valid Ghana mobile number (9 digits)
            if len(clean_number) != 9:
                return {
                    'valid': False,
                    'error': 'Phone number must be 9 digits after country code'
                }
            
            # Check if it starts with valid Ghana mobile prefixes
            valid_prefixes = ['20', '23', '24', '25', '26', '27', '28', '29', '50', '54', '55', '59']
            if not any(clean_number.startswith(prefix) for prefix in valid_prefixes):
                return {
                    'valid': False,
                    'error': 'Invalid Ghana mobile number prefix'
                }
            
            # Format for MTN API (233XXXXXXXXX)
            formatted_number = f"233{clean_number}"
            
            return {
                'valid': True,
                'formatted_number': formatted_number,
                'display_number': f"+233 {clean_number[:2]} {clean_number[2:5]} {clean_number[5:]}"
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Phone number validation error: {str(e)}'
            }
    
    def is_configured(self) -> bool:
        """Check if MTN MoMo is properly configured"""
        required_settings = [
            self.collection_user_id,
            self.collection_api_key,
            self.subscription_key
        ]
        # Check that all settings exist and are not placeholder values
        return all(
            setting and 
            setting not in ['your-collection-user-id', 'your-collection-api-key', 'your-subscription-key', '']
            for setting in required_settings
        )