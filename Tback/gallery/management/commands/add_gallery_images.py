"""
Django management command to bulk add gallery images via URLs
"""
from django.core.management.base import BaseCommand
from gallery.models import GalleryImage, GalleryCategory
from destinations.models import Destination


class Command(BaseCommand):
    help = 'Add multiple images to gallery via URLs'

    def add_arguments(self, parser):
        parser.add_argument('--category', type=str, required=True, help='Gallery category name or slug')
        parser.add_argument('--location', type=str, required=True, help='Location name')
        parser.add_argument('--urls', nargs='+', required=True, help='List of image URLs')
        parser.add_argument('--destination', type=str, help='Destination slug (optional)')
        parser.add_argument('--photographer', type=str, help='Photographer name (optional)')
        parser.add_argument('--featured', action='store_true', help='Mark images as featured')

    def handle(self, *args, **options):
        category_name = options['category']
        location = options['location']
        image_urls = options['urls']
        destination_slug = options.get('destination')
        photographer = options.get('photographer', '')
        is_featured = options.get('featured', False)
        
        # Get or create category
        try:
            category = GalleryCategory.objects.get(name__iexact=category_name)
        except GalleryCategory.DoesNotExist:
            try:
                category = GalleryCategory.objects.get(slug=category_name)
            except GalleryCategory.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Category "{category_name}" not found. Available categories:')
                )
                for cat in GalleryCategory.objects.all():
                    self.stdout.write(f'  - {cat.name} (slug: {cat.slug})')
                return
        
        # Get destination if provided
        destination = None
        if destination_slug:
            try:
                destination = Destination.objects.get(slug=destination_slug)
            except Destination.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Destination "{destination_slug}" not found. Continuing without destination.')
                )
        
        # Add images
        created_count = 0
        errors = []
        
        for i, url in enumerate(image_urls):
            try:
                # Validate URL
                if not url.startswith(('http://', 'https://')):
                    errors.append(f"Invalid URL format: {url}")
                    continue
                
                # Create the image
                image = GalleryImage.objects.create(
                    title=f"{location} - Image {i + 1}",
                    description=f"Beautiful view from {location}",
                    image=url,
                    location=location,
                    category=category,
                    destination=destination,
                    photographer=photographer,
                    is_featured=is_featured and i == 0,  # Only first image is featured
                    order=i + 1
                )
                
                created_count += 1
                self.stdout.write(f'✅ Added image {i + 1}: {image.title}')
                
            except Exception as e:
                errors.append(f"Error creating image from {url}: {str(e)}")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully added {created_count} images to gallery')
        )
        
        if errors:
            self.stdout.write(self.style.WARNING('Errors encountered:'))
            for error in errors:
                self.stdout.write(f'  - {error}')
        
        # Show summary
        total_images = GalleryImage.objects.filter(category=category, location=location).count()
        self.stdout.write(f'📊 Total images for "{location}" in "{category.name}": {total_images}')


# Example usage:
# python manage.py add_gallery_images --category "Nature" --location "Kakum Forest" --urls "https://example.com/forest1.jpg" "https://example.com/forest2.jpg" --photographer "John Doe" --featured