#!/usr/bin/env python
"""
Script to populate the database with sample data for dashboard testing
"""
import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from destinations.models import (
    Category, Destination, DestinationImage, DestinationHighlight, 
    DestinationInclude, Booking, Review
)
from tickets.models import (
    TicketCategory, Venue, Ticket, TicketPurchase, TicketCode
)

User = get_user_model()

def create_sample_users():
    """Create sample users if they don't exist"""
    print("Creating sample users...")
    
    # Create test user if doesn't exist
    if not User.objects.filter(email='test@example.com').exists():
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            phone_number='+233244123456'
        )
        print(f"Created user: {user.email}")
        return user
    else:
        user = User.objects.get(email='test@example.com')
        print(f"Using existing user: {user.email}")
        return user

def create_categories():
    """Create destination categories"""
    print("Creating categories...")
    
    categories_data = [
        {'name': 'Adventure Tours', 'description': 'Thrilling outdoor adventures'},
        {'name': 'Cultural Tours', 'description': 'Explore Ghana\'s rich culture'},
        {'name': 'Beach & Coastal', 'description': 'Beautiful coastal destinations'},
        {'name': 'Wildlife & Nature', 'description': 'Experience Ghana\'s wildlife'},
        {'name': 'Historical Sites', 'description': 'Discover Ghana\'s history'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    return categories

def create_destinations(categories):
    """Create sample destinations"""
    print("Creating destinations...")
    
    destinations_data = [
        {
            'name': 'Cape Coast Castle Tour',
            'location': 'Cape Coast, Central Region',
            'description': 'Explore the historic Cape Coast Castle, a UNESCO World Heritage site that played a significant role in the Atlantic slave trade. Learn about Ghana\'s history and visit the nearby Elmina Castle.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
            'price': Decimal('450.00'),
            'duration': '2_days',
            'max_group_size': 15,
            'rating': Decimal('4.8'),
            'category': categories[4],  # Historical Sites
            'highlights': ['UNESCO World Heritage Site', 'Guided Historical Tour', 'Elmina Castle Visit', 'Local Cultural Experience'],
            'includes': ['Transportation', 'Professional Guide', 'Entrance Fees', 'Lunch']
        },
        {
            'name': 'Kakum National Park Canopy Walk',
            'location': 'Kakum, Central Region',
            'description': 'Experience the thrill of walking through the treetops on suspended bridges 40 meters above the forest floor. Spot rare birds and wildlife in this pristine rainforest.',
            'image': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800',
            'price': Decimal('280.00'),
            'duration': '1_day',
            'max_group_size': 20,
            'rating': Decimal('4.6'),
            'category': categories[3],  # Wildlife & Nature
            'highlights': ['Canopy Walk Experience', 'Bird Watching', 'Nature Photography', 'Forest Hiking'],
            'includes': ['Park Entrance', 'Guide Service', 'Safety Equipment', 'Refreshments']
        },
        {
            'name': 'Mole National Park Safari',
            'location': 'Mole, Northern Region',
            'description': 'Ghana\'s largest wildlife refuge featuring elephants, antelopes, baboons, and over 300 bird species. Enjoy game drives and walking safaris in this spectacular savanna landscape.',
            'image': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?w=800',
            'price': Decimal('850.00'),
            'duration': '3_days',
            'max_group_size': 12,
            'rating': Decimal('4.9'),
            'category': categories[3],  # Wildlife & Nature
            'highlights': ['Elephant Encounters', 'Game Drives', 'Walking Safari', 'Bird Watching'],
            'includes': ['Accommodation', 'All Meals', 'Game Drives', 'Professional Guide']
        },
        {
            'name': 'Kumasi Cultural Heritage Tour',
            'location': 'Kumasi, Ashanti Region',
            'description': 'Discover the heart of Ashanti culture in Kumasi. Visit the Manhyia Palace, Kejetia Market, and traditional craft villages. Experience authentic Ashanti traditions and ceremonies.',
            'image': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800',
            'price': Decimal('380.00'),
            'duration': '2_days',
            'max_group_size': 18,
            'rating': Decimal('4.7'),
            'category': categories[1],  # Cultural Tours
            'highlights': ['Manhyia Palace Museum', 'Kejetia Market Tour', 'Craft Village Visit', 'Traditional Ceremony'],
            'includes': ['Hotel Accommodation', 'Cultural Guide', 'Market Tour', 'Traditional Lunch']
        },
        {
            'name': 'Labadi Beach Resort Experience',
            'location': 'Accra, Greater Accra Region',
            'description': 'Relax at Ghana\'s most popular beach resort. Enjoy water sports, beach volleyball, live music, and delicious seafood while soaking up the sun on golden sands.',
            'image': 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800',
            'price': Decimal('320.00'),
            'duration': '1_day',
            'max_group_size': 25,
            'rating': Decimal('4.4'),
            'category': categories[2],  # Beach & Coastal
            'highlights': ['Beach Activities', 'Water Sports', 'Live Entertainment', 'Seafood Dining'],
            'includes': ['Beach Access', 'Lunch & Drinks', 'Activity Equipment', 'Entertainment']
        },
        {
            'name': 'Volta Region Waterfalls Adventure',
            'location': 'Hohoe, Volta Region',
            'description': 'Discover the stunning Wli Waterfalls, Ghana\'s highest waterfall. Hike through lush forests, swim in natural pools, and visit traditional villages in the scenic Volta Region.',
            'image': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800',
            'price': Decimal('420.00'),
            'duration': '2_days',
            'max_group_size': 16,
            'rating': Decimal('4.8'),
            'category': categories[0],  # Adventure Tours
            'highlights': ['Wli Waterfalls Hike', 'Natural Pool Swimming', 'Village Visits', 'Forest Trekking'],
            'includes': ['Accommodation', 'Hiking Guide', 'Village Tour', 'All Meals']
        }
    ]
    
    destinations = []
    for dest_data in destinations_data:
        destination, created = Destination.objects.get_or_create(
            name=dest_data['name'],
            defaults={
                'location': dest_data['location'],
                'description': dest_data['description'],
                'image': dest_data['image'],
                'price': dest_data['price'],
                'duration': dest_data['duration'],
                'max_group_size': dest_data['max_group_size'],
                'rating': dest_data['rating'],
                'category': dest_data['category'],
                'is_featured': random.choice([True, False])
            }
        )
        
        if created:
            print(f"Created destination: {destination.name}")
            
            # Add highlights
            for i, highlight in enumerate(dest_data['highlights']):
                DestinationHighlight.objects.get_or_create(
                    destination=destination,
                    highlight=highlight,
                    defaults={'order': i}
                )
            
            # Add includes
            for i, include in enumerate(dest_data['includes']):
                DestinationInclude.objects.get_or_create(
                    destination=destination,
                    item=include,
                    defaults={'order': i}
                )
            
            # Add destination image
            DestinationImage.objects.get_or_create(
                destination=destination,
                image_url=dest_data['image'],
                defaults={'is_primary': True, 'order': 0}
            )
        
        destinations.append(destination)
    
    return destinations

def create_ticket_categories():
    """Create ticket categories"""
    print("Creating ticket categories...")
    
    categories_data = [
        {'name': 'Music Events', 'category_type': 'event', 'icon': 'music'},
        {'name': 'Cultural Festivals', 'category_type': 'event', 'icon': 'calendar'},
        {'name': 'Sports Events', 'category_type': 'event', 'icon': 'trophy'},
        {'name': 'Art Exhibitions', 'category_type': 'event', 'icon': 'palette'},
        {'name': 'Food & Drink', 'category_type': 'event', 'icon': 'utensils'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = TicketCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'category_type': cat_data['category_type'],
                'icon': cat_data['icon']
            }
        )
        categories.append(category)
        if created:
            print(f"Created ticket category: {category.name}")
    
    return categories

def create_venues():
    """Create sample venues"""
    print("Creating venues...")
    
    venues_data = [
        {
            'name': 'National Theatre of Ghana',
            'address': 'Liberation Road, Accra',
            'city': 'Accra',
            'region': 'Greater Accra',
            'capacity': 1500,
            'description': 'Ghana\'s premier cultural venue hosting world-class performances.'
        },
        {
            'name': 'Accra Sports Stadium',
            'address': 'Ohene Djan Circle, Accra',
            'city': 'Accra',
            'region': 'Greater Accra',
            'capacity': 40000,
            'description': 'Ghana\'s national stadium for major sporting events.'
        },
        {
            'name': 'Alliance Française',
            'address': 'Liberation Road, Accra',
            'city': 'Accra',
            'region': 'Greater Accra',
            'capacity': 300,
            'description': 'Cultural center promoting arts and French-Ghanaian cultural exchange.'
        },
        {
            'name': 'Kumasi Cultural Centre',
            'address': 'Cultural Centre Road, Kumasi',
            'city': 'Kumasi',
            'region': 'Ashanti',
            'capacity': 800,
            'description': 'Premier cultural venue in the Ashanti Region.'
        }
    ]
    
    venues = []
    for venue_data in venues_data:
        # Check if venue exists first
        existing_venues = Venue.objects.filter(name=venue_data['name'])
        if existing_venues.exists():
            venue = existing_venues.first()
            print(f"Using existing venue: {venue.name}")
        else:
            venue = Venue.objects.create(**venue_data)
            print(f"Created venue: {venue.name}")
        venues.append(venue)
    
    return venues

def create_tickets(categories, venues):
    """Create sample tickets"""
    print("Creating tickets...")
    
    now = timezone.now()
    
    tickets_data = [
        {
            'title': 'Afrobeats Night Live Concert',
            'category': categories[0],  # Music Events
            'venue': venues[0],  # National Theatre
            'description': 'Experience the best of Afrobeats with top Ghanaian and international artists. A night of incredible music, dancing, and cultural celebration.',
            'price': Decimal('150.00'),
            'total_quantity': 500,
            'event_date': now + timedelta(days=30),
            'sale_start_date': now - timedelta(days=10),
            'sale_end_date': now + timedelta(days=29),
            'features': ['VIP Seating Available', 'Meet & Greet', 'Complimentary Drinks', 'Live DJ Set']
        },
        {
            'title': 'Ghana Independence Day Festival',
            'category': categories[1],  # Cultural Festivals
            'venue': venues[2],  # Alliance Française
            'description': 'Celebrate Ghana\'s independence with traditional music, dance performances, local cuisine, and cultural exhibitions.',
            'price': Decimal('75.00'),
            'total_quantity': 300,
            'event_date': now + timedelta(days=45),
            'sale_start_date': now - timedelta(days=5),
            'sale_end_date': now + timedelta(days=44),
            'features': ['Traditional Performances', 'Local Cuisine', 'Art Exhibition', 'Cultural Workshops']
        },
        {
            'title': 'Black Stars vs Nigeria - World Cup Qualifier',
            'category': categories[2],  # Sports Events
            'venue': venues[1],  # Accra Sports Stadium
            'description': 'Watch Ghana\'s Black Stars take on Nigeria in this crucial World Cup qualifier match. Experience the passion of Ghanaian football.',
            'price': Decimal('200.00'),
            'total_quantity': 35000,
            'event_date': now + timedelta(days=60),
            'sale_start_date': now - timedelta(days=15),
            'sale_end_date': now + timedelta(days=59),
            'features': ['Stadium Seating', 'Match Program', 'Pre-match Entertainment', 'Food & Beverages Available']
        },
        {
            'title': 'Contemporary African Art Exhibition',
            'category': categories[3],  # Art Exhibitions
            'venue': venues[2],  # Alliance Française
            'description': 'Discover contemporary African art from emerging and established artists. Interactive exhibitions and artist talks included.',
            'price': Decimal('50.00'),
            'total_quantity': 200,
            'event_date': now + timedelta(days=20),
            'sale_start_date': now - timedelta(days=20),
            'sale_end_date': now + timedelta(days=90),
            'features': ['Artist Talks', 'Interactive Exhibitions', 'Guided Tours', 'Art Workshops']
        },
        {
            'title': 'Taste of Ghana Food Festival',
            'category': categories[4],  # Food & Drink
            'venue': venues[3],  # Kumasi Cultural Centre
            'description': 'Sample the best of Ghanaian cuisine from renowned chefs and local food vendors. Cooking demonstrations and tastings included.',
            'price': Decimal('100.00'),
            'total_quantity': 400,
            'event_date': now + timedelta(days=25),
            'sale_start_date': now - timedelta(days=7),
            'sale_end_date': now + timedelta(days=24),
            'features': ['Food Tastings', 'Cooking Demos', 'Chef Competitions', 'Recipe Cards']
        }
    ]
    
    tickets = []
    for ticket_data in tickets_data:
        # Check if ticket exists first
        existing_tickets = Ticket.objects.filter(title=ticket_data['title'])
        if existing_tickets.exists():
            ticket = existing_tickets.first()
            print(f"Using existing ticket: {ticket.title}")
        else:
            ticket = Ticket.objects.create(
                **ticket_data,
                available_quantity=ticket_data['total_quantity'],
                status='published',
                is_featured=random.choice([True, False])
            )
            print(f"Created ticket: {ticket.title}")
        tickets.append(ticket)
    
    return tickets

def create_bookings(user, destinations):
    """Create sample bookings for the user"""
    print("Creating sample bookings...")
    
    bookings_data = [
        {
            'destination': destinations[0],  # Cape Coast Castle
            'participants': 2,
            'total_amount': Decimal('900.00'),
            'booking_date': timezone.now().date() + timedelta(days=15),
            'status': 'confirmed',
            'created_at': timezone.now() - timedelta(days=5)
        },
        {
            'destination': destinations[1],  # Kakum Canopy Walk
            'participants': 1,
            'total_amount': Decimal('280.00'),
            'booking_date': timezone.now().date() + timedelta(days=30),
            'status': 'pending',
            'created_at': timezone.now() - timedelta(days=2)
        },
        {
            'destination': destinations[2],  # Mole Safari
            'participants': 3,
            'total_amount': Decimal('2550.00'),
            'booking_date': timezone.now().date() - timedelta(days=30),
            'status': 'completed',
            'created_at': timezone.now() - timedelta(days=45)
        },
        {
            'destination': destinations[4],  # Labadi Beach
            'participants': 4,
            'total_amount': Decimal('1280.00'),
            'booking_date': timezone.now().date() - timedelta(days=10),
            'status': 'completed',
            'created_at': timezone.now() - timedelta(days=25)
        }
    ]
    
    bookings = []
    for booking_data in bookings_data:
        # Check if booking exists first
        existing_bookings = Booking.objects.filter(
            user=user,
            destination=booking_data['destination'],
            booking_date=booking_data['booking_date']
        )
        if existing_bookings.exists():
            booking = existing_bookings.first()
            print(f"Using existing booking: {booking.booking_reference}")
        else:
            booking = Booking.objects.create(
                user=user,
                **booking_data
            )
            # Update the created_at manually since it's auto_now_add
            Booking.objects.filter(id=booking.id).update(
                created_at=booking_data['created_at'],
                updated_at=booking_data['created_at']
            )
            print(f"Created booking: {booking.booking_reference}")
        
        bookings.append(booking)
    
    return bookings

def create_ticket_purchases(user, tickets):
    """Create sample ticket purchases for the user"""
    print("Creating sample ticket purchases...")
    
    purchases_data = [
        {
            'ticket': tickets[0],  # Afrobeats Concert
            'quantity': 2,
            'unit_price': Decimal('150.00'),
            'total_amount': Decimal('300.00'),
            'status': 'confirmed',
            'payment_status': 'completed',
            'created_at': timezone.now() - timedelta(days=8)
        },
        {
            'ticket': tickets[1],  # Independence Festival
            'quantity': 1,
            'unit_price': Decimal('75.00'),
            'total_amount': Decimal('75.00'),
            'status': 'confirmed',
            'payment_status': 'completed',
            'created_at': timezone.now() - timedelta(days=3)
        },
        {
            'ticket': tickets[3],  # Art Exhibition
            'quantity': 1,
            'unit_price': Decimal('50.00'),
            'total_amount': Decimal('50.00'),
            'status': 'used',
            'payment_status': 'completed',
            'created_at': timezone.now() - timedelta(days=15)
        }
    ]
    
    purchases = []
    for purchase_data in purchases_data:
        # Check if purchase exists first
        existing_purchases = TicketPurchase.objects.filter(
            user=user,
            ticket=purchase_data['ticket']
        )
        if existing_purchases.exists():
            purchase = existing_purchases.first()
            print(f"Using existing ticket purchase: {purchase.purchase_id}")
        else:
            purchase = TicketPurchase.objects.create(
                user=user,
                **purchase_data,
                customer_name=f"{user.first_name} {user.last_name}",
                customer_email=user.email,
                customer_phone=user.phone_number or '+233244123456',
                payment_method='paystack',
                payment_date=purchase_data['created_at']
            )
            
            # Update the created_at manually
            TicketPurchase.objects.filter(id=purchase.id).update(
                created_at=purchase_data['created_at'],
                updated_at=purchase_data['created_at']
            )
            print(f"Created ticket purchase: {purchase.purchase_id}")
            
            # Create ticket codes for confirmed purchases
            if purchase.status in ['confirmed', 'used']:
                for i in range(purchase.quantity):
                    TicketCode.objects.create(
                        purchase=purchase,
                        status='used' if purchase.status == 'used' else 'active',
                        used_at=purchase_data['created_at'] if purchase.status == 'used' else None
                    )
        
        purchases.append(purchase)
    
    return purchases

def create_reviews(user, destinations):
    """Create sample reviews"""
    print("Creating sample reviews...")
    
    reviews_data = [
        {
            'destination': destinations[2],  # Mole Safari (completed booking)
            'rating': 5,
            'title': 'Amazing Wildlife Experience!',
            'comment': 'The Mole National Park safari exceeded all expectations. We saw elephants up close, beautiful birds, and the guides were incredibly knowledgeable. Highly recommended for nature lovers!'
        },
        {
            'destination': destinations[4],  # Labadi Beach (completed booking)
            'rating': 4,
            'title': 'Great Beach Day',
            'comment': 'Had a wonderful time at Labadi Beach. The facilities were good, food was delicious, and the beach activities were fun. Perfect for a family day out.'
        }
    ]
    
    for review_data in reviews_data:
        review, created = Review.objects.get_or_create(
            user=user,
            destination=review_data['destination'],
            defaults=review_data
        )
        
        if created:
            print(f"Created review for: {review.destination.name}")

def main():
    """Main function to populate all sample data"""
    print("Starting dashboard data population...")
    
    # Create sample user
    user = create_sample_users()
    
    # Create categories and destinations
    categories = create_categories()
    destinations = create_destinations(categories)
    
    # Create ticket-related data
    ticket_categories = create_ticket_categories()
    venues = create_venues()
    tickets = create_tickets(ticket_categories, venues)
    
    # Create user bookings and purchases
    bookings = create_bookings(user, destinations)
    purchases = create_ticket_purchases(user, tickets)
    
    # Create reviews
    create_reviews(user, destinations)
    
    print("\n" + "="*50)
    print("Dashboard data population completed!")
    print("="*50)
    print(f"Created/Updated:")
    print(f"- {len(categories)} destination categories")
    print(f"- {len(destinations)} destinations")
    print(f"- {len(ticket_categories)} ticket categories")
    print(f"- {len(venues)} venues")
    print(f"- {len(tickets)} tickets")
    print(f"- {len(bookings)} bookings")
    print(f"- {len(purchases)} ticket purchases")
    print("\nTest user credentials:")
    print("Email: test@example.com")
    print("Password: testpass123")
    print("\nYou can now visit http://localhost:8080/dashboard to see the populated data!")

if __name__ == '__main__':
    main()