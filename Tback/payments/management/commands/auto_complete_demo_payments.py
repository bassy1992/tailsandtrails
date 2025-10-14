from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Auto-complete demo payments after timeout'

    def add_arguments(self, parser):
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Timeout in seconds before auto-completing payments (default: 30)'
        )
        parser.add_argument(
            '--success-rate',
            type=float,
            default=0.9,
            help='Success rate for auto-completion (default: 0.9 = 90 percent)'
        )

    def handle(self, *args, **options):
        timeout_seconds = options['timeout']
        success_rate = options['success_rate']
        
        # Find payments that are pending/processing and older than timeout
        cutoff_time = timezone.now() - timedelta(seconds=timeout_seconds)
        
        pending_payments = Payment.objects.filter(
            status__in=['pending', 'processing'],
            created_at__lt=cutoff_time
        )
        
        completed_count = 0
        failed_count = 0
        
        for payment in pending_payments:
            # Simulate success/failure based on success rate
            import random
            if random.random() < success_rate:
                # Success
                payment.status = 'successful'
                payment.processed_at = timezone.now()
                payment.save()
                payment.log('info', f'Auto-completed successfully after {timeout_seconds}s timeout')
                completed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Auto-completed payment {payment.reference}')
                )
            else:
                # Failure
                payment.status = 'failed'
                payment.processed_at = timezone.now()
                payment.save()
                payment.log('info', f'Auto-failed after {timeout_seconds}s timeout')
                failed_count += 1
                self.stdout.write(
                    self.style.WARNING(f'❌ Auto-failed payment {payment.reference}')
                )
        
        if completed_count > 0 or failed_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Auto-completion complete: {completed_count} successful, {failed_count} failed'
                )
            )
        else:
            self.stdout.write('No payments to auto-complete')