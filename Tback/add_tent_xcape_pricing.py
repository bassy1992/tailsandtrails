#!/usr/bin/env python
"""
Quick script to add Tent Xcape pricing tiers
Run on Railway: railway run python Tback/add_tent_xcape_pricing.py
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

def add_pricing():
    """Add pricing tiers for Tent Xcape"""
    try:
        destination = Destination.objects.get(slug='tent-xcape')
        print(f"Found destination: {destination.name}")
        
        # Clear existing pricing tiers
        existing = destination.pricing_tiers.all().delete()
        print(f"Cleared {existing[0] if existing else 0} existing tiers")
        
        # Create pricing tiers
        tiers = [
            (1, 1, Decimal('1200.00')),
            (2, 2, Decimal('2100.00')),
            (3, 3, Decimal('2850.00')),
            (4, 4, Decimal('3400.00')),
            (5, 10, Decimal('4000.00')),
        ]
        
        for min_p, max_p, price in tiers:
            tier = PricingTier.objects.create(
                destination=destination,
                min_people=min_p,
                max_people=max_p,
                total_price=price
            )
            print(f"✓ Created: {min_p}-{max_p} people = GH₵{price} (GH₵{tier.price_per_person}/person)")
        
        print(f"\n✅ Successfully added {len(tiers)} pricing tiers for {destination.name}!")
        print("\nTest the API:")
        print(f"curl https://tailsandtrails-production.up.railway.app/api/destinations/tent-xcape/")
        
    except Destination.DoesNotExist:
        print("✗ Tent Xcape destination not found!")
        print("Available destinations:")
        for d in Destination.objects.all()[:5]:
            print(f"  - {d.name} (slug: {d.slug})")
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("Adding Tent Xcape pricing tiers...\n")
    add_pricing()
