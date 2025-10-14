from django.core.management.base import BaseCommand
from django.db import transaction
from destinations.models import Booking


class Command(BaseCommand):
    help = 'Update existing bookings to set appropriate booking_type values'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No changes will be made')
            )
        
        # Get all bookings that don't have a booking_type set or have the default value
        bookings_to_update = Booking.objects.filter(
            booking_type='destination'  # This is the default, so we assume these need review
        )
        
        total_bookings = bookings_to_update.count()
        
        if total_bookings == 0:
            self.stdout.write(
                self.style.SUCCESS('No bookings need updating.')
            )
            return
        
        self.stdout.write(f'Found {total_bookings} bookings to review.')
        
        # For now, we'll keep all existing bookings as 'destination' type
        # In the future, you might want to add logic to detect ticket bookings
        # based on certain criteria (e.g., destination name, special fields, etc.)
        
        updated_count = 0
        
        with transaction.atomic():
            for booking in bookings_to_update:
                # Logic to determine booking type
                # For now, we assume all existing bookings are destination bookings
                # You can add more sophisticated logic here based on your business rules
                
                new_booking_type = 'destination'  # Default assumption
                
                # Example logic (uncomment and modify as needed):
                # if 'ticket' in booking.destination.name.lower() or 'event' in booking.destination.name.lower():
                #     new_booking_type = 'ticket'
                # elif booking.destination.category.name.lower() in ['events', 'concerts', 'shows']:
                #     new_booking_type = 'ticket'
                
                if not dry_run:
                    booking.booking_type = new_booking_type
                    booking.save(update_fields=['booking_type'])
                
                updated_count += 1
                
                if dry_run:
                    self.stdout.write(
                        f'Would update booking {booking.booking_reference} '
                        f'({booking.destination.name}) to type: {new_booking_type}'
                    )
                else:
                    self.stdout.write(
                        f'Updated booking {booking.booking_reference} '
                        f'({booking.destination.name}) to type: {new_booking_type}'
                    )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(f'DRY RUN: Would update {updated_count} bookings')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully updated {updated_count} bookings')
            )
            
        self.stdout.write(
            self.style.SUCCESS(
                '\nBooking type field has been added successfully!\n'
                'You can now:\n'
                '1. Filter bookings by type in the admin panel\n'
                '2. Use booking.is_destination_booking and booking.is_ticket_booking properties\n'
                '3. Query bookings by type: Booking.objects.filter(booking_type="destination")\n'
            )
        )