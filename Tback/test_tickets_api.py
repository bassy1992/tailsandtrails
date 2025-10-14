import requests
import json

def test_tickets_api():
    """Test the tickets API to ensure data is properly loaded"""
    
    print("🔍 TESTING TICKETS API")
    print("=" * 50)
    
    # Test tickets endpoint
    print("1️⃣ Testing /api/tickets/")
    print("-" * 30)
    
    try:
        response = requests.get('http://localhost:8000/api/tickets/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            tickets = response.json()
            print(f"✅ Found {len(tickets)} tickets")
            
            for ticket in tickets:
                price_display = f"GH₵{ticket.get('discount_price', ticket.get('price'))}"
                featured = "⭐" if ticket.get('is_featured') else "  "
                print(f"   {featured} {ticket['title']} - {price_display}")
                print(f"      Category: {ticket.get('category', {}).get('name', 'N/A')}")
                print(f"      Venue: {ticket.get('venue', {}).get('name', 'N/A')}")
                print(f"      Available: {ticket.get('available_quantity', 0)}")
                print()
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test categories endpoint
    print("2️⃣ Testing /api/tickets/categories/")
    print("-" * 30)
    
    try:
        response = requests.get('http://localhost:8000/api/tickets/categories/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Found {len(categories)} categories")
            
            for category in categories:
                print(f"   📂 {category['name']} ({category['category_type']})")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test venues endpoint
    print("\n3️⃣ Testing /api/tickets/venues/")
    print("-" * 30)
    
    try:
        response = requests.get('http://localhost:8000/api/tickets/venues/')
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            venues = response.json()
            print(f"✅ Found {len(venues)} venues")
            
            for venue in venues:
                print(f"   🏢 {venue['name']} - {venue['city']}")
                print(f"      Capacity: {venue.get('capacity', 'N/A')}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    print(f"\n" + "=" * 50)
    print(f"🎯 API TEST COMPLETE")
    print(f"=" * 50)

if __name__ == "__main__":
    test_tickets_api()