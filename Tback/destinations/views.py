from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Destination, Review, Booking, GalleryCategory, GalleryImage, GalleryVideo
from .serializers import (
    CategorySerializer, DestinationListSerializer, DestinationDetailSerializer,
    ReviewSerializer, BookingSerializer, GalleryCategorySerializer, 
    GalleryImageSerializer, GalleryVideoSerializer
)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

class DestinationListView(generics.ListAPIView):
    serializer_class = DestinationListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'duration', 'is_featured']
    search_fields = ['name', 'location', 'description', 'category__name']
    ordering_fields = ['price', 'rating', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Destination.objects.filter(is_active=True).select_related('category').prefetch_related('highlights', 'includes')
        
        # Custom price filtering
        price_filter = self.request.query_params.get('price_category', None)
        if price_filter == 'budget':
            queryset = queryset.filter(price__lt=300)
        elif price_filter == 'mid':
            queryset = queryset.filter(price__gte=300, price__lte=600)
        elif price_filter == 'luxury':
            queryset = queryset.filter(price__gt=600)
        
        # Custom duration filtering
        duration_filter = self.request.query_params.get('duration_category', None)
        if duration_filter == 'day':
            queryset = queryset.filter(duration='1_day')
        elif duration_filter == 'weekend':
            queryset = queryset.filter(duration__in=['2_days', '3_days'])
        elif duration_filter == 'week':
            queryset = queryset.filter(duration__in=['4_days', '5_days', '6_days', '7_days', '7_plus_days'])
        
        return queryset

class DestinationDetailView(generics.RetrieveAPIView):
    queryset = Destination.objects.filter(is_active=True).select_related('category').prefetch_related('highlights', 'includes', 'images')
    serializer_class = DestinationDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'

class DestinationReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        destination_id = self.kwargs['destination_id']
        return Review.objects.filter(
            destination_id=destination_id,
            is_active=True
        ).select_related('user').order_by('-created_at')

@api_view(['GET'])
@permission_classes([AllowAny])
def destination_stats(request):
    """Get general statistics about destinations"""
    total_destinations = Destination.objects.filter(is_active=True).count()
    categories_count = Category.objects.count()
    featured_count = Destination.objects.filter(is_active=True, is_featured=True).count()
    
    return Response({
        'total_destinations': total_destinations,
        'categories_count': categories_count,
        'featured_destinations': featured_count,
    })

# Booking views (require authentication)
class UserBookingsView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('destination').order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BookingDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('destination')

# Galler
y Views
@api_view(['GET'])
@permission_classes([AllowAny])
def gallery_categories(request):
    """Get all gallery categories"""
    categories = GalleryCategory.objects.all()
    serializer = GalleryCategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def gallery_images(request):
    """Get all gallery images with optional filtering"""
    images = GalleryImage.objects.all()
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        images = images.filter(category__slug=category)
    
    # Filter featured only
    featured = request.GET.get('featured')
    if featured == 'true':
        images = images.filter(is_featured=True)
    
    serializer = GalleryImageSerializer(images, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def gallery_videos(request):
    """Get all gallery videos with optional filtering"""
    videos = GalleryVideo.objects.all()
    
    # Filter by category
    category = request.GET.get('category')
    if category:
        videos = videos.filter(category__slug=category)
    
    # Filter featured only
    featured = request.GET.get('featured')
    if featured == 'true':
        videos = videos.filter(is_featured=True)
    
    serializer = GalleryVideoSerializer(videos, many=True)
    return Response(serializer.data)
