from django.core.management.base import BaseCommand
from destinations.models import Destination, PricingTier
from decimal import Decimal

class Command(BaseCommand):
    help = 'Set up sample pricing tiers for destinations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--destination-id',
            type=int,
            help='Set up pricing tiers for a specific destination ID',
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing pricing tiers',
        )

    def handle(self, *args, **options):
        destination_id = options.get('destination_id')
        overwrite = options.get('overwrite', False)
        
        if destination_id:
            try:
                destination = Destination.objects.get(id=destination_id)
                destinations = [destination]
            except Destination.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Destination with ID {destination_id} not found')
                )
                return
        else:
            destinations = Destination.objects.filter(is_active=True)
        
        total_created = 0
        total_skipped = 0
        
        for destination in destinations:
            # Check if destination already has pricing tiers
            existing_tiers = destination.pricing_tiers.filter(is_active=True).count()
            
            if existing_tiers > 0 and not overwrite:
                self.stdout.write(
                    f'Skipping {destination.name} - already has {existing_tiers} pricing tiers'
                )
                total_skipped += 1
                continue
            
            if overwrite and existing_tiers > 0:
                # Delete existing tiers
                destination.pricing_tiers.all().delete()
                self.stdout.write(
                    f'Deleted {existing_tiers} existing pricing tiers for {destination.name}'
                )
            
            # Create sample pricing tiers based on base price
            base_price = destination.price
            
            # Define pricing strategy: larger groups get discounts
            pricing_tiers = [
                {
                    'min_people': 1,
                    'max_people': 1,
                    'price_per_person': base_price,  # Solo traveler - full price
                },
                {
                    'min_people': 2,
                    'max_people': 3,
                    'price_per_person': base_price * Decimal('0.95'),  # 5% discount for 2-3 people
                },
                {
                    'min_people': 4,
                    'max_people': 6,
                    'price_per_person': base_price * Decimal('0.90'),  # 10% discount for 4-6 people
                },
                {
                    'min_people': 7,
                    'max_people': 10,
                    'price_per_person': base_price * Decimal('0.85'),  # 15% discount for 7-10 people
                },
                {
                    'min_people': 11,
                    'max_people': None,  # Unlimited
                    'price_per_person': base_price * Decimal('0.80'),  # 20% discount for 11+ people
                },
            ]
            
            created_count = 0
            for tier_data in pricing_tiers:
                # Don't create tiers that exceed max group size
                if tier_data['min_people'] > destination.max_group_size:
                    continue
                
                # Adjust max_people if it exceeds destination max_group_size
                max_people = tier_data['max_people']
                if max_people and max_people > destination.max_group_size:
                    max_people = destination.max_group_size
                
                # Skip if min_people equals max_people and we already have that tier
                if (max_people and tier_data['min_people'] == max_people and 
                    created_count > 0):
                    continue
                
                PricingTier.objects.create(
                    destination=destination,
                    min_people=tier_data['min_people'],
                    max_people=max_people,
                    price_per_person=tier_data['price_per_person'].quantize(Decimal('0.01')),
                    is_active=True
                )
                created_count += 1
            
            total_created += created_count
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created {created_count} pricing tiers for {destination.name} '
                    f'(Base price: GH₵{base_price})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSummary: Created {total_created} pricing tiers total, '
                f'skipped {total_skipped} destinations'
            )
        )
        
        if total_created > 0:
            self.stdout.write(
                self.style.WARNING(
                    '\nNote: You can customize these pricing tiers in the Django admin '
                    'under Destinations > Pricing tiers'
                )
            )