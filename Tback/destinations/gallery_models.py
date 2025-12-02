"""
Gallery models for standalone gallery images and videos
"""
from django.db import models


class GalleryCategory(models.Model):
    """Categories for organizing gallery items"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Gallery Categories'
    
    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """Standalone gallery images"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    category = models.ForeignKey(
        GalleryCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='images'
    )
    location = models.CharField(max_length=200, blank=True)
    photographer = models.CharField(max_length=100, blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
    
    def __str__(self):
        return self.title


class GalleryVideo(models.Model):
    """Gallery videos"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    video_url = models.URLField(max_length=500, help_text="YouTube, Vimeo, or direct video URL")
    thumbnail_url = models.URLField(max_length=500, blank=True)
    category = models.ForeignKey(
        GalleryCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='videos'
    )
    duration = models.CharField(max_length=20, blank=True, help_text="e.g., 2:30")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']
        verbose_name = 'Gallery Video'
        verbose_name_plural = 'Gallery Videos'
    
    def __str__(self):
        return self.title
