#!/usr/bin/env python
"""
Debug script to identify MTN MoMo issues
"""
import requests
import json
import sys
from datetime import datetime

def check_server_status():
    """Check if Django server is running"""
    print("🔍 Checking Server Status...")
    
    try:
        response = requests.get('http://localhost:8000/api/payments/methods/', timeout=5)
        print(f"✅ Server is running - Status: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running or not accessible")
        print("   Please start the Django server: python manage.py runserver 8000")
        return False
    except Exception as e:
        print(f"❌ Server check error: {e}")
        return False

def test_paystack_endpoint():
    """Test the Paystack endpoint directly"""
    print("\n💳 Testing Paystack Endpoint...")
    
    test_data = {
        'amount': 50.0,
        'email': 'test@example.com',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '0244123456',
        'description': 'Debug test payment'
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Paystack endpoint working")
            print(f"Payment Reference: {result.get('payment', {}).get('reference')}")
            return True, result
        else:
            print(f"❌ Paystack endpoint failed")
            try:
                error_data = response.json()
                print(f"Error Response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Paystack endpoint error: {e}")
        return False, None

def test_frontend_request():
    """Test with exact frontend request format"""
    print("\n🎨 Testing Frontend Request Format...")
    
    # Simulate exact frontend request from MomoCheckout
    frontend_data = {
        'amount': 100.0,
        'currency': 'GHS',
        'payment_method': 'mobile_money',
        'provider': 'mtn',
        'phone_number': '+233244123456',
        'email': 'customer@example.com',
        'description': 'Tour Booking Payment',
        'booking_details': {
            'tourName': 'Cape Coast Castle Tour',
            'total': 100.0
        }
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/paystack/create/',
            json=frontend_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ Frontend format working")
            print(f"Payment Reference: {result.get('payment', {}).get('reference')}")
            
            # Test the paystack response format
            if result.get('paystack'):
                print("✅ Paystack response included")
                paystack_data = result.get('paystack', {})
                print(f"Display Text: {paystack_data.get('display_text', 'N/A')}")
                print(f"Test Mode: {paystack_data.get('test_mode', False)}")
            else:
                print("⚠️ No paystack response data")
            
            return True, result
        else:
            print(f"❌ Frontend format failed")
            try:
                error_data = response.json()
                print(f"Error Response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Frontend request error: {e}")
        return False, None

def test_verification():
    """Test payment verification"""
    print("\n🔍 Testing Payment Verification...")
    
    # First create a payment
    success, result = test_paystack_endpoint()
    if not success or not result:
        print("❌ Cannot test verification - payment creation failed")
        return False
    
    payment_ref = result.get('payment', {}).get('reference')
    if not payment_ref:
        print("❌ No payment reference to verify")
        return False
    
    try:
        verify_response = requests.get(
            f'http://localhost:8000/api/payments/paystack/verify/{payment_ref}/',
            timeout=10
        )
        
        print(f"Verification Status: {verify_response.status_code}")
        
        if verify_response.status_code == 200:
            verify_result = verify_response.json()
            print("✅ Payment verification working")
            
            payment_status = verify_result.get('payment', {}).get('status')
            print(f"Payment Status: {payment_status}")
            
            return True
        else:
            print(f"❌ Verification failed")
            try:
                error_data = verify_response.json()
                print(f"Error Response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error Text: {verify_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def check_console_errors():
    """Check for common console errors"""
    print("\n🐛 Common Issues Checklist...")
    
    issues = []
    
    # Check server
    if not check_server_status():
        issues.append("Django server not running")
    
    # Check if using correct port
    print("📍 Port Check:")
    print("   - Backend should be: http://localhost:8000")
    print("   - Frontend should be: http://localhost:8080")
    print("   - Make sure you're accessing the correct port")
    
    # Check browser console
    print("\n🌐 Browser Console Check:")
    print("   1. Open browser developer tools (F12)")
    print("   2. Go to Console tab")
    print("   3. Try the payment and look for errors")
    print("   4. Common errors:")
    print("      - CORS errors")
    print("      - Network errors")
    print("      - 404 Not Found")
    print("      - 500 Internal Server Error")
    
    # Check network tab
    print("\n📡 Network Tab Check:")
    print("   1. Open Network tab in developer tools")
    print("   2. Try the payment")
    print("   3. Look for failed requests (red entries)")
    print("   4. Check request/response details")
    
    return len(issues) == 0

def main():
    """Run comprehensive debug"""
    print("🔧 MTN MoMo Debug Session")
    print("=" * 50)
    
    # Run tests
    tests = [
        ("Server Status", check_server_status),
        ("Paystack Endpoint", lambda: test_paystack_endpoint()[0]),
        ("Frontend Format", lambda: test_frontend_request()[0]),
        ("Payment Verification", test_verification),
    ]
    
    results = {}
    for test_name, test_func in tests:
        print()
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Debug Results")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:.<25} {status}")
    
    # Recommendations
    print("\n🔧 Troubleshooting Steps:")
    
    if not results.get("Server Status"):
        print("1. Start Django server:")
        print("   cd tailsandtrails-master/Tback")
        print("   python manage.py runserver 8000")
    
    if not results.get("Paystack Endpoint"):
        print("2. Check Paystack configuration:")
        print("   - Verify .env file has correct keys")
        print("   - Check Django logs for errors")
    
    print("\n3. Check browser:")
    print("   - Use correct URL: http://localhost:8080/momo-checkout")
    print("   - Open developer tools and check console/network")
    print("   - Clear browser cache if needed")
    
    print("\n4. Test step by step:")
    print("   - Try http://localhost:8080/test-momo first")
    print("   - If that works, try the main checkout")
    
    # Specific error scenarios
    print("\n❓ If you see specific errors:")
    print("   - 'Connection refused' → Server not running")
    print("   - '404 Not Found' → Wrong URL or route")
    print("   - '500 Internal Error' → Check Django logs")
    print("   - 'CORS error' → Check CORS settings")
    print("   - Payment hangs → Check network tab for failed requests")

if __name__ == '__main__':
    main()