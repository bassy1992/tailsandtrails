from rest_framework import serializers
from .models import (
    TicketCategory, Venue, Ticket, TicketPurchase, 
    TicketCode, TicketReview, TicketPromoCode
)

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'slug', 'category_type', 'description', 'icon', 'order']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'slug', 'address', 'city', 'region', 'country',
            'latitude', 'longitude', 'capacity', 'description', 'image',
            'contact_phone', 'contact_email', 'website'
        ]

class TicketListSerializer(serializers.ModelSerializer):
    category = TicketCategorySerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    is_sold_out = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'slug', 'category', 'venue', 'ticket_type',
            'short_description', 'price', 'discount_price', 'effective_price',
            'discount_percentage', 'currency', 'available_quantity', 'total_quantity',
            'event_date', 'event_end_date', 'image', 'status', 'is_featured',
            'is_available', 'is_sold_out', 'rating', 'reviews_count', 'sales_count'
        ]

class TicketDetailSerializer(serializers.ModelSerializer):
    category = TicketCategorySerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    is_available = serializers.BooleanField(read_only=True)
    is_sold_out = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'slug', 'category', 'venue', 'ticket_type',
            'description', 'short_description', 'price', 'discount_price',
            'effective_price', 'discount_percentage', 'currency',
            'total_quantity', 'available_quantity', 'min_purchase', 'max_purchase',
            'event_date', 'event_end_date', 'sale_start_date', 'sale_end_date',
            'image', 'gallery_images', 'features', 'terms_conditions',
            'cancellation_policy', 'tags', 'status', 'is_featured',
            'is_refundable', 'requires_approval', 'is_available', 'is_sold_out',
            'views_count', 'sales_count', 'rating', 'reviews_count', 'created_at'
        ]

class TicketCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCode
        fields = [
            'id', 'code', 'qr_code_data', 'status', 'used_at', 'used_by',
            'is_transferable', 'expires_at', 'is_valid'
        ]
        read_only_fields = ['code', 'qr_code_data', 'is_valid']

class TicketPurchaseSerializer(serializers.ModelSerializer):
    ticket = TicketListSerializer(read_only=True)
    ticket_codes = TicketCodeSerializer(many=True, read_only=True)
    
    class Meta:
        model = TicketPurchase
        fields = [
            'id', 'purchase_id', 'ticket', 'quantity', 'unit_price',
            'total_amount', 'discount_applied', 'customer_name',
            'customer_email', 'customer_phone', 'status', 'payment_status',
            'payment_method', 'payment_reference', 'payment_date',
            'special_requests', 'ticket_codes', 'created_at'
        ]
        read_only_fields = ['purchase_id', 'total_amount']

class TicketPurchaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPurchase
        fields = [
            'ticket', 'quantity', 'customer_name', 'customer_email',
            'customer_phone', 'special_requests'
        ]
    
    def validate(self, data):
        ticket = data['ticket']
        quantity = data['quantity']
        
        # Check if ticket is available
        if not ticket.is_available:
            raise serializers.ValidationError("This ticket is not available for purchase.")
        
        # Check quantity limits
        if quantity < ticket.min_purchase:
            raise serializers.ValidationError(f"Minimum purchase quantity is {ticket.min_purchase}.")
        
        if quantity > ticket.max_purchase:
            raise serializers.ValidationError(f"Maximum purchase quantity is {ticket.max_purchase}.")
        
        # Check availability
        if quantity > ticket.available_quantity:
            raise serializers.ValidationError(f"Only {ticket.available_quantity} tickets available.")
        
        return data
    
    def create(self, validated_data):
        # Set the user from the request
        validated_data['user'] = self.context['request'].user
        
        # Calculate pricing
        ticket = validated_data['ticket']
        quantity = validated_data['quantity']
        unit_price = ticket.effective_price
        total_amount = unit_price * quantity
        
        validated_data['unit_price'] = unit_price
        validated_data['total_amount'] = total_amount
        
        # Create the purchase
        purchase = super().create(validated_data)
        
        # Update ticket availability
        ticket.available_quantity -= quantity
        ticket.save()
        
        # Create ticket codes
        for i in range(quantity):
            TicketCode.objects.create(purchase=purchase)
        
        return purchase

class TicketReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    
    class Meta:
        model = TicketReview
        fields = [
            'id', 'rating', 'title', 'comment', 'user_name',
            'is_verified', 'created_at'
        ]

class TicketReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketReview
        fields = ['ticket', 'rating', 'title', 'comment']
    
    def validate(self, data):
        user = self.context['request'].user
        ticket = data['ticket']
        
        # Check if user has already reviewed this ticket
        if TicketReview.objects.filter(ticket=ticket, user=user).exists():
            raise serializers.ValidationError("You have already reviewed this ticket.")
        
        # Check if user has purchased this ticket
        if not TicketPurchase.objects.filter(ticket=ticket, user=user, status='confirmed').exists():
            raise serializers.ValidationError("You can only review tickets you have purchased.")
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TicketPromoCodeSerializer(serializers.ModelSerializer):
    is_valid = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = TicketPromoCode
        fields = [
            'id', 'code', 'name', 'description', 'discount_type',
            'discount_value', 'max_discount_amount', 'usage_limit',
            'usage_limit_per_user', 'used_count', 'valid_from',
            'valid_until', 'minimum_purchase_amount', 'minimum_quantity',
            'is_valid'
        ]

class PromoCodeValidationSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)
    ticket_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    
    def validate(self, data):
        try:
            promo_code = TicketPromoCode.objects.get(code=data['code'])
        except TicketPromoCode.DoesNotExist:
            raise serializers.ValidationError("Invalid promo code.")
        
        if not promo_code.is_valid:
            raise serializers.ValidationError("This promo code is not valid or has expired.")
        
        try:
            ticket = Ticket.objects.get(id=data['ticket_id'])
        except Ticket.DoesNotExist:
            raise serializers.ValidationError("Invalid ticket.")
        
        # Check if promo code is applicable to this ticket
        if promo_code.applicable_tickets.exists() and ticket not in promo_code.applicable_tickets.all():
            raise serializers.ValidationError("This promo code is not applicable to this ticket.")
        
        if promo_code.applicable_categories.exists() and ticket.category not in promo_code.applicable_categories.all():
            raise serializers.ValidationError("This promo code is not applicable to this ticket category.")
        
        # Check minimum requirements
        total_amount = ticket.effective_price * data['quantity']
        if total_amount < promo_code.minimum_purchase_amount:
            raise serializers.ValidationError(f"Minimum purchase amount is GH₵{promo_code.minimum_purchase_amount}.")
        
        if data['quantity'] < promo_code.minimum_quantity:
            raise serializers.ValidationError(f"Minimum quantity is {promo_code.minimum_quantity}.")
        
        data['promo_code'] = promo_code
        data['ticket'] = ticket
        data['total_amount'] = total_amount
        
        return data