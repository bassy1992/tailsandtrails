import stripe
import logging
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import StripePaymentIntent, StripePaymentMethod, StripeWebhookEvent
from .serializers import (
    CreatePaymentIntentSerializer, StripePaymentIntentSerializer,
    StripePaymentIntentListSerializer, ConfirmPaymentIntentSerializer,
    StripePaymentMethodSerializer, CreateRefundSerializer, StripeRefundSerializer,
    PaymentIntentClientSecretSerializer
)
from .services import StripeService

logger = logging.getLogger(__name__)

class CreatePaymentIntentView(generics.CreateAPIView):
    """Create a new Stripe Payment Intent"""
    serializer_class = CreatePaymentIntentSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get booking if provided
        booking = None
        booking_id = serializer.validated_data.get('booking_id')
        if booking_id:
            from destinations.models import Booking
            try:
                booking = Booking.objects.get(id=booking_id, user=request.user)
            except Booking.DoesNotExist:
                return Response(
                    {'error': 'Booking not found or does not belong to you'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Create Payment Intent
        stripe_service = StripeService()
        result = stripe_service.create_payment_intent(
            user=request.user,
            amount=float(serializer.validated_data['amount']),
            currency=serializer.validated_data.get('currency', 'USD'),
            description=serializer.validated_data.get('description', ''),
            booking=booking,
            metadata=serializer.validated_data.get('metadata', {})
        )
        
        if result['success']:
            payment_intent = result['payment_intent']
            serializer = StripePaymentIntentSerializer(payment_intent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'error': result['error']},
                status=status.HTTP_400_BAD_REQUEST
            )

class PaymentIntentListView(generics.ListAPIView):
    """List user's payment intents"""
    serializer_class = StripePaymentIntentListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StripePaymentIntent.objects.filter(user=self.request.user)

class PaymentIntentDetailView(generics.RetrieveAPIView):
    """Get payment intent details"""
    serializer_class = StripePaymentIntentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'stripe_payment_intent_id'
    
    def get_queryset(self):
        return StripePaymentIntent.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment_intent(request, payment_intent_id):
    """Confirm a payment intent"""
    try:
        payment_intent = StripePaymentIntent.objects.get(
            stripe_payment_intent_id=payment_intent_id,
            user=request.user
        )
    except StripePaymentIntent.DoesNotExist:
        return Response(
            {'error': 'Payment intent not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = ConfirmPaymentIntentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    stripe_service = StripeService()
    result = stripe_service.confirm_payment_intent(
        payment_intent.stripe_payment_intent_id,
        payment_method_id=serializer.validated_data.get('payment_method_id')
    )
    
    if result['success']:
        updated_payment_intent = result['payment_intent']
        serializer = StripePaymentIntentSerializer(updated_payment_intent)
        return Response(serializer.data)
    else:
        return Response(
            {'error': result['error']},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_payment_intent(request, payment_intent_id):
    """Cancel a payment intent"""
    try:
        payment_intent = StripePaymentIntent.objects.get(
            stripe_payment_intent_id=payment_intent_id,
            user=request.user
        )
    except StripePaymentIntent.DoesNotExist:
        return Response(
            {'error': 'Payment intent not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    stripe_service = StripeService()
    result = stripe_service.cancel_payment_intent(payment_intent.stripe_payment_intent_id)
    
    if result['success']:
        updated_payment_intent = result['payment_intent']
        serializer = StripePaymentIntentSerializer(updated_payment_intent)
        return Response(serializer.data)
    else:
        return Response(
            {'error': result['error']},
            status=status.HTTP_400_BAD_REQUEST
        )

class PaymentMethodListView(generics.ListAPIView):
    """List user's payment methods"""
    serializer_class = StripePaymentMethodSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return StripePaymentMethod.objects.filter(user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_refund(request, payment_intent_id):
    """Create a refund for a payment intent"""
    try:
        payment_intent = StripePaymentIntent.objects.get(
            stripe_payment_intent_id=payment_intent_id,
            user=request.user,
            status='succeeded'
        )
    except StripePaymentIntent.DoesNotExist:
        return Response(
            {'error': 'Payment intent not found or not succeeded'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = CreateRefundSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    stripe_service = StripeService()
    result = stripe_service.create_refund(
        payment_intent.stripe_payment_intent_id,
        amount=serializer.validated_data.get('amount'),
        reason=serializer.validated_data.get('reason'),
        description=serializer.validated_data.get('description')
    )
    
    if result['success']:
        refund = result['refund']
        serializer = StripeRefundSerializer(refund)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {'error': result['error']},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_secret(request, payment_intent_id):
    """Get client secret for a payment intent"""
    try:
        payment_intent = StripePaymentIntent.objects.get(
            stripe_payment_intent_id=payment_intent_id,
            user=request.user
        )
    except StripePaymentIntent.DoesNotExist:
        return Response(
            {'error': 'Payment intent not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = PaymentIntentClientSecretSerializer(payment_intent)
    return Response(serializer.data)

@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        logger.error("Invalid payload in Stripe webhook")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        logger.error("Invalid signature in Stripe webhook")
        return HttpResponse(status=400)
    
    # Store webhook event
    webhook_event, created = StripeWebhookEvent.objects.get_or_create(
        stripe_event_id=event['id'],
        defaults={
            'event_type': event['type'],
            'data': event['data']
        }
    )
    
    if created:
        # Process the webhook event
        stripe_service = StripeService()
        try:
            stripe_service.process_webhook_event(webhook_event)
            webhook_event.processed = True
            webhook_event.processed_at = timezone.now()
            webhook_event.save()
        except Exception as e:
            logger.error(f"Error processing webhook {event['id']}: {str(e)}")
            webhook_event.processing_error = str(e)
            webhook_event.save()
    
    return HttpResponse(status=200)