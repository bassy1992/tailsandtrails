#!/usr/bin/env python3
"""
Debug the live payment issue
"""
import requests
import json
from datetime import datetime

def check_recent_payments():
    """Check recent payments on the live server"""
    print("🔍 Checking Recent Payments on Live Server")
    print("=" * 50)
    
    try:
        # Check recent payments via a simple endpoint
        response = requests.get("https://tailsandtrails-production.up.railway.app/api/health/")
        print(f"✅ Server is responding: {response.status_code}")
        
        # Test payment creation
        print("\n📋 Testing Payment Creation...")
        payment_data = {
            'amount': 50,
            'currency': 'GHS',
            'payment_method': 'mobile_money',
            'provider': 'mtn',
            'phone_number': '0241234567',
            'email': 'test@example.com',
            'description': 'Test Ticket Purchase: Live Debug',
            'booking_details': {
                'type': 'ticket',
                'ticket_id': 2,
                'ticket_title': 'Black Stars vs Nigeria - AFCON Qualifier',
                'quantity': 1,
                'unit_price': 50,
                'customer_name': 'Debug Test',
                'customer_email': 'test@example.com',
                'customer_phone': '0241234567',
                'payment_provider': 'mtn',
                'account_name': 'Debug Account'
            }
        }
        
        payment_response = requests.post(
            "https://tailsandtrails-production.up.railway.app/api/payments/paystack/create/",
            json=payment_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Payment Response Status: {payment_response.status_code}")
        
        if payment_response.status_code == 201:
            result = payment_response.json()
            if result.get('success'):
                reference = result['payment']['reference']
                auth_url = result.get('paystack', {}).get('authorization_url')
                
                print(f"✅ Payment created: {reference}")
                print(f"🔗 Auth URL: {auth_url[:50]}..." if auth_url else "❌ No auth URL")
                
                # Test verification
                print(f"\n🔍 Testing Payment Verification...")
                verify_response = requests.get(
                    f"https://tailsandtrails-production.up.railway.app/api/payments/paystack/verify/{reference}/"
                )
                
                print(f"Verify Response Status: {verify_response.status_code}")
                
                if verify_response.status_code == 200:
                    verify_result = verify_response.json()
                    payment_status = verify_result.get('payment', {}).get('status', 'unknown')
                    print(f"💳 Payment Status: {payment_status}")
                    
                    if payment_status == 'cancelled':
                        print("❌ FOUND THE ISSUE: Payment is being marked as cancelled!")
                        print("This explains the 'Payment was declined or cancelled' message")
                        
                        # Check if it's a test mode issue
                        is_test_mode = verify_result.get('test_mode', False)
                        print(f"🧪 Test Mode: {is_test_mode}")
                        
                        if is_test_mode:
                            print("💡 SOLUTION: In test mode, mobile money payments need special handling")
                            print("The payment might be timing out or not being auto-approved correctly")
                    
                return reference
            else:
                print(f"❌ Payment creation failed: {result.get('error')}")
        else:
            print(f"❌ Payment request failed: {payment_response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    return None

def check_paystack_config():
    """Check Paystack configuration"""
    print("\n🏦 Checking Paystack Configuration")
    print("=" * 40)
    
    try:
        response = requests.get("https://tailsandtrails-production.up.railway.app/api/payments/paystack/config/")
        
        if response.status_code == 200:
            config = response.json()
            public_key = config.get('public_key', '')
            
            print(f"📋 Public Key: {public_key[:20]}..." if public_key else "❌ No public key")
            
            if public_key.startswith('pk_test_'):
                print("🧪 RUNNING IN TEST MODE")
                print("💡 This might be causing the mobile money payment issues")
                print("   Test mode mobile money payments need special handling")
            elif public_key.startswith('pk_live_'):
                print("🚀 RUNNING IN LIVE MODE")
            else:
                print("❓ Unknown key format")
                
            print(f"📱 Supported channels: {config.get('supported_channels', [])}")
            print(f"💰 Supported currencies: {config.get('supported_currencies', [])}")
            
        else:
            print(f"❌ Config request failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking config: {e}")

def main():
    """Main debug function"""
    print("🚨 DEBUGGING LIVE PAYMENT ISSUE")
    print("=" * 60)
    print("Issue: 'Payment was declined or cancelled' on ticket checkout")
    print("=" * 60)
    
    # Check Paystack config first
    check_paystack_config()
    
    # Check recent payments
    reference = check_recent_payments()
    
    print("\n" + "=" * 60)
    print("🎯 LIKELY CAUSES:")
    print("1. Test mode mobile money payments timing out")
    print("2. Payment verification returning 'cancelled' status")
    print("3. Frontend not handling payment redirect properly")
    print("4. Paystack webhook not updating payment status")
    
    print("\n🔧 NEXT STEPS:")
    print("1. Check if payments are being marked as 'cancelled' in verification")
    print("2. Verify test mode mobile money auto-approval is working")
    print("3. Check frontend payment callback handling")
    print("4. Test with a real mobile money transaction if possible")

if __name__ == "__main__":
    main()