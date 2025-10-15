from django.db import models
from django.utils.text import slugify
from destinations.models import Destination

class GalleryCategory(models.Model):
    """Categories for gallery items"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Gallery Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class ImageGallery(models.Model):
    """Main gallery item that can contain multiple images"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Location and categorization
    location = models.CharField(max_length=200)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='image_galleries')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='image_galleries')
    
    # Metadata
    photographer = models.CharField(max_length=100, blank=True)
    date_taken = models.DateField(null=True, blank=True)
    
    # Display options
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = "Image Gallery"
        verbose_name_plural = "Image Galleries"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.location}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.location}"
    
    @property
    def main_image(self):
        """Get the first/main image for this gallery"""
        return self.images.filter(is_main=True).first() or self.images.first()
    
    @property
    def image_count(self):
        """Get total number of images in this gallery"""
        return self.images.count()

class GalleryImage(models.Model):
    """Individual images within a gallery"""
    gallery = models.ForeignKey(ImageGallery, on_delete=models.CASCADE, related_name='images')
    image = models.URLField(max_length=500, help_text="Image URL")
    thumbnail = models.URLField(max_length=500, blank=True, null=True, help_text="Thumbnail URL")
    caption = models.CharField(max_length=300, blank=True)
    
    # Image specific metadata
    camera_info = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False, help_text="Main image for the gallery")
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_main', 'order', 'created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
    
    def save(self, *args, **kwargs):
        # Ensure only one main image per gallery
        if self.is_main:
            GalleryImage.objects.filter(gallery=self.gallery, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.gallery.title} - Image {self.order}"

class GalleryVideo(models.Model):
    """Gallery videos model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='gallery/videos/%Y/%m/', null=True, blank=True, help_text="Upload video file (optional if using video URL)")
    video_url = models.URLField(max_length=500, null=True, blank=True, help_text="External video URL (MP4, WebM, etc.) - alternative to file upload")
    thumbnail = models.URLField(max_length=500, help_text="Video thumbnail URL")
    
    # Video metadata
    duration = models.CharField(max_length=10, help_text="Format: MM:SS or HH:MM:SS")
    file_size = models.PositiveIntegerField(help_text="File size in bytes", null=True, blank=True)
    resolution = models.CharField(max_length=20, blank=True, help_text="e.g., 1920x1080")
    
    # Location and categorization
    location = models.CharField(max_length=200)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='videos')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_videos')
    
    # Metadata
    videographer = models.CharField(max_length=100, blank=True)
    date_recorded = models.DateField(null=True, blank=True)
    equipment_info = models.CharField(max_length=200, blank=True)
    
    # Statistics
    views = models.PositiveIntegerField(default=0)
    
    # Display options
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = "Gallery Video"
        verbose_name_plural = "Gallery Videos"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.location}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.location}"
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_formatted_views(self):
        """Return formatted view count (e.g., 1.2K, 15.3K)"""
        if self.views >= 1000:
            return f"{self.views / 1000:.1f}K"
        return str(self.views)
    
    def get_video_url(self):
        """Get video URL - either from uploaded file or external URL"""
        if self.video_url:
            return self.video_url
        elif self.video_file:
            return self.video_file.url
        return None
    
    def clean(self):
        """Validate that either video_file or video_url is provided"""
        from django.core.exceptions import ValidationError
        if not self.video_file and not self.video_url:
            raise ValidationError("Either upload a video file or provide a video URL.")
        if self.video_file and self.video_url:
            raise ValidationError("Please provide either a video file OR a video URL, not both.")
    
    @property
    def video_source_type(self):
        """Return the type of video source"""
        if self.video_url:
            return "url"
        elif self.video_file:
            return "file"
        return "none"

class GalleryTag(models.Model):
    """Tags for gallery items"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Many-to-many relationships for tags
class ImageTag(models.Model):
    image = models.ForeignKey(GalleryImage, on_delete=models.CASCADE)
    tag = models.ForeignKey(GalleryTag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('image', 'tag')

class VideoTag(models.Model):
    video = models.ForeignKey(GalleryVideo, on_delete=models.CASCADE)
    tag = models.ForeignKey(GalleryTag, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('video', 'tag')