from rest_framework import serializers
from .models import GalleryCategory, ImageGallery, GalleryImage, GalleryVideo, GalleryTag

class GalleryCategorySerializer(serializers.ModelSerializer):
    gallery_count = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'gallery_count', 'video_count']
    
    def get_gallery_count(self, obj):
        return obj.image_galleries.filter(is_active=True).count()
    
    def get_video_count(self, obj):
        return obj.videos.filter(is_active=True).count()

class GalleryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryTag
        fields = ['id', 'name', 'slug']

class GalleryImageSerializer(serializers.ModelSerializer):
    """Serializer for individual images within a gallery"""
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'image_url', 'thumbnail_url', 'caption', 'camera_info',
            'is_main', 'order', 'created_at'
        ]
    
    def get_image_url(self, obj):
        return obj.image if obj.image else None
    
    def get_thumbnail_url(self, obj):
        return obj.thumbnail if obj.thumbnail else obj.image

class ImageGallerySerializer(serializers.ModelSerializer):
    """Full serializer for image galleries with all images"""
    category = GalleryCategorySerializer(read_only=True)
    images = GalleryImageSerializer(many=True, read_only=True)
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    image_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ImageGallery
        fields = [
            'id', 'title', 'slug', 'description', 'location', 'category', 
            'destination_name', 'photographer', 'date_taken', 'is_featured', 
            'images', 'main_image_url', 'image_count', 'created_at'
        ]
    
    def get_main_image_url(self, obj):
        main_img = obj.main_image
        return main_img.image if main_img else None

class ImageGalleryListSerializer(serializers.ModelSerializer):
    """Lighter serializer for gallery list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    main_image_url = serializers.SerializerMethodField()
    image_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = ImageGallery
        fields = [
            'id', 'title', 'slug', 'location', 'category_name', 
            'main_image_url', 'image_count', 'is_featured', 'created_at'
        ]
    
    def get_main_image_url(self, obj):
        main_img = obj.main_image
        return main_img.image if main_img else None

class GalleryVideoSerializer(serializers.ModelSerializer):
    category = GalleryCategorySerializer(read_only=True)
    video_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    formatted_views = serializers.CharField(source='get_formatted_views', read_only=True)
    
    class Meta:
        model = GalleryVideo
        fields = [
            'id', 'title', 'slug', 'description', 'video_url', 'thumbnail_url',
            'duration', 'resolution', 'location', 'category', 'destination_name',
            'videographer', 'date_recorded', 'equipment_info', 'views', 
            'formatted_views', 'is_featured', 'tags', 'created_at'
        ]
    
    def get_video_url(self, obj):
        if obj.video_file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.video_file.url)
            return obj.video_file.url
        return None
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            # obj.thumbnail is now a URL string, not a file
            return obj.thumbnail
        return None
    
    def get_tags(self, obj):
        tags = GalleryTag.objects.filter(videotag__video=obj)
        return GalleryTagSerializer(tags, many=True).data



class GalleryVideoListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    formatted_views = serializers.CharField(source='get_formatted_views', read_only=True)
    
    class Meta:
        model = GalleryVideo
        fields = [
            'id', 'title', 'slug', 'thumbnail_url', 'duration',
            'location', 'category_name', 'views', 'formatted_views', 
            'is_featured', 'created_at'
        ]
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            # obj.thumbnail is now a URL string, not a file
            return obj.thumbnail
        return None