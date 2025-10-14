#!/usr/bin/env python3
"""
Test direct file upload to DigitalOcean Spaces
"""
import os
import sys
import django
from io import BytesIO

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def test_direct_upload():
    print("🧪 Testing Direct Upload to DigitalOcean Spaces")
    print("=" * 60)
    
    # Check storage backend
    print(f"Storage backend: {default_storage.__class__.__name__}")
    print(f"Storage module: {default_storage.__class__.__module__}")
    
    # Create a test file
    test_content = b"This is a test file for DigitalOcean Spaces upload"
    test_file = ContentFile(test_content, name="test-upload.txt")
    
    try:
        print(f"\n📤 Uploading test file...")
        
        # Save the file using Django's storage system
        file_path = default_storage.save("test-files/test-upload.txt", test_file)
        print(f"✅ Upload successful!")
        print(f"   File path: {file_path}")
        
        # Get the URL
        file_url = default_storage.url(file_path)
        print(f"   File URL: {file_url}")
        
        # Check if file exists
        exists = default_storage.exists(file_path)
        print(f"   File exists: {'✅ Yes' if exists else '❌ No'}")
        
        # Get file size
        if exists:
            size = default_storage.size(file_path)
            print(f"   File size: {size} bytes")
        
        # Try to read the file back
        try:
            with default_storage.open(file_path, 'rb') as f:
                content = f.read()
                print(f"   Content matches: {'✅ Yes' if content == test_content else '❌ No'}")
        except Exception as e:
            print(f"   ❌ Could not read file: {e}")
        
        # Clean up - delete the test file
        try:
            default_storage.delete(file_path)
            print(f"   🗑️  Test file cleaned up")
        except Exception as e:
            print(f"   ⚠️  Could not delete test file: {e}")
            
        return True
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_direct_upload()