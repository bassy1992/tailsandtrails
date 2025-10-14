from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from payments.models import Payment
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Complete stuck payments that have been processing for too long'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reference',
            type=str,
            help='Complete a specific payment by reference',
        )
        parser.add_argument(
            '--minutes',
            type=int,
            default=5,
            help='Complete payments stuck for more than X minutes (default: 5)',
        )
        parser.add_argument(
            '--status',
            type=str,
            choices=['successful', 'failed'],
            default='successful',
            help='Status to set for completed payments (default: successful)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        reference = options['reference']
        minutes = options['minutes']
        new_status = options['status']
        dry_run = options['dry_run']

        if reference:
            # Complete specific payment
            try:
                payment = Payment.objects.get(reference=reference)
                if payment.status in ['pending', 'processing']:
                    if not dry_run:
                        payment.status = new_status
                        payment.processed_at = timezone.now()
                        payment.save()
                        payment.log('info', f'Payment manually completed via management command to {new_status}')
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'{"[DRY RUN] " if dry_run else ""}Completed payment {reference}: {payment.status} -> {new_status}'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Payment {reference} is already {payment.status}')
                    )
            except Payment.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Payment {reference} not found')
                )
        else:
            # Complete stuck payments
            cutoff_time = timezone.now() - timedelta(minutes=minutes)
            stuck_payments = Payment.objects.filter(
                status__in=['pending', 'processing'],
                created_at__lt=cutoff_time
            )

            count = stuck_payments.count()
            if count == 0:
                self.stdout.write(
                    self.style.SUCCESS(f'No stuck payments found (older than {minutes} minutes)')
                )
                return

            self.stdout.write(f'Found {count} stuck payment(s):')
            
            for payment in stuck_payments:
                age_minutes = (timezone.now() - payment.created_at).total_seconds() / 60
                self.stdout.write(
                    f'- {payment.reference}: {payment.status} for {age_minutes:.1f} minutes'
                )
                
                if not dry_run:
                    payment.status = new_status
                    payment.processed_at = timezone.now()
                    payment.save()
                    payment.log('info', f'Payment auto-completed via management command to {new_status} after {age_minutes:.1f} minutes')

            if not dry_run:
                self.stdout.write(
                    self.style.SUCCESS(f'Completed {count} stuck payment(s) with status: {new_status}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'[DRY RUN] Would complete {count} payment(s) with status: {new_status}')
                )