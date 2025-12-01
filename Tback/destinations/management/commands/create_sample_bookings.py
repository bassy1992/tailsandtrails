from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from destinations.models import Destination, Booking
from tickets.models import Ticket, TicketPurchase, Venue, TicketCategory
from decimal import Decimal
from datetime import date, timedelta
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample bookings and ticket purchases for testing dashboard'

    def handle(self, *args, **options):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'John',
                'last_name': 'Doe',
                'is_active': True
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created test user: {user.email}')
        else:
            self.stdout.write(f'Using existing user: {user.email}')

        # Get or create a category first
        from destinations.models import Category
        category, created = Category.objects.get_or_create(
            slug='adventure',
            defaults={'name': 'Adventure Tours'}
        )
        if created:
            self.stdout.write(f'Created category: {category.name}')

        # Create sample destinations if they don't exist
        destinations_data = [
            {
                'name': 'Kakum National Park Canopy Walk',
                'slug': 'kakum-national-park',
                'description': 'Experience the thrill of walking through the treetops',
                'price': Decimal('850.00'),
                'duration': '3_days',
                'location': 'Central Region, Ghana',
                'image': 'https://images.pexels.com/photos/1666065/pexels-photo-1666065.jpeg',
                'max_group_size': 15,
                'category': category
            },
            {
                'name': 'Cape Coast Castle Historical Tour',
                'slug': 'cape-coast-castle',
                'description': 'Explore the historical significance of Cape Coast Castle',
                'price': Decimal('650.00'),
                'duration': '2_days',
                'location': 'Cape Coast, Ghana',
                'image': 'https://images.pexels.com/photos/5273081/pexels-photo-5273081.jpeg',
                'max_group_size': 20,
                'category': category
            },
            {
                'name': 'Mole National Park Safari',
                'slug': 'mole-national-park',
                'description': 'Wildlife safari in Ghana\'s largest national park',
                'price': Decimal('1200.00'),
                'duration': '4_days',
                'location': 'Northern Region, Ghana',
                'image': 'https://images.pexels.com/photos/1054655/pexels-photo-1054655.jpeg',
                'max_group_size': 12,
                'category': category
            }
        ]

        destinations = []
        for dest_data in destinations_data:
            destination, created = Destination.objects.get_or_create(
                slug=dest_data['slug'],
                defaults=dest_data
            )
            destinations.append(destination)
            if created:
                self.stdout.write(f'Created destination: {destination.name}')

        # Create sample bookings
        booking_statuses = ['confirmed', 'pending', 'completed']
        for i, destination in enumerate(destinations):
            participants = random.randint(1, 4)
            booking = Booking.objects.create(
                user=user,
                destination=destination,
                booking_date=date.today() + timedelta(days=30 + i*10),
                participants=participants,
                total_amount=destination.price * participants,
                status=booking_statuses[i % len(booking_statuses)],
                special_requests=f'Sample booking for {destination.name}'
            )
            self.stdout.write(f'Created booking: {booking.booking_reference}')

        # Create sample venue and ticket category
        venue, created = Venue.objects.get_or_create(
            slug='national-theatre-accra',
            defaults={
                'name': 'National Theatre of Ghana',
                'address': 'Liberation Road, Accra',
                'city': 'Accra',
                'capacity': 1500,
                'description': 'Premier cultural venue in Ghana'
            }
        )
        if created:
            self.stdout.write(f'Created venue: {venue.name}')

        category, created = TicketCategory.objects.get_or_create(
            slug='cultural-events',
            defaults={
                'name': 'Cultural Events',
                'description': 'Traditional and contemporary cultural performances'
            }
        )
        if created:
            self.stdout.write(f'Created ticket category: {category.name}')

        # Create sample tickets
        from datetime import datetime
        from django.utils import timezone
        
        tickets_data = [
            {
                'title': 'Ghana Cultural Festival 2025',
                'slug': 'ghana-cultural-festival-2025',
                'description': 'Annual celebration of Ghanaian culture',
                'price': Decimal('150.00'),
                'event_date': timezone.now() + timedelta(days=45),
                'sale_start_date': timezone.now(),
                'sale_end_date': timezone.now() + timedelta(days=40),
                'total_quantity': 500,
                'available_quantity': 450
            },
            {
                'title': 'Traditional Dance Performance',
                'slug': 'traditional-dance-performance',
                'description': 'Authentic Ghanaian traditional dance showcase',
                'price': Decimal('80.00'),
                'event_date': timezone.now() + timedelta(days=60),
                'sale_start_date': timezone.now(),
                'sale_end_date': timezone.now() + timedelta(days=55),
                'total_quantity': 200,
                'available_quantity': 180
            }
        ]

        for ticket_data in tickets_data:
            ticket, created = Ticket.objects.get_or_create(
                slug=ticket_data['slug'],
                defaults={
                    **ticket_data,
                    'venue': venue,
                    'category': category,
                    'max_purchase': 10,
                    'status': 'published'
                }
            )
            if created:
                self.stdout.write(f'Created ticket: {ticket.title}')
                
                # Create a sample ticket purchase
                quantity = random.randint(1, 3)
                purchase = TicketPurchase.objects.create(
                    user=user,
                    ticket=ticket,
                    quantity=quantity,
                    unit_price=ticket.price,
                    total_amount=ticket.price * quantity,
                    customer_name=f"{user.first_name} {user.last_name}",
                    customer_email=user.email,
                    status=random.choice(['confirmed', 'pending', 'used'])
                )
                self.stdout.write(f'Created ticket purchase: {purchase.purchase_id}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample bookings and ticket purchases!')
        )