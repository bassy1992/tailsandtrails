#!/usr/bin/env python
"""
Check a specific payment by reference to see what booking details were stored
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

def check_payment(reference):
    """Check a specific payment"""
    
    print("=" * 80)
    print(f"CHECKING PAYMENT: {reference}")
    print("=" * 80)
    
    try:
        payment = Payment.objects.get(reference=reference)
    except Payment.DoesNotExist:
        print(f"\n❌ Payment not found: {reference}")
        return
    
    print(f"\n📋 Payment Details:")
    print(f"Reference: {payment.reference}")
    print(f"Amount: {payment.currency} {payment.amount}")
    print(f"Status: {payment.status}")
    print(f"User: {payment.user.email if payment.user else 'Anonymous'}")
    print(f"Phone: {payment.phone_number}")
    print(f"Description: {payment.description}")
    print(f"Created: {payment.created_at}")
    
    print(f"\n📦 Full Metadata:")
    if payment.metadata:
        print(json.dumps(payment.metadata, indent=2))
    else:
        print("No metadata")
    
    if payment.metadata and 'booking_details' in payment.metadata:
        print(f"\n✅ Booking Details Found:")
        bd = payment.metadata['booking_details']
        
        # Check each field
        print(f"\n🔍 Field Analysis:")
        
        if 'user_info' in bd:
            ui = bd['user_info']
            print(f"✓ User Name: {ui.get('name', 'MISSING')}")
            print(f"✓ User Email: {ui.get('email', 'MISSING')}")
            print(f"✓ User Phone: {ui.get('phone', 'MISSING')}")
        else:
            print("✗ user_info: MISSING")
        
        if 'destination' in bd:
            dest = bd['destination']
            print(f"✓ Destination Name: {dest.get('name', 'MISSING')}")
            print(f"✓ Location: {dest.get('location', 'MISSING')}")
            print(f"✓ Duration: {dest.get('duration', 'MISSING')}")
            print(f"✓ Base Price: {dest.get('base_price', 'MISSING')}")
        else:
            print("✗ destination: MISSING")
        
        if 'travelers' in bd:
            trav = bd['travelers']
            print(f"✓ Adults: {trav.get('adults', 'MISSING')}")
            print(f"✓ Children: {trav.get('children', 'MISSING')}")
        else:
            print("✗ travelers: MISSING")
        
        if 'selected_date' in bd:
            print(f"✓ Selected Date: {bd.get('selected_date', 'MISSING')}")
        else:
            print("✗ selected_date: MISSING")
        
        if 'pricing' in bd:
            pricing = bd['pricing']
            print(f"✓ Base Total: {pricing.get('base_total', 'MISSING')}")
            print(f"✓ Options Total: {pricing.get('options_total', 'MISSING')}")
            print(f"✓ Final Total: {pricing.get('final_total', 'MISSING')}")
        else:
            print("✗ pricing: MISSING")
        
    else:
        print(f"\n❌ No booking_details in metadata")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        reference = sys.argv[1]
    else:
        reference = 'PAY-20251202102507-BXKFAM'  # Default to the one mentioned
    
    check_payment(reference)
