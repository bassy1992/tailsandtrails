from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F, Sum
from django.db import models
from django.utils import timezone
from .models import (
    TicketCategory, Venue, Ticket, TicketPurchase, 
    TicketCode, TicketReview, TicketPromoCode
)
from .serializers import (
    TicketCategorySerializer, VenueSerializer, TicketListSerializer,
    TicketDetailSerializer, TicketPurchaseSerializer, TicketPurchaseCreateSerializer,
    TicketCodeSerializer, TicketReviewSerializer, TicketReviewCreateSerializer,
    TicketPromoCodeSerializer, PromoCodeValidationSerializer
)

class TicketCategoryListView(generics.ListAPIView):
    queryset = TicketCategory.objects.filter(is_active=True)
    serializer_class = TicketCategorySerializer
    permission_classes = [AllowAny]  # Allow public access for browsing
    ordering = ['order', 'name']

class VenueListView(generics.ListAPIView):
    queryset = Venue.objects.filter(is_active=True)
    serializer_class = VenueSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'city', 'address']
    filterset_fields = ['city', 'region']
    ordering = ['name']

class VenueDetailView(generics.RetrieveAPIView):
    queryset = Venue.objects.filter(is_active=True)
    serializer_class = VenueSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing
    lookup_field = 'slug'

