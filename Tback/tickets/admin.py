from django.contrib import admin
from .models import TicketCategory, Venue, Ticket, TicketPurchase, TicketCode, TicketReview, TicketPromoCode
from .addon_models import AddOnCategory, AddOn, AddOnOption, BookingAddOn

@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_active', 'order']
    list_filter = ['category_type', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'region', 'country', 'is_active']
    list_filter = ['city', 'region', 'country', 'is_active']
    search_fields = ['name', 'address', 'city']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'venue', 'price', 'available_quantity', 'status', 'event_date']
    list_filter = ['category', 'status', 'is_featured', 'ticket_type']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'event_date'

@admin.register(TicketPurchase)
class TicketPurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_id', 'ticket', 'customer_name', 'quantity', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method']
    search_fields = ['purchase_id', 'customer_name', 'customer_email']
    readonly_fields = ['purchase_id']

@admin.register(TicketCode)
class TicketCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'purchase', 'status', 'used_at']
    list_filter = ['status']
    search_fields = ['code']

@admin.register(TicketReview)
class TicketReviewAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'user', 'rating', 'is_verified', 'is_active', 'created_at']
    list_filter = ['rating', 'is_verified', 'is_active']

@admin.register(TicketPromoCode)
class TicketPromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'discount_type', 'discount_value', 'used_count', 'is_active']
    list_filter = ['discount_type', 'is_active']
    search_fields = ['code', 'name']

# Add-on Admin Classes
@admin.register(AddOnCategory)
class AddOnCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'is_active', 'order']
    list_filter = ['category_type', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

class AddOnOptionInline(admin.TabularInline):
    model = AddOnOption
    extra = 1

@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'addon_type', 'base_price', 'pricing_type', 'is_required', 'is_active']
    list_filter = ['category', 'addon_type', 'pricing_type', 'is_required', 'is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [AddOnOptionInline]
    filter_horizontal = ['applicable_tickets', 'applicable_categories']

@admin.register(AddOnOption)
class AddOnOptionAdmin(admin.ModelAdmin):
    list_display = ['addon', 'name', 'price', 'is_default', 'is_active', 'order']
    list_filter = ['addon__category', 'is_default', 'is_active']
    search_fields = ['name', 'addon__name']

@admin.register(BookingAddOn)
class BookingAddOnAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'addon', 'option', 'quantity', 'total_price', 'customer_name']
    list_filter = ['addon__category', 'created_at']
    search_fields = ['booking_reference', 'customer_name', 'customer_email']
    readonly_fields = ['total_price']