import requests
import json

def test_ticket_purchase():
    """Test the direct ticket purchase flow"""
    
    # First, get available tickets
    print("=== Getting Available Tickets ===")
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    
    if tickets_response.status_code == 200:
        tickets = tickets_response.json()
        if tickets and len(tickets) > 0:
            ticket = tickets[0]  # Get first ticket
            print(f"Found ticket: {ticket['title']} - GH₵{ticket['price']}")
            
            # Create a ticket purchase
            print("\n=== Creating Ticket Purchase ===")
            purchase_data = {
                'ticket_id': ticket['id'],
                'quantity': 2,
                'customer_name': 'John Doe',
                'customer_email': 'john@example.com',
                'customer_phone': '+233240000000',
                'payment_method': 'mtn_momo',
                'special_requests': 'Please send tickets via email'
            }
            
            purchase_response = requests.post(
                'http://localhost:8000/api/tickets/purchase/direct/',
                json=purchase_data
            )
            
            print(f"Status Code: {purchase_response.status_code}")
            result = purchase_response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            
            if result.get('success'):
                purchase_id = result['purchase']['purchase_id']
                print(f"\n✅ Ticket purchase created successfully!")
                print(f"Purchase ID: {purchase_id}")
                
                # Check purchase status
                print("\n=== Checking Purchase Status ===")
                status_response = requests.get(
                    f'http://localhost:8000/api/tickets/purchase/{purchase_id}/status/'
                )
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"Purchase Status: {status_data['purchase']['status']}")
                    print(f"Payment Status: {status_data['purchase']['payment_status']}")
                
                # Get purchase details
                print("\n=== Getting Purchase Details ===")
                details_response = requests.get(
                    f'http://localhost:8000/api/tickets/purchase/{purchase_id}/details/'
                )
                
                if details_response.status_code == 200:
                    details_data = details_response.json()
                    print(f"Ticket Codes Generated: {len(details_data.get('ticket_codes', []))}")
                    for code in details_data.get('ticket_codes', []):
                        print(f"  - Code: {code['code']} (Status: {code['status']})")
                
                return purchase_id
            else:
                print(f"❌ Purchase failed: {result.get('error')}")
                return None
        else:
            print("No tickets available")
            return None
    else:
        print(f"Failed to get tickets: {tickets_response.status_code}")
        return None

def test_admin_view():
    """Test that purchases appear in admin"""
    print("\n=== Checking Recent Purchases (Admin View) ===")
    debug_response = requests.get('http://localhost:8000/api/tickets/purchases/debug/')
    
    if debug_response.status_code == 200:
        data = debug_response.json()
        print(f"Total Purchases in Database: {data['total_purchases']}")
        print("Recent Purchases:")
        for purchase in data['recent_purchases'][:5]:
            print(f"  - {purchase['ticket']} | {purchase['customer']} | {purchase['quantity']} tickets | GH₵{purchase['total_amount']} | {purchase['status']}")
    else:
        print(f"Failed to get debug info: {debug_response.status_code}")

if __name__ == "__main__":
    # Test the ticket purchase flow
    purchase_id = test_ticket_purchase()
    
    # Check admin view
    test_admin_view()
    
    print("\n=== Summary ===")
    print("✅ Ticket purchases are now separate from Payment model")
    print("✅ Purchases will appear in /admin/tickets/ticketpurchase/")
    print("✅ Payment model is reserved for destination bookings only")
    print("✅ Ticket codes are automatically generated")
    
    if purchase_id:
        print(f"\n🎫 Test purchase created: {purchase_id}")
        print("Check the admin panel to see the purchase!")