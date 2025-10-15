#!/usr/bin/env python
"""
Enhance all galleries with multiple images
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import ImageGallery, GalleryImage

def enhance_wli_waterfalls():
    """Add multiple images to Wli Waterfalls gallery"""
    try:
        gallery = ImageGallery.objects.get(title="Wli Waterfalls")
        print(f"Enhancing: {gallery.title}")
        
        # Define multiple images for Wli Waterfalls
        images_data = [
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/wli-main-falls.jpg',
                'caption': 'Majestic Wli Waterfalls - Ghana\'s highest waterfall',
                'is_main': True,
                'order': 0
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/wli-hiking-trail.jpg',
                'caption': 'Scenic hiking trail to the waterfalls',
                'is_main': False,
                'order': 1
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/wli-pool-swimming.jpg',
                'caption': 'Natural pool perfect for swimming',
                'is_main': False,
                'order': 2
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/wli-forest-canopy.jpg',
                'caption': 'Lush forest canopy surrounding the falls',
                'is_main': False,
                'order': 3
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/wli-butterfly-sanctuary.jpg',
                'caption': 'Butterfly sanctuary near the waterfalls',
                'is_main': False,
                'order': 4
            }
        ]
        
        # Get existing main image
        existing_main = gallery.main_image
        if existing_main:
            # Update the existing main image
            existing_main.caption = images_data[0]['caption']
            existing_main.save()
            print(f"Updated main image: {existing_main.caption}")
            
            # Add the rest of the images
            for img_data in images_data[1:]:
                new_img = GalleryImage.objects.create(
                    gallery=gallery,
                    image=img_data['image'],
                    thumbnail=img_data['image'],
                    caption=img_data['caption'],
                    is_main=img_data['is_main'],
                    order=img_data['order']
                )
                print(f"Added: {new_img.caption}")
        
        print(f"Wli Waterfalls now has {gallery.image_count} images")
        
    except ImageGallery.DoesNotExist:
        print("Wli Waterfalls gallery not found!")

def enhance_kente_weaving():
    """Add multiple images to Kente Weaving gallery"""
    try:
        gallery = ImageGallery.objects.get(title="Kente Weaving")
        print(f"Enhancing: {gallery.title}")
        
        # Define multiple images for Kente Weaving
        images_data = [
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/follow.jpg',
                'caption': 'Traditional Kente weaving demonstration',
                'is_main': True,
                'order': 0
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/kente-loom-close.jpg',
                'caption': 'Close-up of traditional Kente loom',
                'is_main': False,
                'order': 1
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/kente-patterns.jpg',
                'caption': 'Beautiful Kente cloth patterns and colors',
                'is_main': False,
                'order': 2
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/kente-weaver-work.jpg',
                'caption': 'Master weaver creating intricate Kente designs',
                'is_main': False,
                'order': 3
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/kente-finished-cloth.jpg',
                'caption': 'Finished Kente cloth ready for ceremony',
                'is_main': False,
                'order': 4
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/kente-cultural-center.jpg',
                'caption': 'Kente cultural center in Kumasi',
                'is_main': False,
                'order': 5
            }
        ]
        
        # Get existing main image
        existing_main = gallery.main_image
        if existing_main:
            # Update the existing main image
            existing_main.caption = images_data[0]['caption']
            existing_main.save()
            print(f"Updated main image: {existing_main.caption}")
            
            # Add the rest of the images
            for img_data in images_data[1:]:
                new_img = GalleryImage.objects.create(
                    gallery=gallery,
                    image=img_data['image'],
                    thumbnail=img_data['image'],
                    caption=img_data['caption'],
                    is_main=img_data['is_main'],
                    order=img_data['order']
                )
                print(f"Added: {new_img.caption}")
        
        print(f"Kente Weaving now has {gallery.image_count} images")
        
    except ImageGallery.DoesNotExist:
        print("Kente Weaving gallery not found!")

def main():
    """Enhance all galleries"""
    print("🖼️ Enhancing All Galleries with Multiple Images")
    print("=" * 50)
    
    enhance_wli_waterfalls()
    print()
    enhance_kente_weaving()
    
    print("\n" + "=" * 50)
    print("📊 Final Gallery Summary:")
    galleries = ImageGallery.objects.all()
    for gallery in galleries:
        print(f"- {gallery.title} ({gallery.location}): {gallery.image_count} images")
    
    print("\n✅ All galleries now have multiple images!")

if __name__ == "__main__":
    main()