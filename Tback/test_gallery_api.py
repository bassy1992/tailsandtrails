#!/usr/bin/env python
"""
Test script to verify gallery API endpoints
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.test import RequestFactory
from destinations.views import gallery_categories, gallery_images, gallery_videos
from destinations.models import GalleryCategory, GalleryImage, GalleryVideo

def test_gallery_endpoints():
    print("Testing Gallery API Endpoints...\n")
    
    factory = RequestFactory()
    
    # Test categories endpoint
    print("1. Testing /api/gallery/categories/")
    request = factory.get('/api/gallery/categories/')
    response = gallery_categories(request)
    response.render()  # Render the response
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        import json
        data = json.loads(response.content)
        print(f"   Categories found: {len(data)}")
        if data:
            print(f"   Sample: {data[0]['name']}")
    print()
    
    # Test images endpoint
    print("2. Testing /api/gallery/images/")
    request = factory.get('/api/gallery/images/')
    response = gallery_images(request)
    response.render()
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        import json
        data = json.loads(response.content)
        print(f"   Images found: {len(data)}")
        if data:
            print(f"   Sample: {data[0]['title']}")
    print()
    
    # Test images with category filter
    print("3. Testing /api/gallery/images/?category=heritage")
    request = factory.get('/api/gallery/images/?category=heritage')
    response = gallery_images(request)
    response.render()
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        import json
        data = json.loads(response.content)
        print(f"   Heritage images found: {len(data)}")
    print()
    
    # Test featured images
    print("4. Testing /api/gallery/images/?featured=true")
    request = factory.get('/api/gallery/images/?featured=true')
    response = gallery_images(request)
    response.render()
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        import json
        data = json.loads(response.content)
        print(f"   Featured images found: {len(data)}")
    print()
    
    # Test videos endpoint
    print("5. Testing /api/gallery/videos/")
    request = factory.get('/api/gallery/videos/')
    response = gallery_videos(request)
    response.render()
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        import json
        data = json.loads(response.content)
        print(f"   Videos found: {len(data)}")
        if data:
            print(f"   Sample: {data[0]['title']}")
    print()
    
    # Database stats
    print("6. Database Statistics")
    print(f"   Total Categories: {GalleryCategory.objects.count()}")
    print(f"   Total Images: {GalleryImage.objects.count()}")
    print(f"   Featured Images: {GalleryImage.objects.filter(is_featured=True).count()}")
    print(f"   Total Videos: {GalleryVideo.objects.count()}")
    print(f"   Featured Videos: {GalleryVideo.objects.filter(is_featured=True).count()}")
    print()
    
    print("✅ All tests completed!")

if __name__ == '__main__':
    test_gallery_endpoints()
