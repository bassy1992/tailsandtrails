"""
Django management command to bulk add images to destinations via URLs
"""
from django.core.management.base import BaseCommand
from destinations.models import Destination, DestinationImage


class Command(BaseCommand):
    help = 'Add multiple images to a destination via URLs'

    def add_arguments(self, parser):
        parser.add_argument('destination_slug', type=str, help='Destination slug')
        parser.add_argument('--urls', nargs='+', required=True, help='List of image URLs')
        parser.add_argument('--clear', action='store_true', help='Clear existing images first')

    def handle(self, *args, **options):
        destination_slug = options['destination_slug']
        image_urls = options['urls']
        clear_existing = options['clear']
        
        try:
            destination = Destination.objects.get(slug=destination_slug)
        except Destination.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Destination with slug "{destination_slug}" not found')
            )
            return
        
        if clear_existing:
            deleted_count = destination.images.count()
            destination.images.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Deleted {deleted_count} existing images')
            )
        
        # Add new images
        created_count = 0
        for i, url in enumerate(image_urls):
            image = DestinationImage.objects.create(
                destination=destination,
                image=url,
                alt_text=f"{destination.name} - Image {i + 1}",
                order=i + 1,
                is_primary=(i == 0 and not destination.images.exists())  # First image is primary if no images exist
            )
            created_count += 1
            self.stdout.write(f'✅ Added image {i + 1}: {url}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {created_count} images to "{destination.name}"')
        )
        
        # Show current image count
        total_images = destination.images.count()
        self.stdout.write(f'📊 Total images for "{destination.name}": {total_images}')


# Example usage:
# python manage.py add_destination_images tent-escape --urls "https://example.com/tent1.jpg" "https://example.com/tent2.jpg" "https://example.com/tent3.jpg"