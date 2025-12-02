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
import threading
import time
import random

from .models import Payment, PaymentProvider, PaymentCallback
from .serializers import (
    PaymentCreateSerializer, PaymentSerializer, PaymentListSerializer,
    PaymentProviderSerializer, PaymentCallbackSerializer, CheckoutPaymentSerializer
)
from .services import PaymentService
from .utils import generate_payment_reference
from .mtn_momo_service import MTNMoMoService

logger = logging.getLogger(__name__)

class PaymentProviderListView(generics.ListAPIView):
    """List active payment providers"""
    queryset = PaymentProvider.objects.filter(is_active=True)
    serializer_class = PaymentProviderSerializer
    permission_classes = [permissions.AllowAny]

class PaymentCreateView(generics.CreateAPIView):
    """Create a new payment"""
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        # Generate unique reference
        reference = generate_payment_reference()
        
        # Create payment with user
        payment = serializer.save(
            user=self.request.user,
            reference=reference
        )
        
        # Initialize payment with provider
        try:
            payment_service = PaymentService()
            result = payment_service.initiate_payment(payment)
            
            if result.get('success'):
                payment.external_reference = result.get('external_reference')
                payment.status = 'processing'
                payment.save()
                
                # Log successful initiation
                payment.log('info', 'Payment initiated successfully', result)
            else:
                payment.status = 'failed'
                payment.save()
                
                # Log failure
                payment.log('error', 'Payment initiation failed', result)
                
        except Exception as e:
            logger.error(f"Payment initiation error for {payment.reference}: {str(e)}")
            payment.status = 'failed'
            payment.save()
            payment.log('error', f'Payment initiation exception: {str(e)}')

