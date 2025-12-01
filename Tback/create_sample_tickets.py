import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from tickets.models import Ticket, TicketCategory, Venue
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

def create_sample_tickets():
    """Create sample tickets for the frontend"""
    
    print("🎫 CREATING SAMPLE TICKETS")
    print("=" * 50)
    
    # Create categories
    categories_data = [
        {
            'name': 'Cultural Events',
            'slug': 'cultural-events',
            'category_type': 'event',
            'description': 'Traditional and cultural celebrations',
            'icon': 'Calendar',
            'order': 1
        },
        {
            'name': 'Music Concerts',
            'slug': 'music-concerts',
            'category_type': 'event',
            'description': 'Live music performances and concerts',
            'icon': 'Music',
            'order': 2
        },
        {
            'name': 'Sports Events',
            'slug': 'sports-events',
            'category_type': 'event',
            'description': 'Sports matches and competitions',
            'icon': 'Trophy',
            'order': 3
        },
        {
            'name': 'Educational',
            'slug': 'educational',
            'category_type': 'workshop',
            'description': 'Workshops and educational events',
            'icon': 'BookOpen',
            'order': 4
        }
    ]
    
    print("📂 Creating categories...")
    categories = {}
    for cat_data in categories_data:
        category, created = TicketCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categories[cat_data['slug']] = category
        status = "✅ Created" if created else "📋 Exists"
        print(f"   {status}: {category.name}")
    
    # Create venues
    venues_data = [
        {
            'name': 'National Theatre of Ghana',
            'slug': 'national-theatre-accra',
            'address': 'Liberation Road, Accra',
            'city': 'Accra',
            'region': 'Greater Accra',
            'country': 'Ghana',
            'capacity': 1500,
            'description': 'Premier cultural venue in Ghana',
            'contact_phone': '+233302665246',
            'contact_email': 'info@nationaltheatre.gov.gh'
        },
        {
            'name': 'Accra Sports Stadium',
            'slug': 'accra-sports-stadium',
            'address': 'Ohene Djan Sports Stadium, Accra',
            'city': 'Accra',
            'region': 'Greater Accra',
            'country': 'Ghana',
            'capacity': 40000,
            'description': 'National sports stadium of Ghana',
            'contact_phone': '+233302664181',
            'contact_email': 'info@ghanafa.org'
        },
        {
            'name': 'Cape Coast Castle',
            'slug': 'cape-coast-castle',
            'address': 'Cape Coast Castle, Cape Coast',
            'city': 'Cape Coast',
            'region': 'Central Region',
            'country': 'Ghana',
            'capacity': 200,
            'description': 'Historic castle and UNESCO World Heritage Site',
            'contact_phone': '+233332132062',
            'contact_email': 'info@ghanamuseums.org'
        },
        {
            'name': 'University of Ghana Great Hall',
            'slug': 'ug-great-hall',
            'address': 'University of Ghana, Legon',
            'city': 'Accra',
            'region': 'Greater Accra',
            'country': 'Ghana',
            'capacity': 1800,
            'description': 'Premier academic and cultural venue',
            'contact_phone': '+233302500381',
            'contact_email': 'info@ug.edu.gh'
        }
    ]
    
    print("\n🏢 Creating venues...")
    venues = {}
    for venue_data in venues_data:
        venue, created = Venue.objects.get_or_create(
            slug=venue_data['slug'],
            defaults=venue_data
        )
        venues[venue_data['slug']] = venue
        status = "✅ Created" if created else "📋 Exists"
        print(f"   {status}: {venue.name}")
    
    # Create tickets
    now = timezone.now()
    tickets_data = [
        {
            'title': 'Ghana Cultural Festival 2025',
            'slug': 'ghana-cultural-festival-2025',
            'category': categories['cultural-events'],
            'venue': venues['national-theatre-accra'],
            'ticket_type': 'single',
            'short_description': 'Celebrate Ghana\'s rich cultural heritage',
            'description': 'Join us for an amazing celebration of Ghanaian culture featuring traditional music, dance, food, and crafts from all regions of Ghana.',
            'price': Decimal('150.00'),
            'currency': 'GHS',
            'total_quantity': 500,
            'available_quantity': 500,
            'min_purchase': 1,
            'max_purchase': 10,
            'event_date': now + timedelta(days=45),
            'event_end_date': now + timedelta(days=45, hours=8),
            'sale_start_date': now - timedelta(days=1),
            'sale_end_date': now + timedelta(days=44),
            'status': 'published',
            'is_featured': True,
            'is_refundable': True,
            'features': ['Traditional performances', 'Cultural exhibitions', 'Local cuisine', 'Craft demonstrations']
        },
        {
            'title': 'Highlife Legends Concert',
            'slug': 'highlife-legends-concert',
            'category': categories['music-concerts'],
            'venue': venues['national-theatre-accra'],
            'ticket_type': 'single',
            'short_description': 'Classic Highlife music concert',
            'description': 'Experience the golden age of Highlife music with legendary artists performing classic hits that defined Ghanaian music.',
            'price': Decimal('120.00'),
            'currency': 'GHS',
            'total_quantity': 800,
            'available_quantity': 800,
            'min_purchase': 1,
            'max_purchase': 8,
            'event_date': now + timedelta(days=30),
            'event_end_date': now + timedelta(days=30, hours=6),
            'sale_start_date': now - timedelta(days=1),
            'sale_end_date': now + timedelta(days=29),
            'status': 'published',
            'is_featured': True,
            'is_refundable': True,
            'features': ['Live band performances', 'Classic Highlife hits', 'Meet & greet with artists', 'Complimentary drinks']
        },
        {
            'title': 'Ghana Black Stars vs Nigeria',
            'slug': 'ghana-vs-nigeria-football',
            'category': categories['sports-events'],
            'venue': venues['accra-sports-stadium'],
            'ticket_type': 'single',
            'short_description': 'International football match',
            'description': 'Watch the Ghana Black Stars take on Nigeria in this exciting international football match at the Accra Sports Stadium.',
            'price': Decimal('80.00'),
            'currency': 'GHS',
            'total_quantity': 35000,
            'available_quantity': 35000,
            'min_purchase': 1,
            'max_purchase': 6,
            'event_date': now + timedelta(days=60),
            'event_end_date': now + timedelta(days=60, hours=2),
            'sale_start_date': now - timedelta(days=1),
            'sale_end_date': now + timedelta(days=59),
            'status': 'published',
            'is_featured': True,
            'is_refundable': False,
            'features': ['Stadium seating', 'Live commentary', 'Halftime entertainment', 'Food and beverages available']
        },
        {
            'title': 'Traditional Dance Performance',
            'slug': 'traditional-dance-performance',
            'category': categories['cultural-events'],
            'venue': venues['ug-great-hall'],
            'ticket_type': 'single',
            'short_description': 'Authentic Ghanaian dance showcase',
            'description': 'Experience the beauty and energy of traditional Ghanaian dances performed by renowned cultural troupes from across the country.',
            'price': Decimal('60.00'),
            'currency': 'GHS',
            'total_quantity': 300,
            'available_quantity': 300,
            'min_purchase': 1,
            'max_purchase': 5,
            'event_date': now + timedelta(days=20),
            'event_end_date': now + timedelta(days=20, hours=3),
            'sale_start_date': now - timedelta(days=1),
            'sale_end_date': now + timedelta(days=19),
            'status': 'published',
            'is_featured': False,
            'is_refundable': True,
            'features': ['Traditional costumes', 'Live drumming', 'Cultural storytelling', 'Photo opportunities']
        },
        {
            'title': 'Cape Coast Castle Historical Tour',
            'slug': 'cape-coast-castle-tour',
            'category': categories['educational'],
            'venue': venues['cape-coast-castle'],
            'ticket_type': 'single',
            'short_description': 'Guided historical tour',
            'description': 'Explore the rich and complex history of Cape Coast Castle with expert guides who will take you through centuries of Ghanaian heritage.',
            'price': Decimal('40.00'),
            'currency': 'GHS',
            'discount_price': Decimal('30.00'),
            'total_quantity': 150,
            'available_quantity': 150,
            'min_purchase': 1,
            'max_purchase': 15,
            'event_date': now + timedelta(days=15),
            'event_end_date': now + timedelta(days=15, hours=4),
            'sale_start_date': now - timedelta(days=1),
            'sale_end_date': now + timedelta(days=14),
            'status': 'published',
            'is_featured': False,
            'is_refundable': True,
            'features': ['Expert guide', 'Historical artifacts', 'Museum access', 'Educational materials']
        },
        {
            'title': 'Adinkra Symbols Workshop',
            'slug': 'adinkra-symbols-workshop',
            'category': categories['educational'],
            'venue': venues['ug-great-hall'],
            'ticket_type': 'single',
            'short_description': 'Learn traditional Adinkra symbols',
            'description': 'Hands-on workshop to learn about the meaning and creation of traditional Adinkra symbols, an important part of Ghanaian cultural heritage.',
            'price': Decimal('75.00'),
            'currency': 'GHS',
            'total_quantity': 50,
            'available_quantity': 50,
            'min_purchase': 1,
            'max_purchase': 3,
            'event_date': now + timedelta(days=25),
            'event_end_date': now + timedelta(days=25, hours=5),
            'sale_start_date': now - timedelta(days=1),
            'sale_end_date': now + timedelta(days=24),
            'status': 'published',
            'is_featured': False,
            'is_refundable': True,
            'features': ['Hands-on learning', 'Traditional materials', 'Take-home creations', 'Cultural education']
        }
    ]
    
    print("\n🎫 Creating tickets...")
    created_tickets = []
    for ticket_data in tickets_data:
        ticket, created = Ticket.objects.get_or_create(
            slug=ticket_data['slug'],
            defaults=ticket_data
        )
        created_tickets.append(ticket)
        status = "✅ Created" if created else "📋 Exists"
        price_display = f"GH₵{ticket.discount_price}" if ticket.discount_price else f"GH₵{ticket.price}"
        print(f"   {status}: {ticket.title} - {price_display}")
    
    print(f"\n" + "=" * 50)
    print(f"🎉 SAMPLE TICKETS CREATION COMPLETE!")
    print(f"=" * 50)
    print(f"📊 Summary:")
    print(f"   • Categories: {TicketCategory.objects.count()}")
    print(f"   • Venues: {Venue.objects.count()}")
    print(f"   • Tickets: {Ticket.objects.count()}")
    
    print(f"\n🎯 Featured Tickets:")
    featured = Ticket.objects.filter(is_featured=True)
    for ticket in featured:
        print(f"   ⭐ {ticket.title} - GH₵{ticket.price}")
    
    print(f"\n🔗 API Endpoints:")
    print(f"   • All Tickets: http://localhost:8000/api/tickets/")
    print(f"   • Categories: http://localhost:8000/api/tickets/categories/")
    print(f"   • Venues: http://localhost:8000/api/tickets/venues/")
    
    print(f"\n🎪 Admin Panel:")
    print(f"   • Tickets: http://localhost:8000/admin/tickets/ticket/")
    print(f"   • Categories: http://localhost:8000/admin/tickets/ticketcategory/")
    print(f"   • Venues: http://localhost:8000/admin/tickets/venue/")

if __name__ == "__main__":
    create_sample_tickets()