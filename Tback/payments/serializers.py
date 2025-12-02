from rest_framework import serializers
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import Payment, PaymentProvider, PaymentCallback

User = get_user_model()

class PaymentProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProvider
        fields = ['id', 'name', 'code', 'is_active']

class PaymentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating payments"""
    
    class Meta:
        model = Payment
        fields = [
            'amount', 'currency', 'payment_method', 'provider', 
            'phone_number', 'description', 'booking'
        ]
        
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value
        
    def validate_phone_number(self, value):
        if value and not value.startswith('+'):
            raise serializers.ValidationError("Phone number must include country code")
        return value
        
    def validate(self, attrs):
        payment_method = attrs.get('payment_method')
        phone_number = attrs.get('phone_number')
        
        if payment_method == 'mobile_money' and not phone_number:
            raise serializers.ValidationError({
                'phone_number': 'Phone number is required for mobile money payments'
            })
            
        return attrs

class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payment details"""
    user = serializers.StringRelatedField(read_only=True)
    provider = PaymentProviderSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'payment_id', 'reference', 'user', 'booking', 'amount', 'currency',
            'payment_method', 'payment_method_display', 'provider', 'phone_number',
            'status', 'status_display', 'external_reference', 'description',
            'created_at', 'updated_at', 'processed_at'
        ]
        read_only_fields = [
            'payment_id', 'reference', 'user', 'status', 'external_reference',
            'created_at', 'updated_at', 'processed_at'
        ]

class PaymentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for payment lists"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'payment_id', 'reference', 'amount', 'currency',
            'payment_method', 'payment_method_display', 'status', 'status_display',
            'created_at', 'processed_at'
        ]

class PaymentCallbackSerializer(serializers.ModelSerializer):
    """Serializer for payment callbacks"""
    
    class Meta:
        model = PaymentCallback
        fields = ['provider_reference', 'status', 'callback_data']
        
    def create(self, validated_data):
        # Payment will be set in the view
        return super().create(validated_data)

class CheckoutPaymentSerializer(serializers.Serializer):
    """Serializer for checkout payment creation"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    currency = serializers.CharField(max_length=3, default='GHS')
    payment_method = serializers.ChoiceField(choices=[
        ('momo', 'Mobile Money'),
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer')
    ])
    provider_code = serializers.CharField(max_length=20)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    booking_id = serializers.IntegerField(required=False, allow_null=True)
    description = serializers.CharField(max_length=500, required=False, allow_blank=True)
    booking_details = serializers.JSONField(required=False, allow_null=True)
    
    def validate_currency(self, value):
        supported_currencies = ['GHS', 'USD', 'EUR']
        if value.upper() not in supported_currencies:
            raise serializers.ValidationError(f"Currency {value} is not supported")
        return value.upper()
    
    def validate_phone_number(self, value):
        # Phone number is optional, skip validation if empty
        if not value:
            return value
        
        # If phone number doesn't start with +, assume Ghana and add +233
        if not value.startswith('+'):
            # Remove leading 0 if present
            value = value.lstrip('0')
            # Add Ghana country code
            value = '+233' + value
        
        return value
    
    def validate(self, attrs):
        payment_method = attrs.get('payment_method')
        phone_number = attrs.get('phone_number')
        provider_code = attrs.get('provider_code')
        
        # Validate phone number for mobile money
        if payment_method == 'momo' and not phone_number:
            raise serializers.ValidationError({
                'phone_number': 'Phone number is required for mobile money payments'
            })
        
        # Validate provider exists and is active
        try:
            provider = PaymentProvider.objects.get(code=provider_code, is_active=True)
            attrs['provider'] = provider
        except PaymentProvider.DoesNotExist:
            raise serializers.ValidationError({
                'provider_code': f'Provider {provider_code} is not available'
            })
        
        return attrs