from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryImage, GalleryVideo, GalleryTag, ImageTag, VideoTag

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'image_count', 'video_count']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'

class ImageTagInline(admin.TabularInline):
    model = ImageTag
    extra = 1

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'category', 'is_featured', 'is_active', 'image_preview', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at', 'destination']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title', 'location', 'description', 'photographer']
    prepopulated_fields = {'slug': ('title', 'location')}
    date_hierarchy = 'created_at'
    inlines = [ImageTagInline]
    actions = ['duplicate_images']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'image', 'thumbnail')
        }),
        ('Location & Category', {
            'fields': ('location', 'category', 'destination')
        }),
        ('Metadata', {
            'fields': ('photographer', 'date_taken', 'camera_info'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    def duplicate_images(self, request, queryset):
        """Admin action to duplicate selected images for easy bulk creation"""
        duplicated_count = 0
        for image in queryset:
            # Create a copy with modified title
            new_image = GalleryImage.objects.create(
                title=f"{image.title} (Copy)",
                description=image.description,
                image="",  # Empty image URL to be filled
                location=image.location,
                category=image.category,
                destination=image.destination,
                photographer=image.photographer,
                is_featured=False,  # Copies are not featured
                is_active=False,  # Inactive until image URL is added
                order=image.order + 1000  # Put at end
            )
            duplicated_count += 1
        
        self.message_user(request, f'Successfully duplicated {duplicated_count} images. Please add image URLs to the copies.')
    duplicate_images.short_description = "Duplicate selected images for bulk creation"

class VideoTagInline(admin.TabularInline):
    model = VideoTag
    extra = 1

@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'category', 'duration', 'views', 'is_featured', 'is_active', 'thumbnail_preview', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at', 'destination']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title', 'location', 'description', 'videographer']
    prepopulated_fields = {'slug': ('title', 'location')}
    date_hierarchy = 'created_at'
    inlines = [VideoTagInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'video_file', 'thumbnail')
        }),
        ('Video Details', {
            'fields': ('duration', 'file_size', 'resolution')
        }),
        ('Location & Category', {
            'fields': ('location', 'category', 'destination')
        }),
        ('Metadata', {
            'fields': ('videographer', 'date_recorded', 'equipment_info'),
            'classes': ('collapse',)
        }),
        ('Statistics & Display', {
            'fields': ('views', 'is_featured', 'is_active', 'order')
        }),
    )
    
    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.thumbnail
            )
        return "No thumbnail"
    thumbnail_preview.short_description = 'Thumbnail'

@admin.register(GalleryTag)
class GalleryTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'usage_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def usage_count(self, obj):
        image_count = ImageTag.objects.filter(tag=obj).count()
        video_count = VideoTag.objects.filter(tag=obj).count()
        return f"{image_count + video_count} items"
    usage_count.short_description = 'Usage'