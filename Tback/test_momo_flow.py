#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def test_momo_payment_flow():
    """Test the complete mobile money payment flow"""
    base_url = 'http://localhost:8000/api/payments'
    
    print("🧪 Testing Mobile Money Payment Flow")
    print("=" * 50)
    
    # Step 1: Create payment
    print("\n1️⃣ Creating payment...")
    create_data = {
        'amount': 150.00,
        'currency': 'GHS',
        'payment_method': 'momo',
        'provider_code': 'mtn_momo',
        'phone_number': '+233240000000',  # Added country code
        'description': 'Test mobile money payment'
    }
    
    try:
        response = requests.post(f'{base_url}/checkout/create/', 
                               json=create_data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 201:
            result = response.json()
            if result.get('success'):
                payment_ref = result['payment']['reference']
                print(f"✅ Payment created successfully!")
                print(f"   Reference: {payment_ref}")
                print(f"   Status: {result['payment']['status']}")
                
                # Step 2: Check payment status
                print(f"\n2️⃣ Checking payment status...")
                status_response = requests.get(f'{base_url}/{payment_ref}/status/')
                
                if status_response.status_code == 200:
                    payment_status = status_response.json()
                    print(f"✅ Status check successful!")
                    print(f"   Status: {payment_status['status']}")
                    print(f"   Amount: GH₵{payment_status['amount']}")
                    
                    # Step 3: Complete payment
                    print(f"\n3️⃣ Completing payment...")
                    complete_response = requests.post(f'{base_url}/{payment_ref}/complete/')
                    
                    if complete_response.status_code == 200:
                        complete_result = complete_response.json()
                        if complete_result.get('success'):
                            print(f"✅ Payment completed successfully!")
                            print(f"   Status: {complete_result['payment']['status']}")
                            print(f"   Processed at: {complete_result['payment']['processed_at']}")
                            
                            print(f"\n🎉 Mobile Money payment flow test PASSED!")
                            return True
                        else:
                            print(f"❌ Payment completion failed: {complete_result.get('message')}")
                    else:
                        print(f"❌ Payment completion request failed: {complete_response.status_code}")
                        print(f"   Response: {complete_response.text}")
                else:
                    print(f"❌ Status check failed: {status_response.status_code}")
                    print(f"   Response: {status_response.text}")
            else:
                print(f"❌ Payment creation failed: {result.get('error')}")
        else:
            print(f"❌ Payment creation request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    return False

if __name__ == "__main__":
    success = test_momo_payment_flow()
    if success:
        print(f"\n✅ All tests passed! The mobile money payment flow is working correctly.")
    else:
        print(f"\n❌ Tests failed. Please check the server and try again.")