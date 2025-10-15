# Video URL Upload Guide

## 🎬 How to Add Videos Using URLs

You can now add videos to the gallery using external URLs instead of uploading files. This is perfect for using videos from Pexels, Vimeo, or direct video links.

### ✅ Supported Video Sources

1. **Direct Video URLs**:
   - `.mp4` files: `https://example.com/video.mp4`
   - `.webm` files: `https://example.com/video.webm`
   - `.ogg` files: `https://example.com/video.ogg`
   - `.mov` files: `https://example.com/video.mov`

2. **Pexels Videos** (Recommended):
   - `https://videos.pexels.com/video-files/...`
   - Free, high-quality videos
   - No attribution required

3. **Other Platforms**:
   - Vimeo player URLs
   - YouTube URLs (for embedding)

### 📝 How to Add a Video with URL

1. **Go to Admin**: `/admin/gallery/galleryvideo/add/`

2. **Fill in Basic Info**:
   - Title: "Amazing Ghana Sunset"
   - Description: "Beautiful sunset over Accra"
   - Location: "Accra"
   - Category: Select appropriate category

3. **Add Video Source** (Choose ONE):
   - **Option A**: Upload a video file
   - **Option B**: Enter a video URL

4. **Add Thumbnail**: 
   - Always required
   - Use image URL: `https://images.pexels.com/photos/...`

5. **Set Duration**: 
   - Format: `MM:SS` or `HH:MM:SS`
   - Example: `2:30` or `1:15:30`

### 🔗 Finding Video URLs

#### From Pexels:
1. Go to [pexels.com/videos](https://pexels.com/videos)
2. Find a video you like
3. Click "Download" → "Original"
4. Copy the download URL
5. Use this URL in the "Video URL" field

#### Example Pexels URLs:
```
https://videos.pexels.com/video-files/31934467/13602616_360_640_25fps.mp4
https://videos.pexels.com/video-files/29603787/12740641_640_360_60fps.mp4
```

### ⚠️ Important Notes

- **One Source Only**: Use either file upload OR URL, not both
- **Thumbnail Required**: Always provide a thumbnail image URL
- **Duration Format**: Use `MM:SS` format (e.g., `2:30`, `10:15`)
- **URL Validation**: The system will validate video URLs automatically

### 🎯 Best Practices

1. **Use Pexels**: Free, high-quality videos with no attribution required
2. **Consistent Thumbnails**: Use high-quality thumbnail images
3. **Accurate Duration**: Always specify the correct video duration
4. **Descriptive Titles**: Use clear, descriptive titles for better SEO
5. **Proper Categories**: Assign videos to appropriate categories

### 🚀 Admin Features

- **Visual Indicators**: See if video uses URL (🔗) or file (📁)
- **Form Validation**: Automatic validation of video URLs
- **Smart Fields**: Fields hide/show based on your selection
- **URL Suggestions**: Helpful placeholders and validation

### 📊 Current Videos

All existing videos now use URLs from Pexels:
- Volta Region Waterfalls Discovery
- Cape Coast Castle - A Journey Through History  
- Kakum National Park Canopy Adventure

### 🔧 Technical Details

The system automatically:
- Validates video URL formats
- Handles both file and URL sources in the API
- Serves the correct video URL to the frontend
- Maintains backward compatibility with uploaded files

Enjoy using video URLs for easier video management! 🎉