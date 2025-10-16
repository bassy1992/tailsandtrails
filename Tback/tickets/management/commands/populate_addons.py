from django.core.management.base import BaseCommand
from django.utils.text import slugify
from tickets.addon_models import AddOnCategory, AddOn, AddOnOption

class Command(BaseCommand):
    help = 'Populate sample add-on data'

    def handle(self, *args, **options):
        self.stdout.write('Creating add-on categories and add-ons...')

        # Create categories
        categories_data = [
            {
                'name': 'Accommodation',
                'category_type': 'accommodation',
                'description': 'Upgrade your accommodation experience',
                'icon': 'Hotel'
            },
            {
                'name': 'Transport',
                'category_type': 'transport',
                'description': 'Transportation options and upgrades',
                'icon': 'Car'
            },
            {
                'name': 'Meals',
                'category_type': 'meals',
                'description': 'Dining and meal options',
                'icon': 'Utensils'
            },
            {
                'name': 'Medical & Insurance',
                'category_type': 'medical',
                'description': 'Health and safety coverage',
                'icon': 'Shield'
            },
            {
                'name': 'Experiences',
                'category_type': 'experience',
                'description': 'Additional cultural and adventure experiences',
                'icon': 'Star'
            }
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = AddOnCategory.objects.get_or_create(
                slug=slugify(cat_data['name']),
                defaults=cat_data
            )
            categories[cat_data['category_type']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create add-ons
        addons_data = [
            # Accommodation
            {
                'name': 'Accommodation Upgrade',
                'category': categories['accommodation'],
                'addon_type': 'multiple',
                'description': 'Choose your preferred accommodation level',
                'short_description': 'Upgrade your stay with premium accommodations',
                'base_price': 0,
                'pricing_type': 'fixed',
                'is_required': True,
                'is_default': True,
                'features': ['Comfortable rooms', 'Quality service', 'Great locations'],
                'options': [
                    {'name': 'Standard Hotel (included)', 'price': 0, 'is_default': True},
                    {'name': 'Premium Hotel', 'price': 500},
                    {'name': 'Luxury Resort', 'price': 1200}
                ]
            },
            # Transport
            {
                'name': 'Transport Options',
                'category': categories['transport'],
                'addon_type': 'multiple',
                'description': 'Upgrade your transportation experience',
                'short_description': 'Choose from various transport options',
                'base_price': 0,
                'pricing_type': 'fixed',
                'is_required': True,
                'is_default': True,
                'features': ['Reliable transport', 'Professional drivers', 'Comfortable vehicles'],
                'options': [
                    {'name': 'Shared Bus (included)', 'price': 0, 'is_default': True},
                    {'name': 'Private Van', 'price': 800},
                    {'name': 'Airport Pickup & Drop', 'price': 400}
                ]
            },
            # Meals
            {
                'name': 'Meal Options',
                'category': categories['meals'],
                'addon_type': 'multiple',
                'description': 'Customize your dining experience',
                'short_description': 'Various meal options to suit your preferences',
                'base_price': 0,
                'pricing_type': 'fixed',
                'is_required': True,
                'is_default': True,
                'features': ['Quality ingredients', 'Local cuisine', 'Dietary accommodations'],
                'options': [
                    {'name': 'Standard Meals (included)', 'price': 0, 'is_default': True},
                    {'name': 'Vegetarian / Vegan Option', 'price': 0},
                    {'name': 'Luxury Dining Package', 'price': 300}
                ]
            },
            # Medical
            {
                'name': 'Medical & Insurance',
                'category': categories['medical'],
                'addon_type': 'multiple',
                'description': 'Additional health and safety coverage',
                'short_description': 'Comprehensive health and safety options',
                'base_price': 0,
                'pricing_type': 'fixed',
                'is_required': True,
                'is_default': True,
                'features': ['Professional medical support', 'Emergency coverage', 'Peace of mind'],
                'options': [
                    {'name': 'Basic First Aid (included)', 'price': 0, 'is_default': True},
                    {'name': 'Travel Insurance', 'price': 200},
                    {'name': 'On-call Medical Support', 'price': 500}
                ]
            },
            # Experiences
            {
                'name': 'Cultural Experience',
                'category': categories['experience'],
                'addon_type': 'checkbox',
                'description': 'Traditional drumming, cooking class, local market tour',
                'short_description': 'Immerse yourself in local culture',
                'base_price': 250,
                'pricing_type': 'fixed',
                'features': ['Traditional drumming lessons', 'Local cooking class', 'Guided market tour', 'Cultural insights']
            },
            {
                'name': 'Adventure Add-on',
                'category': categories['experience'],
                'addon_type': 'checkbox',
                'description': 'Kakum Canopy Walk, Beach Trip, Nature exploration',
                'short_description': 'Exciting adventure activities',
                'base_price': 400,
                'pricing_type': 'fixed',
                'features': ['Kakum Canopy Walk', 'Beach excursion', 'Nature photography', 'Adventure guide']
            },
            {
                'name': 'Photography Package',
                'category': categories['experience'],
                'addon_type': 'checkbox',
                'description': 'Professional photography service for your tour',
                'short_description': 'Capture your memories professionally',
                'base_price': 350,
                'pricing_type': 'per_group',
                'features': ['Professional photographer', 'Edited photos', 'Digital gallery', 'Print options']
            }
        ]

        for addon_data in addons_data:
            options_data = addon_data.pop('options', [])
            
            addon, created = AddOn.objects.get_or_create(
                slug=slugify(addon_data['name']),
                defaults=addon_data
            )
            
            if created:
                self.stdout.write(f'Created add-on: {addon.name}')
                
                # Create options if any
                for option_data in options_data:
                    option = AddOnOption.objects.create(
                        addon=addon,
                        **option_data
                    )
                    self.stdout.write(f'  - Created option: {option.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated add-on data!'))