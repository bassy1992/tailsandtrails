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

class GalleryImage(models.Model):
    """Gallery images model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/images/%Y/%m/')
    thumbnail = models.ImageField(upload_to='gallery/thumbnails/%Y/%m/', blank=True, null=True)
    
    # Location and categorization
    location = models.CharField(max_length=200)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, related_name='images')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True, related_name='gallery_images')
    
    # Metadata
    photographer = models.CharField(max_length=100, blank=True)
    date_taken = models.DateField(null=True, blank=True)
    camera_info = models.CharField(max_length=200, blank=True)
    
    # Display options
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.location}")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} - {self.location}"

class GalleryVideo(models.Model):
    """Gallery videos model"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    video_file = models.FileField(upload_to='gallery/videos/%Y/%m/')
    thumbnail = models.ImageField(upload_to='gallery/video_thumbnails/%Y/%m/')
    
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