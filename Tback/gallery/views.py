from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import GalleryCategory, ImageGallery, GalleryImage, GalleryVideo
from destinations.models import Destination
from .serializers import (
    GalleryCategorySerializer, ImageGallerySerializer, GalleryImageSerializer, GalleryVideoSerializer,
    ImageGalleryListSerializer, GalleryVideoListSerializer
)

class GalleryCategoryListView(generics.ListAPIView):
    """List all gallery categories"""
    queryset = GalleryCategory.objects.all()
    serializer_class = GalleryCategorySerializer
    permission_classes = [AllowAny]

class ImageGalleryListView(generics.ListAPIView):
    """List image galleries with filtering"""
    serializer_class = ImageGalleryListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_featured', 'destination']
    search_fields = ['title', 'location', 'description', 'photographer']
    ordering_fields = ['created_at', 'title', 'order']
    ordering = ['-is_featured', 'order', '-created_at']
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = ImageGallery.objects.filter(is_active=True)
        
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

class ImageGalleryDetailView(generics.RetrieveAPIView):
    """Get single image gallery with all its images"""
    queryset = ImageGallery.objects.filter(is_active=True)
    serializer_class = ImageGallerySerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class GalleryVideoListView(generics.ListAPIView):
    """List gallery videos with filtering"""
    serializer_class = GalleryVideoListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured', 'destination']
    search_fields = ['title', 'location', 'description', 'videographer']
    ordering_fields = ['created_at', 'title', 'views', 'order']
    ordering = ['-is_featured', 'order', '-created_at']
    permission_classes = [AllowAny]
    
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
    permission_classes = [AllowAny]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def gallery_stats(request):
    """Get gallery statistics"""
    stats = {
        'total_galleries': ImageGallery.objects.filter(is_active=True).count(),
        'total_images': GalleryImage.objects.count(),
        'total_videos': GalleryVideo.objects.filter(is_active=True).count(),
        'featured_galleries': ImageGallery.objects.filter(is_active=True, is_featured=True).count(),
        'featured_videos': GalleryVideo.objects.filter(is_active=True, is_featured=True).count(),
        'categories': GalleryCategory.objects.count(),
        'total_views': sum(GalleryVideo.objects.filter(is_active=True).values_list('views', flat=True)),
    }
    return Response(stats)

@api_view(['GET'])
@permission_classes([AllowAny])
def gallery_mixed_feed(request):
    """Get mixed feed of galleries and videos"""
    category = request.query_params.get('category', 'all')
    featured_only = request.query_params.get('featured', 'false').lower() == 'true'
    limit = int(request.query_params.get('limit', 20))
    
    # Base querysets
    gallery_qs = ImageGallery.objects.filter(is_active=True)
    video_qs = GalleryVideo.objects.filter(is_active=True)
    
    # Apply category filter
    if category != 'all':
        gallery_qs = gallery_qs.filter(
            Q(category__slug=category) | Q(category__name__iexact=category)
        )
        video_qs = video_qs.filter(
            Q(category__slug=category) | Q(category__name__iexact=category)
        )
    
    # Apply featured filter
    if featured_only:
        gallery_qs = gallery_qs.filter(is_featured=True)
        video_qs = video_qs.filter(is_featured=True)
    
    # Get items
    galleries = gallery_qs.order_by('-is_featured', 'order', '-created_at')[:limit//2]
    videos = video_qs.order_by('-is_featured', 'order', '-created_at')[:limit//2]
    
    # Serialize
    gallery_data = ImageGalleryListSerializer(galleries, many=True, context={'request': request}).data
    video_data = GalleryVideoListSerializer(videos, many=True, context={'request': request}).data
    
    # Add type field to distinguish between galleries and videos
    for item in gallery_data:
        item['type'] = 'gallery'
    for item in video_data:
        item['type'] = 'video'
    
    # Combine and sort by featured status and creation date
    combined = list(gallery_data) + list(video_data)
    combined.sort(key=lambda x: (not x.get('is_featured', False), x.get('created_at', '')), reverse=True)
    
    return Response({
        'results': combined[:limit],
        'total_galleries': len(gallery_data),
        'total_videos': len(video_data),
        'category': category
    })

@api_view(['POST'])
@permission_classes([IsAdminUser])
def bulk_add_gallery_images(request):
    """Bulk add multiple images to a gallery via URLs"""
    gallery_title = request.data.get('gallery_title', '')
    image_urls = request.data.get('image_urls', [])
    category_id = request.data.get('category_id')
    location = request.data.get('location', '')
    destination_id = request.data.get('destination_id')
    photographer = request.data.get('photographer', '')
    is_featured = request.data.get('is_featured', False)
    description = request.data.get('description', '')
    
    # Validation
    if not image_urls or not isinstance(image_urls, list):
        return Response(
            {'error': 'image_urls must be a list of URLs'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not category_id:
        return Response(
            {'error': 'category_id is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not location:
        return Response(
            {'error': 'location is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not gallery_title:
        gallery_title = f"{location} Gallery"
    
    # Get category
    try:
        category = GalleryCategory.objects.get(id=category_id)
    except GalleryCategory.DoesNotExist:
        return Response(
            {'error': 'Category not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Get destination if provided
    destination = None
    if destination_id:
        try:
            destination = Destination.objects.get(id=destination_id)
        except Destination.DoesNotExist:
            return Response(
                {'error': 'Destination not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    try:
        # Create the gallery
        gallery = ImageGallery.objects.create(
            title=gallery_title,
            description=description or f"Beautiful images from {location}",
            location=location,
            category=category,
            destination=destination,
            photographer=photographer,
            is_featured=is_featured,
            is_active=True
        )
        
        created_images = []
        errors = []
        
        for i, url in enumerate(image_urls):
            try:
                # Validate URL
                if not url.startswith(('http://', 'https://')):
                    errors.append(f"Invalid URL format: {url}")
                    continue
                
                # Create the image
                image = GalleryImage.objects.create(
                    gallery=gallery,
                    image=url,
                    caption=f"Image {i + 1} from {location}",
                    is_main=i == 0,  # First image is main
                    order=i
                )
                
                created_images.append({
                    'id': image.id,
                    'image': image.image,
                    'caption': image.caption,
                    'is_main': image.is_main,
                    'order': image.order
                })
                
            except Exception as e:
                errors.append(f"Error creating image from {url}: {str(e)}")
        
        response_data = {
            'gallery_id': gallery.id,
            'gallery_title': gallery.title,
            'gallery_slug': gallery.slug,
            'created_count': len(created_images),
            'created_images': created_images,
            'total_images': gallery.images.count()
        }
        
        if errors:
            response_data['errors'] = errors
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error creating gallery: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )