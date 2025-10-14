#!/usr/bin/env python
"""
Test dashboard API with proper authentication
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

def get_or_create_token():
    """Get or create token for test user"""
    try:
        user = User.objects.get(email='test@example.com')
        token, created = Token.objects.get_or_create(user=user)
        print(f"Using token for user: {user.email}")
        return token.key
    except User.DoesNotExist:
        print("Test user not found. Please run populate_dashboard_data.py first")
        return None

def test_dashboard_endpoints():
    """Test all dashboard endpoints"""
    token = get_or_create_token()
    if not token:
        return
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }
    
    base_url = 'http://localhost:8000/api/dashboard'
    
    # Test overview endpoint
    print("\n" + "="*60)
    print("TESTING DASHBOARD OVERVIEW")
    print("="*60)
    try:
        response = requests.get(f'{base_url}/overview/', headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Overview Statistics:")
            print(f"  • Total Bookings: {data.get('total_bookings', 0)}")
            print(f"  • Destinations Visited: {data.get('destinations_visited', 0)}")
            print(f"  • Total Spent: GH₵ {data.get('total_spent', 0)}")
            print(f"  • Member Level: {data.get('member_level', 'N/A')}")
            print(f"  • Points: {data.get('points', 0)}")
            print(f"  • Member Since: {data.get('member_since', 'N/A')}")
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test bookings endpoint
    print("\n" + "="*60)
    print("TESTING DASHBOARD BOOKINGS")
    print("="*60)
    try:
        response = requests.get(f'{base_url}/bookings/', headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} bookings/tickets:")
            for i, booking in enumerate(data[:5], 1):  # Show first 5
                print(f"  {i}. {booking['destination']} ({booking['type']})")
                print(f"     Status: {booking['status']} | Amount: {booking['amount']}")
                print(f"     Date: {booking['date']} | Participants: {booking['participants']}")
                print()
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Error: {e}")
    
    # Test activity endpoint
    print("\n" + "="*60)
    print("TESTING DASHBOARD ACTIVITY")
    print("="*60)
    try:
        response = requests.get(f'{base_url}/activity/', headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Found {len(data)} recent activities:")
            for i, activity in enumerate(data[:5], 1):  # Show first 5
                print(f"  {i}. {activity['title']}")
                print(f"     Status: {activity['status']} | Date: {activity['date']}")
                print(f"     Reference: {activity['reference']}")
                print()
        else:
            print("Error:", response.text)
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "="*60)
    print("DASHBOARD API TESTING COMPLETE")
    print("="*60)
    print(f"Token used: {token}")
    print("Dashboard should now be loaded with real data!")

if __name__ == '__main__':
    test_dashboard_endpoints()