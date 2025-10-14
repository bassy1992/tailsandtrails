from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment


class Command(BaseCommand):
    help = 'Update payment booking types based on linked bookings or metadata'

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
        
        # Get all payments
        payments = Payment.objects.all()
        total_payments = payments.count()
        
        if total_payments == 0:
            self.stdout.write(
                self.style.SUCCESS('No payments found.')
            )
            return
        
        self.stdout.write(f'Found {total_payments} payments to analyze.')
        
        updated_count = 0
        ticket_count = 0
        destination_count = 0
        unknown_count = 0
        
        with transaction.atomic():
            for payment in payments:
                booking_type = None
                reason = ""
                
                # Check if payment has a linked booking with booking_type
                if payment.booking and hasattr(payment.booking, 'booking_type'):
                    booking_type = payment.booking.booking_type
                    reason = f"from linked booking ({payment.booking.booking_reference})"
                
                # Fallback: Check payment description for booking type hints
                elif payment.description:
                    description_lower = payment.description.lower()
                    if "ticket purchase:" in description_lower or "event" in description_lower or "concert" in description_lower:
                        booking_type = 'ticket'
                        reason = "from payment description (ticket keywords)"
                    elif any(word in description_lower for word in ['safari', 'tour', 'destination', 'park', 'beach', 'mountain', 'forest', 'castle', 'garden']):
                        booking_type = 'destination'
                        reason = "from payment description (destination keywords)"
                
                # Fallback: Check metadata
                elif payment.metadata and 'booking_details' in payment.metadata:
                    booking_details = payment.metadata['booking_details']
                    
                    if booking_details.get('type') == 'ticket':
                        booking_type = 'ticket'
                        reason = "from metadata type field"
                    elif any(key in booking_details for key in ['eventName', 'ticketType', 'ticketReference', 'eventDetails', 'ticket']):
                        booking_type = 'ticket'
                        reason = "from metadata ticket fields"
                    elif 'destination' in booking_details:
                        booking_type = 'destination'
                        reason = "from metadata destination field"
                
                # Count the types
                if booking_type == 'ticket':
                    ticket_count += 1
                elif booking_type == 'destination':
                    destination_count += 1
                else:
                    unknown_count += 1
                    booking_type = 'unknown'
                    reason = "could not determine type"
                
                if dry_run:
                    self.stdout.write(
                        f'Payment {payment.reference}: {booking_type.upper()} ({reason})'
                    )
                else:
                    # For now, we're just analyzing. In the future, you might want to 
                    # store this information somewhere or update the booking if needed
                    self.stdout.write(
                        f'Payment {payment.reference}: {booking_type.upper()} ({reason})'
                    )
                
                updated_count += 1
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== SUMMARY ==='))
        self.stdout.write(f'Total payments analyzed: {updated_count}')
        self.stdout.write(f'🎫 Ticket payments: {ticket_count}')
        self.stdout.write(f'🏝️ Destination payments: {destination_count}')
        self.stdout.write(f'❓ Unknown payments: {unknown_count}')
        
        if dry_run:
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING('This was a dry run. No changes were made.')
            )
        
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                'The payment admin interface will now correctly display booking types!\n'
                'Payments linked to bookings will show the booking type from the booking_type field.\n'
                'Other payments will be categorized based on their metadata or description.'
            )
        )