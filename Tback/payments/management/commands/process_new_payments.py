from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment
from payments.booking_details_utils import create_booking_from_payment
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Process new payments by adding booking details and creating booking records'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be processed without making changes',
        )
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Process payments from the last N hours (default: 24)',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        hours = options['hours']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get recent payments that need processing
        cutoff_time = timezone.now() - timedelta(hours=hours)
        
        # Find payments that don't have booking_details or linked bookings
        payments_needing_details = Payment.objects.filter(
            created_at__gte=cutoff_time,
            status='successful'
        ).exclude(
            metadata__has_key='booking_details'
        )
        
        payments_needing_bookings = Payment.objects.filter(
            created_at__gte=cutoff_time,
            status='successful',
            booking__isnull=True,
            metadata__has_key='booking_details'
        )
        
        self.stdout.write(f'Processing payments from the last {hours} hours...')
        self.stdout.write(f'Found {payments_needing_details.count()} payments needing booking details')
        self.stdout.write(f'Found {payments_needing_bookings.count()} payments needing booking records')
        
        processed_count = 0
        
        with transaction.atomic():
            # Step 1: Add booking details to payments that don't have them
            for payment in payments_needing_details:
                if dry_run:
                    self.stdout.write(f'Would add booking details to {payment.reference}')
                else:
                    # Use the existing add_booking_details logic
                    from payments.management.commands.add_booking_details import Command as AddBookingDetailsCommand
                    add_cmd = AddBookingDetailsCommand()
                    booking_details = add_cmd._generate_booking_details(payment)
                    
                    if booking_details:
                        if not payment.metadata:
                            payment.metadata = {}
                        payment.metadata['booking_details'] = booking_details
                        payment.save(update_fields=['metadata'])
                        self.stdout.write(f'Added booking details to {payment.reference}')
                        processed_count += 1
            
            # Step 2: Create booking records for payments that have details but no booking
            all_payments_needing_bookings = Payment.objects.filter(
                created_at__gte=cutoff_time,
                status='successful',
                booking__isnull=True,
                metadata__has_key='booking_details'
            )
            
            for payment in all_payments_needing_bookings:
                booking_details = payment.metadata.get('booking_details', {})
                
                if booking_details.get('type') == 'destination':
                    if dry_run:
                        destination_name = booking_details.get('destination', {}).get('name', 'Unknown')
                        self.stdout.write(f'Would create booking for {payment.reference} - {destination_name}')
                    else:
                        booking = create_booking_from_payment(payment)
                        if booking:
                            self.stdout.write(f'Created booking {booking.booking_reference} for {payment.reference}')
                            processed_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would process {processed_count} items')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully processed {processed_count} items')
            )
            
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                'Tip: You can run this command regularly (e.g., via cron job) to automatically\n'
                'process new payments and ensure they have proper booking details and records.'
            )
        )