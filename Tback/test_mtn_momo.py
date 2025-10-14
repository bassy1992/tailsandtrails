#!/usr/bin/env python
"""
Test script to create and verify MTN MoMo payments for Ghana
"""
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from authentication.models import User
from payments.models import Payment, PaymentProvider
from rest_framework.authtoken.models import Token

def test_mtn_momo_payment():
    print("=== Testing MTN Mobile Money Payment (Ghana) ===")
    
    # Get user and token
    user = User.objects.first()
    token, created = Token.objects.get_or_create(user=user)
    
    print(f"User: {user.email}")
    print(f"Token: {token.key}")
    
    # Get MTN MoMo provider
    try:
        provider = PaymentProvider.objects.get(code='mtn_momo')
        print(f"Provider: {provider.name} (Active: {provider.is_active})")
    except PaymentProvider.DoesNotExist:
        print("ERROR: MTN MoMo provider not found!")
        return
    
    # Test data for Ghana
    payment_data = {
        'amount': 50.00,  # 50 GHS
        'currency': 'GHS',
        'payment_method': 'momo',
        'provider': provider.id,
        'phone_number': '+233244123456',  # Ghana MTN number format
        'description': 'Test MTN MoMo payment for Ghana travel booking'
    }
    
    print(f"Payment data: {json.dumps(payment_data, indent=2)}")
    
    # Create payment directly
    print("\n=== Creating MTN MoMo Payment ===")
    
    payment = Payment.objects.create(
        user=user,
        amount=payment_data['amount'],
        currency=payment_data['currency'],
        payment_method=payment_data['payment_method'],
        provider=provider,
        phone_number=payment_data['phone_number'],
        description=payment_data['description']
    )
    
    print(f"Payment created: {payment.reference}")
    print(f"Status: {payment.status}")
    print(f"Amount: {payment.currency} {payment.amount}")
    print(f"Phone: {payment.phone_number}")
    print(f"Provider: {payment.provider.name}")
    
    # Verify in database
    print("\n=== Verifying MTN MoMo Payments in Database ===")
    mtn_payments = Payment.objects.filter(provider__code='mtn_momo')
    print(f"Total MTN MoMo payments in DB: {mtn_payments.count()}")
    
    for p in mtn_payments:
        print(f"- {p.reference}: {p.currency} {p.amount} ({p.status})")
        print(f"  Provider: {p.provider.name}")
        print(f"  User: {p.user.email}")
        print(f"  Phone: {p.phone_number}")
        print(f"  Created: {p.created_at}")
        print()
    
    # Show all providers
    print("=== Available Payment Providers ===")
    for provider in PaymentProvider.objects.all():
        print(f"- {provider.name} ({provider.code}) - Active: {provider.is_active}")

if __name__ == '__main__':
    test_mtn_momo_payment()