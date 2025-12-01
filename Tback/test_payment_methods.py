#!/usr/bin/env python
"""
Test payment methods API
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.test import Client
from payments.models import PaymentProvider

def test_payment_methods():
    print("🔍 Testing Payment Methods API")
    
    # Check providers in database
    print("\n📊 Providers in Database:")
    for provider in PaymentProvider.objects.all():
        status = "✅ ACTIVE" if provider.is_active else "❌ INACTIVE"
        print(f"  {provider.name} ({provider.code}) - {status}")
    
    # Test API endpoint
    print("\n🌐 Testing API Endpoint:")
    client = Client()
    response = client.get('/api/payments/checkout/methods/')
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n💳 Available Payment Methods:")
        
        for method in data['payment_methods']:
            print(f"\n{method['icon']} {method['name']}")
            print(f"   Description: {method['description']}")
            print(f"   Processing: {method['processing_time']}")
            print(f"   Currencies: {', '.join(method['currencies'])}")
            print(f"   Providers ({len(method['providers'])}):")
            
            for provider in method['providers']:
                print(f"     - {provider['name']} ({provider['code']})")
        
        print(f"\n🌍 Supported Currencies: {', '.join(data['supported_currencies'])}")
        print(f"💰 Default Currency: {data['default_currency']}")
        
    else:
        print(f"❌ Error: {response.content.decode()}")

if __name__ == '__main__':
    test_payment_methods()