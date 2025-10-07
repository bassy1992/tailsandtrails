import requests
import json
import time

def test_destination_payment():
    """Test that destination payments still work correctly"""
    
    print("🏝️ Testing Destination Payment")
    print("=" * 40)
    
    # Create a destination payment (no ticket description)
    payment_data = {
        "amount": 1500.00,
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": "Cape Coast Castle Heritage Tour",  # No "Ticket Purchase:" prefix
        "booking_details": {
            "type": "destination",  # Explicitly destination
            "destination_name": "Cape Coast Castle Heritage Tour",
            "destination_location": "Cape Coast, Ghana",
            "customer_name": "Destination Test User",
            "customer_email": "desttest@example.com"
        }
    }
    
    payment_response = requests.post(
        'http://localhost:8000/api/payments/checkout/create/',
        json=payment_data
    )
    
    if payment_response.status_code == 201:
        payment_result = payment_response.json()
        payment_ref = payment_result['payment']['reference']
        print(f"✅ Destination payment created: {payment_ref}")
        
        # Wait a moment for processing
        print("⏰ Waiting for processing...")
        time.sleep(2)
        
        # Check the payment details using Django ORM
        try:
            import os
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
            django.setup()
            
            from payments.models import Payment
            from payments.admin import PaymentAdmin
            from django.contrib.admin.sites import AdminSite
            
            payment = Payment.objects.get(reference=payment_ref)
            admin = PaymentAdmin(Payment, AdminSite())
            
            # Check booking type display
            booking_type = admin.booking_type_display(payment)
            print(f"📋 Booking type display: {booking_type}")
            
            # Check if metadata has destination details
            if payment.metadata and 'booking_details' in payment.metadata:
                booking_details = payment.metadata['booking_details']
                print(f"📊 Booking details type: {booking_details.get('type', 'unknown')}")
                
                if 'destination' in booking_details:
                    print("✅ SUCCESS: Has destination-specific details!")
                    dest_info = booking_details.get('destination', {})
                    print(f"   🏝️ Destination name: {dest_info.get('name', 'N/A')}")
                    print(f"   📍 Location: {dest_info.get('location', 'N/A')}")
                    print(f"   ⏱️ Duration: {dest_info.get('duration', 'N/A')}")
                else:
                    print(f"❌ ISSUE: No destination details found")
                    print(f"   Details keys: {list(booking_details.keys())}")
            else:
                print("❌ ISSUE: No booking details in metadata")
                
        except Exception as e:
            print(f"❌ Error checking payment details: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Payment creation failed: {payment_response.text}")
    
    print("\n" + "=" * 40)
    print("🎯 DESTINATION TEST COMPLETE")

if __name__ == "__main__":
    test_destination_payment()