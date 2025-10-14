#!/usr/bin/env python3
"""
Script to populate gallery with sample data
"""
import os
import sys
import django
from datetime import date, datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import GalleryCategory, GalleryImage, GalleryVideo, GalleryTag, ImageTag, VideoTag
from destinations.models import Destination

def create_categories():
    """Create gallery categories"""
    categories = [
        {'name': 'Heritage', 'description': 'Historical sites and cultural heritage'},
        {'name': 'Nature', 'description': 'Natural landscapes and wildlife'},
        {'name': 'Culture', 'description': 'Local culture and traditions'},
        {'name': 'Adventure', 'description': 'Adventure activities and sports'},
        {'name': 'Coastal', 'description': 'Beaches and coastal areas'},
        {'name': 'Urban', 'description': 'City life and modern Ghana'},
    ]
    
    created_categories = []
    for i, cat_data in enumerate(categories):
        category, created = GalleryCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'order': i
            }
        )
        created_categories.append(category)
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"ℹ️ Category already exists: {category.name}")
    
    return created_categories

def create_tags():
    """Create gallery tags"""
    tag_names = [
        'UNESCO', 'Castle', 'Waterfall', 'Forest', 'Beach', 'Market', 
        'Traditional', 'Modern', 'Architecture', 'Wildlife', 'Hiking',
        'Cultural', 'Festival', 'Food', 'Art', 'Music', 'Dance'
    ]
    
    created_tags = []
    for tag_name in tag_names:
        tag, created = GalleryTag.objects.get_or_create(name=tag_name)
        created_tags.append(tag)
        if created:
            print(f"✅ Created tag: {tag.name}")
    
    return created_tags

def create_sample_images():
    """Create sample gallery images"""
    # Note: In a real scenario, you would upload actual image files
    # For now, we'll create records without actual files
    
    heritage_cat = GalleryCategory.objects.get(name='Heritage')
    nature_cat = GalleryCategory.objects.get(name='Nature')
    culture_cat = GalleryCategory.objects.get(name='Culture')
    adventure_cat = GalleryCategory.objects.get(name='Adventure')
    coastal_cat = GalleryCategory.objects.get(name='Coastal')
    
    sample_images = [
        {
            'title': 'Cape Coast Castle',
            'description': 'Historic UNESCO World Heritage Site showcasing Ghana\'s colonial history',
            'location': 'Cape Coast',
            'category': heritage_cat,
            'photographer': 'Ghana Tourism Board',
            'is_featured': True,
            'tags': ['UNESCO', 'Castle', 'Architecture']
        },
        {
            'title': 'Wli Waterfalls',
            'description': 'Ghana\'s highest waterfall in the Volta Region',
            'location': 'Volta Region',
            'category': nature_cat,
            'photogra