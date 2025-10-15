#!/usr/bin/env python
"""
Migration script to convert existing GalleryImage data to the new ImageGallery + GalleryImage structure
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from gallery.models import GalleryImage, ImageGallery, GalleryCategory
from destinations.models import Destination

def migrate_gallery_data():
    """
    Convert existing single GalleryImage records to ImageGallery with related GalleryImage records
    """
    print("Starting gallery data migration...")
    
    # First, let's see what we have
    try:
        # Try to get existing images (old structure)
        from django.db import connection
        cursor = connection.cursor()
        
        # Check if old table structure exists
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='gallery_galleryimage'
        """)
        
        if cursor.fetchone():
            print("Found existing gallery_galleryimage table")
            
            # Get existing data before migration
            cursor.execute("""
                SELECT id, title, slug, description, image, thumbnail, location, 
                       category_id, destination_id, photographer, date_taken, camera_info,
                       is_featured, is_active, "order", created_at, updated_at
                FROM gallery_galleryimage
            """)
            
            existing_images = cursor.fetchall()
            print(f"Found {len(existing_images)} existing images to migrate")
            
            # Create ImageGallery records and move images
            migrated_count = 0
            for img_data in existing_images:
                (old_id, title, slug, description, image_url, thumbnail, location,
                 category_id, destination_id, photographer, date_taken, camera_info,
                 is_featured, is_active, order, created_at, updated_at) = img_data
                
                try:
                    # Get category and destination objects
                    category = GalleryCategory.objects.get(id=category_id) if category_id else None
                    destination = Destination.objects.get(id=destination_id) if destination_id else None
                    
                    # Create ImageGallery
                    gallery = ImageGallery.objects.create(
                        title=title,
                        slug=f"{slug}-gallery" if slug else None,
                        description=description,
                        location=location,
                        category=category,
                        destination=destination,
                        photographer=photographer,
                        date_taken=date_taken,
                        is_featured=is_featured,
                        is_active=is_active,
                        order=order,
                        created_at=created_at,
                        updated_at=updated_at
                    )
                    
                    # Create the related GalleryImage
                    GalleryImage.objects.create(
                        gallery=gallery,
                        image=image_url,
                        thumbnail=thumbnail,
                        caption=f"Main image for {title}",
                        camera_info=camera_info,
                        is_main=True,
                        order=0,
                        created_at=created_at,
                        updated_at=updated_at
                    )
                    
                    migrated_count += 1
                    print(f"Migrated: {title} - {location}")
                    
                except Exception as e:
                    print(f"Error migrating image {old_id} ({title}): {e}")
            
            print(f"Successfully migrated {migrated_count} images to new structure")
            
        else:
            print("No existing gallery_galleryimage table found - this might be a fresh installation")
            
    except Exception as e:
        print(f"Error during migration: {e}")
        print("This might be expected if running on a fresh database")

def create_sample_multi_image_gallery():
    """Create a sample gallery with multiple images for testing"""
    print("\nCreating sample multi-image gallery...")
    
    try:
        # Get or create a category
        category, created = GalleryCategory.objects.get_or_create(
            name="Adventure Activities",
            defaults={'description': 'Outdoor adventure activities and experiences'}
        )
        
        # Create a sample gallery with multiple images
        gallery = ImageGallery.objects.create(
            title="Tent Xscape Adventure",
            description="Multiple views of our exciting tent camping experience",
            location="Aburi",
            category=category,
            photographer="Adventure Team",
            is_featured=True,
            is_active=True
        )
        
        # Add multiple sample images
        sample_images = [
            {
                'image': 'https://tailsandtrailsmedia.sfo3.cdn.digitaloceanspaces.com/Aburi%20Eco%20Resort-2.jpg',
                'caption': 'Main tent setup view',
                'is_main': True,
                'order': 0
            },
            {
                'image': 'https://example.com/tent-interior.jpg',
                'caption': 'Cozy tent interior',
                'is_main': False,
                'order': 1
            },
            {
                'image': 'https://example.com/tent-night.jpg',
                'caption': 'Tent under the stars',
                'is_main': False,
                'order': 2
            },
            {
                'image': 'https://example.com/tent-morning.jpg',
                'caption': 'Morning view from tent',
                'is_main': False,
                'order': 3
            }
        ]
        
        for img_data in sample_images:
            GalleryImage.objects.create(
                gallery=gallery,
                **img_data
            )
        
        print(f"Created sample gallery '{gallery.title}' with {len(sample_images)} images")
        print(f"Gallery ID: {gallery.id}")
        
    except Exception as e:
        print(f"Error creating sample gallery: {e}")

if __name__ == "__main__":
    migrate_gallery_data()
    create_sample_multi_image_gallery()
    print("\nMigration completed!")