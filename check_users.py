#!/usr/bin/env python
"""
Check existing users in the database
"""
import os
import sys
import django

# Add the Tback directory to Python path
sys.path.append('Tback')
os.chdir('Tback')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

def check_users():
    """Check existing users and their tokens"""
    print("👥 CHECKING EXISTING USERS")
    print("=" * 50)
    
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"\n📧 Email: {user.email}")
        print(f"   Username: {user.username}")
        print(f"   Name: {user.first_name} {user.last_name}")
        print(f"   Active: {user.is_active}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        
        # Check if user has a token
        try:
            token = Token.objects.get(user=user)
            print(f"   Token: {token.key[:20]}...")
        except Token.DoesNotExist:
            print("   Token: None")
            # Create token for user
            token = Token.objects.create(user=user)
            print(f"   Created token: {token.key[:20]}...")
    
    # Create a test user if none exist
    if users.count() == 0:
        print("\n🆕 Creating test user...")
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        token = Token.objects.create(user=user)
        print(f"✅ Created user: {user.email}")
        print(f"   Token: {token.key}")
    
    print("\n" + "=" * 50)
    print("✅ USER CHECK COMPLETE")
    
    # Test login with first user
    if users.exists():
        first_user = users.first()
        print(f"\n🔑 To test login, try:")
        print(f"   Email: {first_user.email}")
        print(f"   Password: [you need to know the password]")
        
        # Reset password for testing
        first_user.set_password('password123')
        first_user.save()
        print(f"✅ Reset password to 'password123' for {first_user.email}")

if __name__ == '__main__':
    check_users()