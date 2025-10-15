from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import GalleryCategory, ImageGallery, GalleryImage, GalleryVideo, GalleryTag, ImageTag, VideoTag
from .admin_helpers import MultiImageUploadMixin, add_bulk_upload_button

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'gallery_count', 'video_count']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    
    def gallery_count(self, obj):
        return obj.image_galleries.count()
    gallery_count.short_description = 'Image Galleries'
    
    def video_count(self, obj):
        return obj.videos.count()
    video_count.short_description = 'Videos'

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 3
    fields = ['image', 'thumbnail', 'caption', 'is_main', 'order']
    
    def get_extra(self, request, obj=None, **kwargs):
        # Show 3 empty forms for new galleries, 1 for existing
        return 3 if obj is None else 1

@admin.register(ImageGallery)
class ImageGalleryAdmin(MultiImageUploadMixin, admin.ModelAdmin):
    list_display = ['title', 'location', 'category', 'image_count', 'is_featured', 'is_active', 'main_image_preview', 'created_at']
    list_filter = ['category', 'is_featured', 'is_active', 'created_at', 'destination']
    list_editable = ['is_featured', 'is_active']
    search_fields = ['title', 'location', 'description', 'photographer']
    prepopulated_fields = {'slug': ('title', 'location')}
    date_hierarchy = 'created_at'
    inlines = [GalleryImageInline]
    actions = ['duplicate_galleries', add_bulk_upload_button]
    
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_upload_url'] = reverse('admin:gallery_bulk_upload')
        return super().changelist_view(request, extra_context)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description')
        }),
        ('Location & Category', {
            'fields': ('location', 'category', 'destination')
        }),
        ('Metadata', {
            'fields': ('photographer', 'date_taken'),
            'classes': ('collapse',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_active', 'order')
        }),
    )
    
    def main_image_preview(self, obj):
        main_img = obj.main_image
        if main_img and main_img.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                main_img.image
            )
        return "No images"
    main_image_preview.short_description = 'Preview'
    
    def duplicate_galleries(self, request, queryset):
        """Admin action to duplicate selected galleries"""
        duplicated_count = 0
        for gallery in queryset:
            # Create a copy with modified title
            new_gallery = ImageGallery.objects.create(
                title=f"{gallery.title} (Copy)",
                description=gallery.description,
                location=gallery.location,
                category=gallery.category,
                destination=gallery.destination,
                photographer=gallery.photographer,
                is_featured=False,
                is_active=False,
                order=gallery.order + 1000
            )
            duplicated_count += 1
        
        self.message_user(request, f'Successfully duplicated {duplicated_count} galleries. Please add images to the copies.')
    duplicate_galleries.short_description = "Duplicate selected galleries"

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'caption', 'is_main', 'order', 'image_preview', 'created_at']
    list_filter = ['is_main', 'created_at', 'gallery__category']
    list_editable = ['is_main', 'order']
    search_fields = ['gallery__title', 'caption', 'camera_info']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image
            )
        return "No image"
    image_preview.short_description = 'Preview'

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