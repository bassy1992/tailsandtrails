#!/usr/bin/env python3
"""
Deploy video models to production
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def deploy_video_models():
    """Deploy video models to production"""
    print("🚀 Deploying video models to production...")
    
    try:
        from django.core.management import execute_from_command_line
        
        # Check current migration status
        print("📋 Checking migration status...")
        execute_from_command_line(['manage.py', 'showmigrations', 'gallery'])
        
        # Apply migrations
        print("\n🔄 Applying migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'gallery'])
        
        print("✅ Migrations applied successfully!")
        
        # Test if we can import and use the model
        from gallery.models import GalleryVideo, GalleryCategory
        
        video_count = GalleryVideo.objects.count()
        print(f"📊 Current video count: {video_count}")
        
        category_count = GalleryCategory.objects.count()
        print(f"📂 Current category count: {category_count}")
        
        if video_count == 0:
            print("\n💡 No videos found. You can add videos through the admin interface.")
            print("   Admin URL: /admin/gallery/galleryvideo/add/")
        
        print("\n🎉 Deployment complete!")
        print("💡 You can now access the admin at: /admin/gallery/galleryvideo/")
        return True
        
    except Exception as e:
        print(f"❌ Deployment error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def add_sample_videos():
    """Add sample videos to the gallery"""
    from gallery.models import GalleryVideo, GalleryCategory
    
    # Get or create categories
    nature_category, _ = GalleryCategory.objects.get_or_create(
        name="Nature & Wildlife",
        defaults={
            'description': "Natural landscapes, wildlife, and outdoor adventures",
            'order': 1
        }
    )
    
    heritage_category, _ = GalleryCategory.objects.get_or_create(
        name="Heritage & Culture",
        defaults={
            'description': "Historical sites, cultural experiences, and traditions",
            'order': 2
        }
    )
    
    adventure_category, _ = GalleryCategory.objects.get_or_create(
        name="Adventure & Activities",
        defaults={
            'description': "Exciting activities and adventure experiences",
            'order': 3
        }
    )
    
    # Sample video data
    video_data = [
        {
            'title': "Volta Region Waterfalls Discovery",
            'description': "Discover the magnificent Wli Waterfalls and other hidden gems in the Volta Region. A perfect blend of nature, hiking, and local culture.",
            'thumbnail': "https://images.pexels.com/photos/33475234/pexels-photo-33475234.jpeg?auto=compress&cs=tinysrgb&w=600",
            'duration': "10:15",
            'location': "Volta Region",
            'category': nature_category,
            'views': 15200,
            'is_featured': True,
            'order': 1
        },
        {
            'title': "Cape Coast Castle - A Journey Through History",
            'description': "Explore the historic Cape Coast Castle and learn about its significance in Ghana's heritage.",
            'thumbnail': "https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=600",
            'duration': "8:45",
            'location': "Cape Coast",
            'category': heritage_category,
            'views': 12500,
            'is_featured': True,
            'order': 2
        },
        {
            'title': "Kakum National Park Canopy Adventure",
            'description': "Experience the breathtaking canopy walk 40 meters above the forest floor.",
            'thumbnail': "https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=600",
            'duration': "6:30",
            'location': "Kakum National Park",
            'category': adventure_category,
            'views': 8900,
            'is_featured': True,
            'order': 3
        }
    ]
    
    created_count = 0
    
    for video_info in video_data:
        # Check if video already exists
        existing_video = GalleryVideo.objects.filter(
            title=video_info['title']
        ).first()
        
        if existing_video:
            print(f"⚠️  Video '{video_info['title']}' already exists")
            continue
        
        # Create the video
        video = GalleryVideo.objects.create(**video_info)
        print(f"✅ Created video: {video.title}")
        created_count += 1
    
    print(f"\n📊 Sample data summary:")
    print(f"   Created: {created_count} videos")
    print(f"   Total videos: {GalleryVideo.objects.count()}")
    print(f"   Featured videos: {GalleryVideo.objects.filter(is_featured=True).count()}")

if __name__ == "__main__":
    deploy_video_models()