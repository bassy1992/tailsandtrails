#!/usr/bin/env python
"""
Quick test to check what FRONTEND_URL Railway is using
"""
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

print("🔍 Checking Railway Environment Variables:")
print(f"FRONTEND_URL from env: {os.getenv('FRONTEND_URL', 'NOT SET')}")
print(f"FRONTEND_URL from settings: {settings.FRONTEND_URL}")
print(f"BASE_URL from settings: {settings.BASE_URL}")

print("\n📋 CORS Settings:")
for i, origin in enumerate(settings.CORS_ALLOWED_ORIGINS):
    print(f"  {i+1}. {origin}")

print("\n🔒 CSRF Trusted Origins:")
for i, origin in enumerate(settings.CSRF_TRUSTED_ORIGINS):
    print(f"  {i+1}. {origin}")