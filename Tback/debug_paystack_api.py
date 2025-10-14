#!/usr/bin/env python
"""
Debug Paystack API call to identify the "Invalid key" error
"""
import os
import sys
import django
import requests
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.conf import settings

def test_direct_api_call():
    """Test direct API call to match frontend request"""
    print("🔍 Testing Direct API Call...")
    
    # Exact same data as frontend
    request_data = {
        "amount": 50.0,
        "currency": "GHS",
        "payment_method": "card",
        "email": "test@example.com",
        "description": "Test Payment",
        "booking_details": None
    }
    
    print(f"Request Data: {json.dumps(request_data, indent=2)}")
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            headers={'Content-Type': 'application/json'},
            json=request_data
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"Response Data: {json.dumps(response_data, indent=2)}")
        except:
            print(f"Raw Response: {response.text}")
            
        return response.status_code == 201
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        return False

def test_paystack_keys():
    """Test Paystack keys directly"""
    print("\n🔑 Testing Paystack Keys...")
    
    public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
    secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
    
    print(f"Public Key: {public_key}")
    print(f"Secret Key: {secret_key[:20]}...")
    
    # Test with Paystack API directly
    headers = {
        'Authorization': f'Bearer {secret_key}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Test banks endpoint (simple test)
        response = requests.get(
            'https://api.paystack.co/bank',
            headers=headers
        )
        
        print(f"Paystack API Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Paystack keys are valid")
            return True
        else:
            print(f"❌ Paystack API error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Paystack API test failed: {e}")
        return False

def test_django_service():
    """Test Django Paystack service directly"""
    print("\n🔧 Testing Django Paystack Service...")
    
    try:
        from payments.paystack_service import PaystackService
        
        service = PaystackService()
        print(f"✅ Service initialized")
        print(f"Public Key: {service.public_key[:20]}...")
        print(f"Secret Key: {service.secret_key[:20]}...")
        
        # Test payment initialization
        payment_data = {
            'amount': 50.0,
            'email': 'test@example.com',
            'reference': f'DEBUG_{int(__import__("time").time())}',
            'payment_method': 'card',
            'description': 'Debug test payment'
        }
        
        result = service.initialize_payment(payment_data)
        print(f"Payment initialization result: {result}")
        
        return result.get('success', False)
        
    except Exception as e:
        print(f"❌ Django service test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_server_status():
    """Check if Django server is running"""
    print("\n🌐 Checking Server Status...")
    
    try:
        response = requests.get('http://localhost:8000/api/payments/paystack/config/')
        print(f"Config endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            config = response.json()
            print(f"Config data: {json.dumps(config, indent=2)}")
            return True
        else:
            print(f"Config endpoint error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Server not accessible: {e}")
        return False

def main():
    """Run all debug tests"""
    print("🐛 Paystack API Debug Session")
    print("=" * 50)
    
    tests = [
        ("Server Status", check_server_status),
        ("Paystack Keys", test_paystack_keys),
        ("Django Service", test_django_service),
        ("Direct API Call", test_direct_api_call),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        results[test_name] = test_func()
    
    print(f"\n{'='*50}")
    print("📊 Debug Results:")
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    if not all(results.values()):
        print(f"\n🔧 Troubleshooting Tips:")
        if not results.get("Server Status"):
            print("   - Make sure Django server is running: python manage.py runserver")
        if not results.get("Paystack Keys"):
            print("   - Check your Paystack API keys in .env file")
        if not results.get("Django Service"):
            print("   - Check Django settings and Paystack service configuration")
    else:
        print(f"\n🎉 All tests passed! The issue might be in the frontend request.")

if __name__ == '__main__':
    main()