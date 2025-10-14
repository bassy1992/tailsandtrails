#!/usr/bin/env python
"""
Test MoMo payment with specific phone number: 0240381084
"""
import requests
import json
import webbrowser

def test_momo_with_specific_number():
    """Test MoMo payment with phone number 0240381084"""
    print("📱 Testing MoMo Payment with Number: 0240381084")
    print("=" * 50)
    
    # Create MoMo payment with your specific number
    momo_data = {
        'amount': 50.0,  # Test with GHS 50
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',  # MTN (0240 is MTN prefix)
        'phone_number': '0240381084',
        'description': 'Test MoMo Payment - Real Number Test'
    }
    
    print(f"💰 Amount: GHS {momo_data['amount']}")
    print(f"📱 Phone: {momo_data['phone_number']} (MTN)")
    print(f"📧 Email: {momo_data['email']}")
    print()
    
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
            
            # Get payment details
            payment_ref = result.get('payment', {}).get('reference', '')
            auth_url = result.get('paystack', {}).get('authorization_url', '')
            
            print("✅ Payment Created Successfully!")
            print(f"📋 Reference: {payment_ref}")
            print(f"🔗 Paystack URL: {auth_url}")
            print()
            
            print("🎯 What You'll See on Paystack:")
            print("   1. Mobile Money payment options")
            print("   2. MTN Mobile Money option")
            print("   3. Phone number: 233240381084 (auto-formatted)")
            print("   4. Amount: GHS 50.00")
            print()
            
            print("📱 Mobile Money Test Options:")
            print("   Option 1: Use the actual MoMo number (0240381084)")
            print("   Option 2: Use test card numbers:")
            print("     - Success: 4084084084084081")
            print("     - Decline: 4084084084084099")
            print("     - CVV: 408, Expiry: 12/25")
            print()
            
            print("🔄 Expected Flow:")
            print("   1. Click the Paystack URL below")
            print("   2. Choose Mobile Money → MTN")
            print("   3. Confirm phone number: 0240381084")
            print("   4. Complete payment")
            print("   5. Get redirected back to localhost:8080")
            print()
            
            # Show the test URL
            print("🚀 TEST URL:")
            print("=" * 50)
            print(auth_url)
            print("=" * 50)
            
            # Ask if user wants to open
            try:
                open_now = input("\n🌐 Open Paystack checkout now? (y/n): ").lower().strip()
                if open_now in ['y', 'yes']:
                    webbrowser.open(auth_url)
                    print("✅ Opened in browser!")
                    
                    print("\n⏳ After completing payment, you should be redirected to:")
                    print("   Success: http://localhost:8080/payment-success?reference=" + payment_ref)
                    print("   Failed:  http://localhost:8080/payment-failed?reference=" + payment_ref)
                else:
                    print("📋 Copy the URL above to test manually")
            except:
                print("📋 Copy the URL above to test manually")
            
            return True, auth_url, payment_ref
            
        else:
            print("❌ Failed to create payment")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
            return False, None, None
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False, None, None

def create_multiple_test_amounts():
    """Create multiple test payments with different amounts"""
    print("\n💰 Creating Multiple Test Amounts")
    print("=" * 50)
    
    test_amounts = [25.0, 50.0, 100.0, 200.0]
    test_urls = []
    
    for amount in test_amounts:
        momo_data = {
            'amount': amount,
            'email': 'test@example.com',
            'payment_method': 'mobile_money',
            'provider': 'mtn',
            'phone_number': '0240381084',
            'description': f'Test MoMo Payment - GHS {amount}'
        }
        
        try:
            response = requests.post(
                'http://localhost:8000/api/payments/paystack/create/',
                json=momo_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                auth_url = result.get('paystack', {}).get('authorization_url', '')
                reference = result.get('payment', {}).get('reference', '')
                
                test_urls.append({
                    'amount': amount,
                    'reference': reference,
                    'url': auth_url
                })
                
                print(f"✅ GHS {amount:>6.2f}: {reference}")
            else:
                print(f"❌ GHS {amount:>6.2f}: Failed")
                
        except Exception as e:
            print(f"❌ GHS {amount:>6.2f}: Error - {e}")
    
    return test_urls

def main():
    """Main test function"""
    print("🧪 MoMo Payment Test - Phone: 0240381084")
    print("=" * 60)
    
    # Check server
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    print()
    
    # Test main payment
    success, auth_url, payment_ref = test_momo_with_specific_number()
    
    if success:
        # Create additional test amounts
        test_urls = create_multiple_test_amounts()
        
        if test_urls:
            print("\n📋 All Test Payment URLs:")
            print("=" * 50)
            for test in test_urls:
                print(f"GHS {test['amount']:>6.2f}: {test['url']}")
        
        print("\n🎯 Testing Instructions:")
        print("=" * 50)
        print("1. Click any Paystack URL above")
        print("2. On Paystack page, select 'Mobile Money'")
        print("3. Choose 'MTN Mobile Money'")
        print("4. Verify phone number: 0240381084")
        print("5. Complete the payment")
        print("6. You'll be redirected back to localhost:8080")
        print("7. Check Paystack dashboard for the payment")
        
        print("\n💡 Alternative Testing:")
        print("   - If MoMo doesn't work, use test card: 4084084084084081")
        print("   - Both methods will redirect back to your website")
        print("   - Both will appear in Paystack dashboard")
        
        print(f"\n🚀 Quick Test: {auth_url}")
    
    else:
        print("\n❌ Test failed. Check the errors above.")

if __name__ == '__main__':
    main()