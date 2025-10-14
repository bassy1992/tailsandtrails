#!/usr/bin/env python
"""
Simple test for booking details storage
"""
import requests
import json

def test_simple_booking_details():
    """Test basic booking details storage"""
    print("🧪 Testing Booking Details Storage")
    print("=" * 50)
    
    # Simple booking details
    booking_details = {
        'type': 'destination',
        'destination': {
            'name': 'Test Tour',
            'price': 100.0
        },
        'travelers': {
            'adults': 1
        }
    }
    
    # Simple MoMo payment
    momo_data = {
        'amount': 100.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0240381084',
        'description': 'Test booking details storage',
        'booking_details': booking_details
    }
    
    print("📋 Request Data:")
    print(json.dumps(momo_data, indent=2))
    print()
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=momo_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result.get('payment', {}).get('reference', '')
            
            print("✅ Payment Created")
            print(f"📋 Reference: {payment_ref}")
            print()
            
            # Check the payment details
            print("🔍 Checking Payment Details...")
            verify_response = requests.get(f'http://localhost:8000/api/payments/paystack/verify/{payment_ref}/')
            
            if verify_response.status_code == 200:
                verify_result = verify_response.json()
                payment = verify_result.get('payment', {})
                metadata = payment.get('metadata', {})
                
                print("📊 Payment Metadata:")
                print(json.dumps(metadata, indent=2))
                
                if 'booking_details' in metadata:
                    print("✅ Booking details found in metadata!")
                    return True
                else:
                    print("❌ No booking details in metadata")
                    return False
            else:
                print(f"❌ Failed to verify payment: {verify_response.status_code}")
                return False
        else:
            print(f"❌ Payment creation failed")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test"""
    print("🧪 Booking Details Storage Test")
    print("=" * 60)
    
    # Check server
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running")
        return
    
    print()
    
    success = test_simple_booking_details()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Booking details storage is working!")
    else:
        print("❌ Booking details storage failed")
        print("Check the Django logs for errors")

if __name__ == '__main__':
    main()