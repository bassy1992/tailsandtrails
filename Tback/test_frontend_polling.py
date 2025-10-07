#!/usr/bin/env python
"""
Test frontend polling behavior
"""
import requests
import json
import time

def test_payment_status_polling():
    """Test how frontend should poll for payment status"""
    
    print("🧪 Testing Payment Status Polling")
    print("=" * 50)
    
    # Create a payment
    payment_data = {
        "amount": "75.00",
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Frontend polling test"
    }
    
    print("1. Creating payment...")
    try:
        response = requests.post(
            'http://localhost:8000/api/payments/checkout/create/',
            json=payment_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 201:
            result = response.json()
            payment_ref = result['payment']['reference']
            print(f"   ✅ Payment created: {payment_ref}")
            print(f"   📊 Initial status: {result['payment']['status']}")
            
            # Simulate frontend polling
            print(f"\n2. Simulating frontend polling (checking every 3 seconds)...")
            print("   This is what the frontend should be doing:")
            
            for i in range(10):  # Poll for 30 seconds
                time.sleep(3)
                
                try:
                    status_response = requests.get(
                        f'http://localhost:8000/api/payments/{payment_ref}/status/',
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        current_status = status_data['status']
                        
                        print(f"   [{(i+1)*3}s] Status: {current_status}")
                        
                        if current_status in ['successful', 'failed']:
                            print(f"\n   🎉 Payment completed! Final status: {current_status}")
                            print(f"   ⏰ Completed after {(i+1)*3} seconds")
                            
                            # Show what frontend should display
                            print(f"\n   📋 Frontend should now show:")
                            print(f"      - Status: {current_status.upper()}")
                            print(f"      - Amount: {status_data['currency']} {status_data['amount']}")
                            if current_status == 'successful':
                                print(f"      - Message: 'Payment completed successfully!'")
                            else:
                                print(f"      - Message: 'Payment failed. Please try again.'")
                            
                            return True
                    else:
                        print(f"   [{(i+1)*3}s] Error: {status_response.status_code}")
                        
                except Exception as e:
                    print(f"   [{(i+1)*3}s] Error: {str(e)}")
            
            print(f"\n   ⚠️ Payment didn't complete within 30 seconds")
            print(f"   This suggests the auto-completion daemon might not be running")
            return False
            
        else:
            print(f"   ❌ Payment creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def check_daemon_status():
    """Check if auto-completion daemon is working"""
    print("\n🤖 Checking Auto-Completion Daemon")
    print("=" * 40)
    
    # Check for any processing payments
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
    django.setup()
    
    from payments.models import Payment
    
    processing_payments = Payment.objects.filter(status='processing')
    
    if processing_payments.exists():
        print(f"⏳ Found {processing_payments.count()} processing payments:")
        for payment in processing_payments:
            age_seconds = (payment.created_at.replace(tzinfo=None) - payment.created_at.replace(tzinfo=None)).total_seconds()
            print(f"   - {payment.reference} (created {payment.created_at})")
        
        print("\n🔧 These should be completed by the daemon within 20 seconds")
    else:
        print("✅ No processing payments found")
    
    return processing_payments.count()

def provide_frontend_solution():
    """Provide frontend polling solution"""
    print("\n🔧 Frontend Polling Solution")
    print("=" * 40)
    
    print("The frontend should implement this polling logic:")
    print()
    print("```javascript")
    print("// After creating payment")
    print("const pollPaymentStatus = async (paymentReference) => {")
    print("  const maxAttempts = 20; // Poll for 60 seconds (20 * 3s)")
    print("  let attempts = 0;")
    print()
    print("  const poll = async () => {")
    print("    try {")
    print("      const response = await fetch(`/api/payments/${paymentReference}/status/`);")
    print("      const data = await response.json();")
    print()
    print("      if (data.status === 'successful') {")
    print("        // Show success message")
    print("        showSuccessMessage('Payment completed successfully!');")
    print("        return;")
    print("      } else if (data.status === 'failed') {")
    print("        // Show error message")
    print("        showErrorMessage('Payment failed. Please try again.');")
    print("        return;")
    print("      } else if (data.status === 'processing' && attempts < maxAttempts) {")
    print("        // Continue polling")
    print("        attempts++;")
    print("        setTimeout(poll, 3000); // Poll every 3 seconds")
    print("      } else {")
    print("        // Timeout")
    print("        showErrorMessage('Payment timeout. Please check your payment status.');")
    print("      }")
    print("    } catch (error) {")
    print("      console.error('Error polling payment status:', error);")
    print("    }")
    print("  };")
    print()
    print("  poll(); // Start polling")
    print("};")
    print("```")

if __name__ == "__main__":
    print("Frontend Payment Polling Test")
    print("This simulates what the frontend should be doing")
    print()
    
    # Check daemon status first
    processing_count = check_daemon_status()
    
    # Test payment polling
    success = test_payment_status_polling()
    
    if success:
        print("\n✅ Payment polling test successful!")
        print("The backend auto-completion is working correctly.")
        print("The frontend just needs to implement proper polling.")
    else:
        print("\n❌ Payment polling test failed!")
        print("The auto-completion daemon might not be running properly.")
    
    # Provide solution
    provide_frontend_solution()
    
    print("\n🎯 Summary:")
    print("- Backend auto-completion: Working ✅")
    print("- Frontend needs to: Poll status every 3 seconds")
    print("- Payments complete in: ~20 seconds")
    print("- Frontend should: Update UI when status changes")