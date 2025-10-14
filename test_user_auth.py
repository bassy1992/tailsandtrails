#!/usr/bin/env python
"""
Test user authentication and dashboard data
"""
import requests
import json

def test_user_authentication():
    """Test user authentication and dashboard endpoints"""
    base_url = 'http://localhost:8000/api'
    
    print("🔐 Testing User Authentication & Dashboard")
    print("=" * 60)
    
    # Test user login
    login_data = {
        'email': 'admin@example.com',
        'password': 'password123'
    }
    
    try:
        # Try to login
        response = requests.post(f'{base_url}/auth/login/', json=login_data)
        print(f"🔑 Login attempt: {response.status_code}")
        
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data['token']
            user = auth_data['user']
            
            print(f"✅ Login successful!")
            print(f"   User: {user['first_name']} {user['last_name']} ({user['email']})")
            print(f"   Token: {token[:20]}...")
            
            # Test dashboard endpoints with token
            headers = {
                'Authorization': f'Token {token}',
                'Content-Type': 'application/json'
            }
            
            dashboard_endpoints = [
                ('Overview', '/dashboard/overview/'),
                ('Bookings', '/dashboard/bookings/'),
                ('Activity', '/dashboard/activity/')
            ]
            
            for name, endpoint in dashboard_endpoints:
                try:
                    response = requests.get(f'{base_url}{endpoint}', headers=headers)
                    print(f"📊 {name}: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, dict):
                            print(f"   ✅ Data keys: {list(data.keys())}")
                        elif isinstance(data, list):
                            print(f"   ✅ Data items: {len(data)}")
                        else:
                            print(f"   ✅ Data type: {type(data)}")
                    else:
                        error_text = response.text[:100]
                        print(f"   ❌ Error: {error_text}")
                        
                except Exception as e:
                    print(f"   ❌ Exception: {e}")
            
        elif response.status_code == 400:
            error_data = response.json()
            print(f"❌ Login failed: {error_data}")
            
            # Try to create a test user
            print("\n🆕 Creating test user...")
            register_data = {
                'email': 'wyarquah@gmail.com',
                'username': 'wyarquah',
                'first_name': 'Wyarquah',
                'last_name': 'Test',
                'password': 'password123',
                'password_confirm': 'password123'
            }
            
            reg_response = requests.post(f'{base_url}/auth/register/', json=register_data)
            print(f"📝 Registration: {reg_response.status_code}")
            
            if reg_response.status_code == 201:
                print("✅ User created successfully!")
                # Retry login
                login_response = requests.post(f'{base_url}/auth/login/', json=login_data)
                if login_response.status_code == 200:
                    print("✅ Login successful after registration!")
                    auth_data = login_response.json()
                    print(f"   Token: {auth_data['token'][:20]}...")
            else:
                reg_error = reg_response.json()
                print(f"❌ Registration failed: {reg_error}")
        
        else:
            print(f"❌ Unexpected login status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 SUMMARY:")
    print("- Backend server should be running on http://localhost:8000")
    print("- Frontend should be running on http://localhost:8080 or http://localhost:5173")
    print("- User should be able to login and access dashboard data")
    print("\n💡 If authentication works here but not in frontend:")
    print("1. Check browser console for errors")
    print("2. Verify CORS settings")
    print("3. Check if frontend is using correct API URLs")

if __name__ == '__main__':
    test_user_authentication()