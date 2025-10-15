#!/usr/bin/env python
"""
Script to add multiple images to the Tent Xscape gallery
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import ImageGallery, GalleryImage

def add_tent_xscape_images():
    """Add multiple images to the Tent Xscape gallery"""
    
    # Find the Tent Xscape gallery
    try:
        tent_gallery = ImageGallery.objects.get(title="Tent Xscape")
        print(f"Found gallery: {tent_gallery.title} - {tent_gallery.location}")
        print(f"Current images: {tent_gallery.image_count}")
        
        # Sample image URLs for tent camping (you can replace these with real URLs)
        new_images = [
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/tent-interior.jpg',
                'caption': 'Cozy tent interior setup',
                'order': 1
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/tent-night-view.jpg',
                'caption': 'Tent under the starry night sky',
                'order': 2
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/tent-morning.jpg',
                'caption': 'Beautiful morning view from the tent',
                'order': 3
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/tent-campfire.jpg',
                'caption': 'Evening campfire near the tent',
                'order': 4
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/tent-activities.jpg',
                'caption': 'Fun activities around the camping area',
                'order': 5
            }
        ]
        
        # Add the new images
        created_count = 0
        for img_data in new_images:
            try:
                new_image = GalleryImage.objects.create(
                    gallery=tent_gallery,
                    image=img_data['image'],
                    caption=img_data['caption'],
                    is_main=False,  # The existing image remains main
                    order=img_data['order']
                )
                created_count += 1
                print(f"Added image: {new_image.caption}")
                
            except Exception as e:
                print(f"Error adding image {img_data['caption']}: {e}")
        
        print(f"\nSuccessfully added {created_count} new images!")
        print(f"Total images in gallery: {tent_gallery.image_count}")
        
        # List all images in the gallery
        print(f"\nAll images in '{tent_gallery.title}' gallery:")
        for img in tent_gallery.images.all():
            print(f"  - {img.caption} (Main: {img.is_main}, Order: {img.order})")
            print(f"    URL: {img.image}")
        
    except ImageGallery.DoesNotExist:
        print("Tent Xscape gallery not found!")
        print("Available galleries:")
        for gallery in ImageGallery.objects.all():
            print(f"  - {gallery.title} ({gallery.location})")

def test_api_endpoint():
    """Test the API endpoint to see the gallery with multiple images"""
    print("\n" + "="*50)
    print("API TEST - Gallery with Multiple Images")
    print("="*50)
    
    try:
        tent_gallery = ImageGallery.objects.get(title="Tent Xscape")
        
        # Simulate API response
        from gallery.serializers import ImageGallerySerializer
        from django.test import RequestFactory
        
        factory = RequestFactory()
        request = factory.get('/api/gallery/galleries/')
        
        serializer = ImageGallerySerializer(tent_gallery, context={'request': request})
        data = serializer.data
        
        print(f"Gallery: {data['title']}")
        print(f"Location: {data['location']}")
        print(f"Description: {data['description']}")
        print(f"Image Count: {data['image_count']}")
        print(f"Main Image URL: {data['main_image_url']}")
        print(f"\nAll Images ({len(data['images'])}):")
        
        for i, img in enumerate(data['images'], 1):
            print(f"  {i}. {img['caption']}")
            print(f"     URL: {img['image_url']}")
            print(f"     Main: {img['is_main']}, Order: {img['order']}")
        
    except Exception as e:
        print(f"Error testing API: {e}")

if __name__ == "__main__":
    add_tent_xscape_images()
    test_api_endpoint()