#!/usr/bin/env python
"""
Script to create Tent Xcape destination with proper dates
"""
import os
import sys
import django
from datetime import datetime
from decimal import Decimal

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination, Category, DestinationHighlight, DestinationInclude

def create_tent_xcape():
    """Create Tent Xcape destination"""
    
    # Get or create category
    category, _ = Category.objects.get_or_create(
        name='Adventure',
        defaults={
            'description': 'Outdoor adventure and camping experiences'
        }
    )
    
    # Create or update Tent Xcape destination
    destination, created = Destination.objects.update_or_create(
        slug='tent-xcape',
        defaults={
            'name': 'Tent Xcape',
            'location': 'Aburi Mountains, Eastern Region',
            'description': 'Experience the ultimate camping adventure at Tent Xcape! Nestled in the scenic Aburi Mountains, enjoy breathtaking views, outdoor activities, and a memorable escape from city life. Perfect for families, friends, and adventure seekers.',
            'image': 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800',
            'price': Decimal('350.00'),
            'duration': '3_days',
            'max_group_size': 20,
            'start_date': datetime(2025, 12, 19).date(),
            'end_date': datetime(2025, 12, 21).date(),
            'rating': Decimal('4.8'),
            'reviews_count': 45,
            'category': category,
            'is_active': True,
            'is_featured': True,
        }
    )
    
    if created:
        print(f"✓ Created new destination: {destination.name}")
        
        # Add highlights
        highlights = [
            'Mountain camping experience',
            'Bonfire and stargazing',
            'Hiking trails and nature walks',
            'Local cuisine and BBQ',
            'Team building activities',
        ]
        
        for i, highlight in enumerate(highlights):
            DestinationHighlight.objects.create(
                destination=destination,
                highlight=highlight,
                order=i
            )
        
        # Add includes
        includes = [
            'Camping equipment and tents',
            'All meals (breakfast, lunch, dinner)',
            'Professional guides',
            'Transportation from Accra',
            'Activity equipment',
            'First aid and safety gear',
        ]
        
        for i, item in enumerate(includes):
            DestinationInclude.objects.create(
                destination=destination,
                item=item,
                order=i
            )
        
        print(f"  Added {len(highlights)} highlights")
        print(f"  Added {len(includes)} includes")
    else:
        print(f"✓ Updated existing destination: {destination.name}")
    
    print(f"\nDestination Details:")
    print(f"  Name: {destination.name}")
    print(f"  Slug: {destination.slug}")
    print(f"  Start Date: {destination.start_date}")
    print(f"  End Date: {destination.end_date}")
    print(f"  Duration: {destination.duration_display}")
    print(f"  Price: GH₵{destination.price}")
    print(f"  Location: {destination.location}")
    print(f"\n✅ Tent Xcape is ready!")
    print(f"   URL: https://www.talesandtrailsghana.com/tour/tent-xcape")
    print(f"   Booking URL: https://www.talesandtrailsghana.com/booking/tent-xcape")

if __name__ == '__main__':
    print("Creating Tent Xcape destination...\n")
    create_tent_xcape()
