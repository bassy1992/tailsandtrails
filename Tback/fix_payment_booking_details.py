#!/usr/bin/env python
"""
Fix booking details for a specific payment
This script will update the payment metadata with correct booking details
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment
import json

def fix_payment(reference):
    """Fix booking details for a specific payment"""
    
    print("=" * 80)
    print(f"FIXING PAYMENT: {reference}")
    print("=" * 80)
    
    try:
        payment = Payment.objects.get(reference=reference)
    except Payment.DoesNotExist:
        print(f"\n❌ Payment not found: {reference}")
        return
    
    print(f"\n📋 Current Payment Details:")
    print(f"Reference: {payment.reference}")
    print(f"Amount: {payment.currency} {payment.amount}")
    print(f"User: {payment.user.email if payment.user else 'Anonymous'}")
    
    if payment.metadata and 'booking_details' in payment.metadata:
        print(f"\n📦 Current Booking Details:")
        print(json.dumps(payment.metadata['booking_details'], indent=2))
        
        # Fix the booking details
        bd = payment.metadata['booking_details']
        
        # Fix travelers if they're 0
        if 'travelers' in bd:
            if bd['travelers'].get('adults', 0) == 0:
                print(f"\n🔧 Fixing travelers: Setting adults to 1")
                bd['travelers']['adults'] = 1
        
        # Fix pricing if base_total is 0
        if 'pricing' in bd:
            if bd['pricing'].get('base_total', 0) == 0:
                print(f"\n🔧 Fixing pricing: Setting base_total to {float(payment.amount)}")
                bd['pricing']['base_total'] = float(payment.amount)
                bd['pricing']['final_total'] = float(payment.amount)
        
        # Fix selected_date if empty
        if not bd.get('selected_date'):
            print(f"\n🔧 Fixing date: Setting to payment creation date")
            bd['selected_date'] = payment.created_at.date().isoformat()
        
        # Save the updated metadata
        payment.metadata['booking_details'] = bd
        payment.save()
        
        print(f"\n✅ Updated Booking Details:")
        print(json.dumps(payment.metadata['booking_details'], indent=2))
        print(f"\n✅ Payment {reference} fixed successfully!")
        
    else:
        print(f"\n❌ No booking_details found in payment metadata")
        print(f"Creating new booking details...")
        
        # Create booking details from scratch
        booking_details = {
            'user_info': {
                'name': f"{payment.user.first_name} {payment.user.last_name}".strip() if payment.user else "Guest",
                'email': payment.user.email if payment.user else "",
                'phone': payment.phone_number or ""
            },
            'destination': {
                'name': 'Tent Xcape',  # Default, update as needed
                'location': 'Ghana',
                'duration': '3 Days / 2 Nights',
                'base_price': float(payment.amount)
            },
            'travelers': {
                'adults': 1,
                'children': 0
            },
            'selected_date': payment.created_at.date().isoformat(),
            'selected_options': {},
            'pricing': {
                'base_total': float(payment.amount),
                'options_total': 0.00,
                'final_total': float(payment.amount)
            }
        }
        
        if not payment.metadata:
            payment.metadata = {}
        
        payment.metadata['booking_details'] = booking_details
        payment.save()
        
        print(f"\n✅ Created Booking Details:")
        print(json.dumps(payment.metadata['booking_details'], indent=2))
        print(f"\n✅ Payment {reference} fixed successfully!")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        reference = sys.argv[1]
    else:
        # Default to the payment mentioned
        reference = 'PAY-20251202102507-BXKFAM'
    
    fix_payment(reference)
