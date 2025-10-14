#!/usr/bin/env python
"""
Test dashboard API for wyarquah@gmail.com user
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

def get_user_token(email):
    """Get or create token for specified user"""
    try:
        user = User.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        print(f"✓ Using token for user: {user.email}")
        return token.key, user
    except User.DoesNotExist:
        print(f"❌ User {email} not found")
        return None, None

def test_dashboard_for_user(email):
    """Test dashboard endpoints for specific user"""
    token, user = get_user_token(email)
    if not token:
        return
    
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }
    
    base_url = 'http://localhost:8000/api/dashboard'
    
    print("="*70)
    print(f"TESTING DASHBOARD FOR: {email}")
    print("="*70)
    
    # Test overview endpoint
    print("\n📊 DASHBOARD OVERVIEW:")
    print("-" * 40)
    try:
        response = requests.get(f'{base_url}/overview/', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   📈 Total Bookings: {data.get('total_bookings', 0)}")
            print(f"   🌍 Destinations Visited: {data.get('destinations_visited', 0)}")
            print(f"   💰 Total Spent: GH₵{data.get('total_spent', 0)}")
            print(f"   🏆 Member Level: {data.get('member_level', 'N/A')}")
            print(f"   🎯 Points: {data.get('points', 0)}")
            print(f"   📅 Member Since: {data.get('member_since', 'N/A')[:10]}")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test bookings endpoint
    print("\n📅 BOOKINGS & TICKETS:")
    print("-" * 40)
    try:
        response = requests.get(f'{base_url}/bookings/', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   Found {len(data)} bookings/tickets:")
            
            for i, booking in enumerate(data, 1):
                status_emoji = {
                    'confirmed': '✅',
                    'pending': '⏳',
                    'completed': '✔️',
                    'cancelled': '❌'
                }.get(booking['status'], '❓')
                
                type_emoji = '🏞️' if booking['type'] == 'destination' else '🎫'
                
                print(f"   {i}. {type_emoji} {booking['destination']}")
                print(f"      {status_emoji} Status: {booking['status']} | Amount: {booking['amount']}")
                print(f"      📅 Date: {booking['date']} | 👥 Participants: {booking['participants']}")
                print()
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test activity endpoint
    print("\n📋 RECENT ACTIVITY:")
    print("-" * 40)
    try:
        response = requests.get(f'{base_url}/activity/', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"   Found {len(data)} recent activities:")
            
            for i, activity in enumerate(data, 1):
                activity_emoji = '🏞️' if activity['type'] == 'booking' else '🎫'
                status_emoji = {
                    'confirmed': '✅',
                    'pending': '⏳',
                    'completed': '✔️',
                    'cancelled': '❌'
                }.get(activity['status'], '❓')
                
                print(f"   {i}. {activity_emoji} {activity['title']}")
                print(f"      {status_emoji} Status: {activity['status']}")
                print(f"      📅 Date: {activity['date'][:10]}")
                print(f"      🔗 Reference: {activity['reference']}")
                print()
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("="*70)
    print("✅ DASHBOARD TESTING COMPLETE")
    print("="*70)
    print(f"🔑 Token: {token}")
    print("🌐 Dashboard URL: http://localhost:8080/dashboard")
    print("🔗 API Base URL: http://localhost:8000/api/dashboard/")

if __name__ == '__main__':
    test_dashboard_for_user('wyarquah@gmail.com')