#!/usr/bin/env python
"""
Test that mobile money redirects to Paystack properly
"""
import os
import sys
import django

# Add the Tback directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Tback'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from payments.paystack_service import PaystackService
from django.conf import settings

def test_paystack_redirect():
    """Test that mobile money properly redirects to Paystack"""
    print("🧪 Testing Paystack Mobile Money Redirect")
    print("=" * 50)
    
    try:
        # Test the mobile money initialization
        service = PaystackService()
        test_data = {
            'amount': 50.0,
            'email': 'test@example.com',
            'reference': 'TEST-MOMO-REDIRECT-123',
            'payment_method': 'mobile_money',
            'provider': 'mtn',
            'phone_number': '0244123456',
            'description': 'Test mobile money payment'
        }

        result = service.initialize_payment(test_data)
        
        print(f"✅ Mobile Money Payment Initialization:")
        print(f"   Success: {result.get('success')}")
        print(f"   Authorization URL: {result.get('authorization_url')}")
        print(f"   Access Code: {result.get('access_code')}")
        
        # Check if it's a Paystack URL
        auth_url = result.get('authorization_url', '')
        if 'paystack.com' in auth_url or 'checkout.paystack.com' in auth_url:
            print("✅ SUCCESS: Redirects to Paystack website!")
            print("   Users will be taken to Paystack to approve mobile money payment")
        else:
            print(f"⚠️  WARNING: URL doesn't look like Paystack: {auth_url}")
        
        # Check channels configuration
        if result.get('success'):
            print("✅ Payment created successfully - will redirect to Paystack")
        else:
            print(f"❌ Payment creation failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

if __name__ == "__main__":
    test_paystack_redirect()