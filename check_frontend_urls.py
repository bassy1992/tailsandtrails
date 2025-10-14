#!/usr/bin/env python
"""
Check what URLs the frontend is actually using
"""
import requests
import re

def check_frontend_urls():
    """Check the deployed frontend to see what API URLs it's using"""
    
    # Common frontend URLs - update these with your actual frontend URL
    frontend_urls = [
        "https://tailsandtrails.vercel.app",
        "https://tfront-nxcxxw7cr-bassys-projects-fca17413.vercel.app", 
        "https://tfront-b30j1teg7-bassys-projects-fca17413.vercel.app",
        # Add your actual frontend URL here
    ]
    
    print("🔍 CHECKING FRONTEND DEPLOYMENT URLs")
    print("=" * 50)
    
    for url in frontend_urls:
        print(f"\n🌐 Checking: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                
                # Look for API URLs in the HTML/JS
                if "tailsandtrails-production.up.railway.app" in content:
                    print("✅ Production API URL found!")
                elif "localhost:8000" in content or "127.0.0.1:8000" in content:
                    print("❌ Local API URLs still present!")
                else:
                    print("🔍 No obvious API URLs found in HTML")
                
                # Check if it's loading properly
                if "Failed to fetch" in content:
                    print("⚠️  May have connection issues")
                    
            else:
                print(f"❌ HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection failed - site may not exist")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n💡 If you see local URLs, the frontend needs to be rebuilt with production environment variables.")
    print(f"💡 Make sure your deployment platform has these environment variables:")
    print(f"   VITE_API_BASE_URL=https://tailsandtrails-production.up.railway.app")
    print(f"   VITE_API_URL=https://tailsandtrails-production.up.railway.app/api")

if __name__ == '__main__':
    check_frontend_urls()