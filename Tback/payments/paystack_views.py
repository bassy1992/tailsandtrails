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

def format_booking_details_for_admin(booking_details):
    """Format booking details in a more readable format for admin logs"""
    try:
        if not booking_details:
            return "No booking details"
        
        # Extract key information
        booking_data = booking_details.get('bookingData', {})
        selected_addons = booking_details.get('selectedAddOns', [])
        
        # Format the main booking info
        formatted = {
            "📋 BOOKING SUMMARY": {
                "Tour": booking_data.get('tourName', 'N/A'),
                "Duration": booking_data.get('duration', 'N/A'),
                "Date": booking_details.get('selectedDate', 'N/A'),
                "Travelers": f"{booking_data.get('travelers', {}).get('adults', 0)} adults, {booking_data.get('travelers', {}).get('children', 0)} children"
            },
            "💰 PRICING": {
                "Base Price": f"GH₵{booking_details.get('baseTotal', 0)}",
                "Add-ons Total": f"GH₵{booking_details.get('addonTotal', 0)}",
                "Final Total": f"GH₵{booking_data.get('totalPrice', booking_details.get('baseTotal', 0))}"
            }
        }
        
        # Add pricing tiers if available
        pricing_data = booking_data.get('pricingData', {})
        if pricing_data.get('has_tiered_pricing') and pricing_data.get('pricing_tiers'):
            formatted["🎯 PRICING TIERS"] = {}
            for tier in pricing_data['pricing_tiers']:
                tier_key = f"{tier['group_size_display']}"
                formatted["🎯 PRICING TIERS"][tier_key] = f"GH₵{tier['price_per_person']} per person"
        
        # Add selected add-ons if any
        if selected_addons:
            formatted["🎁 SELECTED ADD-ONS"] = {}
            for addon in selected_addons:
                addon_name = addon.get('name', 'Unknown Add-on')
                addon_price = addon.get('total_price', 0)
                formatted["🎁 SELECTED ADD-ONS"][addon_name] = f"GH₵{addon_price}"
        
        # Format as readable string
        result = []
        for section, content in formatted.items():
            result.append(f"\n{section}:")
            if isinstance(content, dict):
                for key, value in content.items():
                    result.append(f"  • {key}: {value}")
            else:
                result.append(f"  {content}")
        
        return "\n".join(result)
        
    except Exception as e:
        # Fallback to original format if formatting fails
        return f"Formatting error: {str(e)}\nOriginal data: {json.dumps(booking_details, indent=2)}"

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
                # Format booking details for better readability
                formatted_details = format_booking_details_for_admin(data['booking_details'])
                payment.log('info', 'Booking details stored from request', formatted_details)
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
            'callback_url': f"{settings.FRONTEND_URL}/payment-callback"
        }
        
        # Handle different payment methods
        if data['payment_method'] == 'mobile_money':
            # For MoMo payments, redirect to Paystack website for processing
            payment_data['provider'] = data.get('provider', 'mtn')  # mtn, vodafone, airteltigo
            
            # Use standard payment initialization which will redirect to Paystack website
            # This allows users to complete mobile money payments on Paystack's secure platform
            result = paystack_service.initialize_payment(payment_data)
        else:
            # Card payment - uses standard checkout
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
        
        # Check for test mode mobile money auto-approval
        if is_test_mode and payment.payment_method == 'mobile_money' and payment.status == 'processing':
            from .test_mobile_money_handler import TestMobileMoneyHandler
            
            if TestMobileMoneyHandler.should_simulate_success(payment):
                # Auto-approve the payment
                payment.status = 'successful'
                from django.utils import timezone
                payment.processed_at = timezone.now()
                payment.save()
                
                payment.log('info', 'Test mode: Mobile money payment auto-approved', {
                    'auto_approved': True,
                    'test_mode': True,
                    'elapsed_seconds': (timezone.now() - payment.created_at).total_seconds()
                })
                
                return Response({
                    'success': True,
                    'payment': PaymentSerializer(payment).data,
                    'test_mode': True,
                    'message': 'Test mode: Mobile money payment auto-approved'
                })
        
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
            
            # In test mode, don't override successful status with failed/cancelled for mobile money
            if (is_test_mode and payment.payment_method == 'mobile_money' and 
                payment.status == 'successful' and new_status in ['failed', 'cancelled']):
                # Keep the successful status for test mode mobile money
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
                'paystack_data': result.get('data', {}),
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
                frontend_url = settings.FRONTEND_URL
                
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
def verify_access_code(request, access_code):
    """Verify payment using access code (for test mode compatibility)"""
    try:
        # Extract reference from access code if it's a test mode access code
        if access_code.startswith('test-momo-'):
            # Extract reference from test access code format: test-momo-PAY-XXXXXXXX-XXXXXX
            reference = access_code.replace('test-momo-', '')
            
            # Find payment by reference
            try:
                payment = Payment.objects.get(reference=reference)
                
                # Check if this is test mode
                public_key = getattr(settings, 'PAYSTACK_PUBLIC_KEY', '')
                is_test_mode = public_key.startswith('pk_test_')
                
                if is_test_mode and payment.payment_method == 'mobile_money':
                    # Check if enough time has passed for auto-approval
                    from django.utils import timezone
                    time_elapsed = (timezone.now() - payment.created_at).total_seconds()
                    
                    if time_elapsed > 10:  # Auto-approve after 10 seconds
                        payment.status = 'successful'
                        payment.processed_at = timezone.now()
                        payment.save()
                        
                        payment.log('info', 'Test mode: Mobile money payment auto-approved via access code', {
                            'access_code': access_code,
                            'auto_approved': True,
                            'elapsed_seconds': time_elapsed
                        })
                        
                        return Response({
                            'success': True,
                            'data': {
                                'status': 'success',
                                'amount': int(float(payment.amount) * 100),
                                'currency': payment.currency,
                                'reference': payment.reference,
                                'paid_at': payment.processed_at.isoformat(),
                                'channel': 'mobile_money',
                                'gateway_response': 'Test mode: Mobile money payment auto-approved'
                            },
                            'payment': PaymentSerializer(payment).data,
                            'test_mode': True
                        })
                    else:
                        # Still processing
                        return Response({
                            'success': True,
                            'data': {
                                'status': 'pending',
                                'amount': int(float(payment.amount) * 100),
                                'currency': payment.currency,
                                'reference': payment.reference,
                                'channel': 'mobile_money',
                                'gateway_response': f'Test mode: Processing mobile money payment ({int(time_elapsed)}s elapsed)'
                            },
                            'payment': PaymentSerializer(payment).data,
                            'test_mode': True
                        })
                
                # For non-test mode or non-mobile money, use regular verification
                return verify_paystack_payment(request, payment.reference)
                
            except Payment.DoesNotExist:
                return Response({
                    'success': False,
                    'error': 'Payment not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        # For regular access codes, try to find payment by access code in metadata
        try:
            payment = Payment.objects.filter(
                metadata__access_code=access_code
            ).first()
            
            if payment:
                return verify_paystack_payment(request, payment.reference)
            else:
                return Response({
                    'success': False,
                    'error': 'Payment not found for access code'
                }, status=status.HTTP_404_NOT_FOUND)
                
        except Exception as e:
            logger.error(f"Access code verification error: {str(e)}")
            return Response({
                'success': False,
                'error': 'Failed to verify access code'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        logger.error(f"Access code verification error: {str(e)}")
        return Response({
            'success': False,
            'error': 'An error occurred while verifying access code'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([AllowAny])
def paystack_api_proxy(request, endpoint_path):
    """Proxy for Paystack API calls to handle test mode access codes"""
    try:
        # Check if this is a verify_access_code call for test mode
        if 'verify_access_code' in endpoint_path:
            # Extract access code from path
            access_code = endpoint_path.split('/')[-1]
            
            # If it's a test mode access code, handle it locally
            if access_code.startswith('test-momo-') or access_code.startswith('fallback_'):
                return verify_access_code(request, access_code)
        
        # For other endpoints, proxy to real Paystack API
        import requests
        
        paystack_url = f"https://api.paystack.co/{endpoint_path}"
        
        # Get authorization header
        secret_key = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
        headers = {
            'Authorization': f'Bearer {secret_key}',
            'Content-Type': 'application/json'
        }
        
        # Forward the request to Paystack
        if request.method == 'GET':
            response = requests.get(paystack_url, headers=headers, params=request.GET)
        elif request.method == 'POST':
            response = requests.post(paystack_url, headers=headers, json=request.data)
        else:
            return Response({
                'success': False,
                'error': 'Method not allowed'
            }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Return Paystack response
        try:
            return Response(response.json(), status=response.status_code)
        except:
            return Response({
                'success': False,
                'error': 'Invalid response from Paystack'
            }, status=response.status_code)
            
    except Exception as e:
        logger.error(f"Paystack API proxy error: {str(e)}")
        return Response({
            'success': False,
            'error': 'Proxy error'
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