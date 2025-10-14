"""
Paystack-specific payment views
"""
import logging
import json
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse

from .models import Payment, PaymentProvider
from .serializers import PaymentSerializer
from .paystack_service import PaystackService
from .utils import generate_payment_reference
from .test_mode_views import simulate_test_payment_success

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_paystack_payment(request):
    """Create a new Paystack payment (both card and mobile money)"""
    try:
        data = request.data
        
        # Debug: Log the received data
        logger.info(f"Received payment request data: {data}")
        
        # Validate required fields
        required_fields = ['amount', 'email', 'payment_method']
        for field in required_fields:
            if not data.get(field):
                return Response({
                    'success': False,
                    'error': f'{field} is required'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Get or create Paystack provider
        provider, created = PaymentProvider.objects.get_or_create(
            code='paystack',
            defaults={
                'name': 'Paystack Ghana',
                'is_active': True,
                'configuration': {
                    'supports_mobile_money': True,
                    'supports_cards': True,
                    'currency': 'GHS'
                }
            }
        )
        
        # Generate payment reference
        reference = generate_payment_reference()
        
        # Create payment record
        user = request.user if request.user.is_authenticated else None
        payment = Payment.objects.create(
            user=user,
            reference=reference,
            amount=data['amount'],
            currency=data.get('currency', 'GHS'),
            payment_method=data['payment_method'],
            provider=provider,
            phone_number=data.get('phone_number', ''),
            description=data.get('description', 'Payment via Paystack')
        )
        
        # Store booking details if provided
        logger.info(f"Checking for booking_details in request data: {'booking_details' in data}")
        if 'booking_details' in data:
            logger.info(f"Booking details found: {data['booking_details']}")
            
        if 'booking_details' in data and data['booking_details']:
            try:
                from .booking_details_utils import add_booking_details_to_payment
                add_booking_details_to_payment(payment, data['booking_details'])
                payment.log('info', 'Booking details stored from request', data['booking_details'])
                logger.info(f"Successfully stored booking details for payment {payment.reference}")
            except Exception as e:
                logger.error(f"Failed to store booking details for payment {payment.reference}: {str(e)}")
                payment.log('error', f'Failed to store booking details: {str(e)}', data.get('booking_details', {}))
        else:
            logger.info(f"No booking details to store for payment {payment.reference}")
        
        # Initialize Paystack service
        paystack_service = PaystackService()
        
        # Prepare payment data for Paystack
        payment_data = {
            'amount': data['amount'],
            'email': data['email'],
            'reference': reference,
            'currency': data.get('currency', 'GHS'),
            'payment_method': data['payment_method'],
            'phone_number': data.get('phone_number', ''),
            'description': data.get('description', 'Payment via Paystack'),
            'callback_url': f"{settings.BASE_URL}/api/payments/paystack/callback/"
        }
        
        # Handle different payment methods
        if data['payment_method'] == 'mobile_money':
            # For MoMo payments, use standard Paystack checkout (will redirect to Paystack website)
            # This allows testing with test cards and ensures payments appear in Paystack dashboard
            payment_data['channels'] = ['card', 'mobile_money']  # Allow both for flexibility
            payment_data['provider'] = data.get('provider', 'mtn')  # mtn, vodafone, airteltigo
            
            result = paystack_service.initialize_payment(payment_data)
        else:
            # Card payment
            result = paystack_service.initialize_payment(payment_data)
        
        if result['success']:
            # Update payment with Paystack data
            payment.external_reference = result.get('reference', reference)
            payment.status = 'processing'
            
            # Merge Paystack data with existing metadata (preserve booking details)
            if not payment.metadata:
                payment.metadata = {}
            
            payment.metadata.update({
                'paystack_data': result.get('data', {}),
                'authorization_url': result.get('authorization_url', ''),
                'access_code': result.get('access_code', '')
            })
            payment.save()
            payment.log('info', 'Paystack payment initialized successfully', result)
            
            return Response({
                'success': True,
                'payment': PaymentSerializer(payment).data,
                'paystack': {
                    'authorization_url': result.get('authorization_url', ''),
                    'access_code': result.get('access_code', ''),
                    'reference': result.get('reference', reference),
                    'display_text': result.get('display_text', 'Please complete payment')
                },
                'message': 'Payment initialized successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            # Payment initialization failed
            payment.status = 'failed'
            payment.save()
            payment.log('error', 'Paystack payment initialization failed', result)
            
            return Response({
                'success': False,
                'error': result.get('error', 'Payment initialization failed')
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Paystack payment creation error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while creating the payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_paystack_payment(request, reference):
    """Verify Paystack payment status"""
    try:
        payment = get_object_or_404(Payment, reference=reference)
        
        # In test mode, if payment is already successful locally, don't override with Paystack
        from django.conf import settings
        public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
        is_test_mode = public_key.startswith('pk_test_')
        
        if is_test_mode and payment.status == 'successful':
            # Return local status without calling Paystack
            return Response({
                'success': True,
                'payment': PaymentSerializer(payment).data,
                'test_mode': True,
                'message': 'Using local test mode status'
            })
        
        # Initialize Paystack service
        paystack_service = PaystackService()
        
        # Verify payment with Paystack
        result = paystack_service.verify_payment(reference)
        
        if result['success']:
            # Update payment status based on Paystack response
            paystack_status = result['status']
            
            # Map Paystack status to our internal status
            status_map = {
                'success': 'successful',
                'failed': 'failed',
                'abandoned': 'cancelled',
                'pending': 'processing'
            }
            
            new_status = status_map.get(paystack_status, 'processing')
            
            # In test mode, don't override successful status with failed/cancelled
            if is_test_mode and payment.status == 'successful' and new_status in ['failed', 'cancelled']:
                # Keep the successful status
                pass
            elif payment.status != new_status:
                old_status = payment.status
                payment.status = new_status
                
                if new_status in ['successful', 'failed', 'cancelled']:
                    from django.utils import timezone
                    payment.processed_at = timezone.now()
                
                payment.save()
                payment.log('info', f'Payment status updated via verification: {old_status} -> {new_status}', result)
            
            return Response({
                'success': True,
                'payment': PaymentSerializer(payment).data,
                'paystack_data': result['data'],
                'test_mode': is_test_mode
            })
        else:
            payment.log('warning', 'Payment verification failed', result)
            return Response({
                'success': False,
                'error': result.get('error', 'Payment verification failed'),
                'payment': PaymentSerializer(payment).data
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Paystack payment verification error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while verifying the payment'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def paystack_webhook(request):
    """Handle Paystack webhook notifications"""
    try:
        # Get the raw body for signature verification
        payload = request.body
        
        # Parse JSON data
        try:
            webhook_data = json.loads(payload.decode('utf-8'))
        except json.JSONDecodeError:
            logger.error("Invalid JSON in Paystack webhook")
            return HttpResponse(status=400)
        
        # Log webhook received
        logger.info(f"Paystack webhook received: {webhook_data.get('event', 'unknown')}")
        
        # Process webhook with Paystack service
        paystack_service = PaystackService()
        result = paystack_service.process_webhook(webhook_data)
        
        if result['success']:
            reference = result.get('reference')
            new_status = result.get('status')
            
            if reference:
                try:
                    payment = Payment.objects.get(reference=reference)
                    
                    # Update payment status if changed
                    if payment.status != new_status:
                        old_status = payment.status
                        payment.status = new_status
                        
                        if new_status in ['successful', 'failed', 'cancelled']:
                            from django.utils import timezone
                            payment.processed_at = timezone.now()
                        
                        payment.save()
                        payment.log('info', f'Status updated via Paystack webhook: {old_status} -> {new_status}', result)
                        
                        logger.info(f"Payment {reference} status updated: {old_status} -> {new_status}")
                    
                    return HttpResponse(status=200)
                    
                except Payment.DoesNotExist:
                    logger.warning(f"Payment not found for Paystack webhook: {reference}")
                    return HttpResponse(status=404)
            else:
                logger.warning("No reference found in Paystack webhook")
                return HttpResponse(status=400)
        else:
            logger.error(f"Paystack webhook processing failed: {result.get('error')}")
            return HttpResponse(status=400)
            
    except Exception as e:
        logger.error(f"Paystack webhook error: {str(e)}")
        return HttpResponse(status=500)

@api_view(['GET'])
@permission_classes([AllowAny])
def paystack_callback(request):
    """Handle Paystack payment callback (redirect after payment)"""
    try:
        # Get reference from query parameters
        reference = request.GET.get('reference')
        
        if not reference:
            return Response({
                'success': False,
                'error': 'Payment reference not provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify payment
        paystack_service = PaystackService()
        result = paystack_service.verify_payment(reference)
        
        if result['success']:
            try:
                payment = Payment.objects.get(reference=reference)
                
                # Update payment status
                paystack_status = result['status']
                status_map = {
                    'success': 'successful',
                    'failed': 'failed',
                    'abandoned': 'cancelled',
                    'pending': 'processing'
                }
                
                new_status = status_map.get(paystack_status, 'processing')
                
                if payment.status != new_status:
                    old_status = payment.status
                    payment.status = new_status
                    
                    if new_status in ['successful', 'failed', 'cancelled']:
                        from django.utils import timezone
                        payment.processed_at = timezone.now()
                    
                    payment.save()
                    payment.log('info', f'Payment status updated via callback: {old_status} -> {new_status}', result)
                
                # Redirect to frontend with payment status
                frontend_url = settings.BASE_URL.replace('8000', '8080')
                
                if new_status == 'successful':
                    redirect_url = f"{frontend_url}/payment-success?reference={reference}&amount={payment.amount}&method={payment.payment_method}"
                elif new_status == 'failed':
                    redirect_url = f"{frontend_url}/payment-failed?reference={reference}&reason=payment_failed"
                elif new_status == 'cancelled':
                    redirect_url = f"{frontend_url}/payment-cancelled?reference={reference}&reason=payment_cancelled"
                else:
                    redirect_url = f"{frontend_url}/payment-pending?reference={reference}"
                
                from django.http import HttpResponseRedirect
                return HttpResponseRedirect(redirect_url)
                
            except Payment.DoesNotExist:
                logger.error(f"Payment not found for callback: {reference}")
                return Response({
                    'success': False,
                    'error': 'Payment not found'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({
                'success': False,
                'error': result.get('error', 'Payment verification failed')
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Paystack callback error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while processing the callback'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_paystack_config(request):
    """Get Paystack public configuration"""
    return Response({
        'public_key': settings.PAYSTACK_PUBLIC_KEY,
        'supported_currencies': ['GHS'],
        'supported_channels': ['card', 'mobile_money'],
        'mobile_money_providers': [
            {'code': 'mtn', 'name': 'MTN Mobile Money'},
            {'code': 'vodafone', 'name': 'Vodafone Cash'},
            {'code': 'airteltigo', 'name': 'AirtelTigo Money'}
        ]
    })