#!/usr/bin/env python
"""
Test script for add-on options functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination, AddOnCategory, AddOnOption, ExperienceAddOn

def test_addon_functionality():
    """Test the add-on options functionality"""
    print("🧪 Testing Add-on Options Functionality\n")
    
    # Get a destination to test with
    destination = Destination.objects.filter(is_active=True).first()
    
    if not destination:
        print("❌ No active destinations found.")
        return
    
    print(f"📍 Testing with destination: {destination.name}")
    print()
    
    # Test add-on categories
    categories = AddOnCategory.objects.filter(is_active=True).order_by('order')
    print("📋 Add-on Categories:")
    print("-" * 50)
    for category in categories:
        print(f"  {category.display_name} ({category.name})")
        print(f"    Description: {category.description}")
        print(f"    Icon: {category.icon}")
        print()
    
    # Test add-on options for the destination
    addon_options = destination.addon_options.filter(is_active=True).order_by('category__order', 'order')
    print(f"🎯 Add-on Options for {destination.name}:")
    print("-" * 50)
    
    current_category = None
    for option in addon_options:
        if current_category != option.category.display_name:
            current_category = option.category.display_name
            print(f"\n📦 {current_category}:")
        
        price_display = option.price_display
        default_text = " (Default)" if option.is_default else ""
        print(f"  • {option.name}: {price_display}{default_text}")
        print(f"    {option.description}")
    
    # Test experience add-ons
    experience_addons = destination.experience_addons.filter(is_active=True).order_by('order')
    if experience_addons.exists():
        print(f"\n🎪 Experience Add-ons for {destination.name}:")
        print("-" * 50)
        for addon in experience_addons:
            print(f"  • {addon.name}: GH₵{addon.price}")
            print(f"    {addon.description}")
            print(f"    Duration: {addon.duration}")
            if addon.max_participants:
                print(f"    Max participants: {addon.max_participants}")
            print()
    
    print("✅ Add-on functionality test completed!")
    
    # Show API endpoint information
    print("\n🔗 API Endpoints:")
    print("-" * 50)
    print(f"  Destination detail: /api/destinations/{destination.id}/")
    print(f"  (Includes addon_options and experience_addons)")
    print()
    
    # Show admin information
    print("🔧 Django Admin:")
    print("-" * 50)
    print("  Add-on Categories: /admin/destinations/addoncategory/")
    print("  Add-on Options: /admin/destinations/addonoption/")
    print("  Experience Add-ons: /admin/destinations/experienceaddon/")
    print()

if __name__ == "__main__":
    test_addon_functionality()