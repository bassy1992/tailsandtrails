from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tickets.models import TicketCategory, Venue, Ticket, TicketPromoCode
from decimal import Decimal

class Command(BaseCommand):
    help = 'Populate sample ticket data'

    def handle(self, *args, **options):
        # Create categories
        categories_data = [
            {
                'name': 'Concerts & Music',
                'category_type': 'event',
                'description': 'Live music performances and concerts',
                'icon': 'Music',
                'order': 1
            },
            {
                'name': 'Cultural Events',
                'category_type': 'event',
                'description': 'Traditional and cultural celebrations',
                'icon': 'Calendar',
                'order': 2
            },
            {
                'name': 'Tourist Attractions',
                'category_type': 'attraction',
                'description': 'Museums, monuments, and tourist sites',
                'icon': 'MapPin',
                'order': 3
            },
            {
                'name': 'Transportation',
                'category_type': 'transport',
                'description': 'Bus, train, and other transport tickets',
                'icon': 'Car',
                'order': 4
            },
            {
                'name': 'Experiences',
                'category_type': 'experience',
                'description': 'Tours, workshops, and unique experiences',
                'icon': 'Star',
                'order': 5
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = TicketCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create venues
        venues_data = [
            {
                'name': 'National Theatre of Ghana',
                'address': 'Liberation Road, Accra',
                'city': 'Accra',
                'region': 'Greater Accra',
                'capacity': 1500,
                'description': 'Premier performing arts venue in Ghana',
                'contact_phone': '+233-30-266-1680',
                'contact_email': 'info@nationaltheatre.gov.gh'
            },
            {
                'name': 'Cape Coast Castle',
                'address': 'Cape Coast',
                'city': 'Cape Coast',
                'region': 'Central Region',
                'capacity': 500,
                'description': 'Historic castle and UNESCO World Heritage Site',
                'contact_phone': '+233-33-213-2138'
            },
            {
                'name': 'Kwame Nkrumah Memorial Park',
                'address': 'High Street, Accra',
                'city': 'Accra',
                'region': 'Greater Accra',
                'capacity': 1000,
                'description': 'Memorial park dedicated to Ghana\'s first president',
                'contact_phone': '+233-30-266-5652'
            },
            {
                'name': 'Elmina Castle',
                'address': 'Elmina',
                'city': 'Elmina',
                'region': 'Central Region',
                'capacity': 300,
                'description': 'Historic Portuguese castle and slave fort',
                'contact_phone': '+233-33-213-4094'
            },
            {
                'name': 'Accra Sports Stadium',
                'address': 'Ohene Djan Sports Stadium, Accra',
                'city': 'Accra',
                'region': 'Greater Accra',
                'capacity': 40000,
                'description': 'Multi-purpose stadium for sports and events',
                'contact_phone': '+233-30-266-4181'
            }
        ]

        venues = {}
        for venue_data in venues_data:
            venue, created = Venue.objects.get_or_create(
                name=venue_data['name'],
                defaults=venue_data
            )
            venues[venue_data['name']] = venue
            if created:
                self.stdout.write(f'Created venue: {venue.name}')

        # Create sample tickets
        now = timezone.now()
        tickets_data = [
            {
                'title': 'Highlife Legends Concert',
                'category': categories['Concerts & Music'],
                'venue': venues['National Theatre of Ghana'],
                'ticket_type': 'single',
                'description': 'Experience the golden age of Highlife music with legendary performers',
                'short_description': 'Classic Highlife music concert featuring legendary artists',
                'price': Decimal('150.00'),
                'discount_price': Decimal('120.00'),
                'total_quantity': 800,
                'available_quantity': 650,
                'event_date': now + timedelta(days=30),
                'sale_start_date': now,
                'sale_end_date': now + timedelta(days=29),
                'features': ['Live band', 'Traditional costumes', 'Meet & greet'],
                'is_featured': True,
                'status': 'published'
            },
            {
                'title': 'Cape Coast Castle Historical Tour',
                'category': categories['Tourist Attractions'],
                'venue': venues['Cape Coast Castle'],
                'ticket_type': 'single',
                'description': 'Guided tour through the historic Cape Coast Castle with expert historians',
                'short_description': 'Historical guided tour of Cape Coast Castle',
                'price': Decimal('50.00'),
                'total_quantity': 200,
                'available_quantity': 180,
                'event_date': now + timedelta(days=7),
                'sale_start_date': now,
                'sale_end_date': now + timedelta(days=6),
                'features': ['Expert guide', 'Historical artifacts', 'Dungeon tour'],
                'is_featured': True,
                'status': 'published'
            },
            {
                'title': 'Adinkra Symbols Workshop',
                'category': categories['Cultural Events'],
                'venue': venues['Kwame Nkrumah Memorial Park'],
                'ticket_type': 'single',
                'description': 'Learn about traditional Adinkra symbols and their meanings',
                'short_description': 'Interactive workshop on Adinkra symbols and culture',
                'price': Decimal('80.00'),
                'total_quantity': 50,
                'available_quantity': 35,
                'event_date': now + timedelta(days=14),
                'sale_start_date': now,
                'sale_end_date': now + timedelta(days=13),
                'features': ['Hands-on workshop', 'Take home materials', 'Cultural expert'],
                'status': 'published'
            },
            {
                'title': 'Elmina Castle Sunset Tour',
                'category': categories['Experiences'],
                'venue': venues['Elmina Castle'],
                'ticket_type': 'single',
                'description': 'Special evening tour of Elmina Castle with stunning sunset views',
                'short_description': 'Evening castle tour with beautiful sunset views',
                'price': Decimal('75.00'),
                'discount_price': Decimal('60.00'),
                'total_quantity': 100,
                'available_quantity': 85,
                'event_date': now + timedelta(days=21),
                'sale_start_date': now,
                'sale_end_date': now + timedelta(days=20),
                'features': ['Sunset viewing', 'Photography session', 'Light refreshments'],
                'is_featured': True,
                'status': 'published'
            },
            {
                'title': 'Ghana Black Stars Match',
                'category': categories['Concerts & Music'],
                'venue': venues['Accra Sports Stadium'],
                'ticket_type': 'single',
                'description': 'Watch Ghana Black Stars in an exciting international friendly match',
                'short_description': 'Ghana Black Stars international football match',
                'price': Decimal('200.00'),
                'total_quantity': 35000,
                'available_quantity': 28000,
                'event_date': now + timedelta(days=45),
                'sale_start_date': now,
                'sale_end_date': now + timedelta(days=44),
                'features': ['Stadium seating', 'Match program', 'Pre-match entertainment'],
                'is_featured': True,
                'status': 'published'
            }
        ]

        created_tickets = []
        for ticket_data in tickets_data:
            ticket, created = Ticket.objects.get_or_create(
                title=ticket_data['title'],
                defaults=ticket_data
            )
            created_tickets.append(ticket)
            if created:
                self.stdout.write(f'Created ticket: {ticket.title}')

        # Create sample promo codes
        promo_codes_data = [
            {
                'code': 'WELCOME20',
                'name': 'Welcome Discount',
                'description': '20% off for new customers',
                'discount_type': 'percentage',
                'discount_value': Decimal('20.00'),
                'usage_limit': 100,
                'valid_from': now,
                'valid_until': now + timedelta(days=90),
                'minimum_purchase_amount': Decimal('50.00')
            },
            {
                'code': 'CULTURE50',
                'name': 'Cultural Events Discount',
                'description': 'GH₵50 off cultural events',
                'discount_type': 'fixed',
                'discount_value': Decimal('50.00'),
                'usage_limit': 50,
                'valid_from': now,
                'valid_until': now + timedelta(days=60),
                'minimum_purchase_amount': Decimal('100.00')
            }
        ]

        for promo_data in promo_codes_data:
            promo_code, created = TicketPromoCode.objects.get_or_create(
                code=promo_data['code'],
                defaults=promo_data
            )
            if created:
                # Add applicable categories for CULTURE50
                if promo_code.code == 'CULTURE50':
                    promo_code.applicable_categories.add(categories['Cultural Events'])
                self.stdout.write(f'Created promo code: {promo_code.code}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {len(created_tickets)} tickets, '
                f'{len(venues)} venues, {len(categories)} categories, '
                f'and {len(promo_codes_data)} promo codes'
            )
        )