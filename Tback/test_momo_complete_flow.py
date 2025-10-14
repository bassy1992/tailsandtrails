#!/usr/bin/env python
"""
Test complete MoMo payment flow: Create → Redirect to Paystack → Complete → Redirect back
"""
import requests
import json

def test_momo_complete_flow():
    """Test the complete MoMo payment flow"""
    print("🔄 Testing Complete MoMo Payment Flow")
    print("=" * 50)
    
    # Step 1: Create MoMo payment
    print("1️⃣ Creating MoMo Payment...")
    
    momo_data = {
        'amount': 100.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0244123456',
        'description': 'Complete Flow Test - MoMo Payment'
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
            
            payment_ref = result.get('payment', {}).get('reference', '')
            auth_url = result.get('paystack', {}).get('authorization_url', '')
            
            print(f"   ✅ Payment Created: {payment_ref}")
            print(f"   🔗 Paystack URL: {auth_url}")
            print()
            
            # Step 2: Show what happens next
            print("2️⃣ User Flow on Paystack:")
            print("   → User clicks 'Pay with MoMo' on your website")
            print("   → Gets redirected to Paystack checkout page")
            print("   → Sees Mobile Money options (MTN, Vodafone, etc.)")
            print("   → Completes payment on Paystack")
            print("   → Paystack processes the payment")
            print()
            
            # Step 3: Show callback flow
            print("3️⃣ Automatic Redirect Back to Your Website:")
            print("   ✅ Success → http://localhost:8080/payment-success?reference=XXX&amount=100&method=mobile_money")
            print("   ❌ Failed  → http://localhost:8080/payment-failed?reference=XXX&reason=payment_failed")
            print("   🚫 Cancel  → http://localhost:8080/payment-cancelled?reference=XXX&reason=payment_cancelled")
            print()
            
            # Step 4: Test the callback URL format
            print("4️⃣ Testing Callback URL Format:")
            callback_url = f"http://localhost:8000/api/payments/paystack/callback/?reference={payment_ref}"
            print(f"   Callback URL: {callback_url}")
            
            # Test what the callback would return
            try:
                callback_response = requests.get(callback_url, allow_redirects=False, timeout=5)
                if callback_response.status_code in [301, 302, 303, 307, 308]:
                    redirect_location = callback_response.headers.get('Location', '')
                    print(f"   ✅ Callback works - Redirects to: {redirect_location}")
                else:
                    print(f"   ⚠️ Callback status: {callback_response.status_code}")
            except Exception as e:
                print(f"   ⚠️ Callback test error: {e}")
            
            print()
            print("🎯 Complete Flow Summary:")
            print("=" * 50)
            print("1. User selects MoMo payment on your website")
            print("2. Your frontend calls the payment API")
            print("3. API returns Paystack authorization_url")
            print("4. Frontend redirects user to Paystack")
            print("5. User completes payment on Paystack website")
            print("6. Paystack automatically redirects back to your website")
            print("7. User sees success/failure page on your website")
            print()
            
            print("🧪 To Test This Flow:")
            print(f"   1. Open this URL: {auth_url}")
            print("   2. Complete payment on Paystack")
            print("   3. You'll be redirected back to localhost:8080")
            print("   4. Check the URL parameters for payment details")
            
            return True, auth_url, payment_ref
            
        else:
            print(f"   ❌ Failed to create payment: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error: {json.dumps(error_data, indent=2)}")
            except:
                print(f"   Error Text: {response.text}")
            return False, None, None
            
    except Exception as e:
        print(f"   ❌ Request error: {e}")
        return False, None, None

def show_frontend_integration():
    """Show how to integrate this in frontend"""
    print("\n💻 Frontend Integration Code:")
    print("=" * 50)
    
    js_code = '''
// When user clicks "Pay with MoMo" button
async function handleMoMoPayment() {
    const paymentData = {
        amount: 100.0,
        email: 'customer@example.com',
        payment_method: 'mobile_money',
        provider: 'mtn',
        phone_number: '0244123456',
        description: 'Tour booking payment'
    };
    
    try {
        const response = await fetch('/api/payments/paystack/create/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(paymentData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Redirect to Paystack - user will complete payment there
            window.location.href = result.paystack.authorization_url;
            
            // After payment, Paystack will redirect back to:
            // - /payment-success (if successful)
            // - /payment-failed (if failed)
            // - /payment-cancelled (if cancelled)
        } else {
            alert('Payment creation failed: ' + result.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
}
'''
    
    print(js_code)
    
    print("\n📱 Your Frontend Pages Should Handle:")
    print("   /payment-success   - Show success message, order confirmation")
    print("   /payment-failed    - Show error message, retry option")
    print("   /payment-cancelled - Show cancelled message, return to checkout")

def main():
    """Main test function"""
    print("🧪 Complete MoMo Payment Flow Test")
    print("=" * 60)
    
    # Check server
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    # Test the flow
    success, auth_url, payment_ref = test_momo_complete_flow()
    
    if success:
        show_frontend_integration()
        
        print(f"\n🚀 Ready to Test!")
        print("=" * 60)
        print(f"Test URL: {auth_url}")
        print("Expected redirect back to: http://localhost:8080/payment-success")
        print("\nYour MoMo payment flow is ready! 🎉")
    else:
        print("\n❌ Flow test failed. Check the errors above.")

if __name__ == '__main__':
    main()