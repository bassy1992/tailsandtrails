#!/usr/bin/env python3
"""
Test the mobile money fix for test mode
"""
import requests
import json
import time

def test_mobile_money_fix():
    """Test mobile money payment with the fix"""
    
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    # Test mobile money payment data
    payment_data = {
        "amount": 90,
        "currency": "GHS",
        "payment_method": "mobile_money",
        "provider": "mtn",
        "phone_number": "0241234567",
        "email": "test@example.com",
        "description": "Ticket Purchase: Test Event (1 tickets)",
        "booking_details": {
            "type": "ticket",
            "ticket_id": 1,
            "ticket_title": "Test Event",
            "quantity": 1,
            "unit_price": 90,
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "customer_phone": "0241234567",
            "payment_provider": "mtn",
            "account_name": "Test Account"
        }
    }
    
    print("🔧 Testing Mobile Money Fix")
    print("=" * 50)
    
    try:
        # Step 1: Create payment
        print("📱 Creating mobile money payment...")
        response = requests.post(
            f"{base_url}/payments/paystack/create/",
            json=payment_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 201:
            result = response.json()
            reference = result['payment']['reference']
            print(f"✅ Payment created: {reference}")
            
            # Check if test mode is detected
            if result.get('paystack', {}).get('test_mode'):
                print("🧪 Test mode detected - fix should activate")
            
            # Step 2: Wait and verify (simulating the 10-second auto-approval)
            print("⏰ Waiting 12 seconds for auto-approval...")
            time.sleep(12)
            
            # Step 3: Verify payment
            print("🔍 Verifying payment status...")
            verify_response = requests.get(
                f"{base_url}/payments/paystack/verify/{reference}/",
                timeout=30
            )
            
            if verify_response.status_code == 200:
                verify_result = verify_response.json()
                payment_status = verify_result['payment']['status']
                
                print(f"Payment Status: {payment_status}")
                
                if payment_status == 'successful':
                    print("✅ SUCCESS! Mobile money payment was auto-approved in test mode")
                    if verify_result.get('test_mode'):
                        print("🧪 Test mode confirmation received")
                    return True
                else:
                    print(f"❌ Payment still shows status: {payment_status}")
                    return False
            else:
                print(f"❌ Verification failed: {verify_response.text}")
                return False
        else:
            print(f"❌ Payment creation failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"💥 Error: {e}")
        return False

if __name__ == "__main__":
    success = test_mobile_money_fix()
    
    if success:
        print("\n🎉 Fix is working! Mobile money payments should now work in test mode.")
        print("Users will see the payment auto-approved after 10 seconds.")
    else:
        print("\n❌ Fix needs to be deployed or there's still an issue.")
        print("The changes may not be live on the server yet.")