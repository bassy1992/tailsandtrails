import requests
import json

def test_vip_ticket_fix():
    """Test the VIP ticket purchase fix"""
    
    print("🎫 TESTING VIP TICKET PURCHASE FIX")
    print("=" * 50)
    
    # Get the Ghana Cultural Festival ticket
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    if tickets_response.status_code != 200:
        print("❌ Failed to get tickets")
        return
    
    tickets = tickets_response.json()
    ticket = None
    for t in tickets:
        if t['title'] == 'Ghana Cultural Festival 2025':
            ticket = t
            break
    
    if not ticket:
        print("❌ Ghana Cultural Festival 2025 ticket not found")
        return
    
    print(f"🎫 Testing with ticket: {ticket['title']}")
    print(f"   Base Price: GH₵{ticket['price']}")
    print(f"   ID: {ticket['id']}")
    
    # Calculate VIP price (base price * 1.8)
    base_price = float(ticket['price'])
    vip_price = round(base_price * 1.8)
    
    print(f"   VIP Price: GH₵{vip_price} (base * 1.8)")
    
    # Test 1: Create payment with VIP price
    print(f"\n1️⃣ CREATING PAYMENT WITH VIP PRICE")
    print("-" * 30)
    
    payment_data = {
        "amount": vip_price,
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": f"Ticket Purchase: {ticket['title']} (1 tickets)",
        "booking_details": {
            "type": "ticket",
            "ticket_id": ticket['id'],
            "ticket_title": ticket['title'],
            "ticket_type": "vip",
            "customer_name": "VIP Test Customer",
            "customer_email": "viptest@example.com"
        }
    }
    
    payment_response = requests.post(
        'http://localhost:8000/api/payments/checkout/create/',
        json=payment_data
    )
    
    if payment_response.status_code != 201:
        print(f"❌ Payment creation failed: {payment_response.text}")
        return
    
    payment_result = payment_response.json()
    payment_ref = payment_result['payment']['reference']
    print(f"✅ Payment created: {payment_ref}")
    print(f"   Amount: GH₵{payment_result['payment']['amount']}")
    
    # Wait for payment to complete
    print("⏰ Waiting for payment completion...")
    import time
    time.sleep(6)  # Ticket payments auto-complete in 5 seconds
    
    # Check payment status
    status_response = requests.get(f'http://localhost:8000/api/payments/{payment_ref}/status/')
    status_result = status_response.json()
    print(f"💳 Payment Status: {status_result['status']}")
    
    if status_result['status'] != 'successful':
        print("❌ Payment not successful, cannot proceed")
        return
    
    # Test 2: Create ticket purchase with VIP price
    print(f"\n2️⃣ CREATING TICKET PURCHASE WITH VIP PRICE")
    print("-" * 30)
    
    purchase_data = {
        "ticket_id": ticket['id'],
        "quantity": 1,
        "total_amount": vip_price,  # Pass the VIP price
        "customer_name": "VIP Test Customer",
        "customer_email": "viptest@example.com",
        "customer_phone": "+233244123456",
        "payment_method": "mtn_momo",
        "payment_reference": payment_ref,  # Link to the actual payment
        "special_requests": "VIP ticket purchase test"
    }
    
    purchase_response = requests.post(
        'http://localhost:8000/api/tickets/purchase/direct/',
        json=purchase_data
    )
    
    print(f"📥 Purchase Response:")
    print(f"   Status Code: {purchase_response.status_code}")
    
    if purchase_response.status_code == 201:
        result = purchase_response.json()
        if result.get('success'):
            purchase = result['purchase']
            print(f"\n✅ SUCCESS!")
            print(f"   Purchase ID: {purchase['purchase_id']}")
            print(f"   Status: {purchase['status']}")
            print(f"   Payment Status: {purchase['payment_status']}")
            print(f"   Unit Price: GH₵{purchase['unit_price']}")
            print(f"   Total Amount: GH₵{purchase['total_amount']}")
            print(f"   Payment Reference: {purchase['payment_reference']}")
            
            # Check if amounts match
            if float(purchase['total_amount']) == vip_price:
                print(f"   ✅ AMOUNT MATCH: Purchase amount matches VIP price!")
            else:
                print(f"   ❌ AMOUNT MISMATCH: Expected {vip_price}, got {purchase['total_amount']}")
                
            # Check ticket codes
            codes = purchase.get('ticket_codes', [])
            print(f"   🎫 Ticket Codes: {len(codes)} generated")
            
        else:
            print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP ERROR: {purchase_response.status_code}")
        print(f"   Response: {purchase_response.text}")
    
    # Test 3: Verify in database
    print(f"\n3️⃣ VERIFYING IN DATABASE")
    print("-" * 30)
    
    try:
        import os
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
        django.setup()
        
        from payments.models import Payment
        from tickets.models import TicketPurchase
        
        # Check payment
        payment = Payment.objects.get(reference=payment_ref)
        print(f"💳 Payment in DB:")
        print(f"   Reference: {payment.reference}")
        print(f"   Amount: GH₵{payment.amount}")
        print(f"   Status: {payment.status}")
        
        # Check ticket purchase
        purchase = TicketPurchase.objects.filter(
            payment_reference=payment_ref
        ).first()
        
        if purchase:
            print(f"🎫 Ticket Purchase in DB:")
            print(f"   ID: {purchase.purchase_id}")
            print(f"   Total Amount: GH₵{purchase.total_amount}")
            print(f"   Unit Price: GH₵{purchase.unit_price}")
            print(f"   Status: {purchase.status}")
            print(f"   Payment Reference: {purchase.payment_reference}")
            
            # Final verification
            if (payment.amount == purchase.total_amount and 
                purchase.payment_reference == payment.reference and
                purchase.status == 'confirmed'):
                print(f"\n🎉 COMPLETE SUCCESS!")
                print(f"   ✅ Payment and ticket purchase are properly linked")
                print(f"   ✅ Amounts match (GH₵{payment.amount})")
                print(f"   ✅ VIP pricing is preserved")
            else:
                print(f"\n⚠️  PARTIAL SUCCESS - some issues remain")
        else:
            print(f"❌ No ticket purchase found with payment reference")
            
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
    
    print(f"\n" + "=" * 50)
    print(f"🎯 VIP TICKET FIX TEST COMPLETE")
    print(f"=" * 50)

if __name__ == "__main__":
    test_vip_ticket_fix()