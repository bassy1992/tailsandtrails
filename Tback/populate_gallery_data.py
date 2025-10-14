#!/usr/bin/env python3
"""
Script to populate gallery with sample data
Run this after deploying to Railway to add sample gallery content
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import GalleryCategory, GalleryImage, GalleryVideo
from destinations.models import Destination

def create_gallery_categories():
    """Create gallery categories"""
    categories = [
        {'name': 'Heritage', 'description': 'Historical sites and cultural heritage locations'},
        {'name': 'Nature', 'description': 'Natural landscapes, waterfalls, and scenic views'},
        {'name': 'Culture', 'description': 'Local culture, traditions, and people'},
        {'name': 'Adventure', 'description': 'Adventure activities and outdoor experiences'},
        {'name': 'Coastal', 'description': 'Beaches, coastal areas, and marine life'},
        {'name': 'Urban', 'description': 'City life, modern architecture, and urban scenes'},
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = GalleryCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        created_categories.append(category)
        print(f"{'Created' if created else 'Found'} category: {category.name}")
    
    return created_categories

def create_sample_images():
    """Create sample gallery images (without actual files for now)"""
    heritage_cat = GalleryCategory.objects.get(name='Heritage')
    nature_cat = GalleryCategory.objects.get(name='Nature')
    culture_cat = GalleryCategory.objects.get(name='Culture')
    
    sample_images = [
        {
            'title': 'Cape Coast Castle',
            'description': 'Historic UNESCO World Heritage Site showcasing Ghana\'s colonial history',
            'location': 'Cape Coast',
            'category': heritage_cat,
            'is_featured': True,
            'photographer': 'Tales & Trails Team'
        },
        {
            'title': 'Wli Waterfalls',
            'description': 'Ghana\'s highest waterfall in the Volta Region',
            'location': 'Volta Region',
            'category': nature_cat,
            'is_featured': True,
            'photographer': 'Tales & Trails Team'
        },
        {
            'title': 'Kente Weaving',
            'description': 'Traditional Kente cloth weaving demonstration',
            'location': 'Kumasi',
            'category': culture_cat,
            'is_featured': False,
            'photographer': 'Tales & Trails Team'
        },
    ]
    
    for img_data in sample_images:
        image, created = GalleryImage.objects.get_or_create(
            title=img_data['title'],
            defaults=img_data
        )
        print(f"{'Created' if created else 'Found'} image: {image.title}")

def create_sample_videos():
    """Create sample gallery videos (without actual files for now)"""
    heritage_cat = GalleryCategory.objects.get(name='Heritage')
    nature_cat = GalleryCategory.objects.get(name='Nature')
    
    sample_videos = [
        {
            'title': 'Cape Coast Castle Tour',
            'description': 'Virtual tour of the historic Cape Coast Castle',
            'location': 'Cape Coast',
            'category': heritage_cat,
            'duration': '8:45',
            'is_featured': True,
            'videographer': 'Tales & Trails Team'
        },
        {
            'title': 'Kakum Canopy Walk',
            'description': 'Experience the thrilling canopy walk adventure',
            'location': 'Kakum National Park',
            'category': nature_cat,
            'duration': '6:30',
            'is_featured': True,
            'videographer': 'Tales & Trails Team'
        },
    ]
    
    for vid_data in sample_videos:
        video, created = GalleryVideo.objects.get_or_create(
            title=vid_data['title'],
            defaults=vid_data
        )
        print(f"{'Created' if created else 'Found'} video: {video.title}")

def main():
    print("🎨 Populating Gallery Data")
    print("=" * 40)
    
    # Create categories
    create_gallery_categories()
    
    # Create sample content
    create_sample_images()
    create_sample_videos()
    
    # Print summary
    print("\n📊 Gallery Summary:")
    print(f"Categories: {GalleryCategory.objects.count()}")
    print(f"Images: {GalleryImage.objects.count()}")
    print(f"Videos: {GalleryVideo.objects.count()}")
    
    print("\n✅ Gallery data population completed!")
    print("\n📝 Next steps:")
    print("1. Access Django admin to upload actual images and videos")
    print("2. Update gallery items with real media files")
    print("3. Set featured status and organize content")

if __name__ == '__main__':
    main()