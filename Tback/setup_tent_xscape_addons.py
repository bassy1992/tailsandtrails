#!/usr/bin/env python
"""
Setup add-ons for Tent Xscape destination
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination, AddOnCategory, AddOnOption, ExperienceAddOn
from decimal import Decimal

def setup_tent_xscape_addons():
    """Setup all add-ons for Tent Xscape destination"""
    print("🎯 Setting up Tent Xscape add-ons...")
    
    # Get Tent Xscape destination
    try:
        tent_xscape = Destination.objects.get(name__icontains="Tent Xscape")
        print(f"✅ Found destination: {tent_xscape.name}")
    except Destination.DoesNotExist:
        print("❌ Tent Xscape destination not found")
        return
    
    # Create or get add-on categories
    categories_data = [
        {
            'name': 'accommodation',
            'display_name': 'Accommodation Options',
            'description': 'Choose your preferred accommodation level',
            'icon': 'hotel',
            'order': 1
        },
        {
            'name': 'transport',
            'display_name': 'Transport Options', 
            'description': 'Select your transportation preferences',
            'icon': 'car',
            'order': 2
        },
        {
            'name': 'meals',
            'display_name': 'Meal Options',
            'description': 'Customize your dining experience',
            'icon': 'utensils',
            'order': 3
        },
        {
            'name': 'medical',
            'display_name': 'Medical & Insurance',
            'description': 'Health and safety coverage options',
            'icon': 'shield',
            'order': 4
        },
        {
            'name': 'experience',
            'display_name': 'Additional Experiences',
            'description': 'Enhance your tour with extra activities',
            'icon': 'camera',
            'order': 5
        }
    ]
    
    print("\n📋 Creating add-on categories...")
    categories = {}
    for cat_data in categories_data:
        category, created = AddOnCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories[cat_data['name']] = category
        status = "Created" if created else "Updated"
        print(f"  {status}: {category.display_name}")
    
    # Create add-on options
    addon_options_data = [
        # Accommodation Options
        {
            'category': 'accommodation',
            'name': 'Standard Hotel',
            'descr