from django.core.management.base import BaseCommand
from payments.models import Payment
from payments.booking_utils import store_booking_details_in_payment, create_sample_booking_details

class Command(BaseCommand):
    help = 'Add sample booking details to existing payments for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--payment-id',
            type=int,
            help='Specific payment ID to update (optional)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all successful payments',
        )
    
    def handle(self, *args, **options):
        if options['payment_id']:
            # Update specific payment
            try:
                payment = Payment.objects.get(id=options['payment_id'])
                self.update_payment_with_sample_data(payment)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated payment {payment.reference}')
                )
            except Payment.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Payment with ID {options["payment_id"]} not found')
                )
        elif options['all']:
            # Update all successful payments
            payments = Payment.objects.filter(status='successful')
            count = 0
            for payment in payments:
                self.update_payment_with_sample_data(payment)
                count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Updated {count} successful payments with sample booking details')
            )
        else:
            # Update the most recent successful payment
            payment = Payment.objects.filter(status='successful').first()
            if payment:
                self.update_payment_with_sample_data(payment)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated most recent successful payment: {payment.reference}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️  No successful payments found')
                )
    
    def update_payment_with_sample_data(self, payment):
        """Update a payment with sample booking details"""
        sample_data = create_sample_booking_details()
        
        # Customize based on payment amount
        if payment.amount:
            # Adjust sample data to match payment amount
            sample_data['final_total'] = float(payment.amount)
            sample_data['base_total'] = float(payment.amount) * 0.7  # 70% base
            sample_data['options_total'] = float(payment.amount) * 0.3  # 30% options
        
        store_booking_details_in_payment(payment, sample_data)
        
        self.stdout.write(f'  📝 Added booking details to {payment.reference} (GH₵{payment.amount})')