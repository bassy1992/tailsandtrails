#!/usr/bin/env python
"""
Test if the signal is working
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment, PaymentProvider
from payments.utils import generate_payment_reference

def test_signal():
    """Test if the post_save signal adds booking details"""
    
    print("🧪 Testing Post-Save Signal")
    print("=" * 30)
    
    # Get a provider
    provider = PaymentProvider.objects.first()
    if not provider:
        print("❌ No payment provider found")
        return
    
    # Create a payment directly
    payment = Payment.objects.create(
        reference=generate_payment_reference(),
        amount=75.00,
        currency='GHS',
        payment_method='momo',
        provider=provider,
        phone_number='+233244123456',
        description='Signal test payment'
    )
    
    print(f"✅ Created payment: {payment.reference}")
    
    # Check if booking details were added by signal
    payment.refresh_from_db()
    has_booking_details = 'booking_details' in payment.metadata
    
    print(f"📋 Has booking details: {has_booking_details}")
    
    if has_booking_details:
        destination = payment.metadata['booking_details']['destination']['name']
        print(f"🏖️ Destination: {destination}")
        print("✅ Signal is working!")
    else:
        print("❌ Signal is not working")
        print(f"Metadata: {payment.metadata}")

if __name__ == "__main__":
    test_signal()