import requests
import json

def test_payment_method_validation():
    """Test payment method validation directly"""
    
    print("🔧 TESTING PAYMENT METHOD VALIDATION")
    print("=" * 50)
    
    # Test with a non-existent ticket ID to focus on payment method validation
    test_cases = [
        {
            'payment_method': 'mtn_momo',
            'expected': 'Should work (if ticket exists)',
            'should_pass_validation': True
        },
        {
            'payment_method': 'mtn_mobile_money', 
            'expected': 'Should fail - Invalid payment method',
            'should_pass_validation': False
        },
        {
            'payment_method': 'vodafone_cash',
            'expected': 'Should work (if ticket exists)',
            'should_pass_validation': True
        },
        {
            'payment_method': 'airteltigo_money',
            'expected': 'Should work (if ticket exists)',
            'should_pass_validation': True
        },
        {
            'payment_method': 'stripe',
            'expected': 'Should work (if ticket exists)',
            'should_pass_validation': True
        },
        {
            'payment_method': 'invalid_method',
            'expected': 'Should fail - Invalid payment method',
            'should_pass_validation': False
        }
    ]
    
    for test_case in test_cases:
        payment_method = test_case['payment_method']
        expected = test_case['expected']
        should_pass = test_case['should_pass_validation']
        
        print(f"\n🧪 Testing: '{payment_method}'")
        print(f"   Expected: {expected}")
        print("-" * 40)
        
        purchase_data = {
            "ticket_id": 999,  # Non-existent ticket ID
            "quantity": 1,
            "total_amount": 100.00,
            "customer_name": "Test User",
            "customer_email": "test@example.com",
            "customer_phone": "+233244123456",
            "payment_method": payment_method,
            "payment_reference": f"TEST-{payment_method.upper()}-123",
            "special_requests": f"Testing payment method: {payment_method}"
        }
        
        response = requests.post(
            'http://localhost:8000/api/tickets/purchase/direct/',
            json=purchase_data
        )
        
        print(f"   Status Code: {response.status_code}")
        
        try:
            result = response.json()
            error_message = result.get('error', 'No error message')
            
            if response.status_code == 400:
                if 'Invalid payment method' in error_message:
                    if not should_pass:
                        print(f"   ✅ CORRECT: Invalid payment method rejected")
                    else:
                        print(f"   ❌ UNEXPECTED: Valid payment method rejected")
                elif 'not found' in error_message.lower() or 'does not exist' in error_message.lower():
                    if should_pass:
                        print(f"   ✅ CORRECT: Payment method accepted, ticket not found (as expected)")
                    else:
                        print(f"   ❌ UNEXPECTED: Should have failed at payment method validation")
                else:
                    print(f"   ⚠️  OTHER ERROR: {error_message}")
            elif response.status_code == 201:
                print(f"   ✅ SUCCESS: {result.get('message', 'No message')}")
            else:
                print(f"   ❌ UNEXPECTED STATUS: {response.status_code}")
                print(f"      Response: {result}")
                
        except json.JSONDecodeError:
            print(f"   ❌ JSON DECODE ERROR")
            print(f"      Raw Response: {response.text}")
    
    print(f"\n" + "=" * 50)
    print(f"🎯 PAYMENT METHOD VALIDATION TEST COMPLETE")
    print(f"=" * 50)
    print(f"✅ The frontend should use these payment method codes:")
    print(f"   • MTN Mobile Money → 'mtn_momo'")
    print(f"   • Vodafone Cash → 'vodafone_cash'")
    print(f"   • AirtelTigo Money → 'airteltigo_money'")
    print(f"   • Stripe → 'stripe'")
    print(f"❌ NOT: 'mtn_mobile_money' (this causes the error)")

if __name__ == "__main__":
    test_payment_method_validation()