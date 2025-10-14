#!/usr/bin/env python
"""
Get admin token for image uploads
"""
import requests
import json

def get_admin_token():
    """Get admin authentication token"""
    
    # Production API URL
    api_url = "https://tailsandtrails-production.up.railway.app/api"
    
    print("🔑 ADMIN TOKEN GENERATOR")
    print("=" * 40)
    
    # Get admin credentials
    email = input("Enter admin email: ").strip()
    password = input("Enter admin password: ").strip()
    
    if not email or not password:
        print("❌ Email and password are required!")
        return None
    
    # Login to get token
    login_data = {
        'email': email,
        'password': password
    }
    
    try:
        print("\n🔄 Logging in...")
        response = requests.post(f"{api_url}/auth/login/", json=login_data, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get('token')
            user = result.get('user', {})
            
            print(f"✅ Login successful!")
            print(f"   User: {user.get('first_name', '')} {user.get('last_name', '')}")
            print(f"   Email: {user.get('email', '')}")
            print(f"   Token: {token}")
            
            # Check if user is admin/staff
            if user.get('is_staff') or user.get('is_superuser'):
                print("✅ User has admin privileges")
            else:
                print("⚠️  Warning: User may not have admin privileges for image uploads")
            
            print(f"\n💾 Save this token for image uploads:")
            print(f"   {token}")
            
            return token
            
        else:
            print(f"❌ Login failed: {response.status_code}")
            try:
                error = response.json()
                print(f"   Error: {error}")
            except:
                print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == '__main__':
    get_admin_token()