#!/usr/bin/env python3
"""
Debug the frontend API configuration issue
"""

import requests
import json
import re

def debug_frontend_api_issue():
    """Debug the frontend API configuration and add-ons loading"""
    
    print("🔍 Debugging Frontend API Configuration Issue")
    print("=" * 60)
    
    frontend_url = "http://localhost:5173"
    backend_url = "https://tailsandtrails-production.up.railway.app"
    
    # Test 1: Check frontend content for API configuration
    print("✅ Test 1: Frontend API Configuration")
    print("-" * 40)
    
    try:
        response = requests.get(frontend_url, timeout=15)
        if response.status_code == 200:
            content = response.text
            
            # Look for API URL patterns
            api_patterns = [
                r'VITE_API_URL["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'api["\']?\s*[:=]\s*["\']([^"\']+)["\']',
                r'https://[^"\']*railway[^"\']*',
                r'localhost:8000',
                r'127\.0\.0\.1:8000'
            ]
            
            found_apis = []
            for pattern in api_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                found_apis.extend(matches)
            
            if found_apis:
                print("   🔍 Found API URLs in frontend:")
                for api in set(found_apis):
                    print(f"      • {api}")
            else:
                print("   ⚠️  No API URLs found in frontend content")
            
            # Check for specific error patterns
            if "Failed to load add-ons" in content:
                print("   ⚠️  'Failed to load add-ons' text found in frontend")
            
            # Check build timestamp or version
            build_patterns = [
                r'index-([a-zA-Z0-9]+)\.js',
                r'assets/index-([a-zA-Z0-9]+)\.js'
            ]
            
            for pattern in build_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    print(f"   📦 Build hash: {matches[0]}")
                    break
            
        else:
            print(f"   ❌ Frontend returned {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error checking frontend: {e}")
    
    # Test 2: Direct API endpoint testing
    print(f"\n✅ Test 2: Direct API Endpoint Testing")
    print("-" * 40)
    
    test_endpoints = [
        f"{backend_url}/api/tickets/1/addons/?travelers=1",
        f"{backend_url}/api/tickets/2/addons/?travelers=1",
        f"{backend_url}/api/tickets/",
        f"{backend_url}/api/health/"
    ]
    
    for endpoint in test_endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            print(f"   {endpoint}")
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'success' in data:
                        print(f"      Success: {data['success']}")
                    if 'categories' in data:
                        print(f"      Categories: {len(data['categories'])}")
                    if 'status' in data:
                        print(f"      Status: {data['status']}")
                except:
                    print(f"      Content: {response.text[:100]}...")
            else:
                print(f"      Error: {response.text[:100]}")
                
        except Exception as e:
            print(f"      Error: {e}")
        print()
    
    # Test 3: CORS and Headers
    print("✅ Test 3: CORS and Headers Check")
    print("-" * 40)
    
    try:
        # Simulate a browser request
        headers = {
            'Origin': frontend_url,
            'Referer': frontend_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(
            f"{backend_url}/api/tickets/1/addons/?travelers=1",
            headers=headers,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   CORS Headers:")
        cors_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Methods',
            'Access-Control-Allow-Headers',
            'Access-Control-Allow-Credentials'
        ]
        
        for header in cors_headers:
            value = response.headers.get(header, 'Not set')
            print(f"      {header}: {value}")
            
    except Exception as e:
        print(f"   ❌ CORS test error: {e}")
    
    # Test 4: Check for rate limiting or blocking
    print(f"\n✅ Test 4: Rate Limiting Check")
    print("-" * 40)
    
    try:
        # Make multiple rapid requests
        for i in range(3):
            response = requests.get(
                f"{backend_url}/api/tickets/1/addons/?travelers=1",
                timeout=5
            )
            print(f"   Request {i+1}: {response.status_code}")
            if response.status_code != 200:
                print(f"      Headers: {dict(response.headers)}")
                break
                
    except Exception as e:
        print(f"   ❌ Rate limiting test error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Diagnosis Results")
    print("=" * 60)
    
    print("🔍 Possible Issues:")
    print("   1. Frontend using cached/wrong API URL")
    print("   2. Browser caching old JavaScript files")
    print("   3. CORS configuration issues")
    print("   4. Network/proxy blocking requests")
    print("   5. Frontend not using latest deployment")
    
    print("\n💡 Troubleshooting Steps:")
    print("   1. Hard refresh browser (Ctrl+Shift+R)")
    print("   2. Clear browser cache completely")
    print("   3. Test in incognito/private mode")
    print("   4. Check browser Network tab for actual requests")
    print("   5. Verify frontend deployment timestamp")
    
    print("\n🔧 Quick Fixes to Try:")
    print("   • Force new Vercel deployment")
    print("   • Check browser console for specific errors")
    print("   • Test with different browser")
    print("   • Verify API URL in browser dev tools")
    
    print("\n✅ Frontend API debugging completed!")

if __name__ == "__main__":
    debug_frontend_api_issue()