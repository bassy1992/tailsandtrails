from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment
from payments.booking_details_utils import create_booking_from_payment


class Command(BaseCommand):
    help = 'Create Booking records from payments that have booking details but no linked booking'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get payments that have booking_details but no linked booking
        payments = Payment.objects.filter(
            booking__isnull=True,
            metadata__has_key='booking_details',
            status='successful'
        )
        
        total_payments = payments.count()
        
        if total_payments == 0:
            self.stdout.write(
                self.style.SUCCESS('No payments need booking record creation.')
            )
            return
        
        self.stdout.write(f'Found {total_payments} payments that could have booking records created.')
        
        created_count = 0
        
        with transaction.atomic():
            for payment in payments:
                booking_details = payment.metadata.get('booking_details', {})
                
                if booking_details.get('type') == 'destination':
                    if dry_run:
                        destination_name = booking_details.get('destination', {}).get('name', 'Unknown')
                        self.stdout.write(
                            f'Would create booking for payment {payment.reference} - {destination_name}'
                        )
                        created_count += 1
                    else:
                        booking = create_booking_from_payment(payment)
                        if booking:
                            self.stdout.write(
                                f'Created booking {booking.booking_reference} for payment {payment.reference}'
                            )
                            created_count += 1
                        else:
                            self.stdout.write(
                                self.style.WARNING(f'Failed to create booking for payment {payment.reference}')
                            )
                else:
                    self.stdout.write(
                        f'Skipping payment {payment.reference} - not a destination booking'
                    )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would create {created_count} booking records')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} booking records')
            )
            
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                'Benefits of creating booking records:\n'
                '- Better organization and tracking\n'
                '- Proper booking references\n'
                '- Integration with booking management system\n'
                '- Clearer payment-to-booking relationships'
            )
        )