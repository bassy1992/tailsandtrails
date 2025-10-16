#!/usr/bin/env python3

import requests

def test_ticket_addons():
    """Test the add-ons endpoint with valid ticket IDs"""
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    # Test with valid ticket IDs
    valid_tickets = [1, 2]
    
    for ticket_id in valid_tickets:
        print(f"\n✅ Testing ticket ID {ticket_id}...")
        url = f"{base_url}/tickets/{ticket_id}/addons/?travelers=1"
        
        try:
            response = requests.get(url)
            print(f"   URL: {url}")
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ Success! Found {len(data.get('categories', []))} add-on categories")
                else:
                    print(f"   ❌ API returned success=false: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ❌ HTTP Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test with invalid ticket ID 7
    print(f"\n❌ Testing invalid ticket ID 7...")
    url = f"{base_url}/tickets/7/addons/?travelers=1"
    
    try:
        response = requests.get(url)
        print(f"   URL: {url}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print(f"   ✅ Expected 400 error: {data.get('error', 'Unknown error')}")
        else:
            print(f"   ⚠️  Unexpected response: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

if __name__ == "__main__":
    print("🧪 Testing ticket add-ons endpoints...")
    test_ticket_addons()
    print("\n✅ Test completed!")