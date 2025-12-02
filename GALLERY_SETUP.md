# Gallery Feature Setup

## Overview
The gallery feature allows you to display images and videos from the database on the frontend. Gallery items can be organized by categories and marked as featured.

## Backend Setup

### Models
The gallery uses three main models in `Tback/destinations/models.py`:
- `GalleryCategory` - Categories for organizing gallery items
- `GalleryImage` - Gallery images with metadata
- `GalleryVideo` - Gallery videos with metadata

### API Endpoints
Available at `/api/gallery/`:
- `GET /api/gallery/categories/` - List all gallery categories
- `GET /api/gallery/images/` - List all images (supports filtering)
  - Query params: `category` (slug), `featured` (true/false)
- `GET /api/gallery/videos/` - List all videos (supports filtering)
  - Query params: `category` (slug), `featured` (true/false)

### Admin Interface
Gallery items can be managed through Django admin:
- Navigate to `/admin/destinations/gallerycategory/`
- Navigate to `/admin/destinations/galleryimage/`
- Navigate to `/admin/destinations/galleryvideo/`

## Frontend Integration

### API Client
Gallery API functions are available in `Tfront/client/lib/api.ts`:
```typescript
import { galleryApi } from '@/lib/api';

// Get all categories
const categories = await galleryApi.getCategories();

// Get all images
const images = await galleryApi.getImages();

// Get featured images only
const featuredImages = await galleryApi.getImages({ featured: true });

// Get images by category
const heritageImages = await galleryApi.getImages({ category: 'heritage' });

// Get videos
const videos = await galleryApi.getVideos();
```

### Gallery Page
The gallery page is located at `Tfront/client/pages/Gallery.tsx` and includes:
- Category filtering
- Tabs for photos and videos
- Image lightbox view
- Video player with support for YouTube, Vimeo, and direct video URLs
- Featured item badges
- Loading states and error handling

## Adding Sample Data

Run the sample data script to populate the gallery:
```bash
cd Tback
python add_sample_gallery.py
```

This creates:
- 6 gallery categories (Heritage, Nature, Culture, Adventure, Coastal, Urban)
- 10 sample images
- 6 sample videos

## Adding Your Own Content

### Via Django Admin
1. Go to `/admin/destinations/galleryimage/add/`
2. Fill in the form:
   - Title: Name of the image
   - Description: Brief description
   - Image URL: Full URL to the image
   - Thumbnail URL: Optional smaller version for listings
   - Category: Select from available categories
   - Location: Where the photo was taken
   - Photographer: Optional credit
   - Is Featured: Check to highlight this image
   - Order: Lower numbers appear first

### Via Python Script
```python
from destinations.models import GalleryCategory, GalleryImage

category = GalleryCategory.objects.get(slug='heritage')

GalleryImage.objects.create(
    title='My Image',
    description='Description here',
    image_url='https://example.com/image.jpg',
    thumbnail_url='https://example.com/thumb.jpg',
    category=category,
    location='Accra',
    is_featured=True
)
```

## Video URL Formats

The gallery supports multiple video formats:
- **Direct video files**: `https://example.com/video.mp4`
- **YouTube**: Embed URL format `https://www.youtube.com/embed/VIDEO_ID`
- **Vimeo**: Embed URL format `https://player.vimeo.com/video/VIDEO_ID`

## Features

- ✅ Category-based filtering
- ✅ Featured items highlighting
- ✅ Image lightbox with full details
- ✅ Video player with multiple format support
- ✅ Responsive grid layout
- ✅ Loading states
- ✅ Error handling
- ✅ SEO-friendly metadata
- ✅ Admin interface for content management

## Next Steps

1. Add more gallery content through the admin interface
2. Customize categories to match your needs
3. Update image/video URLs to use your own media
4. Consider adding image upload functionality (requires media storage setup)
