from django.core.management.base import BaseCommand
from destinations.models import Destination, AddOnCategory, AddOnOption, ExperienceAddOn

class Command(BaseCommand):
    help = 'Populate sample add-on options for existing destinations'

    def handle(self, *args, **options):
        # Get all destinations
        destinations = Destination.objects.all()
        
        if not destinations.exists():
            self.stdout.write(
                self.style.ERROR('No destinations found. Please create destinations first.')
            )
            return

        # Get categories
        try:
            accommodation_cat = AddOnCategory.objects.get(name='accommodation')
            transport_cat = AddOnCategory.objects.get(name='transport')
            meals_cat = AddOnCategory.objects.get(name='meals')
            medical_cat = AddOnCategory.objects.get(name='medical')
        except AddOnCategory.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Add-on categories not found. Please run populate_addon_categories first.')
            )
            return

        # Sample add-on options for each category
        addon_options = [
            # Accommodation options
            {
                'category': accommodation_cat,
                'name': 'Standard Hotel',
                'description': 'Included in base package',
                'price': 0,
                'is_default': True,
                'order': 1
            },
            {
                'category': accommodation_cat,
                'name': 'Premium Hotel',
                'description': '4-star accommodation with pool & spa',
                'price': 500,
                'is_default': False,
                'order': 2
            },
            {
                'category': accommodation_cat,
                'name': 'Luxury Resort',
                'description': '5-star beachfront resort with premium amenities',
                'price': 1200,
                'is_default': False,
                'order': 3
            },
            
            # Transport options
            {
                'category': transport_cat,
                'name': 'Shared Bus',
                'description': 'Comfortable group transportation',
                'price': 0,
                'is_default': True,
                'order': 1
            },
            {
                'category': transport_cat,
                'name': 'Private Van',
                'description': 'Exclusive vehicle for your group',
                'price': 800,
                'pricing_type': 'per_group',
                'is_default': False,
                'order': 2
            },
            {
                'category': transport_cat,
                'name': 'Airport Pickup & Drop',
                'description': 'Convenient airport transfers',
                'price': 400,
                'pricing_type': 'per_group',
                'is_default': False,
                'order': 3
            },
            
            # Meal options
            {
                'category': meals_cat,
                'name': 'Standard Meals',
                'description': 'Local cuisine and international options',
                'price': 0,
                'is_default': True,
                'order': 1
            },
            {
                'category': meals_cat,
                'name': 'Vegetarian / Vegan Option',
                'description': 'Plant-based meals throughout the tour',
                'price': 0,
                'is_default': False,
                'order': 2
            },
            {
                'category': meals_cat,
                'name': 'Luxury Dining Package',
                'description': 'Fine dining and premium restaurants',
                'price': 300,
                'is_default': False,
                'order': 3
            },
            
            # Medical & Insurance options
            {
                'category': medical_cat,
                'name': 'Basic First Aid',
                'description': 'Standard first aid coverage',
                'price': 0,
                'is_default': True,
                'order': 1
            },
            {
                'category': medical_cat,
                'name': 'Travel Insurance',
                'description': 'Comprehensive coverage for emergencies',
                'price': 200,
                'is_default': False,
                'order': 2
            },
            {
                'category': medical_cat,
                'name': 'On-call Medical Support',
                'description': '24/7 medical assistance available',
                'price': 500,
                'is_default': False,
                'order': 3
            }
        ]

        # Experience add-ons
        experience_addons = [
            {
                'name': 'Cultural Experience',
                'description': 'Traditional drumming, cooking class, local market tour',
                'price': 250,
                'duration': 'Half day',
                'order': 1
            },
            {
                'name': 'Adventure Add-on',
                'description': 'Kakum Canopy Walk, Beach Trip, Nature Photography',
                'price': 400,
                'duration': 'Full day',
                'order': 2
            }
        ]

        created_count = 0
        
        for destination in destinations:
            self.stdout.write(f'Processing destination: {destination.name}')
            
            # Create add-on options
            for option_data in addon_options:
                option_data_copy = option_data.copy()
                option_data_copy['destination'] = destination
                
                addon_option, created = AddOnOption.objects.get_or_create(
                    category=option_data_copy['category'],
                    destination=destination,
                    name=option_data_copy['name'],
                    defaults=option_data_copy
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'  Created: {addon_option.name}')
            
            # Create experience add-ons
            for exp_data in experience_addons:
                exp_data_copy = exp_data.copy()
                exp_data_copy['destination'] = destination
                
                exp_addon, created = ExperienceAddOn.objects.get_or_create(
                    destination=destination,
                    name=exp_data_copy['name'],
                    defaults=exp_data_copy
                )
                
                if created:
                    created_count += 1
                    self.stdout.write(f'  Created experience: {exp_addon.name}')

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} add-on options for {destinations.count()} destinations')
        )