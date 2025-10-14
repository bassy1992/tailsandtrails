#!/usr/bin/env python
"""
Add placeholder images to destinations
"""
import os
import sys
import django

# Add the Tback directory to Python path
sys.path.append('Tback')
os.chdir('Tback')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import Destination

def add_placeholder_images():
    """Add placeholder images to destinations"""
    print("🖼️ ADDING PLACEHOLDER IMAGES TO DESTINATIONS")
    print("=" * 60)
    
    # High-quality placeholder images from Unsplash
    placeholder_images = [
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop&crop=center",  # Mountain landscape
        "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop&crop=center",  # Forest path
        "https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=800&h=600&fit=crop&crop=center",  # Beach sunset
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=800&h=600&fit=crop&crop=center",  # Lake and mountains
        "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800&h=600&fit=crop&crop=center",  # Waterfall
        "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop&crop=center",  # Cultural site
    ]
    
    destinations = Destination.objects.all()
    print(f"Found {destinations.count()} destinations")
    
    for i, destination in enumerate(destinations):
        # Use a different placeholder for each destination
        image_url = placeholder_images[i % len(placeholder_images)]
        
        print(f"\n{i+1}. {destination.name}")
        print(f"   Current image: {destination.image}")
        print(f"   New image: {image_url}")
        
        # For now, we'll store the URL in a custom field or use a different approach
        # Since the image field expects a file, let's check if we can modify the serializer instead
        
    print(f"\n💡 Note: The image field expects uploaded files, not URLs.")
    print("We have two options:")
    print("1. Modify the model to use URLField for images")
    print("2. Download and upload actual image files")
    print("3. Use the image_url field in the serializer with placeholder URLs")
    
    # Let's go with option 3 - modify the serializer to return placeholder URLs when no image exists
    print("\n✅ Will modify the serializer to use placeholder images")

if __name__ == '__main__':
    add_placeholder_images()