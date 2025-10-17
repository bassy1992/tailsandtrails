#!/usr/bin/env python3
"""
Debug script for ticket Paystack payment issues
"""
import os
import sys
import django
import requests
import json
from datetime import datetime

# Add the project directory to Python path
sys.path.append('/app' if os.path.exists('/app') else '.')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
django.setup()

from django.conf import settings
from Tback.payments.models import Payment, PaymentProvider
from Tback.payments.paystack_service import PaystackService

def test_ticket_paystack_payment():
    """Test ticket payment with Paystack"""
    print("🎫 Testing Ticket Paystack Payment Flow")
    print("=" * 50)
    
    # Check Paystack configuration
    print(f"Paystack Public Key: {settings.PAYSTACK_PUBLIC_KEY[:20]}..." if settings.PAYSTACK_PUBLIC_KEY else "❌ No public key")
    print(f"Paystack Secret Key: {settings.PAYSTACK_SECRET_KEY[:20]}..." if settings.PAYSTACK_SECRET_KEY else "❌ No secret key")
    print(f"Frontend URL: {settings.FRONTEND_URL}")
    print()
    
    # Test payment data (similar to what frontend sends)
    test_payment_data = {
        'amount': 50,
        'currency': 'GHS',
        'payment_method': 'mobile_money',
        'provider': 'mtn',  # This should map to 'mtn' for Paystack
        'phone_number': '0241234567',
        'email': 'test@example.com',
        'description': 'Test Ticket Purchase: Concert Ticket (1 tickets)',
        'booking_details': {
            'type': 'ticket',
            'ticket_id': 1,
            'ticket_title': 'Concert Ticket',
            'quantity': 1,
            'unit_price': 50,
            'customer_name': 'Test Customer',
            'customer_email': 'test@example.com',
            'customer_phone': '0241234567',
            'payment_provider': 'mtn',
            'account_name': 'Test Account'
        }
    }
    
    print("📋 Test Payment Data:")
    print(json.dumps(test_payment_data, indent=2))
    print()
    
    try:
        # Test the API endpoint directly
        api_url = f"{settings.BASE_URL}/api/payments/paystack/create/"
        print(f"🌐 Testing API endpoint: {api_url}")
        
        response = requests.post(api_url, json=test_payment_data, headers={
            'Content-Type': 'application/json'
        })
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        try:
            result = response.json()
            print("📋 Response Data:")
            print(json.dumps(result, indent=2))
            
            if result.get('success'):
                print("✅ Payment creation successful!")
                
                # Check if authorization URL is present
                auth_url = result.get('paystack', {}).get('authorization_url')
                if auth_url:
                    print(f"🔗 Authorization URL: {auth_url}")
                    print("✅ Should redirect to Paystack")
                else:
                    print("❌ No authorization URL - this is the problem!")
                    
            else:
                print(f"❌ Payment creation failed: {result.get('error')}")
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            
    except Exception as e:
        print(f"❌ API test failed: {str(e)}")
    
    print()
    
    # Test Paystack service directly
    print("🔧 Testing PaystackService directly...")
    try:
        paystack_service = PaystackService()
        
        # Prepare payment data for Paystack service
        service_payment_data = {
            'amount': test_payment_data['amount'],
            'email': test_payment_data['email'],
            'reference': f"TEST-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'currency': test_payment_data.get('currency', 'GHS'),
            'payment_method': test_payment_data['payment_method'],
            'phone_number': test_payment_data.get('phone_number', ''),
            'description': test_payment_data.get('description', 'Test payment'),
            'callback_url': f"{settings.FRONTEND_URL}/payment-callback",
            'provider': test_payment_data.get('provider', 'mtn')
        }
        
        print("📋 Service Payment Data:")
        print(json.dumps(service_payment_data, indent=2))
        print()
        
        # Test payment initialization
        result = paystack_service.initialize_payment(service_payment_data)
        
        print("📋 Service Result:")
        print(json.dumps(result, indent=2))
        
        if result.get('success'):
            print("✅ Paystack service initialization successful!")
            
            auth_url = result.get('authorization_url')
            if auth_url:
                print(f"🔗 Authorization URL: {auth_url}")
                print("✅ Paystack service working correctly")
            else:
                print("❌ No authorization URL from service")
        else:
            print(f"❌ Paystack service failed: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Paystack service test failed: {str(e)}")
        import traceback
        traceback.print_exc()

def check_payment_provider():
    """Check if Paystack provider is configured correctly"""
    print("\n🏦 Checking Payment Provider Configuration")
    print("=" * 50)
    
    try:
        provider = PaymentProvider.objects.get(code='paystack')
        print(f"✅ Paystack provider found: {provider.name}")
        print(f"   Active: {provider.is_active}")
        print(f"   Configuration: {provider.configuration}")
    except PaymentProvider.DoesNotExist:
        print("❌ Paystack provider not found - creating...")
        provider = PaymentProvider.objects.create(
            code='paystack',
            name='Paystack Ghana',
            is_active=True,
            configuration={
                'supports_mobile_money': True,
                'supports_cards': True,
                'currency': 'GHS'
            }
        )
        print(f"✅ Created Paystack provider: {provider.name}")

def check_recent_payments():
    """Check recent payment attempts"""
    print("\n💳 Recent Payment Attempts")
    print("=" * 50)
    
    recent_payments = Payment.objects.filter(
        provider__code='paystack'
    ).order_by('-created_at')[:5]
    
    for payment in recent_payments:
        print(f"📋 Payment {payment.reference}")
        print(f"   Status: {payment.status}")
        print(f"   Amount: {payment.amount} {payment.currency}")
        print(f"   Method: {payment.payment_method}")
        print(f"   Created: {payment.created_at}")
        print(f"   Phone: {payment.phone_number}")
        
        # Check metadata for Paystack data
        if payment.metadata and 'paystack_data' in payment.metadata:
            paystack_data = payment.metadata['paystack_data']
            print(f"   Paystack Status: {paystack_data.get('status', 'N/A')}")
            print(f"   Auth URL: {'Yes' if paystack_data.get('authorization_url') else 'No'}")
        
        print()

if __name__ == "__main__":
    check_payment_provider()
    check_recent_payments()
    test_ticket_paystack_payment()