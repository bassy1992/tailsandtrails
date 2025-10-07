#!/usr/bin/env python
"""
Test automatic booking details storage during payment creation
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

def test_auto_booking_storage():
    """Test if booking details are automatically stored"""
    
    print("🧪 Testing Automatic Booking Details Storage")
    print("=" * 50)
    
    # Test 1: Payment without booking_details in request
    print("1. Creating payment without explicit booking_details...")
    payment_data = {
        "amount": "85.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Test auto booking storage"
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/', 
            json=payment_data
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"   ✅ Payment created: {payment_ref}")
            
            # Check if booking details were stored
            payment = Payment.objects.get(reference=payment_ref)
            has_booking_details = 'booking_details' in payment.metadata
            
            print(f"   📋 Has booking details: {has_booking_details}")
            
            if has_booking_details:
                booking_details = payment.metadata['booking_details']
                destination_name = booking_details.get('destination', {}).get('name', 'Unknown')
                user_name = booking_details.get('user_info', {}).get('name', 'Unknown')
                print(f"   🏖️ Destination: {destination_name}")
                print(f"   👤 User: {user_name}")
                print("   ✅ Automatic booking details storage WORKS!")
                return True
            else:
                print("   ❌ No booking details found - automatic storage FAILED!")
                return False
        else:
            print(f"   ❌ Failed to create payment: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_with_explicit_booking_details():
    """Test with explicit booking details in request"""
    
    print("\n2. Creating payment with explicit booking_details...")
    payment_data = {
        "amount": "120.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Test explicit booking details",
        "booking_details": {
            "user_name": "Alice Johnson",
            "user_email": "alice@example.com",
            "destination_name": "Mole National Park Safari",
            "destination_location": "Northern Ghana",
            "duration": "4 Days / 3 Nights",
            "adults": 2,
            "children": 1,
            "final_total": 120.00
        }
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/', 
            json=payment_data
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"   ✅ Payment created: {payment_ref}")
            
            # Check if booking details were stored
            payment = Payment.objects.get(reference=payment_ref)
            has_booking_details = 'booking_details' in payment.metadata
            
            print(f"   📋 Has booking details: {has_booking_details}")
            
            if has_booking_details:
                booking_details = payment.metadata['booking_details']
                destination_name = booking_details.get('destination', {}).get('name', 'Unknown')
                user_name = booking_details.get('user_info', {}).get('name', 'Unknown')
                print(f"   🏖️ Destination: {destination_name}")
                print(f"   👤 User: {user_name}")
                print("   ✅ Explicit booking details storage WORKS!")
                return True
            else:
                print("   ❌ No booking details found - explicit storage FAILED!")
                return False
        else:
            print(f"   ❌ Failed to create payment: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing Booking Details Auto-Storage")
    print("Make sure Django server is running on localhost:8000")
    print()
    
    test1_success = test_auto_booking_storage()
    test2_success = test_with_explicit_booking_details()
    
    print("\n" + "=" * 50)
    if test1_success and test2_success:
        print("🎉 All tests passed! Booking details auto-storage is working!")
    else:
        print("❌ Some tests failed. Check the output above for details.")
        print("\nTo fix missing booking details manually:")
        print("python manage.py ensure_booking_details")