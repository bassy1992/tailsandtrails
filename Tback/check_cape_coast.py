#!/usr/bin/env python
"""
Check Cape Coast Castle gallery specifically
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import ImageGallery

def check_cape_coast():
    """Check Cape Coast Castle gallery"""
    
    print("🔍 SEARCHING FOR CAPE COAST CASTLE")
    print("=" * 40)
    
    # Search for Cape Coast galleries
    cape_coast_galleries = ImageGallery.objects.filter(title__icontains='cape')
    print(f"Galleries with 'cape' in title: {cape_coast_galleries.count()}")
    
    for gallery in cape_coast_galleries:
        print(f"\n📍 Found: {gallery.title}")
        print(f"   ID: {gallery.id}")
        print(f"   Location: {gallery.location}")
        print(f"   Category: {gallery.category.name}")
        print(f"   Images: {gallery.image_count}")
        print(f"   Slug: {gallery.slug}")
    
    # Search by location
    cape_coast_location = ImageGallery.objects.filter(location__icontains='cape')
    print(f"\nGalleries with 'cape' in location: {cape_coast_location.count()}")
    
    for gallery in cape_coast_location:
        print(f"\n📍 Found: {gallery.title}")
        print(f"   Location: {gallery.location}")
        print(f"   Category: {gallery.category.name}")
        print(f"   Images: {gallery.image_count}")
    
    # List all galleries
    print(f"\n📊 ALL GALLERIES:")
    all_galleries = ImageGallery.objects.all()
    
    for gallery in all_galleries:
        print(f"\n🏛️ {gallery.title}")
        print(f"   Location: {gallery.location}")
        print(f"   Category: {gallery.category.name}")
        print(f"   Images: {gallery.image_count}")
        print(f"   Featured: {gallery.is_featured}")

if __name__ == "__main__":
    check_cape_coast()