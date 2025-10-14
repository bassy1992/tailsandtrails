from django.core.management.base import BaseCommand
from payments.models import Payment
from payments.admin import PaymentAdmin


class Command(BaseCommand):
    help = 'Check the status of all payments and their booking type display'

    def handle(self, *args, **options):
        payments = Payment.objects.all().order_by('-created_at')
        admin = PaymentAdmin(Payment, None)
        
        if not payments.exists():
            self.stdout.write(
                self.style.WARNING('No payments found in the database.')
            )
            return
        
        self.stdout.write(f'Found {payments.count()} payments:')
        self.stdout.write('')
        
        destination_count = 0
        ticket_count = 0
        unknown_count = 0
        
        for payment in payments:
            # Get the booking type display (without HTML tags for cleaner output)
            booking_type_html = admin.booking_type_display(payment)
            
            if '🏝️ DESTINATION' in booking_type_html:
                booking_type = '🏝️ DESTINATION'
                destination_count += 1
            elif '🎫 TICKET' in booking_type_html:
                booking_type = '🎫 TICKET'
                ticket_count += 1
            else:
                booking_type = '❓ UNKNOWN'
                unknown_count += 1
            
            # Status indicators
            has_booking_details = 'booking_details' in (payment.metadata or {})
            has_linked_booking = payment.booking is not None
            
            status_indicators = []
            if has_booking_details:
                status_indicators.append('📋 Details')
            if has_linked_booking:
                status_indicators.append(f'🔗 {payment.booking.booking_reference}')
            
            status = ' | '.join(status_indicators) if status_indicators else '⚠️ Missing data'
            
            self.stdout.write(
                f'{payment.reference} | {payment.description[:30]:<30} | '
                f'{booking_type:<15} | {status}'
            )
        
        # Summary
        self.stdout.write('')
        self.stdout.write('=== SUMMARY ===')
        self.stdout.write(f'🏝️ Destination bookings: {destination_count}')
        self.stdout.write(f'🎫 Ticket bookings: {ticket_count}')
        self.stdout.write(f'❓ Unknown bookings: {unknown_count}')
        
        if unknown_count > 0:
            self.stdout.write('')
            self.stdout.write(
                self.style.WARNING(
                    f'⚠️ {unknown_count} payments are showing as UNKNOWN.\n'
                    'Run "python manage.py process_new_payments" to fix them.'
                )
            )
        else:
            self.stdout.write('')
            self.stdout.write(
                self.style.SUCCESS('✅ All payments have proper booking types!')
            )