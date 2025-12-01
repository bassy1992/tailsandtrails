from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment
from payments.services import PaymentService
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Check status of pending payments'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Check payments pending for more than X hours (default: 24)'
        )
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update payment status from provider'
        )
    
    def handle(self, *args, **options):
        hours = options['hours']
        update = options['update']
        
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        pending_payments = Payment.objects.filter(
            status__in=['pending', 'processing'],
            created_at__lt=cutoff_time
        ).select_related('provider', 'user')
        
        self.stdout.write(f'Found {pending_payments.count()} payments pending for more than {hours} hours')
        
        if update:
            payment_service = PaymentService()
            updated_count = 0
            
            for payment in pending_payments:
                try:
                    result = payment_service.check_payment_status(payment)
                    
                    if result.get('success') and result.get('status'):
                        new_status = result.get('status')
                        if new_status != payment.status:
                            old_status = payment.status
                            payment.status = new_status
                            
                            if new_status in ['successful', 'failed', 'cancelled']:
                                payment.processed_at = timezone.now()
                            
                            payment.save()
                            payment.log('info', f'Status updated from {old_status} to {new_status} via management command')
                            
                            self.stdout.write(
                                self.style.SUCCESS(
                                    f'Updated payment {payment.reference}: {old_status} -> {new_status}'
                                )
                            )
                            updated_count += 1
                        else:
                            self.stdout.write(f'Payment {payment.reference}: status unchanged ({payment.status})')
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Failed to check status for payment {payment.reference}: {result.get("message")}'
                            )
                        )
                        
                except Exception as e:
                    logger.error(f'Error checking payment {payment.reference}: {str(e)}')
                    self.stdout.write(
                        self.style.ERROR(f'Error checking payment {payment.reference}: {str(e)}')
                    )
            
            self.stdout.write(f'Updated {updated_count} payments')
        else:
            for payment in pending_payments:
                self.stdout.write(
                    f'Payment {payment.reference} ({payment.user.email}): '
                    f'{payment.status} for {timezone.now() - payment.created_at}'
                )