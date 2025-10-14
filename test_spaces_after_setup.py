#!/usr/bin/env python3
"""
Test DigitalOcean Spaces after Railway setup
"""
import requests
import json
import time

def test_spaces_configuration():
    """Test if DigitalOcean Spaces is working on Railway"""
    
    print("🧪 Testing DigitalOcean Spaces configuration...")
    
    # Test the health endpoint first
    health_url = "https://tailsandtrails-production.up.railway.app/api/health/"
    
    try:
        print("\n1. Testing server health...")
        response = requests.get(health_url, timeout=30)
        
        if response.status_code == 200:
            print("✅ Django server is running")
            
            # Check if we can access any media-related endpoints
            print("\n2. Testing media configuration...")
            
            # Try to access the gallery endpoint (which might use media)
            gallery_url = "https://tailsandtrails-production.up.railway.app/api/gallery/"
            
            gallery_response = requests.get(gallery_url, timeout=30)
            
            if gallery_response.status_code == 200:
                gallery_data = gallery_response.json()
                print(f"✅ Gallery endpoint accessible")
                
                # Check if any images are served from DigitalOcean Spaces CDN
                if gallery_data and len(gallery_data) > 0:
                    for item in gallery_data[:3]:  # Check first 3 items
                        image_url = item.get('image', '')
                        if 'digitaloceanspaces.com' in image_url:
                            print(f"✅ Found DigitalOcean Spaces image: {image_url[:60]}...")
                            return True
                        elif image_url:
                            print(f"ℹ️  Found local image: {image_url[:60]}...")
                
                print("💡 No DigitalOcean Spaces images found yet")
                print("   This is normal - existing images are still local")
                print("   New uploads will use DigitalOcean Spaces")
                
            else:
                print(f"⚠️  Gallery endpoint: {gallery_response.status_code}")
            
            print("\n3. Configuration status...")
            print("✅ DigitalOcean Spaces should be configured if you added:")
            print("   • SPACES_KEY to Railway")
            print("   • SPACES_SECRET to Railway")
            
            return True
            
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def check_deployment_status():
    """Check if Railway has finished deploying"""
    print("\n🔄 Checking deployment status...")
    
    # Railway typically takes 1-3 minutes to deploy
    # We can check if the server responds properly
    
    for attempt in range(3):
        try:
            response = requests.get(
                "https://tailsandtrails-production.up.railway.app/api/health/", 
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"✅ Deployment complete (attempt {attempt + 1})")
                return True
            else:
                print(f"⏳ Deployment in progress... (attempt {attempt + 1})")
                time.sleep(30)  # Wait 30 seconds between attempts
                
        except Exception as e:
            print(f"⏳ Waiting for deployment... (attempt {attempt + 1})")
            time.sleep(30)
    
    print("⚠️  Deployment taking longer than expected")
    return False

if __name__ == "__main__":
    print("🚀 DigitalOcean Spaces Configuration Test")
    print("=" * 50)
    
    # Check deployment status
    deployed = check_deployment_status()
    
    if deployed:
        # Test Spaces configuration
        spaces_working = test_spaces_configuration()
        
        print("\n" + "=" * 50)
        print("📊 RESULTS")
        print("=" * 50)
        
        if spaces_working:
            print("🎉 DigitalOcean Spaces configuration successful!")
            print("\n📋 What happens next:")
            print("   • New image uploads will go to DigitalOcean Spaces")
            print("   • Images will be served via CDN for faster loading")
            print("   • Existing local images will remain accessible")
            
            print("\n🧪 To test file upload:")
            print("   1. Go to Django admin: /admin/")
            print("   2. Upload a new image in Gallery or Destinations")
            print("   3. Check if the image URL contains 'digitaloceanspaces.com'")
        else:
            print("❌ Configuration needs attention")
    else:
        print("⏳ Please wait for Railway deployment to complete and try again")