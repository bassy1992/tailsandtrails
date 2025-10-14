#!/usr/bin/env python
"""
Test environment variable loading
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

print("🔍 Environment Variable Test")
print("=" * 40)

# Test Paystack keys
public_key = os.getenv('PAYSTACK_PUBLIC_KEY', '')
secret_key = os.getenv('PAYSTACK_SECRET_KEY', '')

print(f"PAYSTACK_PUBLIC_KEY: {public_key}")
print(f"PAYSTACK_SECRET_KEY: {secret_key}")

if public_key.startswith('pk_test_ad2c643f'):
    print("✅ Public key loaded correctly")
else:
    print("❌ Public key not loaded correctly")

if secret_key.startswith('sk_test_26d017072e1c'):
    print("✅ Secret key loaded correctly")
else:
    print("❌ Secret key not loaded correctly")

# Test Django settings loading
print("\n🔧 Testing Django Settings...")
try:
    import django
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
    django.setup()
    
    from django.conf import settings
    
    django_public = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
    django_secret = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
    
    print(f"Django PAYSTACK_PUBLIC_KEY: {django_public}")
    print(f"Django PAYSTACK_SECRET_KEY: {django_secret}")
    
    if django_public == public_key and django_secret == secret_key:
        print("✅ Django settings loaded correctly")
    else:
        print("❌ Django settings not matching environment")
        
except Exception as e:
    print(f"❌ Django settings test failed: {e}")