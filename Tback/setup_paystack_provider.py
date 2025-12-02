"""
Script to create or update Paystack payment provider in the database
Run this after deploying to Railway to ensure Paystack is available
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import PaymentProvider

def setup_paystack_provider():
    """Create or update Paystack payment provider"""
    
    provider, created = PaymentProvider.objects.update_or_create(
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
    
    if created:
        print(f"✅ Created Paystack payment provider")
    else:
        print(f"✅ Updated Paystack payment provider")
    
    print(f"   Provider ID: {provider.id}")
    print(f"   Provider Code: {provider.code}")
    print(f"   Provider Name: {provider.name}")
    print(f"   Is Active: {provider.is_active}")
    
    # Check if API keys are configured
    paystack_secret = os.getenv('PAYSTACK_SECRET_KEY')
    paystack_public = os.getenv('PAYSTACK_PUBLIC_KEY')
    
    if paystack_secret and paystack_public:
        print(f"\n✅ Paystack API keys are configured")
        print(f"   Secret Key: {paystack_secret[:7]}...{paystack_secret[-4:]}")
        print(f"   Public Key: {paystack_public[:7]}...{paystack_public[-4:]}")
    else:
        print(f"\n⚠️  WARNING: Paystack API keys not found in environment variables")
        print(f"   Please set PAYSTACK_SECRET_KEY and PAYSTACK_PUBLIC_KEY on Railway")
    
    # Deactivate other providers (optional)
    other_providers = PaymentProvider.objects.exclude(code='paystack')
    if other_providers.exists():
        print(f"\n📋 Other payment providers found:")
        for p in other_providers:
            print(f"   - {p.name} ({p.code}): {'Active' if p.is_active else 'Inactive'}")
        
        # Optionally deactivate them
        # other_providers.update(is_active=False)
        # print(f"\n✅ Deactivated {other_providers.count()} other providers")
    
    print(f"\n🎉 Paystack setup complete!")
    print(f"\nNext steps:")
    print(f"1. Verify API keys are set on Railway")
    print(f"2. Test payment flow on your deployed site")
    print(f"3. Configure webhook URL in Paystack dashboard (production only)")

if __name__ == '__main__':
    setup_paystack_provider()
