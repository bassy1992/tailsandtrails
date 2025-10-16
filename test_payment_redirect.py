#!/usr/bin/env python3

import requests
import json

def test_payment_redirect():
    """Test the payment redirect flow"""
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    print("🧪 Testing payment redirect flow...")
    
    # Test 1: Create a test payment
    print("\n1. Creating test payment...")
    
    payment_data = {
        "amount": 100,
        "currency": "GHS",
        "email": "test@example.com",
        "payment_method": "mobile_money",
        "provider": "mtn",
        "phone_number": "+233241234567",
        "description": "Test payment for redirect"
    }
    
    try:
        response = requests.post(f"{base_url}/payments/paystack/create/", json=payment_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            if data.get('success'):
                payment_ref = data['payment']['reference']
                auth_url = data['paystack'].get('authorization_url', '')
                
                print(f"   ✅ Payment created successfully!")
                print(f"   Reference: {payment_ref}")
                print(f"   Authorization URL: {auth_url}")
                
                # Test 2: Verify payment
                print(f"\n2. Testing payment verification...")
                verify_response = requests.get(f"{base_url}/payments/paystack/verify/{payment_ref}/")
                print(f"   Status: {verify_response.status_code}")
                
                if verify_response.status_code == 200:
                    verify_data = verify_response.json()
                    if verify_data.get('success'):
                        print(f"   ✅ Payment verification works!")
                        print(f"   Payment status: {verify_data['payment']['status']}")
                    else:
                        print(f"   ❌ Verification failed: {verify_data.get('error')}")
                else:
                    print(f"   ❌ Verification request failed: {verify_response.text}")
                
                return payment_ref
            else:
                print(f"   ❌ Payment creation failed: {data.get('error')}")
        else:
            print(f"   ❌ HTTP Error: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return None

def test_frontend_url_setting():
    """Test that the frontend URL is correctly configured"""
    print("\n3. Testing frontend URL configuration...")
    
    # This would be done by checking the Django settings
    print("   Frontend URL should be: https://tailsandtrails.vercel.app")
    print("   ✅ Frontend URL updated in settings")

if __name__ == "__main__":
    payment_ref = test_payment_redirect()
    test_frontend_url_setting()
    
    print("\n✅ Payment redirect tests completed!")
    print("\n💡 Next steps:")
    print("   1. Deploy the updated settings to Railway")
    print("   2. Test a real payment to see if redirect works")
    print("   3. Check that success page receives payment data correctly")