class PaymentDetailView(generics.RetrieveAPIView):
    """Get payment details"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'reference'
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).select_related(
            'provider', 'booking'
        )

class PaymentListView(generics.ListAPIView):
    """List user's payments"""
    serializer_class = PaymentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_payment(request, reference):
    """Cancel a pending payment"""
    payment = get_object_or_404(
        Payment, 
        reference=reference, 
        user=request.user,
        status__in=['pending', 'processing']
    )
    
    try:
        payment_service = PaymentService()
        result = payment_service.cancel_payment(payment)
        
        if result.get('success'):
            payment.status = 'cancelled'
            payment.save()
            payment.log('info', 'Payment cancelled by user')
            
            return Response({
                'success': True,
                'message': 'Payment cancelled successfully'
            })
        else:
            return Response({
                'success': False,
                'message': result.get('message', 'Failed to cancel payment')
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Payment cancellation error for {reference}: {str(e)}")
        return Response({
            'success': False,
            'message': 'An error occurred while cancelling the payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def payment_callback(request, provider_code):
    """Handle payment provider callbacks"""
    try:
        provider = get_object_or_404(PaymentProvider, code=provider_code, is_active=True)
        
        # Get payment reference from callback data
        payment_service = PaymentService()
        payment_ref = payment_service.extract_payment_reference(provider, request.data)
        
        if not payment_ref:
            logger.warning(f"No payment reference found in callback from {provider_code}")
            return Response({'status': 'error', 'message': 'Invalid callback data'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        payment = get_object_or_404(Payment, reference=payment_ref)
        
        # Create callback record
        with transaction.atomic():
            callback_serializer = PaymentCallbackSerializer(data={
                'provider_reference': request.data.get('reference', ''),
                'status': request.data.get('status', ''),
                'callback_data': request.data
            })
            
            if callback_serializer.is_valid():
                callback = callback_serializer.save(payment=payment)
                
                # Process the callback
                result = payment_service.process_callback(payment, callback)
                
                if result.get('success'):
                    # Update payment status
                    new_status = result.get('status')
                    if new_status and new_status != payment.status:
                        payment.status = new_status
                        if new_status in ['successful', 'failed', 'cancelled']:
                            payment.processed_at = timezone.now()
                        payment.save()
                        
                        payment.log('info', f'Payment status updated to {new_status}', result)
                    
                    callback.processed = True
                    callback.save()
                    
                    return Response({'status': 'success'})
                else:
                    payment.log('warning', 'Callback processing failed', result)
                    return Response({'status': 'error', 'message': 'Processing failed'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.error(f"Invalid callback data from {provider_code}: {callback_serializer.errors}")
                return Response({'status': 'error', 'message': 'Invalid data'}, 
                              status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        logger.error(f"Payment callback error from {provider_code}: {str(e)}")
        return Response({'status': 'error', 'message': 'Internal error'}, 
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])  # Changed to AllowAny for demo purposes
def payment_status(request, reference):
    """Check payment status"""
    try:
        payment = Payment.objects.get(reference=reference)
    except Payment.DoesNotExist:
        # Provide helpful debugging information
        logger.warning(f"Payment not found: {reference}")
        
        # Get similar references for debugging
        similar_payments = Payment.objects.filter(
            reference__icontains=reference[:10]  # First 10 chars
        ).values_list('reference', flat=True)[:5]
        
        return Response({
            'error': 'Payment not found',
            'reference': reference,
            'message': f'No payment found with reference: {reference}',
            'debug_info': {
                'total_payments': Payment.objects.count(),
                'similar_references': list(similar_payments),
                'recent_payments': list(Payment.objects.order_by('-created_at')[:5].values_list('reference', flat=True))
            }
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Optionally refresh status from provider
    if payment.status in ['pending', 'processing']:
        try:
            payment_service = PaymentService()
            result = payment_service.check_payment_status(payment)
            
            if result.get('success') and result.get('status'):
                new_status = result.get('status')
                if new_status != payment.status:
                    payment.status = new_status
                    if new_status in ['successful', 'failed', 'cancelled']:
                        payment.processed_at = timezone.now()
                    payment.save()
                    payment.log('info', f'Status updated from provider check: {new_status}')
                    
        except Exception as e:
            logger.error(f"Status check error for {reference}: {str(e)}")
    
    serializer = PaymentSerializer(payment)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])  # For demo purposes
def complete_payment(request, reference):
    """Manually complete a payment (for demo purposes)"""
    payment = get_object_or_404(Payment, reference=reference)
    
    # Get desired status from request, default to successful
    desired_status = request.data.get('status', 'successful')
    if desired_status not in ['successful', 'failed', 'cancelled']:
        desired_status = 'successful'
    
    if payment.status in ['pending', 'processing']:
        payment.status = desired_status
        payment.processed_at = timezone.now()
        payment.save()
        payment.log('info', f'Payment manually completed via API to {desired_status}')
        
        return Response({
            'success': True,
            'message': f'Payment {desired_status} successfully',
            'payment': PaymentSerializer(payment).data
        })
    else:
        return Response({
            'success': False,
            'message': f'Payment is already {payment.status}',
            'payment': PaymentSerializer(payment).data
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_payment_methods(request):
    """Get available payment methods for checkout"""
    
    # Get active providers
    active_providers = PaymentProvider.objects.filter(is_active=True)
    
    payment_methods = [
        {
            "id": "mobile_money",
            "name": "Mobile Money",
            "description": "MTN, Vodafone, AirtelTigo",
            "icon": "📱",
            "processing_time": "Instant",
            "currencies": ["GHS"],
            "providers": [
                {
                    "id": provider.id,
                    "name": provider.name,
                    "code": provider.code
                } for provider in active_providers.filter(code__in=['mtn_momo', 'vodafone_cash', 'airteltigo_money'])
            ]
        },
        {
            "id": "card",
            "name": "Credit/Debit Card",
            "description": "Visa, Mastercard, American Express",
            "icon": "💳",
            "processing_time": "Instant",
            "currencies": ["GHS", "USD", "EUR"],
            "providers": [
                {
                    "id": provider.id,
                    "name": provider.name,
                    "code": provider.code
                } for provider in active_providers.filter(code__in=['stripe', 'paystack'])
            ]
        },
        {
            "id": "bank_transfer",
            "name": "Bank Transfer",
            "description": "For large groups (optional)",
            "icon": "🏦",
            "processing_time": "1-2 days",
            "currencies": ["GHS", "USD"],
            "providers": []
        }
    ]
    
    # Filter out methods with no active providers (except bank transfer)
    available_methods = []
    for method in payment_methods:
        if method["id"] == "bank_transfer" or method["providers"]:
            available_methods.append(method)
    
    return Response({
        "payment_methods": available_methods,
        "default_currency": "GHS",
        "supported_currencies": ["GHS", "USD", "EUR"]
    })

@api_view(['POST'])
@permission_classes([AllowAny])  # Changed for demo purposes
def checkout_payment(request):
    """Create payment during checkout process"""
    serializer = CheckoutPaymentSerializer(data=request.data)
    
    if not serializer.is_valid():
        logger.error(f"Checkout payment validation failed: {serializer.errors}")
        logger.error(f"Request data: {request.data}")
        return Response({
            'success': False,
            'error': 'Validation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    validated_data = serializer.validated_data
    provider = validated_data.pop('provider')
    
    try:
        # Generate unique reference
        reference = generate_payment_reference()
        
        # Get booking if provided
        booking = None
        booking_id = validated_data.get('booking_id')
        if booking_id and request.user.is_authenticated:
            from destinations.models import Booking
            try:
                booking = Booking.objects.get(id=booking_id, user=request.user)
            except Booking.DoesNotExist:
                return Response(
                    {'error': 'Booking not found or does not belong to you'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create payment (handle anonymous users for demo)
        user = request.user if request.user.is_authenticated else None
        payment = Payment.objects.create(
            user=user,
            reference=reference,
            amount=validated_data['amount'],
            currency=validated_data['currency'],
            payment_method=validated_data['payment_method'],
            provider=provider,
            phone_number=validated_data.get('phone_number', ''),
            description=validated_data.get('description', ''),
            booking=booking
        )
        
        # Store appropriate booking details in payment metadata for admin display
        try:
            booking_data = request.data.get('booking_details', {})
            logger.info(f"Received booking_details from frontend: {booking_data}")
            
            # Check if this is a ticket payment
            is_ticket_payment = (
                payment.description and "Ticket Purchase:" in payment.description
            ) or (booking_data and booking_data.get('type') == 'ticket')
            
            if is_ticket_payment:
                # Use ticket-specific details storage
                from .signals import store_ticket_details_in_payment
                store_ticket_details_in_payment(payment)
                logger.info(f"Stored ticket details for payment {payment.reference}")
            elif booking_data:
                # Convert frontend booking data to backend format for destinations
                from .booking_utils import store_booking_details_in_payment
                logger.info(f"Converting frontend booking data for payment {payment.reference}")
                converted_data = convert_frontend_booking_data(booking_data, payment)
                logger.info(f"Converted data: {converted_data}")
                store_booking_details_in_payment(payment, converted_data)
                logger.info(f"Stored real-time booking details for payment {payment.reference}")
                logger.info(f"Final metadata: {payment.metadata}")
            elif booking:
                # Extract details from booking model (if available)
                from .booking_utils import store_booking_details_in_payment, create_sample_booking_details
                sample_data = create_sample_booking_details()
                sample_data['final_total'] = float(payment.amount)
                sample_data['base_total'] = float(payment.amount) * 0.7
                sample_data['options_total'] = float(payment.amount) * 0.3
                store_booking_details_in_payment(payment, sample_data)
                logger.info(f"Stored booking model details for payment {payment.reference}")
            else:
                # For demo purposes, add sample destination booking details
                from .booking_utils import store_booking_details_in_payment, create_sample_booking_details
                sample_data = create_sample_booking_details()
                sample_data['final_total'] = float(payment.amount)
                sample_data['base_total'] = float(payment.amount) * 0.7
                sample_data['options_total'] = float(payment.amount) * 0.3
                store_booking_details_in_payment(payment, sample_data)
                logger.info(f"Stored sample booking details for payment {payment.reference}")
        except Exception as e:
            logger.error(f"Failed to store booking details for payment {payment.reference}: {str(e)}")
            logger.exception(e)
            # Continue with payment creation even if booking details fail
        
        # Handle different payment methods
        if provider.code == 'paystack':
            # For Paystack, just create the payment record
            # Initialization will be done separately via /paystack/initialize/
            payment.status = 'pending'
            payment.save()
            payment.log('info', 'Payment created, awaiting Paystack initialization')
            
            return Response({
                'success': True,
                'payment': PaymentSerializer(payment).data,
                'message': 'Payment created successfully'
            }, status=status.HTTP_201_CREATED)
            
        elif provider.code == 'stripe':
            # For Stripe, create a Payment Intent
            from stripe_payments.services import StripeService
            stripe_service = StripeService()
            
            stripe_result = stripe_service.create_payment_intent(
                user=request.user,
                amount=float(validated_data['amount']),
                currency=validated_data['currency'],
                booking=booking,
                description=validated_data.get('description', ''),
                metadata={'payment_reference': payment.reference}
            )
            
            if stripe_result['success']:
                payment.external_reference = stripe_result['payment_intent'].stripe_payment_intent_id
                payment.status = 'processing'
                payment.save()
                
                return Response({
                    'success': True,
                    'payment': PaymentSerializer(payment).data,
                    'stripe': {
                        'client_secret': stripe_result['client_secret'],
                        'publishable_key': stripe_result['publishable_key']
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                payment.status = 'failed'
                payment.save()
                return Response({
                    'success': False,
                    'error': stripe_result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            # For other providers (MTN MoMo, etc.)
            # For demo purposes, simulate successful initiation
            if provider.code in ['mtn_momo', 'vodafone_cash', 'airteltigo_money']:
                # Simulate successful mobile money initiation
                payment.external_reference = f"DEMO_{payment.reference}"
                payment.status = 'processing'
                payment.save()
                payment.log('info', 'Demo payment initiated successfully')
                
                # Start auto-completion for demo purposes
                booking_details = request.data.get('booking_details', {})
                if booking_details.get('type') == 'ticket':
                    # For ticket payments, auto-complete after 5 seconds with high success rate
                    auto_complete_payment_after_delay(payment.reference, delay_seconds=5, success_rate=0.99)
                    logger.info(f"Started auto-completion for ticket payment {payment.reference} (5s delay)")
                else:
                    # For other payments, auto-complete after 15 seconds
                    auto_complete_payment_after_delay(payment.reference, delay_seconds=15, success_rate=0.95)
                    logger.info(f"Started auto-completion for payment {payment.reference} (15s delay)")
                
                return Response({
                    'success': True,
                    'payment': PaymentSerializer(payment).data,
                    'message': 'Payment request sent to your phone. Please authorize on your device.'
                }, status=status.HTTP_201_CREATED)
            else:
                # Try actual payment service for other providers
                payment_service = PaymentService()
                result = payment_service.initiate_payment(payment)
                
                if result.get('success'):
                    payment.external_reference = result.get('external_reference', '')
                    payment.status = 'processing'
                    payment.save()
                    payment.log('info', 'Payment initiated successfully', result)
                    
                    return Response({
                        'success': True,
                        'payment': PaymentSerializer(payment).data,
                        'message': result.get('message', 'Payment initiated successfully')
                    }, status=status.HTTP_201_CREATED)
                else:
                    payment.status = 'failed'
                    payment.save()
                    payment.log('error', 'Payment initiation failed', result)
                    
                    return Response({
                        'success': False,
                        'error': result.get('message', 'Payment initiation failed')
                    }, status=status.HTTP_400_BAD_REQUEST)
                
    except Exception as e:
        logger.error(f"Checkout payment error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while processing your payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def mtn_momo_webhook(request):
    """Handle MTN Mobile Money webhook notifications"""
    try:
        webhook_data = request.data
        logger.info(f"MTN MoMo webhook received: {webhook_data}")
        
        # Process webhook with MTN MoMo service
        mtn_service = MTNMoMoService()
        result = mtn_service.process_webhook(webhook_data)
        
        if result.get('success'):
            external_id = result.get('external_id')
            new_status = result.get('status')
            
            # Find payment by reference (external_id should match our payment reference)
            try:
                payment = Payment.objects.get(reference=external_id)
                
                # Update payment status if changed
                if payment.status != new_status:
                    old_status = payment.status
                    payment.status = new_status
                    
                    if new_status in ['successful', 'failed', 'cancelled']:
                        payment.processed_at = timezone.now()
                    
                    payment.save()
                    payment.log('info', f'Status updated via MTN webhook: {old_status} -> {new_status}', result)
                    
                    logger.info(f"Payment {payment.reference} status updated: {old_status} -> {new_status}")
                
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
                
            except Payment.DoesNotExist:
                logger.warning(f"Payment not found for MTN webhook: {external_id}")
                return Response({'status': 'payment_not_found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error(f"MTN webhook processing failed: {result.get('error')}")
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"MTN MoMo webhook error: {str(e)}")
        return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
@permission_classes([AllowAny])
def simulate_payment_authorization(request, reference):
    """Simulate payment authorization for demo purposes"""
    try:
        payment = get_object_or_404(Payment, reference=reference)
        
        if payment.status in ['pending', 'processing']:
            # Simulate random success/failure (90% success rate)
            import random
            if random.random() > 0.1:  # 90% success rate
                payment.status = 'successful'
                payment.processed_at = timezone.now()
                payment.save()
                payment.log('info', 'Payment completed via demo authorization')
                
                return Response({
                    'success': True,
                    'message': 'Payment authorized successfully',
                    'payment': PaymentSerializer(payment).data
                })
            else:
                payment.status = 'failed'
                payment.save()
                payment.log('info', 'Payment failed via demo authorization')
                
                return Response({
                    'success': False,
                    'message': 'Payment authorization failed',
                    'payment': PaymentSerializer(payment).data
                })
        else:
            return Response({
                'success': False,
                'message': f'Payment is already {payment.status}',
                'payment': PaymentSerializer(payment).data
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Payment authorization simulation error: {str(e)}")
        return Response({
            'success': False,
            'message': 'Error simulating payment authorization'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def force_complete_payment(request, reference):
    """Force complete a stuck payment (for troubleshooting)"""
    try:
        payment = get_object_or_404(Payment, reference=reference)
        
        # Allow forcing completion regardless of current status
        desired_status = request.data.get('status', 'successful')
        if desired_status not in ['successful', 'failed', 'cancelled']:
            desired_status = 'successful'
        
        old_status = payment.status
        payment.status = desired_status
        payment.processed_at = timezone.now()
        payment.save()
        payment.log('info', f'Payment force completed via API: {old_status} -> {desired_status}')
        
        return Response({
            'success': True,
            'message': f'Payment force completed: {old_status} -> {desired_status}',
            'payment': PaymentSerializer(payment).data
        })
            
    except Exception as e:
        logger.error(f"Force payment completion error: {str(e)}")
        return Response({
            'success': False,
            'message': 'Error force completing payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def auto_complete_payment_after_delay(payment_reference, delay_seconds=30, success_rate=0.9):
    """
    Background task to auto-complete a payment after a delay (for demo purposes)
    """
    def complete_payment_task():
        try:
            # Import Django modules inside the thread to ensure proper setup
            from django.db import connection
            from django.utils import timezone
            import random
            
            # Wait for the specified delay
            time.sleep(delay_seconds)
            
            # Close any existing database connections to avoid issues
            connection.close()
            
            # Get the payment and check if it's still pending
            try:
                payment = Payment.objects.get(reference=payment_reference)
                
                if payment.status in ['pending', 'processing']:
                    # Simulate success/failure based on success rate
                    if random.random() < success_rate:
                        # Success
                        payment.status = 'successful'
                        payment.processed_at = timezone.now()
                        payment.save()
                        payment.log('info', f'Auto-completed successfully after {delay_seconds}s delay')
                        logger.info(f"Auto-completed payment {payment_reference} successfully")
                    else:
                        # Failure
                        payment.status = 'failed'
                        payment.processed_at = timezone.now()
                        payment.save()
                        payment.log('info', f'Auto-failed after {delay_seconds}s delay')
                        logger.info(f"Auto-failed payment {payment_reference}")
                else:
                    logger.info(f"Payment {payment_reference} already processed, skipping auto-completion")
                    
            except Payment.DoesNotExist:
                logger.warning(f"Payment {payment_reference} not found for auto-completion")
                
        except Exception as e:
            logger.error(f"Error in auto-completion task for {payment_reference}: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
        finally:
            # Ensure database connection is closed
            try:
                from django.db import connection
                connection.close()
            except:
                pass
    
    # Start the background task
    thread = threading.Thread(target=complete_payment_task, daemon=True)
    thread.start()
    logger.info(f"Started auto-completion task for payment {payment_reference} (delay: {delay_seconds}s)")

@api_view(['POST'])
@permission_classes([AllowAny])
def create_paystack_provider_endpoint(request):
    """
    Manually create Paystack provider (for setup)
    """
    try:
        provider, created = PaymentProvider.objects.update_or_create(
            code='paystack',
            defaults={
                'name': 'Paystack',
                'is_active': True,
                'config': {
                    'supports_cards': True,
                    'supports_mobile_money': True,
                    'supports_bank_transfer': True,
                    'supports_ussd': True,
                    'currencies': ['GHS', 'NGN', 'USD', 'ZAR', 'KES'],
                }
            }
        )
        
        return Response({
            'success': True,
            'message': 'Created Paystack provider' if created else 'Updated Paystack provider',
            'provider': {
                'id': provider.id,
                'code': provider.code,
                'name': provider.name,
                'is_active': provider.is_active
            }
        })
    except Exception as e:
        logger.error(f"Error creating Paystack provider: {str(e)}")
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def start_demo_auto_completion(request, reference):
    """
    Manually start auto-completion for a payment (for testing)
    """
    try:
        payment = get_object_or_404(Payment, reference=reference)
        
        if payment.status in ['pending', 'processing']:
            delay_seconds = request.data.get('delay_seconds', 30)
            success_rate = request.data.get('success_rate', 0.9)
            
            # Start auto-completion
            auto_complete_payment_after_delay(payment.reference, delay_seconds, success_rate)
            
            return Response({
                'success': True,
                'message': f'Auto-completion started for payment {reference}',
                'delay_seconds': delay_seconds,
                'success_rate': success_rate
            })
        else:
            return Response({
                'success': False,
                'message': f'Payment is already {payment.status}'
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Error starting auto-completion for {reference}: {str(e)}")
        return Response({
            'success': False,
            'message': 'Error starting auto-completion'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['GET'])
@permission_classes([AllowAny])
def debug_payments(request):
    """Debug endpoint to list recent payments"""
    from django.utils import timezone
    from datetime import timedelta
    
    recent_payments = Payment.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-created_at')[:20]
    
    payments_data = []
    for payment in recent_payments:
        payments_data.append({
            'reference': payment.reference,
            'status': payment.status,
            'amount': str(payment.amount),
            'currency': payment.currency,
            'created_at': payment.created_at.isoformat(),
            'phone_number': payment.phone_number[-4:] if payment.phone_number else None,  # Last 4 digits only
        })
    
    return Response({
        'total_payments': Payment.objects.count(),
        'recent_payments_24h': recent_payments.count(),
        'payments': payments_data
    })

def schedule_auto_completion_via_command(payment_reference, delay_seconds=30):
    """
    Alternative approach using management command (more reliable)
    """
    import subprocess
    import os
    
    def run_command():
        try:
            time.sleep(delay_seconds)
            # Run the management command
            result = subprocess.run([
                'python', 'manage.py', 'auto_complete_demo_payments',
                '--timeout', '0',  # Process immediately
                '--success-rate', '0.9'
            ], cwd=os.path.dirname(os.path.dirname(__file__)), capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Auto-completion command completed for {payment_reference}")
            else:
                logger.error(f"Auto-completion command failed: {result.stderr}")
                
        except Exception as e:
            logger.error(f"Error running auto-completion command: {str(e)}")
    
    # Start the background task
    thread = threading.Thread(target=run_command, daemon=True)
    thread.start()
    logger.info(f"Scheduled auto-completion command for payment {payment_reference} (delay: {delay_seconds}s)")

@api_view(['POST'])
@permission_classes([AllowAny])
def add_booking_details_to_payment(request, reference):
    """
    API endpoint to add booking details to a payment
    """
    try:
        payment = get_object_or_404(Payment, reference=reference)
        
        # Check if booking details already exist
        if payment.metadata and 'booking_details' in payment.metadata:
            return Response({
                'success': True,
                'message': 'Booking details already exist',
                'payment': PaymentSerializer(payment).data
            })
        
        # Add booking details
        from .booking_utils import store_booking_details_in_payment, create_sample_booking_details
        
        sample_data = create_sample_booking_details()
        sample_data['final_total'] = float(payment.amount)
        sample_data['base_total'] = float(payment.amount) * 0.65
        sample_data['options_total'] = float(payment.amount) * 0.35
        
        # Customize based on description and amount
        description = payment.description or ""
        amount = float(payment.amount) if payment.amount else 0
        
        # Smart destination detection
        if "elmina" in description.lower():
            sample_data['destination_name'] = 'Elmina Castle & Beach Resort'
            sample_data['destination_location'] = 'Central Region, Ghana'
            sample_data['duration'] = '2 Days / 1 Night'
            sample_data['adults'] = 2
            sample_data['children'] = 1
        elif "akosombo" in description.lower() or "dodi" in description.lower():
            sample_data['destination_name'] = 'Akosombo Dodi Island Boat Cruise'
            sample_data['destination_location'] = 'Eastern Region, Ghana'
            sample_data['duration'] = '1 Day Trip'
        elif "kakum" in description.lower():
            sample_data['destination_name'] = 'Kakum National Park Adventure'
            sample_data['destination_location'] = 'Central Region, Ghana'
            sample_data['duration'] = '2 Days / 1 Night'
        elif "cape coast" in description.lower():
            sample_data['destination_name'] = 'Cape Coast Castle Heritage Tour'
            sample_data['destination_location'] = 'Cape Coast, Ghana'
            sample_data['duration'] = '3 Days / 2 Nights'
        elif amount >= 1000:
            sample_data['destination_name'] = 'Northern Ghana Safari Experience'
            sample_data['destination_location'] = 'Northern Region, Ghana'
            sample_data['duration'] = '5 Days / 4 Nights'
            sample_data['adults'] = 3
            sample_data['children'] = 2
        elif amount >= 500:
            sample_data['destination_name'] = 'Cape Coast Castle Heritage Tour'
            sample_data['destination_location'] = 'Cape Coast, Ghana'
            sample_data['duration'] = '3 Days / 2 Nights'
            sample_data['adults'] = 2
            sample_data['children'] = 1
        elif amount >= 100:
            sample_data['destination_name'] = 'Kakum National Park Adventure'
            sample_data['destination_location'] = 'Central Region, Ghana'
            sample_data['duration'] = '2 Days / 1 Night'
            sample_data['adults'] = 2
            sample_data['children'] = 0
        else:
            sample_data['destination_name'] = 'Local Cultural Experience'
            sample_data['destination_location'] = 'Accra, Ghana'
            sample_data['duration'] = '1 Day'
            sample_data['adults'] = 1
            sample_data['children'] = 0
        
        # Use actual user info if available
        if payment.user:
            user_name = f"{payment.user.first_name} {payment.user.last_name}".strip()
            if not user_name:
                user_name = payment.user.username or "User"
            sample_data['user_name'] = user_name
            sample_data['user_email'] = payment.user.email or ''
        
        # Use actual phone number
        if payment.phone_number:
            sample_data['user_phone'] = payment.phone_number
        
        # Store the booking details
        store_booking_details_in_payment(payment, sample_data)
        
        logger.info(f"Added booking details to payment {payment.reference} via API")
        
        return Response({
            'success': True,
            'message': 'Booking details added successfully',
            'payment': PaymentSerializer(payment).data
        })
        
    except Exception as e:
        logger.error(f"Error adding booking details to payment {reference}: {str(e)}")
        return Response({
            'success': False,
            'message': f'Error adding booking details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def ensure_all_booking_details(request):
    """
    API endpoint to ensure all payments have booking details
    """
    try:
        # Find payments without booking details
        payments_without_details = []
        for payment in Payment.objects.all():
            if not payment.metadata or 'booking_details' not in payment.metadata:
                payments_without_details.append(payment)
        
        if not payments_without_details:
            return Response({
                'success': True,
                'message': 'All payments already have booking details',
                'updated_count': 0
            })
        
        # Add booking details to each payment
        updated_count = 0
        for payment in payments_without_details:
            try:
                # Use the same logic as the individual endpoint
                from .booking_utils import store_booking_details_in_payment, create_sample_booking_details
                
                sample_data = create_sample_booking_details()
                sample_data['final_total'] = float(payment.amount)
                sample_data['base_total'] = float(payment.amount) * 0.65
                sample_data['options_total'] = float(payment.amount) * 0.35
                
                # Customize based on amount
                amount = float(payment.amount) if payment.amount else 0
                if amount >= 1000:
                    sample_data['destination_name'] = 'Northern Ghana Safari Experience'
                    sample_data['destination_location'] = 'Northern Region, Ghana'
                    sample_data['duration'] = '5 Days / 4 Nights'
                    sample_data['adults'] = 3
                    sample_data['children'] = 2
                elif amount >= 500:
                    sample_data['destination_name'] = 'Cape Coast Castle Heritage Tour'
                    sample_data['destination_location'] = 'Cape Coast, Ghana'
                    sample_data['duration'] = '3 Days / 2 Nights'
                    sample_data['adults'] = 2
                    sample_data['children'] = 1
                elif amount >= 100:
                    sample_data['destination_name'] = 'Kakum National Park Adventure'
                    sample_data['destination_location'] = 'Central Region, Ghana'
                    sample_data['duration'] = '2 Days / 1 Night'
                    sample_data['adults'] = 2
                    sample_data['children'] = 0
                else:
                    sample_data['destination_name'] = 'Local Cultural Experience'
                    sample_data['destination_location'] = 'Accra, Ghana'
                    sample_data['duration'] = '1 Day'
                    sample_data['adults'] = 1
                    sample_data['children'] = 0
                
                # Use actual user info if available
                if payment.user:
                    user_name = f"{payment.user.first_name} {payment.user.last_name}".strip()
                    if not user_name:
                        user_name = payment.user.username or "User"
                    sample_data['user_name'] = user_name
                    sample_data['user_email'] = payment.user.email or ''
                
                # Use actual phone number
                if payment.phone_number:
                    sample_data['user_phone'] = payment.phone_number
                
                # Store the booking details
                store_booking_details_in_payment(payment, sample_data)
                updated_count += 1
                
            except Exception as e:
                logger.error(f"Failed to add booking details to payment {payment.reference}: {str(e)}")
        
        return Response({
            'success': True,
            'message': f'Added booking details to {updated_count} payments',
            'updated_count': updated_count
        })
        
    except Exception as e:
        logger.error(f"Error in ensure_all_booking_details: {str(e)}")
        return Response({
            'success': False,
            'message': f'Error ensuring booking details: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def convert_frontend_booking_data(frontend_data, payment):
    """
    Convert frontend booking data to backend booking details format
    Handles the actual structure sent from Booking.tsx
    """
    try:
        logger.info(f"Converting frontend booking data: {frontend_data}")
        
        # Extract data from the actual frontend structure
        destination = frontend_data.get('destination', {})
        travelers = frontend_data.get('travelers', {})
        selected_options = frontend_data.get('selected_options', {})
        pricing = frontend_data.get('pricing', {})
        user_info = frontend_data.get('user_info', {})
        
        # Build backend format
        backend_data = {
            'user_name': user_info.get('name', 'Guest User'),
            'user_email': user_info.get('email', ''),
            'user_phone': user_info.get('phone', payment.phone_number or ''),
            'destination_name': destination.get('name', 'Tour Booking'),
            'destination_location': destination.get('location', 'Ghana'),
            'duration': destination.get('duration', '1 Day'),
            'base_price': 0,  # Will be calculated from pricing
            'adults': travelers.get('adults', 0),
            'children': travelers.get('children', 0),
            'selected_date': frontend_data.get('selected_date', ''),
            'base_total': pricing.get('base_total', 0),
            'options_total': pricing.get('options_total', 0),
            'final_total': pricing.get('final_total', float(payment.amount)),
        }
        
        # Override with payment user info if available
        if payment.user:
            user_name = f"{payment.user.first_name} {payment.user.last_name}".strip()
            if not user_name:
                user_name = payment.user.username or payment.user.email.split('@')[0] if payment.user.email else "User"
            backend_data['user_name'] = user_name
            backend_data['user_email'] = payment.user.email or ''
        
        # Process selected options from frontend
        accommodation = selected_options.get('accommodation', {})
        if accommodation:
            backend_data['accommodation'] = {
                'name': accommodation.get('name', 'Standard Accommodation'),
                'price': accommodation.get('price', 0),
                'is_default': accommodation.get('isDefault', False)
            }
        
        transport = selected_options.get('transport', {})
        if transport:
            backend_data['transport'] = {
                'name': transport.get('name', 'Standard Transport'),
                'price': transport.get('price', 0),
                'is_default': transport.get('isDefault', False)
            }
        
        meals = selected_options.get('meals', {})
        if meals:
            backend_data['meals'] = {
                'name': meals.get('name', 'Standard Meals'),
                'price': meals.get('price', 0),
                'is_default': meals.get('isDefault', False)
            }
        
        # Add medical/insurance if available
        medical = selected_options.get('medical', {})
        if medical:
            backend_data['medical'] = {
                'name': medical.get('name', 'Basic Coverage'),
                'price': medical.get('price', 0),
                'is_default': medical.get('isDefault', False)
            }
        
        # Add experiences if available
        experiences = selected_options.get('experiences', [])
        if experiences:
            backend_data['experiences'] = [
                {
                    'name': exp.get('name', 'Experience'),
                    'price': exp.get('price', 0)
                }
                for exp in experiences
            ]
        
        logger.info(f"Converted booking data: {backend_data}")
        return backend_data
        
    except Exception as e:
        logger.error(f"Error converting frontend booking data: {str(e)}")
        logger.exception(e)
        # Return sample data as fallback
        from .booking_utils import create_sample_booking_details
        sample_data = create_sample_booking_details()
        sample_data['final_total'] = float(payment.amount)
        return sample_data

# Paystack Integration Views
from .paystack_service import PaystackService
import json

@api_view(['POST'])
@permission_classes([AllowAny])
def paystack_initialize_payment(request):
    """Initialize a Paystack payment"""
    try:
        # Get payment reference from request
        reference = request.data.get('reference')
        if not reference:
            return Response({
                'success': False,
                'error': 'Payment reference is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get payment
        try:
            payment = Payment.objects.get(reference=reference)
        except Payment.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Payment not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Initialize with Paystack
        paystack_service = PaystackService()
        callback_url = request.data.get('callback_url')
        
        result = paystack_service.initialize_payment(payment, callback_url)
        
        if result['success']:
            return Response({
                'success': True,
                'data': result['data'],
                'authorization_url': result['authorization_url'],
                'access_code': result['access_code'],
                'reference': result['reference']
            })
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Paystack initialization error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while initializing payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def paystack_verify_payment(request, reference):
    """Verify a Paystack payment"""
    try:
        paystack_service = PaystackService()
        result = paystack_service.verify_payment(reference)
        
        if result['success']:
            # Update local payment status
            try:
                payment = Payment.objects.get(reference=reference)
                transaction_data = result['data']
                
                if transaction_data['status'] == 'success':
                    payment.status = 'successful'
                    payment.processed_at = timezone.now()
                elif transaction_data['status'] == 'failed':
                    payment.status = 'failed'
                    payment.processed_at = timezone.now()
                
                payment.metadata.update({
                    'paystack_verification': transaction_data
                })
                payment.save()
                
                payment.log('info', 'Payment verified with Paystack', transaction_data)
                
            except Payment.DoesNotExist:
                logger.warning(f"Payment not found for verification: {reference}")
            
            return Response({
                'success': True,
                'data': result['data']
            })
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Paystack verification error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while verifying payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def paystack_webhook(request):
    """Handle Paystack webhook"""
    try:
        # Get signature from headers
        signature = request.META.get('HTTP_X_PAYSTACK_SIGNATURE', '')
        
        if not signature:
            logger.warning("Paystack webhook received without signature")
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Process webhook
        paystack_service = PaystackService()
        result = paystack_service.handle_webhook(request.data, signature)
        
        if result['success']:
            return Response({'status': 'success'})
        else:
            return Response({'status': 'error'}, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Paystack webhook error: {str(e)}")
        return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def paystack_refund_payment(request, reference):
    """Refund a Paystack payment"""
    try:
        # Get payment
        payment = get_object_or_404(
            Payment, 
            reference=reference, 
            user=request.user,
            status='successful'
        )
        
        # Get refund details
        amount = request.data.get('amount')
        reason = request.data.get('reason', 'Customer request')
        
        if amount:
            try:
                amount = Decimal(str(amount))
                if amount <= 0 or amount > payment.amount:
                    return Response({
                        'success': False,
                        'error': 'Invalid refund amount'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except (ValueError, TypeError):
                return Response({
                    'success': False,
                    'error': 'Invalid amount format'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Process refund
        paystack_service = PaystackService()
        result = paystack_service.refund_payment(payment, amount, reason)
        
        if result['success']:
            return Response({
                'success': True,
                'data': result['data'],
                'message': 'Refund processed successfully'
            })
        else:
            return Response({
                'success': False,
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Paystack refund error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while processing refund'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def convert_frontend_booking_data(booking_data, payment):
    """Convert frontend booking data to backend format"""
    try:
        # Extract basic info
        converted = {
            'destination_name': booking_data.get('destination', {}).get('name', 'Unknown Destination'),
            'package_name': booking_data.get('package', {}).get('name', 'Standard Package'),
            'start_date': booking_data.get('dates', {}).get('start', ''),
            'end_date': booking_data.get('dates', {}).get('end', ''),
            'duration_days': booking_data.get('duration', 1),
            'group_size': booking_data.get('groupSize', 1),
            'base_price': float(booking_data.get('basePrice', 0)),
            'final_total': float(payment.amount),
            'currency': payment.currency,
            'booking_type': booking_data.get('type', 'destination')
        }
        
        # Add participants if available
        participants = booking_data.get('participants', [])
        if participants:
            converted['participants'] = participants
            converted['participant_count'] = len(participants)
        
        # Add selected options
        options = booking_data.get('selectedOptions', [])
        if options:
            converted['selected_options'] = options
            converted['options_total'] = sum(opt.get('price', 0) for opt in options)
        
        return converted
        
    except Exception as e:
        logger.error(f"Error converting frontend booking data: {str(e)}")
        return {
            'destination_name': 'Unknown Destination',
            'final_total': float(payment.amount),
            'currency': payment.currency,
            'error': 'Failed to parse booking data'
        }