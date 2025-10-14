#!/usr/bin/env python
"""
Management command to fix booking types for existing payments
"""
from django.core.management.base import BaseCommand
from payments.models import Payment


class Command(BaseCommand):
    help = 'Fix booking types for existing payments based on their metadata and descriptions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )
        parser.add_argument(
            '--reference',
            type=str,
            help='Fix specific payment by reference',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        specific_reference = options.get('reference')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Get payments to process
        if specific_reference:
            payments = Payment.objects.filter(reference=specific_reference)
            if not payments.exists():
                self.stdout.write(self.style.ERROR(f'Payment with reference {specific_reference} not found'))
                return
        else:
            payments = Payment.objects.all()
        
        self.stdout.write(f'Processing {payments.count()} payments...')
        
        updated_count = 0
        destination_count = 0
        ticket_count = 0
        unknown_count = 0
        
        for payment in payments:
            booking_type = self.determine_booking_type(payment)
            
            if booking_type == 'destination':
                destination_count += 1
                status = '🏞️ DESTINATION'
            elif booking_type == 'ticket':
                ticket_count += 1
                status = '🎫 TICKET'
            else:
                unknown_count += 1
                status = '❓ UNKNOWN'
            
            self.stdout.write(
                f'Payment {payment.reference}: {status} - {payment.description[:50]}...'
            )
            
            # Update the payment metadata to include booking type
            if not dry_run and booking_type != 'unknown':
                if not payment.metadata:
                    payment.metadata = {}
                
                payment.metadata['detected_booking_type'] = booking_type
                payment.save(update_fields=['metadata'])
                updated_count += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(f'  🏞️ Destinations: {destination_count}')
        self.stdout.write(f'  🎫 Tickets: {ticket_count}')
        self.stdout.write(f'  ❓ Unknown: {unknown_count}')
        
        if not dry_run:
            self.stdout.write(f'  ✅ Updated: {updated_count}')
        else:
            self.stdout.write(f'  📝 Would update: {destination_count + ticket_count}')

    def determine_booking_type(self, payment):
        """Determine booking type based on payment data"""
        
        # Check linked booking first
        if payment.booking and hasattr(payment.booking, 'booking_type'):
            return payment.booking.booking_type
        
        # Check payment description
        if payment.description:
            description_lower = payment.description.lower()
            
            # Ticket indicators
            if any(word in description_lower for word in [
                'ticket purchase:', 'event', 'concert', 'festival', 'show', 'performance'
            ]):
                return 'ticket'
            
            # Destination indicators
            if any(word in description_lower for word in [
                'safari', 'tour', 'destination', 'park', 'beach', 'mountain', 'forest', 'castle', 'garden',
                'kakum', 'canopy', 'walk', 'adventure', 'cape coast', 'mole', 'aburi', 'kumasi', 'volta',
                'heritage', 'cultural', 'nature', 'escape', 'waterfalls', 'palace', 'national'
            ]):
                return 'destination'
        
        # Check metadata
        if payment.metadata and 'booking_details' in payment.metadata:
            booking_details = payment.metadata['booking_details']
            
            # Explicit type
            if booking_details.get('type') == 'ticket':
                return 'ticket'
            
            # Ticket indicators in metadata
            if any(key in booking_details for key in [
                'eventName', 'ticketType', 'ticketReference', 'eventDetails', 'ticket'
            ]):
                return 'ticket'
            
            # Destination indicators in metadata
            destination_indicators = [
                'destination', 'bookingData', 'tourName', 'selectedDate', 'travelers',
                'selectedOptions', 'accommodation', 'transport', 'duration'
            ]
            
            if any(key in booking_details for key in destination_indicators):
                return 'destination'
            
            # Check nested booking data
            if 'bookingData' in booking_details:
                nested_data = booking_details['bookingData']
                if any(key in nested_data for key in ['tourName', 'tourId', 'selectedDate', 'travelers']):
                    return 'destination'
        
        return 'unknown'