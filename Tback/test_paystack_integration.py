#!/usr/bin/env python
"""
Test Paystack integration with the new API keys
"""
import os
import sys
import django
import requests
import json
import time

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.paystack_service import PaystackService
from payments.models import Payment, PaymentProvider

def test_paystack_service():
    """Test Paystack service initialization and basic functionality"""
    print("🔧 Testing Paystack Service...")
    
    try:
        # Initialize service
        service = PaystackService()
        print(f"✅ Paystack service initialized successfully")
        print(f"   Public Key: {service.public_key[:20]}...")
        print(f"   Secret Key: {service.secret_key[:20]}...")
        
        return True
    except Exception as e:
        print(f"❌ Paystack service initialization failed: {e}")
        return False

def test_payment_initialization():
    """Test payment initialization"""
    print("\n💳 Testing Payment Initialization...")
    
    try:
        service = PaystackService()
        
        # Test card payment
        payment_data = {
            'amount': 50.00,
            'email': 'test@example.com',
            'reference': 'TEST_' + str(int(time.time())),
            'payment_method': 'card',
            'description': 'Test payment for Tails & Trails'
        }
        
        result = service.initialize_payment(payment_data)
        
        if result['success']:
            print(f"✅ Card payment initialized successfully")
            print(f"   Reference: {result['reference']}")
            print(f"   Authorization URL: {result['authorization_url'][:50]}...")
            return True
        else:
            print(f"❌ Card payment initialization failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Payment initialization test failed: {e}")
        return False

def test_mobile_money_initialization():
    """Test mobile money payment initialization"""
    print("\n📱 Testing Mobile Money Initialization...")
    
    try:
        service = PaystackService()
        
        # Test mobile money payment
        payment_data = {
            'amount': 25.00,
            'email': 'test@example.com',
            'reference': 'MOMO_TEST_' + str(int(time.time())),
            'payment_method': 'mobile_money',
            'phone_number': '+233241234567',
            'provider': 'mtn',
            'description': 'Test mobile money payment'
        }
        
        result = service.initialize_mobile_money(payment_data)
        
        if result['success']:
            print(f"✅ Mobile money payment initialized successfully")
            print(f"   Reference: {result['reference']}")
            print(f"   Status: {result['status']}")
            print(f"   Display Text: {result.get('display_text', 'N/A')}")
            return True
        else:
            print(f"❌ Mobile money initialization failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Mobile money initialization test failed: {e}")
        return False

def test_api_endpoints():
    """Test Paystack API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:8000/api/payments"
    
    # Test config endpoint
    try:
        response = requests.get(f"{base_url}/paystack/config/")
        if response.status_code == 200:
            config = response.json()
            print(f"✅ Config endpoint working")
            print(f"   Public Key: {config['public_key'][:20]}...")
            print(f"   Supported Currencies: {config['supported_currencies']}")
            print(f"   Mobile Money Providers: {len(config['mobile_money_providers'])}")
        else:
            print(f"❌ Config endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Config endpoint test failed: {e}")
        return False
    
    # Test payment creation endpoint
    try:
        payment_data = {
            'amount': 10.00,
            'email': 'test@example.com',
            'payment_method': 'card',
            'description': 'API test payment'
        }
        
        response = requests.post(f"{base_url}/paystack/create/", json=payment_data)
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Payment creation endpoint working")
            print(f"   Payment ID: {result['payment']['id']}")
            print(f"   Reference: {result['payment']['reference']}")
            return True
        else:
            print(f"❌ Payment creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Payment creation test failed: {e}")
        return False

def test_banks_api():
    """Test Paystack banks API"""
    print("\n🏦 Testing Banks API...")
    
    try:
        service = PaystackService()
        result = service.get_supported_banks()
        
        if result['success']:
            banks = result['banks']
            print(f"✅ Banks API working")
            print(f"   Total banks: {len(banks)}")
            print(f"   Sample banks: {[bank['name'] for bank in banks[:3]]}")
            return True
        else:
            print(f"❌ Banks API failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Banks API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Paystack Integration Tests")
    print("=" * 50)
    
    import time
    
    tests = [
        test_paystack_service,
        test_payment_initialization,
        test_mobile_money_initialization,
        test_banks_api,
        # test_api_endpoints,  # Requires server to be running
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Paystack integration is ready!")
        print("\n📋 Next Steps:")
        print("1. Start your Django server: python manage.py runserver")
        print("2. Test the frontend integration")
        print("3. Configure webhooks in Paystack dashboard")
        print("4. Test with real payments in sandbox mode")
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
    
    return passed == total

if __name__ == '__main__':
    main()