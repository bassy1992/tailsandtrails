#!/usr/bin/env python
"""
Test script to verify all gallery API endpoints are working correctly
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import json

def test_gallery_endpoints():
    """Test all gallery API endpoints"""
    client = Client()
    
    print("🧪 Testing Gallery API Endpoints")
    print("=" * 50)
    
    # Test 1: Categories endpoint
    print("\n1. Testing /api/gallery/categories/")
    response = client.get('/api/gallery/categories/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Categories found: {len(data)}")
        for cat in data:
            print(f"   - {cat['name']}: {cat['gallery_count']} galleries")
    else:
        print(f"   Error: {response.content}")
    
    # Test 2: Galleries list endpoint
    print("\n2. Testing /api/gallery/galleries/")
    response = client.get('/api/gallery/galleries/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Galleries found: {len(data)}")
        for gallery in data:
            print(f"   - {gallery['title']} ({gallery['location']}): {gallery['image_count']} images")
    else:
        print(f"   Error: {response.content}")
    
    # Test 3: Specific gallery detail
    print("\n3. Testing /api/gallery/galleries/tent-xscape-aburi-gallery/")
    response = client.get('/api/gallery/galleries/tent-xscape-aburi-gallery/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Gallery: {data['title']}")
        print(f"   Location: {data['location']}")
        print(f"   Images: {len(data['images'])}")
        print(f"   Main image: {data['main_image_url']}")
        for i, img in enumerate(data['images'], 1):
            print(f"     {i}. {img['caption']} {'(Main)' if img['is_main'] else ''}")
    else:
        print(f"   Error: {response.content}")
    
    # Test 4: Gallery stats
    print("\n4. Testing /api/gallery/stats/")
    response = client.get('/api/gallery/stats/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Total galleries: {data['total_galleries']}")
        print(f"   Total images: {data['total_images']}")
        print(f"   Featured galleries: {data['featured_galleries']}")
    else:
        print(f"   Error: {response.content}")
    
    # Test 5: Mixed feed
    print("\n5. Testing /api/gallery/feed/")
    response = client.get('/api/gallery/feed/')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Feed items: {len(data['results'])}")
        print(f"   Total galleries: {data['total_galleries']}")
        print(f"   Total videos: {data['total_videos']}")
    else:
        print(f"   Error: {response.content}")
    
    # Test 6: Category filtering
    print("\n6. Testing /api/gallery/galleries/?category=adventure")
    response = client.get('/api/gallery/galleries/?category=adventure')
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Adventure galleries: {len(data)}")
        for gallery in data:
            print(f"   - {gallery['title']}: {gallery['image_count']} images")
    else:
        print(f"   Error: {response.content}")
    
    print("\n" + "=" * 50)
    print("✅ Gallery API endpoint testing completed!")

if __name__ == "__main__":
    test_gallery_endpoints()