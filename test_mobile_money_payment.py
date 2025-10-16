#!/usr/bin/env python3
"""
Test mobile money payment specifically for tickets
"""
import requests
import json
import time

def test_mobile_money_payment():
    """Test mobile money payment flow"""
    
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    # Test mobile money payment data (similar to what frontend sends)
    payment_data = {
        "amount": 90,  # Same as in your debug logs
        "currency": "GHS",
        "payment_method": "mobile_money",
        "provider": "mtn",  # mtn, vodafone, airteltigo
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
    
    print("🎫 Testing Mobile Money Payment for Tickets")
    print("=" * 50)
    print(f"URL: {base_url}/payments/paystack/create/")
    print(f"Data: {json.dumps(payment_data, indent=2)}")
    print()
    
    try:
        # Step 1: Create payment
        print("📱 Step 1: Creating mobile money payment...")
        response = requests.post(
            f"{base_url}/payments/paystack/create/",
            json=payment_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Payment created successfully!")
            print(f"Reference: {result['payment']['reference']}")
            print(f"Status: {result['payment']['status']}")
            
            if 'paystack' in result:
                paystack_data = result['paystack']
                print(f"Authorization URL: {paystack_data.get('authorization_url', 'N/A')}")
                print(f"Display Text: {paystack_data.get('display_text', 'N/A')}")
            
            # Step 2: Verify payment status
            reference = result['payment']['reference']
            print(f"\n🔍 Step 2: Verifying payment status for {reference}...")
            
            verify_response = requests.get(
                f"{base_url}/payments/paystack/verify/{reference}/",
                timeout=30
            )
            
            print(f"Verify Status Code: {verify_response.status_code}")
            
            if verify_response.status_code == 200:
                verify_result = verify_response.json()
                print("✅ Payment verification successful!")
                print(f"Payment Status: {verify_result['payment']['status']}")
                
                if 'paystack_data' in verify_result:
                    paystack_status = verify_result['paystack_data'].get('status', 'unknown')
                    print(f"Paystack Status: {paystack_status}")
                    
                    if paystack_status in ['failed', 'abandoned']:
                        print("❌ Payment was declined or cancelled by Paystack")
                        print("This matches the error you're seeing!")
                        
                        # Check if it's a test mode issue
                        if verify_result.get('test_mode'):
                            print("🧪 Test mode detected - this might be the issue")
                            print("In test mode, mobile money payments may not work properly")
                        
                        # Show gateway response if available
                        gateway_response = verify_result['paystack_data'].get('gateway_response')
                        if gateway_response:
                            print(f"Gateway Response: {gateway_response}")
                    
            else:
                print(f"❌ Verification failed: {verify_response.text}")
        
        else:
            print(f"❌ Payment creation failed: {response.text}")
            
    except requests.exceptions.Timeout:
        print("⏰ Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"🚫 Request error: {e}")
    except Exception as e:
        print(f"💥 Unexpected error: {e}")

def test_card_payment_comparison():
    """Test card payment to compare with mobile money"""
    
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    # Test card payment data
    payment_data = {
        "amount": 90,
        "currency": "GHS", 
        "payment_method": "card",
        "email": "test@example.com",
        "description": "Ticket Purchase: Test Event (1 tickets) - Card Payment",
        "booking_details": {
            "type": "ticket",
            "ticket_id": 1,
            "ticket_title": "Test Event",
            "quantity": 1,
            "unit_price": 90,
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "customer_phone": "0241234567"
        }
    }
    
    print("\n💳 Testing Card Payment for Comparison")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{base_url}/payments/paystack/create/",
            json=payment_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Card payment created successfully!")
            print(f"Reference: {result['payment']['reference']}")
            print(f"Status: {result['payment']['status']}")
            
            if 'paystack' in result:
                paystack_data = result['paystack']
                print(f"Authorization URL: {paystack_data.get('authorization_url', 'N/A')}")
        else:
            print(f"❌ Card payment creation failed: {response.text}")
            
    except Exception as e:
        print(f"💥 Card payment error: {e}")

if __name__ == "__main__":
    test_mobile_money_payment()
    test_card_payment_comparison()
    
    print("\n📋 Summary:")
    print("- If mobile money shows 'failed' or 'abandoned' status, that's your issue")
    print("- If card payment works but mobile money doesn't, it's a MoMo-specific problem")
    print("- Check if you're in test mode - MoMo may not work properly in Paystack test mode")
    print("- The frontend error 'Payment was declined or cancelled' comes from this backend status")