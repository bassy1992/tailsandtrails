#!/usr/bin/env python
"""
Test MoMo payment options on Paystack checkout page
"""
import requests
import json
import webbrowser

def create_momo_payment_with_options():
    """Create MoMo payment that should show Mobile Money options on Paystack"""
    print("🧪 Testing MoMo Options on Paystack Checkout")
    print("=" * 50)
    
    # Create MoMo payment with proper configuration
    momo_data = {
        'amount': 100.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0244123456',
        'description': 'Test MoMo Payment - Should show MoMo options'
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
            
            # Get payment details
            payment_ref = result.get('payment', {}).get('reference', '')
            auth_url = result.get('paystack', {}).get('authorization_url', '')
            
            print("✅ MoMo Payment Created Successfully")
            print(f"📱 Reference: {payment_ref}")
            print(f"🔗 Paystack URL: {auth_url}")
            print()
            
            # Show what user should expect
            print("🎯 What You Should See on Paystack Page:")
            print("   1. Mobile Money option (MTN, Vodafone, AirtelTigo)")
            print("   2. Card payment option (as fallback)")
            print("   3. Phone number pre-filled: 233244123456")
            print("   4. Amount: GHS 100.00")
            print()
            
            print("📱 Mobile Money Test Numbers (Ghana):")
            print("   MTN:        0244123456, 0244000000, 0244111111")
            print("   Vodafone:   0208123456, 0208000000")
            print("   AirtelTigo: 0278123456, 0278000000")
            print()
            
            print("💳 Or use test cards if MoMo not available:")
            print("   Success: 4084084084084081")
            print("   Decline: 4084084084084099")
            print("   CVV: 408, Expiry: 12/25")
            print()
            
            # Ask if user wants to open the URL
            try:
                open_browser = input("🌐 Open Paystack checkout in browser? (y/n): ").lower().strip()
                if open_browser in ['y', 'yes']:
                    webbrowser.open(auth_url)
                    print("✅ Opened in browser!")
                else:
                    print(f"📋 Copy this URL to test: {auth_url}")
            except:
                print(f"📋 Copy this URL to test: {auth_url}")
            
            return True, auth_url
            
        else:
            print("❌ Failed to create MoMo payment")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Request error: {e}")
        return False, None

def create_comparison_payments():
    """Create both MoMo and Card payments for comparison"""
    print("\n🔄 Creating Comparison Payments")
    print("=" * 50)
    
    payments = []
    
    # MoMo Payment
    momo_data = {
        'amount': 50.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0244123456',
        'description': 'MoMo Payment Test'
    }
    
    # Card Payment
    card_data = {
        'amount': 75.0,
        'email': 'test@example.com',
        'payment_method': 'card',
        'description': 'Card Payment Test'
    }
    
    for payment_type, data in [('MoMo', momo_data), ('Card', card_data)]:
        try:
            response = requests.post(
                'http://localhost:8000/api/payments/paystack/create/',
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                auth_url = result.get('paystack', {}).get('authorization_url', '')
                reference = result.get('payment', {}).get('reference', '')
                
                payments.append({
                    'type': payment_type,
                    'reference': reference,
                    'url': auth_url,
                    'amount': data['amount']
                })
                
                print(f"✅ {payment_type} Payment: {reference} - GHS {data['amount']}")
            else:
                print(f"❌ {payment_type} Payment Failed")
                
        except Exception as e:
            print(f"❌ {payment_type} Payment Error: {e}")
    
    return payments

def main():
    """Main test function"""
    print("🔧 MoMo Paystack Options Test")
    print("=" * 60)
    
    # Check server
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    # Test main MoMo payment
    success, url = create_momo_payment_with_options()
    
    if success:
        # Create comparison payments
        comparison_payments = create_comparison_payments()
        
        if comparison_payments:
            print("\n📋 All Test Payment URLs:")
            print("=" * 50)
            for payment in comparison_payments:
                print(f"{payment['type']:>4}: {payment['url']}")
        
        print("\n🎯 Testing Instructions:")
        print("   1. Open any URL above in your browser")
        print("   2. Look for Mobile Money options on Paystack page")
        print("   3. Try selecting MTN Mobile Money")
        print("   4. Enter a test phone number: 0244123456")
        print("   5. Complete the payment process")
        print("   6. Verify payment appears in Paystack dashboard")
        
        print("\n💡 Expected Results:")
        print("   ✅ MoMo URL should show Mobile Money options")
        print("   ✅ Card URL should show only card options")
        print("   ✅ Both should work and appear in dashboard")
    
    else:
        print("\n❌ Main test failed. Check the errors above.")

if __name__ == '__main__':
    main()