from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Destination, DestinationHighlight, 
    DestinationInclude, DestinationImage, Review, Booking,
    AddOnCategory, AddOnOption, ExperienceAddOn, BookingAddOn,
    PricingTier, GalleryCategory, GalleryImage, GalleryVideo
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'destinations_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def destinations_count(self, obj):
        return obj.destinations.count()
    destinations_count.short_description = 'Destinations'

class DestinationHighlightInline(admin.TabularInline):
    model = DestinationHighlight
    extra = 1
    fields = ('highlight', 'order')

class DestinationIncludeInline(admin.TabularInline):
    model = DestinationInclude
    extra = 1
    fields = ('item', 'order')

class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 1
    fields = ('image_url', 'alt_text', 'is_primary', 'order')

class AddOnOptionInline(admin.TabularInline):
    model = AddOnOption
    extra = 0
    fields = ('category', 'name', 'description', 'price', 'pricing_type', 'is_default', 'is_active', 'order')
    
    def has_add_permission(self, request, obj=None):
        # Only allow adding if there are categories available
        return AddOnCategory.objects.filter(is_active=True).exists()

class ExperienceAddOnInline(admin.TabularInline):
    model = ExperienceAddOn
    extra = 0
    fields = ('name', 'description', 'price', 'duration', 'max_participants', 'is_active', 'order')

class PricingTierInline(admin.TabularInline):
    model = PricingTier
    extra = 1
    fields = ('min_people', 'max_people', 'total_price', 'price_per_person')
    readonly_fields = ('price_per_person',)

class BookingAddOnInline(admin.TabularInline):
    model = BookingAddOn
    extra = 0
    readonly_fields = ('price_at_booking', 'created_at')
    fields = ('addon_option', 'experience_addon', 'quantity', 'price_at_booking', 'created_at')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'location', 'category', 'price', 'duration', 
        'rating', 'reviews_count', 'is_active', 'is_featured', 'created_at'
    )
    list_filter = ('category', 'duration', 'is_active', 'is_featured', 'created_at')
    search_fields = ('name', 'location', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PricingTierInline, DestinationHighlightInline, DestinationIncludeInline, DestinationImageInline, AddOnOptionInline, ExperienceAddOnInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'location', 'category', 'description')
        }),
        ('Tour Details', {
            'fields': ('price', 'duration', 'max_group_size', 'start_date', 'end_date', 'image')
        }),
        ('Ratings & Reviews', {
            'fields': ('rating', 'reviews_count')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image)
        return "No image"
    image_preview.short_description = 'Image Preview'
    
    def get_form(self, request, obj=None, **kwargs):
        # Override to handle any form errors gracefully
        try:
            return super().get_form(request, obj, **kwargs)
        except Exception as e:
            # Log the error
            import logging
            logger = logging.getLogger('django')
            logger.error(f"Error in DestinationAdmin.get_form: {e}")
            raise

@admin.register(DestinationImage)
class DestinationImageAdmin(admin.ModelAdmin):
    list_display = ('destination', 'alt_text', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('destination__name', 'alt_text')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'title', 'is_verified', 'is_active', 'created_at')
    list_filter = ('rating', 'is_verified', 'is_active', 'created_at')
    search_fields = ('destination__name', 'user__email', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Review Information', {
            'fields': ('destination', 'user', 'rating', 'title', 'comment')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_reference', 'destination', 'user', 'participants', 
        'total_amount', 'booking_date', 'status', 'created_at'
    )
    list_filter = ('status', 'booking_date', 'created_at')
    search_fields = ('booking_reference', 'destination__name', 'user__email')
    readonly_fields = ('booking_reference', 'created_at', 'updated_at')
    inlines = [BookingAddOnInline]
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_reference', 'destination', 'user', 'participants')
        }),
        ('Financial', {
            'fields': ('total_amount',)
        }),
        ('Schedule', {
            'fields': ('booking_date', 'status')
        }),
        ('Additional Information', {
            'fields': ('special_requests',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AddOnCategory)
class AddOnCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'icon', 'is_active', 'order', 'created_at')
    list_filter = ('is_active', 'name')
    search_fields = ('display_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'display_name', 'description', 'icon')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AddOnOption)
class AddOnOptionAdmin(admin.ModelAdmin):
    list_display = ('destination', 'category', 'name', 'price_display', 'pricing_type', 'is_default', 'is_active', 'order')
    list_filter = ('category', 'pricing_type', 'is_default', 'is_active', 'destination__category')
    search_fields = ('destination__name', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('destination', 'category', 'order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('destination', 'category', 'name', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'pricing_type')
        }),
        ('Settings', {
            'fields': ('is_default', 'is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(PricingTier)
class PricingTierAdmin(admin.ModelAdmin):
    list_display = ('destination', 'people_range', 'total_price', 'price_per_person', 'created_at')
    list_filter = ('destination__category',)
    search_fields = ('destination__name',)
    readonly_fields = ('price_per_person', 'created_at', 'updated_at')
    ordering = ('destination', 'min_people')
    
    fieldsets = (
        ('Destination', {
            'fields': ('destination',)
        }),
        ('Group Size', {
            'fields': ('min_people', 'max_people')
        }),
        ('Pricing', {
            'fields': ('total_price', 'price_per_person')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def people_range(self, obj):
        if obj.min_people == obj.max_people:
            return f"{obj.min_people} person"
        return f"{obj.min_people}-{obj.max_people} people"
    people_range.short_description = 'Group Size'

@admin.register(ExperienceAddOn)
class ExperienceAddOnAdmin(admin.ModelAdmin):
    list_display = ('destination', 'name', 'price', 'duration', 'max_participants', 'is_active', 'order')
    list_filter = ('is_active', 'destination__category')
    search_fields = ('destination__name', 'name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('destination', 'order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('destination', 'name', 'description')
        }),
        ('Details', {
            'fields': ('price', 'duration', 'max_participants')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

#
 Gallery Admin
@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured', 'category', 'created_at')
    search_fields = ('title', 'description', 'location', 'photographer')
    list_editable = ('is_featured', 'order')
    ordering = ('-is_featured', 'order', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Images', {
            'fields': ('image_url', 'thumbnail_url')
        }),
        ('Details', {
            'fields': ('location', 'photographer', 'is_featured', 'order')
        }),
    )


@admin.register(GalleryVideo)
class GalleryVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'is_featured', 'order', 'created_at')
    list_filter = ('is_featured', 'category', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_featured', 'order')
    ordering = ('-is_featured', 'order', '-created_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Video', {
            'fields': ('video_url', 'thumbnail_url', 'duration')
        }),
        ('Display', {
            'fields': ('is_featured', 'order')
        }),
    )
