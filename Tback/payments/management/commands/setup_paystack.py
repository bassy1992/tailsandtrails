from django.core.management.base import BaseCommand
from payments.models import PaymentProvider

class Command(BaseCommand):
    help = 'Set up Paystack payment provider'

    def handle(self, *args, **options):
        # Create or update Paystack provider
        provider, created = PaymentProvider.objects.get_or_create(
            code='paystack',
            defaults={
                'name': 'Paystack',
                'configuration': {
                    'supported_currencies': ['NGN', 'USD', 'GHS'],
                    'supported_channels': ['card', 'bank', 'ussd', 'qr', 'mobile_money'],
                    'webhook_events': ['charge.success', 'charge.failed']
                },
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created Paystack provider')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Paystack provider already exists')
            )