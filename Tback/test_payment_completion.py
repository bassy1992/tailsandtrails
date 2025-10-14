#!/usr/bin/env python
"""
Test the payment completion functionality
"""
import os
import sys
import django
import requests
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def test_complete_workflow():
    """Test the complete payment workflow"""
    print("Testing Complete Payment Workflow")
    print("=" * 40)
    
    # Step 1: Create a payment
    print("\n1. Creating a test payment...")
    
    payment_data = {
        'amount': 100.0,
        'currency': 'GHS',
        'payment_method': 'card',
        'email': 'test@example.com',
        'description': 'Test Payment Completion'
    }
    
    response = requests.post(
        'http://localhost:8000/api/payments/paystack/create/',
        headers={'Content-Type': 'application/json'},
        json=payment_data
    )
    
    if response.status_code != 201:
        print(f"Failed to create payment: {response.status_code}")
        return False
    
    result = response.json()
    payment_reference = result['payment']['reference']
    print(f"Payment created: {payment_reference}")
    
    # Step 2: Check initial status
    print(f"\n2. Checking initial payment status...")
    
    verify_response = requests.get(
        f'http://localhost:8000/api/payments/paystack/verify/{payment_reference}/'
    )
    
    if verify_response.status_code == 200:
        verify_data = verify_response.json()
        initial_status = verify_data['payment']['status']
        print(f"Initial status: {initial_status}")
    else:
        print("Failed to verify payment")
        return False
    
    # Step 3: Complete the payment using test endpoint
    print(f"\n3. Completing payment using test endpoint...")
    
    complete_response = requests.post(
        f'http://localhost:8000/api/payments/paystack/test-complete/{payment_reference}/'
    )
    
    if complete_response.status_code == 200:
        complete_data = complete_response.json()
        print(f"Completion result: {complete_data['message']}")
        print(f"New status: {complete_data['payment']['status']}")
    else:
        print(f"Failed to complete payment: {complete_response.status_code}")
        try:
            error_data = complete_response.json()
            print(f"Error: {error_data}")
        except:
            print(f"Raw response: {complete_response.text}")
        return False
    
    # Step 4: Verify final status
    print(f"\n4. Verifying final payment status...")
    
    final_verify_response = requests.get(
        f'http://localhost:8000/api/payments/paystack/verify/{payment_reference}/'
    )
    
    if final_verify_response.status_code == 200:
        final_verify_data = final_verify_response.json()
        final_status = final_verify_data['payment']['status']
        print(f"Final status: {final_status}")
        
        if final_status == 'successful':
            print("SUCCESS: Payment workflow completed successfully!")
            return True
        else:
            print(f"FAILED: Expected 'successful', got '{final_status}'")
            return False
    else:
        print("Failed to verify final payment status")
        return False

def test_mobile_money_workflow():
    """Test mobile money workflow"""
    print("\n\nTesting Mobile Money Workflow")
    print("=" * 35)
    
    # Create mobile money payment
    print("\n1. Creating mobile money payment...")
    
    momo_data = {
        'amount': 75.0,
        'currency': 'GHS',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '+233241234567',
        'email': 'test@example.com',
        'description': 'Test Mobile Money Completion'
    }
    
    response = requests.post(
        'http://localhost:8000/api/payments/paystack/create/',
        headers={'Content-Type': 'application/json'},
        json=momo_data
    )
    
    if response.status_code != 201:
        print(f"Failed to create mobile money payment: {response.status_code}")
        return False
    
    result = response.json()
    payment_reference = result['payment']['reference']
    print(f"Mobile money payment created: {payment_reference}")
    print(f"Display text: {result['paystack']['display_text']}")
    
    # Complete the payment
    print(f"\n2. Completing mobile money payment...")
    
    complete_response = requests.post(
        f'http://localhost:8000/api/payments/paystack/test-complete/{payment_reference}/'
    )
    
    if complete_response.status_code == 200:
        complete_data = complete_response.json()
        print(f"Mobile money completion: {complete_data['message']}")
        return True
    else:
        print(f"Failed to complete mobile money payment")
        return False

def main():
    """Main test function"""
    print("Payment Completion Test Suite")
    print("=" * 50)
    
    # Test card payment workflow
    card_success = test_complete_workflow()
    
    # Test mobile money workflow
    momo_success = test_mobile_money_workflow()
    
    # Summary
    print(f"\n" + "=" * 50)
    print(f"TEST RESULTS:")
    print(f"Card Payment Workflow: {'PASS' if card_success else 'FAIL'}")
    print(f"Mobile Money Workflow: {'PASS' if momo_success else 'FAIL'}")
    
    if card_success and momo_success:
        print(f"\nALL TESTS PASSED!")
        print(f"\nHow to use in your frontend:")
        print(f"1. Create payment normally")
        print(f"2. If payment shows as 'failed' in test mode:")
        print(f"   POST /api/payments/paystack/test-complete/{{reference}}/")
        print(f"3. Payment will be marked as 'successful'")
        print(f"4. User can proceed to success page")
    else:
        print(f"\nSome tests failed. Check the output above.")

if __name__ == '__main__':
    main()