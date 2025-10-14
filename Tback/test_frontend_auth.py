#!/usr/bin/env python
"""
Test frontend authentication format for dashboard
"""
import os
import sys
import django
import requests
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

def test_frontend_auth():
    """Test authentication format that frontend uses"""
    user_email = 'wyarquah@gmail.com'
    
    try:
        user = User.objects.get(email=user_email)
        token, created = Token.objects.get_or_create(user=user)
        print(f"✓ User: {user.email}")
        print(f"✓ Token: {token.key}")
    except User.DoesNotExist:
        print(f"❌ User {user_email} not found")
        return
    
    # Test with Token format (correct)
    print("\n🔐 Testing Token authentication (correct format):")
    headers_token = {
        'Authorization': f'Token {token.key}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get('http://localhost:8000/api/dashboard/overview/', headers=headers_token)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Total bookings: {data.get('total_bookings', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test with Bearer format (incorrect)
    print("\n🔐 Testing Bearer authentication (incorrect format):")
    headers_bearer = {
        'Authorization': f'Bearer {token.key}',
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get('http://localhost:8000/api/dashboard/overview/', headers=headers_bearer)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Total bookings: {data.get('total_bookings', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print(f"\n📋 SUMMARY:")
    print(f"   User: {user.email}")
    print(f"   Token: {token.key}")
    print(f"   Correct format: Authorization: Token {token.key}")
    print(f"   Frontend should use: 'Authorization': `Token ${{token}}`")

if __name__ == '__main__':
    test_frontend_auth()