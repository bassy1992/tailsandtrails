from rest_framework import serializers
from .models import GalleryCategory, GalleryImage, GalleryVideo, GalleryTag

class GalleryCategorySerializer(serializers.ModelSerializer):
    image_count = serializers.SerializerMethodField()
    video_count = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'image_count', 'video_count']
    
    def get_image_count(self, obj):
        return obj.images.filter(is_active=True).count()
    
    def get_video_count(self, obj):
        return obj.videos.filter(is_active=True).count()

class GalleryTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryTag
        fields = ['id', 'name', 'slug']

class GalleryImageSerializer(serializers.ModelSerializer):
    category = GalleryCategorySerializer(read_only=True)
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'slug', 'description', 'image_url', 'thumbnail_url',
            'location', 'category', 'destination_name', 'photographer', 
            'date_taken', 'camera_info', 'is_featured', 'tags', 'created_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            # obj.image is now a URL string, not a file
            return obj.image
        return None
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            # obj.thumbnail is now a URL string, not a file
            return obj.thumbnail
        return self.get_image_url(obj)  # Fallback to main image
    
    def get_tags(self, obj):
        tags = GalleryTag.objects.filter(imagetag__image=obj)
        return GalleryTagSerializer(tags, many=True).data

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

class GalleryImageListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list views"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryImage
        fields = [
            'id', 'title', 'slug', 'image_url', 'thumbnail_url',
            'location', 'category_name', 'is_featured', 'created_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            # obj.image is now a URL string, not a file
            return obj.image
        return None
    
    def get_thumbnail_url(self, obj):
        if obj.thumbnail:
            # obj.thumbnail is now a URL string, not a file
            return obj.thumbnail
        return self.get_image_url(obj)

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