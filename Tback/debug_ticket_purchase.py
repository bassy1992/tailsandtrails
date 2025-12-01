import requests
import json

def debug_ticket_purchase():
    """Debug ticket purchase creation"""
    
    # Get a ticket
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    ticket = tickets_response.json()[0]
    
    print(f"Using ticket: {ticket['title']} (ID: {ticket['id']})")
    
    # Try to create ticket purchase
    ticket_data = {
        "ticket_id": ticket['id'],
        "quantity": 1,
        "customer_name": "Debug Customer",
        "customer_email": "debug@example.com",
        "customer_phone": "0244123456",
        "payment_method": "mtn_momo",
        "payment_reference": "DEBUG_REF_123"
    }
    
    print("\\nSending request...")
    print(f"Data: {json.dumps(ticket_data, indent=2)}")
    
    response = requests.post(
        'http://localhost:8000/api/tickets/purchase/direct/',
        json=ticket_data
    )
    
    print(f"\\nStatus: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Also try the debug endpoint
    print("\\n" + "="*50)
    print("Checking recent purchases...")
    debug_response = requests.get('http://localhost:8000/api/tickets/purchases/debug/')
    if debug_response.status_code == 200:
        debug_data = debug_response.json()
        print(f"Total purchases: {debug_data.get('total_purchases', 0)}")
        recent = debug_data.get('recent_purchases', [])
        for purchase in recent[:3]:
            print(f"  - {purchase['ticket']} | {purchase['customer']} | {purchase['status']}")

if __name__ == "__main__":
    debug_ticket_purchase()