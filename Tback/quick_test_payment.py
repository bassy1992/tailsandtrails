#!/usr/bin/env python
"""
Quick test to create a payment and check if daemon completes it
"""
import requests
import json
import time

def quick_test():
    # Create payment
    data = {
        "amount": "45.00",
        "currency": "GHS", 
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Quick daemon test"
    }
    
    response = requests.post('http://localhost:8000/api/payments/checkout/create/', json=data)
    
    if response.status_code == 201:
        result = response.json()
        payment_ref = result['payment']['reference']
        print(f"✅ Payment created: {payment_ref}")
        print("⏰ Daemon should complete this in ~20 seconds...")
        
        # Check status after 25 seconds
        time.sleep(25)
        status_response = requests.get(f'http://localhost:8000/api/payments/{payment_ref}/status/')
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"📊 Final status: {status_data['status']}")
            if status_data['status'] in ['successful', 'failed']:
                print("🎉 Daemon auto-completion worked!")
            else:
                print("⚠️ Still processing - daemon might need more time")
        else:
            print("❌ Error checking status")
    else:
        print(f"❌ Failed to create payment: {response.text}")

if __name__ == "__main__":
    quick_test()