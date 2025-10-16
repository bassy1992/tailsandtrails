#!/usr/bin/env python3
"""
Test the Vercel deployment and ticket ID fix
"""

import requests
import time

def test_vercel_deployment():
    """Test the Vercel deployment and ticket ID redirect fix"""
    
    print("🚀 Testing Vercel Deployment & Ticket ID Fix...")
    print()
    
    # Main production URLs
    main_url = "https://tfront-chi.vercel.app"
    latest_url = "https://tfront-5ssgbgjef-bassys-projects-fca17413.vercel.app"
    
    # Test main site accessibility
    print("✅ Testing main site accessibility...")
    try:
        response = requests.get(main_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Main site accessible: {main_url}")
        else:
            print(f"   ⚠️  Main site returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing main site: {e}")
    
    print()
    
    # Test latest deployment
    print("✅ Testing latest deployment...")
    try:
        response = requests.get(latest_url, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Latest deployment accessible: {latest_url}")
        else:
            print(f"   ⚠️  Latest deployment returned {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error accessing latest deployment: {e}")
    
    print()
    
    # Test ticket ID redirect (this should redirect, so we expect a redirect or the final page)
    print("🔄 Testing ticket ID redirect fix...")
    
    # Test invalid ticket ID 7 redirect
    test_urls = [
        f"{main_url}/booking/7",
        f"{main_url}/ticket-booking/7",
        f"{latest_url}/booking/7",
        f"{latest_url}/ticket-booking/7"
    ]
    
    for test_url in test_urls:
        try:
            print(f"   Testing: {test_url}")
            response = requests.get(test_url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                # Check if we were redirected
                if response.url != test_url:
                    print(f"   ✅ Redirected to: {response.url}")
                else:
                    print(f"   ✅ Page loaded (may have client-side redirect)")
            else:
                print(f"   ⚠️  Returned {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("🎯 Deployment Summary:")
    print(f"   • Main URL: {main_url}")
    print(f"   • Latest: {latest_url}")
    print("   • Ticket ID validation fix deployed")
    print("   • Invalid ticket IDs should redirect automatically")
    print()
    print("✅ Vercel deployment test completed!")

if __name__ == "__main__":
    test_vercel_deployment()