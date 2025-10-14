from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import logging
import uuid

from .models import Ticket, TicketPurchase, TicketCode
from .serializers import TicketPurchaseSerializer, TicketListSerializer
from authentication.models import User

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Require authentication for purchases
def create_ticket_purchase(request):
    """Create a ticket purchase directly (separate from Payment model)"""
    try:
        data = request.data
        
        # Get ticket
        ticket_id = data.get('ticket_id')
        if not ticket_id:
            return Response({
                'success': False,
                'error': 'ticket_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        ticket = get_object_or_404(Ticket, id=ticket_id, status='published')
        
        # Validate quantity
        quantity = int(data.get('quantity', 1))
        if quantity < ticket.min_purchase or quantity > ticket.max_purchase:
            return Response({
                'success': False,
                'error': f'Quantity must be between {ticket.min_purchase} and {ticket.max_purchase}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check availability
        if ticket.available_quantity < quantity:
            return Response({
                'success': False,
                'error': f'Only {ticket.available_quantity} tickets available'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Use authenticated user
        user = request.user
        
        # Calculate pricing - use provided amount if available (for VIP/Premium tickets)
        provided_total = data.get('total_amount')
        if provided_total:
            # Use the provided total amount (e.g., for VIP/Premium tickets)
            total_amount = float(provided_total)
            unit_price = total_amount / quantity
        else:
            # Use base ticket price
            unit_price = ticket.discount_price if ticket.discount_price else ticket.price
            total_amount = unit_price * quantity
        
        # Apply promo code if provided
        discount_applied = 0
        promo_code = data.get('promo_code')
        if promo_code:
            # TODO: Implement promo code logic
            pass
        
        # Create ticket purchase
        with transaction.atomic():
            purchase = TicketPurchase.objects.create(
                ticket=ticket,
                user=user,
                quantity=quantity,
                unit_price=unit_price,
                total_amount=total_amount - discount_applied,
                discount_applied=discount_applied,
                customer_name=data.get('customer_name', ''),
                customer_email=data.get('customer_email', ''),
                customer_phone=data.get('customer_phone', ''),
                payment_method=data.get('payment_method', 'momo'),
                special_requests=data.get('special_requests', ''),
                status='pending'  # Start as pending
            )
            
            # Update ticket availability
            ticket.available_quantity -= quantity
            ticket.save()
            
            # Handle payment reference and processing
            payment_method = data.get('payment_method', 'momo')
            payment_reference = data.get('payment_reference')
            
            if payment_method in ['momo', 'mtn_momo', 'vodafone_cash', 'airteltigo_money']:
                # Use provided payment reference if available, otherwise create one
                if payment_reference:
                    purchase.payment_reference = payment_reference
                    # If we have a real payment reference, the payment was already processed
                    purchase.status = 'confirmed'
                    purchase.payment_status = 'completed'
                    purchase.payment_date = timezone.now()
                else:
                    # Simulate mobile money payment for direct purchases without payment reference
                    purchase.payment_reference = f"TICKET_{purchase.purchase_id}"
                    purchase.status = 'confirmed'  # Auto-confirm for demo
                    purchase.payment_status = 'completed'
                    purchase.payment_date = timezone.now()
                purchase.save()
                
                # Generate ticket codes
                generate_ticket_codes(purchase)
                
                return Response({
                    'success': True,
                    'message': 'Ticket purchase completed successfully',
                    'purchase': TicketPurchaseSerializer(purchase).data,
                    'payment_reference': purchase.payment_reference
                }, status=status.HTTP_201_CREATED)
            
            elif payment_method == 'stripe':
                # Use provided payment reference if available
                if payment_reference:
                    purchase.payment_reference = payment_reference
                    # If we have a real payment reference, the payment was already processed
                    purchase.status = 'confirmed'
                    purchase.payment_status = 'completed'
                    purchase.payment_date = timezone.now()
                else:
                    # For Stripe, we'd create a payment intent
                    # For now, just mark as pending
                    purchase.payment_reference = f"STRIPE_{purchase.purchase_id}"
                purchase.save()
                
                return Response({
                    'success': True,
                    'message': 'Ticket purchase created, awaiting payment',
                    'purchase': TicketPurchaseSerializer(purchase).data,
                    'payment_reference': purchase.payment_reference,
                    'requires_payment': True
                }, status=status.HTTP_201_CREATED)
            
            else:
                return Response({
                    'success': False,
                    'error': 'Invalid payment method'
                }, status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        logger.error(f"Ticket purchase error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while processing your ticket purchase'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def generate_ticket_codes(purchase):
    """Generate ticket codes for a purchase"""
    codes = []
    for i in range(purchase.quantity):
        code = TicketCode.objects.create(
            purchase=purchase,
            status='active'
        )
        codes.append(code)
    return codes

@api_view(['GET'])
@permission_classes([AllowAny])
def ticket_purchase_status(request, purchase_id):
    """Check ticket purchase status"""
    try:
        purchase = TicketPurchase.objects.get(purchase_id=purchase_id)
        return Response({
            'success': True,
            'purchase': TicketPurchaseSerializer(purchase).data
        })
    except TicketPurchase.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Purchase not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def complete_ticket_purchase(request, purchase_id):
    """Complete a ticket purchase (for demo/admin purposes)"""
    try:
        purchase = TicketPurchase.objects.get(purchase_id=purchase_id)
        
        if purchase.status in ['pending', 'processing']:
            purchase.status = 'confirmed'
            purchase.payment_status = 'completed'
            purchase.payment_date = timezone.now()
            purchase.save()
            
            # Generate ticket codes if not already generated
            if not purchase.ticket_codes.exists():
                generate_ticket_codes(purchase)
            
            return Response({
                'success': True,
                'message': 'Ticket purchase completed successfully',
                'purchase': TicketPurchaseSerializer(purchase).data
            })
        else:
            return Response({
                'success': False,
                'message': f'Purchase is already {purchase.status}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except TicketPurchase.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Purchase not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_ticket_purchases(request):
    """Get user's ticket purchases"""
    purchases = TicketPurchase.objects.filter(
        user=request.user
    ).select_related('ticket', 'ticket__venue').order_by('-created_at')
    
    return Response({
        'success': True,
        'purchases': TicketPurchaseSerializer(purchases, many=True).data
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def ticket_purchase_details(request, purchase_id):
    """Get detailed ticket purchase information"""
    try:
        purchase = TicketPurchase.objects.select_related(
            'ticket', 'ticket__venue', 'user'
        ).prefetch_related('ticket_codes').get(purchase_id=purchase_id)
        
        # Get ticket codes
        codes = purchase.ticket_codes.all()
        
        return Response({
            'success': True,
            'purchase': TicketPurchaseSerializer(purchase).data,
            'ticket_codes': [
                {
                    'code': code.code,
                    'status': code.status,
                    'qr_code_data': code.qr_code_data,
                    'is_transferable': code.is_transferable,
                    'expires_at': code.expires_at
                } for code in codes
            ]
        })
        
    except TicketPurchase.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Purchase not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([AllowAny])
def simulate_ticket_payment(request, purchase_id):
    """Simulate ticket payment completion (for demo)"""
    try:
        purchase = TicketPurchase.objects.get(purchase_id=purchase_id)
        
        if purchase.status == 'pending':
            # Simulate payment success (90% success rate)
            import random
            if random.random() > 0.1:
                purchase.status = 'confirmed'
                purchase.payment_status = 'completed'
                purchase.payment_date = timezone.now()
                purchase.save()
                
                # Generate ticket codes
                if not purchase.ticket_codes.exists():
                    generate_ticket_codes(purchase)
                
                return Response({
                    'success': True,
                    'message': 'Payment completed successfully',
                    'purchase': TicketPurchaseSerializer(purchase).data
                })
            else:
                purchase.status = 'cancelled'
                purchase.payment_status = 'failed'
                purchase.save()
                
                # Restore ticket availability
                purchase.ticket.available_quantity += purchase.quantity
                purchase.ticket.save()
                
                return Response({
                    'success': False,
                    'message': 'Payment failed',
                    'purchase': TicketPurchaseSerializer(purchase).data
                })
        else:
            return Response({
                'success': False,
                'message': f'Purchase is already {purchase.status}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except TicketPurchase.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Purchase not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([AllowAny])
def debug_ticket_purchases(request):
    """Debug endpoint to list recent ticket purchases"""
    recent_purchases = TicketPurchase.objects.select_related(
        'ticket', 'user'
    ).order_by('-created_at')[:20]
    
    purchases_data = []
    for purchase in recent_purchases:
        purchases_data.append({
            'purchase_id': str(purchase.purchase_id),
            'ticket': purchase.ticket.title,
            'customer': purchase.customer_name or (purchase.user.email if purchase.user else 'Anonymous'),
            'quantity': purchase.quantity,
            'total_amount': str(purchase.total_amount),
            'status': purchase.status,
            'payment_status': purchase.payment_status,
            'created_at': purchase.created_at.isoformat(),
        })
    
    return Response({
        'total_purchases': TicketPurchase.objects.count(),
        'recent_purchases': purchases_data
    })