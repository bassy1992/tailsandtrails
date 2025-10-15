#!/usr/bin/env python
"""
Fix Cape Coast Castle gallery images with proper captions and unique images
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import ImageGallery, GalleryImage

def fix_cape_coast_images():
    """Fix Cape Coast Castle gallery images"""
    
    try:
        cape_coast = ImageGallery.objects.get(title="Cape Coast Castle")
        print(f"Fixing gallery: {cape_coast.title}")
        
        # Get all images
        images = list(cape_coast.images.all())
        print(f"Found {len(images)} images")
        
        # Remove duplicate images (keep only unique URLs)
        seen_urls = set()
        images_to_delete = []
        
        for img in images:
            if img.image in seen_urls:
                images_to_delete.append(img)
                print(f"Marking duplicate image {img.id} for deletion: {img.image}")
            else:
                seen_urls.add(img.image)
        
        # Delete duplicates
        for img in images_to_delete:
            img.delete()
            print(f"Deleted duplicate image {img.id}")
        
        # Refresh the images list
        images = list(cape_coast.images.all())
        
        # Update captions and add more diverse images
        cape_coast_images = [
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/pictures/Aburi%20Eco%20Resort-14.jpg',
                'caption': 'Historic Cape Coast Castle exterior view',
                'is_main': True,
                'order': 0
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/pictures/Aburi%20Eco%20Resort-37.jpg',
                'caption': 'Castle courtyard and colonial architecture',
                'is_main': False,
                'order': 1
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/cape-coast-dungeon.jpg',
                'caption': 'Historical dungeons - Door of No Return',
                'is_main': False,
                'order': 2
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/cape-coast-ocean-view.jpg',
                'caption': 'Stunning Atlantic Ocean view from castle walls',
                'is_main': False,
                'order': 3
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/cape-coast-museum.jpg',
                'caption': 'Castle museum displaying Ghana\'s history',
                'is_main': False,
                'order': 4
            },
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/cape-coast-sunset.jpg',
                'caption': 'Beautiful sunset over Cape Coast Castle',
                'is_main': False,
                'order': 5
            }
        ]
        
        # Update existing images and add new ones
        existing_images = {img.image: img for img in images}
        
        for img_data in cape_coast_images:
            if img_data['image'] in existing_images:
                # Update existing image
                img = existing_images[img_data['image']]
                img.caption = img_data['caption']
                img.is_main = img_data['is_main']
                img.order = img_data['order']
                img.save()
                print(f"Updated existing image: {img.caption}")
            else:
                # Create new image
                new_img = GalleryImage.objects.create(
                    gallery=cape_coast,
                    image=img_data['image'],
                    thumbnail=img_data['image'],
                    caption=img_data['caption'],
                    is_main=img_data['is_main'],
                    order=img_data['order']
                )
                print(f"Created new image: {new_img.caption}")
        
        # Final check
        print(f"\nFinal result:")
        print(f"Gallery: {cape_coast.title}")
        print(f"Total images: {cape_coast.image_count}")
        print("Images:")
        for img in cape_coast.images.all():
            print(f"  - {img.caption} {'(Main)' if img.is_main else ''}")
            
    except ImageGallery.DoesNotExist:
        print("Cape Coast Castle gallery not found!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_cape_coast_images()