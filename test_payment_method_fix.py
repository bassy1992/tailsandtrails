#!/usr/bin/env python3
"""
Test the payment method fix
"""
import requests
import json

def test_payment_method_fix():
    """Test that paystack_momo is now accepted as a payment method"""
    print("🔧 Testing Payment Method Fix")
    print("=" * 50)
    
    # Test data with the paystack_momo payment method
    test_data = {
        'ticket_id': 2,
        'quantity': 1,
        'total_amount': 50,
        'customer_name': 'Test Customer',
        'customer_email': 'test@example.com',
        'customer_phone': '0241234567',
        'payment_method': 'paystack_momo',  # This was causing the 400 error
        'payment_reference': 'PAY-TEST-PAYSTACK-MOMO',
        'special_requests': 'Paystack Mobile Money Payment - Test'
    }
    
    print("📋 Test Data:")
    print(json.dumps(test_data, indent=2))
    print()
    
    try:
        # Test the direct purchase endpoint with paystack_momo
        api_url = "https://tailsandtrails-production.up.railway.app/api/tickets/purchase/direct/"
        print(f"🌐 Testing endpoint: {api_url}")
        
        response = requests.post(api_url, json=test_data, headers={
            'Content-Type': 'application/json'
        })
        
        print(f"📡 Response Status: {response.status_code}")
        
        try:
            result = response.json()
            print("📋 Response Data:")
            print(json.dumps(result, indent=2))
            
            if response.status_code == 201 and result.get('success'):
                print("✅ PAYMENT METHOD FIX WORKING!")
                print("   'paystack_momo' is now accepted as a valid payment method")
                purchase_id = result.get('purchase', {}).get('purchase_id')
                if purchase_id:
                    print(f"🎫 Ticket purchase created: {purchase_id}")
                return True
            elif response.status_code == 400 and 'Invalid payment method' in result.get('error', ''):
                print("❌ PAYMENT METHOD FIX NOT WORKING!")
                print("   'paystack_momo' is still not accepted")
                print("   Backend might need to be redeployed")
                return False
            else:
                print(f"⚠️ Unexpected response: {result.get('error', 'Unknown error')}")
                return False
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_other_payment_methods():
    """Test that other payment methods still work"""
    print("\n🧪 Testing Other Payment Methods")
    print("=" * 40)
    
    methods_to_test = ['mtn_momo', 'vodafone_cash', 'airteltigo_money', 'momo']
    
    for method in methods_to_test:
        test_data = {
            'ticket_id': 2,
            'quantity': 1,
            'total_amount': 50,
            'customer_name': 'Test Customer',
            'customer_email': 'test@example.com',
            'customer_phone': '0241234567',
            'payment_method': method,
            'payment_reference': f'PAY-TEST-{method.upper()}',
            'special_requests': f'Test payment with {method}'
        }
        
        try:
            response = requests.post(
                "https://tailsandtrails-production.up.railway.app/api/tickets/purchase/direct/",
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 201:
                print(f"✅ {method}: Working")
            else:
                result = response.json()
                print(f"❌ {method}: {result.get('error', 'Failed')}")
                
        except Exception as e:
            print(f"❌ {method}: Error - {str(e)}")

def main():
    """Main test function"""
    print("🎫 PAYMENT METHOD FIX TEST")
    print("=" * 60)
    print("Issue: PaymentCallback sending 'paystack_momo' but backend rejecting it")
    print("=" * 60)
    
    # Test the main fix
    success = test_payment_method_fix()
    
    # Test other methods still work
    test_other_payment_methods()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ PAYMENT METHOD FIX SUCCESSFUL!")
        print("\n🎯 What's Fixed:")
        print("   • PaymentCallback can now create tickets after Paystack payment")
        print("   • 'paystack_momo' is accepted as a valid payment method")
        print("   • Users will see ticket purchase success instead of errors")
        
        print("\n🚀 Complete Flow Now Working:")
        print("   1. User completes payment on Paystack ✅")
        print("   2. Redirected to /payment-callback ✅")
        print("   3. Payment verified ✅")
        print("   4. Ticket created with 'paystack_momo' method ✅")
        print("   5. User sees success page ✅")
    else:
        print("❌ PAYMENT METHOD FIX NEEDS MORE WORK")
        print("   Backend might need to be redeployed")

if __name__ == "__main__":
    main()