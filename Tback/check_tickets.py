import requests

def check_available_tickets():
    """Check what tickets are available"""
    
    print("=== Checking Available Tickets ===")
    
    try:
        response = requests.get('http://localhost:8000/api/tickets/')
        if response.status_code == 200:
            tickets = response.json()
            print(f"✅ Found {len(tickets)} tickets:")
            
            for ticket in tickets:
                print(f"   - ID: {ticket['id']}")
                print(f"     Slug: {ticket['slug']}")
                print(f"     Title: {ticket['title']}")
                print(f"     Status: {ticket['status']}")
                print(f"     URL: /tickets/{ticket['slug']}")
                print()
        else:
            print(f"❌ Failed to get tickets: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_ticket_access():
    """Test accessing a specific ticket"""
    
    print("=== Testing Ticket Access ===")
    
    # Get the first ticket and test access
    try:
        response = requests.get('http://localhost:8000/api/tickets/')
        if response.status_code == 200:
            tickets = response.json()
            if tickets:
                first_ticket = tickets[0]
                ticket_slug = first_ticket['slug']
                ticket_id = first_ticket['id']
                
                print(f"Testing access to ticket: {first_ticket['title']}")
                print(f"Slug: {ticket_slug}")
                print(f"ID: {ticket_id}")
                
                # Test slug-based access
                slug_response = requests.get(f'http://localhost:8000/api/tickets/{ticket_slug}/')
                print(f"Slug access (/api/tickets/{ticket_slug}/): {slug_response.status_code}")
                
                # Test ID-based access
                id_response = requests.get(f'http://localhost:8000/api/tickets/?id={ticket_id}')
                print(f"ID access (/api/tickets/?id={ticket_id}): {id_response.status_code}")
                
                if id_response.status_code == 200:
                    id_data = id_response.json()
                    print(f"ID response contains {len(id_data)} tickets")
                
                print(f"\n✅ Frontend URL should be: http://localhost:8081/tickets/{ticket_slug}")
            else:
                print("❌ No tickets found")
    except Exception as e:
        print(f"❌ Error testing ticket access: {e}")

if __name__ == "__main__":
    check_available_tickets()
    test_ticket_access()
    
    print("\n=== Troubleshooting Tips ===")
    print("If you're getting 'EventTicket not found' error:")
    print("1. Make sure you're using the correct ticket slug in the URL")
    print("2. Check that the ticket exists and has status 'active'")
    print("3. Verify the frontend is accessing the right API endpoint")
    print("4. Try refreshing the tickets list at http://localhost:8081/tickets")