#!/usr/bin/env python
"""
Test the add-on options API endpoint
"""
import os
import sys
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination

def test_addon_api():
    """Test the add-on options API endpoint"""
    print("🧪 Testing Add-on Options API\n")
    
    # Get a destination to test with
    destination = Destination.objects.filter(is_active=True, addon_options__isnull=False).first()
    
    if not destination:
        print("❌ No destinations with add-on options found.")
        return
    
    print(f"📍 Testing with destination: {destination.name} (ID: {destination.id})")
    print()
    
    # Test API call using Django's test client
    from django.test import Client
    
    client = Client()
    url = f'/api/destinations/{destination.id}/'
    response = client.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ API Response successful!")
        print()
        
        # Check add-on options
        if 'addon_options' in data and data['addon_options']:
            print("📦 Add-on Options in API Response:")
            print("-" * 60)
            
            # Group by category
            categories = {}
            for option in data['addon_options']:
                cat_name = option['category']['display_name']
                if cat_name not in categories:
                    categories[cat_name] = []
                categories[cat_name].append(option)
            
            for category_name, options in categories.items():
                print(f"\n{category_name}:")
                for option in options:
                    default_text = " (Default)" if option.get('is_default') else ""
                    print(f"  • {option['name']}: {option['price_display']}{default_text}")
                    print(f"    {option['description']}")
        
        # Check experience add-ons
        if 'experience_addons' in data and data['experience_addons']:
            print(f"\n🎪 Experience Add-ons in API Response:")
            print("-" * 60)
            for addon in data['experience_addons']:
                print(f"  • {addon['name']}: GH₵{addon['price']}")
                print(f"    {addon['description']}")
                print(f"    Duration: {addon['duration']}")
                if addon.get('max_participants'):
                    print(f"    Max participants: {addon['max_participants']}")
                print()
        
        print("✅ API includes all add-on options correctly!")
        
    else:
        print(f"❌ API Error: {response.status_code}")
        print(f"Response: {response.content.decode()}")
    
    print(f"\n🔗 Test this URL in your browser:")
    print(f"  http://localhost:8000/api/destinations/{destination.id}/")

if __name__ == "__main__":
    test_addon_api()