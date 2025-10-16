#!/usr/bin/env python
"""
Test the pricing API endpoint
"""
import os
import sys
import django
import requests
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination

def test_pricing_api():
    """Test the pricing API endpoint"""
    print("🧪 Testing Pricing API Endpoint\n")
    
    # Get a destination to test with
    destination = Destination.objects.filter(is_active=True, pricing_tiers__isnull=False).first()
    
    if not destination:
        print("❌ No destinations with pricing tiers found.")
        return
    
    print(f"📍 Testing with destination: {destination.name} (ID: {destination.id})")
    print(f"💰 Base price: GH₵{destination.price}")
    print()
    
    # Test different group sizes
    test_group_sizes = [1, 2, 4, 7, 10]
    
    print("🧮 API Response Tests:")
    print("-" * 60)
    
    for group_size in test_group_sizes:
        if group_size > destination.max_group_size:
            continue
        
        # Simulate API call (we'll use Django's test client instead of actual HTTP)
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        url = f'/api/destinations/{destination.id}/pricing/'
        response = client.get(url, {'group_size': group_size})
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Group size {group_size}:")
            print(f"    Price per person: GH₵{data['price_per_person']}")
            print(f"    Total price: GH₵{data['total_price']}")
            print(f"    Has tiered pricing: {data['has_tiered_pricing']}")
            print()
        else:
            print(f"  ❌ Error for group size {group_size}: {response.status_code}")
            print(f"     Response: {response.content.decode()}")
            print()
    
    # Test destination detail endpoint
    print("📋 Destination Detail API Test:")
    print("-" * 60)
    
    client = Client()
    url = f'/api/destinations/{destination.id}/'
    response = client.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"  ✅ Destination detail loaded successfully")
        print(f"  Has tiered pricing: {data.get('has_tiered_pricing', False)}")
        print(f"  Number of pricing tiers: {len(data.get('pricing_tiers', []))}")
        
        if data.get('pricing_tiers'):
            print("  Pricing tiers:")
            for tier in data['pricing_tiers']:
                print(f"    - {tier['group_size_display']}: GH₵{tier['price_per_person']}")
    else:
        print(f"  ❌ Error loading destination detail: {response.status_code}")
    
    print("\n✅ API testing completed!")
    print(f"\n🔗 Try these URLs in your browser or API client:")
    print(f"  - Destination detail: http://localhost:8000/api/destinations/{destination.id}/")
    print(f"  - Pricing for 4 people: http://localhost:8000/api/destinations/{destination.id}/pricing/?group_size=4")

if __name__ == "__main__":
    test_pricing_api()