class TicketListView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'description', 'venue__name', 'venue__city']
    filterset_fields = ['category', 'venue', 'ticket_type', 'status', 'is_featured']
    ordering_fields = ['price', 'event_date', 'created_at', 'rating', 'sales_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Ticket.objects.filter(status='published').select_related('category', 'venue')
        
        # Filter by ID if provided
        ticket_id = self.request.query_params.get('id')
        if ticket_id:
            queryset = queryset.filter(id=ticket_id)
            return queryset
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(event_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(event_date__lte=end_date)
        
        # Filter by availability
        available_only = self.request.query_params.get('available_only')
        if available_only and available_only.lower() == 'true':
            now = timezone.now()
            queryset = queryset.filter(
                available_quantity__gt=0,
                sale_start_date__lte=now,
                sale_end_date__gte=now
            )
        
        return queryset

class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.filter(status='published').select_related('category', 'venue')
    serializer_class = TicketDetailSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        Ticket.objects.filter(pk=instance.pk).update(views_count=F('views_count') + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class FeaturedTicketsView(generics.ListAPIView):
    queryset = Ticket.objects.filter(
        status='published', 
        is_featured=True
    ).select_related('category', 'venue')[:6]
    serializer_class = TicketListSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing

class PopularTicketsView(generics.ListAPIView):
    queryset = Ticket.objects.filter(
        status='published'
    ).select_related('category', 'venue').order_by('-sales_count', '-rating')[:10]
    serializer_class = TicketListSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing

class UpcomingTicketsView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [AllowAny]  # Allow public access for browsing
    
    def get_queryset(self):
        now = timezone.now()
        return Ticket.objects.filter(
            status='published',
            event_date__gte=now
        ).select_related('category', 'venue').order_by('event_date')[:10]

class TicketPurchaseCreateView(generics.CreateAPIView):
    serializer_class = TicketPurchaseCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            purchase = serializer.save()
            response_serializer = TicketPurchaseSerializer(purchase)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': 'Failed to create purchase. Please try again.'},
                status=status.HTTP_400_BAD_REQUEST
            )

class TicketPurchaseListView(generics.ListAPIView):
    serializer_class = TicketPurchaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return TicketPurchase.objects.filter(
            user=self.request.user
        ).select_related('ticket__category', 'ticket__venue')

class TicketPurchaseDetailView(generics.RetrieveAPIView):
    serializer_class = TicketPurchaseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'purchase_id'
    
    def get_queryset(self):
        return TicketPurchase.objects.filter(
            user=self.request.user
        ).select_related('ticket__category', 'ticket__venue').prefetch_related('ticket_codes')

class TicketCodeValidateView(generics.RetrieveAPIView):
    serializer_class = TicketCodeSerializer
    lookup_field = 'code'
    
    def get_queryset(self):
        return TicketCode.objects.select_related('purchase__ticket')
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            
            # Additional validation info
            data = serializer.data
            data['ticket_info'] = {
                'title': instance.purchase.ticket.title,
                'event_date': instance.purchase.ticket.event_date,
                'venue': instance.purchase.ticket.venue.name if instance.purchase.ticket.venue else None
            }
            
            return Response(data)
        except TicketCode.DoesNotExist:
            return Response(
                {'error': 'Invalid ticket code'},
                status=status.HTTP_404_NOT_FOUND
            )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def use_ticket_code(request, code):
    try:
        ticket_code = TicketCode.objects.get(code=code)
        
        if not ticket_code.is_valid:
            return Response(
                {'error': 'Ticket code is not valid or has already been used'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark as used
        ticket_code.status = 'used'
        ticket_code.used_at = timezone.now()
        ticket_code.used_by = request.user.get_full_name() or request.user.username
        ticket_code.save()
        
        return Response({
            'message': 'Ticket code successfully validated and marked as used',
            'ticket_info': {
                'title': ticket_code.purchase.ticket.title,
                'event_date': ticket_code.purchase.ticket.event_date,
                'customer': ticket_code.purchase.customer_name
            }
        })
        
    except TicketCode.DoesNotExist:
        return Response(
            {'error': 'Invalid ticket code'},
            status=status.HTTP_404_NOT_FOUND
        )

class TicketReviewListView(generics.ListAPIView):
    serializer_class = TicketReviewSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        ticket_id = self.kwargs.get('ticket_id')
        return TicketReview.objects.filter(
            ticket_id=ticket_id,
            is_active=True
        ).select_related('user')

class TicketReviewCreateView(generics.CreateAPIView):
    serializer_class = TicketReviewCreateSerializer
    permission_classes = [IsAuthenticated]

class UserTicketReviewsView(generics.ListAPIView):
    serializer_class = TicketReviewSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-created_at']
    
    def get_queryset(self):
        return TicketReview.objects.filter(
            user=self.request.user
        ).select_related('ticket')

@api_view(['POST'])
@permission_classes([AllowAny])
def validate_promo_code(request):
    serializer = PromoCodeValidationSerializer(data=request.data)
    if serializer.is_valid():
        promo_code = serializer.validated_data['promo_code']
        total_amount = serializer.validated_data['total_amount']
        
        discount_amount = promo_code.calculate_discount(total_amount)
        final_amount = total_amount - discount_amount
        
        return Response({
            'valid': True,
            'discount_amount': discount_amount,
            'final_amount': final_amount,
            'promo_code': TicketPromoCodeSerializer(promo_code).data
        })
    
    return Response({
        'valid': False,
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])  # Allow public access for general stats
def ticket_stats(request):
    """Get general ticket statistics"""
    total_tickets = Ticket.objects.filter(status='published').count()
    total_venues = Venue.objects.filter(is_active=True).count()
    total_categories = TicketCategory.objects.filter(is_active=True).count()
    
    # Upcoming events
    now = timezone.now()
    upcoming_events = Ticket.objects.filter(
        status='published',
        event_date__gte=now
    ).count()
    
    return Response({
        'total_tickets': total_tickets,
        'total_venues': total_venues,
        'total_categories': total_categories,
        'upcoming_events': upcoming_events
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ticket_stats(request):
    """Get user-specific ticket statistics"""
    user = request.user
    
    total_purchases = TicketPurchase.objects.filter(user=user).count()
    total_spent = TicketPurchase.objects.filter(
        user=user, 
        payment_status='completed'
    ).aggregate(total=models.Sum('total_amount'))['total'] or 0
    
    upcoming_tickets = TicketPurchase.objects.filter(
        user=user,
        status='confirmed',
        ticket__event_date__gte=timezone.now()
    ).count()
    
    return Response({
        'total_purchases': total_purchases,
        'total_spent': total_spent,
        'upcoming_tickets': upcoming_tickets
    })