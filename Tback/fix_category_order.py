import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tback.settings')
django.setup()

from destinations.models import AddOnCategory

# Update the order for categories
categories_order = {
    'accommodation': 1,
    'transport': 2,
    'group_transport': 3,
    'meals': 4,
    'medical': 5,
    'experience': 6
}

for name, order in categories_order.items():
    try:
        category = AddOnCategory.objects.get(name=name)
        category.order = order
        category.save()
        print(f'Updated {category.display_name} to order {order}')
    except AddOnCategory.DoesNotExist:
        print(f'Category {name} not found')

print('\nFinal category list:')
print('-' * 60)
categories = AddOnCategory.objects.all().order_by('order')
for c in categories:
    print(f'Order {c.order}: {c.display_name} (ID: {c.id})')
