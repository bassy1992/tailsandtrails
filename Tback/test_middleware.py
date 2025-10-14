#!/usr/bin/env python
"""
Test the booking details middleware
"""
import requests
import json
import os
import sys
import django
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment

def test_middleware():
    """Test if the middleware adds booking details"""
    
    print("🧪 Testing Booking Details Middleware")
    print("=" * 40)
    
    # Create a payment with a specific description
    payment_data = {
        "amount": "95.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Kakum National Park Canopy Walk Adventure"
    }
    
    try:
        print("1. Creating payment via API...")
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/', 
            json=payment_data
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"   ✅ Payment created: {payment_ref}")
            
            # Wait a moment for middleware to process
            time.sleep(1)
            
            # Check if booking details were added
            payment = Payment.objects.get(reference=payment_ref)
            has_booking_details = 'booking_details' in payment.metadata
            
            print(f"   📋 Has booking details: {has_booking_details}")
            
            if has_booking_details:
                booking_details = payment.metadata['booking_details']
                destination_name = booking_details.get('destination', {}).get('name', 'Unknown')
                user_name = booking_details.get('user_info', {}).get('name', 'Unknown')
                print(f"   🏖️ Destination: {destination_name}")
                print(f"   👤 User: {user_name}")
                print("   ✅ Middleware is working!")
                return True
            else:
                print("   ❌ No booking details found - middleware failed!")
                print(f"   Metadata: {payment.metadata}")
                return False
        else:
            print(f"   ❌ Failed to create payment: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Booking Details Middleware")
    print("Make sure Django server is running with the new middleware")
    print()
    
    success = test_middleware()
    
    if success:
        print("\n🎉 Middleware test passed!")
        print("All future payments will automatically have booking details.")
    else:
        print("\n❌ Middleware test failed.")
        print("You may need to restart the Django server to load the middleware.")
        print("\nTo fix existing payments without booking details:")
        print("python manage.py ensure_booking_details")