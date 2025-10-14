import requests
import json
import time

def test_ticket_signal_fix():
    """Test that the signal correctly creates ticket details for ticket payments"""
    
    print("🎫 Testing Ticket Signal Fix")
    print("=" * 40)
    
    # Get a ticket to purchase
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    ticket = tickets_response.json()[0]
    
    print(f"🎫 Creating ticket payment for: {ticket['title']}")
    
    # Create a ticket payment with proper description
    payment_data = {
        "amount": float(ticket['price']),
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": f"Ticket Purchase: {ticket['title']}",  # This should trigger ticket handling
        "booking_details": {
            "type": "ticket",
            "ticket_id": ticket['id'],
            "ticket_title": ticket['title'],
            "customer_name": "Signal Test User",
            "customer_email": "signaltest@example.com"
        }
    }
    
    payment_response = requests.post(
        'http://localhost:8000/api/payments/checkout/create/',
        json=payment_data
    )
    
    if payment_response.status_code == 201:
        payment_result = payment_response.json()
        payment_ref = payment_result['payment']['reference']
        print(f"✅ Ticket payment created: {payment_ref}")
        
        # Wait a moment for the signal to process
        print("⏰ Waiting for signal processing...")
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
            
            # Check if metadata has ticket details
            if payment.metadata and 'booking_details' in payment.metadata:
                booking_details = payment.metadata['booking_details']
                print(f"📊 Booking details type: {booking_details.get('type', 'unknown')}")
                
                if booking_details.get('type') == 'ticket':
                    print("✅ SUCCESS: Signal created ticket-specific details!")
                    ticket_info = booking_details.get('ticket', {})
                    print(f"   🎫 Ticket name: {ticket_info.get('name', 'N/A')}")
                    print(f"   💰 Ticket price: {ticket_info.get('price', 'N/A')}")
                    print(f"   🎟️ Quantity: {ticket_info.get('quantity', 'N/A')}")
                else:
                    print(f"❌ ISSUE: Signal created wrong type: {booking_details.get('type', 'unknown')}")
                    print(f"   Details: {json.dumps(booking_details, indent=2)}")
            else:
                print("❌ ISSUE: No booking details in metadata")
                
            # Check if booking record was created (should NOT be for tickets)
            if payment.booking:
                print(f"⚠️  WARNING: Booking record created for ticket payment")
            else:
                print("✅ CORRECT: No booking record for ticket payment")
                
        except Exception as e:
            print(f"❌ Error checking payment details: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ Payment creation failed: {payment_response.text}")
    
    print("\n" + "=" * 50)
    print("🎯 SIGNAL FIX SUMMARY")
    print("=" * 50)
    print("✅ What should be working now:")
    print("   - Ticket payments get ticket-specific metadata")
    print("   - Destination payments get destination metadata")
    print("   - Admin shows correct booking type")
    print("   - No booking records for tickets")
    
    print("\n🔍 Check admin panels:")
    print("   - Payments: http://localhost:8000/admin/payments/payment/")
    print("   - Look for the new payment with '🎫 TICKET' label")

if __name__ == "__main__":
    test_ticket_signal_fix()