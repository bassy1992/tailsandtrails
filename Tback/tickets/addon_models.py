from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid

class AddOnCategory(models.Model):
    """Categories for organizing add-ons"""
    CATEGORY_TYPES = [
        ('accommodation', 'Accommodation'),
        ('transport', 'Transport'),
        ('meals', 'Meals'),
        ('medical', 'Medical & Insurance'),
        ('experience', 'Experience'),
        ('equipment', 'Equipment'),
        ('service', 'Service'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide icon name")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Add-On Categories"
    
    def __str__(self):
        return self.name

class AddOn(models.Model):
    """Add-on services that can be added to bookings"""
    ADDON_TYPES = [
        ('single', 'Single Selection'),
        ('multiple', 'Multiple Options'),
        ('checkbox', 'Optional Add-on'),
    ]
    
    PRICING_TYPES = [
        ('fixed', 'Fixed Price'),
        ('per_person', 'Per Person'),
        ('per_group', 'Per Group'),
        ('percentage', 'Percentage of Base Price'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(AddOnCategory, on_delete=models.CASCADE, related_name='addons')
    addon_type = models.CharField(max_length=20, choices=ADDON_TYPES, default='checkbox')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    pricing_type = models.CharField(max_length=20, choices=PRICING_TYPES, default='fixed')
    currency = models.CharField(max_length=3, default='GHS')
    
    # Availability
    is_required = models.BooleanField(default=False, help_text="If true, this add-on must be selected")
    is_default = models.BooleanField(default=False, help_text="If true, this add-on is selected by default")
    max_quantity = models.PositiveIntegerField(default=1, help_text="Maximum quantity per booking")
    
    # Applicable to
    applicable_tickets = models.ManyToManyField('Ticket', blank=True, related_name='available_addons')
    applicable_categories = models.ManyToManyField('TicketCategory', blank=True, related_name='available_addons')
    
    # Media and Details
    image = models.ImageField(upload_to='addons/', blank=True, null=True)
    features = models.JSONField(default=list, blank=True, help_text="List of features/benefits")
    terms_conditions = models.TextField(blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category__order', 'order', 'name']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['is_active', 'order']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.category.name})"
    
    def calculate_price(self, base_amount=0, quantity=1, travelers=1):
        """Calculate the price based on pricing type"""
        if self.pricing_type == 'fixed':
            return self.base_price * quantity
        elif self.pricing_type == 'per_person':
            return self.base_price * travelers * quantity
        elif self.pricing_type == 'per_group':
            return self.base_price * quantity
        elif self.pricing_type == 'percentage':
            return (base_amount * self.base_price / 100) * quantity
        return self.base_price * quantity

class AddOnOption(models.Model):
    """Individual options for add-ons that have multiple choices"""
    addon = models.ForeignKey(AddOn, on_delete=models.CASCADE, related_name='options')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        unique_together = ['addon', 'name']
    
    def __str__(self):
        return f"{self.addon.name} - {self.name}"

class BookingAddOn(models.Model):
    """Selected add-ons for a specific booking"""
    booking_reference = models.CharField(max_length=100, help_text="Reference to the main booking")
    addon = models.ForeignKey(AddOn, on_delete=models.CASCADE)
    option = models.ForeignKey(AddOnOption, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Customer details (for cases where booking is not tied to a user account)
    customer_name = models.CharField(max_length=200, blank=True)
    customer_email = models.EmailField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['booking_reference']),
            models.Index(fields=['customer_email']),
        ]
    
    def __str__(self):
        return f"Booking {self.booking_reference} - {self.addon.name}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)