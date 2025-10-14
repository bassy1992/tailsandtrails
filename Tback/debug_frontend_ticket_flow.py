import requests
import json
import time

def debug_frontend_ticket_flow():
    """Debug the exact frontend ticket purchase flow"""
    
    print("🔍 DEBUGGING FRONTEND TICKET FLOW")
    print("=" * 50)
    
    # Step 1: Get ticket data (simulate frontend ticket selection)
    print("1️⃣ GETTING TICKET DATA")
    print("-" * 30)
    
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
    
    print(f"✅ Found ticket: {ticket['title']}")
    print(f"   ID: {ticket['id']}")
    print(f"   Base Price: GH₵{ticket['price']}")
    
    # Step 2: Simulate frontend purchase data (like what's stored in localStorage)
    print("\n2️⃣ SIMULATING FRONTEND PURCHASE DATA")
    print("-" * 30)
    
    # Simulate VIP ticket selection (base price * 1.8)
    base_price = float(ticket['price'])
    vip_price = round(base_price * 1.8)
    
    purchase_data = {
        "type": "ticket",
        "ticketId": ticket['id'],
        "ticketTitle": ticket['title'],
        "venue": ticket['venue']['name'] if ticket.get('venue') else 'TBA',
        "eventDate": ticket['event_date'],
        "quantity": 1,
        "unitPrice": vip_price,  # VIP price
        "totalAmount": vip_price,
        "customerInfo": {
            "name": "Debug Test User",
            "email": "debugtest@example.com",
            "phone": "+233244123456"
        }
    }
    
    print(f"📦 Purchase Data:")
    print(f"   Ticket ID: {purchase_data['ticketId']}")
    print(f"   Quantity: {purchase_data['quantity']}")
    print(f"   Unit Price: GH₵{purchase_data['unitPrice']}")
    print(f"   Total Amount: GH₵{purchase_data['totalAmount']}")
    
    # Step 3: Create payment (simulate frontend payment creation)
    print("\n3️⃣ CREATING PAYMENT")
    print("-" * 30)
    
    payment_data = {
        "amount": purchase_data['totalAmount'],
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": purchase_data['customerInfo']['phone'],
        "description": f"Ticket Purchase: {purchase_data['ticketTitle']} ({purchase_data['quantity']} tickets)",
        "booking_details": {
            "type": "ticket",
            "ticket_id": purchase_data['ticketId'],
            "ticket_title": purchase_data['ticketTitle'],
            "customer_name": purchase_data['customerInfo']['name'],
            "customer_email": purchase_data['customerInfo']['email']
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
    payment_reference = payment_result['payment']['reference']
    print(f"✅ Payment created: {payment_reference}")
    print(f"   Amount: GH₵{payment_result['payment']['amount']}")
    
    # Step 4: Wait for payment completion (simulate frontend polling)
    print("\n4️⃣ WAITING FOR PAYMENT COMPLETION")
    print("-" * 30)
    
    max_attempts = 12  # 60 seconds max (5 second intervals)
    attempt = 0
    payment_successful = False
    
    while attempt < max_attempts:
        attempt += 1
        print(f"   Polling attempt {attempt}/12...")
        
        status_response = requests.get(f'http://localhost:8000/api/payments/{payment_reference}/status/')
        if status_response.status_code != 200:
            print(f"   ❌ Status check failed: {status_response.status_code}")
            time.sleep(5)
            continue
        
        status_result = status_response.json()
        print(f"   Status: {status_result['status']}")
        
        if status_result['status'] == 'successful':
            payment_successful = True
            print(f"   ✅ Payment successful!")
            break
        elif status_result['status'] in ['failed', 'cancelled']:
            print(f"   ❌ Payment failed/cancelled")
            break
        
        time.sleep(5)  # Wait 5 seconds like frontend
    
    if not payment_successful:
        print("❌ Payment did not complete successfully")
        return
    
    # Step 5: Create ticket purchase (simulate exact frontend call)
    print("\n5️⃣ CREATING TICKET PURCHASE")
    print("-" * 30)
    
    # Simulate exact frontend data
    momo_provider = "MTN Mobile Money"
    phone_number = purchase_data['customerInfo']['phone']
    account_name = purchase_data['customerInfo']['name']
    
    # Use correct payment method mapping (like the fixed frontend)
    def get_payment_method_code(provider):
        mapping = {
            'MTN Mobile Money': 'mtn_momo',
            'Vodafone Cash': 'vodafone_cash',
            'AirtelTigo Money': 'airteltigo_money'
        }
        return mapping.get(provider, 'momo')
    
    ticket_purchase_data = {
        "ticket_id": purchase_data['ticketId'],
        "quantity": purchase_data['quantity'],
        "total_amount": purchase_data['totalAmount'],
        "customer_name": purchase_data['customerInfo']['name'],
        "customer_email": purchase_data['customerInfo']['email'],
        "customer_phone": purchase_data['customerInfo']['phone'],
        "payment_method": get_payment_method_code(momo_provider),
        "payment_reference": payment_reference,
        "special_requests": f"Mobile Money Payment - {momo_provider} - {phone_number} - Account: {account_name}"
    }
    
    print(f"📤 Ticket Purchase Request:")
    print(f"   {json.dumps(ticket_purchase_data, indent=2)}")
    
    ticket_response = requests.post(
        'http://localhost:8000/api/tickets/purchase/direct/',
        json=ticket_purchase_data
    )
    
    print(f"\n📥 Ticket Purchase Response:")
    print(f"   Status Code: {ticket_response.status_code}")
    print(f"   Headers: {dict(ticket_response.headers)}")
    
    if ticket_response.status_code == 201:
        try:
            ticket_result = ticket_response.json()
            print(f"   Response Body: {json.dumps(ticket_result, indent=2)}")
            
            if ticket_result.get('success'):
                print(f"\n✅ TICKET CREATION SUCCESS!")
                purchase = ticket_result['purchase']
                print(f"   Purchase ID: {purchase['purchase_id']}")
                print(f"   Status: {purchase['status']}")
                print(f"   Total Amount: GH₵{purchase['total_amount']}")
                print(f"   Payment Reference: {purchase['payment_reference']}")
                
                codes = purchase.get('ticket_codes', [])
                print(f"   Ticket Codes: {len(codes)} generated")
                for code in codes:
                    print(f"      - {code['code']} ({code['status']})")
                
            else:
                print(f"\n❌ TICKET CREATION FAILED!")
                print(f"   Error: {ticket_result.get('error', 'Unknown error')}")
                print(f"   Message: {ticket_result.get('message', 'No message')}")
                
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON Decode Error: {e}")
            print(f"   Raw Response: {ticket_response.text}")
    else:
        print(f"   ❌ HTTP Error: {ticket_response.status_code}")
        print(f"   Raw Response: {ticket_response.text}")
    
    # Step 6: Verify in database
    print("\n6️⃣ VERIFYING IN DATABASE")
    print("-" * 30)
    
    try:
        import os
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
        django.setup()
        
        from payments.models import Payment
        from tickets.models import TicketPurchase
        
        # Check payment
        payment = Payment.objects.get(reference=payment_reference)
        print(f"💳 Payment Status: {payment.status}")
        print(f"   Amount: GH₵{payment.amount}")
        
        # Check ticket purchases
        purchases = TicketPurchase.objects.filter(
            payment_reference=payment_reference
        )
        print(f"🎫 Ticket Purchases: {purchases.count()} found")
        
        for purchase in purchases:
            print(f"   ID: {purchase.purchase_id}")
            print(f"   Status: {purchase.status}")
            print(f"   Amount: GH₵{purchase.total_amount}")
            print(f"   Codes: {purchase.ticket_codes.count()}")
            
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
    
    print(f"\n" + "=" * 50)
    print(f"🎯 FRONTEND FLOW DEBUG COMPLETE")
    print(f"=" * 50)

if __name__ == "__main__":
    debug_frontend_ticket_flow()