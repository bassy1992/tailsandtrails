#!/usr/bin/env python
"""
Test MoMo payment redirect to Paystack
"""
import requests
import json

def test_momo_redirect():
    """Test that MoMo payments redirect to Paystack checkout"""
    print("🧪 Testing MoMo Payment Redirect to Paystack")
    print("=" * 50)
    
    # Test MoMo payment creation
    momo_data = {
        'amount': 100.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0244123456',
        'description': 'Test MoMo Payment for Redirect'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=momo_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            
            # Check if we got the authorization URL for redirect
            paystack_data = result.get('paystack', {})
            auth_url = paystack_data.get('authorization_url', '')
            
            if auth_url:
                print("✅ MoMo payment created successfully")
                print(f"📱 Payment Reference: {result.get('payment', {}).get('reference')}")
                print(f"🔗 Paystack Redirect URL: {auth_url}")
                print()
                print("🎯 Expected Behavior:")
                print("   1. Frontend should redirect user to the Paystack URL")
                print("   2. User will see Paystack checkout page")
                print("   3. User can complete payment with test card numbers:")
                print("      - Success: 4084084084084081")
                print("      - Decline: 4084084084084099")
                print("   4. Payment will appear in Paystack dashboard")
                print()
                print("✅ This is working as expected!")
                return True
            else:
                print("❌ No authorization URL returned")
                print("Response:", json.dumps(result, indent=2))
                return False
        else:
            print(f"❌ Payment creation failed")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False

def test_card_payment_comparison():
    """Test card payment for comparison"""
    print("\n💳 Testing Card Payment for Comparison")
    print("=" * 50)
    
    card_data = {
        'amount': 100.0,
        'email': 'test@example.com',
        'payment_method': 'card',
        'description': 'Test Card Payment for Comparison'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=card_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            paystack_data = result.get('paystack', {})
            auth_url = paystack_data.get('authorization_url', '')
            
            print("✅ Card payment created successfully")
            print(f"💳 Payment Reference: {result.get('payment', {}).get('reference')}")
            print(f"🔗 Paystack Redirect URL: {auth_url}")
            print("✅ Both MoMo and Card payments should redirect to Paystack")
            return True
        else:
            print("❌ Card payment creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Card payment error: {e}")
        return False

def main():
    """Run the tests"""
    print("🔧 MoMo Redirect Test Suite")
    print("=" * 60)
    
    # Test server availability
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    # Run tests
    momo_success = test_momo_redirect()
    card_success = test_card_payment_comparison()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results")
    print("=" * 60)
    print(f"MoMo Redirect Test: {'✅ PASS' if momo_success else '❌ FAIL'}")
    print(f"Card Payment Test: {'✅ PASS' if card_success else '❌ FAIL'}")
    
    if momo_success and card_success:
        print("\n🎉 Success! Both payment methods redirect to Paystack")
        print("\n📋 Frontend Integration:")
        print("   1. When user selects MoMo payment")
        print("   2. Call your payment API")
        print("   3. Get the authorization_url from response")
        print("   4. Redirect user: window.location.href = authorization_url")
        print("   5. User completes payment on Paystack website")
        print("   6. Paystack redirects back to your callback URL")
        print("   7. Payment appears in Paystack dashboard ✅")
    else:
        print("\n❌ Some tests failed. Check the errors above.")

if __name__ == '__main__':
    main()