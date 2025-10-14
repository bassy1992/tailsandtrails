#!/usr/bin/env python
"""
Management command to automatically create bookings from successful payments
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment
from payments.booking_details_utils import create_booking_from_payment, create_ticket_purchase_from_payment


class Command(BaseCommand):
    help = 'Automatically create bookings and ticket purchases from successful payments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be created without making changes',
        )
        parser.add_argument(
            '--user-email',
            type=str,
            help='Process payments for specific user only',
        )
        parser.add_argument(
            '--reference',
            type=str,
            help='Process specific payment by reference',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        user_email = options.get('user_email')
        specific_reference = options.get('reference')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Get payments to process
        payments = Payment.objects.filter(status='successful')
        
        if specific_reference:
            payments = payments.filter(reference=specific_reference)
        elif user_email:
            payments = payments.filter(user__email=user_email)
        
        # Only process payments without existing bookings or ticket purchases
        payments = payments.filter(booking__isnull=True)
        
        self.stdout.write(f'Processing {payments.count()} successful payments without bookings...')
        
        bookings_created = 0
        tickets_created = 0
        errors = 0
        
        for payment in payments:
            self.stdout.write(f'\nProcessing payment: {payment.reference}')
            self.stdout.write(f'  User: {payment.user.email}')
            self.stdout.write(f'  Amount: GHS {payment.amount}')
            self.stdout.write(f'  Description: {payment.description}')
            
            try:
                with transaction.atomic():
                    # Determine if this should be a destination booking or ticket purchase
                    description_lower = payment.description.lower() if payment.description else ''
                    
                    is_ticket = any(word in description_lower for word in [
                        'ticket', 'event', 'concert', 'festival', 'show', 'performance'
                    ])
                    
                    if is_ticket:
                        self.stdout.write('  🎫 Creating ticket purchase...')
                        if not dry_run:
                            purchase = create_ticket_purchase_from_payment(payment)
                            if purchase:
                                self.stdout.write(f'  ✅ Created ticket purchase: {purchase.purchase_id}')
                                tickets_created += 1
                            else:
                                self.stdout.write('  ❌ Failed to create ticket purchase')
                                errors += 1
                        else:
                            self.stdout.write('  📝 Would create ticket purchase')
                            tickets_created += 1
                    else:
                        self.stdout.write('  🏞️ Creating destination booking...')
                        if not dry_run:
                            booking = create_booking_from_payment(payment)
                            if booking:
                                self.stdout.write(f'  ✅ Created booking: {booking.booking_reference}')
                                bookings_created += 1
                            else:
                                self.stdout.write('  ❌ Failed to create booking')
                                errors += 1
                        else:
                            self.stdout.write('  📝 Would create booking')
                            bookings_created += 1
                            
            except Exception as e:
                self.stdout.write(f'  ❌ Error: {str(e)}')
                errors += 1
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Summary:'))
        self.stdout.write(f'  🏞️ Bookings created: {bookings_created}')
        self.stdout.write(f'  🎫 Ticket purchases created: {tickets_created}')
        self.stdout.write(f'  ❌ Errors: {errors}')
        
        if not dry_run and (bookings_created > 0 or tickets_created > 0):
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✅ Dashboard will now show updated bookings and purchases!'))
            self.stdout.write('Visit http://localhost:8080/dashboard to see the changes.')
        elif dry_run:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('Run without --dry-run to create the bookings and purchases.'))