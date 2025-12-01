import requests
import json

def check_payment_separation():
    """Check that tickets and destinations are properly separated"""
    
    print("=== Checking Payment System Separation ===")
    
    # Check Payment records (should only have destination bookings)
    print("\n1. Checking Payment records (destinations only)...")
    try:
        # We don't have a direct API for payments, so let's check via debug
        response = requests.get('http://localhost:8000/api/payments/debug/')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Payment records found: {data.get('total_payments', 0)}")
            
            payments = data.get('recent_payments', [])
            for payment in payments[:3]:
                print(f"   - {payment.get('booking_reference', 'N/A')} | {payment.get('destination', 'N/A')} | GH₵{payment.get('amount', 0)}")
        else:
            print(f"❌ Could not check payments: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking payments: {e}")
    
    # Check TicketPurchase records (should only have ticket purchases)
    print("\n2. Checking TicketPurchase records (tickets only)...")
    try:
        response = requests.get('http://localhost:8000/api/tickets/purchases/debug/')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Ticket purchase records found: {data.get('total_purchases', 0)}")
            
            purchases = data.get('recent_purchases', [])
            for purchase in purchases[:3]:
                print(f"   - {purchase.get('customer', 'N/A')} | {purchase.get('ticket', 'N/A')} | GH₵{purchase.get('total_amount', 0)}")
        else:
            print(f"❌ Could not check ticket purchases: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking ticket purchases: {e}")

def test_new_ticket_purchase():
    """Test creating a new ticket purchase via the correct API"""
    
    print("\n3. Testing new ticket purchase API...")
    
    # Get a ticket to purchase
    try:
        tickets_response = requests.get('http://localhost:8000/api/tickets/')
        if tickets_response.status_code == 200:
            tickets = tickets_response.json()
            if tickets:
                ticket = tickets[0]
                print(f"   Testing with ticket: {ticket['title']}")
                
                # Create purchase via new API
                purchase_data = {
                    'ticket_id': ticket['id'],
                    'quantity': 1,
                    'customer_name': 'Test Customer',
                    'customer_email': 'test@example.com',
                    'customer_phone': '+233240000000',
                    'payment_method': 'mtn_momo',
                    'special_requests': 'Test purchase to verify separation'
                }
                
                response = requests.post(
                    'http://localhost:8000/api/tickets/purchase/direct/',
                    json=purchase_data
                )
                
                if response.status_code == 201:
                    result = response.json()
                    if result.get('success'):
                        print(f"   ✅ New ticket purchase created: {result['purchase']['purchase_id'][:8]}...")
                        print(f"   ✅ This should appear in /admin/tickets/ticketpurchase/")
                        print(f"   ✅ This should NOT appear in /admin/payments/payment/")
                    else:
                        print(f"   ❌ Purchase failed: {result.get('error')}")
                else:
                    print(f"   ❌ API call failed: {response.status_code}")
            else:
                print("   ❌ No tickets available for testing")
        else:
            print(f"   ❌ Could not get tickets: {tickets_response.status_code}")
    except Exception as e:
        print(f"   ❌ Error testing ticket purchase: {e}")

def show_admin_urls():
    """Show the correct admin URLs for verification"""
    
    print("\n=== Admin URLs for Verification ===")
    print("🎫 Ticket Purchases (NEW system):")
    print("   http://localhost:8000/admin/tickets/ticketpurchase/")
    print("   - Should contain: All ticket purchases")
    print("   - Should show: Customer names, ticket titles, purchase IDs")
    
    print("\n🏝️ Destination Payments (OLD system):")
    print("   http://localhost:8000/admin/payments/payment/")
    print("   - Should contain: Only destination bookings")
    print("   - Should show: Booking references, destination names")
    
    print("\n⚠️ If tickets appear in the payments admin:")
    print("   1. Clear browser cache and localStorage")
    print("   2. Make sure you're using the updated frontend")
    print("   3. Check that ticket purchases go to /ticket-checkout, not /momo-checkout")

if __name__ == "__main__":
    check_payment_separation()
    test_new_ticket_purchase()
    show_admin_urls()
    
    print("\n=== Summary ===")
    print("✅ Ticket purchases should go to: TicketPurchase model")
    print("✅ Destination bookings should go to: Payment model")
    print("✅ Frontend updated to redirect tickets to new system")
    print("✅ MomoCheckout now redirects ticket purchases automatically")
    print("\n🎯 Next: Test a ticket purchase at http://localhost:8081/tickets")