#!/usr/bin/env python3
"""
Test Railway environment variables
"""
import requests
import json

def test_railway_environment():
    """Test if environment variables are properly set on Railway"""
    
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    print("🧪 Testing Railway environment variables...")
    
    # Test 1: Paystack Configuration
    print("\n1. Testing Paystack configuration...")
    try:
        response = requests.get(f"{base_url}/payments/paystack/config/", timeout=30)
        
        if response.status_code == 200:
            config = response.json()
            public_key = config.get('public_key', '')
            
            if public_key:
                print(f"✅ Paystack public key configured: {public_key[:20]}...")
                if public_key.startswith('pk_test_'):
                    print("🧪 Paystack in TEST mode")
                elif public_key.startswith('pk_live_'):
                    print("🚀 Paystack in LIVE mode")
            else:
                print("❌ Paystack public key NOT configured")
                print("💡 Add PAYSTACK_PUBLIC_KEY and PAYSTACK_SECRET_KEY to Railway")
        else:
            print(f"❌ Paystack config endpoint failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Paystack test failed: {str(e)}")
    
    # Test 2: Media Storage (check if Spaces is configured)
    print("\n2. Testing media storage configuration...")
    try:
        # Try to access a media endpoint or check Django admin
        response = requests.get(f"{base_url}/health/", timeout=30)
        
        if response.status_code == 200:
            print("✅ Django server is running")
            print("💡 DigitalOcean Spaces configuration will be tested when uploading files")
        else:
            print(f"⚠️  Server response: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Server test failed: {str(e)}")
    
    # Test 3: Payment Creation (if Paystack is configured)
    print("\n3. Testing payment creation...")
    try:
        payment_data = {
            "amount": 10,
            "email": "test@example.com", 
            "payment_method": "card",
            "description": "Test payment"
        }
        
        response = requests.post(
            f"{base_url}/payments/paystack/create/",
            json=payment_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Payment creation successful!")
            auth_url = result.get('paystack', {}).get('authorization_url', '')
            if auth_url:
                print(f"✅ Authorization URL generated: {auth_url[:50]}...")
        elif response.status_code == 500:
            print("❌ Payment creation failed - likely missing Paystack keys")
        else:
            print(f"⚠️  Payment creation response: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
    
    except Exception as e:
        print(f"❌ Payment test failed: {str(e)}")
    
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    print("✅ Environment variables to add to Railway:")
    print("   • SPACES_KEY (✅ you have this)")
    print("   • SPACES_SECRET (❌ you need this)")
    print("   • PAYSTACK_PUBLIC_KEY (❌ you need this)")
    print("   • PAYSTACK_SECRET_KEY (❌ you need this)")

if __name__ == "__main__":
    test_railway_environment()