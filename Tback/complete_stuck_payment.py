import requests
import json

def complete_stuck_payment():
    """Complete the most recent stuck payment"""
    
    print("🔧 Completing Stuck Payment")
    print("=" * 40)
    
    # Get the most recent processing payment
    try:
        import os
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
        django.setup()
        
        from payments.models import Payment
        
        recent_payments = Payment.objects.filter(status='processing').order_by('-created_at')[:5]
        
        if not recent_payments:
            print("❌ No processing payments found")
            return
        
        print("📋 Processing payments:")
        for i, payment in enumerate(recent_payments, 1):
            print(f"   {i}. {payment.reference}: {payment.description}")
        
        # Complete the most recent one
        payment = recent_payments[0]
        payment_ref = payment.reference
        
        print(f"\n🎯 Completing payment: {payment_ref}")
        
        # Use the API to complete the payment
        response = requests.post(
            f'http://localhost:8000/api/payments/{payment_ref}/complete/',
            json={"status": "successful"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Payment completed successfully!")
            print(f"   Status: {result['payment']['status']}")
            
            # Check if this was a ticket payment
            if "Ticket Purchase:" in payment.description:
                print("\n🎫 This was a ticket payment - the frontend should now:")
                print("   1. Detect the successful payment")
                print("   2. Create the ticket purchase")
                print("   3. Redirect to success page")
                print("   4. Show ticket codes")
        else:
            print(f"❌ Failed to complete payment: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Fallback: try to complete via direct API call
        print("\n🔄 Trying direct API approach...")
        
        # Get recent payments via API
        try:
            debug_response = requests.get('http://localhost:8000/api/payments/debug/')
            if debug_response.status_code == 200:
                debug_data = debug_response.json()
                recent = debug_data.get('recent_payments', [])
                
                processing_payments = [p for p in recent if p['status'] == 'processing']
                
                if processing_payments:
                    payment_ref = processing_payments[0]['reference']
                    print(f"Found processing payment: {payment_ref}")
                    
                    # Complete it
                    response = requests.post(
                        f'http://localhost:8000/api/payments/{payment_ref}/complete/',
                        json={"status": "successful"}
                    )
                    
                    if response.status_code == 200:
                        print("✅ Payment completed via API!")
                    else:
                        print(f"❌ API completion failed: {response.status_code}")
                else:
                    print("❌ No processing payments found via API")
        except Exception as api_error:
            print(f"❌ API approach failed: {api_error}")

def show_completion_instructions():
    """Show manual completion instructions"""
    
    print("\n" + "=" * 50)
    print("📱 MANUAL PAYMENT COMPLETION")
    print("=" * 50)
    
    print("\n🔧 If payment is still stuck, you can:")
    print("   1. Go to Django Admin: http://localhost:8000/admin/")
    print("   2. Navigate to Payments > Payments")
    print("   3. Find the processing payment")
    print("   4. Change status to 'successful'")
    print("   5. Save the payment")
    
    print("\n🚀 Or use the API directly:")
    print("   POST http://localhost:8000/api/payments/{REFERENCE}/complete/")
    print("   Body: {\"status\": \"successful\"}")
    
    print("\n⚡ Quick completion commands:")
    print("   python manage.py shell")
    print("   >>> from payments.models import Payment")
    print("   >>> p = Payment.objects.filter(status='processing').first()")
    print("   >>> p.status = 'successful'")
    print("   >>> p.save()")

if __name__ == "__main__":
    complete_stuck_payment()
    show_completion_instructions()