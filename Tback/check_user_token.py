#!/usr/bin/env python
"""
Check current token for wyarquah@gmail.com user
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

def check_user_token():
    """Check current token for the user"""
    user_email = 'wyarquah@gmail.com'
    
    try:
        user = User.objects.get(email=user_email)
        print(f"✅ User found: {user.email}")
        print(f"   Name: {user.first_name} {user.last_name}")
        print(f"   Username: {user.username}")
        print(f"   Active: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
        
        # Get or create token
        token, created = Token.objects.get_or_create(user=user)
        print(f"\n🔑 Authentication Token:")
        print(f"   Token: {token.key}")
        print(f"   Created: {'Just now' if created else 'Previously exists'}")
        
        print(f"\n📋 Frontend Setup Instructions:")
        print(f"   1. Open browser developer tools")
        print(f"   2. Go to Application/Storage > Local Storage")
        print(f"   3. Set: auth_token = {token.key}")
        print(f"   4. Set: user = {{'email': '{user.email}', 'name': '{user.first_name} {user.last_name}', 'first_name': '{user.first_name}', 'last_name': '{user.last_name}'}}")
        print(f"   5. Refresh dashboard page")
        
        print(f"\n🌐 Or use the debug tool:")
        print(f"   Open: Tfront/debug_token.html")
        print(f"   Click: 'Set Test Token' button")
        
        return token.key
        
    except User.DoesNotExist:
        print(f"❌ User {user_email} not found")
        return None

if __name__ == '__main__':
    check_user_token()