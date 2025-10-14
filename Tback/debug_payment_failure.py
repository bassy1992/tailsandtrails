#!/usr/bin/env python
"""
Debug payment failure issue
"""
import os
import sys
import django
import requests
import json
import traceback

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def test_payment_creation_detailed():
    """Test payment creation with detailed debugging"""
    print("🔍 Detailed Payment Creation Debug")
    print("=" * 50)
    
    # Test both card and mobile money
    test_cases = [
        {
            'name': 'Card Payment',
            'data': {
                'amount': 50.0,
                'currency': 'GHS',
                'payment_method': 'card',
                'email': 'test@example.com',
                'description': 'Test Card Payment'
            }
        },
        {
            'name': 'Mobile Money Payment',
            'data': {
                'amount': 50.0,
                'currency': 'GHS',
                'payment_method': 'mobile_money',
                'provider': 'mtn',
                'phone_number': '+233241234567',
                'email': 'test@example.com',
                'description': 'Test Mobile Money Payment'
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        print(f"Request Data: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                'http://localhost:8000/api/payments/paystack/create/',
                headers={'Content-Type': 'application/json'},
                json=test_case['data']
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            
            try:
                response_data = response.json()
                print(f"Response Data: {json.dumps(response_data, indent=2)}")
                
                if response.status_code == 201 and response_data.get('success'):
                    print(f"✅ {test_case['name']} - SUCCESS")
                    
                    # Test verification
                    payment_ref = response_data.get('payment', {}).get('reference')
                    if payment_ref:
                        print(f"\n🔍 Testing verification for: {payment_ref}")
                        verify_response = requests.get(
                            f'http://localhost:8000/api/payments/paystack/verify/{payment_ref}/'
                        )
                        print(f"Verify Status: {verify_response.status_code}")
                        if verify_response.status_code == 200:
                            verify_data = verify_response.json()
                            print(f"Verify Success: {verify_data.get('success')}")
                            print(f"Payment Status: {verify_data.get('payment', {}).get('status')}")
                        
                else:
                    print(f"❌ {test_case['name']} - FAILED")
                    print(f"Error: {response_data.get('error', 'Unknown error')}")
                    
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception during {test_case['name']}: {e}")
            traceback.print_exc()

def test_paystack_service_directly():
    """Test Paystack service directly"""
    print(f"\n🔧 Direct Paystack Service Test")
    print("=" * 40)
    
    try:
        from payments.paystack_service import PaystackService
        
        service = PaystackService()
        print(f"✅ Service initialized")
        
        # Test card payment
        print(f"\n💳 Testing Card Payment...")
        card_data = {
            'amount': 50.0,
            'email': 'test@example.com',
            'reference': f'TEST_CARD_{int(__import__("time").time())}',
            'payment_method': 'card',
            'description': 'Direct service test - card'
        }
        
        card_result = service.initialize_payment(card_data)
        print(f"Card Result: {json.dumps(card_result, indent=2)}")
        
        # Test mobile money
        print(f"\n📱 Testing Mobile Money...")
        momo_data = {
            'amount': 50.0,
            'email': 'test@example.com',
            'reference': f'TEST_MOMO_{int(__import__("time").time())}',
            'payment_method': 'mobile_money',
            'phone_number': '+233241234567',
            'provider': 'mtn',
            'description': 'Direct service test - mobile money'
        }
        
        momo_result = service.initialize_mobile_money(momo_data)
        print(f"Mobile Money Result: {json.dumps(momo_result, indent=2)}")
        
        return card_result.get('success', False), momo_result.get('success', False)
        
    except Exception as e:
        print(f"❌ Direct service test failed: {e}")
        traceback.print_exc()
        return False, False

def check_database_payments():
    """Check recent payments in database"""
    print(f"\n💾 Database Payments Check")
    print("=" * 30)
    
    try:
        from payments.models import Payment
        
        recent_payments = Payment.objects.all().order_by('-created_at')[:5]
        
        if recent_payments:
            print(f"Recent payments ({len(recent_payments)}):")
            for payment in recent_payments:
                print(f"  - {payment.reference}: {payment.status} (GH₵{payment.amount})")
        else:
            print("No payments found in database")
            
        return len(recent_payments)
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")
        return 0

def check_server_logs():
    """Check for any server errors"""
    print(f"\n📋 Server Status Check")
    print("=" * 25)
    
    try:
        # Test basic server health
        response = requests.get('http://localhost:8000/api/health/')
        print(f"Health Check: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"Server Status: {health_data.get('status')}")
        
        # Test Paystack config
        config_response = requests.get('http://localhost:8000/api/payments/paystack/config/')
        print(f"Paystack Config: {config_response.status_code}")
        
        if config_response.status_code == 200:
            config_data = config_response.json()
            public_key = config_data.get('public_key', '')
            print(f"Public Key: {public_key[:20]}..." if public_key else "Public Key: NOT SET")
            
        return response.status_code == 200 and config_response.status_code == 200
        
    except Exception as e:
        print(f"❌ Server check failed: {e}")
        return False

def main():
    """Main debug function"""
    print("🐛 Payment Failure Debug Session")
    print("=" * 50)
    
    # Check server status
    server_ok = check_server_logs()
    
    # Check database
    db_payments = check_database_payments()
    
    # Test Paystack service directly
    card_ok, momo_ok = test_paystack_service_directly()
    
    # Test API endpoints
    test_payment_creation_detailed()
    
    # Summary
    print(f"\n📊 Debug Summary")
    print("=" * 20)
    print(f"Server Health: {'✅' if server_ok else '❌'}")
    print(f"Database Payments: {db_payments} found")
    print(f"Card Service: {'✅' if card_ok else '❌'}")
    print(f"Mobile Money Service: {'✅' if momo_ok else '❌'}")
    
    if not server_ok:
        print(f"\n🔧 Server Issues Detected:")
        print(f"   - Check if Django server is running")
        print(f"   - Verify Paystack configuration")
    
    if not (card_ok and momo_ok):
        print(f"\n🔧 Service Issues Detected:")
        print(f"   - Check Paystack API keys")
        print(f"   - Verify network connectivity")
        print(f"   - Check Django logs for errors")
    
    print(f"\n💡 Next Steps:")
    print(f"   1. Check the detailed output above for specific errors")
    print(f"   2. Ensure Django server is running: python manage.py runserver")
    print(f"   3. Check browser network tab for exact error messages")
    print(f"   4. Look at Django console for any error logs")

if __name__ == '__main__':
    main()