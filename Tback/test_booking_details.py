#!/usr/bin/env python
"""
Test script to create a payment and verify booking details are stored
"""
import requests
import json

def test_payment_with_booking_details():
    """Test creating a payment with booking details"""
    
    print("🧪 Testing Payment with Booking Details")
    print("=" * 50)
    
    # Test data
    payment_data = {
        "amount": "150.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Test payment with booking details",
        "booking_details": {
            "user_name": "Jane Smith",
            "user_email": "jane.smith@example.com",
            "user_phone": "+233244123456",
            "destination_name": "Kakum National Park Adventure",
            "destination_location": "Central Region, Ghana",
            "duration": "2 Days / 1 Night",
            "base_price": 800.00,
            "adults": 2,
            "children": 0,
            "selected_date": "2025-10-15",
            "accommodation": {
                "name": "Eco Lodge",
                "price": 300.00,
                "is_default": False
            },
            "transport": {
                "name": "4WD Vehicle",
                "price": 400.00,
                "is_default": False
            },
            "meals": {
                "name": "All Meals Included",
                "price": 200.00,
                "is_default": False
            },
            "medical": {
                "name": "Basic Insurance",
                "price": 50.00,
                "is_default": True
            },
            "experiences": [
                {
                    "name": "Canopy Walk",
                    "price": 100.00
                },
                {
                    "name": "Wildlife Safari",
                    "price": 200.00
                }
            ],
            "base_total": 1600.00,  # 800 * 2 people
            "options_total": 1250.00,  # 300*2 + 400 + 200 + 50 + 100 + 200
            "final_total": 2850.00
        }
    }
    
    try:
        print("1. Creating payment with booking details...")
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/', 
            json=payment_data
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"   ✅ Payment created: {payment_ref}")
            print(f"   💰 Amount: {result['payment']['currency']} {result['payment']['amount']}")
            
            # Check if booking details were stored
            print("\n2. Checking if booking details were stored...")
            
            # We'll need to check via Django shell since the API doesn't expose metadata
            print(f"   📋 Payment reference: {payment_ref}")
            print("   🔍 Check booking details in Django admin or run:")
            print(f"      python manage.py shell -c \"from payments.models import Payment; p = Payment.objects.get(reference='{payment_ref}'); print('Has booking details:', 'booking_details' in p.metadata)\"")
            
            return payment_ref
            
        else:
            print(f"   ❌ Failed to create payment: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    payment_ref = test_payment_with_booking_details()
    
    if payment_ref:
        print(f"\n🎯 Next Steps:")
        print(f"1. Check Django admin: http://localhost:8000/admin/payments/payment/")
        print(f"2. Look for payment: {payment_ref}")
        print(f"3. Expand 'Booking Details' section to see formatted details")
        print(f"4. The booking details should show customer info, destination, options, and pricing")