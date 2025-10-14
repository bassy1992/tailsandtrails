from django.core.management.base import BaseCommand
from django.utils import timezone
from payments.models import Payment
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fix common payment flow issues'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            type=str,
            choices=['list-stuck', 'complete-all-stuck', 'complete-reference', 'reset-reference'],
            required=True,
            help='Action to perform',
        )
        parser.add_argument(
            '--reference',
            type=str,
            help='Payment reference for specific actions',
        )
        parser.add_argument(
            '--status',
            type=str,
            choices=['successful', 'failed', 'cancelled'],
            default='successful',
            help='Status to set (default: successful)',
        )

    def handle(self, *args, **options):
        action = options['action']
        reference = options['reference']
        status = options['status']

        if action == 'list-stuck':
            self.list_stuck_payments()
        
        elif action == 'complete-all-stuck':
            self.complete_all_stuck_payments(status)
        
        elif action == 'complete-reference':
            if not reference:
                self.stdout.write(self.style.ERROR('--reference is required for this action'))
                return
            self.complete_payment_by_reference(reference, status)
        
        elif action == 'reset-reference':
            if not reference:
                self.stdout.write(self.style.ERROR('--reference is required for this action'))
                return
            self.reset_payment_by_reference(reference)

    def list_stuck_payments(self):
        stuck_payments = Payment.objects.filter(
            status__in=['pending', 'processing']
        ).order_by('-created_at')

        if not stuck_payments.exists():
            self.stdout.write(self.style.SUCCESS('No stuck payments found!'))
            return

        self.stdout.write(f'Found {stuck_payments.count()} stuck payment(s):')
        self.stdout.write('-' * 80)
        
        for payment in stuck_payments:
            age = timezone.now() - payment.created_at
            age_minutes = age.total_seconds() / 60
            
            self.stdout.write(
                f'Reference: {payment.reference}\n'
                f'Status: {payment.status}\n'
                f'Amount: {payment.currency} {payment.amount}\n'
                f'Phone: {payment.phone_number}\n'
                f'Age: {age_minutes:.1f} minutes\n'
                f'Created: {payment.created_at}\n'
                f'-' * 40
            )

    def complete_all_stuck_payments(self, status):
        stuck_payments = Payment.objects.filter(
            status__in=['pending', 'processing']
        )

        count = stuck_payments.count()
        if count == 0:
            self.stdout.write(self.style.SUCCESS('No stuck payments to complete!'))
            return

        for payment in stuck_payments:
            payment.status = status
            payment.processed_at = timezone.now()
            payment.save()
            payment.log('info', f'Payment completed via fix_payment_flow command to {status}')

        self.stdout.write(
            self.style.SUCCESS(f'Completed {count} stuck payment(s) with status: {status}')
        )

    def complete_payment_by_reference(self, reference, status):
        try:
            payment = Payment.objects.get(reference=reference)
            
            if payment.status in ['pending', 'processing']:
                old_status = payment.status
                payment.status = status
                payment.processed_at = timezone.now()
                payment.save()
                payment.log('info', f'Payment completed via fix_payment_flow command: {old_status} -> {status}')
                
                self.stdout.write(
                    self.style.SUCCESS(f'Payment {reference} completed: {old_status} -> {status}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment {reference} is already {payment.status}')
                )
                
        except Payment.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Payment {reference} not found')
            )

    def reset_payment_by_reference(self, reference):
        try:
            payment = Payment.objects.get(reference=reference)
            
            old_status = payment.status
            payment.status = 'pending'
            payment.processed_at = None
            payment.save()
            payment.log('info', f'Payment reset via fix_payment_flow command: {old_status} -> pending')
            
            self.stdout.write(
                self.style.SUCCESS(f'Payment {reference} reset: {old_status} -> pending')
            )
                
        except Payment.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Payment {reference} not found')
            )