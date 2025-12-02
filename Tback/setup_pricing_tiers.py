#!/usr/bin/env python
"""
Script to set up tiered pricing for destinations
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination, PricingTier

def setup_tent_xcape_pricing():
    """Set up pricing for Tent Xcape"""
    try:
        destination = Destination.objects.get(slug='tent-xcape')
        
        # Clear existing pricing tiers
        destination.pricing_tiers.all().delete()
        
        # Create pricing tiers
        pricing_data = [
            {'min': 1, 'max': 1, 'total': Decimal('1200.00')},
            {'min': 2, 'max': 2, 'total': Decimal('2100.00')},
            {'min': 3, 'max': 3, 'total': Decimal('2850.00')},  # Example: GH₵950 per person
            {'min': 4, 'max': 4, 'total': Decimal('3400.00')},  # Example: GH₵850 per person
            {'min': 5, 'max': 10, 'total': Decimal('4000.00')}, # Example: GH₵800 per person for 5+
        ]
        
        for tier in pricing_data:
            PricingTier.objects.create(
                destination=destination,
                min_people=tier['min'],
                max_people=tier['max'],
                total_price=tier['total']
            )
        
        print(f"✓ Set up pricing tiers for {destination.name}")
        print(f"  1 person: GH₵1,200")
        print(f"  2 people: GH₵2,100 (GH₵1,050 per person)")
        print(f"  3 people: GH₵2,850 (GH₵950 per person)")
        print(f"  4 people: GH₵3,400 (GH₵850 per person)")
        print(f"  5-10 people: GH₵4,000 (GH₵800 per person)")
        
    except Destination.DoesNotExist:
        print("✗ Tent Xcape destination not found. Please create it first.")

def setup_other_destinations():
    """Set up example pricing for other destinations"""
    
    # Example: Cape Coast Castle
    try:
        destination = Destination.objects.get(slug='cape-coast-castle')
        destination.pricing_tiers.all().delete()
        
        pricing_data = [
            {'min': 1, 'max': 1, 'total': Decimal('800.00')},
            {'min': 2, 'max': 2, 'total': Decimal('1400.00')},
            {'min': 3, 'max': 5, 'total': Decimal('1800.00')},
            {'min': 6, 'max': 10, 'total': Decimal('2400.00')},
        ]
        
        for tier in pricing_data:
            PricingTier.objects.create(
                destination=destination,
                min_people=tier['min'],
                max_people=tier['max'],
                total_price=tier['total']
            )
        
        print(f"\n✓ Set up pricing tiers for {destination.name}")
        
    except Destination.DoesNotExist:
        print("\n✗ Cape Coast Castle not found, skipping...")
    
    # Example: Kakum National Park
    try:
        destination = Destination.objects.get(slug='kakum-national-park')
        destination.pricing_tiers.all().delete()
        
        pricing_data = [
            {'min': 1, 'max': 1, 'total': Decimal('600.00')},
            {'min': 2, 'max': 2, 'total': Decimal('1000.00')},
            {'min': 3, 'max': 5, 'total': Decimal('1350.00')},
            {'min': 6, 'max': 10, 'total': Decimal('1800.00')},
        ]
        
        for tier in pricing_data:
            PricingTier.objects.create(
                destination=destination,
                min_people=tier['min'],
                max_people=tier['max'],
                total_price=tier['total']
            )
        
        print(f"✓ Set up pricing tiers for {destination.name}")
        
    except Destination.DoesNotExist:
        print("✗ Kakum National Park not found, skipping...")

if __name__ == '__main__':
    print("Setting up tiered pricing for destinations...\n")
    setup_tent_xcape_pricing()
    setup_other_destinations()
    print("\n✅ Pricing setup complete!")
    print("\nYou can now:")
    print("1. View pricing in Django admin: /admin/destinations/pricingtier/")
    print("2. Edit pricing for each destination")
    print("3. Add pricing tiers for more destinations")
