#!/usr/bin/env python
"""
Comprehensive payment system diagnostics
"""
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.models import Payment, PaymentProvider

def check_django_server():
    """Check if Django server is running"""
    print("🌐 Checking Django Server")
    print("-" * 30)
    
    try:
        response = requests.get('http://localhost:8000/api/health/', timeout=5)
        if response.status_code == 200:
            print("✅ Django server is running on localhost:8000")
            return True
        else:
            print(f"⚠️ Django server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Django server is not running on localhost:8000")
        print("   Start it with: python manage.py runserver 8000")
        return False
    except Exception as e:
        print(f"❌ Error checking server: {str(e)}")
        return False

def check_payment_providers():
    """Check payment providers configuration"""
    print("\n💳 Checking Payment Providers")
    print("-" * 30)
    
    providers = PaymentProvider.objects.all()
    if not providers.exists():
        print("❌ No payment providers found")
        return False
    
    for provider in providers:
        status = "✅ Active" if provider.is_active else "❌ Inactive"
        print(f"{status} {provider.name} ({provider.code})")
    
    return True

def test_payment_methods_api():
    """Test payment methods API endpoint"""
    print("\n🔌 Testing Payment Methods API")
    print("-" * 30)
    
    try:
        response = requests.get('http://localhost:8000/api/payments/checkout/methods/')
        if response.status_code == 200:
            methods = response.json()
            print("✅ Payment methods API working")
            print(f"   Available methods: {len(methods.get('payment_methods', []))}")
            for method in methods.get('payment_methods', []):
                print(f"   - {method.get('name', 'Unknown')} ({method.get('id', 'Unknown')})")
            return True
        else:
            print(f"❌ Payment methods API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing payment methods API: {str(e)}")
        return False

def test_payment_creation():
    """Test payment creation"""
    print("\n💰 Testing Payment Creation")
    print("-" * 30)
    
    payment_data = {
        "amount": "25.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Diagnostic test payment"
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/',
            json=payment_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print("✅ Payment creation successful")
            print(f"   Payment reference: {payment_ref}")
            print(f"   Status: {result['payment']['status']}")
            return payment_ref
        else:
            print(f"❌ Payment creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error creating payment: {str(e)}")
        return None

def test_payment_status(payment_ref):
    """Test payment status checking"""
    print(f"\n📊 Testing Payment Status for {payment_ref}")
    print("-" * 30)
    
    try:
        response = requests.get(f'http://localhost:8000/api/payments/{payment_ref}/status/')
        if response.status_code == 200:
            status_data = response.json()
            print("✅ Payment status API working")
            print(f"   Status: {status_data['status']}")
            print(f"   Amount: {status_data['currency']} {status_data['amount']}")
            return status_data['status']
        else:
            print(f"❌ Payment status API failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error checking payment status: {str(e)}")
        return None

def check_recent_payments():
    """Check recent payments in database"""
    print("\n📋 Recent Payments in Database")
    print("-" * 30)
    
    recent_payments = Payment.objects.order_by('-created_at')[:10]
    
    if not recent_payments.exists():
        print("❌ No payments found in database")
        return
    
    print(f"Found {recent_payments.count()} recent payments:")
    
    status_counts = {}
    for payment in recent_payments:
        status = payment.status
        status_counts[status] = status_counts.get(status, 0) + 1
        
        # Show status with appropriate icon
        if status == 'successful':
            icon = "✅"
        elif status == 'processing':
            icon = "⏳"
        elif status == 'failed':
            icon = "❌"
        else:
            icon = "❓"
        
        print(f"   {icon} {payment.reference} ({status}) - {payment.created_at.strftime('%H:%M:%S')}")
    
    print(f"\nStatus summary:")
    for status, count in status_counts.items():
        print(f"   {status}: {count}")

def check_cors_configuration():
    """Check CORS configuration"""
    print("\n🌐 Testing CORS Configuration")
    print("-" * 30)
    
    headers = {
        'Origin': 'http://localhost:8080',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get('http://localhost:8000/api/cors-test/', headers=headers)
        if response.status_code == 200:
            cors_header = response.headers.get('Access-Control-Allow-Origin', 'Not present')
            print("✅ CORS test endpoint working")
            print(f"   Access-Control-Allow-Origin: {cors_header}")
            return True
        else:
            print(f"❌ CORS test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CORS test error: {str(e)}")
        return False

def main():
    """Run comprehensive diagnostics"""
    print("🔍 Payment System Diagnostics")
    print("=" * 50)
    
    # Run all checks
    server_ok = check_django_server()
    if not server_ok:
        print("\n❌ Django server is not running. Please start it first.")
        return
    
    providers_ok = check_payment_providers()
    methods_ok = test_payment_methods_api()
    cors_ok = check_cors_configuration()
    
    check_recent_payments()
    
    # Test payment creation if basic checks pass
    if providers_ok and methods_ok:
        payment_ref = test_payment_creation()
        if payment_ref:
            test_payment_status(payment_ref)
    
    print("\n" + "=" * 50)
    print("🎯 Diagnostic Summary")
    print("=" * 50)
    
    if server_ok and providers_ok and methods_ok and cors_ok:
        print("✅ All basic systems are working")
        print("\nIf payments are still not working, the issue might be:")
        print("1. Frontend not connecting to backend")
        print("2. Auto-completion daemon not running")
        print("3. Browser cache issues")
        print("4. Network connectivity problems")
        
        print("\n🔧 Solutions to try:")
        print("1. Clear browser cache (Ctrl+Shift+R)")
        print("2. Start auto-completion daemon:")
        print("   python manage.py auto_complete_daemon --interval 10 --timeout 30")
        print("3. Check browser console for errors")
        print("4. Try payment in incognito mode")
    else:
        print("❌ Some systems are not working properly")
        print("Please fix the issues above before testing payments")

if __name__ == "__main__":
    main()