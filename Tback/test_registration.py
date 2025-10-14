#!/usr/bin/env python
import os
import django
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from authentication.models import User
from authentication.serializers import UserRegistrationSerializer
from rest_framework.authtoken.models import Token

def test_registration():
    print("Testing user registration...")
    
    # Test data with unique email/username
    import time
    timestamp = str(int(time.time()))
    data = {
        'email': f'test{timestamp}@example.com',
        'username': f'testuser{timestamp}',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpassword123',
        'password_confirm': 'testpassword123'
    }
    
    try:
        # Test serializer
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            print(f"✅ User created successfully!")
            print(f"   ID: {user.id}")
            print(f"   Email: {user.email}")
            print(f"   Name: {user.first_name} {user.last_name}")
            print(f"   Token: {token.key}")
            
            # Clean up
            user.delete()
            print("✅ Test user cleaned up")
            
        else:
            print("❌ Serializer validation failed:")
            print(serializer.errors)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_registration()