#!/usr/bin/env python
"""
Debug login endpoint by making a direct request
"""
import requests
import json

def debug_login():
    """Debug the login endpoint"""
    url = 'http://localhost:8000/api/auth/login/'
    
    # Test data
    test_cases = [
        {'email': 'test@test.com', 'password': 'testpass123'},
        {'email': 'admin@example.com', 'password': 'password123'},
    ]
    
    for i, data in enumerate(test_cases, 1):
        print(f"\n🔍 Test Case {i}: {data['email']}")
        print("-" * 40)
        
        # Try different request methods
        methods = [
            ('POST with JSON', lambda: requests.post(url, json=data)),
            ('POST with form data', lambda: requests.post(url, data=data)),
            ('POST with explicit headers', lambda: requests.post(
                url, 
                json=data, 
                headers={
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            )),
        ]
        
        for method_name, method_func in methods:
            try:
                response = method_func()
                print(f"  {method_name}:")
                print(f"    Status: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"    ✅ Success: {result.get('message', 'No message')}")
                    print(f"    Token: {result.get('token', 'No token')[:20]}...")
                    return result['token']  # Return token if successful
                else:
                    try:
                        error = response.json()
                        print(f"    ❌ Error: {error}")
                    except:
                        print(f"    ❌ Error: {response.text[:100]}")
                        
            except Exception as e:
                print(f"    ❌ Exception: {e}")
    
    return None

if __name__ == '__main__':
    print("🔐 DEBUGGING LOGIN ENDPOINT")
    print("=" * 50)
    
    token = debug_login()
    
    if token:
        print(f"\n✅ Login successful! Testing dashboard endpoints...")
        
        headers = {'Authorization': f'Token {token}'}
        base_url = 'http://localhost:8000/api'
        
        endpoints = [
            '/dashboard/overview/',
            '/dashboard/bookings/',
            '/dashboard/activity/'
        ]
        
        for endpoint in endpoints:
            try:
                response = requests.get(f'{base_url}{endpoint}', headers=headers)
                print(f"📊 {endpoint}: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, dict):
                        print(f"    ✅ Data keys: {list(data.keys())}")
                    elif isinstance(data, list):
                        print(f"    ✅ Data items: {len(data)}")
                else:
                    print(f"    ❌ Error: {response.text[:100]}")
                    
            except Exception as e:
                print(f"    ❌ Exception: {e}")
    else:
        print("\n❌ All login attempts failed!")
        print("\n💡 Possible issues:")
        print("1. CSRF middleware blocking requests")
        print("2. Authentication backend not configured properly")
        print("3. User password not set correctly")
        print("4. Django server not running or accessible")