from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid

User = get_user_model()

class StripeCustomer(models.Model):
    """Store Stripe customer information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stripe_customer')
    stripe_customer_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Stripe Customer: {self.user.email}"

class StripePaymentIntent(models.Model):
    """Store Stripe Payment Intent information"""
    STATUS_CHOICES = [
        ('requires_payment_method', 'Requires Payment Method'),
        ('requires_confirmation', 'Requires Confirmation'),
        ('requires_action', 'Requires Action'),
        ('processing', 'Processing'),
        ('requires_capture', 'Requires Capture'),
        ('canceled', 'Canceled'),
        ('succeeded', 'Succeeded'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stripe_payment_intents')
    booking = models.ForeignKey('destinations.Booking', on_delete=models.CASCADE, null=True, blank=True)
    stripe_payment_intent_id = models.CharField(max_length=100, unique=True)
    client_secret = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='requires_payment_method')
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Payment method details
    payment_method_id = models.CharField(max_length=100, blank=True)
    payment_method_type = models.CharField(max_length=50, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    succeeded_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['stripe_payment_intent_id']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"Payment Intent {self.stripe_payment_intent_id} - ${self.amount} ({self.status})"

class StripePaymentMethod(models.Model):
    """Store Stripe Payment Method information"""
    TYPE_CHOICES = [
        ('card', 'Card'),
        ('bank_account', 'Bank Account'),
        ('wallet', 'Wallet'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stripe_payment_methods')
    stripe_payment_method_id = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    
    # Card details (if type is card)
    card_brand = models.CharField(max_length=20, blank=True)
    card_last4 = models.CharField(max_length=4, blank=True)
    card_exp_month = models.IntegerField(null=True, blank=True)
    card_exp_year = models.IntegerField(null=True, blank=True)
    
    # Other payment method details
    details = models.JSONField(default=dict, blank=True)
    
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        if self.type == 'card':
            return f"{self.card_brand.title()} ending in {self.card_last4}"
        return f"{self.type.title()} Payment Method"

class StripeWebhookEvent(models.Model):
    """Store Stripe webhook events for processing"""
    stripe_event_id = models.CharField(max_length=100, unique=True)
    event_type = models.CharField(max_length=100)
    data = models.JSONField()
    processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['stripe_event_id']),
            models.Index(fields=['event_type', 'processed']),
            models.Index(fields=['processed', 'created_at']),
        ]
    
    def __str__(self):
        return f"Webhook {self.event_type} - {self.stripe_event_id}"

class StripeRefund(models.Model):
    """Store Stripe refund information"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('canceled', 'Canceled'),
    ]
    
    payment_intent = models.ForeignKey(StripePaymentIntent, on_delete=models.CASCADE, related_name='refunds')
    stripe_refund_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Refund {self.stripe_refund_id} - ${self.amount} ({self.status})"