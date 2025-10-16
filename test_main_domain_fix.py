#!/usr/bin/env python3
"""
Test the main production domain with the ticket ID fix
"""

import requests
import time

def test_main_domain_fix():
    """Test the main production domain for the ticket ID fix"""
    
    print("🚀 Testing Main Production Domain Fix...")
    print()
    
    main_domain = "https://tailsandtrails.vercel.app"
    
    # Test main site
    print("✅ Testing main domain accessibility...")
    try:
        response = requests.get(main_domain, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Main domain accessible: {main_domain}")
            
            # Check if it's the new version by looking for specific content
            content = response.text
            if "index-BNIAwRRh.js" in content:
                print("   ⚠️  Still showing old version (cached)")
            else:
                print("   ✅ New version detected")
        else:
            print(f"   ⚠️  Main domain returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing main domain: {e}")
    
    print()
    
    # Test the specific problematic URLs
    print("🔄 Testing problematic ticket ID URLs...")
    
    test_urls = [
        f"{main_domain}/booking/7",
        f"{main_domain}/ticket-booking/7", 
        f"{main_domain}/booking/6",
        f"{main_domain}/ticket-booking/6"
    ]
    
    for test_url in test_urls:
        try:
            print(f"   Testing: {test_url}")
            response = requests.get(test_url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                print(f"   ✅ Page loads successfully")
                if response.url != test_url:
                    print(f"   ✅ Redirected to: {response.url}")
                else:
                    print(f"   ✅ Page loaded (client-side redirect expected)")
            else:
                print(f"   ⚠️  Returned {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("🎯 Cache Clearing Instructions:")
    print("   If you're still seeing the old errors:")
    print("   1. Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)")
    print("   2. Clear browser cache for tailsandtrails.vercel.app")
    print("   3. Open in incognito/private mode")
    print("   4. Wait 5-10 minutes for CDN propagation")
    print()
    print("✅ Main domain test completed!")
    print(f"🌐 Production URL: {main_domain}")

if __name__ == "__main__":
    test_main_domain_fix()