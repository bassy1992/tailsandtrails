import os
import sys
import django

# Add the Tback directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.settings')
django.setup()

from destinations.models import AddOnCategory

try:
    category = AddOnCategory.objects.get(name='group_transport')
    category.display_name = 'Group Transport'
    category.save()
    print(f'Updated display name to: {category.display_name}')
except AddOnCategory.DoesNotExist:
    print('Group Transport category not found')
