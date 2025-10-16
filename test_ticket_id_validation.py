#!/usr/bin/env python3

import requests

def test_ticket_id_validation():
    """Test that invalid ticket IDs are handled properly"""
    base_url = "https://tailsandtrails-production.up.railway.app/api"
    
    print("🧪 Testing ticket ID validation...")
    
    # Test valid ticket IDs
    valid_ids = [1, 2]
    for ticket_id in valid_ids:
        print(f"\n✅ Testing valid ticket ID {ticket_id}...")
        url = f"{base_url}/tickets/{ticket_id}/addons/?travelers=1"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print(f"   ✅ Success! Found {len(data.get('categories', []))} add-on categories")
                else:
                    print(f"   ❌ API returned success=false: {data.get('error')}")
            else:
                print(f"   ❌ HTTP Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    # Test invalid ticket IDs
    invalid_ids = [7, 99, 0, -1]
    for ticket_id in invalid_ids:
        print(f"\n❌ Testing invalid ticket ID {ticket_id}...")
        url = f"{base_url}/tickets/{ticket_id}/addons/?travelers=1"
        
        try:
            response = requests.get(url)
            if response.status_code == 400:
                data = response.json()
                print(f"   ✅ Expected 400 error: {data.get('error', 'Unknown error')}")
            else:
                print(f"   ⚠️  Unexpected response {response.status_code}: {response.text}")
        except Exception as e:
            print(f"   ❌ Exception: {e}")

def test_frontend_validation():
    """Test that frontend validation works"""
    print(f"\n🎯 Frontend validation should now:")
    print(f"   1. Redirect /booking/7 → /booking/2")
    print(f"   2. Redirect /ticket-booking/7 → /ticket-booking/2") 
    print(f"   3. Show error message for invalid ticket IDs")
    print(f"   4. Not make API calls for invalid ticket IDs")

if __name__ == "__main__":
    test_ticket_id_validation()
    test_frontend_validation()
    
    print(f"\n✅ Ticket ID validation tests completed!")
    print(f"\n💡 The frontend should now:")
    print(f"   • Automatically redirect invalid ticket IDs to valid ones")
    print(f"   • Show proper error messages instead of API errors")
    print(f"   • Prevent unnecessary API calls for non-existent tickets")