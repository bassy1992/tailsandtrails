#!/usr/bin/env python3
"""
Test production API and create admin user
"""
import requests
import json

API_BASE_URL = "https://tailsandtrails-production.up.railway.app"

def test_endpoints():
    """Test various API endpoints to see what's available"""
    
    endpoints = [
        "/",
        "/api/",
        "/admin/",
        "/api/auth/",
        "/api/auth/register/",
        "/api/destinations/",
        "/api/categories/"
    ]
    
    print("🔍 Testing API endpoints...")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            url = f"{API_BASE_URL}{endpoint}"
            response = requests.get(url, timeout=10)
            status = "✅" if response.status_code < 400 else "❌"
            print(f"{status} {endpoint} -> {response.status_code}")
            
            if response.status_code == 200 and endpoint == "/api/":
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"   Response: {response.text[:100]}...")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint} -> Error: {e}")
    
    print("\n" + "=" * 50)

def create_user_via_api():
    """Try to create a user via the registration API"""
    
    user_data = {
        "username": "admin",
        "email": "admin@tailsandtrails.com",
        "first_name": "Admin",
        "last_name": "User",
        "password": "TailsTrails2024!",
        "password_confirm": "TailsTrails2024!"
    }
    
    try:
        print("🔄 Attempting to create user via API...")
        response = requests.post(
            f"{API_BASE_URL}/api/auth/register/",
            json=user_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            print("✅ User created successfully!")
            print(f"Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print("❌ Failed to create user")
            try:
                error = response.json()
                print(f"Error: {json.dumps(error, indent=2)}")
            except:
                print(f"Error response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def check_admin_access():
    """Check if Django admin is accessible"""
    
    try:
        print("🔄 Checking Django admin access...")
        response = requests.get(f"{API_BASE_URL}/admin/", timeout=10)
        
        if response.status_code == 200:
            print("✅ Django admin is accessible!")
            print(f"Admin URL: {API_BASE_URL}/admin/")
            return True
        else:
            print(f"❌ Admin returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access admin: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Production API Test & Admin Creation")
    print("=" * 50)
    
    # Test all endpoints
    test_endpoints()
    
    # Check admin access
    check_admin_access()
    
    # Try to create user
    create_user_via_api()
    
    print("\n📝 Manual Steps:")
    print("1. Access Railway console for your backend project")
    print("2. Run: python create_admin.py")
    print("3. Or run: python manage.py createsuperuser")
    print(f"4. Then access: {API_BASE_URL}/admin/")