from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from payments.mtn_momo_service import MTNMoMoService
from payments.models import Payment, PaymentProvider
import json

class Command(BaseCommand):
    help = 'Test MTN Mobile Money integration'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to test payment (e.g., 233244123456)',
        )
        parser.add_argument(
            '--amount',
            type=float,
            default=1.0,
            help='Amount to test (default: 1.0)',
        )
        parser.add_argument(
            '--check-config',
            action='store_true',
            help='Check MTN MoMo configuration',
        )
    
    def handle(self, *args, **options):
        mtn_service = MTNMoMoService()
        
        if options['check_config']:
            self.check_configuration(mtn_service)
            return
        
        if options['phone']:
            self.test_payment_flow(mtn_service, options['phone'], options['amount'])
        else:
            self.test_api_connection(mtn_service)
    
    def check_configuration(self, mtn_service):
        """Check MTN MoMo configuration"""
        self.stdout.write(self.style.HTTP_INFO('🔧 Checking MTN MoMo Configuration'))
        self.stdout.write('=' * 50)
        
        # Check environment variables
        config_items = [
            ('Environment', settings.MTN_MOMO_ENVIRONMENT),
            ('Base URL', settings.MTN_MOMO_BASE_URL),
            ('Collection User ID', settings.MTN_MOMO_COLLECTION_USER_ID),
            ('Collection API Key', '***' if settings.MTN_MOMO_COLLECTION_API_KEY else ''),
            ('Subscription Key', '***' if settings.MTN_MOMO_COLLECTION_SUBSCRIPTION_KEY else ''),
            ('Callback URL', settings.MTN_MOMO_CALLBACK_URL),
        ]
        
        for name, value in config_items:
            status = '✅' if value else '❌'
            display_value = value if name in ['Environment', 'Base URL', 'Callback URL'] else ('Set' if value else 'Not Set')
            self.stdout.write(f'{status} {name}: {display_value}')
        
        # Check if service is configured
        if mtn_service.is_configured():
            self.stdout.write(self.style.SUCCESS('\n✅ MTN MoMo is properly configured'))
        else:
            self.stdout.write(self.style.ERROR('\n❌ MTN MoMo is not properly configured'))
            self.stdout.write('Please set the required environment variables in your .env file')
    
    def test_api_connection(self, mtn_service):
        """Test API connection"""
        self.stdout.write(self.style.HTTP_INFO('🧪 Testing MTN MoMo API Connection'))
        self.stdout.write('=' * 50)
        
        if not mtn_service.is_configured():
            self.stdout.write(self.style.ERROR('❌ MTN MoMo not configured. Use --check-config to see details.'))
            return
        
        # Test access token
        self.stdout.write('Testing access token...')
        token_result = mtn_service._get_access_token()
        
        if token_result['success']:
            self.stdout.write(self.style.SUCCESS('✅ Access token obtained successfully'))
            self.stdout.write(f'   Token expires in: {token_result.get("expires_in", "unknown")} seconds')
        else:
            self.stdout.write(self.style.ERROR(f'❌ Failed to get access token: {token_result.get("error")}'))
    
    def test_payment_flow(self, mtn_service, phone_number, amount):
        """Test complete payment flow"""
        self.stdout.write(self.style.HTTP_INFO('🧪 Testing MTN MoMo Payment Flow'))
        self.stdout.write('=' * 50)
        
        # Validate phone number
        self.stdout.write(f'Testing phone number: {phone_number}')
        validation_result = mtn_service.validate_phone_number(phone_number)
        
        if not validation_result['valid']:
            self.stdout.write(self.style.ERROR(f'❌ Invalid phone number: {validation_result.get("error")}'))
            return
        
        formatted_number = validation_result['formatted_number']
        self.stdout.write(self.style.SUCCESS(f'✅ Phone number valid: {formatted_number}'))
        
        if not mtn_service.is_configured():
            self.stdout.write(self.style.WARNING('⚠️  MTN MoMo not configured, running in demo mode'))
            self.stdout.write(self.style.SUCCESS('✅ Demo payment flow would work'))
            return
        
        # Create test payment
        try:
            provider = PaymentProvider.objects.get(code='mtn_momo')
        except PaymentProvider.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ MTN MoMo provider not found. Run: python manage.py setup_payment_providers'))
            return
        
        # Create test payment record
        payment = Payment.objects.create(
            reference=f'TEST_MTN_{phone_number}_{int(amount * 100)}',
            amount=amount,
            currency='GHS',
            payment_method='momo',
            provider=provider,
            phone_number=f'+{formatted_number}',
            description=f'Test payment for {amount} GHS'
        )
        
        self.stdout.write(f'Created test payment: {payment.reference}')
        
        # Test payment initiation
        self.stdout.write('Initiating payment...')
        result = mtn_service.initiate_payment(payment)
        
        if result['success']:
            self.stdout.write(self.style.SUCCESS('✅ Payment initiated successfully'))
            self.stdout.write(f'   Transaction ID: {result.get("external_reference")}')
            self.stdout.write(f'   Message: {result.get("message")}')
            
            # Update payment with external reference
            payment.external_reference = result.get('external_reference')
            payment.status = 'processing'
            payment.save()
            
            # Test status check
            self.stdout.write('\nChecking payment status...')
            status_result = mtn_service.check_payment_status(payment.external_reference)
            
            if status_result['success']:
                self.stdout.write(self.style.SUCCESS('✅ Status check successful'))
                self.stdout.write(f'   Status: {status_result.get("status")}')
                self.stdout.write(f'   MTN Status: {status_result.get("mtn_status")}')
            else:
                self.stdout.write(self.style.ERROR(f'❌ Status check failed: {status_result.get("error")}'))
        else:
            self.stdout.write(self.style.ERROR(f'❌ Payment initiation failed: {result.get("error")}'))
        
        # Clean up test payment
        payment.delete()
        self.stdout.write(f'\nCleaned up test payment: {payment.reference}')
        
        self.stdout.write(self.style.SUCCESS('\n🎉 MTN MoMo test completed!'))