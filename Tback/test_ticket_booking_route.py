import requests

def test_ticket_booking_routes():
    """Test ticket booking routes"""
    
    print("🎫 Testing Ticket Booking Routes")
    print("=" * 40)
    
    # Test different ports
    ports = [8080, 8081, 8082]
    working_port = None
    
    for port in ports:
        try:
            response = requests.get(f'http://localhost:{port}/', timeout=3)
            if response.status_code == 200:
                working_port = port
                print(f"✅ Frontend running on port {port}")
                break
        except:
            continue
    
    if not working_port:
        print("❌ Frontend not accessible")
        return
    
    base_url = f'http://localhost:{working_port}'
    
    # Test the specific route that was failing
    routes_to_test = [
        ('/ticket-booking/6', 'Ticket booking with ID 6'),
        ('/ticket-booking/7', 'Ticket booking with ID 7'),
        ('/tickets/traditional-dance-performance', 'Ticket booking with slug'),
        ('/tickets', 'Tickets list'),
        ('/ticket-checkout', 'Ticket checkout')
    ]
    
    print(f"\n📋 Testing routes on {base_url}:")
    
    for route, description in routes_to_test:
        try:
            response = requests.get(f'{base_url}{route}', timeout=5)
            if response.status_code == 200:
                print(f"✅ {route} - {description}: Working")
            else:
                print(f"❌ {route} - {description}: {response.status_code}")
        except Exception as e:
            print(f"❌ {route} - {description}: Error - {e}")
    
    print(f"\n🎯 The problematic URL should now work:")
    print(f"   {base_url}/ticket-booking/6")
    
    # Get available tickets to show valid IDs
    try:
        response = requests.get('http://localhost:8000/api/tickets/')
        if response.status_code == 200:
            tickets = response.json()
            print(f"\n📋 Available ticket IDs:")
            for ticket in tickets[:5]:
                print(f"   ID {ticket['id']}: {ticket['title']}")
                print(f"   URL: {base_url}/ticket-booking/{ticket['id']}")
    except:
        print("\n⚠️  Could not fetch ticket list from backend")

if __name__ == "__main__":
    test_ticket_booking_routes()