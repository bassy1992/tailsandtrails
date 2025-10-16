#!/usr/bin/env python3

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent / 'Tback'
sys.path.insert(0, str(project_root))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.conf import settings

print("🔍 Current Environment Variables:")
print("=" * 50)

# Check key environment variables
env_vars = [
    'FRONTEND_URL',
    'BASE_URL', 
    'PAYSTACK_PUBLIC_KEY',
    'PAYSTACK_SECRET_KEY',
    'DATABASE_URL',
    'SPACES_KEY',
    'SPACES_SECRET'
]

for var in env_vars:
    value = os.getenv(var, 'NOT SET')
    if 'KEY' in var or 'SECRET' in var:
        # Mask sensitive values
        if value != 'NOT SET' and len(value) > 8:
            masked = value[:8] + '...' + value[-4:]
        else:
            masked = value
        print(f"{var}: {masked}")
    else:
        print(f"{var}: {value}")

print("\n🔍 Django Settings Values:")
print("=" * 50)
print(f"FRONTEND_URL: {settings.FRONTEND_URL}")
print(f"BASE_URL: {settings.BASE_URL}")
print(f"DEBUG: {settings.DEBUG}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

print("\n🔍 CORS Configuration:")
print("=" * 50)
print(f"CORS_ALLOWED_ORIGINS: {settings.CORS_ALLOWED_ORIGINS}")