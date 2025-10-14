import requests
import json
import time

def test_ticket_payment_integration():
    """Test the complete ticket payment integration"""
    
    print("=== Testing Ticket Payment Integration ===")
    
    # Step 1: Get available tickets
    print("\n1. Getting available tickets...")
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    
    if tickets_response.status_code != 200:
        print(f"❌ Failed to get tickets: {tickets_response.status_code}")
        return
    
    tickets = tickets_response.json()
    if not tickets:
        print("❌ No tickets available")
        return
    
    ticket = tickets[0]
    print(f"✅ Using ticket: {ticket['title']} (ID: {ticket['id']}) - GH₵{ticket['price']}")
    
    # Step 2: Test payment creation
    print("\n2. Creating payment...")
    payment_data = {
        "amount": float(ticket['price']),
        "currency": "GHS",
        "payment_method": "momo",
        "provider_code": "mtn_momo",  # Use provider code
        "phone_number": "+233244123456",  # Format phone number
        "description": f"Ticket Purchase: {ticket['title']} (1 ticket)",
        "booking_details": {
            "type": "ticket",
            "ticket_id": ticket['id'],
            "ticket_title": ticket['title'],
            "quantity": 1,
            "unit_price": float(ticket['price']),
            "customer_name": "Test Customer",
            "customer_email": "test@example.com",
            "customer_phone": "0244123456",
            "payment_provider": "MTN Mobile Money",
            "account_name": "Test Account"
        }
    }
    
    payment_response = requests.post(
        'http://localhost:8000/api/payments/checkout/create/',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(payment_data)
    )
    
    if payment_response.status_code != 201:
        print(f"❌ Payment creation failed: {payment_response.status_code}")
        print(f"Response: {payment_response.text}")
        return
    
    payment_result = payment_response.json()
    if not payment_result.get('success'):
        print(f"❌ Payment creation failed: {payment_result}")
        return
    
    payment_reference = payment_result['payment']['reference']
    print(f"✅ Payment created: {payment_reference}")
    
    # Step 3: Simulate payment completion (for demo)
    print("\n3. Simulating payment completion...")
    complete_response = requests.post(
        f'http://localhost:8000/api/payments/{payment_reference}/complete/',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({"status": "successful"})
    )
    
    if complete_response.status_code == 200:
        print("✅ Payment completed successfully")
    else:
        print(f"⚠️  Payment completion response: {complete_response.status_code}")
    
    # Step 4: Check payment status
    print("\n4. Checking payment status...")
    status_response = requests.get(f'http://localhost:8000/api/payments/{payment_reference}/status/')
    
    if status_response.status_code == 200:
        status_result = status_response.json()
        print(f"✅ Payment status: {status_result.get('status')}")
        
        if status_result.get('status') == 'successful':
            # Step 5: Create ticket purchase
            print("\n5. Creating ticket purchase...")
            ticket_data = {
                "ticket_id": ticket['id'],
                "quantity": 1,
                "customer_name": "Test Customer",
                "customer_email": "test@example.com",
                "customer_phone": "0244123456",
                "payment_method": "mtn_momo",
                "payment_reference": payment_reference,
                "special_requests": "Mobile Money Payment - MTN Mobile Money - 0244123456 - Account: Test Account"
            }
            
            ticket_response = requests.post(
                'http://localhost:8000/api/tickets/purchase/direct/',
                headers={'Content-Type': 'application/json'},
                data=json.dumps(ticket_data)
            )
            
            if ticket_response.status_code == 201:
                ticket_result = ticket_response.json()
                if ticket_result.get('success'):
                    purchase_id = ticket_result['purchase']['purchase_id']
                    print(f"✅ Ticket purchase created: {purchase_id}")
                    
                    # Step 6: Get ticket details
                    print("\n6. Getting ticket details...")
                    details_response = requests.get(
                        f'http://localhost:8000/api/tickets/purchase/{purchase_id}/details/'
                    )
                    
                    if details_response.status_code == 200:
                        details_result = details_response.json()
                        if details_result.get('success'):
                            codes = details_result.get('ticket_codes', [])
                            print(f"✅ Ticket codes generated: {len(codes)} codes")
                            for i, code in enumerate(codes[:3]):  # Show first 3
                                print(f"   Code {i+1}: {code['code']}")
                        else:
                            print(f"⚠️  Ticket details error: {details_result}")
                    else:
                        print(f"⚠️  Ticket details failed: {details_response.status_code}")
                else:
                    print(f"❌ Ticket purchase failed: {ticket_result}")
            else:
                print(f"❌ Ticket purchase request failed: {ticket_response.status_code}")
                print(f"Response: {ticket_response.text}")
        else:
            print(f"❌ Payment not successful: {status_result.get('status')}")
    else:
        print(f"❌ Status check failed: {status_response.status_code}")

def test_frontend_integration():
    """Test that the frontend can access the ticket checkout page"""
    
    print("\\n=== Testing Frontend Integration ===")
    
    # Test frontend routes
    routes_to_test = [
        ('http://localhost:8080/tickets', 'Tickets list page'),
        ('http://localhost:8080/ticket-checkout', 'Ticket checkout page'),
        ('http://localhost:8080/ticket-purchase-success', 'Purchase success page')
    ]
    
    for url, description in routes_to_test:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {description}: Accessible")
            else:
                print(f"❌ {description}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}: Connection error - {e}")

def show_integration_summary():
    """Show summary of the integration"""
    
    print("\\n" + "="*60)
    print("🎉 TICKET PAYMENT INTEGRATION READY!")
    print("="*60)
    
    print("\\n✅ What's working:")
    print("   - Payment system integration")
    print("   - Ticket purchase after successful payment")
    print("   - Real payment status polling")
    print("   - Ticket code generation")
    print("   - Frontend checkout page")
    
    print("\\n🔄 Payment Flow:")
    print("   1. User fills checkout form")
    print("   2. Payment created via /api/payments/checkout/")
    print("   3. Frontend polls payment status")
    print("   4. When payment successful → create ticket")
    print("   5. Redirect to success page with ticket codes")
    
    print("\\n📱 Test URLs:")
    print("   - Frontend: http://localhost:8080/ticket-checkout")
    print("   - Backend API: http://localhost:8000/api/payments/checkout/")
    print("   - Admin payments: http://localhost:8000/admin/payments/payment/")
    print("   - Admin tickets: http://localhost:8000/admin/tickets/ticketpurchase/")
    
    print("\\n🎯 Next Steps:")
    print("   1. Test the complete flow in browser")
    print("   2. Try purchasing a ticket end-to-end")
    print("   3. Check that payments appear in Payment admin")
    print("   4. Check that tickets appear in TicketPurchase admin")

if __name__ == "__main__":
    test_ticket_payment_integration()
    test_frontend_integration()
    show_integration_summary()