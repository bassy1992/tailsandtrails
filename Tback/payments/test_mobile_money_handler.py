"""
Test mode handler for mobile money payments
This handles mobile money payments in test mode since Paystack doesn't support them
"""
import logging
from django.utils import timezone
from datetime import timedelta
from .models import Payment

logger = logging.getLogger(__name__)

class TestMobileMoneyHandler:
    """Handle mobile money payments in test mode"""
    
    @staticmethod
    def auto_approve_test_payments():
        """Auto-approve mobile money payments in test mode after 10 seconds"""
        try:
            # Find processing mobile money payments older than 10 seconds
            cutoff_time = timezone.now() - timedelta(seconds=10)
            
            payments_to_approve = Payment.objects.filter(
                payment_method='mobile_money',
                status='processing',
                created_at__lt=cutoff_time
            )
            
            for payment in payments_to_approve:
                # Check if we're in test mode
                from django.conf import settings
                secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
                
                if secret_key.startswith('sk_test_'):
                    # Auto-approve the payment
                    payment.status = 'successful'
                    payment.processed_at = timezone.now()
                    payment.save()
                    
                    payment.log('info', 'Test mode: Mobile money payment auto-approved', {
                        'auto_approved': True,
                        'test_mode': True,
                        'elapsed_seconds': (timezone.now() - payment.created_at).total_seconds()
                    })
                    
                    logger.info(f"Auto-approved test mobile money payment: {payment.reference}")
            
            return len(payments_to_approve)
            
        except Exception as e:
            logger.error(f"Error auto-approving test payments: {str(e)}")
            return 0
    
    @staticmethod
    def should_simulate_success(payment):
        """Check if a mobile money payment should be simulated as successful"""
        try:
            from django.conf import settings
            secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
            
            if not secret_key.startswith('sk_test_'):
                return False
            
            if payment.payment_method != 'mobile_money':
                return False
            
            if payment.status != 'processing':
                return False
            
            # Check if 10 seconds have passed
            time_elapsed = (timezone.now() - payment.created_at).total_seconds()
            return time_elapsed > 10
            
        except Exception as e:
            logger.error(f"Error checking simulation conditions: {str(e)}")
            return False