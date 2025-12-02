# Generated migration to create Paystack provider

from django.db import migrations


def create_paystack_provider(apps, schema_editor):
    """Create Paystack payment provider"""
    PaymentProvider = apps.get_model('payments', 'PaymentProvider')
    
    # Create or update Paystack provider
    PaymentProvider.objects.update_or_create(
        code='paystack',
        defaults={
            'name': 'Paystack',
            'is_active': True,
            'config': {
                'supports_cards': True,
                'supports_mobile_money': True,
                'supports_bank_transfer': True,
                'supports_ussd': True,
                'currencies': ['GHS', 'NGN', 'USD', 'ZAR', 'KES'],
                'description': 'Secure payment gateway supporting cards, mobile money, bank transfers, and USSD'
            }
        }
    )
    print("✅ Created Paystack payment provider")


def remove_paystack_provider(apps, schema_editor):
    """Remove Paystack payment provider"""
    PaymentProvider = apps.get_model('payments', 'PaymentProvider')
    PaymentProvider.objects.filter(code='paystack').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_payment_payment_method'),
    ]

    operations = [
        migrations.RunPython(create_paystack_provider, remove_paystack_provider),
    ]
