#!/usr/bin/env python3
"""
Django management script to create superuser in production
Run this in Railway console or production environment
"""
import os
import sys
import django
from django.conf import settings

# Add the project directory to Python path
sys.path.append('/app')  # Railway's app directory

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')

# Setup Django
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Create a superuser interactively"""
    
    print("🚀 Creating Production Superuser")
    print("=" * 40)
    
    # Get user input
    username = input("Username: ")
    email = input("Email: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"❌ User '{username}' already exists!")
        
        # Ask if they want to promote existing user
        promote = input("Do you want to make this user a superuser? (y/n): ")
        if promote.lower() == 'y':
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            print(f"✅ User '{username}' promoted to superuser!")
            return True
        else:
            return False
    
    if User.objects.filter(email=email).exists():
        print(f"❌ Email '{email}' already exists!")
        return False
    
    # Get password
    import getpass
    password = getpass.getpass("Password: ")
    password_confirm = getpass.getpass("Confirm Password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match!")
        return False
    
    try:
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"   ID: {user.id}")
        print(f"   Email: {user.email}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

def create_superuser_non_interactive():
    """Create superuser with predefined values (for automation)"""
    
    # You can modify these values or get them from environment variables
    username = os.getenv('SUPERUSER_USERNAME', 'admin')
    email = os.getenv('SUPERUSER_EMAIL', 'admin@tailsandtrails.com')
    password = os.getenv('SUPERUSER_PASSWORD', 'admin123')
    first_name = os.getenv('SUPERUSER_FIRST_NAME', 'Admin')
    last_name = os.getenv('SUPERUSER_LAST_NAME', 'User')
    
    try:
        # Check if superuser already exists
        if User.objects.filter(username=username).exists():
            print(f"ℹ️ Superuser '{username}' already exists")
            return True
        
        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        print(f"✅ Superuser '{username}' created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        return False

if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) > 1 and sys.argv[1] == '--non-interactive':
        create_superuser_non_interactive()
    else:
        create_superuser()