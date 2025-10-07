from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StripePaymentIntent, StripePaymentMethod, StripeRefund

User = get_user_model()

class CreatePaymentIntentSerializer(serializers.Serializer):
    """Serializer for creating a Payment Intent"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0.50)
    currency = serializers.CharField(max_length=3, default='USD')
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    booking_id = serializers.IntegerField(required=False, allow_null=True)
    save_payment_method = serializers.BooleanField(default=False)
    
    def validate_currency(self, value):
        """Validate currency code"""
        supported_currencies = ['USD', 'EUR', 'GBP', 'KES', 'UGX', 'TZS']
        if value.upper() not in supported_currencies:
            raise serializers.ValidationError(f"Currency {value} is not supported")
        return value.upper()
    
    def validate_booking_id(self, value):
        """Validate booking exists and belongs to user"""
        if value:
            from destinations.models import Booking
            try:
                booking = Booking.objects.get(id=value)
                # Check if booking belongs to the current user (will be set in view)
                return value
            except Booking.DoesNotExist:
                raise serializers.ValidationError("Booking not found")
        return value

class StripePaymentIntentSerializer(serializers.ModelSerializer):
    """Serializer for Payment Intent details"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    booking_reference = serializers.CharField(source='booking.reference', read_only=True)
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = StripePaymentIntent
        fields = [
            'id', 'stripe_payment_intent_id', 'user_email', 'booking_reference',
            'amount', 'currency', 'status', 'status_display', 'description',
            'payment_method_type', 'created_at', 'updated_at', 'confirmed_at', 'succeeded_at'
        ]
        read_only_fields = [
            'id', 'stripe_payment_intent_id', 'user_email', 'booking_reference',
            'status', 'payment_method_type', 'created_at', 'updated_at', 
            'confirmed_at', 'succeeded_at'
        ]
    
    def get_status_display(self, obj):
        """Get human-readable status"""
        status_map = {
            'requires_payment_method': 'Requires Payment Method',
            'requires_confirmation': 'Requires Confirmation',
            'requires_action': 'Requires Action',
            'processing': 'Processing',
            'requires_capture': 'Requires Capture',
            'canceled': 'Canceled',
            'succeeded': 'Succeeded',
        }
        return status_map.get(obj.status, obj.status.title())

class StripePaymentIntentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Payment Intent lists"""
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = StripePaymentIntent
        fields = [
            'id', 'stripe_payment_intent_id', 'amount', 'currency', 
            'status', 'status_display', 'created_at', 'succeeded_at'
        ]
    
    def get_status_display(self, obj):
        status_map = {
            'requires_payment_method': 'Requires Payment Method',
            'requires_confirmation': 'Requires Confirmation',
            'requires_action': 'Requires Action',
            'processing': 'Processing',
            'requires_capture': 'Requires Capture',
            'canceled': 'Canceled',
            'succeeded': 'Succeeded',
        }
        return status_map.get(obj.status, obj.status.title())

class ConfirmPaymentIntentSerializer(serializers.Serializer):
    """Serializer for confirming a Payment Intent"""
    payment_method_id = serializers.CharField(required=False, allow_blank=True)
    save_payment_method = serializers.BooleanField(default=False)

class StripePaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer for Payment Method details"""
    display_name = serializers.SerializerMethodField()
    
    class Meta:
        model = StripePaymentMethod
        fields = [
            'id', 'stripe_payment_method_id', 'type', 'display_name',
            'card_brand', 'card_last4', 'card_exp_month', 'card_exp_year',
            'is_default', 'created_at'
        ]
        read_only_fields = [
            'id', 'stripe_payment_method_id', 'type', 'card_brand', 
            'card_last4', 'card_exp_month', 'card_exp_year', 'created_at'
        ]
    
    def get_display_name(self, obj):
        """Get display name for payment method"""
        if obj.type == 'card':
            return f"{obj.card_brand.title()} ending in {obj.card_last4}"
        return f"{obj.type.title()} Payment Method"

class CreateRefundSerializer(serializers.Serializer):
    """Serializer for creating a refund"""
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    reason = serializers.ChoiceField(
        choices=[
            ('duplicate', 'Duplicate'),
            ('fraudulent', 'Fraudulent'),
            ('requested_by_customer', 'Requested by Customer'),
        ],
        default='requested_by_customer'
    )
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    
    def validate_amount(self, value):
        """Validate refund amount"""
        if value is not None and value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than 0")
        return value

class StripeRefundSerializer(serializers.ModelSerializer):
    """Serializer for Refund details"""
    payment_intent_id = serializers.CharField(source='payment_intent.stripe_payment_intent_id', read_only=True)
    status_display = serializers.SerializerMethodField()
    
    class Meta:
        model = StripeRefund
        fields = [
            'id', 'stripe_refund_id', 'payment_intent_id', 'amount', 'currency',
            'status', 'status_display', 'reason', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'stripe_refund_id', 'payment_intent_id', 'status', 
            'created_at', 'updated_at'
        ]
    
    def get_status_display(self, obj):
        """Get human-readable status"""
        status_map = {
            'pending': 'Pending',
            'succeeded': 'Succeeded',
            'failed': 'Failed',
            'canceled': 'Canceled',
        }
        return status_map.get(obj.status, obj.status.title())

class PaymentIntentClientSecretSerializer(serializers.Serializer):
    """Serializer for returning client secret"""
    client_secret = serializers.CharField()
    publishable_key = serializers.CharField()
    payment_intent_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField()

class WebhookEventSerializer(serializers.Serializer):
    """Serializer for webhook event data"""
    id = serializers.CharField()
    type = serializers.CharField()
    data = serializers.JSONField()