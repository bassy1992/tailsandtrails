#!/usr/bin/env python3
"""
Test Paystack configuration endpoint
"""
import requests
import json

def test_paystack_config():
    """Test if Paystack configuration is accessible"""
    
    # Production URL
    config_url = "https://tailsandtrails-production.up.railway.app/api/payments/paystack/config/"
    
    try:
        print("Testing Paystack configuration endpoint...")
        print(f"URL: {config_url}")
        
        response = requests.get(config_url, timeout=30)
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            config_data = response.json()
            print(f"Response Body: {json.dumps(config_data, indent=2)}")
            
            # Check if public key is configured
            public_key = config_data.get('public_key', '')
            if public_key:
                print(f"\n✅ Paystack public key is configured: {public_key[:20]}...")
                if public_key.startswith('pk_test_'):
                    print("🧪 Running in TEST mode")
                elif public_key.startswith('pk_live_'):
                    print("🚀 Running in LIVE mode")
                else:
                    print("⚠️  Unknown key format")
            else:
                print("\n❌ Paystack public key is NOT configured")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
        return response.status_code == 200
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_paystack_config()