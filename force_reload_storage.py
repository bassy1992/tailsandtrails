#!/usr/bin/env python3
"""
Force reload Django storage configuration
"""
import os
import sys
import django

# Set environment variables first
os.environ['SPACES_KEY'] = 'DO00996PQ2XCMKJMCADR'
os.environ['SPACES_SECRET'] = 'fhu5MLcQoQ9Fc1Rc3m1mpsTVd8w+kwih48VeRkwXfcg'

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def force_reload_storage():
    print("🔄 Force Reloading Storage Configuration")
    print("=" * 60)
    
    # Force reload settings
    from importlib import reload
    import Tback.tback_api.settings as settings_module
    reload(settings_module)
    
    # Check storage again
    print(f"Storage backend: {default_storage.__class__.__name__}")
    print(f"Storage module: {default_storage.__class__.__module__}")
    
    # Try to create a new storage instance directly
    from storages.backends.s3boto3 import S3Boto3Storage
    
    try:
        s3_storage = S3Boto3Storage()
        print(f"✅ Direct S3 storage created: {s3_storage.__class__.__name__}")
        
        # Test upload with direct S3 storage
        test_content = b"Test file for DigitalOcean Spaces"
        test_file = ContentFile(test_content, name="test-direct.txt")
        
        file_path = s3_storage.save("test-direct-upload.txt", test_file)
        print(f"✅ Direct upload successful: {file_path}")
        
        file_url = s3_storage.url(file_path)
        print(f"✅ File URL: {file_url}")
        
        # Check if file exists in Spaces
        exists = s3_storage.exists(file_path)
        print(f"✅ File exists in Spaces: {exists}")
        
        # Clean up
        s3_storage.delete(file_path)
        print(f"✅ Test file cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct S3 storage failed: {e}")
        return False

if __name__ == "__main__":
    force_reload_storage()