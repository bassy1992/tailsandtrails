#!/usr/bin/env python
"""
Check Cape Coast Castle gallery images
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import ImageGallery, GalleryImage

def check_cape_coast_images():
    """Check Cape Coast Castle gallery images"""
    
    try:
        cape_coast = ImageGallery.objects.get(title="Cape Coast Castle")
        print(f"Gallery: {cape_coast.title}")
        print(f"Location: {cape_coast.location}")
        print(f"Total images: {cape_coast.image_count}")
        main_img = cape_coast.main_image
        print(f"Main image URL: {main_img.image if main_img else 'None'}")
        print("\nDetailed image info:")
        
        for i, img in enumerate(cape_coast.images.all(), 1):
            print(f"  {i}. ID: {img.id}")
            print(f"     Caption: '{img.caption}'")
            print(f"     Image URL: '{img.image}'")
            print(f"     Thumbnail: '{img.thumbnail}'")
            print(f"     Is Main: {img.is_main}")
            print(f"     Order: {img.order}")
            print()
            
    except ImageGallery.DoesNotExist:
        print("Cape Coast Castle gallery not found!")

if __name__ == "__main__":
    check_cape_coast_images()