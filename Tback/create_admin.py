#!/usr/bin/env python
"""
Simple script to create admin user for production
Run this on Railway console: python create_admin.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    # Admin user details
    username = 'admin'
    email = 'admin@tailsandtrails.com'
    password = 'TailsTrails2024!'
    first_name = 'Admin'
    last_name = 'User'
    
    try:
        # Check if admin already exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f"User '{username}' already exists!")
            
            # Make sure they're superuser
            if not user.is_superuser:
                user.is_superuser = True
                user.is_staff = True
                user.save()
                print(f"✅ User '{username}' promoted to superuser!")
            else:
                print(f"✅ User '{username}' is already a superuser!")
            
            return user
        
        # Create new superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        print(f"✅ Superuser created successfully!")
        print(f"Username: {username}")
        print(f"Email: {email}")
        print(f"Password: {password}")
        print(f"Admin URL: https://tailsandtrails-production.up.railway.app/admin/")
        
        return user
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == '__main__':
    print("🚀 Creating admin user for production...")
    create_admin()