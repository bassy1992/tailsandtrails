#!/usr/bin/env python
"""
Test production API vs local API
"""
import requests
import json

def test_production_vs_local():
    """Compare production and local API responses"""
    
    print("🌐 TESTING PRODUCTION vs LOCAL API")
    print("=" * 60)
    
    # Test production API
    print("\n1. 🚀 PRODUCTION API (Railway)")
    print("URL: https://tailsandtrails-production.up.railway.app/api/gallery/galleries/")
    
    try:
        prod_response = requests.get(
            "https://tailsandtrails-production.up.railway.app/api/gallery/galleries/",
            timeout=10
        )
        
        if prod_response.status_code == 200:
            prod_data = prod_response.json()
            print(f"✅ Status: {prod_response.status_code}")
            print(f"📊 Total galleries: {len(prod_data)}")
            
            # Find Cape Coast Castle
            cape_coast_prod = None
            for gallery in prod_data:
                if "cape" in gallery.get('title', '').lower():
                    cape_coast_prod = gallery
                    break
            
            if cape_coast_prod:
                print(f"\n🏰 Cape Coast Castle (Production):")
                print(f"   Title: {cape_coast_prod.get('title')}")
                print(f"   Image Count: {cape_coast_prod.get('image_count')}")
                print(f"   Has images array: {'images' in cape_coast_prod}")
                print(f"   Main image URL: {cape_coast_prod.get('main_image_url', 'None')[:50]}...")
            else:
                print("❌ Cape Coast Castle not found in production")
                
        else:
            print(f"❌ Status: {prod_response.status_code}")
            print(f"Error: {prod_response.text}")
            
    except Exception as e:
        print(f"❌ Production API Error: {e}")
    
    # Test local API
    print(f"\n2. 🏠 LOCAL API")
    print("URL: http://127.0.0.1:8000/api/gallery/galleries/")
    
    try:
        local_response = requests.get(
            "http://127.0.0.1:8000/api/gallery/galleries/",
            timeout=5
        )
        
        if local_response.status_code == 200:
            local_data = local_response.json()
            print(f"✅ Status: {local_response.status_code}")
            print(f"📊 Total galleries: {len(local_data)}")
            
            # Find Cape Coast Castle
            cape_coast_local = None
            for gallery in local_data:
                if "cape" in gallery.get('title', '').lower():
                    cape_coast_local = gallery
                    break
            
            if cape_coast_local:
                print(f"\n🏰 Cape Coast Castle (Local):")
                print(f"   Title: {cape_coast_local.get('title')}")
                print(f"   Image Count: {cape_coast_local.get('image_count')}")
                print(f"   Has images array: {'images' in cape_coast_local}")
                print(f"   Main image URL: {cape_coast_local.get('main_image_url', 'None')[:50]}...")
            else:
                print("❌ Cape Coast Castle not found locally")
                
        else:
            print(f"❌ Status: {local_response.status_code}")
            
    except Exception as e:
        print(f"❌ Local API Error: {e}")
    
    # Test production detail endpoint
    print(f"\n3. 🔍 PRODUCTION DETAIL API")
    print("URL: https://tailsandtrails-production.up.railway.app/api/gallery/galleries/cape-coast-castle-cape-coast-gallery/")
    
    try:
        prod_detail_response = requests.get(
            "https://tailsandtrails-production.up.railway.app/api/gallery/galleries/cape-coast-castle-cape-coast-gallery/",
            timeout=10
        )
        
        if prod_detail_response.status_code == 200:
            prod_detail_data = prod_detail_response.json()
            print(f"✅ Status: {prod_detail_response.status_code}")
            print(f"🏰 Title: {prod_detail_data.get('title')}")
            print(f"📸 Image Count: {prod_detail_data.get('image_count')}")
            print(f"🖼️ Images Array: {len(prod_detail_data.get('images', []))} images")
            
            if prod_detail_data.get('images'):
                print(f"📝 First image caption: {prod_detail_data['images'][0].get('caption', 'No caption')}")
            
        else:
            print(f"❌ Status: {prod_detail_response.status_code}")
            print(f"Error: {prod_detail_response.text}")
            
    except Exception as e:
        print(f"❌ Production Detail API Error: {e}")
    
    print(f"\n" + "=" * 60)
    print("🎯 DIAGNOSIS:")
    print("If production shows image_count=1 and local shows image_count=6:")
    print("➡️  Production backend needs to be deployed with latest code")
    print("➡️  Frontend is working correctly, just calling outdated API")
    print("\n🚀 SOLUTION:")
    print("1. Deploy backend to Railway")
    print("2. Wait for deployment to complete")
    print("3. Test production API again")
    print("4. Frontend will automatically work with updated API")

if __name__ == "__main__":
    test_production_vs_local()