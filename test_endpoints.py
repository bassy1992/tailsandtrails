#!/usr/bin/env python
"""
Test image upload endpoints
"""
import requests

def test_endpoints():
    api_url = 'https://tailsandtrails-production.up.railway.app/api'
    
    print('🔍 Testing image upload endpoints...')
    
    try:
        response = requests.get(f'{api_url}/destinations/', timeout=10)
        if response.status_code == 200:
            destinations = response.json()
            print(f'✅ Found {len(destinations)} destinations')
            
            if destinations:
                dest = destinations[0]
                print(f'   Example: {dest.get("name", "Unknown")} (ID: {dest.get("id", "N/A")})')
                print(f'   Current image: {dest.get("image", "None")}')
                print(f'   Current image_url: {dest.get("image_url", "None")}')
        else:
            print(f'❌ Failed to get destinations: {response.status_code}')
            
    except Exception as e:
        print(f'❌ Error: {e}')
    
    try:
        response = requests.patch(f'{api_url}/destinations/1/upload-image/', timeout=5)
        print(f'📤 Image upload endpoint: {response.status_code} (401 expected - needs auth)')
    except Exception as e:
        print(f'📤 Image upload endpoint test failed: {e}')

if __name__ == '__main__':
    test_endpoints()