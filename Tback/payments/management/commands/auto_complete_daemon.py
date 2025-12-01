from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment
import time
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run auto-completion daemon that processes payments every 30 seconds'

    def add_arguments(self, parser):
        parser.add_argument(
            '--interval',
            type=int,
            default=30,
            help='Check interval in seconds (default: 30)'
        )
        parser.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Payment timeout in seconds (default: 30)'
        )
        parser.add_argument(
            '--success-rate',
            type=float,
            default=0.9,
            help='Success rate for auto-completion (default: 0.9)'
        )

    def handle(self, *args, **options):
        interval = options['interval']
        timeout = options['timeout']
        success_rate = options['success_rate']
        
        self.stdout.write(f"🚀 Starting auto-completion daemon")
        self.stdout.write(f"   Check interval: {interval}s")
        self.stdout.write(f"   Payment timeout: {timeout}s")
        self.stdout.write(f"   Success rate: {success_rate * 100}%")
        self.stdout.write("   Press Ctrl+C to stop")
        
        try:
            while True:
                self.process_payments(timeout, success_rate)
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stdout.write("\n🛑 Auto-completion daemon stopped")

    def process_payments(self, timeout_seconds, success_rate):
        """Process payments that are ready for auto-completion"""
        
        # Find payments that are pending/processing and older than timeout
        cutoff_time = timezone.now() - timedelta(seconds=timeout_seconds)
        
        pending_payments = Payment.objects.filter(
            status__in=['pending', 'processing'],
            created_at__lt=cutoff_time
        )
        
        if pending_payments.exists():
            self.stdout.write(f"⚡ Processing {pending_payments.count()} payments...")
            
            for payment in pending_payments:
                self.complete_payment(payment, success_rate)
        else:
            # Only show this occasionally to avoid spam
            import random
            if random.random() < 0.1:  # 10% chance
                self.stdout.write("✅ No payments to process")

    def complete_payment(self, payment, success_rate):
        """Complete a single payment"""
        
        # Simulate success/failure based on success rate
        import random
        if random.random() < success_rate:
            # Success
            payment.status = 'successful'
            payment.processed_at = timezone.now()
            payment.save()
            payment.log('info', 'Auto-completed successfully by daemon')
            self.stdout.write(f"   ✅ {payment.reference} -> successful")
        else:
            # Failure
            payment.status = 'failed'
            payment.processed_at = timezone.now()
            payment.save()
            payment.log('info', 'Auto-failed by daemon')
            self.stdout.write(f"   ❌ {payment.reference} -> failed")