#!/usr/bin/env python
"""
Debug booking storage issue
"""
import requests
import json
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment

def debug_booking_storage():
    """Debug why booking storage isn't working"""
    
    print("🔍 Debugging Booking Storage Issue")
    print("=" * 40)
    
    # Create a simple payment
    payment_data = {
        "amount": "55.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Debug booking storage"
    }
    
    try:
        print("1. Creating payment...")
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/', 
            json=payment_data
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"   Payment: {payment_ref}")
            
            # Check immediately
            payment = Payment.objects.get(reference=payment_ref)
            print(f"   Metadata empty: {not payment.metadata}")
            print(f"   Metadata: {payment.metadata}")
            
            if not payment.metadata or 'booking_details' not in payment.metadata:
                print("   ❌ Booking details not stored automatically")
                
                # Try to add manually
                print("2. Adding booking details manually...")
                from payments.booking_utils import store_booking_details_in_payment, create_sample_booking_details
                
                sample_data = create_sample_booking_details()
                sample_data['final_total'] = float(payment.amount)
                store_booking_details_in_payment(payment, sample_data)
                
                payment.refresh_from_db()
                print(f"   Manual storage successful: {'booking_details' in payment.metadata}")
            else:
                print("   ✅ Booking details stored automatically!")
                
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"   Exception: {str(e)}")

if __name__ == "__main__":
    debug_booking_storage()