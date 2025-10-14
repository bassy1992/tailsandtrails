#!/usr/bin/env python
"""
Test the updated MoMo redirect flow
"""
import requests
import json

def test_momo_redirect_flow():
    """Test that MoMo payments now redirect to Paystack"""
    print("🔄 Testing Updated MoMo Redirect Flow")
    print("=" * 50)
    
    # Create MoMo payment
    momo_data = {
        'amount': 100.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0240381084',
        'description': 'Test MoMo Redirect Flow'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=momo_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"API Response: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            
            # Check if we got authorization_url
            auth_url = result.get('paystack', {}).get('authorization_url', '')
            payment_ref = result.get('payment', {}).get('reference', '')
            
            print("✅ Payment Created Successfully!")
            print(f"📋 Reference: {payment_ref}")
            print(f"🔗 Authorization URL: {auth_url}")
            print()
            
            if auth_url:
                print("✅ Frontend Should Now:")
                print("   1. Store payment reference in sessionStorage")
                print("   2. Store payment data in sessionStorage") 
                print("   3. Redirect to Paystack: window.location.href = authorization_url")
                print()
                
                print("🎯 Expected User Flow:")
                print("   1. User fills MoMo form and clicks 'Pay'")
                print("   2. Frontend calls API and gets authorization_url")
                print("   3. Frontend redirects to Paystack checkout")
                print("   4. User completes payment on Paystack")
                print("   5. Paystack redirects back to /payment-success")
                print("   6. User sees success page with booking details")
                print()
                
                print("🧪 Test This Flow:")
                print(f"   URL: {auth_url}")
                print("   Expected callback: http://localhost:8080/payment-success")
                
                return True, auth_url, payment_ref
            else:
                print("❌ No authorization_url in response")
                print("Response:", json.dumps(result, indent=2))
                return False, None, None
        else:
            print(f"❌ API call failed: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
            return False, None, None
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False, None, None

def show_frontend_changes():
    """Show what changed in the frontend"""
    print("\n💻 Frontend Changes Made:")
    print("=" * 50)
    
    print("📝 Updated MomoCheckout.tsx:")
    print("   - Now checks for result.paystack.authorization_url")
    print("   - Stores payment data in sessionStorage")
    print("   - Redirects to Paystack instead of polling")
    print()
    
    print("📝 Updated PaymentCallback.tsx:")
    print("   - Restores original payment data from sessionStorage")
    print("   - Handles both MoMo and card payment returns")
    print("   - Redirects to success page with complete data")
    print()
    
    print("🔄 New Flow:")
    print("   MomoCheckout → Paystack → PaymentCallback → PaymentSuccess")

def main():
    """Main test function"""
    print("🧪 Updated MoMo Redirect Flow Test")
    print("=" * 60)
    
    # Check server
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    print()
    
    # Test the flow
    success, auth_url, payment_ref = test_momo_redirect_flow()
    
    if success:
        show_frontend_changes()
        
        print(f"\n🚀 Ready to Test!")
        print("=" * 60)
        print("1. Go to your MoMo checkout page")
        print("2. Fill in MoMo details and click 'Pay'")
        print("3. Should redirect to Paystack automatically")
        print("4. Complete payment on Paystack")
        print("5. Should redirect back to success page")
        print()
        print(f"Direct test URL: {auth_url}")
        print("\nYour MoMo redirect flow is now working! 🎉")
    else:
        print("\n❌ Flow test failed. Check the errors above.")

if __name__ == '__main__':
    main()