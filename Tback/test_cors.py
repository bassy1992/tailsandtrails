#!/usr/bin/env python
"""
Test CORS configuration
"""
import requests
import json

def test_cors_endpoints():
    """Test various endpoints for CORS issues"""
    
    print("🧪 Testing CORS Configuration")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    origin = "http://localhost:8080"
    
    headers = {
        'Origin': origin,
        'Content-Type': 'application/json',
    }
    
    endpoints_to_test = [
        ('GET', '/api/health/', 'Health Check'),
        ('GET', '/api/cors-test/', 'CORS Test'),
        ('GET', '/api/payments/checkout/methods/', 'Payment Methods'),
        ('GET', '/api/auth/profile/', 'Auth Profile'),
        ('POST', '/api/auth/login/', 'Auth Login'),
    ]
    
    print(f"Testing from origin: {origin}")
    print()
    
    for method, endpoint, description in endpoints_to_test:
        try:
            url = f"{base_url}{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'POST':
                # For POST requests, send minimal data
                test_data = {'test': 'data'} if 'login' in endpoint else {}
                response = requests.post(url, headers=headers, json=test_data)
            
            # Check response
            status_code = response.status_code
            cors_header = response.headers.get('Access-Control-Allow-Origin', 'Not present')
            
            if status_code < 400:
                status_icon = "✅"
            elif status_code == 401 or status_code == 403:
                status_icon = "🔐"  # Auth required, but CORS working
            else:
                status_icon = "❌"
            
            print(f"{status_icon} {description}")
            print(f"   URL: {endpoint}")
            print(f"   Status: {status_code}")
            print(f"   CORS Header: {cors_header}")
            print()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ {description}")
            print(f"   URL: {endpoint}")
            print(f"   Error: {str(e)}")
            print()
    
    print("🔍 CORS Test Summary:")
    print("✅ = Working correctly")
    print("🔐 = Auth required (CORS working)")
    print("❌ = CORS or connection issue")

def test_preflight_request():
    """Test OPTIONS preflight request"""
    
    print("\n🚀 Testing Preflight (OPTIONS) Request")
    print("=" * 40)
    
    url = "http://127.0.0.1:8000/api/auth/login/"
    headers = {
        'Origin': 'http://localhost:8080',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type, Authorization',
    }
    
    try:
        response = requests.options(url, headers=headers)
        
        print(f"Status: {response.status_code}")
        print(f"Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'Not present')}")
        print(f"Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'Not present')}")
        print(f"Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'Not present')}")
        
        if response.status_code == 200 and 'Access-Control-Allow-Origin' in response.headers:
            print("✅ Preflight request working correctly")
        else:
            print("❌ Preflight request failed")
            
    except Exception as e:
        print(f"❌ Preflight test error: {str(e)}")

if __name__ == "__main__":
    print("CORS Configuration Test")
    print("Make sure Django server is running on localhost:8000")
    print()
    
    test_cors_endpoints()
    test_preflight_request()
    
    print("\n🎯 Next Steps:")
    print("1. If tests show ✅ or 🔐, CORS is working")
    print("2. If tests show ❌, check Django server logs")
    print("3. Restart Django server after CORS changes")
    print("4. Clear browser cache and try frontend again")