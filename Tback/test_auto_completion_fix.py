#!/usr/bin/env python
"""
Test the auto-completion fix
"""
import requests
import json
import time

def test_auto_completion():
    """Test if auto-completion works for new payments"""
    
    print("🧪 Testing Auto-Completion Fix")
    print("=" * 40)
    
    # Create a payment
    payment_data = {
        "amount": "35.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Test auto-completion fix"
    }
    
    try:
        print("1. Creating payment...")
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/', 
            json=payment_data
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"   ✅ Payment created: {payment_ref}")
            print(f"   📊 Status: {result['payment']['status']}")
            
            print(f"\n2. Monitoring auto-completion (35 seconds)...")
            print("   This should complete automatically after 30 seconds...")
            
            # Monitor for 35 seconds
            for i in range(7):  # Check every 5 seconds for 35 seconds
                time.sleep(5)
                try:
                    status_response = requests.get(f'http://localhost:8000/api/payments/{payment_ref}/status/')
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        current_status = status_data['status']
                        print(f"   [{(i+1)*5}s] Status: {current_status}")
                        
                        if current_status in ['successful', 'failed']:
                            print(f"   🎉 Auto-completion worked! Final status: {current_status}")
                            return True
                    else:
                        print(f"   [{(i+1)*5}s] Error checking status: {status_response.status_code}")
                except Exception as e:
                    print(f"   [{(i+1)*5}s] Error: {str(e)}")
            
            print("   ⚠️ Auto-completion didn't work within 35 seconds")
            return False
            
        else:
            print(f"   ❌ Failed to create payment: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_auto_completion()
    
    if not success:
        print("\n🔧 Manual Fix Options:")
        print("1. Complete stuck payments manually:")
        print("   python manage.py auto_complete_demo_payments --timeout 0")
        print("2. Or complete specific payment:")
        print("   python simple_auto_complete.py <payment_reference> 0 1.0")
        print("3. Check Django logs for auto-completion errors")