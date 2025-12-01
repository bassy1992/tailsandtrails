#!/usr/bin/env python
"""
Test MTN MoMo API endpoints
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

def test_mtn_momo_api():
    print("=== Testing MTN MoMo API Endpoints ===")
    
    # Setup
    client = Client()
    user = User.objects.first()
    token, created = Token.objects.get_or_create(user=user)
    
    # Get MTN MoMo provider
    provider = PaymentProvider.objects.get(code='mtn_momo')
    
    print(f"User: {user.email}")
    print(f"Provider: {provider.name}")
    
    # Test payment creation via API
    payment_data = {
        'amount': 75.50,
        'currency': 'GHS',
        'payment_method': 'momo',
        'provider': provider.id,
        'phone_number': '+233244987654',
        'description': 'API test payment for MTN MoMo Ghana'
    }
    
    print(f"\nPayment data: {json.dumps(payment_data, indent=2)}")
    
    # Make API request
    response = client.post(
        '/api/payments/create/',
        data=json.dumps(payment_data),
        content_type='application/json',
        HTTP_AUTHORIZATION=f'Token {token.key}'
    )
    
    print(f"\nAPI Response Status: {response.status_code}")
    
    if response.status_code == 201:
        response_data = response.json()
        print("Payment created successfully!")
        print(f"Response: {json.dumps(response_data, indent=2)}")
    else:
        print(f"Error: {response.content.decode()}")
    
    # Test payment list API
    print("\n=== Testing Payment List API ===")
    response = client.get(
        '/api/payments/list/',
        HTTP_AUTHORIZATION=f'Token {token.key}'
    )
    
    print(f"List API Status: {response.status_code}")
    if response.status_code == 200:
        payments = response.json()
        print(f"Found {len(payments)} payments")
        for payment in payments:
            print(f"- {payment.get('reference')}: {payment.get('currency')} {payment.get('amount')}")

if __name__ == '__main__':
    test_mtn_momo_api()