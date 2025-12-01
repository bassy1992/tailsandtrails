from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    TicketCategory, Venue, Ticket, TicketPurchase, 
    TicketCode, TicketReview, TicketPromoCode
)

@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'tickets_count', 'is_active', 'order', 'created_at')
    list_filter = ('category_type', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category_type', 'description', 'icon')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def tickets_count(self, obj):
        return obj.tickets.count()
    tickets_count.short_description = 'Tickets'

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'region', 'capacity', 'tickets_count', 'is_active', 'created_at')
    list_filter = ('region', 'city', 'is_active')
    search_fields = ('name', 'city', 'address')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Location', {
            'fields': ('address', 'city', 'region', 'country', 'latitude', 'longitude')
        }),
        ('Details', {
            'fields': ('capacity',)
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email', 'website')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def tickets_count(self, obj):
        return obj.tickets.count()
    tickets_count.short_description = 'Tickets'

class TicketCodeInline(admin.TabularInline):
    model = TicketCode
    extra = 0
    readonly_fields = ('code', 'qr_code_data', 'created_at', 'used_at')
    fields = ('code', 'status', 'used_at', 'used_by', 'is_transferable', 'expires_at')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'venue', 'price_display', 'available_quantity', 
        'total_quantity', 'event_date', 'status', 'is_featured', 'sales_count'
    )
    list_filter = (
        'category', 'ticket_type', 'status', 'is_featured', 
        'is_refundable', 'venue__city', 'event_date'
    )
    search_fields = ('title', 'description', 'venue__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'views_count', 'sales_count')
    date_hierarchy = 'event_date'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'venue', 'ticket_type')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'features')
        }),
        ('Pricing', {
            'fields': ('price', 'currency', 'discount_price')
        }),
        ('Availability', {
            'fields': ('total_quantity', 'available_quantity', 'min_purchase', 'max_purchase')
        }),
        ('Schedule', {
            'fields': ('event_date', 'event_end_date', 'sale_start_date', 'sale_end_date')
        }),
        ('Media', {
            'fields': ('image', 'gallery_images')
        }),
        ('Policies', {
            'fields': ('terms_conditions', 'cancellation_policy')
        }),
        ('SEO & Marketing', {
            'fields': ('meta_title', 'meta_description', 'tags'),
            'classes': ('collapse',)
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'is_refundable', 'requires_approval')
        }),
        ('Analytics', {
            'fields': ('views_count', 'sales_count', 'rating', 'reviews_count'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def price_display(self, obj):
        if obj.discount_price:
            return format_html(
                '<span style="text-decoration: line-through; color: #999;">GH₵{}</span> '
                '<strong style="color: #e74c3c;">GH₵{}</strong>',
                obj.price, obj.discount_price
            )
        return f"GH₵{obj.price}"
    price_display.short_description = 'Price'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="60" style="object-fit: cover;" />', obj.image)
        return "No image"
    image_preview.short_description = 'Image Preview'

@admin.register(TicketPurchase)
class TicketPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'purchase_id_short', 'ticket_link', 'customer_info', 'quantity', 
        'total_amount_display', 'status_badge', 'payment_status_badge', 
        'ticket_codes_count', 'created_at'
    )
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at', 'ticket__category')
    search_fields = ('purchase_id', 'ticket__title', 'user__email', 'customer_name', 'customer_email')
    readonly_fields = ('purchase_id', 'created_at', 'updated_at')
    inlines = [TicketCodeInline]
    date_hierarchy = 'created_at'
    actions = ['mark_as_confirmed', 'mark_as_cancelled', 'resend_tickets']
    
    fieldsets = (
        ('Purchase Information', {
            'fields': ('purchase_id', 'ticket', 'user', 'quantity')
        }),
        ('Pricing', {
            'fields': ('unit_price', 'total_amount', 'discount_applied')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Status', {
            'fields': ('status', 'payment_status')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_reference', 'payment_date')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('ticket', 'user').prefetch_related('ticket_codes')
    
    def purchase_id_short(self, obj):
        return f"{str(obj.purchase_id)[:8]}..."
    purchase_id_short.short_description = 'Purchase ID'
    
    def ticket_link(self, obj):
        url = reverse('admin:tickets_ticket_change', args=[obj.ticket.id])
        return format_html('<a href="{}">{}</a>', url, obj.ticket.title[:30])
    ticket_link.short_description = 'Ticket'
    
    def customer_info(self, obj):
        return format_html(
            '<strong>{}</strong><br/><small>{}</small>',
            obj.customer_name,
            obj.customer_email
        )
    customer_info.short_description = 'Customer'
    
    def total_amount_display(self, obj):
        return format_html('<strong>GH₵{}</strong>', obj.total_amount)
    total_amount_display.short_description = 'Amount'
    
    def status_badge(self, obj):
        colors = {
            'pending': '#f39c12',
            'confirmed': '#27ae60',
            'cancelled': '#e74c3c',
            'refunded': '#9b59b6'
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.status.upper()
        )
    status_badge.short_description = 'Status'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': '#f39c12',
            'completed': '#27ae60',
            'failed': '#e74c3c',
            'refunded': '#9b59b6'
        }
        color = colors.get(obj.payment_status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.payment_status.upper()
        )
    payment_status_badge.short_description = 'Payment'
    
    def ticket_codes_count(self, obj):
        count = obj.ticket_codes.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #3498db; color: white; padding: 2px 6px; border-radius: 10px; font-size: 10px;">{}</span>',
                count
            )
        return '-'
    ticket_codes_count.short_description = 'Codes'
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} purchases marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected purchases as confirmed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} purchases marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected purchases as cancelled"
    
    def resend_tickets(self, request, queryset):
        # TODO: Implement email sending functionality
        count = queryset.count()
        self.message_user(request, f'Tickets will be resent for {count} purchases.')
    resend_tickets.short_description = "Resend tickets to customers"

@admin.register(TicketCode)
class TicketCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'purchase_link', 'ticket_title', 'customer_name', 'status_badge', 'used_info', 'created_at')
    list_filter = ('status', 'is_transferable', 'used_at', 'created_at', 'purchase__ticket__category')
    search_fields = ('code', 'purchase__purchase_id', 'purchase__ticket__title', 'purchase__customer_name')
    readonly_fields = ('code', 'qr_code_data', 'created_at', 'updated_at')
    actions = ['mark_as_used', 'mark_as_active', 'generate_qr_codes']
    
    fieldsets = (
        ('Code Information', {
            'fields': ('code', 'purchase', 'qr_code_data')
        }),
        ('Usage', {
            'fields': ('status', 'used_at', 'used_by')
        }),
        ('Settings', {
            'fields': ('is_transferable', 'expires_at')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('purchase__ticket', 'purchase')
    
    def purchase_link(self, obj):
        url = reverse('admin:tickets_ticketpurchase_change', args=[obj.purchase.id])
        return format_html('<a href="{}">{}</a>', url, f"{obj.purchase.purchase_id[:8]}...")
    purchase_link.short_description = 'Purchase'
    
    def ticket_title(self, obj):
        return obj.purchase.ticket.title[:30]
    ticket_title.short_description = 'Ticket'
    
    def customer_name(self, obj):
        return obj.purchase.customer_name
    customer_name.short_description = 'Customer'
    
    def status_badge(self, obj):
        colors = {
            'active': '#27ae60',
            'used': '#95a5a6',
            'expired': '#e74c3c',
            'cancelled': '#e74c3c'
        }
        color = colors.get(obj.status, '#95a5a6')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.status.upper()
        )
    status_badge.short_description = 'Status'
    
    def used_info(self, obj):
        if obj.used_at:
            return format_html(
                '<small>{}<br/>by: {}</small>',
                obj.used_at.strftime('%Y-%m-%d %H:%M'),
                obj.used_by or 'Unknown'
            )
        return '-'
    used_info.short_description = 'Used'
    
    def mark_as_used(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(status='active').update(
            status='used',
            used_at=timezone.now(),
            used_by=request.user.username
        )
        self.message_user(request, f'{updated} ticket codes marked as used.')
    mark_as_used.short_description = "Mark selected codes as used"
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status='active', used_at=None, used_by=None)
        self.message_user(request, f'{updated} ticket codes marked as active.')
    mark_as_active.short_description = "Mark selected codes as active"
    
    def generate_qr_codes(self, request, queryset):
        # TODO: Implement QR code generation
        count = queryset.count()
        self.message_user(request, f'QR codes will be generated for {count} ticket codes.')
    generate_qr_codes.short_description = "Generate QR codes"

@admin.register(TicketReview)
class TicketReviewAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'rating', 'title', 'is_verified', 'is_active', 'created_at')
    list_filter = ('rating', 'is_verified', 'is_active', 'created_at')
    search_fields = ('ticket__title', 'user__email', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Review Information', {
            'fields': ('ticket', 'user', 'purchase', 'rating', 'title', 'comment')
        }),
        ('Moderation', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(TicketPromoCode)
class TicketPromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'name', 'discount_display', 'used_count', 'usage_limit', 
        'valid_from', 'valid_until', 'is_active'
    )
    list_filter = ('discount_type', 'is_active', 'valid_from', 'valid_until')
    search_fields = ('code', 'name', 'description')
    readonly_fields = ('used_count', 'created_at', 'updated_at')
    filter_horizontal = ('applicable_tickets', 'applicable_categories')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'description')
        }),
        ('Discount Settings', {
            'fields': ('discount_type', 'discount_value', 'max_discount_amount')
        }),
        ('Usage Limits', {
            'fields': ('usage_limit', 'usage_limit_per_user', 'used_count')
        }),
        ('Validity Period', {
            'fields': ('valid_from', 'valid_until')
        }),
        ('Applicable Items', {
            'fields': ('applicable_tickets', 'applicable_categories')
        }),
        ('Requirements', {
            'fields': ('minimum_purchase_amount', 'minimum_quantity')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def discount_display(self, obj):
        if obj.discount_type == 'percentage':
            return f"{obj.discount_value}%"
        else:
            return f"GH₵{obj.discount_value}"
    discount_display.short_description = 'Discount'
# Custom Admin Site for Tickets
class TicketsAdminSite(admin.AdminSite):
    site_header = "Tickets Administration"
    site_title = "Tickets Admin"
    index_title = "Ticket Management Dashboard"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='tickets_dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        """Custom dashboard view with ticket statistics"""
        # Get date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Purchase statistics
        total_purchases = TicketPurchase.objects.count()
        confirmed_purchases = TicketPurchase.objects.filter(status='confirmed').count()
        pending_purchases = TicketPurchase.objects.filter(status='pending').count()
        
        # Revenue statistics
        total_revenue = TicketPurchase.objects.filter(
            payment_status='completed'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        weekly_revenue = TicketPurchase.objects.filter(
            payment_status='completed',
            created_at__gte=week_ago
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Ticket statistics
        total_tickets = Ticket.objects.count()
        active_tickets = Ticket.objects.filter(status='active').count()
        sold_out_tickets = Ticket.objects.filter(available_quantity=0).count()
        
        # Popular tickets
        popular_tickets = Ticket.objects.annotate(
            purchase_count=Count('ticketpurchase')
        ).order_by('-purchase_count')[:5]
        
        # Recent purchases
        recent_purchases = TicketPurchase.objects.select_related(
            'ticket', 'user'
        ).order_by('-created_at')[:10]
        
        # Ticket codes statistics
        total_codes = TicketCode.objects.count()
        used_codes = TicketCode.objects.filter(status='used').count()
        active_codes = TicketCode.objects.filter(status='active').count()
        
        context = {
            'title': 'Tickets Dashboard',
            'total_purchases': total_purchases,
            'confirmed_purchases': confirmed_purchases,
            'pending_purchases': pending_purchases,
            'total_revenue': total_revenue,
            'weekly_revenue': weekly_revenue,
            'total_tickets': total_tickets,
            'active_tickets': active_tickets,
            'sold_out_tickets': sold_out_tickets,
            'popular_tickets': popular_tickets,
            'recent_purchases': recent_purchases,
            'total_codes': total_codes,
            'used_codes': used_codes,
            'active_codes': active_codes,
        }
        
        return TemplateResponse(request, 'admin/tickets/dashboard.html', context)

# Create custom admin site instance
tickets_admin_site = TicketsAdminSite(name='tickets_admin')

# Register models with custom admin site
tickets_admin_site.register(TicketCategory, TicketCategoryAdmin)
tickets_admin_site.register(Venue, VenueAdmin)
tickets_admin_site.register(Ticket, TicketAdmin)
tickets_admin_site.register(TicketPurchase, TicketPurchaseAdmin)
tickets_admin_site.register(TicketCode, TicketCodeAdmin)
tickets_admin_site.register(TicketReview, TicketReviewAdmin)
tickets_admin_site.register(TicketPromoCode, TicketPromoCodeAdmin)