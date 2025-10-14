#!/usr/bin/env python
import os
import django
import sys
import requests

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def test_api_endpoints():
    base_url = 'http://127.0.0.1:8000/api'
    
    print("Testing Destinations API endpoints...")
    
    # Test categories endpoint
    try:
        response = requests.get(f'{base_url}/categories/')
        print(f"✅ Categories endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} categories")
    except Exception as e:
        print(f"❌ Categories endpoint error: {e}")
    
    # Test destinations endpoint
    try:
        response = requests.get(f'{base_url}/destinations/')
        print(f"✅ Destinations endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data)} destinations")
            if data:
                print(f"   First destination: {data[0]['name']}")
    except Exception as e:
        print(f"❌ Destinations endpoint error: {e}")
    
    # Test destination detail endpoint
    try:
        response = requests.get(f'{base_url}/destinations/cape-coast-castle-heritage-tour/')
        print(f"✅ Destination detail endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Destination: {data['name']}")
            print(f"   Price: GH₵{data['price']}")
            print(f"   Highlights: {len(data['highlights'])} items")
    except Exception as e:
        print(f"❌ Destination detail endpoint error: {e}")
    
    # Test stats endpoint
    try:
        response = requests.get(f'{base_url}/stats/')
        print(f"✅ Stats endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Total destinations: {data['total_destinations']}")
            print(f"   Categories: {data['categories_count']}")
            print(f"   Featured: {data['featured_destinations']}")
    except Exception as e:
        print(f"❌ Stats endpoint error: {e}")

if __name__ == "__main__":
    test_api_endpoints()