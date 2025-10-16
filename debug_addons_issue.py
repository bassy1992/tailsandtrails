#!/usr/bin/env python3
"""
Debug the add-ons loading issue
"""

import requests
import json

def debug_addons_issue():
    """Debug the specific add-ons loading issue"""
    
    print("🔍 Debugging Add-ons Loading Issue...")
    print()
    
    base_url = "https://tailsandtrails-production.up.railway.app"
    
    # Test valid ticket IDs first
    print("✅ Testing valid ticket IDs...")
    for ticket_id in [1, 2]:
        print(f"\n📋 Testing ticket ID {ticket_id}:")
        
        try:
            # Test add-ons endpoint
            url = f"{base_url}/api/tickets/{ticket_id}/addons/?travelers=1"
            print(f"   URL: {url}")
            
            response = requests.get(url, timeout=15)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('success'):
                        categories = data.get('categories', [])
                        ticket_info = data.get('ticket_info', {})
                        print(f"   ✅ Success! Found {len(categories)} categories")
                        print(f"   📋 Ticket: {ticket_info.get('title', 'Unknown')}")
                        print(f"   💰 Price: {ticket_info.get('base_price', 0)} {ticket_info.get('currency', 'USD')}")
                        
                        # Show category details
                        for i, cat in enumerate(categories[:2]):  # Show first 2 categories
                            print(f"   📂 Category {i+1}: {cat.get('name', 'Unknown')} ({len(cat.get('addons', []))} add-ons)")
                    else:
                        print(f"   ❌ API returned success=false: {data.get('error', 'Unknown error')}")
                except json.JSONDecodeError:
                    print(f"   ❌ Invalid JSON response: {response.text[:200]}")
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"   📄 Error details: {error_data}")
                except:
                    print(f"   📄 Raw response: {response.text[:200]}")
                    
        except requests.exceptions.Timeout:
            print(f"   ⏰ Request timeout (15s)")
        except requests.exceptions.ConnectionError:
            print(f"   🔌 Connection error")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
    
    print("\n" + "="*50)
    print("🔍 Testing Frontend API Configuration...")
    
    # Test if the frontend is using the correct API URL
    frontend_url = "https://tailsandtrails.vercel.app"
    try:
        print(f"\n📋 Checking frontend at: {frontend_url}")
        response = requests.get(frontend_url, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # Look for API URL configuration
            if "tailsandtrails-production.up.railway.app" in content:
                print("   ✅ Frontend is configured to use Railway backend")
            else:
                print("   ⚠️  Frontend might not be configured for Railway backend")
                
            # Look for specific error patterns
            if "VITE_API_URL" in content:
                print("   ✅ Frontend has API URL configuration")
            
        else:
            print(f"   ❌ Frontend returned {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error checking frontend: {e}")
    
    print("\n" + "="*50)
    print("🎯 Diagnosis Summary:")
    print("   1. Check if valid ticket IDs (1, 2) work correctly")
    print("   2. Verify frontend is using correct API URL")
    print("   3. Check browser console for specific error details")
    print("   4. Ensure you're testing on the latest deployment")
    print()
    print("💡 Next Steps:")
    print("   • If valid tickets work: Issue is with invalid ticket handling")
    print("   • If valid tickets fail: Backend API issue")
    print("   • Check browser network tab for actual requests")
    print()
    print("✅ Add-ons debugging completed!")

if __name__ == "__main__":
    debug_addons_issue()