#!/usr/bin/env python
"""
Create a custom migration to handle the gallery model changes
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from django.db import migrations, models
import django.db.models.deletion
from django.utils.text import slugify

def create_image_galleries_from_existing(apps, schema_editor):
    """
    Migration function to create ImageGallery records from existing GalleryImage records
    """
    # Get the old model state
    GalleryImage = apps.get_model('gallery', 'GalleryImage')
    ImageGallery = apps.get_model('gallery', 'ImageGallery')
    
    # Get all existing images
    existing_images = GalleryImage.objects.all()
    
    for old_image in existing_images:
        # Create a new ImageGallery for each old image
        gallery = ImageGallery.objects.create(
            title=old_image.title,
            slug=old_image.slug + '-gallery' if old_image.slug else slugify(f"{old_image.title}-gallery"),
            description=old_image.description,
            location=old_image.location,
            category_id=old_image.category_id,
            destination_id=old_image.destination_id,
            photographer=old_image.photographer,
            date_taken=old_image.date_taken,
            is_featured=old_image.is_featured,
            is_active=old_image.is_active,
            order=old_image.order,
            created_at=old_image.created_at,
            updated_at=old_image.updated_at
        )
        
        # Update the old image to reference the new gallery
        old_image.gallery_id = gallery.id
        old_image.caption = f"Main image for {old_image.title}"
        old_image.is_main = True
        old_image.save()

def reverse_migration(apps, schema_editor):
    """
    Reverse the migration - not implemented as it would be destructive
    """
    pass

# Create the migration operations
migration_operations = [
    # First, create the ImageGallery model
    migrations.CreateModel(
        name='ImageGallery',
        fields=[
            ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('title', models.CharField(max_length=200)),
            ('slug', models.SlugField(blank=True, max_length=200, unique=True)),
            ('description', models.TextField(blank=True)),
            ('location', models.CharField(max_length=200)),
            ('photographer', models.CharField(blank=True, max_length=100)),
            ('date_taken', models.DateField(blank=True, null=True)),
            ('is_featured', models.BooleanField(default=False)),
            ('is_active', models.BooleanField(default=True)),
            ('order', models.PositiveIntegerField(default=0)),
            ('created_at', models.DateTimeField(auto_now_add=True)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='image_galleries', to='gallery.gallerycategory')),
            ('destination', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='image_galleries', to='destinations.destination')),
        ],
        options={
            'verbose_name': 'Image Gallery',
            'verbose_name_plural': 'Image Galleries',
            'ordering': ['-is_featured', 'order', '-created_at'],
        },
    ),
    
    # Add the gallery field to GalleryImage (nullable first)
    migrations.AddField(
        model_name='galleryimage',
        name='gallery',
        field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gallery.imagegallery'),
    ),
    
    # Add new fields to GalleryImage
    migrations.AddField(
        model_name='galleryimage',
        name='caption',
        field=models.CharField(blank=True, max_length=300),
    ),
    migrations.AddField(
        model_name='galleryimage',
        name='is_main',
        field=models.BooleanField(default=False, help_text='Main image for the gallery'),
    ),
    
    # Run the data migration
    migrations.RunPython(create_image_galleries_from_existing, reverse_migration),
    
    # Now make the gallery field non-nullable
    migrations.AlterField(
        model_name='galleryimage',
        name='gallery',
        field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gallery.imagegallery'),
    ),
    
    # Remove old fields from GalleryImage that are now in ImageGallery
    migrations.RemoveField(model_name='galleryimage', name='title'),
    migrations.RemoveField(model_name='galleryimage', name='slug'),
    migrations.RemoveField(model_name='galleryimage', name='description'),
    migrations.RemoveField(model_name='galleryimage', name='location'),
    migrations.RemoveField(model_name='galleryimage', name='category'),
    migrations.RemoveField(model_name='galleryimage', name='destination'),
    migrations.RemoveField(model_name='galleryimage', name='photographer'),
    migrations.RemoveField(model_name='galleryimage', name='date_taken'),
    migrations.RemoveField(model_name='galleryimage', name='is_featured'),
    migrations.RemoveField(model_name='galleryimage', name='is_active'),
]

print("Migration operations created. You can now run:")
print("python manage.py makemigrations gallery --empty")
print("Then copy these operations into the migration file.")