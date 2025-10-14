from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from decimal import Decimal
import uuid

class TicketCategory(models.Model):
    CATEGORY_TYPES = [
        ('event', 'Event'),
        ('transport', 'Transport'),
        ('attraction', 'Attraction'),
        ('experience', 'Experience'),
        ('accommodation', 'Accommodation'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Lucide icon name")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Ticket Categories"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Venue(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Ghana')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=500, blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    contact_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}, {self.city}"

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('sold_out', 'Sold Out'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
    ]
    
    TICKET_TYPES = [
        ('single', 'Single Entry'),
        ('multiple', 'Multiple Entry'),
        ('season', 'Season Pass'),
        ('group', 'Group Ticket'),
        ('vip', 'VIP Access'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(TicketCategory, on_delete=models.CASCADE, related_name='tickets')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='tickets', blank=True, null=True)
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES, default='single')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='GHS')
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    
    # Availability
    total_quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_quantity = models.PositiveIntegerField()
    min_purchase = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    max_purchase = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1)])
    
    # Dates and Times
    event_date = models.DateTimeField()
    event_end_date = models.DateTimeField(blank=True, null=True)
    sale_start_date = models.DateTimeField()
    sale_end_date = models.DateTimeField()
    
    # Media
    image = models.URLField(max_length=500, blank=True)
    gallery_images = models.JSONField(default=list, blank=True)
    
    # Features
    features = models.JSONField(default=list, blank=True, help_text="List of ticket features")
    terms_conditions = models.TextField(blank=True)
    cancellation_policy = models.TextField(blank=True)
    
    # SEO and Marketing
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    tags = models.JSONField(default=list, blank=True)
    
    # Status and Settings
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    is_refundable = models.BooleanField(default=True)
    requires_approval = models.BooleanField(default=False)
    
    # Analytics
    views_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    reviews_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['event_date']),
            models.Index(fields=['price']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['venue']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.available_quantity:
            self.available_quantity = self.total_quantity
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def is_available(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.status == 'published' and
            self.available_quantity > 0 and
            self.sale_start_date <= now <= self.sale_end_date
        )
    
    @property
    def is_sold_out(self):
        return self.available_quantity <= 0
    
    @property
    def discount_percentage(self):
        if self.discount_price and self.price > 0:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

class TicketPurchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
        ('used', 'Used'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Purchase Information
    purchase_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='purchases')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='ticket_purchases')
    
    # Quantity and Pricing
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Customer Information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Payment Information
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(blank=True, null=True)
    
    # Additional Information
    special_requests = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['ticket', 'status']),
            models.Index(fields=['payment_status']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Purchase {self.purchase_id} - {self.ticket.title}"
    
    def save(self, *args, **kwargs):
        if not self.total_amount:
            self.total_amount = (self.unit_price * self.quantity) - self.discount_applied
        super().save(*args, **kwargs)

class TicketCode(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('used', 'Used'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    purchase = models.ForeignKey(TicketPurchase, on_delete=models.CASCADE, related_name='ticket_codes')
    code = models.CharField(max_length=50, unique=True)
    qr_code_data = models.TextField(blank=True)
    
    # Usage Information
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    used_at = models.DateTimeField(blank=True, null=True)
    used_by = models.CharField(max_length=200, blank=True, help_text="Staff member who validated the ticket")
    
    # Validation
    is_transferable = models.BooleanField(default=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['status']),
            models.Index(fields=['purchase']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"TKT-{uuid.uuid4().hex[:8].upper()}"
        if not self.qr_code_data:
            self.qr_code_data = f"{self.purchase.purchase_id}:{self.code}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Ticket Code: {self.code}"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.status == 'active' and
            (not self.expires_at or self.expires_at > now)
        )

class TicketReview(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='ticket_reviews')
    purchase = models.ForeignKey(TicketPurchase, on_delete=models.CASCADE, related_name='reviews', blank=True, null=True)
    
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField()
    
    # Moderation
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['ticket', 'user']
        indexes = [
            models.Index(fields=['ticket', 'is_active']),
            models.Index(fields=['rating']),
        ]
    
    def __str__(self):
        return f"{self.user.first_name} - {self.ticket.title} ({self.rating} stars)"

class TicketPromoCode(models.Model):
    DISCOUNT_TYPES = [
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Discount Settings
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # Usage Limits
    usage_limit = models.PositiveIntegerField(blank=True, null=True, help_text="Total number of times this code can be used")
    usage_limit_per_user = models.PositiveIntegerField(default=1, help_text="Number of times a single user can use this code")
    used_count = models.PositiveIntegerField(default=0)
    
    # Validity
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    # Applicable Tickets
    applicable_tickets = models.ManyToManyField(Ticket, blank=True, related_name='promo_codes')
    applicable_categories = models.ManyToManyField(TicketCategory, blank=True, related_name='promo_codes')
    
    # Minimum Purchase Requirements
    minimum_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    minimum_quantity = models.PositiveIntegerField(default=1)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_until and
            (not self.usage_limit or self.used_count < self.usage_limit)
        )
    
    def calculate_discount(self, amount):
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value
        
        return min(discount, amount)  # Discount cannot exceed the total amount