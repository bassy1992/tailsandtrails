from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking, Destination, Review
from tickets.models import TicketPurchase
from .serializers import BookingSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_overview(request):
    """Get dashboard overview statistics for the authenticated user"""
    user = request.user
    
    # Get user's bookings
    bookings = Booking.objects.filter(user=user)
    completed_bookings = bookings.filter(status='completed')
    
    # Get user's ticket purchases
    ticket_purchases = TicketPurchase.objects.filter(user=user)
    completed_tickets = ticket_purchases.filter(status='completed')
    
    # Calculate statistics
    total_bookings = bookings.count()
    total_tickets = ticket_purchases.count()
    destinations_visited = completed_bookings.values('destination').distinct().count()
    
    # Calculate total spent (bookings + tickets)
    booking_total = bookings.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    ticket_total = ticket_purchases.aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    total_spent = float(booking_total) + float(ticket_total)
    
    # Get member since date (assuming user creation date)
    member_since = user.date_joined
    
    # Calculate member level based on total spent
    if total_spent >= 5000:
        member_level = 'Platinum'
        member_color = 'bg-purple-100 text-purple-800'
    elif total_spent >= 2000:
        member_level = 'Gold'
        member_color = 'bg-yellow-100 text-yellow-800'
    elif total_spent >= 500:
        member_level = 'Silver'
        member_color = 'bg-gray-100 text-gray-800'
    else:
        member_level = 'Bronze'
        member_color = 'bg-orange-100 text-orange-800'
    
    return Response({
        'total_bookings': total_bookings + total_tickets,
        'destinations_visited': destinations_visited,
        'total_spent': total_spent,
        'member_since': member_since,
        'member_level': member_level,
        'member_color': member_color,
        'points': int(total_spent * 0.1)  # 10% of spending as points
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_bookings(request):
    """Get user's bookings for dashboard"""
    user = request.user
    
    # Get destination bookings
    bookings = Booking.objects.filter(user=user).select_related(
        'destination'
    ).prefetch_related(
        'destination__images'
    ).order_by('-created_at')
    
    # Get ticket purchases
    ticket_purchases = TicketPurchase.objects.filter(user=user).select_related(
        'ticket', 'ticket__venue'
    ).order_by('-created_at')
    
    # Serialize bookings
    booking_data = []
    for booking in bookings:
        image_url = booking.destination.images.first().image_url if booking.destination.images.exists() else None
        # Convert duration choice to readable format
        duration_map = {
            '1_day': '1 Day',
            '2_days': '2 Days, 1 Night',
            '3_days': '3 Days, 2 Nights',
            '4_days': '4 Days, 3 Nights',
            '5_days': '5 Days, 4 Nights',
            '6_days': '6 Days, 5 Nights',
            '7_days': '7 Days, 6 Nights',
            '7_plus_days': '7+ Days'
        }
        
        booking_data.append({
            'id': booking.booking_reference,
            'type': 'destination',
            'destination': booking.destination.name,
            'date': booking.booking_date,
            'duration': duration_map.get(booking.destination.duration, booking.destination.duration),
            'status': booking.status,
            'amount': f"GH₵ {booking.total_amount}",
            'image': image_url,
            'participants': booking.participants,
            'created_at': booking.created_at
        })
    
    # Add ticket purchases
    for purchase in ticket_purchases:
        booking_data.append({
            'id': str(purchase.purchase_id),
            'type': 'ticket',
            'destination': purchase.ticket.title,
            'date': purchase.ticket.event_date.date() if purchase.ticket.event_date else None,
            'duration': f"Event at {purchase.ticket.venue.name}" if purchase.ticket.venue else "Event",
            'status': purchase.status,
            'amount': f"GH₵ {purchase.total_amount}",
            'image': purchase.ticket.image if purchase.ticket.image else None,
            'participants': purchase.quantity,
            'created_at': purchase.created_at
        })
    
    # Sort by creation date
    booking_data.sort(key=lambda x: x['created_at'], reverse=True)
    
    return Response(booking_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_activity(request):
    """Get recent activity for dashboard"""
    user = request.user
    
    activities = []
    
    # Get recent bookings
    recent_bookings = Booking.objects.filter(
        user=user
    ).select_related('destination').order_by('-updated_at')[:5]
    
    for booking in recent_bookings:
        status_color = {
            'confirmed': 'green',
            'pending': 'yellow',
            'completed': 'blue',
            'cancelled': 'red'
        }.get(booking.status, 'gray')
        
        activities.append({
            'id': booking.id,
            'type': 'booking',
            'title': f"{booking.destination.name} booking {booking.status}",
            'date': booking.updated_at,
            'status': booking.status,
            'status_color': status_color,
            'reference': booking.booking_reference
        })
    
    # Get recent ticket purchases
    recent_tickets = TicketPurchase.objects.filter(
        user=user
    ).select_related('ticket').order_by('-updated_at')[:5]
    
    for purchase in recent_tickets:
        status_color = {
            'confirmed': 'green',
            'pending': 'yellow',
            'completed': 'blue',
            'cancelled': 'red'
        }.get(purchase.status, 'gray')
        
        activities.append({
            'id': purchase.id,
            'type': 'ticket',
            'title': f"{purchase.ticket.title} ticket {purchase.status}",
            'date': purchase.updated_at,
            'status': purchase.status,
            'status_color': status_color,
            'reference': str(purchase.purchase_id)
        })
    
    # Sort by date and limit to 10 most recent
    activities.sort(key=lambda x: x['date'], reverse=True)
    activities = activities[:10]
    
    return Response(activities)