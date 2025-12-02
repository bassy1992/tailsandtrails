#!/usr/bin/env python
"""
Script to add "No Transport" option to Tent Xcape
Run on Railway: railway run python Tback/add_no_transport_option.py
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination, AddOnCategory, AddOnOption

def add_no_transport_option():
    """Add 'No Transport' option to transport categories for Tent Xcape"""
    try:
        # Get Tent Xcape destination
        destination = Destination.objects.get(slug='tent-xcape')
        print(f"Found destination: {destination.name}")
        
        # Get transport categories
        transport_categories = AddOnCategory.objects.filter(
            name__in=['transport', 'group_transport']
        )
        
        if not transport_categories.exists():
            print("✗ No transport categories found")
            print("\nAvailable categories:")
            for cat in AddOnCategory.objects.all():
                print(f"  - {cat.name}: {cat.display_name}")
            return
        
        added_count = 0
        for category in transport_categories:
            # Check if "No Transport" already exists
            existing = AddOnOption.objects.filter(
                destination=destination,
                category=category,
                name__icontains='no transport'
            ).first()
            
            if existing:
                print(f"✓ 'No Transport' already exists for {category.display_name}")
                continue
            
            # Create "No Transport" option
            no_transport = AddOnOption.objects.create(
                destination=destination,
                category=category,
                name='No Transport',
                description='I will arrange my own transportation',
                price=Decimal('0.00'),
                pricing_type='per_person',
                is_default=True,  # Make it the default option
                is_active=True,
                order=0  # Show it first
            )
            
            print(f"✓ Added 'No Transport' to {category.display_name}")
            print(f"  - Price: GH₵{no_transport.price}")
            print(f"  - Default: {no_transport.is_default}")
            print(f"  - Order: {no_transport.order}")
            added_count += 1
        
        if added_count > 0:
            print(f"\n✅ Successfully added {added_count} 'No Transport' option(s)!")
        else:
            print("\n✅ All transport categories already have 'No Transport' option")
        
        # Show all transport options for Tent Xcape
        print(f"\n📋 All transport options for {destination.name}:")
        all_options = AddOnOption.objects.filter(
            destination=destination,
            category__name__in=['transport', 'group_transport']
        ).order_by('category__name', 'order', 'name')
        
        for option in all_options:
            default_marker = " (DEFAULT)" if option.is_default else ""
            print(f"  [{option.category.display_name}] {option.name} - GH₵{option.price}{default_marker}")
        
    except Destination.DoesNotExist:
        print("✗ Tent Xcape destination not found!")
        print("\nAvailable destinations:")
        for d in Destination.objects.all()[:5]:
            print(f"  - {d.name} (slug: {d.slug})")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("Adding 'No Transport' option to Tent Xcape...\n")
    add_no_transport_option()
