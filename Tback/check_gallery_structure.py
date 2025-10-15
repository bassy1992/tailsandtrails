#!/usr/bin/env python
"""
Check the current gallery structure
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import ImageGallery, GalleryCategory

def check_gallery_structure():
    """Check how galleries are organized by category"""
    
    print("📊 CURRENT GALLERY STRUCTURE")
    print("=" * 50)
    
    # Get all galleries
    all_galleries = ImageGallery.objects.all()
    print(f"Total Galleries: {all_galleries.count()}")
    
    print("\n🏷️ BY CATEGORY:")
    categories = GalleryCategory.objects.all()
    
    for category in categories:
        galleries_in_category = category.image_galleries.all()
        print(f"\n📂 {category.name} ({galleries_in_category.count()} galleries):")
        
        if galleries_in_category.exists():
            for gallery in galleries_in_category:
                print(f"   - {gallery.title} ({gallery.location})")
                print(f"     📸 {gallery.image_count} images")
                print(f"     🌟 Featured: {gallery.is_featured}")
        else:
            print("   (No galleries in this category)")
    
    print("\n📍 BY LOCATION:")
    locations = set(gallery.location for gallery in all_galleries)
    
    for location in sorted(locations):
        galleries_in_location = all_galleries.filter(location=location)
        print(f"\n🌍 {location} ({galleries_in_location.count()} galleries):")
        
        for gallery in galleries_in_location:
            print(f"   - {gallery.title} ({gallery.category.name})")
            print(f"     📸 {gallery.image_count} images")
    
    print("\n" + "=" * 50)
    print("🎯 FRONTEND DESIGN ANALYSIS:")
    print("✅ Frontend shows MULTIPLE gallery cards in a grid")
    print("✅ Each card represents ONE gallery (like Cape Coast Castle)")
    print("✅ Each gallery can contain MULTIPLE images (slider)")
    print("✅ Users can filter by category to see relevant galleries")
    print("✅ Each gallery card shows image count badge")
    
    print("\n💡 CURRENT STRUCTURE:")
    print("- One gallery per major destination/attraction")
    print("- Each gallery contains multiple images of that destination")
    print("- Categories group related types of destinations")
    print("- Frontend displays all galleries, filterable by category")

if __name__ == "__main__":
    check_gallery_structure()