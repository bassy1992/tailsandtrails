#!/usr/bin/env python3
"""
Simple script to set up gallery videos on production
Run this on Railway after deployment
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def main():
    """Main setup function"""
    print("🎬 Setting up Gallery Videos...")
    
    try:
        # Import after Django setup
        from gallery.models import GalleryVideo, GalleryCategory
        
        # Test database connection
        print("📊 Testing database connection...")
        try:
            video_count = GalleryVideo.objects.count()
            print(f"✅ Database connected. Current videos: {video_count}")
        except Exception as e:
            print(f"❌ Database connection failed: {str(e)}")
            if "does not exist" in str(e):
                print("💡 The video table doesn't exist. Migration needed.")
                print("   Run: python manage.py migrate gallery")
            return False
        
        # Check categories
        category_count = GalleryCategory.objects.count()
        print(f"📂 Categories available: {category_count}")
        
        if category_count == 0:
            print("⚠️  No categories found. Creating default categories...")
            create_default_categories()
        
        if video_count == 0:
            print("📹 No videos found. Creating sample videos...")
            create_sample_videos()
        else:
            print("✅ Videos already exist in database")
        
        print("\n🎉 Setup complete!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("💡 Make sure all migrations are applied: python manage.py migrate")
        return False
    except Exception as e:
        print(f"❌ Setup error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_default_categories():
    """Create default gallery categories"""
    from gallery.models import GalleryCategory
    
    categories = [
        {
            'name': "Nature & Wildlife",
            'description': "Natural landscapes, wildlife, and outdoor adventures",
            'order': 1
        },
        {
            'name': "Heritage & Culture", 
            'description': "Historical sites, cultural experiences, and traditions",
            'order': 2
        },
        {
            'name': "Adventure & Activities",
            'description': "Exciting activities and adventure experiences", 
            'order': 3
        }
    ]
    
    for cat_data in categories:
        category, created = GalleryCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"⚠️  Category already exists: {category.name}")

def create_sample_videos():
    """Create sample videos"""
    from gallery.models import GalleryVideo, GalleryCategory
    
    # Get categories
    nature_cat = GalleryCategory.objects.filter(name="Nature & Wildlife").first()
    heritage_cat = GalleryCategory.objects.filter(name="Heritage & Culture").first()
    adventure_cat = GalleryCategory.objects.filter(name="Adventure & Activities").first()
    
    if not all([nature_cat, heritage_cat, adventure_cat]):
        print("❌ Categories not found. Creating them first...")
        create_default_categories()
        nature_cat = GalleryCategory.objects.get(name="Nature & Wildlife")
        heritage_cat = GalleryCategory.objects.get(name="Heritage & Culture")
        adventure_cat = GalleryCategory.objects.get(name="Adventure & Activities")
    
    videos = [
        {
            'title': "Volta Region Waterfalls Discovery",
            'description': "Discover the magnificent Wli Waterfalls and other hidden gems in the Volta Region.",
            'thumbnail': "https://images.pexels.com/photos/33475234/pexels-photo-33475234.jpeg?auto=compress&cs=tinysrgb&w=600",
            'duration': "10:15",
            'location': "Volta Region",
            'category': nature_cat,
            'views': 15200,
            'is_featured': True,
            'order': 1
        },
        {
            'title': "Cape Coast Castle - A Journey Through History",
            'description': "Explore the historic Cape Coast Castle and learn about Ghana's heritage.",
            'thumbnail': "https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=600",
            'duration': "8:45",
            'location': "Cape Coast",
            'category': heritage_cat,
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
            'category': adventure_cat,
            'views': 8900,
            'is_featured': True,
            'order': 3
        }
    ]
    
    created_count = 0
    for video_data in videos:
        video, created = GalleryVideo.objects.get_or_create(
            title=video_data['title'],
            defaults=video_data
        )
        if created:
            print(f"✅ Created video: {video.title}")
            created_count += 1
        else:
            print(f"⚠️  Video already exists: {video.title}")
    
    print(f"\n📊 Summary:")
    print(f"   Created: {created_count} videos")
    print(f"   Total videos: {GalleryVideo.objects.count()}")
    print(f"   Featured videos: {GalleryVideo.objects.filter(is_featured=True).count()}")

if __name__ == "__main__":
    main()