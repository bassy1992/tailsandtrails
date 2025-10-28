# Generated migration to add Group transportation add-on category

from django.db import migrations
from django.utils.text import slugify


def add_group_transportation_category(apps, schema_editor):
    """Add Group transportation to AddOnCategory"""
    AddOnCategory = apps.get_model('tickets', 'AddOnCategory')
    
    # Check if it already exists
    if not AddOnCategory.objects.filter(slug='group-transportation').exists():
        AddOnCategory.objects.create(
            name='Group transportation',
            slug='group-transportation',
            category_type='transport',
            description='Group transportation services for tours and excursions',
            icon='Bus',
            is_active=True,
            order=2  # Place after individual transport options
        )


def remove_group_transportation_category(apps, schema_editor):
    """Remove Group transportation category if migration is reversed"""
    AddOnCategory = apps.get_model('tickets', 'AddOnCategory')
    AddOnCategory.objects.filter(slug='group-transportation').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_alter_ticketpurchase_user'),
    ]

    operations = [
        migrations.RunPython(
            add_group_transportation_category,
            remove_group_transportation_category
        ),
    ]
