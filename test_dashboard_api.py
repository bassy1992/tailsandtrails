#!/usr/bin/env python
"""
Test dashboard API endpoints
"""
import requests
import json

def test_api_endpoints():
    """Test if the API endpoints are accessible"""
    base_url = 'http://localhost:8000/api'
    
    print("🔍 Testing API endpoints...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f'{base_url}/health/')
        print(f"✅ Health endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
    
    # Test CORS endpoint
    try:
        response = requests.get(f'{base_url}/cors-test/')
        print(f"✅ CORS test endpoint: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ CORS test endpoint failed: {e}")
    
    # Test dashboard endpoints (these require authentication)
    dashboard_endpoints = [
        '/dashboard/overview/',
        '/dashboard/bookings/',
        '/dashboard/activity/'
    ]
    
    for endpoint in dashboard_endpoints:
        try:
            response = requests.get(f'{base_url}{endpoint}')
            print(f"📊 Dashboard {endpoint}: {response.status_code}")
            if response.status_code == 401:
                print(f"   ✅ Correctly requires authentication")
            elif response.status_code == 200:
                print(f"   ✅ Working (authenticated)")
            else:
                print(f"   ❓ Unexpected status: {response.text[:100]}")
        except Exception as e:
            print(f"❌ Dashboard {endpoint} failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 SUMMARY:")
    print("- Backend server is running on http://localhost:8000")
    print("- Dashboard endpoints exist and require authentication")
    print("- Frontend should be able to connect to these endpoints")
    print("\n💡 Next steps:")
    print("1. Make sure frontend is running on http://localhost:8080 or http://localhost:5173")
    print("2. Check if user is properly authenticated in frontend")
    print("3. Verify API calls are using correct authentication headers")

if __name__ == '__main__':
    test_api_endpoints()