from django.core.management.base import BaseCommand
from payments.models import PaymentProvider

class Command(BaseCommand):
    help = 'Setup default payment providers'
    
    def handle(self, *args, **options):
        providers = [
            {
                'name': 'MTN Mobile Money',
                'code': 'mtn_momo',
                'configuration': {
                    'collection_user_id': '',
                    'collection_api_key': '',
                    'subscription_key': '',
                    'base_url': 'https://sandbox.momodeveloper.mtn.com',
                    'callback_url': 'http://localhost:8000/api/payments/mtn-momo/webhook/',
                    'environment': 'sandbox'  # sandbox or production
                },
                'is_active': True
            },
            {
                'name': 'Vodafone Cash',
                'code': 'vodafone_cash',
                'configuration': {
                    'merchant_id': '',
                    'api_key': '',
                    'base_url': 'https://api.vodafone.com.gh',
                    'callback_url': ''
                },
                'is_active': False
            },
            {
                'name': 'AirtelTigo Money',
                'code': 'airteltigo_money',
                'configuration': {
                    'merchant_id': '',
                    'api_key': '',
                    'base_url': 'https://api.airteltigo.com.gh',
                    'callback_url': ''
                },
                'is_active': False
            },
            {
                'name': 'M-Pesa (Kenya)',
                'code': 'mpesa_kenya',
                'configuration': {
                    'consumer_key': '',
                    'consumer_secret': '',
                    'business_short_code': '',
                    'passkey': '',
                    'token_url': 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
                    'stk_push_url': 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
                },
                'is_active': False
            },
            {
                'name': 'Stripe',
                'code': 'stripe',
                'configuration': {
                    'publishable_key': '',
                    'secret_key': '',
                    'webhook_secret': ''
                },
                'is_active': False
            }
        ]
        
        for provider_data in providers:
            provider, created = PaymentProvider.objects.get_or_create(
                code=provider_data['code'],
                defaults=provider_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created payment provider: {provider.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Payment provider already exists: {provider.name}')
                )