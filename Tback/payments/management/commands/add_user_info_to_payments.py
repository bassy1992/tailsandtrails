from django.core.management.base import BaseCommand
from payments.models import Payment
import random

class Command(BaseCommand):
    help = 'Add user information to existing payments for testing'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--payment-id',
            type=int,
            help='Specific payment ID to update (optional)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Update all payments with booking details',
        )
    
    def handle(self, *args, **options):
        # Sample user data for testing
        sample_users = [
            {'name': 'John Doe', 'email': 'john.doe@example.com', 'phone': '+233244123456'},
            {'name': 'Jane Smith', 'email': 'jane.smith@gmail.com', 'phone': '+233201234567'},
            {'name': 'Michael Johnson', 'email': 'michael.j@yahoo.com', 'phone': '+233554567890'},
            {'name': 'Sarah Wilson', 'email': 'sarah.wilson@outlook.com', 'phone': '+233267890123'},
            {'name': 'David Brown', 'email': 'david.brown@hotmail.com', 'phone': '+233501234567'},
            {'name': 'Emily Davis', 'email': 'emily.davis@gmail.com', 'phone': '+233241234567'},
            {'name': 'Robert Miller', 'email': 'robert.miller@example.com', 'phone': '+233551234567'},
            {'name': 'Lisa Anderson', 'email': 'lisa.anderson@gmail.com', 'phone': '+233261234567'},
        ]
        
        if options['payment_id']:
            # Update specific payment
            try:
                payment = Payment.objects.get(id=options['payment_id'])
                self.add_user_info_to_payment(payment, sample_users)
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated payment {payment.reference}')
                )
            except Payment.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'❌ Payment with ID {options["payment_id"]} not found')
                )
        elif options['all']:
            # Update all payments with booking details
            payments = Payment.objects.filter(metadata__booking_details__isnull=False)
            count = 0
            for payment in payments:
                self.add_user_info_to_payment(payment, sample_users)
                count += 1
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Updated {count} payments with user information')
            )
        else:
            # Update payments with booking details but no user info
            payments = Payment.objects.filter(
                metadata__booking_details__isnull=False
            ).exclude(
                metadata__booking_details__user_info__isnull=False
            )[:5]  # Limit to 5 for testing
            
            count = 0
            for payment in payments:
                self.add_user_info_to_payment(payment, sample_users)
                count += 1
            
            if count > 0:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Updated {count} payments with user information')
                )
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️  No payments found that need user information updates')
                )
    
    def add_user_info_to_payment(self, payment, sample_users):
        """Add user information to a payment's booking details"""
        if not payment.metadata or 'booking_details' not in payment.metadata:
            return
        
        booking_details = payment.metadata['booking_details']
        
        # Skip if user info already exists
        if 'user_info' in booking_details:
            return
        
        # Get user info from payment's user field or use sample data
        if payment.user:
            user_name = f"{payment.user.first_name} {payment.user.last_name}".strip()
            if not user_name:
                user_name = payment.user.username or "User"
            
            user_info = {
                'name': user_name,
                'email': payment.user.email or 'user@example.com',
                'phone': payment.phone_number or '+233244000000'
            }
        else:
            # Use random sample user data
            user_info = random.choice(sample_users).copy()
            # Use the payment's phone number if available
            if payment.phone_number:
                user_info['phone'] = payment.phone_number
        
        # Add user info to booking details
        booking_details['user_info'] = user_info
        
        # Update the payment
        Payment.objects.filter(id=payment.id).update(metadata=payment.metadata)
        
        self.stdout.write(f'  📝 Added user info to {payment.reference}: {user_info["name"]} ({user_info["email"]})')