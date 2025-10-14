#!/usr/bin/env python3
"""
Test Railway DigitalOcean Spaces connection
"""
import os
import sys
import django
import requests

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')
django.setup()

from django.conf import settings

def test_railway_spaces():
    print("🧪 Testing Railway DigitalOcean Spaces Connection")
    print("=" * 60)
    
    # Check if we're using Spaces storage
    storage_backend = settings.DEFAULT_FILE_STORAGE
    print(f"Storage Backend: {storage_backend}")
    
    # Check environment variables
    spaces_key = os.getenv('SPACES_KEY')
    spaces_secret = os.getenv('SPACES_SECRET')
    
    print(f"SPACES_KEY: {'✅ Set' if spaces_key else '❌ Not set'}")
    print(f"SPACES_SECRET: {'✅ Set' if spaces_secret else '❌ Not set'}")
    
    if spaces_key:
        print(f"Key starts with: {spaces_key[:10]}...")
    if spaces_secret:
        print(f"Secret starts with: {spaces_secret[:10]}...")
    
    # Check Django settings
    print(f"\nDjango Spaces Settings:")
    print(f"Bucket: {getattr(settings, 'AWS_STORAGE_BUCKET_NAME', 'Not set')}")
    print(f"Region: {getattr(settings, 'AWS_S3_REGION_NAME', 'Not set')}")
    print(f"Endpoint: {getattr(settings, 'AWS_S3_ENDPOINT_URL', 'Not set')}")
    print(f"ACL: {getattr(settings, 'AWS_DEFAULT_ACL', 'Not set')}")
    print(f"Media URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    
    # Test if we can create a storage instance
    if spaces_key and spaces_secret:
        try:
            from storages.backends.s3boto3 import S3Boto3Storage
            storage = S3Boto3Storage()
            print(f"\n✅ Storage backend initialized successfully")
            print(f"Storage class: {storage.__class__.__name__}")
            return True
        except Exception as e:
            print(f"\n❌ Storage backend failed: {e}")
            return False
    else:
        print(f"\n⚠️  Using fallback storage (credentials not set)")
        return False

if __name__ == "__main__":
    test_railway_spaces()