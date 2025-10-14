#!/usr/bin/env python
"""
Test MoMo payments with different scenarios
"""
import requests
import json

def create_test_payment(scenario="success"):
    """Create a test MoMo payment"""
    
    scenarios = {
        "success": {
            "amount": 100.0,
            "description": "Test MoMo Payment - Success Scenario"
        },
        "decline": {
            "amount": 50.0,
            "description": "Test MoMo Payment - Decline Scenario"
        },
        "insufficient": {
            "amount": 200.0,
            "description": "Test MoMo Payment - Insufficient Funds"
        }
    }
    
    payment_data = {
        'amount': scenarios[scenario]['amount'],
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0244123456',
        'description': scenarios[scenario]['description']
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=payment_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            auth_url = result.get('paystack', {}).get('authorization_url', '')
            reference = result.get('payment', {}).get('reference', '')
            
            print(f"✅ {scenario.upper()} Payment Created")
            print(f"   Reference: {reference}")
            print(f"   Amount: GHS {payment_data['amount']}")
            print(f"   Redirect URL: {auth_url}")
            print()
            
            return {
                'success': True,
                'reference': reference,
                'url': auth_url,
                'scenario': scenario
            }
        else:
            print(f"❌ Failed to create {scenario} payment")
            return {'success': False}
            
    except Exception as e:
        print(f"❌ Error creating {scenario} payment: {e}")
        return {'success': False}

def print_test_instructions():
    """Print test instructions"""
    print("🧪 MoMo Payment Test Instructions")
    print("=" * 50)
    print()
    print("📱 Test Card Numbers for Paystack:")
    print("   SUCCESS:     4084084084084081")
    print("   DECLINE:     4084084084084099") 
    print("   INSUFFICIENT: 4084084084084107")
    print("   CVV:         408")
    print("   EXPIRY:      12/25 (any future date)")
    print()
    print("🔄 Testing Process:")
    print("   1. Run this script to create test payments")
    print("   2. Copy the redirect URL and open in browser")
    print("   3. Use the test card numbers above")
    print("   4. Complete payment on Paystack")
    print("   5. Check Paystack dashboard for results")
    print()

def main():
    """Main test function"""
    print_test_instructions()
    
    # Check server
    try:
        requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Start with: python manage.py runserver")
        return
    
    print("\n🚀 Creating Test Payments...")
    print("=" * 50)
    
    # Create different test scenarios
    scenarios = ['success', 'decline', 'insufficient']
    results = []
    
    for scenario in scenarios:
        result = create_test_payment(scenario)
        if result['success']:
            results.append(result)
    
    # Summary
    print("📋 Test Payment URLs:")
    print("=" * 50)
    for result in results:
        print(f"{result['scenario'].upper():>12}: {result['url']}")
    
    print("\n💡 Next Steps:")
    print("   1. Copy any URL above and open in browser")
    print("   2. You'll see Paystack checkout page")
    print("   3. Enter test card details:")
    print("      - For SUCCESS: 4084084084084081")
    print("      - For DECLINE: 4084084084084099")
    print("   4. Complete payment and verify in dashboard")

if __name__ == '__main__':
    main()