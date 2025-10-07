from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    StripeCustomer, StripePaymentIntent, StripePaymentMethod, 
    StripeWebhookEvent, StripeRefund
)

@admin.register(StripeCustomer)
class StripeCustomerAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'stripe_customer_id', 'payment_intents_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'stripe_customer_id')
    readonly_fields = ('stripe_customer_id', 'created_at', 'updated_at')
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def payment_intents_count(self, obj):
        count = obj.user.stripe_payment_intents.count()
        if count > 0:
            url = reverse('admin:stripe_payments_stripepaymentintent_changelist') + f'?user__id__exact={obj.user.id}'
            return format_html('<a href="{}">{} intents</a>', url, count)
        return '0 intents'
    payment_intents_count.short_description = 'Payment Intents'

class StripeRefundInline(admin.TabularInline):
    model = StripeRefund
    extra = 0
    readonly_fields = ('stripe_refund_id', 'amount', 'currency', 'status', 'reason', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False

@admin.register(StripePaymentIntent)
class StripePaymentIntentAdmin(admin.ModelAdmin):
    list_display = (
        'stripe_payment_intent_id', 'user_email', 'amount_display', 
        'status_display', 'booking_reference', 'created_at', 'succeeded_at'
    )
    list_filter = ('status', 'currency', 'created_at', 'succeeded_at')
    search_fields = ('stripe_payment_intent_id', 'user__email', 'booking__reference')
    readonly_fields = (
        'stripe_payment_intent_id', 'client_secret', 'payment_method_id',
        'created_at', 'updated_at', 'confirmed_at', 'succeeded_at'
    )
    inlines = [StripeRefundInline]
    
    fieldsets = (
        ('Payment Intent Information', {
            'fields': ('stripe_payment_intent_id', 'user', 'booking', 'client_secret')
        }),
        ('Amount & Currency', {
            'fields': ('amount', 'currency', 'description')
        }),
        ('Status & Payment Method', {
            'fields': ('status', 'payment_method_id', 'payment_method_type')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'succeeded_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        })
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount}"
    amount_display.short_description = 'Amount'
    
    def status_display(self, obj):
        colors = {
            'requires_payment_method': '#6b7280',
            'requires_confirmation': '#fbbf24',
            'requires_action': '#f59e0b',
            'processing': '#3b82f6',
            'requires_capture': '#8b5cf6',
            'canceled': '#6b7280',
            'succeeded': '#10b981',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def booking_reference(self, obj):
        return obj.booking.reference if obj.booking else '-'
    booking_reference.short_description = 'Booking'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'booking')

@admin.register(StripePaymentMethod)
class StripePaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user_email', 'type', 'is_default', 'created_at')
    list_filter = ('type', 'is_default', 'card_brand', 'created_at')
    search_fields = ('user__email', 'stripe_payment_method_id', 'card_last4')
    readonly_fields = (
        'stripe_payment_method_id', 'type', 'card_brand', 'card_last4',
        'card_exp_month', 'card_exp_year', 'details', 'created_at'
    )
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    
    def display_name(self, obj):
        if obj.type == 'card':
            return f"{obj.card_brand.title()} ending in {obj.card_last4}"
        return f"{obj.type.title()} Payment Method"
    display_name.short_description = 'Payment Method'

@admin.register(StripeWebhookEvent)
class StripeWebhookEventAdmin(admin.ModelAdmin):
    list_display = ('stripe_event_id', 'event_type', 'processed', 'created_at', 'processed_at')
    list_filter = ('event_type', 'processed', 'created_at')
    search_fields = ('stripe_event_id', 'event_type')
    readonly_fields = ('stripe_event_id', 'event_type', 'data', 'created_at', 'processed_at')
    
    fieldsets = (
        ('Event Information', {
            'fields': ('stripe_event_id', 'event_type', 'processed', 'processed_at')
        }),
        ('Processing', {
            'fields': ('processing_error',)
        }),
        ('Event Data', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def has_add_permission(self, request):
        return False

@admin.register(StripeRefund)
class StripeRefundAdmin(admin.ModelAdmin):
    list_display = (
        'stripe_refund_id', 'payment_intent_id', 'amount_display', 
        'status_display', 'reason', 'created_at'
    )
    list_filter = ('status', 'reason', 'currency', 'created_at')
    search_fields = ('stripe_refund_id', 'payment_intent__stripe_payment_intent_id')
    readonly_fields = (
        'stripe_refund_id', 'payment_intent', 'amount', 'currency', 
        'status', 'reason', 'created_at', 'updated_at'
    )
    
    def payment_intent_id(self, obj):
        return obj.payment_intent.stripe_payment_intent_id
    payment_intent_id.short_description = 'Payment Intent ID'
    
    def amount_display(self, obj):
        return f"{obj.currency} {obj.amount}"
    amount_display.short_description = 'Amount'
    
    def status_display(self, obj):
        colors = {
            'pending': '#fbbf24',
            'succeeded': '#10b981',
            'failed': '#ef4444',
            'canceled': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def has_add_permission(self, request):
        return False
