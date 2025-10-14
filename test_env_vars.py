#!/usr/bin/env python3
"""
Test environment variables directly
"""
import os

print("🔍 Environment Variables Test")
print("=" * 40)

# Check all environment variables
env_vars = ['SPACES_KEY', 'SPACES_SECRET', 'DATABASE_URL', 'SECRET_KEY', 'DEBUG']

for var in env_vars:
    value = os.getenv(var)
    if value:
        if var in ['SPACES_KEY', 'SPACES_SECRET']:
            print(f"{var}: {value[:10]}... (length: {len(value)})")
        else:
            print(f"{var}: {'✅ Set' if value else '❌ Not set'}")
    else:
        print(f"{var}: ❌ Not set")

print("=" * 40)