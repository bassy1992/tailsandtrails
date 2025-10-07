import requests
import json
import time

def demo_ticket_payment():
    """Demo the complete ticket payment flow"""
    
    print("🎫 TICKET PAYMENT DEMO")
    print("=" * 50)
    
    # Step 1: Show available tickets
    print("\n📋 Available Tickets:")
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    tickets = tickets_response.json()
    
    for i, ticket in enumerate(tickets[:3], 1):
        print(f"   {i}. {ticket['title']}")
        print(f"      Price: GH₵{ticket['price']}")
        print(f"      Date: {ticket['event_date']}")
        print(f"      Venue: {ticket.get('venue', {}).get('name', 'TBA')}")
        print()
    
    # Use first ticket for demo
    ticket = tickets[0]
    print(f"🎯 Demo using: {ticket['title']} (GH₵{ticket['price']})")
    
    # Step 2: Create payment
    print("\n💳 Creating payment...")
    payment_data = {
        "amount": float(ticket['price']),
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",
        "phone_number": "+233244123456",
        "description": f"Ticket: {ticket['title']}",
        "booking_details": {
            "type": "ticket",
            "ticket_id": ticket['id'],
            "customer_name": "Demo Customer",
            "customer_email": "demo@example.com"
        }
    }
    
    payment_response = requests.post(
        'http://localhost:8000/api/payments/checkout/create/',
        json=payment_data
    )
    
    if payment_response.status_code != 201:
        print(f"❌ Payment failed: {payment_response.text}")
        return
    
    payment_result = payment_response.json()
    payment_ref = payment_result['payment']['reference']
    print(f"✅ Payment created: {payment_ref}")
    print("📱 In real life: User would get SMS prompt on their phone")
    
    # Step 3: Simulate payment completion
    print("\n⏳ Simulating payment authorization...")
    time.sleep(2)  # Simulate user thinking time
    
    complete_response = requests.post(
        f'http://localhost:8000/api/payments/{payment_ref}/complete/',
        json={"status": "successful"}
    )
    
    if complete_response.status_code == 200:
        print("✅ Payment authorized successfully!")
    else:
        print("❌ Payment authorization failed")
        return
    
    # Step 4: Create ticket purchase
    print("\n🎫 Creating ticket purchase...")
    ticket_data = {
        "ticket_id": ticket['id'],
        "quantity": 1,
        "customer_name": "Demo Customer",
        "customer_email": "demo@example.com",
        "customer_phone": "0244123456",
        "payment_method": "mtn_momo",
        "payment_reference": payment_ref
    }
    
    ticket_response = requests.post(
        'http://localhost:8000/api/tickets/purchase/direct/',
        json=ticket_data
    )
    
    if ticket_response.status_code != 201:
        print(f"❌ Ticket creation failed: {ticket_response.text}")
        return
    
    ticket_result = ticket_response.json()
    purchase_id = ticket_result['purchase']['purchase_id']
    print(f"✅ Ticket purchased: {purchase_id}")
    
    # Step 5: Get ticket codes
    print("\n🎟️ Getting ticket codes...")
    details_response = requests.get(
        f'http://localhost:8000/api/tickets/purchase/{purchase_id}/details/'
    )
    
    if details_response.status_code == 200:
        details = details_response.json()
        codes = details.get('ticket_codes', [])
        print(f"✅ Generated {len(codes)} ticket code(s):")
        for code in codes:
            print(f"   🎫 {code['code']}")
    
    print("\n" + "=" * 50)
    print("🎉 DEMO COMPLETE!")
    print("\n📊 What happened:")
    print("   1. Payment created in Payment model")
    print("   2. Payment completed (simulated)")
    print("   3. Ticket purchase created in TicketPurchase model")
    print("   4. Ticket codes generated")
    print("\n🔍 Check admin panels:")
    print("   - Payments: http://localhost:8000/admin/payments/payment/")
    print("   - Tickets: http://localhost:8000/admin/tickets/ticketpurchase/")
    print("\n🌐 Frontend test:")
    print("   - Visit: http://localhost:8080/tickets")
    print("   - Click any ticket → Book Now → Fill form → Pay")
    print("   - Should work end-to-end now!")

if __name__ == "__main__":
    demo_ticket_payment()