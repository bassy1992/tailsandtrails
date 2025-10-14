from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Payment, PaymentProvider


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_details(request, reference):
    """Get complete payment details including booking information"""
    try:
        payment = get_object_or_404(Payment, reference=reference, user=request.user)
        
        # Build complete payment data for frontend
        payment_data = {
            'reference': payment.reference,
            'amount': float(payment.amount),
            'currency': payment.currency,
            'status': payment.status,
            'description': payment.description,
            'payment_method': payment.payment_method,
            'created_at': payment.created_at.isoformat(),
            'processed_at': payment.processed_at.isoformat() if payment.processed_at else None,
        }
        
        # Add booking details from metadata
        if payment.metadata and 'booking_details' in payment.metadata:
            booking_details = payment.metadata['booking_details']
            payment_data['bookingDetails'] = booking_details
            
            # Extract tour name for easier access
            if 'bookingData' in booking_details and 'tourName' in booking_details['bookingData']:
                payment_data['tourName'] = booking_details['bookingData']['tourName']
        
        # Add customer info
        payment_data['customerInfo'] = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': getattr(request.user, 'phone_number', None) or payment.phone_number
        }
        
        # Add payment details
        payment_data['paymentDetails'] = {
            'method': 'Mobile Money' if payment.payment_method == 'mobile_money' else 'Card Payment',
            'provider': payment.provider.name if payment.provider else None,
            'transactionId': payment.reference,
            'timestamp': payment.processed_at.isoformat() if payment.processed_at else payment.created_at.isoformat(),
            'gateway': 'Paystack'
        }
        
        return Response(payment_data)
        
    except Payment.DoesNotExist:
        return Response(
            {'error': 'Payment not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_payment_methods(request):
    """Get available payment methods for checkout"""
    try:
        # Define available payment methods
        payment_methods = [
            {
                'id': 'mobile_money',
                'name': 'Mobile Money',
                'description': 'MTN, Vodafone, AirtelTigo',
                'icon': '📱',
                'processing_time': 'Instant',
                'providers': [
                    {'name': 'MTN Mobile Money', 'code': 'mtn'},
                    {'name': 'Vodafone Cash', 'code': 'vodafone'},
                    {'name': 'AirtelTigo Money', 'code': 'airteltigo'}
                ]
            },
            {
                'id': 'card',
                'name': 'Credit/Debit Card',
                'description': 'Visa, Mastercard, Verve',
                'icon': '💳',
                'processing_time': 'Secure',
                'providers': [
                    {'name': 'Paystack', 'code': 'paystack'}
                ]
            },
            {
                'id': 'bank_transfer',
                'name': 'Bank Transfer',
                'description': 'Direct bank transfer',
                'icon': '🏦',
                'processing_time': '1-2 days',
                'providers': []
            }
        ]
        
        return Response({
            'success': True,
            'payment_methods': payment_methods
        })
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )