#!/usr/bin/env python3
"""
Diagnose Railway storage configuration
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage

def diagnose_railway_storage():
    print("🔍 Railway Storage Configuration Diagnosis")
    print("=" * 60)
    
    # Check environment variables
    spaces_key = os.getenv('SPACES_KEY')
    spaces_secret = os.getenv('SPACES_SECRET')
    
    print(f"Environment Variables:")
    print(f"  SPACES_KEY: {'✅ Set' if spaces_key else '❌ Not set'}")
    print(f"  SPACES_SECRET: {'✅ Set' if spaces_secret else '❌ Not set'}")
    
    if spaces_key:
        print(f"  Key preview: {spaces_key[:15]}...")
    if spaces_secret:
        print(f"  Secret preview: {spaces_secret[:15]}...")
    
    # Check Django settings
    print(f"\nDjango Settings:")
    print(f"  AWS_ACCESS_KEY_ID: {'✅ Set' if settings.AWS_ACCESS_KEY_ID else '❌ Not set'}")
    print(f"  AWS_SECRET_ACCESS_KEY: {'✅ Set' if settings.AWS_SECRET_ACCESS_KEY else '❌ Not set'}")
    print(f"  AWS_STORAGE_BUCKET_NAME: {settings.AWS_STORAGE_BUCKET_NAME}")
    print(f"  AWS_S3_REGION_NAME: {settings.AWS_S3_REGION_NAME}")
    print(f"  AWS_S3_ENDPOINT_URL: {settings.AWS_S3_ENDPOINT_URL}")
    print(f"  AWS_DEFAULT_ACL: {settings.AWS_DEFAULT_ACL}")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    
    # Check actual storage backend
    print(f"\nActual Storage Backend:")
    print(f"  Class: {default_storage.__class__.__name__}")
    print(f"  Module: {default_storage.__class__.__module__}")
    
    # Check if storages is installed
    try:
        import storages
        print(f"  Storages version: {storages.__version__}")
    except ImportError:
        print(f"  ❌ Storages not installed")
    except AttributeError:
        print(f"  ✅ Storages installed (no version info)")
    
    # Check boto3
    try:
        import boto3
        print(f"  Boto3 version: {boto3.__version__}")
    except ImportError:
        print(f"  ❌ Boto3 not installed")
    
    # Test storage backend creation
    print(f"\nStorage Backend Test:")
    try:
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            from storages.backends.s3boto3 import S3Boto3Storage
            storage = S3Boto3Storage()
            print(f"  ✅ S3Boto3Storage created successfully")
            print(f"  Storage bucket: {storage.bucket_name}")
            print(f"  Storage endpoint: {storage.endpoint_url}")
        else:
            print(f"  ⚠️  Credentials not available, using fallback")
    except Exception as e:
        print(f"  ❌ Storage creation failed: {e}")
    
    # Check the fallback logic
    print(f"\nFallback Logic Check:")
    aws_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    aws_secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    print(f"  AWS_ACCESS_KEY_ID exists: {bool(aws_key)}")
    print(f"  AWS_SECRET_ACCESS_KEY exists: {bool(aws_secret)}")
    print(f"  Should use S3: {bool(aws_key and aws_secret)}")
    
    if not (aws_key and aws_secret):
        print(f"  ⚠️  Fallback to FileSystemStorage triggered!")
        print(f"  This means environment variables aren't being read properly")

if __name__ == "__main__":
    diagnose_railway_storage()