#!/usr/bin/env python
"""
Test checkout payment methods and creation
"""
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from payments.models import PaymentProvider

User = get_user_model()

def test_checkout_endpoints():
    print("🛒 === Testing Checkout Endpoints ===")
    
    # Setup
    client = Client()
    user = User.objects.first()
    token, created = Token.objects.get_or_create(user=user)
    
    print(f"User: {user.email}")
    print(f"Token: {token.key}")
    
    # Test payment methods endpoint
    print("\n📱 Testing Payment Methods Endpoint")
    response = client.get('/api/payments/checkout/methods/')
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Available Payment Methods:")
        for method in data['payment_methods']:
            print(f"  {method['icon']} {method['name']}")
            print(f"    Description: {method['description']}")
            print(f"    Processing: {method['processing_time']}")
            print(f"    Providers: {len(method['providers'])}")
            for provider in method['providers']:
                print(f"      - {provider['name']} ({provider['code']})")
            print()
    
    # Test checkout payment creation - MTN MoMo
    print("\n📱 Testing MTN MoMo Checkout Payment")
    mtn_provider = PaymentProvider.objects.get(code='mtn_momo')
    
    momo_payment_data = {
        'amount': 25.50,
        'currency': 'GHS',
        'payment_method': 'momo',
        'provider_code': 'mtn_momo',
        'phone_number': '+233244123456',
        'description': 'Test checkout payment - MTN MoMo'
    }
    
    response = client.post(
        '/api/payments/checkout/create/',
        data=json.dumps(momo_payment_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {token.key}'
    )
    
    print(f"MTN MoMo Payment Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print("✅ MTN MoMo Payment Created Successfully!")
        print(f"Reference: {data['payment']['reference']}")
        print(f"Status: {data['payment']['status']}")
        print(f"Message: {data.get('message', 'N/A')}")
    else:
        print(f"❌ Error: {response.content.decode()}")
    
    # Test checkout payment creation - Stripe
    print("\n💳 Testing Stripe Checkout Payment")
    stripe_provider = PaymentProvider.objects.get(code='stripe')
    
    stripe_payment_data = {
        'amount': 50.00,
        'currency': 'USD',
        'payment_method': 'card',
        'provider_code': 'stripe',
        'description': 'Test checkout payment - Stripe'
    }
    
    response = client.post(
        '/api/payments/checkout/create/',
        data=json.dumps(stripe_payment_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {token.key}'
    )
    
    print(f"Stripe Payment Status: {response.status_code}")
    if response.status_code == 201:
        data = response.json()
        print("✅ Stripe Payment Created Successfully!")
        print(f"Reference: {data['payment']['reference']}")
        print(f"Status: {data['payment']['status']}")
        if 'stripe' in data:
            print(f"Client Secret: {data['stripe']['client_secret'][:20]}...")
            print(f"Publishable Key: {data['stripe']['publishable_key'][:20]}...")
    else:
        print(f"❌ Error: {response.content.decode()}")

if __name__ == '__main__':
    test_checkout_endpoints()