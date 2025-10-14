#!/usr/bin/env python3
"""
Quick test to verify the Paystack create endpoint is accessible
"""
import requests
import json

def test_paystack_endpoint():
    """Test if the Paystack create endpoint responds correctly"""
    
    # Test data
    test_data = {
        "amount": 100,
        "email": "test@example.com",
        "payment_method": "card",
        "description": "Test payment"
    }
    
    # Production URL from the error
    production_url = "https://tailsandtrails-production.up.railway.app/api/payments/paystack/create/"
    
    try:
        print("Testing Paystack endpoint...")
        print(f"URL: {production_url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(
            production_url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 404:
            print("\n❌ 404 Error - Endpoint not found!")
            print("This confirms the URL routing issue.")
        else:
            print(f"Response Body: {response.text}")
            
        return response.status_code
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return None

if __name__ == "__main__":
    test_paystack_endpoint()