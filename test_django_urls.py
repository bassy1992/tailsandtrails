#!/usr/bin/env python3
"""
Test what URLs Django is actually generating
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')
django.setup()

from django.core.files.storage import default_storage
from django.conf import settings

def test_django_urls():
    print("🔍 Django URL Generation Test")
    print("=" * 50)
    
    # Check storage backend
    print(f"Storage Backend: {default_storage.__class__.__name__}")
    print(f"Storage Module: {default_storage.__class__.__module__}")
    
    # Check settings
    print(f"\nSettings:")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  AWS_LOCATION: {getattr(settings, 'AWS_LOCATION', 'Not set')}")
    print(f"  AWS_STORAGE_BUCKET_NAME: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
    
    # Test URL generation for a sample file
    sample_paths = [
        'destinations/5.jpg',
        'test-file.jpg',
        'gallery/image.png'
    ]
    
    print(f"\nURL Generation Test:")
    for path in sample_paths:
        try:
            url = default_storage.url(path)
            print(f"  {path} → {url}")
        except Exception as e:
            print(f"  {path} → ERROR: {e}")
    
    # Check if we can generate a proper upload path
    print(f"\nUpload Path Test:")
    try:
        test_path = default_storage.get_available_name('test-upload.jpg')
        test_url = default_storage.url(test_path)
        print(f"  Upload path: {test_path}")
        print(f"  Upload URL: {test_url}")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    test_django_urls()