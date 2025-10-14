#!/usr/bin/env python
"""
Script to populate the database with sample destinations and tickets data
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Category, Destination, DestinationHighlight, DestinationInclude
from tickets.models import TicketCategory, Venue, Ticket
from decimal import Decimal

def create_sample_data():
    print("Creating sample data...")
    
    # Create Categories
    categories_data = [
        {"name": "Adventure Tours", "description": "Exciting outdoor adventures and activities"},
        {"name": "Cultural Tours", "description": "Explore Ghana's rich cultural heritage"},
        {"name": "Beach & Coastal", "description": "Beautiful beaches and coastal experiences"},
        {"name": "Wildlife & Nature", "description": "Wildlife parks and nature reserves"},
        {"name": "Historical Sites", "description": "Historical landmarks and monuments"},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={"description": cat_data["description"]}
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    # Create Destinations
    destinations_data = [
        {
            "name": "Kakum National Park Canopy Walk",
            "location": "Central Region, Ghana",
            "description": "Experience the thrill of walking through the treetops on suspended bridges 40 meters above the forest floor. Kakum National Park offers one of Africa's most spectacular canopy walks with breathtaking views of the rainforest.",
            "price": Decimal("150.00"),
            "duration": "1_day",
            "max_group_size": 15,
            "category": categories[3],  # Wildlife & Nature
            "rating": Decimal("4.8"),
            "reviews_count": 127,
            "is_featured": True,
            "highlights": [
                "40-meter high canopy walkway",
                "Guided nature walks",
                "Bird watching opportunities",
                "Educational visitor center"
            ],
            "includes": [
                "Professional guide",
                "Park entrance fees",
                "Safety equipment",
                "Transportation from Cape Coast"
            ]
        },
        {
            "name": "Cape Coast Castle Tour",
            "location": "Cape Coast, Central Region",
            "description": "Explore the historic Cape Coast Castle, a UNESCO World Heritage site that played a significant role in the Atlantic slave trade. Learn about Ghana's complex history through guided tours of the dungeons, museums, and exhibitions.",
            "price": Decimal("80.00"),
            "duration": "1_day",
            "max_group_size": 25,
            "category": categories[4],  # Historical Sites
            "rating": Decimal("4.6"),
            "reviews_count": 89,
            "is_featured": True,
            "highlights": [
                "UNESCO World Heritage site",
                "Historical dungeons and chambers",
                "Museum exhibitions",
                "Panoramic ocean views"
            ],
            "includes": [
                "Expert historian guide",
                "Castle entrance fees",
                "Museum access",
                "Audio guide system"
            ]
        },
        {
            "name": "Mole National Park Safari",
            "location": "Northern Region, Ghana",
            "description": "Ghana's largest wildlife refuge offers incredible safari experiences with elephants, antelopes, baboons, and over 300 bird species. Stay at the Mole Motel and enjoy game drives and walking safaris.",
            "price": Decimal("450.00"),
            "duration": "3_days",
            "max_group_size": 8,
            "category": categories[3],  # Wildlife & Nature
            "rating": Decimal("4.7"),
            "reviews_count": 64,
            "is_featured": True,
            "highlights": [
                "Elephant sightings guaranteed",
                "Over 300 bird species",
                "Walking safari experiences",
                "Professional safari guides"
            ],
            "includes": [
                "2 nights accommodation",
                "All meals included",
                "Game drives",
                "Walking safari",
                "Park fees"
            ]
        },
        {
            "name": "Labadi Beach Experience",
            "location": "Accra, Greater Accra Region",
            "description": "Relax at Ghana's most popular beach with golden sand, live music, and vibrant beach culture. Enjoy horseback riding, beach volleyball, and fresh seafood while soaking up the Atlantic sun.",
            "price": Decimal("120.00"),
            "duration": "1_day",
            "max_group_size": 20,
            "category": categories[2],  # Beach & Coastal
            "rating": Decimal("4.3"),
            "reviews_count": 156,
            "is_featured": False,
            "highlights": [
                "Golden sand beach",
                "Live music and entertainment",
                "Horseback riding available",
                "Fresh seafood restaurants"
            ],
            "includes": [
                "Beach access",
                "Welcome drink",
                "Beach chair rental",
                "Local guide"
            ]
        },
        {
            "name": "Kumasi Cultural Heritage Tour",
            "location": "Kumasi, Ashanti Region",
            "description": "Discover the heart of Ashanti culture in Kumasi, the traditional capital. Visit the Manhyia Palace, Kejetia Market, and traditional craft villages to experience authentic Ghanaian culture.",
            "price": Decimal("200.00"),
            "duration": "2_days",
            "max_group_size": 12,
            "category": categories[1],  # Cultural Tours
            "rating": Decimal("4.5"),
            "reviews_count": 73,
            "is_featured": False,
            "highlights": [
                "Manhyia Palace Museum",
                "Largest market in West Africa",
                "Traditional craft villages",
                "Ashanti cultural performances"
            ],
            "includes": [
                "Cultural guide",
                "Palace entrance fees",
                "Traditional lunch",
                "Craft workshop visit"
            ]
        },
        {
            "name": "Volta Region Waterfalls Adventure",
            "location": "Volta Region, Ghana",
            "description": "Explore the stunning Wli Waterfalls, Ghana's highest waterfall, and the beautiful Tagbo Falls. Hike through lush forests, swim in natural pools, and experience the scenic beauty of the Volta Region.",
            "price": Decimal("180.00"),
            "duration": "2_days",
            "max_group_size": 10,
            "category": categories[0],  # Adventure Tours
            "rating": Decimal("4.9"),
            "reviews_count": 91,
            "is_featured": True,
            "highlights": [
                "Ghana's highest waterfall",
                "Natural swimming pools",
                "Forest hiking trails",
                "Butterfly sanctuary visit"
            ],
            "includes": [
                "Hiking guide",
                "Park entrance fees",
                "Picnic lunch",
                "Transportation"
            ]
        }
    ]
    
    # Create destinations
    for dest_data in destinations_data:
        highlights = dest_data.pop('highlights')
        includes = dest_data.pop('includes')
        
        destination, created = Destination.objects.get_or_create(
            name=dest_data["name"],
            defaults=dest_data
        )
        
        if created:
            print(f"Created destination: {destination.name}")
            
            # Add highlights
            for i, highlight in enumerate(highlights):
                DestinationHighlight.objects.create(
                    destination=destination,
                    highlight=highlight,
                    order=i
                )
            
            # Add includes
            for i, include in enumerate(includes):
                DestinationInclude.objects.create(
                    destination=destination,
                    item=include,
                    order=i
                )
    
    # Create Ticket Categories
    ticket_categories_data = [
        {"name": "event", "category_type": "event", "icon": "calendar"},
        {"name": "transport", "category_type": "transport", "icon": "bus"},
        {"name": "attraction", "category_type": "attraction", "icon": "map-pin"},
    ]
    
    ticket_categories = []
    for cat_data in ticket_categories_data:
        category, created = TicketCategory.objects.get_or_create(
            name=cat_data["name"],
            defaults=cat_data
        )
        ticket_categories.append(category)
        if created:
            print(f"Created ticket category: {category.name}")
    
    # Create Venues
    venues_data = [
        {
            "name": "National Theatre of Ghana",
            "address": "Liberation Road, Accra",
            "city": "Accra",
            "region": "Greater Accra",
            "capacity": 1500,
            "description": "Ghana's premier performing arts venue"
        },
        {
            "name": "Accra Sports Stadium",
            "address": "Ohene Djan Sports Stadium",
            "city": "Accra", 
            "region": "Greater Accra",
            "capacity": 40000,
            "description": "National sports stadium hosting major events"
        }
    ]
    
    venues = []
    for venue_data in venues_data:
        venue, created = Venue.objects.get_or_create(
            name=venue_data["name"],
            defaults=venue_data
        )
        venues.append(venue)
        if created:
            print(f"Created venue: {venue.name}")
    
    # Create Sample Tickets
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    tickets_data = [
        {
            "title": "Ghana Music Festival 2024",
            "category": ticket_categories[0],  # event
            "venue": venues[0],  # National Theatre
            "description": "Annual celebration of Ghanaian music featuring top local and international artists",
            "short_description": "Ghana's biggest music festival with amazing performances",
            "price": Decimal("75.00"),
            "total_quantity": 1000,
            "available_quantity": 850,
            "event_date": timezone.now() + timedelta(days=30),
            "sale_start_date": timezone.now() - timedelta(days=10),
            "sale_end_date": timezone.now() + timedelta(days=25),
            "status": "published",
            "is_featured": True,
            "features": ["VIP seating area", "Welcome drink", "Festival merchandise", "Meet & greet opportunity"]
        },
        {
            "title": "Black Stars vs Nigeria - AFCON Qualifier",
            "category": ticket_categories[0],  # event
            "venue": venues[1],  # Sports Stadium
            "description": "Crucial AFCON qualifier match between Ghana Black Stars and Nigeria Super Eagles",
            "short_description": "Ghana vs Nigeria football match",
            "price": Decimal("50.00"),
            "total_quantity": 35000,
            "available_quantity": 28000,
            "event_date": timezone.now() + timedelta(days=45),
            "sale_start_date": timezone.now() - timedelta(days=5),
            "sale_end_date": timezone.now() + timedelta(days=40),
            "status": "published",
            "is_featured": True,
            "features": ["Stadium seating", "Match program", "Pre-match entertainment"]
        }
    ]
    
    for ticket_data in tickets_data:
        ticket, created = Ticket.objects.get_or_create(
            title=ticket_data["title"],
            defaults=ticket_data
        )
        if created:
            print(f"Created ticket: {ticket.title}")
    
    print("\n=== SAMPLE DATA CREATED SUCCESSFULLY ===")
    print(f"Categories: {Category.objects.count()}")
    print(f"Destinations: {Destination.objects.count()}")
    print(f"Ticket Categories: {TicketCategory.objects.count()}")
    print(f"Venues: {Venue.objects.count()}")
    print(f"Tickets: {Ticket.objects.count()}")

if __name__ == "__main__":
    create_sample_data()