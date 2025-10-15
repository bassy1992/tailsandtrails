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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DestinationImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'is_primary', 'order']
    
    def get_image_url(self, obj):
        if obj.image:
            # obj.image is now a URL string, not a file
            return obj.image
        return None

class ImageUploadSerializer(serializers.ModelSerializer):
    """Serializer for setting image URLs for destinations"""
    
    class Meta:
        model = DestinationImage
        fields = ['destination', 'image', 'alt_text', 'is_primary', 'order']
    
    def validate_image(self, value):
        """Validate image URL"""
        if value:
            # Basic URL validation - Django URLField already handles most validation
            if not value.startswith(('http://', 'https://')):
                raise serializers.ValidationError("Image must be a valid URL starting with http:// or https://")
        
        return value

class DestinationImageUploadSerializer(serializers.ModelSerializer):
    """Serializer for setting main destination image URL"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = ['id', 'image', 'image_url']
    
    def get_image_url(self, obj):
        if obj.image:
            # obj.image is now a URL string, not a file
            return obj.image
        return None
    
    def validate_image(self, value):
        """Validate image URL"""
        if value:
            # Basic URL validation - Django URLField already handles most validation
            if not value.startswith(('http://', 'https://')):
                raise serializers.ValidationError("Image must be a valid URL starting with http:// or https://")
        
        return value

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
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'location', 'description', 'image', 'image_url',
            'price', 'duration', 'duration_display', 'max_group_size',
            'rating', 'reviews_count', 'category', 'highlights', 'includes',
            'price_category', 'is_featured'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            # obj.image is now a URL string, not a file
            return obj.image
        
        # Return placeholder image based on destination name/location
        placeholder_images = {
            'volta': 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800&h=600&fit=crop&crop=center',  # Waterfall
            'kumasi': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop&crop=center',  # Cultural heritage
            'labadi': 'https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=800&h=600&fit=crop&crop=center',  # Beach
            'mole': 'https://images.unsplash.com/photo-1549366021-9f761d040a94?w=800&h=600&fit=crop&crop=center',  # Safari/Wildlife
            'cape coast': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop&crop=center',  # Castle/Historical
            'kakum': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop&crop=center',  # Forest/Canopy
        }
        
        # Find matching placeholder based on destination name or location
        name_lower = obj.name.lower()
        location_lower = obj.location.lower()
        
        for key, image_url in placeholder_images.items():
            if key in name_lower or key in location_lower:
                return image_url
        
        # Default placeholder if no match found
        return 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop&crop=center'

class DestinationDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    highlights = DestinationHighlightSerializer(many=True, read_only=True)
    includes = DestinationIncludeSerializer(many=True, read_only=True)
    images = DestinationImageSerializer(many=True, read_only=True)
    addon_options = AddOnOptionSerializer(many=True, read_only=True)
    experience_addons = ExperienceAddOnSerializer(many=True, read_only=True)
    duration_display = serializers.CharField(read_only=True)
    price_category = serializers.CharField(read_only=True)
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'location', 'description', 'image', 'image_url',
            'price', 'duration', 'duration_display', 'max_group_size',
            'rating', 'reviews_count', 'category', 'highlights', 'includes',
            'images', 'addon_options', 'experience_addons', 'price_category', 
            'is_featured', 'created_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            # obj.image is now a URL string, not a file
            return obj.image
        
        # Return placeholder image based on destination name/location
        placeholder_images = {
            'volta': 'https://images.unsplash.com/photo-1501594907352-04cda38ebc29?w=800&h=600&fit=crop&crop=center',  # Waterfall
            'kumasi': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop&crop=center',  # Cultural heritage
            'labadi': 'https://images.unsplash.com/photo-1506197603052-3cc9c3a201bd?w=800&h=600&fit=crop&crop=center',  # Beach
            'mole': 'https://images.unsplash.com/photo-1549366021-9f761d040a94?w=800&h=600&fit=crop&crop=center',  # Safari/Wildlife
            'cape coast': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop&crop=center',  # Castle/Historical
            'kakum': 'https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=800&h=600&fit=crop&crop=center',  # Forest/Canopy
        }
        
        # Find matching placeholder based on destination name or location
        name_lower = obj.name.lower()
        location_lower = obj.location.lower()
        
        for key, image_url in placeholder_images.items():
            if key in name_lower or key in location_lower:
                return image_url
        
        # Default placeholder if no match found
        return 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop&crop=center'

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
    booking_type_display = serializers.CharField(source='get_booking_type_display', read_only=True)
    is_destination_booking = serializers.BooleanField(read_only=True)
    is_ticket_booking = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_reference', 'destination', 'destination_name',
            'booking_type', 'booking_type_display', 'is_destination_booking', 
            'is_ticket_booking', 'participants', 'total_amount', 'booking_date', 
            'status', 'special_requests', 'selected_addons', 'created_at'
        ]
        read_only_fields = ['booking_reference']