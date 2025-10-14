#!/usr/bin/env python
"""
Setup script for Paystack integration
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
    print("🔧 Setting up Paystack provider...")
    
    provider, created = PaymentProvider.objects.get_or_create(
        code='paystack',
        defaults={
            'name': 'Paystack Ghana',
            'is_active': True,
            'configuration': {
                'supports_mobile_money': True,
                'supports_cards': True,
                'currency': 'GHS',
                'mobile_money_providers': [
                    {'code': 'mtn', 'name': 'MTN Mobile Money'},
                    {'code': 'vodafone', 'name': 'Vodafone Cash'},
                    {'code': 'airteltigo', 'name': 'AirtelTigo Money'}
                ],
                'test_cards': [
                    {'number': '4084084084084081', 'type': 'Success'},
                    {'number': '4084084084084099', 'type': 'Decline'},
                    {'number': '4084084084084107', 'type': 'Insufficient Funds'}
                ]
            }
        }
    )
    
    if created:
        print("✅ Paystack provider created successfully")
    else:
        print("✅ Paystack provider already exists")
        # Update configuration
        provider.configuration.update({
            'supports_mobile_money': True,
            'supports_cards': True,
            'currency': 'GHS',
            'mobile_money_providers': [
                {'code': 'mtn', 'name': 'MTN Mobile Money'},
                {'code': 'vodafone', 'name': 'Vodafone Cash'},
                {'code': 'airteltigo', 'name': 'AirtelTigo Money'}
            ],
            'test_cards': [
                {'number': '4084084084084081', 'type': 'Success'},
                {'number': '4084084084084099', 'type': 'Decline'},
                {'number': '4084084084084107', 'type': 'Insufficient Funds'}
            ]
        })
        provider.save()
        print("✅ Paystack provider configuration updated")
    
    return provider

def check_environment():
    """Check environment configuration"""
    print("\n🔍 Checking environment configuration...")
    
    from django.conf import settings
    
    # Check Paystack keys
    public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
    secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
    
    if public_key and public_key != 'pk_test_your_paystack_public_key_here':
        print(f"✅ Paystack public key configured: {public_key[:20]}...")
    else:
        print("❌ Paystack public key not configured")
        return False
    
    if secret_key and secret_key != 'sk_test_your_paystack_secret_key_here':
        print(f"✅ Paystack secret key configured: {secret_key[:20]}...")
    else:
        print("❌ Paystack secret key not configured")
        return False
    
    # Check webhook URL
    webhook_url = getattr(settings, 'PAYSTACK_WEBHOOK_URL', '')
    if webhook_url:
        print(f"✅ Webhook URL configured: {webhook_url}")
    else:
        print("⚠️  Webhook URL not configured")
    
    return True

def main():
    """Main setup function"""
    print("🚀 Paystack Integration Setup")
    print("=" * 40)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment configuration incomplete")
        return False
    
    # Setup provider
    provider = setup_paystack_provider()
    
    print(f"\n📋 Setup Summary:")
    print(f"   Provider: {provider.name}")
    print(f"   Code: {provider.code}")
    print(f"   Active: {provider.is_active}")
    print(f"   Supports Cards: {provider.configuration.get('supports_cards', False)}")
    print(f"   Supports Mobile Money: {provider.configuration.get('supports_mobile_money', False)}")
    
    print(f"\n🎉 Paystack integration setup complete!")
    print(f"\n📝 Next Steps:")
    print(f"1. Start Django server: python manage.py runserver")
    print(f"2. Open test page: http://localhost:8000/paystack_test_frontend.html")
    print(f"3. Test card payments with: 4084084084084081")
    print(f"4. Test mobile money with any Ghana number")
    
    return True

if __name__ == '__main__':
    main()