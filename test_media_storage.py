#!/usr/bin/env python3
"""
Test media storage configuration
"""
import os
import sys
import django
from pathlib import Path

# Add the Django project to the path
sys.path.append(str(Path(__file__).parent / 'Tback'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def test_media_storage():
    """Test media storage configuration"""
    print("🧪 Testing media storage configuration...")
    
    # Check settings
    print(f"\n📋 Current Configuration:")
    print(f"   DEFAULT_FILE_STORAGE: {getattr(settings, 'DEFAULT_FILE_STORAGE', 'Not set')}")
    print(f"   MEDIA_URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    
    # Check DigitalOcean Spaces settings
    spaces_key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    spaces_secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
    bucket_name = getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None)
    
    print(f"\n🔧 DigitalOcean Spaces Settings:")
    print(f"   Bucket: {bucket_name}")
    print(f"   Access Key: {'✅ Configured' if spaces_key else '❌ Not configured'}")
    print(f"   Secret Key: {'✅ Configured' if spaces_secret else '❌ Not configured'}")
    print(f"   Endpoint: {getattr(settings, 'AWS_S3_ENDPOINT_URL', 'Not set')}")
    print(f"   CDN URL: {getattr(settings, 'MEDIA_URL', 'Not set')}")
    
    # Test storage backend
    print(f"\n🔍 Storage Backend:")
    print(f"   Type: {type(default_storage).__name__}")
    print(f"   Module: {type(default_storage).__module__}")
    
    # Test file operations (only if credentials are configured)
    if spaces_key and spaces_secret:
        print(f"\n🧪 Testing file operations...")
        try:
            # Create a test file
            test_content = "This is a test file for DigitalOcean Spaces"
            test_file = ContentFile(test_content.encode('utf-8'))
            
            # Save the file
            file_name = default_storage.save('test/test_file.txt', test_file)
            print(f"   ✅ File saved: {file_name}")
            
            # Get the URL
            file_url = default_storage.url(file_name)
            print(f"   ✅ File URL: {file_url}")
            
            # Check if file exists
            exists = default_storage.exists(file_name)
            print(f"   ✅ File exists: {exists}")
            
            # Clean up - delete the test file
            default_storage.delete(file_name)
            print(f"   ✅ Test file cleaned up")
            
            print(f"\n🎉 DigitalOcean Spaces is working correctly!")
            return True
            
        except Exception as e:
            print(f"   ❌ Storage test failed: {str(e)}")
            print(f"\n💡 This might be due to:")
            print(f"   • Incorrect API credentials")
            print(f"   • Bucket doesn't exist")
            print(f"   • Network connectivity issues")
            print(f"   • Permissions issues")
            return False
    else:
        print(f"\n⚠️  Spaces credentials not configured - using local storage")
        print(f"   This is normal for development environment")
        return True

def check_environment_variables():
    """Check if environment variables are set"""
    print(f"\n🔍 Environment Variables:")
    
    env_vars = ['SPACES_KEY', 'SPACES_SECRET']
    
    for var in env_vars:
        value = os.getenv(var)
        if value:
            print(f"   {var}: ✅ Set ({value[:10]}...)")
        else:
            print(f"   {var}: ❌ Not set")
    
    return all(os.getenv(var) for var in env_vars)

if __name__ == "__main__":
    print("🚀 DigitalOcean Spaces Media Storage Test")
    print("=" * 50)
    
    # Check environment variables
    env_configured = check_environment_variables()
    
    # Test storage
    storage_working = test_media_storage()
    
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if env_configured and storage_working:
        print("🎉 DigitalOcean Spaces is fully configured and working!")
    elif storage_working:
        print("✅ Storage configuration is working (local fallback)")
        print("💡 Add SPACES_KEY and SPACES_SECRET to use DigitalOcean Spaces")
    else:
        print("❌ Storage configuration has issues")
        print("🔧 Please check your DigitalOcean Spaces setup")