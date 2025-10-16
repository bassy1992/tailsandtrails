#!/usr/bin/env python3

import requests
import json

# Test the add-ons API endpoint
def test_addons_api():
    print("🧪 Testing add-ons API endpoint...")
    
    # Test URL
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    # First, let's get a list of tickets to find a valid ticket ID
    print("\n1. Getting list of tickets...")
    try:
        tickets_response = requests.get(f"{base_url}/tickets/")
        print(f"Tickets API Status: {tickets_response.status_code}")
        
        if tickets_response.status_code == 200:
            tickets_data = tickets_response.json()
            print(f"Tickets data type: {type(tickets_data)}")
            
            # Handle both list and paginated response formats
            if isinstance(tickets_data, list):
                tickets_list = tickets_data
            else:
                tickets_list = tickets_data.get('results', [])
            
            print(f"Found {len(tickets_list)} tickets")
            
            if tickets_list:
                # Use the first ticket for testing
                first_ticket = tickets_list[0]
                print(f"First ticket data: {first_ticket}")
                ticket_id = first_ticket['id']
                ticket_name = first_ticket.get('name', first_ticket.get('title', 'Unknown'))
                print(f"Testing with ticket: {ticket_name} (ID: {ticket_id})")
                
                # Test the add-ons endpoint
                print(f"\n2. Testing add-ons endpoint for ticket {ticket_id}...")
                addons_url = f"{base_url}/tickets/{ticket_id}/addons/?travelers=2"
                print(f"URL: {addons_url}")
                
                addons_response = requests.get(addons_url)
                print(f"Add-ons API Status: {addons_response.status_code}")
                
                if addons_response.status_code == 200:
                    addons_data = addons_response.json()
                    print("✅ Add-ons API is working!")
                    print(f"Response: {json.dumps(addons_data, indent=2)}")
                else:
                    print("❌ Add-ons API failed!")
                    print(f"Error: {addons_response.text}")
            else:
                print("❌ No tickets found to test with")
        else:
            print(f"❌ Failed to get tickets: {tickets_response.text}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_addons_api()