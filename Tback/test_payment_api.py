#!/usr/bin/env python
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def test_payment_methods_api():
    """Test the payment methods API endpoint"""
    try:
        response = requests.get('http://localhost:8000/api/payments/checkout/methods/', timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ Payment Methods API Response:")
            print(json.dumps(data, indent=2))
            
            print("\n📋 Available Payment Methods:")
            for method in data.get('payment_methods', []):
                providers_count = len(method.get('providers', []))
                print(f"- {method['name']} ({method['id']}): {providers_count} providers")
                
                if method.get('providers'):
                    for provider in method['providers']:
                        print(f"  * {provider['name']} ({provider['code']})")
                        
            # Check if Stripe is available
            stripe_methods = [m for m in data.get('payment_methods', []) if m['id'] == 'card']
            if stripe_methods:
                stripe_method = stripe_methods[0]
                stripe_providers = [p for p in stripe_method.get('providers', []) if p['code'] == 'stripe']
                if stripe_providers:
                    print(f"\n✅ Stripe is available as a payment option!")
                    print(f"   Provider: {stripe_providers[0]['name']}")
                else:
                    print(f"\n❌ Stripe provider not found in card payment method")
            else:
                print(f"\n❌ Card payment method not available")
                
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Make sure Django server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_payment_methods_api()