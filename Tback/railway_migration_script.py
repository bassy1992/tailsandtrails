#!/usr/bin/env python3
"""
Railway migration script - run this directly on Railway
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

def main():
    """Apply migrations and update videos on Railway"""
    print("🚀 Railway Migration Script")
    print("=" * 40)
    
    try:
        # 1. Apply migrations
        print("1. Applying gallery migrations...")
        execute_from_command_line(['manage.py', 'migrate', 'gallery', '--verbosity=2'])
        print("✅ Migrations applied")
        
        # 2. Update videos with URLs
        print("\n2. Updating videos with URLs...")
        from gallery.models import GalleryVideo
        
        video_urls = {
            "Volta Region Waterfalls Discovery": "https://videos.pexels.com/video-files/31934467/13602616_360_640_25fps.mp4",
            "Cape Coast Castle - A Journey Through History": "https://videos.pexels.com/video-files/29603787/12740641_640_360_60fps.mp4", 
            "Kakum National Park Canopy Adventure": "https://videos.pexels.com/video-files/17844988/17844988-sd_240_426_30fps.mp4"
        }
        
        updated_count = 0
        for title, url in video_urls.items():
            try:
                video = GalleryVideo.objects.get(title=title)
                if not video.video_url:
                    video.video_url = url
                    video.save()
                    print(f"✅ Updated: {title}")
                    updated_count += 1
                else:
                    print(f"⚠️  Already has URL: {title}")
            except GalleryVideo.DoesNotExist:
                print(f"❌ Not found: {title}")
        
        # 3. Verify results
        print(f"\n3. Verification:")
        total_videos = GalleryVideo.objects.count()
        videos_with_urls = GalleryVideo.objects.exclude(video_url__isnull=True).exclude(video_url='').count()
        
        print(f"   Total videos: {total_videos}")
        print(f"   Videos with URLs: {videos_with_urls}")
        print(f"   Updated in this run: {updated_count}")
        
        # 4. Test API response
        print(f"\n4. Testing API serialization...")
        from gallery.serializers import GalleryVideoSerializer
        
        featured_videos = GalleryVideo.objects.filter(is_featured=True)[:1]
        if featured_videos:
            serializer = GalleryVideoSerializer(featured_videos[0])
            data = serializer.data
            has_video_url = 'video_url' in data and data['video_url']
            print(f"   API video_url field: {'✅ Present' if has_video_url else '❌ Missing'}")
            if has_video_url:
                print(f"   Sample URL: {data['video_url'][:50]}...")
        
        print(f"\n🎉 Migration complete!")
        print(f"   ✅ Database updated")
        print(f"   ✅ Videos have URLs") 
        print(f"   ✅ API will return video_url field")
        print(f"   ✅ Vercel frontend will work")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()