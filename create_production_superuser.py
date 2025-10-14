#!/usr/bin/env python3
"""
Script to create a superuser for production Django backend on Railway
"""
import requests
import json

# Production API URL
API_BASE_URL = "https://tailsandtrails-production.up.railway.app"

def create_superuser():
    """Create a superuser via the Django admin API"""
    
    print("Creating superuser for production backend...")
    print(f"API URL: {API_BASE_URL}")
    
    # Get user input
    username = input("Enter superuser username: ")
    email = input("Enter superuser email: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    password = input("Enter password: ")
    password_confirm = input("Confirm password: ")
    
    if password != password_confirm:
        print("❌ Passwords don't match!")
        return False
    
    # Registration data
    registration_data = {
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "password_confirm": password_confirm
    }
    
    try:
        # Try to register the user first
        print("\n🔄 Creating user account...")
        response = requests.post(
            f"{API_BASE_URL}/api/auth/register/",
            json=registration_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ User created successfully!")
            print(f"User ID: {result['user']['id']}")
            print(f"Username: {result['user']['username']}")
            print(f"Email: {result['user']['email']}")
            
            # Note: To make this user a superuser, you'll need to access the Django admin
            # or use Railway's console to run: python manage.py shell
            print("\n📝 To make this user a superuser:")
            print("1. Access Railway console for your backend")
            print("2. Run: python manage.py shell")
            print("3. Execute:")
            print(f"   from django.contrib.auth.models import User")
            print(f"   user = User.objects.get(username='{username}')")
            print(f"   user.is_superuser = True")
            print(f"   user.is_staff = True")
            print(f"   user.save()")
            
            return True
            
        else:
            print(f"❌ Failed to create user: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {json.dumps(error_data, indent=2)}")
            except:
                print(f"Error response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_api_connection():
    """Test if the API is accessible"""
    try:
        print("🔄 Testing API connection...")
        response = requests.get(f"{API_BASE_URL}/api/", timeout=10)
        if response.status_code == 200:
            print("✅ API is accessible")
            return True
        else:
            print(f"⚠️ API returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to API: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Production Superuser Creation Tool")
    print("=" * 50)
    
    # Test API connection first
    if not test_api_connection():
        print("\n❌ Cannot proceed without API connection")
        exit(1)
    
    # Create superuser
    success = create_superuser()
    
    if success:
        print("\n🎉 User creation completed!")
        print("Remember to promote the user to superuser using Railway console.")
    else:
        print("\n❌ User creation failed!")