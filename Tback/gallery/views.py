from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import GalleryCategory, GalleryImage, GalleryVideo
from .serializers import (
    GalleryCategorySerializer, GalleryImageSerializer, GalleryVideoSerializer,
    GalleryImageListSerializer, GalleryVideoListSerializer
)

class GalleryCategoryListView(generics.ListAPIView):
    """List all gallery categories"""
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer

class GalleryImageListView(generics.ListAPIView):
    """List gallery images with filtering"""
    serializer_class = GalleryImageListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'destination']
    search_fields = ['title', 'location', 'description', 'photographer']
    ordering_fields = ['created_at', 'title', 'order']
    ordering = ['-is_featured', 'order', '-created_at']
    
    def get_queryset(self):
        queryset = GalleryImage.objects.filter(is_active=True)
        
        # Filter by category slug or name
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(
                Q(category__slug=category) | Q(category__name__iexact=category)
            )
        
        # Filter featured only
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset

class GalleryImageDetailView(generics.RetrieveAPIView):
    """Get single gallery image details"""
    queryset = GalleryImage.objects.filter(is_active=True)
    serializer_class = GalleryImageSerializer
    lookup_field = 'slug'

class GalleryVideoListView(generics.ListAPIView):
    """List gallery videos with filtering"""
    serializer_class = GalleryVideoListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'destination']
    search_fields = ['title', 'location', 'description', 'videographer']
    ordering_fields = ['created_at', 'title', 'views', 'order']
    ordering = ['-is_featured', 'order', '-created_at']
    
    def get_queryset(self):
        queryset = GalleryVideo.objects.filter(is_active=True)
        
        # Filter by category slug or name
        category = self.request.query_params.get('category')
        if category and category != 'all':
            queryset = queryset.filter(
                Q(category__slug=category) | Q(category__name__iexact=category)
            )
        
        # Filter featured only
        featured = self.request.query_params.get('featured')
        if featured and featured.lower() == 'true':
            queryset = queryset.filter(is_featured=True)
        
        return queryset

class GalleryVideoDetailView(generics.RetrieveAPIView):
    """Get single gallery video details and increment view count"""
    queryset = GalleryVideo.objects.filter(is_active=True)
    serializer_class = GalleryVideoSerializer
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@api_view(['GET'])
def gallery_stats(request):
    """Get gallery statistics"""
    stats = {
        'total_images': GalleryImage.objects.filter(is_active=True).count(),
        'total_videos': GalleryVideo.objects.filter(is_active=True).count(),
        'featured_images': GalleryImage.objects.filter(is_active=True, is_featured=True).count(),
        'featured_videos': GalleryVideo.objects.filter(is_active=True, is_featured=True).count(),
        'categories': GalleryCategory.objects.count(),
        'total_views': sum(GalleryVideo.objects.filter(is_active=True).values_list('views', flat=True)),
    }
    return Response(stats)

@api_view(['GET'])
def gallery_mixed_feed(request):
    """Get mixed feed of images and videos"""
    category = request.query_params.get('category', 'all')
    featured_only = request.query_params.get('featured', 'false').lower() == 'true'
    limit = int(request.query_params.get('limit', 20))
    
    # Base querysets
    image_qs = GalleryImage.objects.filter(is_active=True)
    video_qs = GalleryVideo.objects.filter(is_active=True)
    
    # Apply category filter
    if category != 'all':
        image_qs = image_qs.filter(
            Q(category__slug=category) | Q(category__name__iexact=category)
        )
        video_qs = video_qs.filter(
            Q(category__slug=category) | Q(category__name__iexact=category)
        )
    
    # Apply featured filter
    if featured_only:
        image_qs = image_qs.filter(is_featured=True)
        video_qs = video_qs.filter(is_featured=True)
    
    # Get items
    images = image_qs.order_by('-is_featured', 'order', '-created_at')[:limit//2]
    videos = video_qs.order_by('-is_featured', 'order', '-created_at')[:limit//2]
    
    # Serialize
    image_data = GalleryImageListSerializer(images, many=True, context={'request': request}).data
    video_data = GalleryVideoListSerializer(videos, many=True, context={'request': request}).data
    
    # Add type field to distinguish between images and videos
    for item in image_data:
        item['type'] = 'image'
    for item in video_data:
        item['type'] = 'video'
    
    # Combine and sort by featured status and creation date
    combined = list(image_data) + list(video_data)
    combined.sort(key=lambda x: (not x.get('is_featured', False), x.get('created_at', '')), reverse=True)
    
    return Response({
        'results': combined[:limit],
        'total_images': len(image_data),
        'total_videos': len(video_data),
        'category': category
    })