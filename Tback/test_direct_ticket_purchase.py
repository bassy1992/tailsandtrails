import requests
import json

def test_direct_ticket_purchase():
    """Test the direct ticket purchase endpoint to see what's failing"""
    
    print("🎫 TESTING DIRECT TICKET PURCHASE")
    print("=" * 50)
    
    # Get a ticket to test with
    tickets_response = requests.get('http://localhost:8000/api/tickets/')
    if tickets_response.status_code != 200:
        print("❌ Failed to get tickets")
        return
    
    tickets = tickets_response.json()
    ticket = tickets[1]  # Ghana Cultural Festival 2025
    
    print(f"🎫 Testing with ticket: {ticket['title']}")
    print(f"   Price: GH₵{ticket['price']}")
    print(f"   ID: {ticket['id']}")
    
    # Test the direct purchase endpoint
    purchase_data = {
        "ticket_id": ticket['id'],
        "quantity": 1,
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        "customer_phone": "+233244123456",
        "payment_method": "mtn_momo",
        "payment_reference": "TEST-PAYMENT-REF-123",
        "special_requests": "Test purchase"
    }
    
    print(f"\n📤 Sending purchase request...")
    print(f"   Data: {json.dumps(purchase_data, indent=2)}")
    
    response = requests.post(
        'http://localhost:8000/api/tickets/purchase/direct/',
        json=purchase_data
    )
    
    print(f"\n📥 Response:")
    print(f"   Status Code: {response.status_code}")
    print(f"   Content: {response.text}")
    
    if response.status_code == 201:
        result = response.json()
        if result.get('success'):
            purchase = result['purchase']
            print(f"\n✅ SUCCESS!")
            print(f"   Purchase ID: {purchase['purchase_id']}")
            print(f"   Status: {purchase['status']}")
            print(f"   Payment Status: {purchase['payment_status']}")
            print(f"   Total Amount: {purchase['total_amount']}")
            print(f"   Payment Reference: {purchase.get('payment_reference', 'None')}")
        else:
            print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP ERROR: {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data}")
        except:
            print(f"   Raw response: {response.text}")
    
    # Check if purchase was created in database
    print(f"\n🔍 Checking database...")
    try:
        import os
        import django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
        django.setup()
        
        from tickets.models import TicketPurchase
        
        recent_purchase = TicketPurchase.objects.filter(
            customer_email="test@example.com"
        ).order_by('-created_at').first()
        
        if recent_purchase:
            print(f"   ✅ Found purchase in database:")
            print(f"      ID: {recent_purchase.purchase_id}")
            print(f"      Status: {recent_purchase.status}")
            print(f"      Payment Status: {recent_purchase.payment_status}")
            print(f"      Payment Reference: {recent_purchase.payment_reference}")
            print(f"      Total Amount: {recent_purchase.total_amount}")
            
            # Check ticket codes
            codes_count = recent_purchase.ticket_codes.count()
            print(f"      Ticket Codes: {codes_count}")
        else:
            print(f"   ❌ No purchase found in database")
            
    except Exception as e:
        print(f"   ❌ Database check failed: {e}")

if __name__ == "__main__":
    test_direct_ticket_purchase()