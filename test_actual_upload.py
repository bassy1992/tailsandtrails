#!/usr/bin/env python3
"""
Test actual file upload to verify storage backend
"""
import os
import sys
import django
from io import BytesIO
from PIL import Image

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.tback_api.settings')
sys.path.append('Tback')
django.setup()

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

def test_actual_upload():
    print("🧪 Testing Actual File Upload")
    print("=" * 50)
    
    # Check current storage configuration
    print(f"Storage Backend: {default_storage.__class__.__name__}")
    print(f"Storage Module: {default_storage.__class__.__module__}")
    print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    
    # Check credentials
    print(f"AWS_ACCESS_KEY_ID: {'✅ Set' if settings.AWS_ACCESS_KEY_ID else '❌ Not set'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'✅ Set' if settings.AWS_SECRET_ACCESS_KEY else '❌ Not set'}")
    
    # Create a test image file
    print(f"\n📤 Creating and uploading test image...")
    
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Create Django file
    test_file = ContentFile(img_buffer.getvalue(), name='test-upload.png')
    
    try:
        # Upload the file
        file_path = default_storage.save('test-uploads/test-image.png', test_file)
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
        
        # Determine if this went to S3 or local storage
        if 'digitaloceanspaces.com' in file_url:
            print(f"   🎉 File uploaded to DigitalOcean Spaces!")
        else:
            print(f"   ⚠️  File uploaded to local storage")
        
        # Don't delete the file so we can verify it exists in Spaces
        print(f"   📝 File left in storage for verification")
        
        return file_path, file_url
        
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        return None, None

if __name__ == "__main__":
    # Set credentials for testing
    os.environ['SPACES_KEY'] = 'DO00996PQ2XCMKJMCADR'
    os.environ['SPACES_SECRET'] = 'fhu5MLcQoQ9Fc1Rc3m1mpsTVd8w+kwih48VeRkwXfcg'
    
    test_actual_upload()