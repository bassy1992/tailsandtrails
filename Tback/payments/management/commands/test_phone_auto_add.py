from django.core.management.base import BaseCommand
from django.db import transaction
from payments.models import Payment, PaymentProvider
from authentication.models import User
from decimal import Decimal


class Command(BaseCommand):
    help = 'Test automatic phone number addition when creating payments'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Testing automatic phone number addition...')
        
        # Get test data
        user = User.objects.first()
        provider = PaymentProvider.objects.first()
        
        if not user:
            self.stdout.write(
                self.style.ERROR('No users found. Please create a user first.')
            )
            return
            
        if not provider:
            self.stdout.write(
                self.style.ERROR('No payment providers found. Please create a provider first.')
            )
            return
        
        self.stdout.write(f'Using user: {user.email}')
        self.stdout.write(f'User phone number: {user.phone_number}')
        self.stdout.write(f'Using provider: {provider.name}')
        
        # Test 1: Create payment without phone number
        self.stdout.write('\n📱 Test 1: Creating payment without phone number...')
        
        with transaction.atomic():
            payment1 = Payment.objects.create(
                user=user,
                amount=Decimal('250.00'),
                currency='GHS',
                payment_method='card',
                provider=provider,
                description='Test Payment - No Phone Provided'
            )
            
            self.stdout.write(f'✅ Payment created: {payment1.reference}')
            self.stdout.write(f'   Payment phone: {payment1.phone_number}')
            self.stdout.write(f'   Expected: {user.phone_number}')
            
            if payment1.phone_number == user.phone_number:
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Phone number automatically added from user!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('   ❌ Phone number not added automatically')
                )
        
        # Test 2: Create payment with explicit phone number
        self.stdout.write('\n📱 Test 2: Creating payment with explicit phone number...')
        
        explicit_phone = '+233501234567'
        
        with transaction.atomic():
            payment2 = Payment.objects.create(
                user=user,
                amount=Decimal('450.00'),
                currency='GHS',
                payment_method='momo',
                provider=provider,
                phone_number=explicit_phone,
                description='Test Payment - Explicit Phone'
            )
            
            self.stdout.write(f'✅ Payment created: {payment2.reference}')
            self.stdout.write(f'   Payment phone: {payment2.phone_number}')
            self.stdout.write(f'   Expected: {explicit_phone}')
            
            if payment2.phone_number == explicit_phone:
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Explicit phone number preserved!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('   ❌ Explicit phone number not preserved')
                )
        
        # Test 3: Check booking details
        self.stdout.write('\n📋 Test 3: Checking booking details...')
        
        for payment in [payment1, payment2]:
            booking_details = payment.metadata.get('booking_details', {})
            user_info = booking_details.get('user_info', {})
            booking_phone = user_info.get('phone', '')
            
            self.stdout.write(f'Payment {payment.reference}:')
            self.stdout.write(f'   Booking details phone: {booking_phone}')
            
            if booking_phone == payment.phone_number:
                self.stdout.write(
                    self.style.SUCCESS('   ✅ Phone number in booking details matches payment!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('   ❌ Phone number mismatch in booking details')
                )
        
        self.stdout.write('\n🎉 Phone number auto-addition test completed!')
        self.stdout.write('')
        self.stdout.write('Summary:')
        self.stdout.write('- When creating payments, phone numbers are automatically added from user profile')
        self.stdout.write('- Explicit phone numbers in requests are preserved')
        self.stdout.write('- Booking details automatically include the correct phone number')
        self.stdout.write('- This ensures admin interface always shows phone numbers')