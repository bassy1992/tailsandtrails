#!/usr/bin/env python3
"""
Debug Railway deployment storage configuration
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')

try:
    django.setup()
    from django.conf import settings
    from django.core.files.storage import default_storage
    
    print("🔍 Railway Deployment Debug")
    print("=" * 50)
    
    # Check environment
    print(f"Environment Variables:")
    print(f"  SPACES_KEY: {'✅ Set' if os.getenv('SPACES_KEY') else '❌ Not set'}")
    print(f"  SPACES_SECRET: {'✅ Set' if os.getenv('SPACES_SECRET') else '❌ Not set'}")
    
    # Check Django settings
    print(f"\nDjango Settings:")
    print(f"  DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"  MEDIA_URL: {settings.MEDIA_URL}")
    print(f"  AWS_ACCESS_KEY_ID: {'✅ Set' if settings.AWS_ACCESS_KEY_ID else '❌ Not set'}")
    print(f"  AWS_SECRET_ACCESS_KEY: {'✅ Set' if settings.AWS_SECRET_ACCESS_KEY else '❌ Not set'}")
    
    # Check actual storage
    print(f"\nActual Storage:")
    print(f"  Backend: {default_storage.__class__.__name__}")
    print(f"  Module: {default_storage.__class__.__module__}")
    
    # Check package availability
    print(f"\nPackage Check:")
    try:
        import boto3
        print(f"  ✅ boto3 available: {boto3.__version__}")
    except ImportError as e:
        print(f"  ❌ boto3 not available: {e}")
    
    try:
        import storages
        print(f"  ✅ storages available")
        from storages.backends.s3boto3 import S3Boto3Storage
        print(f"  ✅ S3Boto3Storage importable")
    except ImportError as e:
        print(f"  ❌ storages not available: {e}")
    
    print(f"\n" + "=" * 50)
    
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    import traceback
    traceback.print_exc()