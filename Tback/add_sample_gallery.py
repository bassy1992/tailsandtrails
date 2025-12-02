#!/usr/bin/env python
"""
Script to add sample gallery images and videos to the database
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tback_api.settings')
django.setup()

from destinations.models import GalleryCategory, GalleryImage, GalleryVideo

def create_sample_gallery():
    print("Creating sample gallery data...")
    
    # Create categories
    categories_data = [
        {
            'name': 'Heritage',
            'slug': 'heritage',
            'description': 'Historic sites and cultural landmarks',
            'order': 1
        },
        {
            'name': 'Nature',
            'slug': 'nature',
            'description': 'Natural landscapes and wildlife',
            'order': 2
        },
        {
            'name': 'Culture',
            'slug': 'culture',
            'description': 'Local culture and traditions',
            'order': 3
        },
        {
            'name': 'Adventure',
            'slug': 'adventure',
            'description': 'Exciting outdoor activities',
            'order': 4
        },
        {
            'name': 'Coastal',
            'slug': 'coastal',
            'description': 'Beaches and coastal areas',
            'order': 5
        },
        {
            'name': 'Urban',
            'slug': 'urban',
            'description': 'City life and modern Ghana',
            'order': 6
        }
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = GalleryCategory.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        categories[cat_data['slug']] = category
        print(f"{'Created' if created else 'Found'} category: {category.name}")
    
    # Create sample images
    images_data = [
        {
            'title': 'Cape Coast Castle',
            'description': 'Historic architecture of the UNESCO World Heritage Site',
            'image_url': 'https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['heritage'],
            'location': 'Cape Coast',
            'is_featured': True,
            'order': 1
        },
        {
            'title': 'Aburi Botanical Gardens',
            'description': 'Lush gardens with stunning mountain views',
            'image_url': 'https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/27116488/pexels-photo-27116488.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['nature'],
            'location': 'Aburi',
            'is_featured': True,
            'order': 2
        },
        {
            'title': 'Kumasi Street Life',
            'description': 'Vibrant street culture and local fashion',
            'image_url': 'https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['culture'],
            'location': 'Kumasi',
            'order': 3
        },
        {
            'title': 'Forest Canopy Walk',
            'description': 'Thrilling canopy walk through pristine rainforest',
            'image_url': 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['adventure'],
            'location': 'Kakum National Park',
            'is_featured': True,
            'order': 4
        },
        {
            'title': 'Accra Coastline',
            'description': 'Beautiful sandy beaches with traditional fishing boats',
            'image_url': 'https://images.pexels.com/photos/30211750/pexels-photo-30211750.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/30211750/pexels-photo-30211750.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['coastal'],
            'location': 'Accra',
            'order': 5
        },
        {
            'title': 'Street Vendors',
            'description': 'Local entrepreneurs and vibrant street life',
            'image_url': 'https://images.pexels.com/photos/15887695/pexels-photo-15887695.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/15887695/pexels-photo-15887695.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['culture'],
            'location': 'Accra',
            'order': 6
        },
        {
            'title': 'Coastal Fort',
            'description': 'Historic coastal fortifications and serene beaches',
            'image_url': 'https://images.pexels.com/photos/5110556/pexels-photo-5110556.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/5110556/pexels-photo-5110556.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['heritage'],
            'location': 'Ghana Coast',
            'order': 7
        },
        {
            'title': 'Traditional Architecture',
            'description': 'Ancient mosque with distinctive Sudano-Sahelian architecture',
            'image_url': 'https://images.pexels.com/photos/32981288/pexels-photo-32981288.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/32981288/pexels-photo-32981288.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['heritage'],
            'location': 'Northern Ghana',
            'order': 8
        },
        {
            'title': 'Volta River',
            'description': 'Peaceful river journey through lush landscapes',
            'image_url': 'https://images.pexels.com/photos/12190172/pexels-photo-12190172.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/12190172/pexels-photo-12190172.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['nature'],
            'location': 'Volta Region',
            'order': 9
        },
        {
            'title': 'Modern Accra',
            'description': 'Contemporary architecture and urban development',
            'image_url': 'https://images.pexels.com/photos/1422408/pexels-photo-1422408.jpeg?auto=compress&cs=tinysrgb&w=1200',
            'thumbnail_url': 'https://images.pexels.com/photos/1422408/pexels-photo-1422408.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['urban'],
            'location': 'Accra',
            'order': 10
        }
    ]
    
    for img_data in images_data:
        image, created = GalleryImage.objects.get_or_create(
            title=img_data['title'],
            defaults=img_data
        )
        print(f"{'Created' if created else 'Found'} image: {image.title}")
    
    # Create sample videos
    videos_data = [
        {
            'title': 'Cape Coast Castle - A Journey Through History',
            'description': 'Explore the historic Cape Coast Castle and learn about its significance in Ghana\'s heritage.',
            'video_url': 'https://videos.pexels.com/video-files/29603787/12740641_640_360_60fps.mp4',
            'thumbnail_url': 'https://images.pexels.com/photos/16136199/pexels-photo-16136199.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['heritage'],
            'duration': '8:45',
            'is_featured': True,
            'order': 1
        },
        {
            'title': 'Kakum National Park Canopy Adventure',
            'description': 'Experience the breathtaking canopy walk 40 meters above the forest floor.',
            'video_url': 'https://videos.pexels.com/video-files/17844988/17844988-sd_240_426_30fps.mp4',
            'thumbnail_url': 'https://images.pexels.com/photos/33008767/pexels-photo-33008767.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['adventure'],
            'duration': '6:30',
            'is_featured': True,
            'order': 2
        },
        {
            'title': 'Volta Region Waterfalls Discovery',
            'description': 'Discover the magnificent Wli Waterfalls and other hidden gems in the Volta Region.',
            'video_url': 'https://videos.pexels.com/video-files/31934467/13602616_360_640_25fps.mp4',
            'thumbnail_url': 'https://images.pexels.com/photos/33475234/pexels-photo-33475234.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['nature'],
            'duration': '10:15',
            'order': 3
        },
        {
            'title': 'Ashanti Culture & Traditions',
            'description': 'Immerse yourself in the rich Ashanti culture and traditional ceremonies.',
            'video_url': 'https://videos.pexels.com/video-files/7823374/7823374-hd_720_1280_60fps.mp4',
            'thumbnail_url': 'https://images.pexels.com/photos/33033556/pexels-photo-33033556.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['culture'],
            'duration': '12:20',
            'order': 4
        },
        {
            'title': 'Ghana\'s Golden Beaches',
            'description': 'Relax on Ghana\'s pristine beaches along the Atlantic coast.',
            'video_url': 'https://videos.pexels.com/video-files/19019788/19019788-sd_240_426_30fps.mp4',
            'thumbnail_url': 'https://images.pexels.com/photos/30211750/pexels-photo-30211750.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['coastal'],
            'duration': '7:55',
            'order': 5
        },
        {
            'title': 'Accra City Life & Modern Ghana',
            'description': 'Experience the vibrant capital city of Accra where tradition meets modernity.',
            'video_url': 'https://videos.pexels.com/video-files/32156428/13711037_360_640_50fps.mp4',
            'thumbnail_url': 'https://images.pexels.com/photos/1422408/pexels-photo-1422408.jpeg?auto=compress&cs=tinysrgb&w=600',
            'category': categories['urban'],
            'duration': '9:10',
            'order': 6
        }
    ]
    
    for vid_data in videos_data:
        video, created = GalleryVideo.objects.get_or_create(
            title=vid_data['title'],
            defaults=vid_data
        )
        print(f"{'Created' if created else 'Found'} video: {video.title}")
    
    print("\n✅ Sample gallery data created successfully!")
    print(f"Categories: {GalleryCategory.objects.count()}")
    print(f"Images: {GalleryImage.objects.count()}")
    print(f"Videos: {GalleryVideo.objects.count()}")

if __name__ == '__main__':
    create_sample_gallery()
