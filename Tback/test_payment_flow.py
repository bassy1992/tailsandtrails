#!/usr/bin/env python
"""
Test the complete payment flow to identify issues
"""
import os
import sys
import django
import requests
import json
import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def test_complete_payment_flow():
    """Test the complete payment flow"""
    
    print("🧪 Testing Complete Payment Flow")
    print("=" * 50)
    
    base_url = "http://localhost:8000/api/payments"
    
    # Step 1: Test payment methods endpoint
    print("1. Testing payment methods endpoint...")
    try:
        response = requests.get(f"{base_url}/checkout/methods/")
        if response.status_code == 200:
            methods = response.json()
            print(f"   ✅ Payment methods available: {len(methods)}")
            for method in methods:
                print(f"      - {method['name']} ({method['id']})")
        else:
            print(f"   ❌ Failed to get payment methods: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error getting payment methods: {e}")
        return False
    
    # Step 2: Create a payment
    print("\n2. Creating a test payment...")
    payment_data = {
        "amount": "25.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Test payment flow"
    }
    
    try:
        response = requests.post(f"{base_url}/checkout/create/", json=payment_data)
        if response.status_code == 201:
            payment_result = response.json()
            payment_ref = payment_result['payment']['reference']
            print(f"   ✅ Payment created: {payment_ref}")
            print(f"   💰 Amount: {payment_result['payment']['currency']} {payment_result['payment']['amount']}")
            print(f"   📊 Status: {payment_result['payment']['status']}")
        else:
            print(f"   ❌ Failed to create payment: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error creating payment: {e}")
        return False
    
    # Step 3: Test status endpoint immediately
    print(f"\n3. Testing status endpoint for {payment_ref}...")
    try:
        response = requests.get(f"{base_url}/{payment_ref}/status/")
        if response.status_code == 200:
            status_data = response.json()
            print(f"   ✅ Status check successful")
            print(f"   📊 Current status: {status_data['status']}")
            print(f"   🆔 Reference: {status_data['reference']}")
        else:
            print(f"   ❌ Status check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ❌ Error checking status: {e}")
        return False
    
    # Step 4: Wait for auto-completion
    print(f"\n4. Monitoring auto-completion (30 seconds)...")
    for i in range(6):  # Check every 5 seconds for 30 seconds
        time.sleep(5)
        try:
            response = requests.get(f"{base_url}/{payment_ref}/status/")
            if response.status_code == 200:
                status_data = response.json()
                current_status = status_data['status']
                print(f"   [{(i+1)*5}s] Status: {current_status}")
                
                if current_status in ['successful', 'failed']:
                    print(f"   🎉 Auto-completion worked! Final status: {current_status}")
                    break
            else:
                print(f"   [{(i+1)*5}s] Error checking status: {response.status_code}")
        except Exception as e:
            print(f"   [{(i+1)*5}s] Error: {e}")
    
    print("\n✅ Payment flow test completed!")
    return True

def test_debug_endpoint():
    """Test the debug endpoint"""
    
    print("\n🔍 Testing Debug Endpoint")
    print("=" * 30)
    
    try:
        response = requests.get("http://localhost:8000/api/payments/debug/")
        if response.status_code == 200:
            debug_data = response.json()
            print(f"✅ Debug endpoint working")
            print(f"📊 Total payments: {debug_data['total_payments']}")
            print(f"📅 Recent payments (24h): {debug_data['recent_payments_24h']}")
            
            if debug_data['payments']:
                print("\n📋 Recent payments:")
                for payment in debug_data['payments'][:5]:
                    print(f"   - {payment['reference']} ({payment['status']}) - {payment['amount']} {payment['currency']}")
        else:
            print(f"❌ Debug endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing debug endpoint: {e}")

def check_server_status():
    """Check if Django server is running"""
    
    print("🌐 Checking Server Status")
    print("=" * 25)
    
    try:
        response = requests.get("http://localhost:8000/api/payments/checkout/methods/", timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running on localhost:8000")
            return True
        else:
            print(f"⚠️ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Django server is not running on localhost:8000")
        print("   Please start it with: python manage.py runserver 8000")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {e}")
        return False

if __name__ == "__main__":
    print("Payment Flow Test Suite")
    print("=" * 50)
    
    # Check server first
    if not check_server_status():
        print("\n🚨 Please start the Django server first:")
        print("   cd Tback")
        print("   python manage.py runserver 8000")
        sys.exit(1)
    
    # Run tests
    print()
    success = test_complete_payment_flow()
    test_debug_endpoint()
    
    if success:
        print("\n🎯 All tests passed!")
        print("\nIf you're still getting 404 errors in the frontend:")
        print("1. Clear browser cache and localStorage")
        print("2. Check browser developer tools for the exact URL being requested")
        print("3. Verify the payment reference exists in the database")
        print("4. Check if there are any CORS issues")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")