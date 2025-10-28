from django.core.management.base import BaseCommand
from destinations.models import AddOnCategory

class Command(BaseCommand):
    help = 'Populate default add-on categories'

    def handle(self, *args, **options):
        categories = [
            {
                'name': 'accommodation',
                'display_name': 'Accommodation Options',
                'description': 'Choose your preferred accommodation level',
                'icon': 'Hotel',
                'order': 1
            },
            {
                'name': 'transport',
                'display_name': 'Transport Options',
                'description': 'Upgrade your transportation',
                'icon': 'Car',
                'order': 2
            },
            {
                'name': 'group_transport',
                'display_name': 'Group Transport',
                'description': 'Shared transportation options for groups',
                'icon': 'Bus',
                'order': 3
            },
            {
                'name': 'meals',
                'display_name': 'Meal Options',
                'description': 'Customize your dining experience',
                'icon': 'Utensils',
                'order': 4
            },
            {
                'name': 'medical',
                'display_name': 'Medical & Insurance',
                'description': 'Additional health and safety coverage',
                'icon': 'Shield',
                'order': 5
            },
            {
                'name': 'experience',
                'display_name': 'Additional Experiences',
                'description': 'Extra activities and experiences',
                'icon': 'Star',
                'order': 6
            }
        ]

        for category_data in categories:
            category, created = AddOnCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.display_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Category already exists: {category.display_name}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully populated add-on categories')
        )