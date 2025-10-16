from django.core.management.base import BaseCommand
from destinations.models import Destination, AddOnCategory, AddOnOption, ExperienceAddOn
from decimal import Decimal

class Command(BaseCommand):
    help = 'Set up add-on categories and options for all destinations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--destination-id',
            type=int,
            help='Set up add-ons for a specific destination ID',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing add-on options',
        )

    def handle(self, *args, **options):
        destination_id = options.get('destination_id')
        overwrite = options.get('overwrite', False)
        
        # First, create or get add-on categories
        self.stdout.write("Creating add-on categories...")
        
        categories_data = [
            {
                'name': 'accommodation',
                'display_name': 'Accommodation Options',
                'description': 'Choose your preferred accommodation level',
                'icon': 'hotel',
                'order': 1
            },
            {
                'name': 'transport',
                'display_name': 'Transport Options',
                'description': 'Select your transportation preferences',
                'icon': 'car',
                'order': 2
            },
            {
                'name': 'meals',
                'display_name': 'Meal Options',
                'description': 'Customize your dining experience',
                'icon': 'utensils',
                'order': 3
            },
            {
                'name': 'medical',
                'display_name': 'Medical & Insurance',
                'description': 'Health and safety coverage options',
                'icon': 'shield',
                'order': 4
            },
            {
                'name': 'experience',
                'display_name': 'Additional Experiences',
                'description': 'Enhance your tour with extra activities',
                'icon': 'camera',
                'order': 5
            }
        ]
        
        categories = {}
        for cat_data in categories_data:
            category, created = AddOnCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'display_name': cat_data['display_name'],
                    'description': cat_data['description'],
                    'icon': cat_data['icon'],
                    'order': cat_data['order'],
                    'is_active': True
                }
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f"Created category: {category.display_name}")
            else:
                self.stdout.write(f"Category exists: {category.display_name}")
        
        # Get destinations to add options to
        if destination_id:
            try:
                destinations = [Destination.objects.get(id=destination_id)]
            except Destination.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Destination with ID {destination_id} not found')
                )
                return
        else:
            destinations = Destination.objects.filter(is_active=True)
        
        total_created = 0
        
        for destination in destinations:
            self.stdout.write(f"\nSetting up add-ons for: {destination.name}")
            
            # Check if destination already has add-ons
            existing_count = destination.addon_options.count()
            if existing_count > 0 and not overwrite:
                self.stdout.write(f"Skipping {destination.name} - already has {existing_count} add-ons")
                continue
            
            if overwrite and existing_count > 0:
                destination.addon_options.all().delete()
                destination.experience_addons.all().delete()
                self.stdout.write(f"Deleted {existing_count} existing add-ons")
            
            # Define add-on options for each category
            addon_options = [
                # Accommodation Options
                {
                    'category': 'accommodation',
                    'name': 'Standard Hotel',
                    'description': 'Included in base package',
                    'price': Decimal('0.00'),
                    'pricing_type': 'per_person',
                    'is_default': True,
                    'order': 1
                },
                {
                    'category': 'accommodation',
                    'name': 'Premium Hotel',
                    'description': '4-star accommodation with pool & spa',
                    'price': Decimal('500.00'),
                    'pricing_type': 'per_person',
                    'is_default': False,
                    'order': 2
                },
                {
                    'category': 'accommodation',
                    'name': 'Luxury Resort',
                    'description': '5-star beachfront resort with premium amenities',
                    'price': Decimal('1200.00'),
                    'pricing_type': 'per_person',
                    'is_default': False,
                    'order': 3
                },
                
                # Transport Options
                {
                    'category': 'transport',
                    'name': 'Shared Bus',
                    'description': 'Comfortable group transportation',
                    'price': Decimal('0.00'),
                    'pricing_type': 'per_person',
                    'is_default': True,
                    'order': 1
                },
                {
                    'category': 'transport',
                    'name': 'Private Van',
                    'description': 'Exclusive vehicle for your group',
                    'price': Decimal('800.00'),
                    'pricing_type': 'per_group',
                    'is_default': False,
                    'order': 2
                },
                {
                    'category': 'transport',
                    'name': 'Airport Pickup & Drop',
                    'description': 'Convenient airport transfers',
                    'price': Decimal('400.00'),
                    'pricing_type': 'per_group',
                    'is_default': False,
                    'order': 3
                },
                
                # Meal Options
                {
                    'category': 'meals',
                    'name': 'Standard Meals',
                    'description': 'Local cuisine and international options',
                    'price': Decimal('0.00'),
                    'pricing_type': 'per_person',
                    'is_default': True,
                    'order': 1
                },
                {
                    'category': 'meals',
                    'name': 'Vegetarian / Vegan Option',
                    'description': 'Plant-based meals throughout the tour',
                    'price': Decimal('0.00'),
                    'pricing_type': 'per_person',
                    'is_default': False,
                    'order': 2
                },
                {
                    'category': 'meals',
                    'name': 'Luxury Dining Package',
                    'description': 'Fine dining and premium restaurants',
                    'price': Decimal('300.00'),
                    'pricing_type': 'per_person',
                    'is_default': False,
                    'order': 3
                },
                
                # Medical & Insurance
                {
                    'category': 'medical',
                    'name': 'Basic First Aid',
                    'description': 'Standard first aid coverage',
                    'price': Decimal('0.00'),
                    'pricing_type': 'per_person',
                    'is_default': True,
                    'order': 1
                },
                {
                    'category': 'medical',
                    'name': 'Travel Insurance',
                    'description': 'Comprehensive coverage for emergencies',
                    'price': Decimal('200.00'),
                    'pricing_type': 'per_person',
                    'is_default': False,
                    'order': 2
                },
                {
                    'category': 'medical',
                    'name': 'On-call Medical Support',
                    'description': '24/7 medical assistance available',
                    'price': Decimal('500.00'),
                    'pricing_type': 'per_group',
                    'is_default': False,
                    'order': 3
                }
            ]
            
            # Create add-on options
            created_count = 0
            for option_data in addon_options:
                category = categories[option_data['category']]
                
                addon_option = AddOnOption.objects.create(
                    category=category,
                    destination=destination,
                    name=option_data['name'],
                    description=option_data['description'],
                    price=option_data['price'],
                    pricing_type=option_data['pricing_type'],
                    is_default=option_data['is_default'],
                    is_active=True,
                    order=option_data['order']
                )
                created_count += 1
            
            # Create experience add-ons
            experience_addons = [
                {
                    'name': 'Cultural Experience',
                    'description': 'Traditional drumming, cooking class, local market tour',
                    'price': Decimal('250.00'),
                    'duration': '4 hours',
                    'max_participants': 20,
                    'order': 1
                },
                {
                    'name': 'Adventure Add-on',
                    'description': 'Kakum Canopy Walk, Beach Trip, Nature Photography',
                    'price': Decimal('400.00'),
                    'duration': '6 hours',
                    'max_participants': 15,
                    'order': 2
                }
            ]
            
            for exp_data in experience_addons:
                ExperienceAddOn.objects.create(
                    destination=destination,
                    name=exp_data['name'],
                    description=exp_data['description'],
                    price=exp_data['price'],
                    duration=exp_data['duration'],
                    max_participants=exp_data['max_participants'],
                    is_active=True,
                    order=exp_data['order']
                )
                created_count += 1
            
            total_created += created_count
            self.stdout.write(
                self.style.SUCCESS(f"Created {created_count} add-ons for {destination.name}")
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSummary: Created {total_created} add-on options total for {len(destinations)} destinations"
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                "\nNote: You can customize these add-on options in the Django admin "
                "under Destinations > Add on options and Experience add ons"
            )
        )