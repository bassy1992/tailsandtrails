#!/usr/bin/env python
"""
Force reload environment variables in running Django instance
"""
import os
import sys
import django
from dotenv import load_dotenv

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')

# Force reload environment
load_dotenv('.env', override=True)

django.setup()

from django.conf import settings

# Update Django settings at runtime (not recommended for production)
settings.PAYSTACK_PUBLIC_KEY = os.getenv('PAYSTACK_PUBLIC_KEY', '')
settings.PAYSTACK_SECRET_KEY = os.getenv('PAYSTACK_SECRET_KEY', '')

print("🔄 Environment Variables Force Reloaded")
print(f"Public Key: {settings.PAYSTACK_PUBLIC_KEY[:20]}...")
print(f"Secret Key: {settings.PAYSTACK_SECRET_KEY[:20]}...")

# Test the API endpoint
import requests
try:
    response = requests.get('http://localhost:8000/api/payments/paystack/config/')
    if response.status_code == 200:
        config = response.json()
        print(f"✅ Config endpoint now returns: {config['public_key'][:20]}...")
    else:
        print(f"❌ Config endpoint error: {response.status_code}")
except Exception as e:
    print(f"❌ Could not test endpoint: {e}")

print("\n🎯 Try your PaystackCheckout.tsx again now!")