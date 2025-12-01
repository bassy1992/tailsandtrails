from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import PaymentProvider, Payment, PaymentCallback, PaymentLog

@admin.register(PaymentProvider)
class PaymentProviderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active', 'payments_count', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Provider Information', {
            'fields': ('name', 'code', 'is_active')
        }),
        ('Configuration', {
            'fields': ('configuration',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def payments_count(self, obj):
        count = obj.payment_set.count()
        if count > 0:
            url = reverse('admin:payments_payment_changelist') + f'?provider__id__exact={obj.id}'
            return format_html('<a href="{}" style="color: #0066cc;">{} payments</a>', url, count)
        return '0 payments'
    payments_count.short_description = 'Payments'
    payments_count.admin_order_field = 'payment_count'

class PaymentCallbackInline(admin.TabularInline):
    model = PaymentCallback
    extra = 0
    readonly_fields = ('provider_reference', 'status', 'callback_data', 'processed', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

class PaymentLogInline(admin.TabularInline):
    model = PaymentLog
    extra = 0
    readonly_fields = ('level', 'message', 'data', 'created_at')
    can_delete = False
    ordering = ['-created_at']
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'reference', 'user_email', 'amount_display', 'payment_method_display', 
        'provider_name', 'status_display', 'phone_number', 'booking_type_display', 'created_at', 'processed_at'
    )
    list_filter = ('status', 'payment_method', 'provider', 'currency', 'created_at')
    search_fields = ('reference', 'user__email', 'phone_number', 'external_reference')
    readonly_fields = (
        'payment_id', 'reference', 'user', 'booking', 'amount', 'currency',
        'payment_method', 'provider', 'phone_number', 'status', 'external_reference',
        'description', 'metadata', 'created_at', 'updated_at', 'processed_at', 
        'booking_details_display'
    )
    inlines = [PaymentCallbackInline, PaymentLogInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('payment_id', 'reference', 'user', 'booking')
        }),
        ('Amount & Method', {
            'fields': ('amount', 'currency', 'payment_method', 'provider', 'phone_number')
        }),
        ('Status & Tracking', {
            'fields': ('status', 'external_reference', 'description')
        }),
        ('Booking Details', {
            'fields': ('booking_details_display',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        })
    )
    
    def user_email(self, obj):
        return obj.user.email if obj.user else 'Anonymous'
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'
    
    def booking_details_display(self, obj):
        """Display booking details in a formatted way"""
        if not obj.metadata or 'booking_details' not in obj.metadata:
            return format_html('<div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; color: #6c757d;"><em>No booking details available</em></div>')
        
        booking_details = obj.metadata.get('booking_details', {})
        
        html_parts = ['<div style="max-width: 800px;">']
        
        # User info (from payment record)
        user_info_html = self._get_user_info_html(obj)
        if user_info_html:
            html_parts.append(user_info_html)
        
        # Check if this is a ticket payment
        if booking_details.get('type') == 'ticket':
            # Display ticket-specific information
            ticket_info = booking_details.get('ticket', {})
            purchase_info = booking_details.get('purchase_info', {})
            
            html_parts.append(f"""
                <div style="margin-bottom: 15px; padding: 12px; background-color: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 5px;">
                    <h4 style="margin: 0 0 8px 0; color: #1976d2; font-size: 16px;">🎫 Ticket Information</h4>
                    <div style="font-size: 15px; font-weight: 600; margin-bottom: 4px;">{ticket_info.get('name', 'Event Ticket')}</div>
                    <div style="font-size: 13px; color: #666;">💰 Price: {ticket_info.get('currency', 'GHS')} {ticket_info.get('price', 0):,.2f} • 🎟️ Quantity: {ticket_info.get('quantity', 1)}</div>
                </div>
            """)
            
            if purchase_info:
                html_parts.append(f"""
                    <div style="margin-bottom: 15px; padding: 12px; background-color: #e8f5e8; border-left: 4px solid #4caf50; border-radius: 5px;">
                        <h4 style="margin: 0 0 8px 0; color: #388e3c; font-size: 16px;">📋 Purchase Details</h4>
                        <div style="margin-bottom: 6px;">
                            <span style="font-weight: 600; color: #333;">Purchase Date:</span> 
                            <span style="margin-left: 8px;">{purchase_info.get('purchase_date', 'N/A')}</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="font-weight: 600; color: #333;">Payment Method:</span> 
                            <span style="margin-left: 8px;">{purchase_info.get('payment_method', 'N/A')}</span>
                        </div>
                        <div style="margin-bottom: 6px;">
                            <span style="font-weight: 600; color: #333;">Total Amount:</span> 
                            <span style="margin-left: 8px; color: #4caf50; font-weight: 600;">{ticket_info.get('currency', 'GHS')} {purchase_info.get('total_amount', 0):,.2f}</span>
                        </div>
                    </div>
                """)
        
        # Destination info (for destination bookings)
        elif 'destination' in booking_details:
            dest = booking_details['destination']
            html_parts.append(f"""
                <div style="margin-bottom: 15px; padding: 12px; background-color: #e3f2fd; border-left: 4px solid #2196f3; border-radius: 5px;">
                    <h4 style="margin: 0 0 8px 0; color: #1976d2; font-size: 16px;">🏖️ Destination</h4>
                    <div style="font-size: 15px; font-weight: 600; margin-bottom: 4px;">{dest.get('name', 'N/A')}</div>
                    <div style="font-size: 13px; color: #666;">📍 {dest.get('location', 'N/A')} • ⏱️ {dest.get('duration', 'N/A')}</div>
                </div>
            """)
        
        # Travelers info
        if 'travelers' in booking_details:
            travelers = booking_details['travelers']
            html_parts.append(f"""
                <div style="margin-bottom: 15px; padding: 12px; background-color: #e8f5e8; border-left: 4px solid #4caf50; border-radius: 5px;">
                    <h4 style="margin: 0 0 8px 0; color: #388e3c; font-size: 16px;">👥 Travelers</h4>
                    <div style="font-size: 15px; font-weight: 600; margin-bottom: 4px;">{travelers.get('adults', 0)} Adults + {travelers.get('children', 0)} Children</div>
                    <div style="font-size: 13px; color: #666;">📅 Date: {booking_details.get('selected_date', 'N/A')}</div>
                </div>
            """)
        
        # Selected options
        if 'selected_options' in booking_details:
            options = booking_details['selected_options']
            html_parts.append(f"""
                <div style="margin-bottom: 15px; padding: 12px; background-color: #fff3e0; border-left: 4px solid #ff9800; border-radius: 5px;">
                    <h4 style="margin: 0 0 12px 0; color: #f57c00; font-size: 16px;">⚙️ Selected Options</h4>
            """)
            
            # Accommodation
            if 'accommodation' in options:
                acc = options['accommodation']
                price_text = '<span style="color: #4caf50; font-weight: 600;">Included</span>' if acc.get('is_default') else f'<span style="color: #4caf50; font-weight: 600;">GH₵{acc.get("price", 0):,.2f}</span>'
                html_parts.append(f"""
                    <div style="margin-bottom: 10px; padding: 8px; background-color: #fff; border-radius: 3px; border: 1px solid #e0e0e0;">
                        <div style="font-weight: 600; color: #333;">🏨 Accommodation</div>
                        <div style="margin-top: 2px;">{acc.get('name', 'N/A')} • {price_text}</div>
                    </div>
                """)
            
            # Transport
            if 'transport' in options:
                trans = options['transport']
                price_text = '<span style="color: #4caf50; font-weight: 600;">Included</span>' if trans.get('is_default') else f'<span style="color: #4caf50; font-weight: 600;">GH₵{trans.get("price", 0):,.2f}</span>'
                html_parts.append(f"""
                    <div style="margin-bottom: 10px; padding: 8px; background-color: #fff; border-radius: 3px; border: 1px solid #e0e0e0;">
                        <div style="font-weight: 600; color: #333;">🚐 Transport</div>
                        <div style="margin-top: 2px;">{trans.get('name', 'N/A')} • {price_text}</div>
                    </div>
                """)
            
            # Meals
            if 'meals' in options:
                meals = options['meals']
                price_text = '<span style="color: #4caf50; font-weight: 600;">Included</span>' if meals.get('is_default') else f'<span style="color: #4caf50; font-weight: 600;">GH₵{meals.get("price", 0):,.2f}</span>'
                html_parts.append(f"""
                    <div style="margin-bottom: 10px; padding: 8px; background-color: #fff; border-radius: 3px; border: 1px solid #e0e0e0;">
                        <div style="font-weight: 600; color: #333;">🍽️ Meals</div>
                        <div style="margin-top: 2px;">{meals.get('name', 'N/A')} • {price_text}</div>
                    </div>
                """)
            
            # Medical & Insurance
            if 'medical' in options:
                medical = options['medical']
                price_text = '<span style="color: #4caf50; font-weight: 600;">Included</span>' if medical.get('is_default') else f'<span style="color: #4caf50; font-weight: 600;">GH₵{medical.get("price", 0):,.2f}</span>'
                html_parts.append(f"""
                    <div style="margin-bottom: 10px; padding: 8px; background-color: #fff; border-radius: 3px; border: 1px solid #e0e0e0;">
                        <div style="font-weight: 600; color: #333;">🏥 Medical & Insurance</div>
                        <div style="margin-top: 2px;">{medical.get('name', 'N/A')} • {price_text}</div>
                    </div>
                """)
            
            # Additional Experiences
            if 'experiences' in options:
                experiences = options['experiences']
                if experiences:
                    html_parts.append(f"""
                        <div style="margin-bottom: 10px; padding: 8px; background-color: #fff; border-radius: 3px; border: 1px solid #e0e0e0;">
                            <div style="font-weight: 600; color: #333; margin-bottom: 6px;">🎯 Additional Experiences</div>
                    """)
                    for exp in experiences:
                        html_parts.append(f"""
                            <div style="margin-left: 15px; margin-bottom: 4px; font-size: 14px;">
                                • {exp.get('name', 'N/A')} • <span style="color: #4caf50; font-weight: 600;">GH₵{exp.get('price', 0):,.2f}</span>
                            </div>
                        """)
                    html_parts.append('</div>')
            
            html_parts.append('</div>')
        
        # Pricing breakdown
        if 'pricing' in booking_details:
            pricing = booking_details['pricing']
            html_parts.append(f"""
                <div style="margin-bottom: 15px; padding: 12px; background-color: #ffebee; border-left: 4px solid #f44336; border-radius: 5px;">
                    <h4 style="margin: 0 0 12px 0; color: #d32f2f; font-size: 16px;">💰 Pricing Breakdown</h4>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px; padding: 4px 0;">
                        <span style="font-weight: 500;">Base Total:</span>
                        <span style="font-weight: 600;">GH₵{pricing.get('base_total', 0):,.2f}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-bottom: 6px; padding: 4px 0;">
                        <span style="font-weight: 500;">Options Total:</span>
                        <span style="font-weight: 600;">GH₵{pricing.get('options_total', 0):,.2f}</span>
                    </div>
                    <div style="border-top: 2px solid #d32f2f; padding-top: 8px; margin-top: 8px;">
                        <div style="display: flex; justify-content: space-between; font-size: 16px;">
                            <span style="font-weight: 700;">Final Total:</span>
                            <span style="font-weight: 700; color: #d32f2f;">GH₵{pricing.get('final_total', 0):,.2f}</span>
                        </div>
                    </div>
                </div>
            """)
        
        html_parts.append('</div>')
        
        if len(html_parts) <= 2:  # Only opening and closing div
            return format_html('<div style="padding: 10px; background-color: #f8f9fa; border-radius: 5px; color: #6c757d;"><em>No booking details found in metadata</em></div>')
        
        return format_html(''.join(html_parts))
    
    booking_details_display.short_description = 'Booking Details'
    
    def _get_user_info_html(self, obj):
        """Get user information HTML for booking details"""
        user_name = "Anonymous User"
        user_email = "Not provided"
        phone_number = obj.phone_number or "Not provided"
        
        # Get user info from the payment's user field
        if obj.user:
            user_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
            if not user_name:
                user_name = obj.user.username or "User"
            user_email = obj.user.email or "Not provided"
        
        # Also check if user info is stored in booking details metadata
        if obj.metadata and 'booking_details' in obj.metadata:
            booking_details = obj.metadata['booking_details']
            if 'user_info' in booking_details:
                user_info = booking_details['user_info']
                user_name = user_info.get('name', user_name)
                user_email = user_info.get('email', user_email)
                phone_number = user_info.get('phone', phone_number)
        
        return f"""
            <div style="margin-bottom: 15px; padding: 12px; background-color: #f3e5f5; border-left: 4px solid #9c27b0; border-radius: 5px;">
                <h4 style="margin: 0 0 8px 0; color: #7b1fa2; font-size: 16px;">👤 Customer Information</h4>
                <div style="margin-bottom: 6px;">
                    <span style="font-weight: 600; color: #333;">Name:</span> 
                    <span style="margin-left: 8px;">{user_name}</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="font-weight: 600; color: #333;">Email:</span> 
                    <span style="margin-left: 8px;">{user_email}</span>
                </div>
                <div style="margin-bottom: 6px;">
                    <span style="font-weight: 600; color: #333;">Phone:</span> 
                    <span style="margin-left: 8px;">{phone_number}</span>
                </div>
            </div>
        """
    
    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount}"
    amount_display.short_description = 'Amount'
    amount_display.admin_order_field = 'amount'
    
    def payment_method_display(self, obj):
        method_icons = {
            'momo': '📱',
            'mobile_money': '📱',
            'card': '💳',
            'bank': '🏦',
            'cash': '💵'
        }
        icon = method_icons.get(obj.payment_method, '💰')
        return f"{icon} {obj.get_payment_method_display()}"
    payment_method_display.short_description = 'Payment Method'
    payment_method_display.admin_order_field = 'payment_method'
    
    def provider_name(self, obj):
        if obj.provider:
            if obj.provider.code == 'mtn_momo':
                return f"🇬🇭 {obj.provider.name}"
            return obj.provider.name
        return '-'
    provider_name.short_description = 'Provider'
    provider_name.admin_order_field = 'provider__name'
    
    def status_display(self, obj):
        colors = {
            'pending': '#fbbf24',      # Yellow
            'processing': '#3b82f6',   # Blue
            'successful': '#10b981',   # Green
            'failed': '#ef4444',       # Red
            'cancelled': '#6b7280',    # Gray
            'refunded': '#8b5cf6'      # Purple
        }
        
        icons = {
            'pending': '⏳',
            'processing': '⚡',
            'successful': '✅',
            'failed': '❌',
            'cancelled': '🚫',
            'refunded': '↩️'
        }
        
        color = colors.get(obj.status, '#6b7280')
        icon = icons.get(obj.status, '❓')
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    status_display.admin_order_field = 'status'
    
    def booking_type_display(self, obj):
        """Display the type of booking to help identify tickets vs destinations"""
        # First check if this is a ticket payment by description
        if obj.description and "Ticket Purchase:" in obj.description:
            return format_html(
                '<span style="background-color: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">🎫 TICKET</span>'
            )
        
        if obj.metadata and 'booking_details' in obj.metadata:
            booking_details = obj.metadata['booking_details']
            
            # Check if this is explicitly marked as a ticket
            if booking_details.get('type') == 'ticket':
                return format_html(
                    '<span style="background-color: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">🎫 TICKET</span>'
                )
            
            # Check if this looks like a ticket purchase (legacy format)
            if any(key in booking_details for key in ['eventName', 'ticketType', 'ticketReference', 'eventDetails', 'ticket']):
                return format_html(
                    '<span style="background-color: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">🎫 TICKET</span>'
                )
            
            # Check if this is a destination booking (correct place)
            if 'destination' in booking_details:
                return format_html(
                    '<span style="background-color: #e8f5e8; color: #2e7d32; padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;">🏝️ DESTINATION</span>'
                )
        
        # Default for unclear bookings
        return format_html(
            '<span style="background-color: #f5f5f5; color: #666; padding: 4px 8px; border-radius: 4px; font-size: 11px;">❓ UNKNOWN</span>'
        )
    booking_type_display.short_description = 'Booking Type'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'provider', 'booking')
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion of all payments - no protection"""
        return True
    
    def has_change_permission(self, request, obj=None):
        """Allow viewing but all fields are read-only"""
        return True
    
    # Custom actions
    actions = ['mark_as_successful', 'mark_as_failed', 'mark_as_cancelled']
    
    def mark_as_successful(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'processing']).update(status='successful')
        self.message_user(request, f'{updated} payments marked as successful.')
    mark_as_successful.short_description = "Mark selected payments as successful"
    
    def mark_as_failed(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'processing']).update(status='failed')
        self.message_user(request, f'{updated} payments marked as failed.')
    mark_as_failed.short_description = "Mark selected payments as failed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.filter(status__in=['pending', 'processing']).update(status='cancelled')
        self.message_user(request, f'{updated} payments marked as cancelled.')
    mark_as_cancelled.short_description = "Mark selected payments as cancelled"

@admin.register(PaymentCallback)
class PaymentCallbackAdmin(admin.ModelAdmin):
    list_display = ('payment_reference', 'provider_name', 'status', 'processed', 'created_at')
    list_filter = ('status', 'processed', 'created_at', 'payment__provider')
    search_fields = ('payment__reference', 'provider_reference')
    readonly_fields = ('payment', 'provider_reference', 'status', 'callback_data', 'created_at')
    date_hierarchy = 'created_at'
    
    def payment_reference(self, obj):
        url = reverse('admin:payments_payment_change', args=[obj.payment.id])
        return format_html('<a href="{}">{}</a>', url, obj.payment.reference)
    payment_reference.short_description = 'Payment Reference'
    payment_reference.admin_order_field = 'payment__reference'
    
    def provider_name(self, obj):
        if obj.payment.provider:
            if obj.payment.provider.code == 'mtn_momo':
                return f"🇬🇭 {obj.payment.provider.name}"
            return obj.payment.provider.name
        return '-'
    provider_name.short_description = 'Provider'
    provider_name.admin_order_field = 'payment__provider__name'
    
    def has_add_permission(self, request):
        return False

@admin.register(PaymentLog)
class PaymentLogAdmin(admin.ModelAdmin):
    list_display = ('payment_reference', 'level_display', 'message_short', 'created_at')
    list_filter = ('level', 'created_at', 'payment__provider')
    search_fields = ('payment__reference', 'message')
    readonly_fields = ('payment', 'level', 'message', 'data', 'created_at')
    date_hierarchy = 'created_at'
    
    def payment_reference(self, obj):
        url = reverse('admin:payments_payment_change', args=[obj.payment.id])
        return format_html('<a href="{}">{}</a>', url, obj.payment.reference)
    payment_reference.short_description = 'Payment Reference'
    payment_reference.admin_order_field = 'payment__reference'
    
    def level_display(self, obj):
        colors = {
            'info': '#3b82f6',      # Blue
            'warning': '#fbbf24',   # Yellow
            'error': '#ef4444',     # Red
            'debug': '#6b7280'      # Gray
        }
        
        icons = {
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '🚨',
            'debug': '🔍'
        }
        
        color = colors.get(obj.level, '#6b7280')
        icon = icons.get(obj.level, '📝')
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color,
            icon,
            obj.level.upper()
        )
    level_display.short_description = 'Level'
    level_display.admin_order_field = 'level'
    
    def message_short(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_short.short_description = 'Message'
    
    def has_add_permission(self, request):
        return False

# Customize admin site header
admin.site.site_header = "Trails & Trails - MoMo Payments Admin"
admin.site.site_title = "MoMo Payments Admin"
admin.site.index_title = "Mobile Money Payment Management"
