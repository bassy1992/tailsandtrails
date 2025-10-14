#!/usr/bin/env python3
"""
Test Paystack after configuration
"""
import requests
import json
import time

def test_paystack_after_config():
    """Test Paystack endpoints after configuration"""
    
    base_url = "https://tailsandtrails-production.up.railway.app/api/payments"
    
    print("🧪 Testing Paystack configuration after setup...")
    
    # Test 1: Check configuration
    print("\n1. Testing configuration endpoint...")
    config_response = requests.get(f"{base_url}/paystack/config/")
    
    if config_response.status_code == 200:
        config = config_response.json()
        public_key = config.get('public_key', '')
        
        if public_key:
            print(f"✅ Public key configured: {public_key[:20]}...")
            
            # Test 2: Try creating a payment
            print("\n2. Testing payment creation...")
            
            payment_data = {
                "amount": 10,  # Small test amount
                "email": "test@example.com",
                "payment_method": "card",
                "description": "Test payment after config"
            }
            
            create_response = requests.post(
                f"{base_url}/paystack/create/",
                json=payment_data,
                headers={'Content-Type': 'application/json'}
            )
            
            print(f"Status: {create_response.status_code}")
            
            if create_response.status_code == 201:
                result = create_response.json()
                print("✅ Payment creation successful!")
                print(f"Authorization URL: {result.get('paystack', {}).get('authorization_url', 'N/A')}")
                return True
            else:
                print(f"❌ Payment creation failed: {create_response.text}")
                return False
        else:
            print("❌ Public key still not configured")
            return False
    else:
        print(f"❌ Config endpoint failed: {config_response.status_code}")
        return False

if __name__ == "__main__":
    test_paystack_after_config()