#!/usr/bin/env python
"""
Test Cape Coast Castle API response
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.test import Client
import json

def test_cape_coast_api():
    """Test Cape Coast Castle API response"""
    client = Client()
    
    print("🧪 Testing Cape Coast Castle API")
    print("=" * 40)
    
    # Test new galleries endpoint
    print("\n1. Testing /api/gallery/galleries/cape-coast-castle-cape-coast-gallery/")
    response = client.get('/api/gallery/galleries/cape-coast-castle-cape-coast-gallery/')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Gallery: {data['title']}")
        print(f"Location: {data['location']}")
        print(f"Image count: {data['image_count']}")
        print(f"Main image: {data['main_image_url']}")
        print("\nAll images:")
        for i, img in enumerate(data['images'], 1):
            main_indicator = " (MAIN)" if img['is_main'] else ""
            print(f"  {i}. {img['caption']}{main_indicator}")
    else:
        print(f"❌ Status: {response.status_code}")
        print(f"Error: {response.content}")
    
    # Test legacy endpoint
    print("\n2. Testing legacy /api/gallery/images/ endpoint")
    response = client.get('/api/gallery/images/')
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"Total galleries: {len(data)}")
        
        # Find Cape Coast Castle
        cape_coast = None
        for item in data:
            if item['title'] == 'Cape Coast Castle':
                cape_coast = item
                break
        
        if cape_coast:
            print(f"\nCape Coast Castle in legacy format:")
            print(f"  Title: {cape_coast['title']}")
            print(f"  Location: {cape_coast['location']}")
            print(f"  Image URL: {cape_coast['image_url']}")
            print(f"  Category: {cape_coast['category']['name']}")
        else:
            print("Cape Coast Castle not found in legacy response")
    else:
        print(f"❌ Status: {response.status_code}")
        print(f"Error: {response.content}")

if __name__ == "__main__":
    test_cape_coast_api()