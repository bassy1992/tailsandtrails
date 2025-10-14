#!/usr/bin/env python
"""
Debug API call to see what's happening
"""
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from payments.paystack_views import create_paystack_payment
from payments.models import Payment

def test_api_call_directly():
    """Test the API call directly"""
    print("🧪 Testing API Call Directly")
    print("=" * 50)
    
    # Create request factory
    factory = RequestFactory()
    
    # Test data
    test_data = {
        'amount': 100.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0240381084',
        'description': 'Direct API test',
        'booking_details': {
            'type': 'destination',
            'destination': {
                'name': 'Direct API Test Tour',
                'price': 100.0
            },
            'travelers': {
                'adults': 1
            }
        }
    }
    
    print("📋 Test Data:")
    print(json.dumps(test_data, indent=2))
    print()
    
    # Create request
    request = factory.post(
        '/api/payments/paystack/create/',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    request.user = AnonymousUser()
    
    print("🔄 Calling API view directly...")
    
    try:
        response = create_paystack_payment(request)
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 201:
            response_data = json.loads(response.content)
            payment_ref = response_data.get('payment', {}).get('reference', '')
            
            print(f"✅ Payment Created: {payment_ref}")
            
            # Check the payment in database
            try:
                payment = Payment.objects.get(reference=payment_ref)
                print(f"📊 Payment Metadata: {payment.metadata}")
                
                if payment.metadata and 'booking_details' in payment.metadata:
                    print("✅ Booking details found!")
                    return True
                else:
                    print("❌ No booking details found")
                    return False
                    
            except Payment.DoesNotExist:
                print("❌ Payment not found in database")
                return False
        else:
            print(f"❌ API call failed")
            print(f"Response: {response.content}")
            return False
            
    except Exception as e:
        print(f"❌ Error calling API: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test"""
    print("🧪 Direct API Call Test")
    print("=" * 60)
    
    success = test_api_call_directly()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Direct API call works!")
    else:
        print("❌ Direct API call failed")

if __name__ == '__main__':
    main()