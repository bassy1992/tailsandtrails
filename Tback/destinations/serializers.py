from rest_framework import serializers
from .models import (
    Category, Destination, DestinationHighlight, 
    DestinationInclude, DestinationImage, Review, Booking,
    AddOnCategory, AddOnOption, ExperienceAddOn, BookingAddOn
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class DestinationHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationHighlight
        fields = ['highlight']

class DestinationIncludeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationInclude
        fields = ['item']

class DestinationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationImage
        fields = ['image_url', 'alt_text', 'is_primary']

class AddOnCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOnCategory
        fields = ['id', 'name', 'display_name', 'description', 'icon', 'order']

class AddOnOptionSerializer(serializers.ModelSerializer):
    category = AddOnCategorySerializer(read_only=True)
    price_display = serializers.CharField(read_only=True)
    
    class Meta:
        model = AddOnOption
        fields = [
            'id', 'category', 'name', 'description', 'price', 
            'pricing_type', 'price_display', 'is_default', 'order'
        ]

class ExperienceAddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperienceAddOn
        fields = [
            'id', 'name', 'description', 'price', 'duration', 
            'max_participants', 'order'
        ]

class DestinationListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    highlights = DestinationHighlightSerializer(many=True, read_only=True)
    includes = DestinationIncludeSerializer(many=True, read_only=True)
    duration_display = serializers.CharField(read_only=True)
    price_category = serializers.CharField(read_only=True)
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'location', 'description', 'image',
            'price', 'duration', 'duration_display', 'max_group_size',
            'rating', 'reviews_count', 'category', 'highlights', 'includes',
            'price_category', 'is_featured'
        ]

class DestinationDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    highlights = DestinationHighlightSerializer(many=True, read_only=True)
    includes = DestinationIncludeSerializer(many=True, read_only=True)
    images = DestinationImageSerializer(many=True, read_only=True)
    addon_options = AddOnOptionSerializer(many=True, read_only=True)
    experience_addons = ExperienceAddOnSerializer(many=True, read_only=True)
    duration_display = serializers.CharField(read_only=True)
    price_category = serializers.CharField(read_only=True)
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'location', 'description', 'image',
            'price', 'duration', 'duration_display', 'max_group_size',
            'rating', 'reviews_count', 'category', 'highlights', 'includes',
            'images', 'addon_options', 'experience_addons', 'price_category', 
            'is_featured', 'created_at'
        ]

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.first_name', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'rating', 'title', 'comment', 'user_name',
            'is_verified', 'created_at'
        ]

class BookingAddOnSerializer(serializers.ModelSerializer):
    addon_option = AddOnOptionSerializer(read_only=True)
    experience_addon = ExperienceAddOnSerializer(read_only=True)
    
    class Meta:
        model = BookingAddOn
        fields = [
            'id', 'addon_option', 'experience_addon', 'quantity', 'price_at_booking'
        ]

class BookingSerializer(serializers.ModelSerializer):
    destination_name = serializers.CharField(source='destination.name', read_only=True)
    selected_addons = BookingAddOnSerializer(many=True, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'destination', 'destination_name',
            'participants', 'total_amount', 'booking_date', 'status',
            'special_requests', 'selected_addons', 'created_at'
        ]
        read_only_fields = ['booking_reference']