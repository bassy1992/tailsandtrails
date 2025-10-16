"""
Management command to process test mode mobile money payments
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment
from payments.test_mobile_money_handler import TestMobileMoneyHandler

class Command(BaseCommand):
    help = 'Process test mode mobile money payments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--auto-approve',
            action='store_true',
            help='Auto-approve pending mobile money payments in test mode',
        )

    def handle(self, *args, **options):
        if options['auto_approve']:
            count = TestMobileMoneyHandler.auto_approve_test_payments()
            self.stdout.write(
                self.style.SUCCESS(f'Auto-approved {count} test mobile money payments')
            )
        else:
            # Show pending mobile money payments
            pending_payments = Payment.objects.filter(
                payment_method='mobile_money',
                status='processing'
            )
            
            self.stdout.write(f'Found {pending_payments.count()} pending mobile money payments:')
            
            for payment in pending_payments:
                elapsed = (timezone.now() - payment.created_at).total_seconds()
                self.stdout.write(f'  - {payment.reference}: {elapsed:.0f}s old')