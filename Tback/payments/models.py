from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class PaymentProvider(models.Model):
    """Payment providers like M-Pesa, Airtel Money, Stripe"""
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=20, unique=True)
    configuration = models.JSONField(default=dict, help_text="Provider-specific configuration")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('momo', 'Mobile Money'),
        ('card', 'Credit/Debit Card'),
        ('bank', 'Bank Transfer'),
        ('cash', 'Cash'),
        ('paystack', 'Paystack'),
    ]
    
    # Payment identification
    payment_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    reference = models.CharField(max_length=50, unique=True, blank=True)
    
    # Related models
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    booking = models.ForeignKey('destinations.Booking', on_delete=models.CASCADE, related_name='payments', null=True, blank=True)
    
    # Payment details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0'))])
    currency = models.CharField(max_length=3, default='GHS')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='momo')
    
    # Mobile Money specific fields
    provider = models.ForeignKey(PaymentProvider, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    
    # Payment status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    external_reference = models.CharField(max_length=100, blank=True)  # Provider's transaction ID
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Store additional payment info
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['reference']),
            models.Index(fields=['external_reference']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.reference:
            # Generate unique reference
            self.reference = f"PAY{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
    
    def log(self, level, message, data=None):
        """Create a log entry for this payment"""
        PaymentLog.objects.create(
            payment=self,
            level=level,
            message=message,
            data=data or {}
        )
    
    def __str__(self):
        return f"Payment {self.reference} - {self.currency} {self.amount} ({self.status})"

class PaymentCallback(models.Model):
    """Store payment callbacks from MoMo providers"""
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='callbacks')
    provider_reference = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    callback_data = models.JSONField()  # Store the full callback payload
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Callback for {self.payment.reference} - {self.status}"

class PaymentLog(models.Model):
    """Log all payment-related activities"""
    LOG_LEVELS = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('debug', 'Debug'),
    ]
    
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='logs')
    level = models.CharField(max_length=10, choices=LOG_LEVELS, default='info')
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.payment.reference} - {self.level.upper()}: {self.message[:50]}"