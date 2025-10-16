#!/usr/bin/env python
"""
Test script for pricing tiers functionality
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination, PricingTier
from decimal import Decimal

def test_pricing_functionality():
    """Test the pricing tier functionality"""
    print("🧪 Testing Pricing Tiers Functionality\n")
    
    # Get a destination to test with
    destination = Destination.objects.filter(is_active=True).first()
    
    if not destination:
        print("❌ No active destinations found. Please create some destinations first.")
        return
    
    print(f"📍 Testing with destination: {destination.name}")
    print(f"💰 Base price: GH₵{destination.price}")
    print(f"👥 Max group size: {destination.max_group_size}")
    print()
    
    # Check if destination has pricing tiers
    if not destination.has_tiered_pricing:
        print("⚠️  No pricing tiers found. Creating sample tiers...")
        
        # Create sample pricing tiers
        tiers = [
            {'min': 1, 'max': 1, 'price': destination.price},
            {'min': 2, 'max': 3, 'price': destination.price * Decimal('0.95')},
            {'min': 4, 'max': 6, 'price': destination.price * Decimal('0.90')},
            {'min': 7, 'max': None, 'price': destination.price * Decimal('0.85')},
        ]
        
        for tier in tiers:
            PricingTier.objects.create(
                destination=destination,
                min_people=tier['min'],
                max_people=tier['max'],
                price_per_person=tier['price'].quantize(Decimal('0.01')),
                is_active=True
            )
        
        print("✅ Sample pricing tiers created!")
        print()
    
    # Display all pricing tiers
    print("📊 Current Pricing Tiers:")
    print("-" * 50)
    for tier in destination.get_pricing_tiers_display():
        print(f"  {tier.group_size_display}: GH₵{tier.price_per_person}")
    print()
    
    # Test pricing for different group sizes
    test_group_sizes = [1, 2, 4, 7, 10, 15]
    
    print("🧮 Price Calculation Tests:")
    print("-" * 50)
    for group_size in test_group_sizes:
        if group_size > destination.max_group_size:
            continue
            
        price_per_person = destination.get_price_for_group(group_size)
        total_price = price_per_person * group_size
        
        print(f"  {group_size} people: GH₵{price_per_person} per person = GH₵{total_price} total")
    
    print()
    print("✅ Pricing functionality test completed!")
    
    # Show API endpoint information
    print("\n🔗 API Endpoints:")
    print("-" * 50)
    print(f"  Destination detail: /api/destinations/{destination.id}/")
    print(f"  Pricing endpoint: /api/destinations/{destination.id}/pricing/?group_size=4")
    print()

if __name__ == "__main__":
    test_pricing_functionality()