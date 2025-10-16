from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction, models
from django.utils import timezone
from decimal import Decimal
import uuid

from .models import Ticket, TicketCategory, TicketPurchase
from .addon_models import AddOnCategory, AddOn, BookingAddOn
from .serializers import (
    TicketSerializer, TicketCategorySerializer, AddOnCategorySerializer,
    AddOnSerializer, TicketPurchaseSerializer, BookingAddOnSerializer
)

class TicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        now = timezone.now()
        return Ticket.objects.filter(
            status='published',
            available_quantity__gt=0,
            sale_start_date__lte=now,
            sale_end_date__gte=now
        )

class TicketDetailView(generics.RetrieveAPIView):
    queryset = Ticket.objects.filter(status='published')
    serializer_class = TicketSerializer
    lookup_field = 'slug'
    permission_classes = [AllowAny]

class TicketCategoryListView(generics.ListAPIView):
    queryset = TicketCategory.objects.filter(is_active=True)
    serializer_class = TicketCategorySerializer
    permission_classes = [AllowAny]

@api_view(['GET'])
@permission_classes([AllowAny])
def get_ticket_addons(request, ticket_id):
    """Get available add-ons for a specific ticket"""
    try:
        ticket = get_object_or_404(Ticket, id=ticket_id)
        
        # Get add-ons applicable to this ticket or its category
        addons = AddOn.objects.filter(
            is_active=True
        ).filter(
            models.Q(applicable_tickets=ticket) | 
            models.Q(applicable_categories=ticket.category) |
            models.Q(applicable_tickets__isnull=True, applicable_categories__isnull=True)
        ).prefetch_related('options', 'category').distinct()
        
        # Group by category
        categories = AddOnCategory.objects.filter(
            is_active=True,
            addons__in=addons
        ).prefetch_related('addons').distinct()
        
        # Calculate prices based on ticket base price
        base_amount = float(ticket.effective_price)
        travelers = int(request.GET.get('travelers', 1))
        
        context = {
            'request': request,
            'base_amount': base_amount,
            'travelers': travelers
        }
        
        serializer = AddOnCategorySerializer(categories, many=True, context=context)
        
        return Response({
            'success': True,
            'categories': serializer.data,
            'ticket_info': {
                'id': ticket.id,
                'title': ticket.title,
                'base_price': float(ticket.effective_price),
                'currency': ticket.currency
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_booking_total(request):
    """Calculate total booking cost including selected add-ons"""
    try:
        data = request.data
        ticket_id = data.get('ticket_id')
        quantity = int(data.get('quantity', 1))
        travelers = int(data.get('travelers', 1))
        selected_addons = data.get('selected_addons', [])
        
        ticket = get_object_or_404(Ticket, id=ticket_id)
        base_price = float(ticket.effective_price)
        base_total = base_price * quantity
        
        addon_total = Decimal('0.00')
        addon_details = []
        
        for addon_selection in selected_addons:
            addon_id = addon_selection.get('addon_id')
            option_id = addon_selection.get('option_id')
            addon_quantity = int(addon_selection.get('quantity', 1))
            
            addon = get_object_or_404(AddOn, id=addon_id, is_active=True)
            
            if option_id:
                # Add-on with specific option selected
                option = get_object_or_404(AddOnOption, id=option_id, addon=addon)
                unit_price = option.price
                addon_name = f"{addon.name} - {option.name}"
            else:
                # Simple add-on
                unit_price = addon.calculate_price(
                    base_amount=base_total, 
                    quantity=addon_quantity, 
                    travelers=travelers
                )
                addon_name = addon.name
            
            total_addon_price = unit_price * addon_quantity
            addon_total += total_addon_price
            
            addon_details.append({
                'addon_id': addon_id,
                'option_id': option_id,
                'name': addon_name,
                'unit_price': float(unit_price),
                'quantity': addon_quantity,
                'total_price': float(total_addon_price),
                'pricing_type': addon.pricing_type
            })
        
        grand_total = base_total + float(addon_total)
        
        return Response({
            'success': True,
            'calculation': {
                'base_total': base_total,
                'addon_total': float(addon_total),
                'grand_total': grand_total,
                'currency': ticket.currency,
                'breakdown': {
                    'ticket': {
                        'name': ticket.title,
                        'unit_price': base_price,
                        'quantity': quantity,
                        'total': base_total
                    },
                    'addons': addon_details
                }
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_booking_with_addons(request):
    """Create a booking with selected add-ons"""
    try:
        with transaction.atomic():
            data = request.data
            
            # Create main ticket purchase
            ticket_id = data.get('ticket_id')
            quantity = int(data.get('quantity', 1))
            customer_info = data.get('customer_info', {})
            selected_addons = data.get('selected_addons', [])
            payment_info = data.get('payment_info', {})
            
            ticket = get_object_or_404(Ticket, id=ticket_id)
            
            # Generate booking reference
            booking_reference = f"BK{uuid.uuid4().hex[:8].upper()}"
            
            # Calculate totals
            base_total = float(ticket.effective_price) * quantity
            addon_total = Decimal('0.00')
            
            # Create ticket purchase
            purchase = TicketPurchase.objects.create(
                ticket=ticket,
                quantity=quantity,
                unit_price=ticket.effective_price,
                total_amount=base_total,  # Will be updated after add-ons
                customer_name=customer_info.get('name', ''),
                customer_email=customer_info.get('email', ''),
                customer_phone=customer_info.get('phone', ''),
                payment_method=payment_info.get('method', ''),
                special_requests=f"Booking Reference: {booking_reference}"
            )
            
            # Process selected add-ons
            for addon_selection in selected_addons:
                addon_id = addon_selection.get('addon_id')
                option_id = addon_selection.get('option_id')
                addon_quantity = int(addon_selection.get('quantity', 1))
                
                addon = get_object_or_404(AddOn, id=addon_id, is_active=True)
                option = None
                
                if option_id:
                    option = get_object_or_404(AddOnOption, id=option_id, addon=addon)
                    unit_price = option.price
                else:
                    unit_price = addon.calculate_price(
                        base_amount=base_total,
                        quantity=addon_quantity,
                        travelers=data.get('travelers', 1)
                    )
                
                total_addon_price = unit_price * addon_quantity
                addon_total += total_addon_price
                
                # Create booking add-on record
                BookingAddOn.objects.create(
                    booking_reference=booking_reference,
                    addon=addon,
                    option=option,
                    quantity=addon_quantity,
                    unit_price=unit_price,
                    total_price=total_addon_price,
                    customer_name=customer_info.get('name', ''),
                    customer_email=customer_info.get('email', '')
                )
            
            # Update purchase total with add-ons
            purchase.total_amount = base_total + float(addon_total)
            purchase.save()
            
            # Update ticket availability
            ticket.available_quantity -= quantity
            ticket.save()
            
            return Response({
                'success': True,
                'booking': {
                    'reference': booking_reference,
                    'purchase_id': str(purchase.purchase_id),
                    'total_amount': float(purchase.total_amount),
                    'base_amount': base_total,
                    'addon_amount': float(addon_total),
                    'currency': ticket.currency
                }
            })
            
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_booking_details(request, booking_reference):
    """Get booking details including add-ons"""
    try:
        # Get main purchase
        purchase = TicketPurchase.objects.filter(
            special_requests__icontains=booking_reference
        ).first()
        
        if not purchase:
            return Response({
                'success': False,
                'error': 'Booking not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Get add-ons
        booking_addons = BookingAddOn.objects.filter(
            booking_reference=booking_reference
        ).select_related('addon', 'option')
        
        purchase_data = TicketPurchaseSerializer(purchase).data
        addons_data = BookingAddOnSerializer(booking_addons, many=True).data
        
        return Response({
            'success': True,
            'booking': {
                'reference': booking_reference,
                'purchase': purchase_data,
                'addons': addons_data,
                'total_with_addons': float(purchase.total_amount)
            }
        })
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)