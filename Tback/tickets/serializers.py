from rest_framework import serializers
from .models import Ticket, TicketCategory, Venue, TicketPurchase, TicketCode
from .addon_models import AddOnCategory, AddOn, AddOnOption, BookingAddOn

class AddOnOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOnOption
        fields = ['id', 'name', 'description', 'price', 'is_default', 'order']

class AddOnSerializer(serializers.ModelSerializer):
    options = AddOnOptionSerializer(many=True, read_only=True)
    calculated_price = serializers.SerializerMethodField()
    
    class Meta:
        model = AddOn
        fields = [
            'id', 'name', 'slug', 'addon_type', 'description', 'short_description',
            'base_price', 'pricing_type', 'currency', 'is_required', 'is_default',
            'max_quantity', 'image', 'features', 'options', 'calculated_price'
        ]
    
    def get_calculated_price(self, obj):
        # Get context for price calculation
        request = self.context.get('request')
        base_amount = self.context.get('base_amount', 0)
        travelers = self.context.get('travelers', 1)
        
        return float(obj.calculate_price(base_amount=base_amount, travelers=travelers))

class AddOnCategorySerializer(serializers.ModelSerializer):
    addons = AddOnSerializer(many=True, read_only=True)
    
    class Meta:
        model = AddOnCategory
        fields = ['id', 'name', 'slug', 'category_type', 'description', 'icon', 'addons']

class BookingAddOnSerializer(serializers.ModelSerializer):
    addon_name = serializers.CharField(source='addon.name', read_only=True)
    option_name = serializers.CharField(source='option.name', read_only=True)
    
    class Meta:
        model = BookingAddOn
        fields = [
            'id', 'addon', 'option', 'quantity', 'unit_price', 'total_price',
            'addon_name', 'option_name'
        ]

class TicketCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketCategory
        fields = ['id', 'name', 'slug', 'category_type', 'description', 'icon']

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'slug', 'address', 'city', 'region', 'country',
            'latitude', 'longitude', 'capacity', 'description', 'image',
            'contact_phone', 'contact_email', 'website'
        ]

class TicketSerializer(serializers.ModelSerializer):
    category = TicketCategorySerializer(read_only=True)
    venue = VenueSerializer(read_only=True)
    available_addons = AddOnSerializer(many=True, read_only=True)
    
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
            'views_count', 'sales_count', 'rating', 'reviews_count',
            'available_addons'
        ]

class TicketPurchaseSerializer(serializers.ModelSerializer):
    selected_addons = BookingAddOnSerializer(many=True, read_only=True)
    
    class Meta:
        model = TicketPurchase
        fields = [
            'id', 'purchase_id', 'ticket', 'quantity', 'unit_price', 'total_amount',
            'discount_applied', 'customer_name', 'customer_email', 'customer_phone',
            'status', 'payment_status', 'payment_method', 'payment_reference',
            'special_requests', 'selected_addons', 'created_at'
        ]