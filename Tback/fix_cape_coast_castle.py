#!/usr/bin/env python
"""
Fix Cape Coast Castle gallery
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import ImageGallery, GalleryCategory, GalleryImage

def fix_cape_coast_castle():
    """Fix the Cape Coast Castle gallery"""
    
    print("🔧 FIXING CAPE COAST CASTLE GALLERY")
    print("=" * 50)
    
    # Get the corrupted gallery
    try:
        corrupted_gallery = ImageGallery.objects.get(title="Cape Coas")
        print(f"Found corrupted gallery: {corrupted_gallery.title}")
        print(f"Current category: {corrupted_gallery.category.name}")
        print(f"Current images: {corrupted_gallery.image_count}")
        
        # Get Heritage category
        heritage_category = GalleryCategory.objects.get(name="Heritage")
        
        # Fix the gallery
        corrupted_gallery.title = "Cape Coast Castle"
        corrupted_gallery.slug = "cape-coast-castle-cape-coast-gallery"
        corrupted_gallery.category = heritage_category
        corrupted_gallery.description = "Historic UNESCO World Heritage Site showcasing Ghana's colonial history"
        corrupted_gallery.save()
        
        print(f"✅ Fixed gallery title: {corrupted_gallery.title}")
        print(f"✅ Fixed category: {corrupted_gallery.category.name}")
        print(f"✅ Fixed slug: {corrupted_gallery.slug}")
        
        # Check current images
        current_images = corrupted_gallery.images.all()
        print(f"\nCurrent images ({len(current_images)}):")
        for i, img in enumerate(current_images, 1):
            print(f"  {i}. {img.caption}")
        
        # Add the missing 6th image if needed
        if len(current_images) < 6:
            print(f"\n🔧 Adding missing image...")
            GalleryImage.objects.create(
                gallery=corrupted_gallery,
                image='https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/cape-coast-sunset.jpg',
                thumbnail='https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/cape-coast-sunset.jpg',
                caption='Beautiful sunset over Cape Coast Castle',
                is_main=False,
                order=5
            )
            print(f"✅ Added 6th image")
        
        # Final verification
        print(f"\n✅ FINAL RESULT:")
        print(f"   Title: {corrupted_gallery.title}")
        print(f"   Category: {corrupted_gallery.category.name}")
        print(f"   Location: {corrupted_gallery.location}")
        print(f"   Images: {corrupted_gallery.image_count}")
        print(f"   Slug: {corrupted_gallery.slug}")
        
    except ImageGallery.DoesNotExist:
        print("❌ Corrupted gallery not found")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    fix_cape_coast_castle()